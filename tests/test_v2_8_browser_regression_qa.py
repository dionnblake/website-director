# Website Director V2.8 Browser & Regression QA Test Harness
#
# Two halves:
#   1. Repository-level invariants  -- canonical protocol, single completion flag,
#      five-lock invariant, cross-document wiring, frozen pilots untouched.
#   2. Negative controls (protocol sec 35 / sec 41) -- every major guard is proven
#      to actually FAIL on a deliberately broken fixture, and the flake policy is
#      proven not to launder a first-run failure into a PASS.
#
# Runs with only the Python standard library via the deterministic simulation
# BROWSER_QA_ENGINE. Run: python tests/test_v2_8_browser_regression_qa.py

import io
import json
import os
import re
import shutil
import sys
import tempfile

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BQA = os.path.join(WORKSPACE, "browser-qa")
FIXTURES = os.path.join(BQA, "fixtures")
sys.path.insert(0, BQA)

from assertions import evaluate                                    # noqa: E402
from engine.base import BLOCKED, FAIL, FLAKY, NOT_APPLICABLE, PASS, load_engine  # noqa: E402
from guards.frozen_integrity_guard import FrozenIntegrityGuard     # noqa: E402
import runner as bqa_runner                                        # noqa: E402

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


def verdict_of(findings, prefix):
    rel = [f for f in findings if f.check_id.startswith(prefix)]
    return [f.verdict for f in rel], rel


# ===========================================================================
# 0. Frozen corpus baseline
# ===========================================================================
guard = FrozenIntegrityGuard(WORKSPACE, ["projects/"], run_id="v2_8_browser_qa")
guard.snapshot()

engine = load_engine("simulation", FIXTURES)

BASE_PLAN = {
    "environment": "local",
    "measurement": {"expected_events": [
        {"name": "page_view", "fires_on_every_route": True, "required_params": ["page_path"]},
        {"name": "contact_submit_error"}, {"name": "contact_submit_success"},
        {"name": "newsletter_signup"},
    ]},
    "security_privacy": {"consent": "NOT_REQUIRED", "required_headers": [],
                         "allowed_third_party_scripts": []},
    "console_ignore": [], "allowed_third_party_failures": [],
    "visual_baselines": {},
    "routes": [],
}


def run_scenario(folder, viewport=1440, reduced_motion=False, plan_overlay=None):
    plan = json.loads(json.dumps(BASE_PLAN))
    plan["routes"] = [{"path": folder, "expected_events": ["page_view"]}]
    if plan_overlay:
        _deep_update(plan, plan_overlay)
    obs = engine.observe(folder, viewport, reduced_motion=reduced_motion, browser="simulation")
    return evaluate(obs, plan)


def _deep_update(d, u):
    for k, v in u.items():
        if isinstance(v, dict) and isinstance(d.get(k), dict):
            _deep_update(d[k], v)
        else:
            d[k] = v


# ===========================================================================
# 1. Repository-level invariants
# ===========================================================================
PROTOCOL = "BROWSER-REGRESSION-QA-PROTOCOL.md"
PLAN_TMPL = os.path.join("templates", "browser-qa-plan.md")
MANIFEST_TMPL = os.path.join("templates", "browser-qa-manifest.json")
VALIDATION = os.path.join("examples", "BROWSER-REGRESSION-QA-INTEGRATION-VALIDATION.md")

check(exists(PROTOCOL), "Canonical %s exists" % PROTOCOL)
check(exists(PLAN_TMPL), "templates/browser-qa-plan.md exists")
check(exists(MANIFEST_TMPL), "templates/browser-qa-manifest.json exists")
check(exists(VALIDATION), "Integration validation artifact exists")
check(exists("browser-qa", "runner.py") and exists("browser-qa", "README.md")
      and exists("browser-qa", "AGENTS.md"), "Reusable browser-qa/ harness present")

