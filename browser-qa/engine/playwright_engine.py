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
import json
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
    FormState,
    KeyboardTrace,
    LayoutMetrics,
    ApplicationObservation,
    LocalizationObservation,
    NetworkRequest,
    PageObservation,
    PerfSample,
    SecurityObservation,
    TEST_ENVIRONMENT_NOISE,
)

try:  # pragma: no cover - availability probe
    from playwright.sync_api import sync_playwright  # type: ignore
    _HAS_PLAYWRIGHT = True
except Exception:  # noqa: BLE001
    _HAS_PLAYWRIGHT = False


_SECRET_TOKENS = ("AKIA", "sk_live_", "ghp_", "-----BEGIN", "AIza", "xoxb-", "service_account")


_FORM_DISCOVERY_JS = r"""
() => {
    const visible = el => {
        if (!el) return false;
        const s = getComputedStyle(el), r = el.getBoundingClientRect();
        return !el.hidden && s.display !== 'none' && s.visibility !== 'hidden'
            && Number(s.opacity) !== 0 && (r.width > 0 || r.height > 0);
    };
    const labelFor = el => Boolean(el.labels && el.labels.length)
        || Boolean(el.getAttribute('aria-label') || el.getAttribute('aria-labelledby'))
        || Boolean(el.closest('label'));
    const errorNodes = form => [...form.querySelectorAll(
        '[role="alert"], [aria-live], [data-qa*="error" i], [data-form-error]')];
    return [...document.forms].map((form, index) => {
        const allControls = [...form.querySelectorAll('input,select,textarea')];
        const controls = allControls.filter(el => {
            const type = (el.getAttribute('type') || '').toLowerCase();
            return type !== 'hidden' && type !== 'submit' && type !== 'button'
                && type !== 'reset';
        });
        const required = controls.filter(el => el.required
            || el.getAttribute('aria-required') === 'true');
        const submit = form.querySelector('button[type="submit"], input[type="submit"]')
            || form.querySelector('button:not([type]), input[type="image"]');
        const ref = form.getAttribute('data-qa-form') || form.id
            || form.getAttribute('name') || ('form-' + (index + 1));
        const errors = errorNodes(form);
        return {
            form_ref: ref,
            selector: form.id ? '#' + form.id : 'form:nth-of-type(' + (index + 1) + ')',
            required_controls_found: required.length > 0,
            required_control_count: required.length,
            fields_have_labels: controls.every(labelFor),
            submit_control_found: Boolean(submit),
            submit_disabled: Boolean(submit && submit.disabled),
            method: (form.getAttribute('method') || 'get').toUpperCase(),
            action: form.action || location.href,
            consent_required: controls.some(el => /consent|agree|terms/i.test(
                [el.name, el.id, el.getAttribute('data-consent') || ''].join(' '))),
            initial_error_visible: errors.some(visible),
            initial_success_visible: [...form.querySelectorAll(
                '[role="status"], [data-qa*="success" i], [data-form-success]')]
                .some(visible),
            controls: allControls.map((el, fillable_index) => ({
                fillable_index,
                type: (el.getAttribute('type') || el.tagName || '').toLowerCase(),
                name: el.name || '', id: el.id || '', disabled: Boolean(el.disabled),
                consent: /consent|agree|terms/i.test(
                    [el.name, el.id, el.getAttribute('data-consent') || ''].join(' '))
            }))
        };
    });
}
"""


