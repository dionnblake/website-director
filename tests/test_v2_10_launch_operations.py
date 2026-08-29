# Website Director V2.10 Launch & Post-Launch Operations Test Harness
#
# 1. Repository invariants -- one canonical launch protocol, one completion flag
#    (launch_ops.complete), five owner locks (no launch/deploy/rollback lock),
#    cross-document wiring, no false deployment / production-verified claims.
# 2. Negative controls (protocol sec 49 / sec 50) -- every launch guard proven
#    to FAIL / BLOCK on a deliberately broken synthetic fixture, the state
#    machine proven to reject impossible transitions, and production_verified
#    proven unreachable from a localhost / staging manifest.
#
# Runs with only the standard library. Run: python tests/test_v2_10_launch_operations.py

import io
import json
import os
import re
import sys

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WORKSPACE, "launch-ops"))
sys.path.insert(0, os.path.join(WORKSPACE, "browser-qa"))

from validator import (  # noqa: E402
    BLOCKED,
    FAIL,
    NOT_APPLICABLE,
    PASS,
    LAUNCH_STATUSES,
    evaluate_deployment_authorization,
    evaluate_production_verification,
    evaluate_release_readiness,
    evaluate_rollback_trigger,
    production_verified,
    release_ready,
    validate_transition,
    validate_transition_path,
)
from guards.frozen_integrity_guard import FrozenIntegrityGuard  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
except Exception:  # noqa: BLE001
    pass

runs = passed = 0
failures = []


def check(cond, msg):
    global runs, passed
    runs += 1
    if cond:
        passed += 1
        print("[PASS] " + msg)
    else:
        failures.append(msg)
        print("[FAIL] " + msg)


def read(*p):
    with io.open(os.path.join(WORKSPACE, *p), encoding="utf-8") as f:
        return f.read()


def exists(*p):
    return os.path.exists(os.path.join(WORKSPACE, *p))


def ver_ge(text, lo=(2, 10, 0), prefix=r"> \*\*Version:\*\* "):
    m = re.search(r"^%s(\d+)\.(\d+)\.(\d+)" % prefix, text, re.M)
    return bool(m) and tuple(int(x) for x in m.groups()) >= lo


def verdict(findings, cid):
    for f in findings:
        if f.check_id == cid:
            return f.verdict
    return None


guard = FrozenIntegrityGuard(WORKSPACE, ["projects/"], run_id="v2_10_launch_operations")
guard.snapshot()

# ===========================================================================
# 1. Repository invariants
# ===========================================================================
PROTOCOL = "LAUNCH-OPERATIONS-PROTOCOL.md"
PLAN = os.path.join("templates", "launch-plan.md")
MANIFEST = os.path.join("templates", "launch-evidence-manifest.json")
VALIDATION = os.path.join("examples", "LAUNCH-OPERATIONS-INTEGRATION-VALIDATION.md")

check(exists(PROTOCOL), "Canonical %s exists" % PROTOCOL)
check(exists(PLAN), "templates/launch-plan.md exists")
check(exists(MANIFEST), "templates/launch-evidence-manifest.json exists")
check(exists(VALIDATION), "Integration validation artifact exists")
check(exists("launch-ops/validator.py"), "launch-ops/validator.py exists")

proto = read(PROTOCOL)
for token in ("[RELEASE_READY]", "launch_ops.complete", "DEPLOYMENT_AUTHORIZED",
              "No second, independently-writable completion flag",
              "not** a sixth owner/design lock", "DEPLOYED_IDENTITY = UNVERIFIED",
              "Website Director does not deploy", "FrozenIntegrityGuard",
              'environment = "production"', "ROLLBACK_REQUIRED",
              "does **not** mean deployed", "Post-launch"):
    check(token in proto, "Protocol declares %r" % token)

# exactly one canonical launch protocol at repo root
root_md = [f for f in os.listdir(WORKSPACE) if f.endswith(".md")]
launch_protocols = [f for f in root_md
                    if re.search(r"LAUNCH|DEPLOY|RELEASE", f) and f.endswith("PROTOCOL.md")]