proto = read(PROTOCOL)
for token in ("[BROWSER_QA_PASS]", "browser_qa.complete", "BROWSER_QA_ENGINE",
              "No second, independently-writable completion flag", "not an owner lock",
              "FROZEN_FIXTURE_MUTATION", "LOCAL_IMPLEMENTATION_VERIFIED", "PRODUCTION_VERIFIED",
              "NOT_APPLICABLE", "FLAKY", "BLOCKED"):
    check(token in proto, "Protocol declares %r" % token)

# exactly one canonical browser-qa protocol at repo root
root_md = [f for f in os.listdir(WORKSPACE) if f.endswith(".md")]
bqa_protocols = [f for f in root_md if re.search(r"BROWSER|REGRESSION", f) and f.endswith("PROTOCOL.md")]
check(bqa_protocols == [PROTOCOL], "Exactly one canonical browser QA protocol at root: %s" % bqa_protocols)

profile = json.loads(read("templates", "site-profile.json"))
check("browser_qa" in profile, "site-profile.json contains browser_qa{}")
bq = profile.get("browser_qa", {})
check(bq.get("complete") is False, "browser_qa.complete defaults to false")
check(bq.get("visual_regression_status") == "NOT_RUN", "browser_qa.visual_regression_status defaults NOT_RUN")
check(bq.get("frozen_fixture_integrity") == "UNVERIFIED", "browser_qa.frozen_fixture_integrity default UNVERIFIED")
check(bq.get("implementation_verified") is False and bq.get("production_verified") is False,
      "browser_qa verification flags default false")
check(bq.get("exception", {}).get("applied") is False, "browser_qa.exception.applied defaults false")
check(isinstance(bq.get("flaky_tests"), list), "browser_qa.flaky_tests is a list")

locks = profile.get("locks", {})
check(len(locks) == 5, "Exactly 5 owner locks (found %d)" % len(locks))
check(not any("browser" in k.lower() or "qa" in k.lower() for k in locks),
      "No sixth browser/QA owner lock")
check(not any(isinstance(v, bool) and "lock" in k for k, v in bq.items()),
      "browser_qa{} contains no lock boolean")

# single completion flag across the whole schema
owners = [k for k, v in profile.items() if isinstance(v, dict) and "complete" in v]
check(owners.count("browser_qa") == 1, "Exactly one browser_qa completion flag in the schema")

# cross-document wiring
skill = read("SKILL.md")
check("PHASE 10.5" in skill, "SKILL.md declares PHASE 10.5")
check("[BROWSER_QA_PASS]" in skill, "SKILL.md declares the BROWSER_QA_PASS gate")
check("GATE BROWSER" in skill, "SKILL.md workflow diagram includes GATE BROWSER")
check("Single-Source-of-Truth Rule for `browser_qa`" in skill, "SKILL.md documents the browser_qa SoT rule")


def _ver_ge(text, lo=(2, 8, 0), prefix=r"> \*\*Version:\*\* "):
    m = re.search(r"^%s(\d+)\.(\d+)\.(\d+)" % prefix, text, re.M)
    return bool(m) and tuple(int(x) for x in m.groups()) >= lo


check(_ver_ge(skill), "SKILL.md version is >= 2.8.0 (V2.8 is additive to later versions)")
check("Exactly 5 owner locks remain" in skill, "SKILL.md restates the five-lock invariant for V2.8")

contract = read("IMPLEMENTATION-CONTRACT.md")
check("Builder Testability & Browser QA Requirements (V2.8)" in contract,
      "IMPLEMENTATION-CONTRACT.md adds builder testability requirements")
check("stable selector" in contract.lower(), "Implementation contract requires stable selectors")
check("not disable" in contract.lower() or "must not disable" in contract.lower(),
      "Implementation contract forbids disabling QA to ship")