_FORM_INVALID_JS = r"""
([index, forceInvalid]) => {
    const form = document.forms[index];
    if (!form) return {form_found: false};
    const visible = el => {
        if (!el) return false;
        const s = getComputedStyle(el), r = el.getBoundingClientRect();
        return !el.hidden && s.display !== 'none' && s.visibility !== 'hidden'
            && Number(s.opacity) !== 0 && (r.width > 0 || r.height > 0);
    };
    const controls = [...form.querySelectorAll('input,select,textarea')]
        .filter(el => !['hidden','submit','button','reset'].includes(
            (el.getAttribute('type') || '').toLowerCase()));
    if (forceInvalid) {
        for (const el of controls) {
            if (el.disabled || !(el.required || el.getAttribute('aria-required') === 'true')) continue;
            const type = (el.getAttribute('type') || '').toLowerCase();
            if (type === 'checkbox' || type === 'radio') el.checked = false;
            else if (el.tagName.toLowerCase() === 'select') el.selectedIndex = -1;
            else if (type !== 'file') el.value = '';
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        }
    }
    const invalid = controls.filter(el => !el.checkValidity());
    let invalidEvents = 0;
    const onInvalid = () => { invalidEvents += 1; };
    form.addEventListener('invalid', onInvalid, true);
    const wasValid = form.checkValidity();
    const reportValid = form.reportValidity();
    form.removeEventListener('invalid', onInvalid, true);
    const errors = [...form.querySelectorAll(
        '[role="alert"], [aria-live], [data-qa*="error" i], [data-form-error]')];
    const active = document.activeElement;
    return {
        form_found: true,
        validation_triggered: invalidEvents > 0 || invalid.length > 0,
        invalid_submission_blocked: !wasValid && !reportValid,
        invalid_count: invalid.length,
        error_state_visible_or_programmatic: invalid.some(el => Boolean(el.validationMessage))
            || errors.some(visible),
        error_text: errors.filter(visible).map(el => (el.textContent || '').trim()).filter(Boolean),
        focus_moves_on_error: Boolean(active && invalid.length && active === invalid[0]),
        active_element: active ? (active.id || active.name || active.tagName) : '',
        first_invalid: invalid[0] ? (invalid[0].id || invalid[0].name || invalid[0].tagName) : ''
    };
}
"""


_FORM_STATE_JS = r"""
(index) => {
    const form = document.forms[index];
    if (!form) return {form_found: false};
    const visible = el => {
        if (!el) return false;
        const s = getComputedStyle(el), r = el.getBoundingClientRect();
        return !el.hidden && s.display !== 'none' && s.visibility !== 'hidden'
            && Number(s.opacity) !== 0 && (r.width > 0 || r.height > 0);
    };
    const errors = [...form.querySelectorAll(
        '[role="alert"], [aria-live], [data-qa*="error" i], [data-form-error]')];
    const successes = [...form.querySelectorAll(
        '[role="status"], [data-qa*="success" i], [data-form-success]')];
    const submit = form.querySelector('button[type="submit"], input[type="submit"]')
        || form.querySelector('button:not([type]), input[type="image"]');
    return {
        form_found: true,
        error_state_visible: errors.some(visible),
        error_text: errors.filter(visible).map(el => (el.textContent || '').trim()).filter(Boolean),
        success_state_visible: successes.some(visible),
        submit_disabled: Boolean(submit && submit.disabled),
        focus: document.activeElement ? (document.activeElement.id
            || document.activeElement.name || document.activeElement.tagName) : ''
    };
}
"""


_NAV_DISCOVERY_JS = r"""
() => {
    const visible = el => {
        if (!el) return false;
        const s = getComputedStyle(el), r = el.getBoundingClientRect();
        return !el.hidden && s.display !== 'none' && s.visibility !== 'hidden'
            && Number(s.opacity) !== 0 && (r.width > 0 || r.height > 0);
    };
    const controls = [...document.querySelectorAll('[aria-controls]')];
    const candidates = controls.map((el, index) => {
        const targetId = el.getAttribute('aria-controls') || '';
        const target = targetId ? document.getElementById(targetId) : null;
        const targetLooksLikeNav = target && (target.matches('nav,[role="navigation"]')
            || target.querySelector('a,button'));
        return {el, index, target, targetId, targetLooksLikeNav};
    }).filter(x => x.targetLooksLikeNav || x.el.matches(
        'button.nav-toggle,[data-mobile-nav-toggle],[data-qa="mobile-nav-toggle"]'));
    const candidate = candidates[0];
    if (!candidate) return {found: false, reason: 'no-mobile-navigation-trigger'};
    const state = () => ({
        aria_expanded: candidate.el.getAttribute('aria-expanded'),
        hidden: candidate.target ? candidate.target.hidden : null,
        menu_visible: candidate.target ? visible(candidate.target) : false,
        menu_links: candidate.target ? candidate.target.querySelectorAll('a[href]').length : 0,
        body_overflow: getComputedStyle(document.body).overflow,
        document_overflow: getComputedStyle(document.documentElement).overflow,
        focus: document.activeElement ? (document.activeElement.id
            || document.activeElement.getAttribute('aria-label')
            || document.activeElement.tagName) : ''
    });
    return {
        found: true, aria_controls_index: candidate.index, target_id: candidate.targetId,
        trigger_ref: candidate.el.id || candidate.el.getAttribute('data-qa')
            || candidate.el.getAttribute('aria-label') || candidate.el.tagName,
        initial: state(), destination_links: candidate.target
            ? [...candidate.target.querySelectorAll('a[href]')].map(a => ({
                href: a.href, text: (a.textContent || '').trim().slice(0, 80)})) : []
    };
}
"""