check(launch_protocols == [PROTOCOL], "Exactly one canonical launch protocol at root: %s" % launch_protocols)

# ---- no false deployment / production-verified claims ---------------------
BANNED = ["DEPLOYMENT COMPLETE", "SITE IS LIVE", "PRODUCTION VERIFIED FROM LOCALHOST",
          "DEPLOY VERIFIED", "LAUNCH GUARANTEED", "ZERO DOWNTIME GUARANTEED"]
scan = list(root_md)
scan += [os.path.join("templates", f) for f in os.listdir(os.path.join(WORKSPACE, "templates")) if f.endswith(".md")]
scan += [os.path.join("examples", f) for f in os.listdir(os.path.join(WORKSPACE, "examples")) if f.endswith(".md")]
NEG = ("never", "Never", "not ", "no ", "No ", "without", "unless", "NOT", "does not",
       "must not", "prohibit", "Prohibit", "boundary", "≠", "!=")
bad = []
for rel in scan:
    lines = read(rel).splitlines()
    for i, line in enumerate(lines):
        for b in BANNED:
            if b in line.upper() and not any(m in probe for probe in lines[max(0, i - 6):i + 1] for m in NEG):
                bad.append("%s :: %s" % (rel, line.strip()[:90]))
check(not bad, "No framework document makes a false deployment/launch claim (violations: %s)" % (bad or "none"))

# ---- state object -------------------------------------------------------
profile = json.loads(read("templates", "site-profile.json"))
check(profile.get("schema_version") == "2.10.0", "site-profile.json schema_version == 2.10.0")
check("launch_ops" in profile, "site-profile.json contains launch_ops{}")
lo0 = profile.get("launch_ops", {})
check(lo0.get("complete") is False, "launch_ops.complete defaults to false")
check(lo0.get("status") == "NOT_EVALUATED", "launch_ops.status defaults to NOT_EVALUATED")
check(lo0.get("deployed") is False, "launch_ops.deployed defaults to false")
check(lo0.get("deployment_authorized") is False, "launch_ops.deployment_authorized defaults to false")
for pv in ("production_browser_verified", "production_accessibility_verified",
           "production_security_privacy_verified", "production_measurement_verified",
           "production_seo_verified", "production_forms_verified"):
    check(lo0.get(pv) is False, "launch_ops.%s defaults to false" % pv)
check(lo0.get("rollback_ready") is False and lo0.get("rollback_tested") is False,
      "launch_ops rollback flags default false and are distinct fields")
check(isinstance(lo0.get("known_incidents"), list), "launch_ops.known_incidents is a list")
check(lo0.get("exception", {}).get("applied") is False, "launch_ops.exception.applied defaults false")

locks = profile.get("locks", {})
check(len(locks) == 5, "Exactly 5 owner locks (found %d)" % len(locks))
check(not any(s in k.lower() for k in locks for s in ("launch", "deploy", "rollback", "release")),
      "No sixth launch/deploy/rollback owner lock")
check(not any(isinstance(vv, bool) and "lock" in k for k, vv in lo0.items()),
      "launch_ops{} contains no lock boolean")
owners = [k for k, vv in profile.items() if isinstance(vv, dict) and "complete" in vv]
check(owners.count("launch_ops") == 1, "Exactly one launch completion flag in the schema")
check("browser_qa" in profile and "measurement" in profile and "security_privacy" in profile
      and "accessibility" in profile, "V2.6-V2.9 state objects preserved")

# ---- no separate runner -------------------------------------------------
check(not exists("launch-qa") and not exists("launch-runner.py") and not exists("deploy-runner.py"),
      "No separate launch/deploy runner was created")
check("browser-qa/runner.py" and 'environment' in read("browser-qa", "runner.py"),
      "Production Browser QA reuses the V2.8 harness (environment mode already present)")

