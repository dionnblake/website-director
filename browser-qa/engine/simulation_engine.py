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
    A11yViolation,
    AccessibilityObservation,
    ApplicationObservation,
    AnalyticsEvent,
    BrowserQAEngine,
    ConsoleMessage,
    FormState,
    KeyboardTrace,
    LayoutMetrics,
    LocalizationObservation,
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
        obs.raw["engine_identity"] = "SIMULATION"
        obs.raw["engine_version"] = "synthetic-fixture"
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
        obs.raw["mobile_nav_observation"] = {
            "status": "SYNTHETIC_FIXTURE",
            "NAV_TRIGGER_FOUND": bool(nav_fx),
            "NAV_INITIAL_STATE": nav_fx.get("initial_state", {}),
            "TRIGGER_ACTIVATED": obs.nav_open_after_toggle is not None,
            "NAV_OPEN_STATE": {"open_after_toggle": obs.nav_open_after_toggle},
            "MENU_VISIBLE": bool(obs.nav_open_after_toggle),
            "KEYBOARD_OPERATION": {"fixture": True},
            "ESCAPE_CLOSE_BEHAVIOR": {"fixture": True},
            "NAV_CLOSE_STATE": {"closed_after_route_change": obs.nav_closed_after_route_change},
            "DESTINATION_LINKS_AVAILABLE": nav_fx.get("destination_links", []),
            "BODY_SCROLL_STATE": nav_fx.get("body_scroll_state", {}),
            "INTERACTION_BLOCKAGE": None,
        }

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
            form_raw = {
                "FORM_FOUND": True,
                "FORM_ID_OR_SELECTOR": f.get("form_ref", "form"),
                "REQUIRED_CONTROLS_FOUND": f.get("required_controls_found", True),
                "LABEL_ASSOCIATION_STATUS": "PASS" if f.get("fields_have_labels", True) else "FAIL",
                "SUBMIT_CONTROL_FOUND": f.get("submit_control_found", True),
                "VALIDATION_TRIGGERED": f.get("validation_triggered", True),
                "INVALID_SUBMISSION_BLOCKED": f.get("invalid_submission_blocked", True),
                "ERROR_STATE_VISIBLE_OR_PROGRAMMATIC": sr.get(
                    "error_visible", f.get("error_message_visible", True)),
                "VALID_SUBMISSION_PATH_OBSERVED": f.get("success_state_on_success", True),
                "NAVIGATION_OR_SIDE_EFFECT_ATTEMPTED": bool(sr),
                "NETWORK_REQUEST_OBSERVED": bool(sr),
                "CONSOLE_ERROR_DURING_FORM_FLOW": [],
                "status": "SYNTHETIC_FIXTURE",
                "engine": "simulation",
                "synthetic_interception": False,
            }
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
                raw=form_raw,
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

        obs.raw["form_observations"] = [f.raw for f in obs.forms]
        obs.raw["observation_status"] = "EMITTED"

        # -- perf ---------------------------------------
        p = fx.get("perf", {})
        if p:
            obs.perf = PerfSample(
                lcp_ms=p.get("lcp_ms"), cls=p.get("cls"), inp_ms=p.get("inp_ms"),
                long_tasks=int(p.get("long_tasks", 0)),
                measurement_kind=p.get("measurement_kind", "SYNTHETIC"))

        # -- accessibility ----------------------------------
        a = fx.get("a11y")
        if a is not None:
            eng = a.get("engine", {})
            a11y = AccessibilityObservation(
                engine_name=eng.get("name"),
                engine_version=eng.get("version"),
                engine_status=eng.get("status", "RAN" if eng.get("name") else "NOT_RUN"),
                violations=[A11yViolation(rule_id=v.get("rule_id", ""), impact=v.get("impact", "moderate"),
                                          wcag=v.get("wcag", ""), target=v.get("target", ""),
                                          help_text=v.get("help", ""))
                            for v in a.get("violations", [])],
                missing_accessible_name_refs=list(a.get("missing_accessible_name", [])),
                contrast_failures=list(a.get("contrast_failures", [])),
                focus_visible=a.get("focus_visible", True),
                focus_obscured_refs=list(a.get("focus_obscured", [])),
                focus_obscured_indeterminate=a.get("focus_obscured_indeterminate", False),
                landmarks=list(a.get("landmarks", ["header", "nav", "main", "footer"])),
                heading_order_ok=a.get("heading_order_ok", True),
                h1_count=int(a.get("h1_count", 1)),
                page_lang=a.get("page_lang", "en"),
                page_title=a.get("page_title", obs.title or "Untitled"),
                skip_link_present=a.get("skip_link_present"),
                color_only_state_refs=list(a.get("color_only_state", [])),
                small_target_refs=list(a.get("small_targets", [])),
                tiny_target_refs=list(a.get("tiny_targets", [])),
                reflow_failures=list(a.get("reflow_failures", [])),
                text_spacing_failures=list(a.get("text_spacing_failures", [])),
                unlabelled_field_refs=list(a.get("unlabelled_fields", [])),
                unassociated_error_refs=list(a.get("unassociated_errors", [])),
                drag_without_alternative_refs=list(a.get("drag_without_alternative", [])),
                meaningful_images_missing_alt=list(a.get("meaningful_images_missing_alt", [])),
                decorative_images_exposed=list(a.get("decorative_images_exposed", [])),
                dialogs=list(a.get("dialogs", [])),
                keyboard_trap_refs=list(a.get("keyboard_traps", [])),
                screen_reader_status=a.get("screen_reader_status", "NOT_RUN"),
                manual_keyboard_result=a.get("manual_keyboard_result"),
            )
            obs.a11y = a11y

        # -- localization ---------------------------------------------
        loc = fx.get("localization")
        if loc is not None:
            if not isinstance(loc, dict):
                loc = {"route_resolves": False}
            switcher = loc.get("switcher", {}) if isinstance(loc.get("switcher", {}), dict) else {}
            fallback = loc.get("fallback", {}) if isinstance(loc.get("fallback", {}), dict) else {}
            rtl = loc.get("rtl", {}) if isinstance(loc.get("rtl", {}), dict) else {}
            forms = loc.get("forms", {}) if isinstance(loc.get("forms", {}), dict) else {}
            obs.localization = LocalizationObservation(
                locale=loc.get("locale", ""),
                html_lang=loc.get("html_lang", ""),
                html_dir=loc.get("html_dir", ""),
                route_resolves=loc.get("route_resolves", False),
                switcher_present=loc.get("switcher_present", switcher.get("present", False)),
                switcher_accessible=loc.get("switcher_accessible", switcher.get("accessible", True)),
                switcher_keyboard_operable=loc.get(
                    "switcher_keyboard_operable", switcher.get("keyboard_operable", True)),
                switcher_labels=list(loc.get("switcher_labels", switcher.get("labels", []))),
                switcher_current_locale=loc.get(
                    "switcher_current_locale", switcher.get("current_locale", "")),
                equivalent_route=loc.get("equivalent_route", ""),
                hreflang=list(loc.get("hreflang", [])),
                canonical=loc.get("canonical", ""),
                canonical_is_self=loc.get("canonical_is_self"),
                canonical_points_to_source=loc.get("canonical_points_to_source", False),
                localized_title=loc.get("localized_title", False),
                localized_description=loc.get("localized_description", False),
                localized_og=loc.get("localized_og", False),
                localized_alt=loc.get("localized_alt", False),
                untranslated_system_strings=list(loc.get("untranslated_system_strings", [])),
                fallback_explicit=loc.get("fallback_explicit", fallback.get("explicit", False)),
                fallback_locale=loc.get("fallback_locale", fallback.get("locale", "")),
                fallback_source_silent=loc.get(
                    "fallback_source_silent", fallback.get("source_silent", False)),
                localized_form_labels=loc.get(
                    "localized_form_labels", forms.get("labels", False)),
                localized_form_errors=loc.get(
                    "localized_form_errors", forms.get("errors", False)),
                text_expansion_ratio=float(loc.get("text_expansion_ratio", 1.0)),
                text_overflow_refs=list(loc.get("text_overflow_refs", [])),
                rtl_layout_direction=loc.get(
                    "rtl_layout_direction", rtl.get("layout_direction", "")),
                rtl_focus_visible=loc.get("rtl_focus_visible", rtl.get("focus_visible", False)),
                rtl_navigation_operable=loc.get(
                    "rtl_navigation_operable", rtl.get("navigation_operable", False)),
                rtl_icon_mirror_policy=loc.get(
                    "rtl_icon_mirror_policy", rtl.get("icon_mirror_policy", "")),
                rtl_icon_failures=list(loc.get("rtl_icon_failures", rtl.get("icon_failures", []))),
                rtl_forms_operable=loc.get("rtl_forms_operable", rtl.get("forms_operable", False)),
                rtl_overflow_refs=list(loc.get("rtl_overflow_refs", rtl.get("overflow_refs", []))),
            )

        # -- conditional application architecture ----------------------
        app = fx.get("application")
        if app is not None:
            if not isinstance(app, dict):
                app = {}

            def app_fact(name: str, *aliases: str):
                for key in (name,) + aliases:
                    if key in app:
                        return app[key]
                return None

            obs.application = ApplicationObservation(
                authenticated=app_fact("authenticated"),
                authorization_enforced=app_fact("authorization_enforced", "server_authorization_enforced"),
                object_access_allowed=app_fact("object_access_allowed", "object_level_access_allowed"),
                client_role_trusted=app_fact("client_role_trusted", "trust_client_role"),
                password_plaintext=app_fact("password_plaintext", "plaintext_password"),
                password_hash_exposed=app_fact("password_hash_exposed", "hash_exposed"),
                account_recovery_defined=app_fact("account_recovery_defined", "recovery_defined"),
                admin_route_server_protected=app_fact("admin_route_server_protected", "admin_server_protected"),
                client_price_trusted=app_fact("client_price_trusted", "trust_client_price"),
                canonical_price_verified=app_fact("canonical_price_verified", "server_price_verified"),
                checkout_click_marks_paid=app_fact("checkout_click_marks_paid", "button_marks_paid"),
                payment_confirmed=app_fact("payment_confirmed", "server_payment_confirmed"),
                webhook_signature_verified=app_fact("webhook_signature_verified", "signature_verified"),
                webhook_idempotent=app_fact("webhook_idempotent", "idempotent_webhook"),
                duplicate_side_effect_created=app_fact("duplicate_side_effect_created", "duplicate_effect"),
                raw_card_stored=app_fact("raw_card_stored", "stores_raw_card"),
                hosted_or_tokenized_payment=app_fact("hosted_or_tokenized_payment", "hosted_or_tokenized"),
                subscription_entitlement_granted=app_fact("subscription_entitlement_granted", "entitlement_granted"),
                entitlement_revoked_on_payment_failure=app_fact("entitlement_revoked_on_payment_failure", "failed_payment_revokes_entitlement"),
                digital_shipping_unnecessary=app_fact("digital_shipping_unnecessary", "digital_shipping_bloat"),
                physical_shipping_defined=app_fact("physical_shipping_defined", "shipping_defined"),
                booking_overlap_prevented=app_fact("booking_overlap_prevented", "overlap_prevented"),
                booking_timezone_explicit=app_fact("booking_timezone_explicit", "timezone_explicit"),
                upload_allowlist_enforced=app_fact("upload_allowlist_enforced", "allowlist_enforced"),
                executable_upload_accepted=app_fact("executable_upload_accepted", "accepts_executable"),
                private_storage_authorized=app_fact("private_storage_authorized", "authorized_download"),
                private_file_public=app_fact("private_file_public", "public_url_exposed"),
                ugc_sanitized=app_fact("ugc_sanitized", "sanitized"),
                ugc_script_executed=app_fact("ugc_script_executed", "script_executed"),
                transactional_email_failure_visible=app_fact("transactional_email_failure_visible", "delivery_failure_visible"),
                transactional_email_failure_reported_success=app_fact("transactional_email_failure_reported_success", "failure_reported_as_success"),
                integration_inventory_complete=app_fact("integration_inventory_complete", "inventory_complete"),
                application_secret_exposed=app_fact("application_secret_exposed", "secret_exposed_client"),
                purchase_event_authoritative=app_fact("purchase_event_authoritative", "server_confirmed_purchase"),
                purchase_event_from_click=app_fact("purchase_event_from_click", "purchase_event_button_triggered"),
                canonical_event_with_locale=app_fact("canonical_event_with_locale", "locale_parameter_present"),
                private_route_indexable=app_fact("private_route_indexable", "private_route_indexed"),
                provider_available=app_fact("provider_available"),
                live_payment_attempted=app_fact("live_payment_attempted", "real_payment_attempted"),
                live_user_created=app_fact("live_user_created", "real_user_attempted"),
                raw=dict(app),
            )

        # Synthetic motion facts are intentionally labeled as SIMULATION. The
        # assertion catalogue may inspect them for deterministic negative
        # controls, but they can never satisfy a Level 2/3 real-browser gate.
        motion_fx = fx.get("motion", {})
        if isinstance(motion_fx, dict):
            rows = motion_fx.get("motion_observations", motion_fx.get("sequences", []))
            if isinstance(rows, list):
                obs.motion_observations = [dict(row) for row in rows if isinstance(row, dict)]
            obs.raw["motion_observations"] = obs.motion_observations
            obs.raw["motion_runtime"] = {
                "engine_identity": "SIMULATION",
                "runtime_observed": bool(obs.motion_observations),
                "synthetic": True,
            }
        obs.raw["rendered_colors"] = fx.get("rendered_colors", [])

        # Preserve the engine identity/version written at observation start.
        # Replacing raw here previously erased those fields and weakened the
        # distinction between synthetic and real runtime evidence.
        obs.raw.update({"fixture_dir": fixture_dir, "fixture": fx, "flaky": fx.get("flaky")})
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