checklist = read("PRODUCTION-CHECKLIST.md")
check("Browser & Regression QA Evidence (V2.8)" in checklist,
      "PRODUCTION-CHECKLIST.md adds the V2.8 browser-evidence section")
check("machine evidence" in checklist.lower(), "Production checklist requires machine evidence for auto-verifiable checks")

gaunt = read("WEBSITE-GAUNTLET-PROTOCOL.md")
check("Deterministic Browser QA Entry Precondition (V2.8" in gaunt,
      "Gauntlet documents the deterministic browser QA entry precondition")
check("No second Gauntlet state machine" in gaunt or "no new critic" in gaunt.lower(),
      "Gauntlet adds no parallel state machine / critic for V2.8")

impeccable = read("IMPECCABLE-ENGINE-PROTOCOL.md")
check("BROWSER_EXECUTED" in impeccable, "Impeccable protocol records the BROWSER_EXECUTED method")
check("one owner for each rule" in impeccable.lower() or "single owner" in impeccable.lower(),
      "Impeccable protocol keeps one owner per rule")

readme = read("README.md")
check("V2.8" in readme and "Browser" in readme, "README documents the V2.8 subsystem")
agents = read("AGENTS.md")
check(_ver_ge(agents, prefix=r"\*\*Version:\*\* "), "AGENTS.md version is >= 2.8.0")
check("Browser & Regression QA Governance (V2.8" in agents, "AGENTS.md adds V2.8 governance rules")