_NAV_STATE_JS = r"""
(targetId) => {
    const controls = [...document.querySelectorAll('[aria-controls]')];
    const trigger = controls.find(el => el.getAttribute('aria-controls') === targetId);
    const target = targetId ? document.getElementById(targetId) : null;
    if (!trigger) return {found: false};
    const visible = el => {
        if (!el) return false;
        const s = getComputedStyle(el), r = el.getBoundingClientRect();
        return !el.hidden && s.display !== 'none' && s.visibility !== 'hidden'
            && Number(s.opacity) !== 0 && (r.width > 0 || r.height > 0);
    };
    return {
        found: true, aria_expanded: trigger.getAttribute('aria-expanded'),
        hidden: target ? target.hidden : null, menu_visible: target ? visible(target) : false,
        menu_links: target ? target.querySelectorAll('a[href]').length : 0,
        body_overflow: getComputedStyle(document.body).overflow,
        document_overflow: getComputedStyle(document.documentElement).overflow,
        focus: document.activeElement ? (document.activeElement.id
            || document.activeElement.getAttribute('aria-label')
            || document.activeElement.tagName) : ''
    };
}
"""


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
    def observe_surface(self, route: str, viewport: int, *, reduced_motion: bool = False,
                        browser: str = "chromium", interactions: Optional[List[Dict[str, Any]]] = None,
                        capture: str = "VIEWPORT",
                        ) -> PageObservation:
        return self.observe(route, viewport, reduced_motion=reduced_motion,
                            browser=browser, interactions=interactions, capture=capture)

    def observe(self, route: str, viewport: int, *, reduced_motion: bool = False,
                browser: str = "chromium", interactions: Optional[List[Dict[str, Any]]] = None,
                capture: str = "VIEWPORT",
                ) -> PageObservation:
        assert self._pw is not None, "PlaywrightEngine.start() was not called"
        btype = {"chromium": self._pw.chromium, "firefox": self._pw.firefox,
                 "webkit": self._pw.webkit}[browser]
        b = btype.launch(headless=True)
        obs = PageObservation(route=route, viewport=viewport, engine=self.name,
                              browser=browser, reduced_motion=reduced_motion)
        obs.raw["engine_identity"] = "REAL_BROWSER"
        obs.raw["engine_version"] = getattr(b, "version", "unknown")
        try:
            ctx = b.new_context(
                viewport={"width": viewport, "height": 900},
                reduced_motion="reduce" if reduced_motion else "no-preference",
                device_scale_factor=1,
            )
            page = ctx.new_page()
            net: List[NetworkRequest] = []
            intercepted_urls = set()
            target = self._url_for(route)
            page.on("console", lambda m: obs.console.append(ConsoleMessage(
                level=m.type, text=m.text,
                classification=THIRD_PARTY_DEFECT if _is_third_party(m.location.get("url", ""), target)
                else APPLICATION_DEFECT)))
            page.on("pageerror", lambda e: obs.console.append(
                ConsoleMessage(level="error", text=str(e), classification=APPLICATION_DEFECT)))

            def record_response(r):
                net.append(NetworkRequest(
                    url=r.url, status=r.status, resource_type=r.request.resource_type,
                    ok=r.ok, third_party=_is_third_party(r.url, target),
                    # A form rejection deliberately fulfilled by this adapter
                    # is evidence, not an unexplained application asset failure.
                    blocked_allowed=r.url in intercepted_urls and r.status >= 400))

            page.on("response", record_response)

            resp = page.goto(target, wait_until="networkidle")
            for step in (interactions or []):
                _apply_interaction(page, step)

            # These are runtime interactions, not source or fixture claims.
            # The raw records are retained in the evidence manifest so a
            # release review can see exactly what the real browser observed.
            form_console_start = len(obs.console)
            form_states, form_observations = self._observe_forms(
                page, route, intercepted_urls)
            form_console_errors = [m.text for m in obs.console[form_console_start:]
                                   if m.level == "error"]
            for message in obs.console[form_console_start:]:
                if (message.level == "error" and message.text.startswith("Failed to load resource")
                        and intercepted_urls):
                    message.classification = TEST_ENVIRONMENT_NOISE
            for evidence in form_observations:
                evidence["CONSOLE_ERROR_DURING_FORM_FLOW"] = form_console_errors
            obs.forms = form_states
            obs.raw["form_observations"] = form_observations

            nav_console_start = len(obs.console)
            nav_state = self._observe_mobile_nav(page, viewport)
            nav_state["CONSOLE_ERRORS"] = [m.text for m in obs.console[nav_console_start:]
                                            if m.level == "error"]
            obs.raw["mobile_nav_observation"] = nav_state
            if (nav_state.get("NAV_TRIGGER_FOUND") is True
                    and nav_state.get("TRIGGER_ACTIVATED") is True):
                obs.nav_open_after_toggle = bool(nav_state.get("MENU_VISIBLE", False))
            else:
                obs.nav_open_after_toggle = None
            close_state = nav_state.get("NAV_CLOSE_STATE")
            if isinstance(close_state, dict) and "menu_visible" in close_state:
                obs.nav_closed_after_route_change = not bool(close_state["menu_visible"])
            else:
                obs.nav_closed_after_route_change = None
            obs.analytics_events = _collect_analytics(page)
            obs.raw["observation_status"] = "EMITTED"

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

            shot = page.screenshot(full_page=str(capture).upper() == "FULL_PAGE")
            obs.render_signature = __import__("hashlib").sha256(shot).hexdigest()[:16]
            obs.raw["screenshot_bytes"] = shot
            obs.raw["render_capture"] = str(capture).upper()
            if (self.config or {}).get("capture_render_artifacts"):
                obs.raw["rendered_dom"] = page.content()
                obs.raw["rendered_css"] = page.evaluate(
                    """() => [...document.styleSheets].map(sheet => {
                        try {
                            return [...sheet.cssRules].map(rule => rule.cssText)
                                .join(String.fromCharCode(10));
                        } catch (error) {
                            return '/* stylesheet inaccessible: ' + (sheet.href || 'inline') + ' */';
                        }
                    }).join(String.fromCharCode(10))"""
                )

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

    def _runtime_observation_cfg(self, kind: str) -> Dict[str, Any]:
        """Read the explicit runtime-observation exercise settings."""
        for container_name in ("runtime_observations", "observations"):
            container = (self.config or {}).get(container_name, {})
            if not isinstance(container, dict):
                continue
            value = container.get(kind)
            if isinstance(value, dict):
                return value
            if isinstance(value, bool):
                return {"required": value}
        alias = "mobile_nav" if kind == "mobile_navigation" else "forms"
        value = (self.config or {}).get(alias, {})
        if isinstance(value, dict):
            return value
        if isinstance(value, bool):
            return {"required": value}
        return {}

    def _observe_forms(self, page, route: str, intercepted_urls) -> tuple:
        """Exercise same-origin forms through a locally intercepted response.

        The interception is deliberately limited to non-GET requests and the
        current origin.  A production URL or an external action is never
        submitted by this adapter.  Native validation is always observed;
        success/rejection and duplicate-submit facts require the plan's
        ``runtime_observations.forms.exercise`` opt-in.
        """
        discovered = page.evaluate(_FORM_DISCOVERY_JS)
        if not discovered:
            return [], []
        cfg = self._runtime_observation_cfg("forms")
        exercise = bool(cfg.get("exercise", cfg.get("required", False)))
        request_records: List[Dict[str, Any]] = []
        handler = None

        if exercise:
            def handle_form_route(route_obj):
                request = route_obj.request
                method = (request.method or "GET").upper()
                if method not in ("POST", "PUT", "PATCH") or not _same_origin(request.url, page.url):
                    route_obj.continue_()
                    return
                intercepted_urls.add(request.url)
                ordinal = len(request_records) + 1
                record = {"url": request.url, "method": method,
                          "resource_type": request.resource_type, "ordinal": ordinal}
                request_records.append(record)
                if request.resource_type == "document":
                    # Prevent an unhandled native navigation while retaining
                    # the attempted side effect as evidence.
                    record["status"] = "ABORTED_BY_QA_INTERCEPT"
                    route_obj.abort(error_code="blockedbyclient")
                    return
                status = 500 if ordinal == 1 else 200
                record["status"] = status
                route_obj.fulfill(
                    status=status, content_type="application/json",
                    body=json.dumps({"ok": status < 400, "qa_intercepted": True}))

            handler = handle_form_route
            page.route("**/*", handler)

        states: List[FormState] = []
        evidence_rows: List[Dict[str, Any]] = []
        try:
            for index, info in enumerate(discovered):
                invalid = page.evaluate(_FORM_INVALID_JS, [index, exercise])
                row = {
                    "FORM_FOUND": bool(invalid.get("form_found", False)),
                    "FORM_ID_OR_SELECTOR": info.get("selector") or info.get("form_ref"),
                    "REQUIRED_CONTROLS_FOUND": bool(info.get("required_controls_found", False)),
                    "LABEL_ASSOCIATION_STATUS": "PASS" if info.get("fields_have_labels") else "FAIL",
                    "SUBMIT_CONTROL_FOUND": bool(info.get("submit_control_found", False)),
                    "VALIDATION_TRIGGERED": bool(invalid.get("validation_triggered", False)),
                    "INVALID_SUBMISSION_BLOCKED": bool(invalid.get("invalid_submission_blocked", False)),
                    "ERROR_STATE_VISIBLE_OR_PROGRAMMATIC": bool(
                        invalid.get("error_state_visible_or_programmatic", False)),
                    "VALID_SUBMISSION_PATH_OBSERVED": False,
                    "NAVIGATION_OR_SIDE_EFFECT_ATTEMPTED": False,
                    "NETWORK_REQUEST_OBSERVED": False,
                    "CONSOLE_ERROR_DURING_FORM_FLOW": [],
                    "status": "PARTIAL",
                    "engine": "playwright",
                    "synthetic_interception": exercise,
                    "invalid_error_text": invalid.get("error_text", []),
                    "focus_after_invalid": invalid.get("active_element", ""),
                    "first_invalid_control": invalid.get("first_invalid", ""),
                }
                if exercise and _safe_form_action(info, page.url):
                    flow_start = len(request_records)
                    keyboard_ok = self._keyboard_form_attempt(page, index, request_records)
                    self._fill_form_with_synthetic_values(page, index, info)
                    events_before_flow = _collect_analytics(page)
                    # Dispatch two submit events in one browser task. A
                    # pending guard must collapse them to one request.
                    page.evaluate(
                        """(i) => {
                            const form = document.forms[i];
                            const submitter = form.querySelector(
                                'button[type="submit"],input[type="submit"]');
                            const event = () => typeof SubmitEvent === 'function'
                                ? new SubmitEvent('submit', {
                                    bubbles: true, cancelable: true, submitter
                                })
                                : new Event('submit', {bubbles: true, cancelable: true});
                            form.dispatchEvent(event());
                            form.dispatchEvent(event());
                        }""", index)
                    pending = page.evaluate(_FORM_STATE_JS, index)
                    _wait_for_form_activity(page)
                    _wait_for_form_state(page, index, "error")
                    rejected = page.evaluate(_FORM_STATE_JS, index)
                    first_flow = request_records[flow_start:]
                    reject_events = _collect_analytics(page)
                    # A second native submit exercises the success response of
                    # the same intercepted local request sequence.
                    page.evaluate(
                        """(i) => { const form = document.forms[i]; form.requestSubmit(); }""",
                        index)
                    _wait_for_form_activity(page)
                    _wait_for_form_state(page, index, "success")
                    succeeded = page.evaluate(_FORM_STATE_JS, index)
                    final_flow = request_records[flow_start:]
                    has_rejection = any(isinstance(r.get("status"), int)
                                        and r.get("status") >= 400 for r in first_flow)
                    has_success = any(isinstance(r.get("status"), int)
                                      and r.get("status") < 400 for r in final_flow)
                    success_event_on_reject = _has_success_event(
                        _events_since(events_before_flow, reject_events))
                    row.update({
                        "VALID_SUBMISSION_PATH_OBSERVED": bool(has_success),
                        "NAVIGATION_OR_SIDE_EFFECT_ATTEMPTED": bool(final_flow),
                        "NETWORK_REQUEST_OBSERVED": bool(final_flow),
                        "DUPLICATE_SUBMIT_REQUEST_COUNT": len(first_flow),
                        "REQUEST_RECORDS": final_flow,
                        "SERVER_REJECT_OBSERVED": bool(has_rejection),
                        "SERVER_REJECT_ERROR_VISIBLE": bool(rejected.get("error_state_visible", False)),
                        "SERVER_REJECT_SUCCESS_VISIBLE": bool(rejected.get("success_state_visible", False)),
                        "SUCCESS_STATE_VISIBLE": bool(succeeded.get("success_state_visible", False)),
                        "SUCCESS_EVENT_ON_SERVER_REJECT": success_event_on_reject,
                        "SUBMIT_DISABLED_DURING_FLOW": bool(
                            pending.get("submit_disabled", False)
                            or rejected.get("submit_disabled", False)),
                        "KEYBOARD_SUBMIT_ATTEMPTED": True,
                        "status": "COMPLETE" if has_success else "PARTIAL",
                    })
                    row["KEYBOARD_SUBMIT_WORKED"] = keyboard_ok
                else:
                    row["interaction_blockage"] = (
                        "form action is external/GET or safe exercise was not requested")

                evidence_rows.append(row)
                states.append(FormState(
                    form_ref=info.get("form_ref", "form-%d" % (index + 1)),
                    fields_have_labels=bool(info.get("fields_have_labels", False)),
                    invalid_shows_error=bool(invalid.get("error_state_visible_or_programmatic", False)),
                    error_message_visible=bool(invalid.get("error_state_visible_or_programmatic", False)),
                    submit_disabled_while_pending=bool(row.get("SUBMIT_DISABLED_DURING_FLOW", False)),
                    duplicate_submit_prevented=(row.get("DUPLICATE_SUBMIT_REQUEST_COUNT") == 1),
                    success_state_on_success=bool(row.get("SUCCESS_STATE_VISIBLE", False)),
                    success_state_on_server_reject=bool(row.get("SERVER_REJECT_SUCCESS_VISIBLE", False)),
                    success_event_on_server_reject=bool(row.get("SUCCESS_EVENT_ON_SERVER_REJECT", False)),
                    keyboard_submittable=bool(row.get("KEYBOARD_SUBMIT_WORKED", False)),
                    focus_moves_on_error=bool(invalid.get("focus_moves_on_error", False)),
                    consent_gate_respected=not bool(info.get("consent_required", False)),
                    raw=row,
                ))
        finally:
            if handler is not None:
                with contextlib.suppress(Exception):
                    page.unroute("**/*", handler)
        return states, evidence_rows

    def _fill_form_with_synthetic_values(self, page, index: int, info: Dict[str, Any]) -> None:
        form = page.locator("form").nth(index)
        controls = form.locator("input,select,textarea")
        for item in info.get("controls", []):
            control_index = int(item.get("fillable_index", -1))
            if control_index < 0 or item.get("disabled"):
                continue
            kind = (item.get("type") or "").lower()
            control = controls.nth(control_index)
            if kind in ("hidden", "submit", "button", "reset", "image", "file"):
                continue
            if item.get("consent"):
                continue
            if kind in ("checkbox", "radio"):
                with contextlib.suppress(Exception):
                    control.check()
                continue
            if kind == "select-one" or item.get("type") == "select":
                with contextlib.suppress(Exception):
                    control.select_option(index=0)
                continue
            with contextlib.suppress(Exception):
                control.fill(_synthetic_form_value(kind, item.get("name", "")))

    def _keyboard_form_attempt(self, page, index: int, request_records=None) -> bool:
        try:
            control = page.locator("form").nth(index).locator(
                "input:not([type=hidden]),select,textarea").first
            control.focus()
            before = page.evaluate("() => document.activeElement && document.activeElement.tagName")
            page.keyboard.press("Enter")
            _wait_for_form_activity(page)
            return bool(before) and (request_records is None or not request_records)
        except Exception:  # noqa: BLE001
            return False

    def _observe_mobile_nav(self, page, viewport: int) -> Dict[str, Any]:
        if viewport > 767:
            return {"status": "NOT_APPLICABLE", "viewport": viewport,
                    "NAV_TRIGGER_FOUND": False, "TRIGGER_ACTIVATED": False,
                    "MENU_VISIBLE": False, "NAV_CLOSE_STATE": {}}
        discovered = page.evaluate(_NAV_DISCOVERY_JS)
        base = {
            "status": "EMITTED", "viewport": viewport,
            "NAV_TRIGGER_FOUND": bool(discovered.get("found", False)),
            "NAV_INITIAL_STATE": discovered.get("initial", {}),
            "TRIGGER_ACTIVATED": False, "NAV_OPEN_STATE": {}, "MENU_VISIBLE": False,
            "FOCUS_BEHAVIOR": {}, "KEYBOARD_OPERATION": {},
            "ESCAPE_CLOSE_BEHAVIOR": {}, "NAV_CLOSE_STATE": {},
            "DESTINATION_LINKS_AVAILABLE": discovered.get("destination_links", []),
            "BODY_SCROLL_STATE": {}, "INTERACTION_BLOCKAGE": None,
        }
        if not discovered.get("found"):
            base["status"] = "NOT_APPLICABLE"
            base["INTERACTION_BLOCKAGE"] = discovered.get("reason", "trigger-not-found")
            return base

        target_id = discovered.get("target_id", "")
        try:
            trigger = page.locator("[aria-controls]").nth(
                int(discovered.get("aria_controls_index", 0)))
            trigger.click()
            opened = page.evaluate(_NAV_STATE_JS, target_id)
            base.update({
                "TRIGGER_ACTIVATED": True,
                "NAV_OPEN_STATE": opened,
                "MENU_VISIBLE": bool(opened.get("menu_visible", False)),
                "FOCUS_BEHAVIOR": {"after_click": opened.get("focus", "")},
                "BODY_SCROLL_STATE": {
                    "body_overflow_after_open": opened.get("body_overflow"),
                    "document_overflow_after_open": opened.get("document_overflow")},
            })

            # Reset to closed, then exercise the actual keyboard activation.
            if opened.get("menu_visible"):
                trigger.click()
            trigger.focus()
            page.keyboard.press("Enter")
            keyboard_state = page.evaluate(_NAV_STATE_JS, target_id)
            if not keyboard_state.get("menu_visible"):
                page.keyboard.press(" ")
                keyboard_state = page.evaluate(_NAV_STATE_JS, target_id)
            base["KEYBOARD_OPERATION"] = {
                "focus_before_key": True,
                "opened_with_enter_or_space": bool(keyboard_state.get("menu_visible", False)),
                "state": keyboard_state,
            }
            if keyboard_state.get("menu_visible"):
                page.keyboard.press("Escape")
            escaped = page.evaluate(_NAV_STATE_JS, target_id)
            base["ESCAPE_CLOSE_BEHAVIOR"] = {
                "attempted": True, "closed": not bool(escaped.get("menu_visible", False)),
                "state": escaped,
            }

            # Route-change close is only exercised for an explicitly safe,
            # same-origin destination. Hash-only placeholders are excluded.
            route_link = page.locator("#%s a[href]" % target_id).first if target_id else None
            links = discovered.get("destination_links", [])
            safe_link = next((link for link in links if _same_origin(link.get("href", ""), page.url)
                              and link.get("href", "") not in ("", "#")
                              and not link.get("href", "").endswith("#")), None)
            if safe_link is not None and route_link is not None:
                trigger.click()
                with contextlib.suppress(Exception):
                    route_link.click(no_wait_after=True)
                with contextlib.suppress(Exception):
                    page.wait_for_load_state("networkidle", timeout=2000)
                closed = page.evaluate(_NAV_STATE_JS, target_id)
                base["NAV_CLOSE_STATE"] = closed
            else:
                base["INTERACTION_BLOCKAGE"] = "no-safe-same-origin-destination-link"
        except Exception as exc:  # noqa: BLE001
            base["status"] = "PARTIAL"
            base["INTERACTION_BLOCKAGE"] = str(exc).splitlines()[0]
        return base

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