# ---- cross-document wiring --------------------------------------------
skill = read("SKILL.md")
check("PHASE 12.25" in skill, "SKILL.md declares PHASE 12.25")
check("[RELEASE_READY]" in skill, "SKILL.md declares the RELEASE_READY gate")
check("GATE LAUNCH" in skill, "SKILL.md workflow diagram includes GATE LAUNCH")
check("Single-Source-of-Truth Rule for `launch_ops`" in skill, "SKILL.md documents the launch_ops SoT rule")
check(ver_ge(skill), "SKILL.md version >= 2.10.0")
check("RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED" in skill, "SKILL.md restates the authorization boundary")
check("Exactly 5 owner locks remain immutable" in skill, "SKILL.md restates the five-lock invariant")

contract = read("IMPLEMENTATION-CONTRACT.md")
check("Launch Requirements (V2.10)" in contract, "IMPLEMENTATION-CONTRACT.md adds §2.9 launch requirements")
check(ver_ge(contract, lo=(1, 7, 0)), "IMPLEMENTATION-CONTRACT.md version >= 1.7.0")
check("Unauthorized Deployment" in contract and "Staging Marked Production" in contract,
      "Implementation contract adds launch prohibitions")

checklist = read("PRODUCTION-CHECKLIST.md")
check("Launch & Post-Launch Operations Boundary (V2.10)" in checklist,
      "PRODUCTION-CHECKLIST.md adds §11 launch boundary")
check(ver_ge(checklist, lo=(1, 7, 0)), "PRODUCTION-CHECKLIST.md version >= 1.7.0")
check("RELEASE_READY" in checklist and "DEPLOYMENT_AUTHORIZED" in checklist,
      "Production checklist distinguishes candidate readiness from deployment authorization")

handoff = read("CLIENT-CMS-HANDOFF-PROTOCOL.md")
check("Launch Operations Intake (V2.10)" in handoff, "CLIENT-CMS-HANDOFF-PROTOCOL.md adds §13 intake")
check("handoff_transferred" in handoff, "Handoff protocol references launch_ops.handoff_transferred")

bqa = read("BROWSER-REGRESSION-QA-PROTOCOL.md")
check("Launch Operations (V2.10) reuses this harness" in bqa,
      "Browser QA protocol notes the V2.10 production-mode reuse -- no second runner")

readme = read("README.md")
check("V2.10" in readme and "Launch" in readme, "README documents the V2.10 subsystem")
agents = read("AGENTS.md")
check(ver_ge(agents, prefix=r"\*\*Version:\*\* "), "AGENTS.md version >= 2.10.0")
check("Launch" in agents and "V2.10" in agents, "AGENTS.md adds V2.10 governance")