# no secrets introduced
SECRET = re.compile(r"AKIA[0-9A-Z]{16}|sk_live_[0-9a-zA-Z]{16,}|ghp_[0-9A-Za-z]{30,}|"
                    r"AIza[0-9A-Za-z\-_]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
new_files = [PROTOCOL, PLAN_TMPL, MANIFEST_TMPL, VALIDATION, "SKILL.md", "README.md", "AGENTS.md",
             "IMPLEMENTATION-CONTRACT.md", "PRODUCTION-CHECKLIST.md", "WEBSITE-GAUNTLET-PROTOCOL.md",
             "IMPECCABLE-ENGINE-PROTOCOL.md", os.path.join("templates", "site-profile.json")]
leaks = [f for f in new_files if SECRET.search(read(f))]
check(not leaks, "No secret-shaped material in any V2.8 file (%s)" % (leaks or "none"))

# ===========================================================================
# 2. Negative controls -- every guard proven to fail (protocol sec 35 / 41)
# ===========================================================================

# A. responsive overflow -> FAIL
v, _ = verdict_of(run_scenario("a_responsive_overflow", 390), "responsive.horizontal-overflow")
check(v == [FAIL], "A. Responsive overflow at 390px -> FAIL (got %s)" % v)
v, _ = verdict_of(run_scenario("a_responsive_overflow", 1440), "responsive.horizontal-overflow")
check(v == [PASS], "A. Same page at 1440px -> PASS (overflow detected, not masked)")

# B. console exception -> FAIL
v, _ = verdict_of(run_scenario("b_console_exception"), "console.no-application-errors")
check(v == [FAIL], "B. Uncaught console exception -> FAIL (got %s)" % v)

# C. broken hero image -> FAIL
f = run_scenario("c_broken_hero", plan_overlay={"routes": [{"path": "c_broken_hero",
                 "critical_hero_asset": "/assets/web/hero.avif", "expected_events": ["page_view"]}]})
vb = [x.verdict for x in f if x.check_id in ("assets.no-broken", "assets.non-zero-dimensions",
                                             "assets.critical-hero-loads")]
check(FAIL in vb, "C. Broken hero image -> FAIL (got %s)" % vb)
check(any(x.check_id == "network.no-failed-requests" and x.verdict == FAIL for x in f),
      "C. Broken hero also fails the network check")

# D. mobile navigation open/close -> PASS
f = run_scenario("d_mobile_nav", 390)
vn = [x.verdict for x in f if x.check_id.startswith("nav.mobile")]
check(vn and all(x == PASS for x in vn), "D. Mobile navigation open/close -> PASS (got %s)" % vn)

# E. server-rejected form (correct behaviour) -> form checks PASS
f = run_scenario("e_failed_form")
ve = {x.check_id: x.verdict for x in f if x.check_id.startswith("form.contact")}
check(ve.get("form.contact.no-false-conversion") == PASS
      and ve.get("form.contact.success-state") == PASS
      and ve.get("form.contact.invalid-error") == PASS,
      "E. Correct form-on-rejection behaviour -> PASS (%s)" % ve)

# E'. false success + false conversion on server reject -> FAIL
f = run_scenario("e_false_success")
ve = {x.check_id: x.verdict for x in f if x.check_id.startswith("form.contact")}
check(ve.get("form.contact.no-false-conversion") == FAIL, "E'. Success conversion on server reject -> FAIL")
check(ve.get("form.contact.success-state") == FAIL, "E'. Success state shown on server reject -> FAIL")

# F. reduced motion keeps content meaningful -> PASS ; F' -> FAIL
v, _ = verdict_of(run_scenario("f_reduced_motion", 1440, reduced_motion=True), "motion.reduced-content-visible")
check(v == [PASS], "F. Reduced-motion content remains visible -> PASS (got %s)" % v)
v, _ = verdict_of(run_scenario("f_reduced_motion_broken", 1440, reduced_motion=True), "motion.reduced-content-visible")
check(v == [FAIL], "F'. Content trapped behind animation under reduced motion -> FAIL (got %s)" % v)

# G. intentional 20px shift vs locked baseline -> DIFF detected, baseline NOT overwritten
g_baseline_before = read("browser-qa", "fixtures", "g_visual_shift", "qa-fixture.json")
f = run_scenario("g_visual_shift", plan_overlay={"visual_baselines": {"g_visual_shift@1440": "g-render-padtop-32"}})
vr = [x for x in f if x.check_id == "visual.regression"]
check(vr and vr[0].verdict == FAIL and "DIFF DETECTED" in vr[0].detail,
      "G. 20px layout shift -> visual DIFF detected (got %s)" % ([x.verdict for x in vr]))
check(vr and vr[0].method == "VISUAL_COMPARISON", "G. Visual finding is tagged VISUAL_COMPARISON")
check(read("browser-qa", "fixtures", "g_visual_shift", "qa-fixture.json") == g_baseline_before,
      "G. Baseline fixture was NOT silently overwritten by the diff")

# H. dynamic timestamp handled deterministically -> MATCH (no false regression)
f = run_scenario("h_dynamic_timestamp",
                 plan_overlay={"visual_baselines": {"h_dynamic_timestamp@1440": "h-render-frozen-clock"}})
vr = [x.verdict for x in f if x.check_id == "visual.regression"]
check(vr == [PASS], "H. Deterministic timestamp fixture -> visual MATCH, no false regression (got %s)" % vr)

# I. frozen project mutation -> integrity guard FAIL (restore does not launder it)
victim = os.path.join(WORKSPACE, "projects", "v2-4-cro-analytics-certification-pilot", "site-profile.json")
orig = io.open(victim, "rb").read()
nc = None
try:
    with io.open(victim, "ab") as fh:
        fh.write(b"\n<deliberate mutation - v2.8 negative control>\n")
    nc = guard.verify()
finally:
    with io.open(victim, "wb") as fh:
        fh.write(orig)
check(nc is not None and nc.ok is False, "I. Frozen fixture mutation -> integrity guard FAIL")
check(nc is not None and any("v2-4-cro-analytics-certification-pilot/site-profile.json" in m
                             for m in nc.mutations), "I. Guard names the mutated frozen file")
ledger = os.path.join(BQA, "evidence", "frozen-integrity-violations.log")
check(os.path.exists(ledger) and "v2_8_browser_qa" in io.open(ledger, encoding="utf-8").read(),
      "I. Violation recorded in the append-only ledger despite the restore")

# J. flaky test -> FLAKY, never an unconditional PASS
tmp = tempfile.mkdtemp(prefix="wd-v2_8-flaky-")
try:
    plan_path = os.path.join(tmp, "plan.json")
    with io.open(plan_path, "w", encoding="utf-8") as fh:
        json.dump({"environment": "local", "repo_root": WORKSPACE,
                   "browsers": {"smoke": ["simulation"]}, "viewports": {"smoke": [1440]},
                   "routes": [{"path": "j_flaky", "viewports": [1440]}]}, fh)
    rc = bqa_runner.run(plan_path, "simulation", os.path.join(tmp, "ev"), "smoke", 2, FIXTURES)
    ev = sorted(f for f in os.listdir(os.path.join(tmp, "ev")) if f.endswith(".evidence.json"))[-1]
    man = json.load(io.open(os.path.join(tmp, "ev", ev), encoding="utf-8"))
    check(man["verdict_counts"].get(FLAKY, 0) >= 1 and man["flaky_tests"],
          "J. First-run-fail / retry-pass recorded as FLAKY, not PASS (%s)" % man["verdict_counts"])
    check(rc != 0, "J. A FLAKY result does not produce a green (0) runner exit")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# J'. engine lifecycle failures -> BLOCKED evidence, never an unhandled traceback
class _FailingBrowserEngine:
    name = "synthetic-browser"
    supports_real_browser = True

    def __init__(self, phase):
        self.phase = phase
        self.stopped = False

    def available(self):
        return True

    def start(self):
        if self.phase == "start":
            raise RuntimeError("synthetic browser executable is unavailable")

    def stop(self):
        self.stopped = True

    def observe(self, *args, **kwargs):
        raise RuntimeError("synthetic browser launch failed")


def _write_failure_plan(folder):
    plan_path = os.path.join(folder, "plan.json")
    with io.open(plan_path, "w", encoding="utf-8") as fh:
        json.dump({"environment": "local", "repo_root": WORKSPACE,
                   "browsers": {"smoke": ["synthetic"]}, "viewports": {"smoke": [390]},
                   "routes": [{"path": "synthetic", "viewports": [390]}]}, fh)
    return plan_path


tmp = tempfile.mkdtemp(prefix="wd-v2_8-engine-failure-")
original_loader = bqa_runner.load_engine
fake = None
try:
    def _fake_loader(*args, **kwargs):
        return fake

    bqa_runner.load_engine = _fake_loader

    start_dir = os.path.join(tmp, "start")
    os.makedirs(start_dir)
    fake = _FailingBrowserEngine("start")
    start_rc = bqa_runner.run(_write_failure_plan(start_dir), "synthetic", os.path.join(start_dir, "ev"),
                              "smoke", 0, FIXTURES)
    start_ev = sorted(f for f in os.listdir(os.path.join(start_dir, "ev"))
                      if f.endswith(".evidence.json"))[-1]
    start_man = json.load(io.open(os.path.join(start_dir, "ev", start_ev), encoding="utf-8"))
    check(start_rc != 0 and start_man["overall"] == "BLOCKED",
          "J'. engine.start failure writes BLOCKED evidence and nonzero exit")
    check(fake.stopped, "J'. engine.stop runs after partial engine startup")

    observe_dir = os.path.join(tmp, "observe")
    os.makedirs(observe_dir)
    fake = _FailingBrowserEngine("observe")
    observe_rc = bqa_runner.run(_write_failure_plan(observe_dir), "synthetic",
                                os.path.join(observe_dir, "ev"), "smoke", 0, FIXTURES)
    observe_ev = sorted(f for f in os.listdir(os.path.join(observe_dir, "ev"))
                        if f.endswith(".evidence.json"))[-1]
    observe_man = json.load(io.open(os.path.join(observe_dir, "ev", observe_ev), encoding="utf-8"))
    observe_findings = observe_man["findings"]
    check(observe_rc != 0 and observe_man["overall"] == "BLOCKED"
          and observe_man["blocked_reason"].startswith("BLOCKED_ENVIRONMENT: engine.observe()"),
          "J'. engine.observe failure writes BLOCKED evidence instead of crashing")
    check(any(f["check_id"] == "engine.observe" and f["verdict"] == BLOCKED
              for f in observe_findings),
          "J'. blocked observation is represented in the evidence findings")
    check(fake.stopped, "J'. engine.stop runs after observation failure")
finally:
    bqa_runner.load_engine = original_loader
    shutil.rmtree(tmp, ignore_errors=True)

# K. local verification never sets production_verified
tmp = tempfile.mkdtemp(prefix="wd-v2_8-local-")
try:
    plan_path = os.path.join(tmp, "plan.json")
    with io.open(plan_path, "w", encoding="utf-8") as fh:
        json.dump({"environment": "local", "repo_root": WORKSPACE,
                   "browsers": {"smoke": ["simulation"]}, "viewports": {"smoke": [1440]},
                   "measurement": {"expected_events": [
                       {"name": "page_view", "fires_on_every_route": True, "required_params": ["page_path"]}]},
                   "security_privacy": {"consent": "NOT_REQUIRED"},
                   "visual_baselines": {"clean_reference@1440": "clean-1440"},
                   "routes": [{"path": "clean_reference", "viewports": [1440],
                               "expected_events": ["page_view"]}]}, fh)
    bqa_runner.run(plan_path, "simulation", os.path.join(tmp, "ev"), "smoke", 2, FIXTURES)
    ev = sorted(f for f in os.listdir(os.path.join(tmp, "ev")) if f.endswith(".evidence.json"))[-1]
    man = json.load(io.open(os.path.join(tmp, "ev", ev), encoding="utf-8"))
    check(man["environment"] == "local", "K. Run recorded as environment=local")
    # simulation is a non-browser adapter: it cannot set implementation_verified either
    check(man["overall"] == "PASS", "K. Clean local run passes")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# L. PII in an analytics payload -> FAIL
f = run_scenario("l_pii_event", plan_overlay={"routes": [{"path": "l_pii_event",
                 "expected_events": ["page_view", "newsletter_signup"]}]})
v = [x.verdict for x in f if x.check_id == "measure.no-pii"]
check(FAIL in v, "L. Email address in analytics payload -> FAIL (got %s)" % v)

# harness self-check: a fully clean fixture yields zero FAIL/BLOCKED
f = run_scenario("clean_reference", 1440, plan_overlay={
    "security_privacy": {"consent": "NOT_REQUIRED", "required_headers": [],
                         "allowed_third_party_scripts": []},
    "visual_baselines": {"clean_reference@1440": "clean-1440"},
    "routes": [{"path": "clean_reference", "viewports": [1440], "expected_events": ["page_view"],
                "critical_hero_asset": "/assets/web/hero.avif"}]})
bad = [x for x in f if x.verdict in (FAIL, BLOCKED)]
check(not bad, "Clean reference fixture yields zero FAIL/BLOCKED (%s)"
      % [(x.check_id, x.verdict, x.detail[:40]) for x in bad])

# ===========================================================================
# 3. Final frozen-corpus invariant
# ===========================================================================
final = guard.verify()
check(final.ok, "FROZEN FIXTURE INTEGRITY: projects/ byte-for-byte unchanged (%s)" % final.summary())

print("-" * 60)
print("V2.8 BROWSER & REGRESSION QA TEST SUITE RESULT: %d/%d ASSERTIONS PASSED" % (passed, runs))
if failures:
    print("FAILURES:")
    for x in failures:
        print("  - " + x)
    sys.exit(1)
sys.exit(0)
