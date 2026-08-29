"""Deterministic, dependency-free BROWSER_QA_ENGINE.

Materialises a ``PageObservation`` from a fixture directory:

    <fixture>/index.html        -- the page under test (lightly parsed)
    <fixture>/qa-fixture.json   -- declared observations, keyed by viewport

This engine launches no browser and opens no socket. It exists so the
framework's own negative-control validation (tests/test_v2_8_browser_regression_qa.py)
runs anywhere with only the Python standard library, and so authors can dry-run
a browser-qa plan before a real engine is available. It is NOT a substitute for
real-browser verification of a generated project.
"""

from __future__ import annotations

import hashlib
import os
import re
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional

from .base import (
    APPLICATION_DEFECT,
    AnalyticsEvent,
    BrowserQAEngine,
    ConsoleMessage,
    FormState,
    KeyboardTrace,
    LayoutMetrics,
    NetworkRequest,
    PageObservation,
    PerfSample,
    SecurityObservation,
    read_json,
)

_HASH_LINK = re.compile(r'<a\b[^>]*\bhref\s*=\s*"(#|#\s*)"', re.I)
_SRC_ATTR = re.compile(r'\b(?:src|href)\s*=\s*"([^"]+)"', re.I)
_OBVIOUS_JS_ERROR = re.compile(r'throw\s+new\s+\w*Error|(?<![\w.])undefinedFunction\s*\(', re.I)


class _ImgParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.imgs: List[Dict[str, str]] = []
        self.hash_links: List[str] = []
        self.has_nav_toggle = False

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "img":
            self.imgs.append(a)
        if tag == "a" and a.get("href", "").strip() in ("#", ""):
            self.hash_links.append(a.get("href", "#"))
        if tag == "button" and ("nav" in a.get("class", "").lower()
                                or a.get("aria-controls", "") or "menu" in a.get("id", "").lower()):
            self.has_nav_toggle = True