# ---- no secrets --------------------------------------------------------
SEC = re.compile(r"AKIA[0-9A-Z]{16}|sk_live_[0-9a-zA-Z]{16,}|ghp_[0-9A-Za-z]{30,}|"
                 r"AIza[0-9A-Za-z\-_]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
new_files = [PROTOCOL, PLAN, MANIFEST, VALIDATION, "launch-ops/validator.py", "launch-ops/__init__.py",
             "SKILL.md", "README.md", "AGENTS.md", "IMPLEMENTATION-CONTRACT.md",
             "PRODUCTION-CHECKLIST.md", "CLIENT-CMS-HANDOFF-PROTOCOL.md",
             os.path.join("templates", "site-profile.json")]
check(not [f for f in new_files if SEC.search(read(f))], "No secret-shaped material in any V2.10 file")

# ---- all repo JSON valid --------------------------------------------
badj = []
for r, d, fs in os.walk(WORKSPACE):
    d[:] = [x for x in d if x not in (".git", "node_modules", "__pycache__", ".chrome_test_profile", "scratch")]
    for fn in fs:
        if fn.endswith(".json"):
            try:
                json.load(io.open(os.path.join(r, fn), encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                badj.append("%s (%s)" % (os.path.relpath(os.path.join(r, fn), WORKSPACE), type(e).__name__))
check(not badj, "All repository JSON parses (invalid: %s)" % (badj or "none"))

# ===========================================================================
# 2. State-machine invariants
# ===========================================================================
check(len(LAUNCH_STATUSES) == 16, "16 launch statuses defined")
check(validate_transition("NOT_EVALUATED", "PLANNING").verdict == PASS, "NOT_EVALUATED -> PLANNING legal")
check(validate_transition("NOT_EVALUATED", "STABILIZED").verdict == FAIL,
      "NOT_EVALUATED -> STABILIZED rejected (impossible jump)")
check(validate_transition("RELEASE_READY", "PRODUCTION_VERIFIED").verdict == FAIL,
      "RELEASE_READY -> PRODUCTION_VERIFIED rejected")
check(validate_transition("PLANNING", "DEPLOYED").verdict == FAIL, "PLANNING -> DEPLOYED rejected")
good_path = ["NOT_EVALUATED", "PLANNING", "RELEASE_READY", "AWAITING_DEPLOYMENT_AUTHORIZATION",
             "DEPLOYMENT_AUTHORIZED", "DEPLOYING", "DEPLOYED", "PRODUCTION_VERIFICATION_RUNNING",
             "PRODUCTION_VERIFIED", "POST_LAUNCH_MONITORING", "STABILIZED"]
check(validate_transition_path(good_path).verdict == PASS, "Canonical forward path is legal end-to-end")
check(validate_transition("DEPLOYED", "ROLLBACK_REQUIRED").verdict == PASS, "DEPLOYED -> ROLLBACK_REQUIRED legal")
check(validate_transition("ROLLBACK_REQUIRED", "ROLLED_BACK").verdict == PASS, "ROLLBACK_REQUIRED -> ROLLED_BACK legal")

# ===========================================================================
# 3. Negative controls (scenarios A-R)
# ===========================================================================
READY_LO = {
    "release_candidate_ready": True,
    "release_sha": "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678",
    "release_version": "1.0.0",
    "deployment_target": "STATIC_HOST",
    "deployment_provider": "OTHER",
    "environment_ready": True,
    "monitoring_requirement": "BASIC_REQUIRED",
    "monitoring_ready": True,
    "rollback_ready": True,
    "deployed": False,
}


def prod_manifest(**overrides):
    checks = {
        "dns_resolves": PASS, "https": PASS, "http_to_https_redirect": PASS,
        "no_mixed_content": PASS, "www_apex_canonical": PASS, "redirect_map": PASS,
        "production_browser_qa": {"result": PASS, "environment": "production"},
        "production_accessibility": PASS,
        "security_headers": PASS, "third_party_scripts_match": PASS, "consent_gating": PASS,
        "analytics_loads": PASS, "analytics_environment": PASS, "no_duplicate_conversion": PASS,
        "analytics_consent_gated": PASS, "utm_preserved": PASS,
        "seo_canonical": {"result": PASS, "target": "https://example.com/"},
        "seo_robots": {"result": PASS, "noindex": False},
        "seo_sitemap": PASS, "seo_open_graph": PASS, "custom_404": PASS,
        "forms_config": {"result": PASS, "real_submission_sent": False},
        "cache_cdn": PASS, "critical_assets": PASS, "monitoring_active": PASS, "rollback_ready": PASS,
    }
    checks.update(overrides.pop("checks", {}))
    m = {"environment": "production", "production_url": "https://example.com",
         "deployed_sha": READY_LO["release_sha"], "release_sha": READY_LO["release_sha"], "checks": checks}
    m.update(overrides)
    return m


# A. Local QA passed, never deployed
fa = evaluate_release_readiness(dict(READY_LO))
check(release_ready(fa), "A. Local QA passed candidate -> release readiness PASS")
check(READY_LO["deployed"] is False, "A. deployed = false")
check(evaluate_deployment_authorization(dict(READY_LO)).verdict == BLOCKED,
      "A. production_verified unreachable -- no deployment authorization yet -> BLOCKED")

# B. Deployment without owner authorization
check(evaluate_deployment_authorization({"deployment_authorized": False},
                                        signals={"qa_passed": True, "gauntlet_pass": True}).verdict == FAIL,
      "B. Deployment inferred from QA / Gauntlet pass -> FAIL")
check(evaluate_deployment_authorization({"deployment_authorized": True}).verdict == FAIL,
      "B'. deployment_authorized=true with no reference / durable policy -> FAIL")
check(evaluate_deployment_authorization({"deployment_authorized": True,
                                         "deployment_authorization_ref": "owner-note-2026-09-01"}).verdict == PASS,
      "B''. Explicit per-release owner authorization reference -> PASS")

# C. Release SHA mismatch
fc = evaluate_production_verification(dict(READY_LO), prod_manifest(deployed_sha="deadbeef" * 5))
check(verdict(fc, "launch.release_sha_match") == FAIL, "C. deployed_sha != release_sha -> FAIL")
fc2 = evaluate_production_verification(dict(READY_LO), prod_manifest(deployed_sha=None))
check(verdict(fc2, "launch.release_sha_match") == BLOCKED, "C'. Unprovable deployed identity -> BLOCKED (never assumed)")

# D. HTTPS failure
fd = evaluate_production_verification(dict(READY_LO), prod_manifest(checks={"https": FAIL}))
check(verdict(fd, "launch.https") == FAIL, "D. HTTPS failure -> FAIL")

# E. HTTP -> HTTPS redirect correct
fe = evaluate_production_verification(dict(READY_LO), prod_manifest())
check(verdict(fe, "launch.http_redirect") == PASS, "E. HTTP -> HTTPS redirect correct -> PASS")

# F. Production has staging noindex
ff = evaluate_production_verification(dict(READY_LO),
                                     prod_manifest(checks={"seo_robots": {"result": PASS, "noindex": True}}))
check(verdict(ff, "launch.seo_indexable") == FAIL, "F. Staging noindex on production -> SEO launch FAIL")

# G. Production canonical points to localhost/staging
fg = evaluate_production_verification(dict(READY_LO),
                                     prod_manifest(checks={"seo_canonical": {"result": PASS,
                                                                             "target": "http://localhost:3000/"}}))
check(verdict(fg, "launch.seo_canonical") == FAIL, "G. Canonical points to localhost -> FAIL")

# H. Analytics missing in production
fh = evaluate_production_verification(dict(READY_LO), prod_manifest(checks={"analytics_loads": FAIL}))
check(verdict(fh, "launch.analytics_loads") == FAIL, "H. Analytics missing in production -> measurement FAIL")

# I. Analytics fires duplicate conversion
fi = evaluate_production_verification(dict(READY_LO), prod_manifest(checks={"no_duplicate_conversion": FAIL}))
check(verdict(fi, "launch.no_duplicate_conversion") == FAIL, "I. Duplicate conversion event -> FAIL")

# J. Consent-dependent analytics fires before consent
fj = evaluate_production_verification(dict(READY_LO), prod_manifest(checks={"analytics_consent_gated": FAIL}))
check(verdict(fj, "launch.analytics_consent_gated") == FAIL, "J. Analytics fires before consent -> FAIL")

# K. Production form endpoint misconfigured (no real submission)
fk = evaluate_production_verification(dict(READY_LO),
                                     prod_manifest(checks={"forms_config": {"result": FAIL,
                                                                            "real_submission_sent": False}}))
check(verdict(fk, "launch.forms_config") == FAIL, "K. Misconfigured form endpoint -> FAIL without a real submission")
fk2 = evaluate_production_verification(dict(READY_LO),
                                      prod_manifest(checks={"forms_config": {"result": PASS,
                                                                             "real_submission_sent": True,
                                                                             "production_test_authorized": False}}))
check(verdict(fk2, "launch.forms_config") == FAIL,
      "K'. Real production submission without production-test authorization -> FAIL")

# L. Critical asset missing
fl = evaluate_production_verification(dict(READY_LO), prod_manifest(checks={"critical_assets": FAIL}))
check(verdict(fl, "launch.critical_assets") == FAIL, "L. Critical asset missing -> FAIL")

# M. Staging passes all checks -> production_verified = false
staging_manifest = prod_manifest(environment="staging", production_url="https://preview.example.com")
fm = evaluate_production_verification(dict(READY_LO), staging_manifest)
check(production_verified(fm, dict(READY_LO), staging_manifest) is False,
      "M. Perfect staging pass -> production_verified = false")
check(verdict(fm, "launch.environment_is_production") == FAIL, "M'. Staging manifest flagged not-production")

# N. Rollback plan absent where required
fn = evaluate_release_readiness({k: v for k, v in READY_LO.items() if k != "rollback_ready"})
check(not release_ready(fn), "N. Rollback plan absent (required) -> release readiness FAIL")
check(verdict(fn, "launch.rollback_ready") == FAIL, "N'. launch.rollback_ready is the failing check")
fn2 = evaluate_release_readiness({k: v for k, v in READY_LO.items() if k != "rollback_ready"},
                                 rollback_required=False)
check(verdict(fn2, "launch.rollback_ready") == NOT_APPLICABLE,
      "N''. Rollback genuinely not required -> NOT_APPLICABLE, gate not blocked")

# O. Post-launch critical incident -> ROLLBACK_REQUIRED
fo = evaluate_rollback_trigger({"trigger": "site_unavailable"})
check(fo.verdict == FAIL and "ROLLBACK_REQUIRED" in fo.detail, "O. SEV0 incident -> ROLLBACK_REQUIRED")
fo_low = evaluate_rollback_trigger({"trigger": "cosmetic_discrepancy"})
check(fo_low.verdict == PASS, "O'. Cosmetic discrepancy is below the rollback threshold -- triage, not rollback")

# P. Production Browser QA local/production confusion -> framework validation FAIL
fp = evaluate_production_verification(dict(READY_LO),
                                     prod_manifest(checks={"production_browser_qa": {"result": PASS,
                                                                                     "environment": "local"}}))
check(verdict(fp, "launch.production_browser_qa") == FAIL,
      "P. Browser QA evidence tagged environment=local inside a production manifest -> FAIL")

# Q. Sixth owner lock
check(set(profile["locks"]) == {"design_direction_locked", "information_architecture_locked",
                                "content_structure_locked", "design_system_locked",
                                "motion_direction_locked"},
      "Q. Exactly the five canonical owner locks, no launch/deploy/rollback lock")

# R. Frozen pilot mutation -> V2.8 FrozenIntegrityGuard FAIL (restore does not launder it)
victim = os.path.join(WORKSPACE, "projects", "v2-4-cro-analytics-certification-pilot", "site-profile.json")
orig = io.open(victim, "rb").read()
nc = None
try:
    with io.open(victim, "ab") as fh:
        fh.write(b"\n<deliberate mutation - v2.10 negative control>\n")
    nc = guard.verify()
finally:
    with io.open(victim, "wb") as fh:
        fh.write(orig)
check(nc is not None and nc.ok is False, "R. Frozen pilot mutation -> integrity guard FAIL")
check(nc is not None and any("v2-4-cro-analytics-certification-pilot/site-profile.json" in m
                             for m in nc.mutations), "R. Guard names the mutated frozen file")

# ===========================================================================
# 4. Final frozen-corpus invariant
# ===========================================================================
final = guard.verify()
check(final.ok, "FROZEN FIXTURE INTEGRITY: projects/ byte-for-byte unchanged (%s)" % final.summary())

print("-" * 60)
print("V2.10 LAUNCH & POST-LAUNCH OPERATIONS TEST SUITE RESULT: %d/%d ASSERTIONS PASSED" % (passed, runs))
if failures:
    print("FAILURES:")
    for x in failures:
        print("  - " + x)
    sys.exit(1)
sys.exit(0)
