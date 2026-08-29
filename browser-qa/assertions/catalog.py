"""The browser QA assertion catalogue.

Grouped by protocol section. Each function returns ``None`` (not applicable to
this observation), one ``Finding``, or a list of ``Finding``. Register new checks
by appending to ``ALL_CHECKS`` at the bottom.
"""

from __future__ import annotations

import re
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
]