class SimulationEngine(BrowserQAEngine):
    name = "simulation"
    supports_real_browser = False

    def available(self) -> bool:
        return True

    # -- helpers ---------------------------------------------------------
    def _fixture_dir(self, route: str) -> str:
        route = route.strip()
        if os.path.isabs(route) and os.path.isdir(route):
            return route
        candidate = os.path.join(self.project_root, route.lstrip("/\\"))
        if os.path.isdir(candidate):
            return candidate
        if os.path.isfile(candidate):
            return os.path.dirname(candidate)
        return self.project_root

    @staticmethod
    def _pick(mapping: Dict[str, Any], viewport: int, default: Any = None) -> Any:
        if not isinstance(mapping, dict):
            return default
        if str(viewport) in mapping:
            return mapping[str(viewport)]
        numeric = sorted((int(k) for k in mapping if str(k).isdigit()))
        chosen = None
        for n in numeric:
            if n <= viewport:
                chosen = n
        if chosen is None and numeric:
            chosen = numeric[0]
        return mapping.get(str(chosen), default) if chosen is not None else default

    # -- observation ---------------------------------------------------
    def observe(self, route: str, viewport: int, *, reduced_motion: bool = False,
                browser: str = "simulation", interactions: Optional[List[Dict[str, Any]]] = None,
                ) -> PageObservation:
        fixture_dir = self._fixture_dir(route)
        fx_path = os.path.join(fixture_dir, "qa-fixture.json")
        fx: Dict[str, Any] = read_json(fx_path) if os.path.isfile(fx_path) else {}

        html = ""
        html_path = os.path.join(fixture_dir, "index.html")
        if os.path.isfile(html_path):
            with open(html_path, "r", encoding="utf-8") as fh:
                html = fh.read()

        parser = _ImgParser()
        try:
            parser.feed(html)
        except Exception:  # noqa: BLE001 - malformed fixture HTML is not our concern
            pass

        obs = PageObservation(route=route, viewport=viewport, engine=self.name,
                              browser=browser, reduced_motion=reduced_motion)
        obs.final_url = fx.get("final_url", route)
        obs.title = fx.get("title", "")

        # -- console --------------------------------------------------
        for c in fx.get("console", []):
            obs.console.append(ConsoleMessage(
                level=c.get("level", "error"), text=c.get("text", ""),
                classification=c.get("classification", APPLICATION_DEFECT)))
        # a fixture cannot hide an obvious inline exception
        if _OBVIOUS_JS_ERROR.search(html) and not any(m.level == "error" for m in obs.console):
            obs.console.append(ConsoleMessage(level="error",
                               text="Uncaught error detected in inline script",
                               classification=APPLICATION_DEFECT))

        # -- network -------------------------------------------------
        declared_net = {n["url"]: n for n in fx.get("network", [])}
        for m in _SRC_ATTR.finditer(html):
            url = m.group(1)
            if url.startswith(("data:", "#", "mailto:", "javascript:")):
                continue
            if url not in declared_net:
                declared_net[url] = {"url": url, "status": 200,
                                     "resource_type": _rtype(url), "ok": True}
        for n in declared_net.values():
            status = int(n.get("status", 200))
            obs.network.append(NetworkRequest(
                url=n["url"], status=status,
                resource_type=n.get("resource_type", _rtype(n["url"])),
                ok=n.get("ok", 200 <= status < 400),
                third_party=n.get("third_party", False),
                blocked_allowed=n.get("blocked_allowed", False)))

        # -- layout ------------------------------------------------
        layout_fx = self._pick(fx.get("layout", {}), viewport, {}) or {}
        client_w = int(layout_fx.get("client_width", viewport))
        scroll_w = int(layout_fx.get("document_scroll_width",
                                     layout_fx.get("scroll_width", client_w)))
        body_w = int(layout_fx.get("body_width", scroll_w))
        obs.layout = LayoutMetrics(
            viewport_width=viewport,
            document_scroll_width=scroll_w,
            client_width=client_w,
            body_width=body_w,
            has_horizontal_overflow=scroll_w > client_w + 1 or body_w > client_w + 1,
            clipped_interactive_refs=list(layout_fx.get("clipped_interactive_refs", [])),
            zero_size_interactive_refs=list(layout_fx.get("zero_size_interactive_refs", [])),
            offscreen_control_refs=list(layout_fx.get("offscreen_control_refs", [])),
            fixed_nav_overlap=bool(layout_fx.get("fixed_nav_overlap", False)),
            layout_shift_after_load=float(layout_fx.get("layout_shift_after_load", 0.0)),
            primary_cta_visible=bool(layout_fx.get("primary_cta_visible", True)),
        )

        # -- assets ---------------------------------------------
        obs.images_zero_dimension = list(fx.get("images_zero_dimension", []))
        obs.broken_assets = [n.url for n in obs.network
                             if n.resource_type in ("image", "font", "script", "stylesheet")
                             and not n.ok and not n.blocked_allowed]
        obs.broken_assets += [b for b in fx.get("broken_assets", []) if b not in obs.broken_assets]
        obs.placeholder_images = list(fx.get("placeholder_images", []))

        # -- nav / hash links ------------------------------------
        obs.placeholder_hash_links = parser.hash_links + list(fx.get("placeholder_hash_links", []))
        nav_fx = fx.get("nav", {})
        obs.nav_open_after_toggle = nav_fx.get("open_after_toggle")
        obs.nav_closed_after_route_change = nav_fx.get("closed_after_route_change")

        # -- reduced motion -----------------------------------
        rm_fx = fx.get("reduced_motion", {})
        if reduced_motion:
            obs.reduced_motion_hidden_content = list(rm_fx.get("hidden_content", []))

        # -- render signature (visual regression) -------------
        sig_map = fx.get("render_signature", {})
        if reduced_motion and isinstance(rm_fx.get("render_signature"), dict):
            sig_map = rm_fx["render_signature"]
        sig = self._pick(sig_map, viewport, None)
        if sig is None:
            sig = hashlib.sha256(
                ("%s|%s|%s|%s" % (route, viewport, reduced_motion, scroll_w)).encode()
            ).hexdigest()[:16]
        obs.render_signature = str(sig)

        # -- forms -------------------------------------------
        for f in fx.get("forms", []):
            sr = f.get("server_reject", {})
            obs.forms.append(FormState(
                form_ref=f.get("form_ref", "form"),
                fields_have_labels=f.get("fields_have_labels", True),
                invalid_shows_error=f.get("invalid_shows_error", True),
                error_message_visible=sr.get("error_visible", f.get("error_message_visible", True)),
                submit_disabled_while_pending=f.get("submit_disabled_while_pending", True),
                duplicate_submit_prevented=f.get("duplicate_submit_prevented", True),
                success_state_on_success=f.get("success_state_on_success", True),
                success_state_on_server_reject=sr.get("success_state", False),
                success_event_on_server_reject=sr.get("success_event", False),
                keyboard_submittable=f.get("keyboard_submittable", True),
                focus_moves_on_error=f.get("focus_moves_on_error", True),
                consent_gate_respected=f.get("consent_gate_respected", True),
            ))

        # -- keyboard --------------------------------------
        kb = fx.get("keyboard", {})
        obs.keyboard = KeyboardTrace(
            primary_nav_reachable=kb.get("primary_nav_reachable", True),
            visible_focus_ring=kb.get("visible_focus_ring", True),
            menu_toggle_operable=kb.get("menu_toggle_operable", True),
            dialog_escape_closes=kb.get("dialog_escape_closes", True),
            no_keyboard_trap=kb.get("no_keyboard_trap", True),
            primary_cta_reachable=kb.get("primary_cta_reachable", True),
        )

        # -- security -------------------------------------
        sec = fx.get("security", {})
        obs.security = SecurityObservation(
            is_https=fx.get("https", sec.get("is_https", True)),
            mixed_content_urls=list(sec.get("mixed_content_urls", [])),
            response_headers=dict(sec.get("response_headers", {})),
            insecure_cookies=list(sec.get("insecure_cookies", [])),
            dom_secret_hits=list(sec.get("dom_secret_hits", [])),
            third_party_scripts=list(sec.get("third_party_scripts", [])),
            analytics_active_before_consent=sec.get("analytics_active_before_consent", False),
            consent_reject_reachable=sec.get("consent_reject_reachable", True),
            disclosure_routes_resolve=sec.get("disclosure_routes_resolve", True),
        )

        # -- analytics events ----------------------------
        for e in fx.get("analytics_events", []):
            obs.analytics_events.append(AnalyticsEvent(
                name=e.get("name", ""), params=e.get("params", {}),
                count=int(e.get("count", 1)), trigger=e.get("trigger")))

        # -- perf ---------------------------------------
        p = fx.get("perf", {})
        if p:
            obs.perf = PerfSample(
                lcp_ms=p.get("lcp_ms"), cls=p.get("cls"), inp_ms=p.get("inp_ms"),
                long_tasks=int(p.get("long_tasks", 0)),
                measurement_kind=p.get("measurement_kind", "SYNTHETIC"))

        obs.raw = {"fixture_dir": fixture_dir, "fixture": fx, "flaky": fx.get("flaky")}
        return obs


def _rtype(url: str) -> str:
    u = url.split("?")[0].lower()
    if u.endswith((".js", ".mjs")):
        return "script"
    if u.endswith(".css"):
        return "stylesheet"
    if u.endswith((".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".svg")):
        return "image"
    if u.endswith((".woff", ".woff2", ".ttf", ".otf")):
        return "font"
    if u.endswith((".json",)):
        return "fetch"
    return "document"
