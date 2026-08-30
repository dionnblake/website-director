"""The browser QA assertion catalogue.

Grouped by protocol section. Each function returns ``None`` (not applicable to
this observation), one ``Finding``, or a list of ``Finding``. Register new checks
by appending to ``ALL_CHECKS`` at the bottom.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, List, Optional

from engine.base import APPLICATION_DEFECT
from . import Finding  # noqa: F401  (dataclass used by type readers / re-export)


def _F(check_id, title, ok, source, obs, **kw):
    from . import finding
    return finding(check_id, title, ok, source, obs, **kw)


PII_TOKENS = re.compile(
    r"^(email|e_mail|phone|tel|mobile|full_?name|first_?name|last_?name|address|street|"
    r"postal|zip|message|message_body|comment|comments|note|notes|password|passwd|"
    r"card|cc_number|cvv|cvc|ssn|dob|date_of_birth|nin|passport)$", re.I)
PII_VALUE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+|\+?\d[\d\-\s().]{7,}\d")
SECRET_SHAPES = re.compile(r"AKIA[0-9A-Z]{16}|sk_live_[0-9a-zA-Z]{16,}|ghp_[0-9A-Za-z]{30,}|"
                           r"AIza[0-9A-Za-z\-_]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----")


def _route_cfg(plan: Dict[str, Any], route: str) -> Dict[str, Any]:
    for r in plan.get("routes", []):
        if r.get("path") == route or r.get("route") == route:
            return r
    return {}


# ===========================================================================
# 7. RESPONSIVE INVARIANTS
# ===========================================================================
def check_horizontal_overflow(obs, plan):
    if obs.layout is None:
        return None
    lm = obs.layout
    ok = not lm.has_horizontal_overflow
    return _F("responsive.horizontal-overflow",
              "No horizontal overflow at %dpx" % obs.viewport, ok,
              "PRODUCTION_CHECKLIST", obs, owning_spec="LOCKED_SPEC / design-system.md",
              detail=("scrollWidth=%d clientWidth=%d bodyWidth=%d"
                      % (lm.document_scroll_width, lm.client_width, lm.body_width)),
              evidence={"scroll_width": lm.document_scroll_width, "client_width": lm.client_width})


def check_clipped_and_zero_targets(obs, plan):
    if obs.layout is None:
        return None
    lm = obs.layout
    out = []
    if lm.clipped_interactive_refs:
        out.append(_F("responsive.content-clipped", "No interactive content clipped outside viewport",
                      False, "PRODUCTION_CHECKLIST", obs, detail=str(lm.clipped_interactive_refs)))
    if lm.zero_size_interactive_refs:
        out.append(_F("responsive.zero-size-target", "No zero-sized interactive targets", False,
                      "PRODUCTION_CHECKLIST", obs, detail=str(lm.zero_size_interactive_refs)))
    if lm.offscreen_control_refs:
        out.append(_F("responsive.offscreen-control", "No primary control stranded off-screen", False,
                      "PRODUCTION_CHECKLIST", obs, detail=str(lm.offscreen_control_refs)))
    if lm.fixed_nav_overlap:
        out.append(_F("responsive.fixed-nav-overlap", "Fixed/sticky nav does not overlap content",
                      False, "PAGE_EXPERIENCE_SPEC", obs))
    if not lm.primary_cta_visible:
        out.append(_F("responsive.primary-cta-hidden", "Primary CTA is visible at this viewport",
                      False, "LOCKED_SPEC", obs, owning_spec="content-plan.md"))
    if lm.layout_shift_after_load > 0.1:
        out.append(_F("responsive.post-hydration-shift",
                      "Layout stable after load/hydration (CLS proxy <= 0.1)", False,
                      "PRODUCTION_CHECKLIST", obs, detail="shift=%.3f" % lm.layout_shift_after_load))
    if not out:
        out.append(_F("responsive.invariants", "Responsive invariants hold at %dpx" % obs.viewport,
                      True, "PRODUCTION_CHECKLIST", obs))
    return out


# ===========================================================================
# 8. NAVIGATION QA
# ===========================================================================
def check_placeholder_hash_links(obs, plan):
    intentional = set(_route_cfg(plan, obs.route).get("intentional_hash_links", []))
    stray = [t for t in obs.placeholder_hash_links if t not in intentional]
    if not obs.placeholder_hash_links:
        return _F("nav.no-placeholder-links", "No unresolved '#' placeholder links", True,
                  "PRODUCTION_CHECKLIST", obs)
    return _F("nav.no-placeholder-links", "No unresolved '#' placeholder links", not stray,
              "PRODUCTION_CHECKLIST", obs, detail="stray=%s" % stray)


def check_broken_internal_links(obs, plan):
    broken = [n.url for n in obs.network if n.resource_type == "document" and not n.ok
              and not n.third_party]
    return _F("nav.internal-links-resolve", "Internal routes resolve (no 4xx/5xx documents)",
              not broken, "PRODUCTION_CHECKLIST", obs, detail=str(broken))


def check_mobile_nav(obs, plan):
    if obs.viewport > 767 or obs.nav_open_after_toggle is None:
        return None
    out = [_F("nav.mobile-opens", "Mobile navigation opens on toggle", bool(obs.nav_open_after_toggle),
              "PAGE_EXPERIENCE_SPEC", obs)]
    if obs.nav_closed_after_route_change is not None:
        out.append(_F("nav.mobile-closes-on-route", "Mobile navigation closes on route change",
                      bool(obs.nav_closed_after_route_change), "PAGE_EXPERIENCE_SPEC", obs))
    return out


# ===========================================================================
# 9. CONSOLE & PAGE ERROR CAPTURE
# ===========================================================================
def check_console_clean(obs, plan):
    ignore = plan.get("console_ignore", [])
    def ignored(msg):
        return any(re.search(pat["pattern"], msg.text) for pat in ignore if pat.get("justification"))
    defects = [m for m in obs.console if m.level == "error"
               and m.classification in (APPLICATION_DEFECT,) and not ignored(m)]
    third = [m for m in obs.console if m.level == "error" and m.classification == "THIRD_PARTY_DEFECT"
             and not ignored(m)]
    out = [_F("console.no-application-errors", "Console free of uncaught application errors",
              not defects, "PRODUCTION_CHECKLIST", obs,
              detail="; ".join(m.text[:120] for m in defects))]
    if third:
        out.append(_F("console.third-party-errors",
                      "Third-party console errors reviewed (not silently ignored)", False,
                      "SECURITY_PRIVACY_REVIEW", obs, detail="; ".join(m.text[:120] for m in third)))
    return out


# ===========================================================================
# 10. NETWORK QA
# ===========================================================================
def check_network(obs, plan):
    allow = set(plan.get("allowed_third_party_failures", []))
    bad = []
    for n in obs.network:
        if n.ok:
            continue
        if n.blocked_allowed or n.url in allow:
            continue
        if n.third_party and any(a in n.url for a in allow):
            continue
        bad.append("%s -> %d" % (n.url, n.status))
    return _F("network.no-failed-requests",
              "No unexplained 4xx/5xx or aborted requests", not bad,
              "PRODUCTION_CHECKLIST", obs, detail="; ".join(bad))


# ===========================================================================
# 11. IMAGE / ASSET QA
# ===========================================================================
def check_assets(obs, plan):
    out = []
    if obs.broken_assets:
        out.append(_F("assets.no-broken", "No broken/missing image, font, script, or style assets",
                      False, "PRODUCTION_CHECKLIST", obs, detail=str(obs.broken_assets[:8])))
    if obs.images_zero_dimension:
        out.append(_F("assets.non-zero-dimensions", "Images render with non-zero dimensions", False,
                      "PRODUCTION_CHECKLIST", obs, detail=str(obs.images_zero_dimension[:8])))
    if obs.placeholder_images:
        out.append(_F("assets.no-accidental-placeholder", "No accidental placeholder images shipped",
                      False, "LOCKED_SPEC", obs, owning_spec="asset-manifest.json",
                      detail=str(obs.placeholder_images[:8])))
    hero = _route_cfg(plan, obs.route).get("critical_hero_asset")
    if hero:
        loaded = any(hero in n.url and n.ok for n in obs.network)
        out.append(_F("assets.critical-hero-loads", "Critical hero asset loads", loaded,
                      "LOCKED_SPEC", obs, owning_spec="asset-manifest.json", detail=hero))
    if not out:
        out.append(_F("assets.integrity", "Asset integrity holds at %dpx" % obs.viewport, True,
                      "PRODUCTION_CHECKLIST", obs))
    return out


# ===========================================================================
# 12. FORM QA
# ===========================================================================
def check_forms(obs, plan):
    out = []
    for f in obs.forms:
        cid = "form.%s" % f.form_ref
        out.append(_F(cid + ".labels", "Form '%s' fields have labels" % f.form_ref,
                      f.fields_have_labels, "PRODUCTION_CHECKLIST", obs))
        out.append(_F(cid + ".invalid-error", "Form '%s' shows a visible error on invalid submit"
                      % f.form_ref, f.invalid_shows_error and f.error_message_visible,
                      "PRODUCTION_CHECKLIST", obs))
        out.append(_F(cid + ".dup-submit", "Form '%s' prevents duplicate submit" % f.form_ref,
                      f.duplicate_submit_prevented, "PRODUCTION_CHECKLIST", obs))
        out.append(_F(cid + ".success-state", "Form '%s' shows success only on real success"
                      % f.form_ref,
                      f.success_state_on_success and not f.success_state_on_server_reject,
                      "SECURITY_PRIVACY_REVIEW", obs,
                      detail="server_reject_shows_success=%s" % f.success_state_on_server_reject))
        out.append(_F(cid + ".no-false-conversion",
                      "Form '%s' emits NO success conversion event on server reject" % f.form_ref,
                      not f.success_event_on_server_reject, "MEASUREMENT_PLAN", obs))
        out.append(_F(cid + ".keyboard", "Form '%s' is keyboard submittable" % f.form_ref,
                      f.keyboard_submittable, "PRODUCTION_CHECKLIST", obs))
        if not f.consent_gate_respected:
            out.append(_F(cid + ".consent", "Form '%s' respects consent dependency" % f.form_ref,
                          False, "SECURITY_PRIVACY_REVIEW", obs))
    return out or None


# ===========================================================================
# 13. MEASUREMENT EVENT QA
# ===========================================================================
def check_measurement(obs, plan):
    required = plan.get("measurement", {}).get("expected_events")
    if not required:
        return None
    out = []
    by_name: Dict[str, List] = {}
    for e in obs.analytics_events:
        by_name.setdefault(e.name, []).append(e)

    # Which events are expected to FIRE on THIS route: the route's own list, plus
    # any event flagged fires_on_every_route in the plan vocabulary.
    route_events = set(_route_cfg(plan, obs.route).get("expected_events", []))
    for spec in required:
        if isinstance(spec, dict) and spec.get("fires_on_every_route"):
            route_events.add(spec["name"])
    for spec in required:
        name = spec["name"] if isinstance(spec, dict) else spec
        if name not in route_events:
            continue
        fires = by_name.get(name, [])
        total = sum(e.count for e in fires)
        out.append(_F("measure.%s.fires-once" % name,
                      "Event '%s' fires exactly once on %s" % (name, obs.route), total == 1,
                      "MEASUREMENT_PLAN", obs, detail="count=%d" % total))
        if isinstance(spec, dict) and spec.get("required_params") and fires:
            missing = [p for p in spec["required_params"] if p not in fires[0].params]
            out.append(_F("measure.%s.params" % name, "Event '%s' carries required params" % name,
                          not missing, "MEASUREMENT_PLAN", obs, detail="missing=%s" % missing))

    for e in obs.analytics_events:
        pii_keys = [k for k in e.params if PII_TOKENS.match(str(k))]
        pii_vals = [k for k, v in e.params.items() if isinstance(v, str) and PII_VALUE.search(v)]
        if pii_keys or pii_vals:
            out.append(_F("measure.no-pii", "Analytics event '%s' carries NO PII" % e.name, False,
                          "SECURITY_PRIVACY_REVIEW", obs,
                          detail="pii_keys=%s pii_values_in=%s" % (pii_keys, pii_vals)))
        known = {(s["name"] if isinstance(s, dict) else s) for s in required}
        if e.name not in known:
            out.append(_F("measure.no-undeclared-event",
                          "No analytics event outside the measurement plan", False,
                          "MEASUREMENT_PLAN", obs, detail="undeclared=%s" % e.name))
    if not out:
        out.append(_F("measure.events", "Measurement events conform to the plan", True,
                      "MEASUREMENT_PLAN", obs))
    return out


# ===========================================================================
# 14. SECURITY / PRIVACY BROWSER QA
# ===========================================================================
def check_security_privacy(obs, plan):
    if obs.security is None:
        return None
    s = obs.security
    sp = plan.get("security_privacy", {})
    rc = _route_cfg(plan, obs.route)
    is_prod = plan.get("environment") == "production"
    # Header / HTTPS / consent assertions apply where the route opts in or in production.
    surface_checks = bool(rc.get("security_privacy")) or is_prod
    out = []
    if surface_checks and sp.get("expect_https_production") and is_prod:
        out.append(_F("sec.https", "Production surface served over HTTPS", s.is_https,
                      "SECURITY_PRIVACY_REVIEW", obs))
        out.append(_F("sec.no-mixed-content", "No mixed content on HTTPS page",
                      not s.mixed_content_urls, "SECURITY_PRIVACY_REVIEW", obs,
                      detail=str(s.mixed_content_urls[:6])))
    if surface_checks:
        for header in sp.get("required_headers", []):
            present = header.lower() in {k.lower() for k in s.response_headers}
            out.append(_F("sec.header.%s" % header.lower(), "Response header %s present" % header,
                          present, "SECURITY_PRIVACY_REVIEW", obs))
    if s.dom_secret_hits or any(SECRET_SHAPES.search(x) for x in s.dom_secret_hits):
        out.append(_F("sec.no-dom-secrets", "No secret-shaped values in DOM / client bundle", False,
                      "SECURITY_PRIVACY_REVIEW", obs, detail=str(s.dom_secret_hits[:4])))
    declared = set(sp.get("allowed_third_party_scripts", []))
    undeclared = [u for u in s.third_party_scripts
                  if not any(d in u for d in declared)]
    if s.third_party_scripts:
        out.append(_F("sec.third-party-inventory",
                      "Runtime third-party scripts match the approved inventory", not undeclared,
                      "SECURITY_PRIVACY_REVIEW", obs, detail="undeclared=%s" % undeclared))
    if surface_checks and sp.get("consent") == "REQUIRED":
        out.append(_F("sec.analytics-after-consent",
                      "Analytics/marketing inactive before consent", not s.analytics_active_before_consent,
                      "SECURITY_PRIVACY_REVIEW", obs))
        out.append(_F("sec.reject-reachable", "Consent rejection path is reachable",
                      s.consent_reject_reachable, "SECURITY_PRIVACY_REVIEW", obs))
    if surface_checks and sp.get("disclosure_routes"):
        out.append(_F("sec.disclosure-routes", "Privacy/disclosure routes resolve",
                      s.disclosure_routes_resolve, "SECURITY_PRIVACY_REVIEW", obs))
    return out or None


# ===========================================================================
# 15. REDUCED MOTION
# ===========================================================================
def check_reduced_motion(obs, plan):
    if not obs.reduced_motion:
        return None
    out = [_F("motion.reduced-content-visible",
              "Essential content remains visible under prefers-reduced-motion",
              not obs.reduced_motion_hidden_content, "MOTION_SPEC", obs,
              detail=str(obs.reduced_motion_hidden_content[:6]))]
    if obs.keyboard is not None:
        out.append(_F("motion.reduced-nav-operable", "Navigation operable under reduced motion",
                      obs.keyboard.primary_nav_reachable, "MOTION_SPEC", obs))
    return out


# ===========================================================================
# 16. KEYBOARD SMOKE QA
# ===========================================================================
def check_keyboard(obs, plan):
    if obs.keyboard is None:
        return None
    k = obs.keyboard
    checks = [
        ("keyboard.nav-reachable", "Primary navigation reachable by keyboard", k.primary_nav_reachable),
        ("keyboard.visible-focus", "Visible focus indicator present", k.visible_focus_ring),
        ("keyboard.no-trap", "No obvious keyboard trap", k.no_keyboard_trap),
        ("keyboard.cta-reachable", "Primary CTA reachable by keyboard", k.primary_cta_reachable),
    ]
    if obs.nav_open_after_toggle is not None:
        checks.append(("keyboard.menu-operable", "Menu toggle operable by keyboard", k.menu_toggle_operable))
    return [_F(cid, title, ok, "PRODUCTION_CHECKLIST", obs) for cid, title, ok in checks]


# ===========================================================================
# 18. VISUAL REGRESSION
# ===========================================================================
def check_visual_regression(obs, plan):
    if "visual_baselines" not in plan:
        return None  # visual regression is not part of this plan
    baselines = plan.get("visual_baselines", {})
    key = "%s@%d%s" % (obs.route, obs.viewport, "+rm" if obs.reduced_motion else "")
    baseline = baselines.get(key)
    if baseline is None:
        return Finding(check_id="visual.baseline-missing",
                       title="Visual baseline recorded for %s" % key, verdict="BLOCKED",
                       requirement_source="BROWSER_QA_PLAN", route=obs.route, viewport=obs.viewport,
                       detail="no baseline; run baseline creation explicitly", method="VISUAL_COMPARISON")
    match = baseline == obs.render_signature
    f = _F("visual.regression", "Render matches locked visual baseline for %s" % key, match,
           "BROWSER_QA_PLAN", obs, detail="baseline=%s current=%s" % (baseline, obs.render_signature))
    f.method = "VISUAL_COMPARISON"
    # A diff is evidence of change, not automatically a defect (protocol sec 18).
    if not match:
        f.detail += "  [DIFF DETECTED — review; do not overwrite baseline without authorization]"
    return f


# ===========================================================================
# 37. PERFORMANCE BOUNDARY (existing thresholds only)
# ===========================================================================
def check_perf(obs, plan):
    if obs.perf is None:
        return None
    th = plan.get("perf_thresholds", {"lcp_ms": 2500, "cls": 0.1, "inp_ms": 200})
    p = obs.perf
    out = []
    if p.lcp_ms is not None:
        out.append(_F("perf.lcp", "LCP within threshold (%s measurement)" % p.measurement_kind,
                      p.lcp_ms <= th.get("lcp_ms", 2500), "PRODUCTION_CHECKLIST", obs,
                      detail="lcp=%.0fms kind=%s" % (p.lcp_ms, p.measurement_kind)))
    if p.cls is not None:
        out.append(_F("perf.cls", "CLS within threshold", p.cls <= th.get("cls", 0.1),
                      "PRODUCTION_CHECKLIST", obs, detail="cls=%.3f" % p.cls))
    if p.inp_ms is not None:
        out.append(_F("perf.inp", "INP within threshold", p.inp_ms <= th.get("inp_ms", 200),
                      "PRODUCTION_CHECKLIST", obs, detail="inp=%.0fms" % p.inp_ms))
    return out or None


# ===========================================================================
# LOCALIZATION / INTERNATIONALIZATION (Website Director V2.14)
# Gated on plan["localization"]; source LOCALIZATION_PLAN.
# This group owns only runtime-observable route, DOM, metadata, fallback,
# pseudo-localization, and RTL facts. The localization validator owns the
# provider-neutral readiness and content/translation contracts.
# ===========================================================================
def _locale_key(value: Any) -> str:
    return str(value or "").strip().replace("_", "-").lower()


def _has_text_label(value: Any) -> bool:
    # Emoji flags and bare icon glyphs do not satisfy the text-label contract.
    return any(unicodedata.category(char).startswith("L") for char in str(value or ""))


def check_localization(obs, plan):
    cfg = plan.get("localization")
    if not cfg or (cfg.get("required") is False and not cfg.get("run", False)):
        return None
    S = "LOCALIZATION_PLAN"
    if obs.localization is None:
        return Finding(check_id="localization.observation", title="Localization runtime facts were collected",
                       verdict="BLOCKED", requirement_source=S, route=obs.route,
                       viewport=obs.viewport, detail="BLOCKED_LOCALIZATION_OBSERVATION_UNAVAILABLE",
                       method="BROWSER_EXECUTED")

    l = obs.localization
    rc = _route_cfg(plan, obs.route)
    out = []

    def lf(cid, title, ok, **kw):
        return _F("localization." + cid, title, ok, S, obs, **kw)

    expected_locale = rc.get("locale") or rc.get("expected_locale") or cfg.get("expected_locale")
    expected_direction = rc.get("direction") or rc.get("expected_direction") or cfg.get("direction")
    supported = cfg.get("supported_locales") or cfg.get("locales") or []
    if isinstance(supported, dict):
        supported = list(supported.keys())
    supported_keys = {_locale_key(value) for value in supported if value}

    if cfg.get("check_routes", True):
        out.append(lf("route-resolves", "Localized route resolves", l.route_resolves,
                      detail="route=%s" % obs.route))

    if expected_locale:
        got = l.html_lang or l.locale
        out.append(lf("html-lang", "Rendered page language matches the route locale",
                      _locale_key(got) == _locale_key(expected_locale),
                      detail="got=%r expected=%r" % (got, expected_locale)))
        if l.locale and supported_keys:
            out.append(lf("locale-supported", "Rendered locale is in the supported locale registry",
                          _locale_key(l.locale) in supported_keys,
                          detail="got=%r supported=%s" % (l.locale, sorted(supported_keys))))

    switcher_cfg = cfg.get("switcher", {})
    if not isinstance(switcher_cfg, dict):
        switcher_cfg = {}
    switcher_required = switcher_cfg.get(
        "required", cfg.get("switcher_required", len(supported_keys) > 1))
    if switcher_required:
        out.append(lf("switcher-present", "Locale switcher is present", l.switcher_present))
        out.append(lf("switcher-accessible", "Locale switcher has an accessible name and role",
                      l.switcher_accessible))
        out.append(lf("switcher-keyboard", "Locale switcher is keyboard operable",
                      l.switcher_keyboard_operable))
        labels_ok = bool(l.switcher_labels) and all(_has_text_label(label) for label in l.switcher_labels)
        out.append(lf("switcher-text-labels", "Locale choices have visible or assistive text labels",
                      labels_ok, detail=str(l.switcher_labels[:8])))
        if expected_locale:
            out.append(lf("switcher-current-locale", "Locale switcher identifies the current locale",
                          _locale_key(l.switcher_current_locale) == _locale_key(expected_locale),
                          detail="got=%r expected=%r" % (l.switcher_current_locale, expected_locale)))

    expected_equivalent = rc.get("equivalent_route") or rc.get("expected_equivalent_route")
    if expected_equivalent:
        out.append(lf("equivalent-route", "Locale route maps to the equivalent content route",
                      l.equivalent_route == expected_equivalent,
                      detail="got=%r expected=%r" % (l.equivalent_route, expected_equivalent)))

    hcfg = cfg.get("hreflang", {})
    if not isinstance(hcfg, dict):
        hcfg = {}
    hreflang_required = hcfg.get(
        "required", cfg.get("require_hreflang", len(supported_keys) > 1))
    if hreflang_required:
        entries = [entry for entry in l.hreflang if isinstance(entry, dict)]
        codes = {_locale_key(entry.get("hreflang") or entry.get("locale")) for entry in entries}
        expected_codes = {_locale_key(value) for value in (hcfg.get("locales") or supported) if value}
        valid_codes = bool(entries) and all(bool(code) and (code == "x-default" or re.match(
            r"^[a-z]{2,8}(?:-[a-z0-9]{2,8})*$", code, re.I)) for code in codes)
        out.append(lf("hreflang-present", "Localized hreflang links are present", bool(entries)))
        out.append(lf("hreflang-codes", "Localized hreflang codes are syntactically valid", valid_codes,
                      detail=str(sorted(codes))))
        if expected_codes:
            out.append(lf("hreflang-coverage", "Localized hreflang links cover the declared locales",
                          expected_codes.issubset(codes),
                          detail="missing=%s" % sorted(expected_codes - codes)))
        reciprocal_ok = all(entry.get("reciprocal") is True for entry in entries)
        out.append(lf("hreflang-reciprocal", "Localized hreflang links are reciprocal", reciprocal_ok))
        if expected_locale:
            self_code = _locale_key(expected_locale)
            out.append(lf("hreflang-self", "The current locale has a self hreflang entry",
                          self_code in codes))
        if hcfg.get("require_x_default"):
            out.append(lf("hreflang-x-default", "Localized hreflang links include x-default",
                          "x-default" in codes))

    canonical_required = hcfg.get(
        "require_localized_canonical", cfg.get("require_localized_canonical", False))
    if canonical_required:
        canonical_ok = (bool(l.canonical) and l.canonical_points_to_source is not True
                        and l.canonical_is_self is True)
        out.append(lf("canonical-self", "Localized page canonical is self-referencing",
                      canonical_ok, detail="canonical=%r" % l.canonical))
    if hcfg.get("expected_canonical"):
        out.append(lf("canonical-value", "Localized page uses the declared canonical URL",
                      l.canonical == hcfg["expected_canonical"],
                      detail="got=%r expected=%r" % (l.canonical, hcfg["expected_canonical"])))

    metadata_cfg = cfg.get("metadata", {})
    if not isinstance(metadata_cfg, dict):
        metadata_cfg = {}
    for key, label in (("title", "title"), ("description", "description"),
                       ("og", "Open Graph metadata"), ("alt", "localized image alt text")):
        if metadata_cfg.get(key) or metadata_cfg.get("localized_" + key):
            out.append(lf("metadata-" + key, "%s is localized" % label.capitalize(),
                          bool(getattr(l, "localized_" + key)),
                          detail="metadata field=%s" % key))

    if l.untranslated_system_strings:
        out.append(lf("untranslated-system-strings", "No untranslated system strings remain",
                      False, detail=str(l.untranslated_system_strings[:8])))

    fallback_cfg = cfg.get("fallback", {})
    if not isinstance(fallback_cfg, dict):
        fallback_cfg = {}
    fallback_required = fallback_cfg.get("required", cfg.get("fallback_required", False))
    if fallback_required:
        expected_fallback = fallback_cfg.get("locale") or rc.get("fallback_locale")
        fallback_ok = l.fallback_explicit and not l.fallback_source_silent
        if expected_fallback:
            fallback_ok = fallback_ok and _locale_key(l.fallback_locale) == _locale_key(expected_fallback)
        out.append(lf("fallback-explicit", "Locale fallback behavior is explicit", fallback_ok,
                      detail="locale=%r expected=%r" % (l.fallback_locale, expected_fallback)))

    forms_cfg = cfg.get("forms", {})
    if not isinstance(forms_cfg, dict):
        forms_cfg = {}
    if forms_cfg.get("required"):
        out.append(lf("form-labels", "Localized form labels are present", l.localized_form_labels))
        out.append(lf("form-errors", "Localized form errors are present", l.localized_form_errors))

    pseudo_cfg = cfg.get("pseudo_localization", cfg.get("pseudolocalization", {}))
    if not isinstance(pseudo_cfg, dict):
        pseudo_cfg = {}
    if pseudo_cfg.get("enabled") or pseudo_cfg.get("required") or cfg.get("text_expansion_required"):
        minimum_ratio = float(pseudo_cfg.get("minimum_ratio", pseudo_cfg.get("expansion_ratio", 1.3)))
        expansion_ok = (l.text_expansion_ratio >= minimum_ratio and not l.text_overflow_refs
                        and not (obs.layout is not None and obs.layout.has_horizontal_overflow))
        out.append(lf("text-expansion", "Localized text meets the expansion target without overflow",
                      expansion_ok,
                      detail="ratio=%.3f minimum=%.3f overflow=%s" %
                             (l.text_expansion_ratio, minimum_ratio, l.text_overflow_refs[:8])))
    elif l.text_overflow_refs:
        out.append(lf("text-overflow", "Localized text does not overflow its container", False,
                      detail=str(l.text_overflow_refs[:8])))
    elif obs.layout is not None and obs.layout.has_horizontal_overflow and cfg.get("check_overflow", False):
        out.append(lf("text-overflow", "Localized page has no horizontal overflow", False,
                      detail="viewport=%d" % obs.viewport))

    rtl_cfg = cfg.get("rtl", {})
    if not isinstance(rtl_cfg, dict):
        rtl_cfg = {}
    rtl_required = rtl_cfg.get("required", cfg.get("rtl_required", expected_direction == "rtl"))
    if rtl_required:
        out.append(lf("rtl-direction", "RTL locale renders with RTL direction",
                      l.html_dir == "rtl" and l.rtl_layout_direction == "rtl",
                      detail="html_dir=%r layout=%r" % (l.html_dir, l.rtl_layout_direction)))
        out.append(lf("rtl-focus", "RTL focus remains visible", l.rtl_focus_visible))
        out.append(lf("rtl-navigation", "RTL navigation remains operable", l.rtl_navigation_operable))
        out.append(lf("rtl-icon-policy", "RTL directional icon mirroring follows an explicit policy",
                      bool(l.rtl_icon_mirror_policy)))
        out.append(lf("rtl-icons", "RTL directional icons follow the mirror policy",
                      not l.rtl_icon_failures, detail=str(l.rtl_icon_failures[:8])))
        out.append(lf("rtl-forms", "RTL forms remain operable", l.rtl_forms_operable))
        layout_overflow = obs.layout is not None and obs.layout.has_horizontal_overflow
        out.append(lf("rtl-overflow", "RTL layout has no overflow",
                      not l.rtl_overflow_refs and not layout_overflow,
                      detail=str(l.rtl_overflow_refs[:8])))

    if expected_direction and expected_direction != "rtl":
        out.append(lf("direction", "Rendered direction matches the locale contract",
                      l.html_dir == expected_direction,
                      detail="got=%r expected=%r" % (l.html_dir, expected_direction)))

    return out


# ===========================================================================
# ACCESSIBILITY (Website Director V2.9 — ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md §32)
# Gated on plan["accessibility"]; source ACCESSIBILITY_REVIEW; method BROWSER_EXECUTED.
# Deterministic contrast MATH is Impeccable's; this only checks it was run + classifies.
# ===========================================================================
def check_accessibility(obs, plan):
    acfg = plan.get("accessibility")
    if not acfg or obs.a11y is None:
        return None
    a = obs.a11y
    rc = _route_cfg(plan, obs.route)
    out = []
    S = "ACCESSIBILITY_REVIEW"

    def af(cid, title, ok, **kw):
        f = _F("a11y." + cid, title, ok, S, obs, **kw)
        return f

    # -- automated engine (§31) --------------------------------------
    min_sev = {"minor": 0, "moderate": 1, "serious": 2, "critical": 3}
    floor = min_sev.get(acfg.get("engine", {}).get("min_severity_fails", "moderate"), 1)
    if a.engine_status == "ENGINE_UNAVAILABLE":
        out.append(Finding(check_id="a11y.engine", title="Automated accessibility engine ran",
                           verdict="BLOCKED", requirement_source=S, route=obs.route,
                           viewport=obs.viewport, detail="BLOCKED_ACCESSIBILITY_ENGINE_UNAVAILABLE",
                           method="BROWSER_EXECUTED"))
    elif a.engine_status == "RAN":
        blocking = [v for v in a.violations if min_sev.get(v.impact, 1) >= floor]
        f = af("engine-violations",
               "Accessibility engine (%s %s): no violations at/above %s"
               % (a.engine_name, a.engine_version or "?", acfg.get("engine", {}).get("min_severity_fails", "moderate")),
               not blocking, detail="; ".join("%s[%s]%s" % (v.rule_id, v.impact, (" " + v.wcag) if v.wcag else "")
                                              for v in blocking))
        out.append(f)
    elif acfg.get("engine", {}).get("require", False):
        out.append(Finding(check_id="a11y.engine", title="Automated accessibility engine ran",
                           verdict="BLOCKED", requirement_source=S, route=obs.route,
                           viewport=obs.viewport, detail="engine required by plan but not run",
                           method="BROWSER_EXECUTED"))
    else:
        out.append(af("engine", "Automated accessibility engine scan", True, na=True,
                      detail="engine not run for this observation"))

    # -- names / roles / values (§8) --------------------------------
    if a.missing_accessible_name_refs:
        out.append(af("accessible-name", "All interactive controls expose an accessible name",
                      False, detail=str(a.missing_accessible_name_refs[:8])))
    else:
        out.append(af("accessible-name", "Interactive controls expose an accessible name", True))

    # -- contrast (§12) — consumes Impeccable math ------------------
    if a.contrast_failures:
        f = af("contrast", "Text / UI contrast meets the WCAG 2.2 AA target", False,
                detail=str(a.contrast_failures[:8]), owning_spec="IMPECCABLE-ENGINE-PROTOCOL.md (math)")
        f.method = "DETERMINISTIC"
        out.append(f)

    # -- colour independence (§13) ---------------------------------
    if a.color_only_state_refs:
        out.append(af("color-independence", "Meaning is not conveyed by colour alone", False,
                      detail=str(a.color_only_state_refs[:8])))

    # -- focus visibility + not obscured (§10, §11) ----------------
    out.append(af("focus-visible", "Visible focus indicator present", a.focus_visible))
    if a.focus_obscured_refs:
        out.append(af("focus-not-obscured", "Focused control not obscured by sticky/fixed UI (WCAG 2.4.11)",
                      False, detail=str(a.focus_obscured_refs[:6])))
    elif a.focus_obscured_indeterminate:
        out.append(Finding(check_id="a11y.focus-not-obscured",
                           title="Focus-not-obscured requires manual verification here",
                           verdict="BLOCKED", requirement_source=S, route=obs.route, viewport=obs.viewport,
                           detail="MANUAL_REQUIRED — engine cannot objectively establish", method="BROWSER_EXECUTED"))

    # -- keyboard trap (§9) — extends V2.8 keyboard smoke ----------
    if a.keyboard_trap_refs:
        out.append(af("keyboard-trap", "No keyboard trap", False, detail=str(a.keyboard_trap_refs[:6])))

    # -- semantic structure (§7) ---------------------------------
    expected_lm = set(rc.get("expected_landmarks", ["main"]))
    missing_lm = sorted(expected_lm - set(a.landmarks))
    out.append(af("landmarks", "Expected landmark regions present", not missing_lm,
                  detail="missing=%s" % missing_lm))
    out.append(af("heading-order", "Logical heading hierarchy (no skipped levels)", a.heading_order_ok))
    out.append(af("single-h1", "Exactly one primary page heading", a.h1_count == 1,
                  detail="h1_count=%d" % a.h1_count))

    # -- page language + title (§32) ----------------------------
    out.append(af("page-lang", "Page declares a language (WCAG 3.1.1)", bool(a.page_lang),
                  detail="lang=%r" % a.page_lang))
    exp_lang = rc.get("expected_lang")
    if exp_lang and a.page_lang and a.page_lang.split("-")[0] != exp_lang.split("-")[0]:
        out.append(af("page-lang-value", "Page language matches the expected value", False,
                      detail="got %r expected %r" % (a.page_lang, exp_lang)))
    out.append(af("page-title", "Page has a non-empty <title> (WCAG 2.4.2)", bool(a.page_title)))
    if rc.get("requires_skip_link") and a.skip_link_present is False:
        out.append(af("skip-link", "Skip-navigation link present", False))

    # -- reflow (§14) ------------------------------------------
    if a.reflow_failures:
        out.append(af("reflow", "Content reflows at the target width without loss (WCAG 1.4.10)",
                      False, detail=str(a.reflow_failures[:6])))

    # -- text spacing (§15) -----------------------------------
    if a.text_spacing_failures:
        out.append(af("text-spacing", "Interface tolerates the WCAG 1.4.12 text-spacing override",
                      False, detail=str(a.text_spacing_failures[:6])))

    # -- target size (§16) — project ergonomic + WCAG floor -----
    tgt = acfg.get("target_size", {})
    if a.tiny_target_refs:
        out.append(af("target-size-wcag", "No control below the WCAG 2.2 24px floor without an exception",
                      False, detail=str(a.tiny_target_refs[:8])))
    if a.small_target_refs:
        out.append(af("target-size-project",
                      "Adjacent targets meet the project minimum (%dpx)" % tgt.get("project_minimum_px", 44),
                      False, detail=str(a.small_target_refs[:8])))

    # -- dragging (§17) --------------------------------------
    if a.drag_without_alternative_refs:
        out.append(af("drag-alternative", "Every drag interaction has a non-drag alternative (WCAG 2.5.7)",
                      False, detail=str(a.drag_without_alternative_refs[:6])))

    # -- images (§19) ---------------------------------------
    if a.meaningful_images_missing_alt:
        out.append(af("image-alt", "Meaningful images have alt text (WCAG 1.1.1)", False,
                      detail=str(a.meaningful_images_missing_alt[:8])))
    if a.decorative_images_exposed:
        out.append(af("decorative-image", "Decorative images are hidden from assistive tech", False,
                      detail=str(a.decorative_images_exposed[:8])))

    # -- forms (§21) ---------------------------------------
    if a.unlabelled_field_refs:
        out.append(af("form-label", "Every form field has a programmatic label", False,
                      detail=str(a.unlabelled_field_refs[:8])))
    if a.unassociated_error_refs:
        out.append(af("form-error-association",
                      "Form errors are programmatically associated with their field", False,
                      detail=str(a.unassociated_error_refs[:8])))

    # -- dialogs (§23) — deterministic portion ------------------
    for d in a.dialogs:
        ref = d.get("ref", "dialog")
        ok = (d.get("role") in ("dialog", "alertdialog") and d.get("has_name", False)
              and d.get("initial_focus", False) and d.get("escape_closes", False)
              and d.get("focus_returns", False))
        out.append(af("dialog.%s" % ref,
                      "Dialog '%s': role, name, initial focus, Escape, focus return" % ref, ok,
                      detail=str({k: d.get(k) for k in ("role", "has_name", "initial_focus",
                                                        "escape_closes", "focus_returns")})))

    # -- reduced motion (§18) — reuse V2.8 §15 result -----------
    if obs.reduced_motion and obs.reduced_motion_hidden_content:
        out.append(af("reduced-motion-trap",
                      "No content trapped behind motion under prefers-reduced-motion", False,
                      detail=str(obs.reduced_motion_hidden_content[:6]),
                      owning_spec="MOTION-DIRECTION-PROTOCOL.md / BROWSER-REGRESSION-QA-PROTOCOL.md §15"))

    # -- screen reader (§30) — never auto-PASS ------------------
    if a.screen_reader_status == "SCREEN_READER_UNAVAILABLE":
        out.append(Finding(check_id="a11y.screen-reader",
                           title="Screen-reader smoke review", verdict="BLOCKED",
                           requirement_source=S, route=obs.route, viewport=obs.viewport,
                           detail="BLOCKED_SCREEN_READER_ENVIRONMENT", method="BROWSER_EXECUTED"))
    elif a.screen_reader_status == "COMPLETED":
        out.append(af("screen-reader", "Screen-reader smoke review completed", True,
                      detail="MANUAL_VERIFIED"))

    # -- manual keyboard result gates a full PASS (§41 P) -------
    if a.manual_keyboard_result == "FAIL":
        out.append(af("manual-keyboard", "Manual keyboard walkthrough passed", False,
                      detail="engine may be clean, but the manual keyboard review FAILED — "
                             "overall accessibility verification is not a full PASS"))
    elif a.manual_keyboard_result == "PASS":
        out.append(af("manual-keyboard", "Manual keyboard walkthrough passed", True,
                      detail="MANUAL_VERIFIED"))

    if not out:
        out.append(af("baseline", "Accessibility checks pass for %s" % obs.route, True))
    return out


ALL_CHECKS = [
    check_horizontal_overflow,
    check_clipped_and_zero_targets,
    check_placeholder_hash_links,
    check_broken_internal_links,
    check_mobile_nav,
    check_console_clean,
    check_network,
    check_assets,
    check_forms,
    check_measurement,
    check_security_privacy,
    check_reduced_motion,
    check_keyboard,
    check_visual_regression,
    check_perf,
    check_localization,
    check_accessibility,
]
