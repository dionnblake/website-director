"""Reference real-browser BROWSER_QA_ENGINE built on Playwright.

Used to verify generated Website Director projects. Requires ``playwright`` and
its browser binaries (``python -m playwright install chromium``). When either is
absent, ``available()`` returns ``False`` and the runner records the affected
checks as ``BLOCKED`` with a specific reason -- it never silently downgrades to
a PASS (protocol sec 38).

This engine follows IMPECCABLE-ENGINE-PROTOCOL.md sec 8: no persistent browser
daemon. A context is launched per ``observe`` group and torn down in ``stop()``.
A local static file server (if needed) is ephemeral and killed in ``stop()``.
"""

from __future__ import annotations

import contextlib
import functools
import http.server
import os
import socket
import threading
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

from .base import (
    APPLICATION_DEFECT,
    THIRD_PARTY_DEFECT,
    AnalyticsEvent,
    BrowserQAEngine,
    ConsoleMessage,
    KeyboardTrace,
    LayoutMetrics,
    ApplicationObservation,
    LocalizationObservation,
    NetworkRequest,
    PageObservation,
    PerfSample,
    SecurityObservation,
)

try:  # pragma: no cover - availability probe
    from playwright.sync_api import sync_playwright  # type: ignore
    _HAS_PLAYWRIGHT = True
except Exception:  # noqa: BLE001
    _HAS_PLAYWRIGHT = False


_SECRET_TOKENS = ("AKIA", "sk_live_", "ghp_", "-----BEGIN", "AIza", "xoxb-", "service_account")


