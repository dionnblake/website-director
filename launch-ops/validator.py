"""Deterministic Launch & Post-Launch Operations validators (Website Director V2.10).

Canonical policy: ``../LAUNCH-OPERATIONS-PROTOCOL.md``.

Nothing here deploys, pushes, resolves DNS, opens a socket, or launches a
browser. Every function takes plain dicts (the ``launch_ops{}`` state object and
a ``launch-evidence-manifest`` payload) and returns ``Finding`` records with a
verdict from the shared vocabulary. The caller decides what to do with them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Verdict vocabulary -- identical to browser-qa/engine/base.py so evidence
# manifests read the same across subsystems. (FLAKY is browser-only.)
# ---------------------------------------------------------------------------
PASS = "PASS"
FAIL = "FAIL"
BLOCKED = "BLOCKED"
NOT_APPLICABLE = "NOT_APPLICABLE"
NOT_EVALUATED = "NOT_EVALUATED"
VERDICTS = (PASS, FAIL, BLOCKED, NOT_APPLICABLE, NOT_EVALUATED)

# ---------------------------------------------------------------------------
# Status model (LAUNCH-OPERATIONS-PROTOCOL.md sec 7) and the allowed
# transition graph (sec 22 / SKILL.md sec 5.17).
# ---------------------------------------------------------------------------
LAUNCH_STATUSES = (
    "NOT_EVALUATED",
    "PLANNING",
    "BLOCKED",
    "RELEASE_READY",
    "AWAITING_DEPLOYMENT_AUTHORIZATION",
    "DEPLOYMENT_AUTHORIZED",
    "DEPLOYING",
    "DEPLOYED",
    "PRODUCTION_VERIFICATION_RUNNING",
    "PRODUCTION_VERIFICATION_FAILED",
    "PRODUCTION_VERIFIED",
    "POST_LAUNCH_MONITORING",
    "STABILIZED",
    "ROLLBACK_REQUIRED",
    "ROLLED_BACK",
    "EXCEPTION_APPLIED",
)

# A directed graph. Absent key => terminal-ish / only self. Failure and
# rollback edges are explicit; impossible jumps (NOT_EVALUATED -> STABILIZED)
# are simply not present.
STATE_TRANSITIONS: Dict[str, tuple] = {
    "NOT_EVALUATED": ("PLANNING", "EXCEPTION_APPLIED"),
    "PLANNING": ("PLANNING", "BLOCKED", "RELEASE_READY", "EXCEPTION_APPLIED"),
    "BLOCKED": ("PLANNING", "BLOCKED", "RELEASE_READY", "EXCEPTION_APPLIED"),
    "RELEASE_READY": ("AWAITING_DEPLOYMENT_AUTHORIZATION", "BLOCKED", "PLANNING",
                      "EXCEPTION_APPLIED"),
    "AWAITING_DEPLOYMENT_AUTHORIZATION": ("DEPLOYMENT_AUTHORIZED", "BLOCKED",
                                         "RELEASE_READY", "EXCEPTION_APPLIED"),
    "DEPLOYMENT_AUTHORIZED": ("DEPLOYING", "BLOCKED", "EXCEPTION_APPLIED"),
    "DEPLOYING": ("DEPLOYED", "PRODUCTION_VERIFICATION_FAILED", "ROLLBACK_REQUIRED",
                  "BLOCKED"),
    "DEPLOYED": ("PRODUCTION_VERIFICATION_RUNNING", "ROLLBACK_REQUIRED", "BLOCKED"),
    "PRODUCTION_VERIFICATION_RUNNING": ("PRODUCTION_VERIFIED",
                                        "PRODUCTION_VERIFICATION_FAILED",
                                        "ROLLBACK_REQUIRED"),
    "PRODUCTION_VERIFICATION_FAILED": ("PRODUCTION_VERIFICATION_RUNNING",
                                      "ROLLBACK_REQUIRED", "BLOCKED",
                                      "DEPLOYMENT_AUTHORIZED"),
    "PRODUCTION_VERIFIED": ("POST_LAUNCH_MONITORING", "ROLLBACK_REQUIRED"),
    "POST_LAUNCH_MONITORING": ("STABILIZED", "ROLLBACK_REQUIRED",
                               "PRODUCTION_VERIFICATION_RUNNING"),
    "STABILIZED": ("STABILIZED", "ROLLBACK_REQUIRED"),
    "ROLLBACK_REQUIRED": ("ROLLED_BACK", "BLOCKED"),
    "ROLLED_BACK": ("PLANNING", "RELEASE_READY", "BLOCKED", "EXCEPTION_APPLIED"),
    "EXCEPTION_APPLIED": ("EXCEPTION_APPLIED", "PLANNING"),
}

# Things that DO NOT constitute deployment authorization (protocol sec 4).
NON_AUTHORIZING_SIGNALS = (
    "qa_passed", "browser_qa_passed", "implementation_complete", "design_approved",
    "gauntlet_pass", "owner_said_looks_good", "prior_project_authorization",
    "previous_release_authorization", "production_preflight_passed",
)

SEVERITY_ORDER = ("SEV3_LOW", "SEV2_MODERATE", "SEV1_HIGH", "SEV0_CRITICAL")


@dataclass
class Finding:
    check_id: str
    verdict: str
    detail: str = ""
    blocker: bool = False
    evidence_ref: Optional[str] = None
    method: str = "DETERMINISTIC"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "check": self.check_id,
            "result": self.verdict,
            "detail": self.detail,
            "blocker": self.blocker,
            "evidence_ref": self.evidence_ref,
            "method": self.method,
        }


# ---------------------------------------------------------------------------
# State-transition validation
# ---------------------------------------------------------------------------
def validate_transition(src: str, dst: str) -> Finding:
    """One hop. FAIL for an unknown state or a disallowed edge."""
    if src not in LAUNCH_STATUSES:
        return Finding("launch.transition", FAIL, "unknown source status %r" % src, blocker=True)
    if dst not in LAUNCH_STATUSES:
        return Finding("launch.transition", FAIL, "unknown target status %r" % dst, blocker=True)
    allowed = STATE_TRANSITIONS.get(src, ())
    if dst in allowed:
        return Finding("launch.transition", PASS, "%s -> %s" % (src, dst))
    return Finding("launch.transition", FAIL,
                   "illegal transition %s -> %s (allowed: %s)" % (src, dst, ", ".join(allowed) or "none"),
                   blocker=True)


def validate_transition_path(path: List[str]) -> Finding:
    """A whole ordered history. FAIL on the first illegal hop."""
    if not path:
        return Finding("launch.transition-path", NOT_EVALUATED, "empty path")
    for a, b in zip(path, path[1:]):
        hop = validate_transition(a, b)
        if hop.verdict != PASS:
            return Finding("launch.transition-path", FAIL, hop.detail, blocker=True)
    return Finding("launch.transition-path", PASS, " -> ".join(path))


# ---------------------------------------------------------------------------
# Release-readiness gate  (launch_ops.complete)
# ---------------------------------------------------------------------------
def evaluate_release_readiness(lo: Dict[str, Any], *, rollback_required: bool = True) -> List[Finding]:
    """Can the candidate legitimately request deployment authorization?

    ``launch_ops.complete`` may be true only when every finding here is PASS /
    NOT_APPLICABLE. It never means deployed and never means production verified.
    """
    out: List[Finding] = []
    exc = (lo.get("exception") or {}).get("applied") is True

    # Release candidate identity must be immutable and complete (protocol sec 8).
    ident_ok = bool(lo.get("release_candidate_ready")) and bool(lo.get("release_sha")) \
        and bool(lo.get("release_version"))
    out.append(Finding("launch.release_identity",
                       PASS if ident_ok else FAIL,
                       "release_sha=%s release_version=%s candidate_ready=%s"
                       % (lo.get("release_sha"), lo.get("release_version"),
                          lo.get("release_candidate_ready")),
                       blocker=not ident_ok))

    out.append(Finding("launch.deployment_target",
                       PASS if lo.get("deployment_target") else FAIL,
                       "deployment_target=%s provider=%s" % (lo.get("deployment_target"),
                                                             lo.get("deployment_provider")),
                       blocker=not lo.get("deployment_target")))

    out.append(Finding("launch.environment_ready",
                       PASS if lo.get("environment_ready") else FAIL,
                       "environment_ready=%s" % lo.get("environment_ready"),
                       blocker=not lo.get("environment_ready")))

    # Rollback readiness must exist BEFORE authorization where practical
    # (protocol sec 25). ``rollback_tested`` is a separate, stronger state.
    if rollback_required:
        rb = bool(lo.get("rollback_ready"))
        out.append(Finding("launch.rollback_ready",
                           PASS if rb else FAIL,
                           "rollback_ready=%s rollback_tested=%s"
                           % (lo.get("rollback_ready"), lo.get("rollback_tested")),
                           blocker=not rb))
    else:
        out.append(Finding("launch.rollback_ready", NOT_APPLICABLE,
                           "rollback not required for this deployment class"))

    # Monitoring readiness decision must be made, not skipped (protocol sec 23).
    mon = lo.get("monitoring_ready")
    mon_decl = lo.get("monitoring_requirement") in ("NOT_REQUIRED", "BASIC_REQUIRED",
                                                    "APPLICATION_MONITORING_REQUIRED")
    out.append(Finding("launch.monitoring_ready",
                       PASS if (mon or mon_decl) else FAIL,
                       "monitoring_requirement=%s monitoring_ready=%s"
                       % (lo.get("monitoring_requirement"), mon),
                       blocker=not (mon or mon_decl)))

    # The candidate must NOT already claim deployed / verified at readiness time.
    premature = lo.get("deployed") or lo.get("production_browser_verified") \
        or lo.get("production_measurement_verified")
    out.append(Finding("launch.not_prematurely_deployed",
                       FAIL if premature else PASS,
                       "deployed=%s -- release readiness never means deployed"
                       % lo.get("deployed"),
                       blocker=bool(premature)))

    if exc:
        # An applied exception is a valid gate-engaged state; the exception is
        # the deliverable. It still must carry a reason.
        reason = (lo.get("exception") or {}).get("reason")
        out.append(Finding("launch.exception",
                           PASS if reason else FAIL,
                           "exception.reason=%s" % reason, blocker=not reason))
    return out


def release_ready(findings: List[Finding]) -> bool:
    return all(f.verdict in (PASS, NOT_APPLICABLE, NOT_EVALUATED) for f in findings)


# ---------------------------------------------------------------------------
# Owner deployment-authorization boundary  (protocol sec 4)
# ---------------------------------------------------------------------------
def evaluate_deployment_authorization(lo: Dict[str, Any],
                                     signals: Optional[Dict[str, Any]] = None,
                                     *, durable_policy: bool = False) -> Finding:
    """Deployment proceeds only on explicit per-release owner authorization
    (or a separate durable deployment policy). QA passing, an approved design,
    "looks good", or a prior authorization never imply it.
    """
    signals = signals or {}
    leaned_on = [k for k in NON_AUTHORIZING_SIGNALS if signals.get(k)]
    explicit = lo.get("deployment_authorized") is True
    auth_ref = lo.get("deployment_authorization_ref") or lo.get("authorized_by")

    if explicit and (auth_ref or durable_policy):
        return Finding("launch.deployment_authorization", PASS,
                       "explicit owner authorization recorded (ref=%s, durable_policy=%s)"
                       % (auth_ref, durable_policy))
    if explicit and not auth_ref and not durable_policy:
        return Finding("launch.deployment_authorization", FAIL,
                       "deployment_authorized=true but no authorization reference / "
                       "durable policy recorded", blocker=True)
    if leaned_on:
        return Finding("launch.deployment_authorization", FAIL,
                       "deployment inferred from non-authorizing signal(s): %s"
                       % ", ".join(leaned_on), blocker=True)
    return Finding("launch.deployment_authorization", BLOCKED,
                   "no explicit owner deployment authorization for this release", blocker=True)


# ---------------------------------------------------------------------------
# Production verification  (protocol sec 12-22, 36, 37)
# ---------------------------------------------------------------------------
_STAGING_MARKERS = ("localhost", "127.0.0.1", "0.0.0.0", ".local", "staging.",
                    "preview.", "vercel.app", "netlify.app", "pages.dev",
                    "ngrok", "-staging", "test.", "dev.")


def _looks_like_staging(url: str) -> bool:
    u = (url or "").lower()
    return any(m in u for m in _STAGING_MARKERS)


def evaluate_production_verification(lo: Dict[str, Any],
                                    manifest: Dict[str, Any]) -> List[Finding]:
    """Verify a *known release identity* on the *production* surface.

    ``manifest`` is a launch-evidence-manifest payload (see
    templates/launch-evidence-manifest.json).
    """
    out: List[Finding] = []
    env = manifest.get("environment")
    prod_url = manifest.get("production_url") or lo.get("production_domain") or ""

    # 0. Never verify "whatever is on the server" -- match the deployed artifact.
    expected = lo.get("release_sha")
    deployed = manifest.get("deployed_sha") or lo.get("deployed_sha")
    if not expected:
        out.append(Finding("launch.release_sha_match", BLOCKED,
                           "no expected release_sha recorded", blocker=True))
    elif not deployed:
        out.append(Finding("launch.release_sha_match", BLOCKED,
                           "DEPLOYED_IDENTITY = UNVERIFIED (platform exposed no build id)",
                           blocker=True))
    elif str(deployed) != str(expected):
        out.append(Finding("launch.release_sha_match", FAIL,
                           "deployed_sha %s != expected release_sha %s" % (deployed, expected),
                           blocker=True))
    else:
        out.append(Finding("launch.release_sha_match", PASS,
                           "deployed_sha matches release_sha %s" % expected))

    # 1. Staging is never production.
    if env != "production":
        out.append(Finding("launch.environment_is_production", FAIL,
                           "evidence environment=%r -- a staging/preview pass is not "
                           "production verification" % env, blocker=True))
    elif _looks_like_staging(prod_url):
        out.append(Finding("launch.environment_is_production", FAIL,
                           "production_url %r resolves to a staging/preview host" % prod_url,
                           blocker=True))
    else:
        out.append(Finding("launch.environment_is_production", PASS,
                           "production surface %s" % prod_url))

    checks = manifest.get("checks", {}) or {}

    def _c(cid: str, key: str, na_ok: bool = False):
        raw = checks.get(key)
        if raw is None:
            out.append(Finding(cid, NOT_APPLICABLE if na_ok else BLOCKED,
                               "no evidence for %r" % key, blocker=not na_ok))
            return
        val = raw.get("result") if isinstance(raw, dict) else raw
        detail = raw.get("detail", "") if isinstance(raw, dict) else ""
        ref = raw.get("evidence_ref") if isinstance(raw, dict) else None
        if val in (PASS, "PASS", True):
            out.append(Finding(cid, PASS, detail or key, evidence_ref=ref))
        elif val in (NOT_APPLICABLE, "NOT_APPLICABLE", "NA"):
            out.append(Finding(cid, NOT_APPLICABLE, detail or key, evidence_ref=ref))
        elif val in (BLOCKED, "BLOCKED"):
            out.append(Finding(cid, BLOCKED, detail or key, evidence_ref=ref, blocker=True))
        else:
            out.append(Finding(cid, FAIL, detail or ("%s = %s" % (key, val)),
                               evidence_ref=ref, blocker=True))

    # HTTPS / TLS (protocol sec 13)
    _c("launch.https", "https")
    _c("launch.http_redirect", "http_to_https_redirect")
    _c("launch.mixed_content", "no_mixed_content")

    # Domain / redirects (sec 12, 14)
    _c("launch.dns_resolves", "dns_resolves")
    _c("launch.canonical_redirect", "www_apex_canonical")
    _c("launch.redirects", "redirect_map")

    # SEO launch verification (sec 19) -- production canonical / robots
    canonical = checks.get("seo_canonical")
    if isinstance(canonical, dict):
        cval = canonical.get("target") or canonical.get("detail") or ""
        if canonical.get("result") in (FAIL, "FAIL") or _looks_like_staging(str(cval)):
            out.append(Finding("launch.seo_canonical", FAIL,
                               "production canonical points to non-production host: %s" % cval,
                               blocker=True))
        else:
            out.append(Finding("launch.seo_canonical", PASS, "canonical=%s" % cval))
    else:
        out.append(Finding("launch.seo_canonical", BLOCKED, "no canonical evidence", blocker=True))

    robots = checks.get("seo_robots")
    if isinstance(robots, dict):
        noindex = robots.get("noindex") is True or "noindex" in str(robots.get("detail", "")).lower()
        out.append(Finding("launch.seo_indexable",
                           FAIL if noindex else PASS,
                           "staging noindex still present on production" if noindex
                           else "production is indexable per spec",
                           blocker=noindex))
    else:
        out.append(Finding("launch.seo_indexable", BLOCKED, "no robots/indexability evidence",
                           blocker=True))

    _c("launch.seo_sitemap", "seo_sitemap", na_ok=True)
    _c("launch.seo_og", "seo_open_graph", na_ok=True)
    _c("launch.custom_404", "custom_404", na_ok=True)

    # Production browser QA (sec 15) -- delegated result from browser-qa in
    # environment=production; here we only confirm it was that, not local.
    bq = checks.get("production_browser_qa")
    if isinstance(bq, dict):
        if bq.get("environment") not in (None, "production"):
            out.append(Finding("launch.production_browser_qa", FAIL,
                               "browser QA evidence environment=%r (not production)"
                               % bq.get("environment"), blocker=True))
        else:
            _c("launch.production_browser_qa", "production_browser_qa")
    else:
        _c("launch.production_browser_qa", "production_browser_qa")

    # Accessibility production re-check (sec 16) -- delegated field only.
    _c("launch.production_accessibility", "production_accessibility", na_ok=True)

    # Security / privacy production realization (sec 17)
    _c("launch.security_headers", "security_headers")
    _c("launch.third_party_scripts_match", "third_party_scripts_match")
    _c("launch.consent_gating", "consent_gating", na_ok=True)

    # Measurement production verification (sec 18)
    _c("launch.analytics_loads", "analytics_loads")
    _c("launch.analytics_environment", "analytics_environment")
    _c("launch.no_duplicate_conversion", "no_duplicate_conversion")
    _c("launch.analytics_consent_gated", "analytics_consent_gated", na_ok=True)
    _c("launch.utm_preserved", "utm_preserved", na_ok=True)

    # Forms / integrations (sec 20) -- config-only, never a real submission.
    forms = checks.get("forms_config")
    if isinstance(forms, dict):
        real = forms.get("real_submission_sent") is True
        if real and not forms.get("production_test_authorized"):
            out.append(Finding("launch.forms_config", FAIL,
                               "a real production form submission was sent without "
                               "explicit production-test authorization", blocker=True))
        else:
            _c("launch.forms_config", "forms_config")
    else:
        _c("launch.forms_config", "forms_config", na_ok=True)

    # Cache / CDN (sec 21) and production assets (sec 22)
    _c("launch.cache_cdn", "cache_cdn", na_ok=True)
    _c("launch.critical_assets", "critical_assets")

    # Monitoring + rollback readiness re-confirmed at production
    _c("launch.monitoring_active", "monitoring_active", na_ok=True)
    _c("launch.rollback_ready_confirmed", "rollback_ready", na_ok=False)

    return out


def production_verified(findings: List[Finding], lo: Dict[str, Any],
                        manifest: Dict[str, Any]) -> bool:
    """A localhost/staging manifest can never set production_verified."""
    if manifest.get("environment") != "production":
        return False
    if _looks_like_staging(manifest.get("production_url") or lo.get("production_domain") or ""):
        return False
    return all(f.verdict in (PASS, NOT_APPLICABLE) for f in findings)


# ---------------------------------------------------------------------------
# Rollback trigger evaluation  (protocol sec 27)
# ---------------------------------------------------------------------------
DEFAULT_ROLLBACK_TRIGGERS = {
    "site_unavailable": "SEV0_CRITICAL",
    "critical_route_failure": "SEV0_CRITICAL",
    "primary_conversion_broken": "SEV1_HIGH",
    "checkout_failure": "SEV0_CRITICAL",
    "authentication_failure": "SEV0_CRITICAL",
    "sensitive_data_exposure": "SEV0_CRITICAL",
    "privacy_security_regression": "SEV1_HIGH",
    "severe_js_errors": "SEV1_HIGH",
    "accessibility_blocker_introduced": "SEV1_HIGH",
    "severe_visual_break_core_routes": "SEV1_HIGH",
    "release_identity_mismatch": "SEV1_HIGH",
    "secondary_feature_failure": "SEV2_MODERATE",
    "isolated_route_issue": "SEV2_MODERATE",
    "cosmetic_discrepancy": "SEV3_LOW",
}


def evaluate_rollback_trigger(incident: Dict[str, Any],
                              triggers: Optional[Dict[str, str]] = None) -> Finding:
    """Concrete, explicit criteria -- never "rollback if something looks bad"."""
    triggers = {**DEFAULT_ROLLBACK_TRIGGERS, **(triggers or {})}
    kind = incident.get("trigger") or incident.get("symptom_class")
    sev = incident.get("severity") or triggers.get(kind)
    if kind is None and sev is None:
        return Finding("launch.rollback_trigger", NOT_EVALUATED,
                       "incident carries no trigger class or severity")
    if sev not in SEVERITY_ORDER:
        return Finding("launch.rollback_trigger", FAIL,
                       "unknown severity %r" % sev, blocker=True)
    if sev in ("SEV0_CRITICAL", "SEV1_HIGH"):
        return Finding("launch.rollback_trigger", FAIL,
                       "incident %r (%s) meets a defined rollback trigger -> "
                       "ROLLBACK_REQUIRED" % (kind, sev), blocker=True)
    return Finding("launch.rollback_trigger", PASS,
                   "incident %r (%s) is below the rollback threshold -- triage, do not roll back"
                   % (kind, sev))