def _same_origin(candidate: str, current: str) -> bool:
    """Return whether a browser target stays on the current origin."""
    try:
        candidate_url = urlparse(candidate)
        current_url = urlparse(current)
        if candidate_url.scheme == "" and current:
            candidate_url = urlparse(urljoin(current, candidate))
        if candidate_url.scheme == "file" or current_url.scheme == "file":
            return candidate_url.scheme == current_url.scheme == "file"
        return (candidate_url.scheme, candidate_url.hostname, candidate_url.port) == (
            current_url.scheme, current_url.hostname, current_url.port)
    except Exception:  # noqa: BLE001
        return False


def _safe_form_action(info: Dict[str, Any], current_url: str) -> bool:
    """Only allow the form exercise for an intercepted same-origin mutation."""
    method = (info.get("method") or "GET").upper()
    return method in ("POST", "PUT", "PATCH") and _same_origin(info.get("action", ""), current_url)


def _synthetic_form_value(kind: str, name: str) -> str:
    token = "%s %s" % (kind or "", name or "")
    if "email" in token.lower():
        return "synthetic@example.invalid"
    if any(x in token.lower() for x in ("phone", "tel", "mobile")):
        return "5550100000"
    if "url" in token.lower() or "website" in token.lower():
        return "https://example.invalid/qa"
    if "date" in token.lower():
        return "2026-01-01"
    if any(x in token.lower() for x in ("number", "quantity", "count", "age")):
        return "1"
    if "password" in token.lower():
        return "synthetic-qa-password"
    return "Synthetic QA"