class PlaywrightEngine(BrowserQAEngine):
    name = "playwright"
    supports_real_browser = True

    def __init__(self, project_root: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(project_root, config)
        self._pw = None
        self._server: Optional[http.server.ThreadingHTTPServer] = None
        self._server_thread: Optional[threading.Thread] = None
        self.base_url: str = (self.config or {}).get("base_url", "")

    def available(self) -> bool:
        return _HAS_PLAYWRIGHT

    # -- lifecycle ----------------------------------------------------
    def start(self) -> None:
        if not self.available():
            raise RuntimeError("playwright is not installed; run: python -m playwright install chromium")
        serve_dir = (self.config or {}).get("serve_dir")
        if serve_dir and not self.base_url:
            self._start_static_server(os.path.join(self.project_root, serve_dir))
        self._pw = sync_playwright().start()

    def stop(self) -> None:
        with contextlib.suppress(Exception):
            if self._pw:
                self._pw.stop()
        self._pw = None
        if self._server:
            with contextlib.suppress(Exception):
                self._server.shutdown()
                self._server.server_close()
            self._server = None
        if self._server_thread:
            self._server_thread.join(timeout=5)
            self._server_thread = None

    def _start_static_server(self, directory: str) -> None:
        sock = socket.socket()
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.close()
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
        self._server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
        self._server_thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._server_thread.start()
        self.base_url = "http://127.0.0.1:%d" % port

    def _url_for(self, route: str) -> str:
        if route.startswith("http://") or route.startswith("https://"):
            return route
        if self.base_url:
            return urljoin(self.base_url + "/", route.lstrip("/"))
        return "file://" + os.path.join(self.project_root, route.lstrip("/\\"))

    # -- observation ------------------------------------------------
    def observe(self, route: str, viewport: int, *, reduced_motion: bool = False,
                browser: str = "chromium", interactions: Optional[List[Dict[str, Any]]] = None,
                ) -> PageObservation:
        assert self._pw is not None, "PlaywrightEngine.start() was not called"
        btype = {"chromium": self._pw.chromium, "firefox": self._pw.firefox,
                 "webkit": self._pw.webkit}[browser]
        b = btype.launch(headless=True)
        obs = PageObservation(route=route, viewport=viewport, engine=self.name,
                              browser=browser, reduced_motion=reduced_motion)
        try:
            ctx = b.new_context(
                viewport={"width": viewport, "height": 900},
                reduced_motion="reduce" if reduced_motion else "no-preference",
                device_scale_factor=1,
            )
            page = ctx.new_page()
            net: List[NetworkRequest] = []
            page.on("console", lambda m: obs.console.append(ConsoleMessage(
                level=m.type, text=m.text,
                classification=THIRD_PARTY_DEFECT if _is_third_party(m.location.get("url", ""), route)
                else APPLICATION_DEFECT)))
            page.on("pageerror", lambda e: obs.console.append(
                ConsoleMessage(level="error", text=str(e), classification=APPLICATION_DEFECT)))
            page.on("response", lambda r: net.append(NetworkRequest(
                url=r.url, status=r.status, resource_type=r.request.resource_type,
                ok=r.ok, third_party=_is_third_party(r.url, route))))

            target = self._url_for(route)
            resp = page.goto(target, wait_until="networkidle")
            for step in (interactions or []):
                _apply_interaction(page, step)

            obs.final_url = page.url
            obs.title = page.title()
            obs.network = net
            obs.broken_assets = [n.url for n in net if not n.ok and n.resource_type in
                                 ("image", "font", "script", "stylesheet") and not n.blocked_allowed]

            metrics = page.evaluate(
                """() => {
                    const de = document.documentElement, b = document.body;
                    const cta = document.querySelector('[data-qa="primary-cta"], .primary-cta, a.cta');
                    const r = cta && cta.getBoundingClientRect();
                    return {
                        sw: de.scrollWidth, cw: de.clientWidth, bw: b ? b.getBoundingClientRect().width : de.clientWidth,
                        ctaVisible: !!(r && r.width > 0 && r.height > 0 && r.bottom > 0 && r.top < innerHeight * 3)
                    };
                }""")
            obs.layout = LayoutMetrics(
                viewport_width=viewport, document_scroll_width=int(metrics["sw"]),
                client_width=int(metrics["cw"]), body_width=int(metrics["bw"]),
                has_horizontal_overflow=int(metrics["sw"]) > int(metrics["cw"]) + 1,
                primary_cta_visible=bool(metrics["ctaVisible"]))

            obs.images_zero_dimension = page.evaluate(
                """() => [...document.images].filter(i => i.complete && i.naturalWidth === 0)
                        .map(i => i.currentSrc || i.src)""")
            obs.placeholder_hash_links = page.evaluate(
                """() => [...document.querySelectorAll('a[href="#"], a[href=""]')]
                        .filter(a => !a.hasAttribute('data-qa-intentional-hash'))
                        .map(a => a.textContent.trim().slice(0, 40))""")

            secret_hits = page.evaluate(
                """(tokens) => {
                    const html = document.documentElement.outerHTML;
                    return tokens.filter(t => html.includes(t));
                }""", list(_SECRET_TOKENS))
            obs.security = SecurityObservation(
                is_https=urlparse(page.url).scheme == "https",
                mixed_content_urls=[n.url for n in net if n.url.startswith("http://")
                                    and urlparse(page.url).scheme == "https"],
                dom_secret_hits=secret_hits,
                third_party_scripts=sorted({n.url for n in net if n.resource_type == "script"
                                            and _is_third_party(n.url, page.url)}),
                response_headers=dict(resp.headers) if resp else {})

            perf = page.evaluate(
                """() => {
                    const nav = performance.getEntriesByType('navigation')[0] || {};
                    const lcp = performance.getEntriesByType('largest-contentful-paint').pop();
                    let cls = 0;
                    for (const e of performance.getEntriesByType('layout-shift') || []) {
                        if (!e.hadRecentInput) cls += e.value;
                    }
                    return { lcp: lcp ? lcp.startTime : (nav.responseEnd || null), cls };
                }""")
            obs.perf = PerfSample(lcp_ms=perf.get("lcp"), cls=perf.get("cls"),
                                  measurement_kind="SYNTHETIC")

            shot = page.screenshot(full_page=False)
            obs.render_signature = __import__("hashlib").sha256(shot).hexdigest()[:16]
            obs.raw["screenshot_bytes"] = shot

            obs.keyboard = _keyboard_trace(page)

            if (self.config or {}).get("localization") or (self.config or {}).get("run_localization"):
                obs.localization = self._localization_scan(page, resp)

            if (self.config or {}).get("application") or (self.config or {}).get("run_application"):
                obs.application = self._application_scan(page)

            if (self.config or {}).get("accessibility") or (self.config or {}).get("run_axe"):
                obs.a11y = self._axe_scan(page)

            ctx.close()
        finally:
            b.close()
        return obs

    def _axe_scan(self, page) -> "AccessibilityObservation":
        """Best-effort axe-core run. axe-core is a replaceable engine, not policy
        (ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md §31). If axe cannot be injected,
        engine_status is ENGINE_UNAVAILABLE and the assertion records BLOCKED — never PASS."""
        from .base import AccessibilityObservation, A11yViolation

        a = AccessibilityObservation()
        # baseline DOM facts that need no engine
        facts = page.evaluate(
            """() => ({
                lang: document.documentElement.lang || '',
                title: document.title || '',
                h1: document.querySelectorAll('h1').length,
                landmarks: [...new Set([...document.querySelectorAll(
                    'header,nav,main,footer,[role=banner],[role=navigation],[role=main],[role=contentinfo]')]
                    .map(e => e.tagName.toLowerCase().replace('div','') ||
                              (e.getAttribute('role')||'').replace('banner','header')
                                .replace('navigation','nav').replace('contentinfo','footer')))].filter(Boolean),
                skipLink: !!document.querySelector('a[href^="#"]:first-child, a.skip-link, a[href="#main"]'),
                unlabelled: [...document.querySelectorAll('input:not([type=hidden]),select,textarea')]
                    .filter(el => !el.labels?.length && !el.getAttribute('aria-label')
                                  && !el.getAttribute('aria-labelledby') && !el.closest('label'))
                    .map(el => el.name || el.id || el.tagName).slice(0, 20),
                noName: [...document.querySelectorAll('button,a[href],[role=button]')]
                    .filter(el => !(el.textContent||'').trim() && !el.getAttribute('aria-label')
                                  && !el.getAttribute('aria-labelledby') && !el.querySelector('img[alt]:not([alt=""])'))
                    .map(el => el.outerHTML.slice(0, 60)).slice(0, 20)
            })""")
        a.page_lang = facts["lang"]
        a.page_title = facts["title"]
        a.h1_count = int(facts["h1"])
        a.landmarks = list(facts["landmarks"])
        a.skip_link_present = bool(facts["skipLink"])
        a.unlabelled_field_refs = list(facts["unlabelled"])
        a.missing_accessible_name_refs = list(facts["noName"])

        axe_path = os.path.join(self.project_root, "..", "browser-qa", "vendor", "axe.min.js")
        axe_path = os.path.normpath(axe_path)
        if not os.path.isfile(axe_path):
            for cand in [os.path.join(os.path.dirname(__file__), "..", "vendor", "axe.min.js")]:
                if os.path.isfile(os.path.normpath(cand)):
                    axe_path = os.path.normpath(cand)
                    break
        try:
            if not os.path.isfile(axe_path):
                raise FileNotFoundError(axe_path)
            page.add_script_tag(path=axe_path)
            result = page.evaluate("async () => await axe.run(document, "
                                   "{ runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag21aa','wcag22aa'] } })")
            a.engine_name = "axe-core"
            a.engine_version = page.evaluate("() => (window.axe && axe.version) || null")
            a.engine_status = "RAN"
            for v in result.get("violations", []):
                for node in v.get("nodes", [{}]):
                    a.violations.append(A11yViolation(
                        rule_id=v.get("id", ""), impact=v.get("impact") or "moderate",
                        wcag=",".join(t for t in v.get("tags", []) if t.startswith("wcag")),
                        target=";".join(node.get("target", [])), help_text=v.get("help", "")))
        except Exception as exc:  # noqa: BLE001
            a.engine_name = "axe-core"
            a.engine_status = "ENGINE_UNAVAILABLE"
            a.violations = []
            a.__dict__["_engine_error"] = str(exc)
        return a

    def _application_scan(self, page) -> "ApplicationObservation":
        """Collect explicit application QA hooks without guessing intent.

        Generated projects may expose boolean facts on a
        ``[data-qa-application]`` element or the document root. Absent hooks
        remain ``None`` so required assertions fail closed.
        """
        from .base import ApplicationObservation

        facts = page.evaluate(
            """() => {
                const root = document.documentElement;
                const marker = document.querySelector('[data-qa-application]') || root;
                const bool = name => {
                    const value = marker.getAttribute('data-qa-' + name);
                    if (value === null) return null;
                    return !['false', '0', 'no', 'fail'].includes(value.toLowerCase());
                };
                return {
                    authenticated: bool('authenticated'),
                    authorization_enforced: bool('authorization-enforced'),
                    object_access_allowed: bool('object-access-allowed'),
                    client_role_trusted: bool('client-role-trusted'),
                    password_plaintext: bool('password-plaintext'),
                    password_hash_exposed: bool('password-hash-exposed'),
                    account_recovery_defined: bool('account-recovery-defined'),
                    admin_route_server_protected: bool('admin-route-server-protected'),
                    client_price_trusted: bool('client-price-trusted'),
                    canonical_price_verified: bool('canonical-price-verified'),
                    checkout_click_marks_paid: bool('checkout-click-marks-paid'),
                    payment_confirmed: bool('payment-confirmed'),
                    webhook_signature_verified: bool('webhook-signature-verified'),
                    webhook_idempotent: bool('webhook-idempotent'),
                    duplicate_side_effect_created: bool('duplicate-side-effect-created'),
                    raw_card_stored: bool('raw-card-stored'),
                    hosted_or_tokenized_payment: bool('hosted-or-tokenized-payment'),
                    subscription_entitlement_granted: bool('subscription-entitlement-granted'),
                    entitlement_revoked_on_payment_failure: bool('entitlement-revoked-on-payment-failure'),
                    digital_shipping_unnecessary: bool('digital-shipping-unnecessary'),
                    physical_shipping_defined: bool('physical-shipping-defined'),
                    booking_overlap_prevented: bool('booking-overlap-prevented'),
                    booking_timezone_explicit: bool('booking-timezone-explicit'),
                    upload_allowlist_enforced: bool('upload-allowlist-enforced'),
                    executable_upload_accepted: bool('executable-upload-accepted'),
                    private_storage_authorized: bool('private-storage-authorized'),
                    private_file_public: bool('private-file-public'),
                    ugc_sanitized: bool('ugc-sanitized'),
                    ugc_script_executed: bool('ugc-script-executed'),
                    transactional_email_failure_visible: bool('transactional-email-failure-visible'),
                    transactional_email_failure_reported_success: bool('transactional-email-failure-reported-success'),
                    integration_inventory_complete: bool('integration-inventory-complete'),
                    application_secret_exposed: bool('application-secret-exposed'),
                    purchase_event_authoritative: bool('purchase-event-authoritative'),
                    purchase_event_from_click: bool('purchase-event-from-click'),
                    canonical_event_with_locale: bool('canonical-event-with-locale'),
                    private_route_indexable: bool('private-route-indexable'),
                    provider_available: bool('provider-available'),
                    live_payment_attempted: bool('live-payment-attempted'),
                    live_user_created: bool('live-user-created')
                };
            }""")
        return ApplicationObservation(**facts, raw=facts)

    def _localization_scan(self, page, response) -> "LocalizationObservation":
        """Collect only browser-observable localization facts.

        The page may expose explicit ``data-*`` QA hooks for facts such as
        fallback and translation metadata. Unknown authoring intent is not
        guessed; the assertion catalogue remains the authority for whether a
        plan requires each fact.
        """
        facts = page.evaluate(
            """() => {
                const root = document.documentElement;
                const text = el => (el.getAttribute('aria-label') || el.textContent || '').trim();
                const attrBool = (el, name, fallback) => {
                    const value = el && el.getAttribute(name);
                    if (value === null) return fallback;
                    return !['false', '0', 'no'].includes(value.toLowerCase());
                };
                const switcher = document.querySelector(
                    '[data-locale-switcher], [data-language-switcher], ' +
                    '[aria-label*="language" i], [aria-label*="locale" i]');
                const items = switcher ? [...switcher.querySelectorAll(
                    'a,button,[role="option"],[role="menuitem"]')] : [];
                const forms = [...document.querySelectorAll('form')];
                const localizedNodes = [...document.querySelectorAll(
                    '[data-i18n], [data-i18n-key], [data-localized]')];
                const ratios = localizedNodes.map(el => {
                    const sourceLength = Number(el.getAttribute('data-source-length'));
                    const currentLength = (el.textContent || '').trim().length;
                    return sourceLength > 0 ? currentLength / sourceLength : 1;
                }).filter(Number.isFinite);
                const alternate = [...document.querySelectorAll(
                    'link[rel="alternate"][hreflang]')].map(link => ({
                    hreflang: link.getAttribute('hreflang') || '',
                    url: link.href || link.getAttribute('href') || '',
                    reciprocal: attrBool(link, 'data-reciprocal', false),
                    self: attrBool(link, 'data-self', false),
                    x_default: (link.getAttribute('hreflang') || '').toLowerCase() === 'x-default'
                }));
                const canonicalLink = document.querySelector('link[rel="canonical"]');
                const canonical = canonicalLink ? (canonicalLink.href || canonicalLink.getAttribute('href') || '') : '';
                const currentUrl = location.href.split('#')[0];
                const canonicalUrl = canonical.split('#')[0];
                const overflow = localizedNodes.filter(el => el.scrollWidth > el.clientWidth + 1)
                    .map(el => el.getAttribute('data-i18n') || el.getAttribute('data-i18n-key') || el.tagName);
                const rootFallback = root.getAttribute('data-locale-fallback');
                const rootLocale = root.getAttribute('data-locale') || root.lang || '';
                return {
                    locale: rootLocale,
                    html_lang: root.lang || '',
                    html_dir: root.getAttribute('dir') ||
                        (getComputedStyle(root).direction === 'rtl' ? 'rtl' : 'ltr'),
                    switcher_present: !!switcher,
                    switcher_accessible: !!switcher && !!(switcher.getAttribute('aria-label') || switcher.getAttribute('role') || switcher.textContent.trim()),
                    switcher_keyboard_operable: !!switcher && items.length > 0 && items.every(el => ['A', 'BUTTON'].includes(el.tagName) || el.getAttribute('role')),
                    switcher_labels: items.map(text).filter(Boolean),
                    switcher_current_locale: (() => {
                        const current = items.find(el => el.getAttribute('aria-current') === 'true' ||
                            el.getAttribute('aria-current') === 'page');
                        return current ? (current.getAttribute('data-locale') || current.lang || '') : '';
                    })(),
                    equivalent_route: root.getAttribute('data-equivalent-route') ||
                        (document.body && document.body.getAttribute('data-equivalent-route')) || '',
                    hreflang: alternate,
                    canonical: canonical,
                    canonical_is_self: !!canonical && canonicalUrl === currentUrl,
                    localized_title: attrBool(root, 'data-localized-title', false),
                    localized_description: attrBool(root, 'data-localized-description',
                        false),
                    localized_og: attrBool(root, 'data-localized-og',
                        false),
                    localized_alt: attrBool(root, 'data-localized-alt', false),
                    untranslated_system_strings: [...document.querySelectorAll(
                        '[data-i18n-untranslated]')].map(text).filter(Boolean),
                    fallback_explicit: (rootFallback !== null && !!rootFallback.trim()) ||
                        attrBool(root, 'data-locale-fallback-explicit', false),
                    fallback_locale: rootFallback || root.getAttribute('data-fallback-locale') || '',
                    fallback_source_silent: attrBool(root, 'data-locale-fallback-source-silent', false),
                    localized_form_labels: forms.length === 0 || attrBool(root, 'data-localized-form-labels', false),
                    localized_form_errors: forms.length === 0 || attrBool(root, 'data-localized-form-errors', false),
                    text_expansion_ratio: ratios.length ? Math.max(...ratios) : 1,
                    text_overflow_refs: overflow,
                    rtl_layout_direction: root.getAttribute('dir') || '',
                    rtl_focus_visible: attrBool(root, 'data-rtl-focus-visible', false),
                    rtl_navigation_operable: attrBool(root, 'data-rtl-navigation-operable', false),
                    rtl_icon_mirror_policy: root.getAttribute('data-rtl-icon-mirror-policy') || '',
                    rtl_icon_failures: [...document.querySelectorAll(
                        '[data-directional-icon][data-mirrored="false"]')].map(text),
                    rtl_forms_operable: attrBool(root, 'data-rtl-forms-operable', false),
                    rtl_overflow_refs: overflow
                };
            }""")
        return LocalizationObservation(
            locale=facts.get("locale", ""),
            html_lang=facts.get("html_lang", ""),
            html_dir=facts.get("html_dir", ""),
            route_resolves=response is None or bool(response.ok),
            switcher_present=bool(facts.get("switcher_present", False)),
            switcher_accessible=bool(facts.get("switcher_accessible", False)),
            switcher_keyboard_operable=bool(facts.get("switcher_keyboard_operable", False)),
            switcher_labels=list(facts.get("switcher_labels", [])),
            switcher_current_locale=facts.get("switcher_current_locale", ""),
            equivalent_route=facts.get("equivalent_route", ""),
            hreflang=list(facts.get("hreflang", [])),
            canonical=facts.get("canonical", ""),
            canonical_is_self=facts.get("canonical_is_self"),
            localized_title=bool(facts.get("localized_title", False)),
            localized_description=bool(facts.get("localized_description", False)),
            localized_og=bool(facts.get("localized_og", False)),
            localized_alt=bool(facts.get("localized_alt", False)),
            untranslated_system_strings=list(facts.get("untranslated_system_strings", [])),
            fallback_explicit=bool(facts.get("fallback_explicit", False)),
            fallback_locale=facts.get("fallback_locale", ""),
            fallback_source_silent=bool(facts.get("fallback_source_silent", False)),
            localized_form_labels=bool(facts.get("localized_form_labels", False)),
            localized_form_errors=bool(facts.get("localized_form_errors", False)),
            text_expansion_ratio=float(facts.get("text_expansion_ratio", 1)),
            text_overflow_refs=list(facts.get("text_overflow_refs", [])),
            rtl_layout_direction=facts.get("rtl_layout_direction", ""),
            rtl_focus_visible=bool(facts.get("rtl_focus_visible", False)),
            rtl_navigation_operable=bool(facts.get("rtl_navigation_operable", False)),
            rtl_icon_mirror_policy=facts.get("rtl_icon_mirror_policy", ""),
            rtl_icon_failures=list(facts.get("rtl_icon_failures", [])),
            rtl_forms_operable=bool(facts.get("rtl_forms_operable", False)),
            rtl_overflow_refs=list(facts.get("rtl_overflow_refs", [])),
        )


def _is_third_party(url: str, route: str) -> bool:
    try:
        host = urlparse(url).hostname or ""
        return bool(host) and host not in ("localhost", "127.0.0.1") and "://" in url \
            and urlparse(url).hostname != urlparse(route).hostname
    except Exception:  # noqa: BLE001
        return False


def _apply_interaction(page, step: Dict[str, Any]) -> None:
    action = step.get("action")
    if action == "click":
        page.click(step["selector"])
    elif action == "press":
        page.keyboard.press(step["key"])
    elif action == "fill":
        page.fill(step["selector"], step.get("value", ""))
    elif action == "wait_for":
        page.wait_for_selector(step["selector"], state=step.get("state", "visible"))
    elif action == "scroll_to":
        page.eval_on_selector(step["selector"], "el => el.scrollIntoView()")


def _keyboard_trace(page) -> KeyboardTrace:
    try:
        for _ in range(12):
            page.keyboard.press("Tab")
        active = page.evaluate("() => document.activeElement && document.activeElement.tagName")
        ring = page.evaluate(
            """() => { const el = document.activeElement; if (!el) return false;
                       const s = getComputedStyle(el);
                       return s.outlineStyle !== 'none' || s.boxShadow !== 'none'; }""")
        return KeyboardTrace(no_keyboard_trap=active in ("A", "BUTTON", "INPUT", "SELECT",
                                                        "TEXTAREA", "BODY", "DIV"),
                             visible_focus_ring=bool(ring))
    except Exception:  # noqa: BLE001
        return KeyboardTrace()
