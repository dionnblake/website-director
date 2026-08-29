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