def _wait_for_form_activity(page) -> None:
    """Yield to browser task/microtask completion without an arbitrary sleep."""
    with contextlib.suppress(Exception):
        page.wait_for_load_state("networkidle", timeout=2000)


def _wait_for_form_state(page, index: int, state: str) -> None:
    """Wait for the DOM state produced by the exercised form response."""
    with contextlib.suppress(Exception):
        page.wait_for_function(
            """([i, expected]) => {
                const form = document.forms[i];
                if (!form) return false;
                const visible = el => {
                    if (!el) return false;
                    const s = getComputedStyle(el), r = el.getBoundingClientRect();
                    return !el.hidden && s.display !== 'none' && s.visibility !== 'hidden'
                        && Number(s.opacity) !== 0 && (r.width > 0 || r.height > 0);
                };
                const selector = expected === 'success'
                    ? '[role="status"], [data-qa*="success" i], [data-form-success]'
                    : '[role="alert"], [aria-live], [data-qa*="error" i], [data-form-error]';
                return [...form.querySelectorAll(selector)].some(visible);
            }""", arg=[index, state], timeout=2000)


def _collect_analytics(page) -> List[AnalyticsEvent]:
    """Read the canonical page event bus when the application exposes it."""
    try:
        raw = page.evaluate(
            """() => Array.isArray(window.__analyticsEvents)
                ? window.__analyticsEvents : []""")
    except Exception:  # noqa: BLE001
        return []
    events: List[AnalyticsEvent] = []
    for item in raw if isinstance(raw, list) else []:
        if isinstance(item, str):
            events.append(AnalyticsEvent(name=item))
            continue
        if not isinstance(item, dict):
            continue
        name = item.get("name") or item.get("event_name") or item.get("event") or ""
        if not name:
            continue
        params = item.get("params")
        if not isinstance(params, dict):
            params = item.get("properties") if isinstance(item.get("properties"), dict) else {}
        try:
            count = int(item.get("count", 1))
        except (TypeError, ValueError):
            count = 1
        events.append(AnalyticsEvent(name=str(name), params=params, count=count,
                                     trigger=item.get("trigger")))
    return events


def _events_since(before: List[AnalyticsEvent], after: List[AnalyticsEvent]) -> List[AnalyticsEvent]:
    if len(after) >= len(before) and after[:len(before)] == before:
        return after[len(before):]
    return after


def _has_success_event(events: List[AnalyticsEvent]) -> bool:
    return any("success" in (event.name or "").lower()
               or "success" in (event.trigger or "").lower() for event in events)


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
        focus_seen = False
        active = ""
        for _ in range(12):
            page.keyboard.press("Tab")
            state = page.evaluate(
                """() => { const el = document.activeElement; if (!el) return {};
                           const s = getComputedStyle(el);
                           return {tag: el.tagName,
                                   ring: s.outlineStyle !== 'none' || s.boxShadow !== 'none'}; }""")
            active = state.get("tag", "")
            focus_seen = focus_seen or bool(state.get("ring", False))
        return KeyboardTrace(no_keyboard_trap=active in ("A", "BUTTON", "INPUT", "SELECT",
                                                        "TEXTAREA", "BODY", "DIV"),
                             visible_focus_ring=focus_seen)
    except Exception:  # noqa: BLE001
        return KeyboardTrace()
