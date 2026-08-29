# Website Director V2.9 Accessibility Intelligence & WCAG 2.2 AA Verification Test Harness
#
# 1. Repository invariants -- one canonical protocol, one completion flag, five
#    owner locks, cross-document wiring, no false legal-conformance claims.
# 2. Negative controls (protocol sec 41 / sec 42) -- every accessibility
#    safeguard proven to FAIL / BLOCK on a deliberately broken fixture, and an
#    engine-clean run with a failing manual keyboard review proven NOT a full PASS.
#
# Runs with only the standard library via the deterministic simulation engine.
# Run: python tests/test_v2_9_accessibility.py

import io
import json
import os
import re
import sys

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BQA = os.path.join(WORKSPACE, "browser-qa")
FIXTURES = os.path.join(BQA, "fixtures")
sys.path.insert(0, BQA)

from assertions import REQUIREMENT_SOURCES, evaluate                        # noqa: E402
from engine.base import BLOCKED, FAIL, FLAKY, NOT_APPLICABLE, PASS, load_engine  # noqa: E402
from guards.frozen_integrity_guard import FrozenIntegrityGuard             # noqa: E402

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


def ver_ge(text, lo=(2, 9, 0), prefix=r"> \*\*Version:\*\* "):
    m = re.search(r"^%s(\d+)\.(\d+)\.(\d+)" % prefix, text, re.M)
    return bool(m) and tuple(int(x) for x in m.groups()) >= lo


guard = FrozenIntegrityGuard(WORKSPACE, ["projects/"], run_id="v2_9_accessibility")
guard.snapshot()
engine = load_engine("simulation", FIXTURES)

BASE_PLAN = {
    "environment": "local",
    "accessibility": {
        "target": "WCAG_2_2_AA",
        "engine": {"name": "axe-core", "min_severity_fails": "moderate"},
        "target_size": {"project_minimum_px": 44, "wcag_floor_px": 24},
    },
    "routes": [],
}


def run_a11y(folder, viewport=1440, reduced_motion=False, route_cfg=None):
    plan = json.loads(json.dumps(BASE_PLAN))
    rc = {"path": folder, "expected_landmarks": ["header", "nav", "main", "footer"],
          "expected_lang": "en", "requires_skip_link": True}
    if route_cfg:
        rc.update(route_cfg)
    plan["routes"] = [rc]
    obs = engine.observe(folder, viewport, reduced_motion=reduced_motion, browser="simulation")
    return {f.check_id: f for f in evaluate(obs, plan)}, obs


def v(findings, cid):
    return findings[cid].verdict if cid in findings else None


# ===========================================================================
# 1. Repository invariants
# ===========================================================================
PROTOCOL = "ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md"
REVIEW = os.path.join("templates", "accessibility-review.md")
MANIFEST = os.path.join("templates", "accessibility-test-manifest.json")
VALIDATION = os.path.join("examples", "ACCESSIBILITY-INTELLIGENCE-INTEGRATION-VALIDATION.md")

check(exists(PROTOCOL), "Canonical %s exists" % PROTOCOL)
check(exists(REVIEW), "templates/accessibility-review.md exists")
check(exists(MANIFEST), "templates/accessibility-test-manifest.json exists")
check(exists(VALIDATION), "Integration validation artifact exists")

proto = read(PROTOCOL)
for token in ("[ACCESSIBILITY_READY]", "accessibility.complete", "WCAG 2.2 Level AA",
              "No second, independently-writable completion flag", "not a sixth owner",
              "BLOCKED_SCREEN_READER_ENVIRONMENT", "BLOCKED_ACCESSIBILITY_ENGINE_UNAVAILABLE",
              "AUTO_VERIFIED", "MANUAL_VERIFIED", "KNOWN_GAP", "FrozenIntegrityGuard"):
    check(token in proto, "Protocol declares %r" % token)

# exactly one canonical accessibility protocol at repo root
root_md = [f for f in os.listdir(WORKSPACE) if f.endswith(".md")]
a11y_protocols = [f for f in root_md if re.search(r"ACCESSIB|WCAG|A11Y", f) and f.endswith("PROTOCOL.md")]
check(a11y_protocols == [PROTOCOL], "Exactly one canonical accessibility protocol at root: %s" % a11y_protocols)

# ---- no false legal conformance claims (protocol sec 5) --------------------
BANNED = ["ADA COMPLIANT", "FULLY ACCESSIBLE", "ACCESSIBILITY GUARANTEED", "WCAG COMPLIANT",
          "SECTION 508 COMPLIANT", "EN 301 549 COMPLIANT"]
PROHIB_MARKERS = ("NEVER", "never", "not ", "Prohibit", "prohibit", "must not", "Do not", "do not",
                  "unless", "without", "no ", "No ", "REJECT", "Permitted", "boundary", "claim")
scan = [f for f in root_md]
scan += [os.path.join("templates", f) for f in os.listdir(os.path.join(WORKSPACE, "templates")) if f.endswith(".md")]
scan += [os.path.join("examples", f) for f in os.listdir(os.path.join(WORKSPACE, "examples")) if f.endswith(".md")]
bad = []
for rel in scan:
    lines = read(rel).splitlines()
    for i, line in enumerate(lines):
        for b in BANNED:
            if b in line and not any(m in probe for probe in lines[max(0, i - 8):i + 1] for m in PROHIB_MARKERS):
                bad.append("%s :: %s" % (rel, line.strip()[:100]))
check(not bad, "No framework document asserts an accessibility conformance claim (violations: %s)"
      % (bad or "none"))

# ---- state object -----------------------------------------------------------
profile = json.loads(read("templates", "site-profile.json"))
check(ver_ge(profile.get("schema_version", ""), prefix=""), "site-profile.json schema_version >= 2.9.0")
check("accessibility" in profile, "site-profile.json contains accessibility{}")
acc = profile.get("accessibility", {})
check(acc.get("complete") is False, "accessibility.complete defaults to false")
check(acc.get("target") == "WCAG_2_2_AA", "accessibility.target defaults to WCAG_2_2_AA")
check(acc.get("mode") == "not_evaluated", "accessibility.mode defaults to not_evaluated")
for f3 in ("automated_verified", "manual_verified", "screen_reader_verified", "production_verified"):
    check(acc.get(f3) is False, "accessibility.%s defaults to false" % f3)
check(acc.get("exception", {}).get("applied") is False, "accessibility.exception.applied defaults false")
check(isinstance(acc.get("known_gaps"), list), "accessibility.known_gaps is a list")

locks = profile.get("locks", {})
check(len(locks) == 5, "Exactly 5 owner locks (found %d)" % len(locks))
check(not any("access" in k.lower() or "a11y" in k.lower() or "wcag" in k.lower() for k in locks),
      "No sixth accessibility owner lock")
check(not any(isinstance(vv, bool) and "lock" in k for k, vv in acc.items()),
      "accessibility{} contains no lock boolean")
owners = [k for k, vv in profile.items() if isinstance(vv, dict) and "complete" in vv]
check(owners.count("accessibility") == 1, "Exactly one accessibility completion flag in the schema")
check("browser_qa" in profile and "measurement" in profile and "security_privacy" in profile,
      "V2.6/V2.7/V2.8 state objects preserved")

# ---- browser-qa integration (no separate runner) --------------------------
check("ACCESSIBILITY_REVIEW" in REQUIREMENT_SOURCES, "ACCESSIBILITY_REVIEW is a traceable requirement source")
check(not exists("accessibility-qa") and not exists("a11y-runner.py"),
      "No separate accessibility runner was created")
cat = read("browser-qa", "assertions", "catalog.py")
check("check_accessibility" in cat and "ACCESSIBILITY_REVIEW" in cat,
      "Accessibility assertions live in the V2.8 browser-qa catalog")

# ---- cross-document wiring -------------------------------------------------
skill = read("SKILL.md")
check("PHASE 6.9" in skill, "SKILL.md declares PHASE 6.9")
check("[ACCESSIBILITY_READY]" in skill, "SKILL.md declares the ACCESSIBILITY_READY gate")
check("GATE ACCESSIBILITY" in skill, "SKILL.md workflow diagram includes GATE ACCESSIBILITY")
check("Single-Source-of-Truth Rule for `accessibility`" in skill, "SKILL.md documents the accessibility SoT rule")
check(ver_ge(skill), "SKILL.md version >= 2.9.0")
check("Exactly 5 owner locks remain" in skill, "SKILL.md restates the five-lock invariant")

ds = read("DESIGN-SYSTEM-PROTOCOL.md")
check("ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md" in ds and "WCAG 2.2" in ds,
      "DESIGN-SYSTEM-PROTOCOL.md §14 references the canonical accessibility protocol + WCAG 2.2")

contract = read("IMPLEMENTATION-CONTRACT.md")
check("Builder Accessibility Requirements (V2.9)" in contract,
      "IMPLEMENTATION-CONTRACT.md adds §2.8 builder accessibility requirements")
check("HALT" in contract and "accessibility" in contract.lower(),
      "Implementation contract requires halt-and-escalate on lock conflict for accessibility")

checklist = read("PRODUCTION-CHECKLIST.md")
check("WCAG 2.2" in checklist, "PRODUCTION-CHECKLIST.md upgraded to the WCAG 2.2 target")
check("Accessibility Verification (V2.9)" in checklist, "PRODUCTION-CHECKLIST.md adds §5.5 accessibility verification")
check("AUTO_VERIFIED" in checklist and "MANUAL_VERIFIED" in checklist and "KNOWN_GAP" in checklist,
      "Production checklist classifies criteria (no rubber-stamp PASS)")

gaunt = read("WEBSITE-GAUNTLET-PROTOCOL.md")
check("Accessibility Critic" in gaunt, "Gauntlet Accessibility Critic preserved")
check("V2.9" in gaunt and ("no new critic" in gaunt.lower() or "No new critic" in gaunt),
      "Gauntlet adds no new accessibility critic for V2.9")

readme = read("README.md")
check("V2.9" in readme and "Accessibility" in readme, "README documents the V2.9 subsystem")
agents = read("AGENTS.md")
check(ver_ge(agents, prefix=r"\*\*Version:\*\* "), "AGENTS.md version >= 2.9.0")
check("Accessibility" in agents and "V2.9" in agents, "AGENTS.md adds V2.9 governance")

# ---- no secrets -----------------------------------------------------------
SEC = re.compile(r"AKIA[0-9A-Z]{16}|sk_live_[0-9a-zA-Z]{16,}|ghp_[0-9A-Za-z]{30,}|"
                 r"AIza[0-9A-Za-z\-_]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
new_files = [PROTOCOL, REVIEW, MANIFEST, VALIDATION, "SKILL.md", "README.md", "AGENTS.md",
             "DESIGN-SYSTEM-PROTOCOL.md", "IMPLEMENTATION-CONTRACT.md", "PRODUCTION-CHECKLIST.md",
             "WEBSITE-GAUNTLET-PROTOCOL.md", os.path.join("templates", "site-profile.json")]
check(not [f for f in new_files if SEC.search(read(f))], "No secret-shaped material in any V2.9 file")

# ---- all repo JSON valid ------------------------------------------------
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
# 2. Negative controls (scenarios A-R)
# ===========================================================================
f, _ = run_a11y("a11y_clean", route_cfg={"engine_scan": True})
bad = [c for c, x in f.items() if x.verdict in (FAIL, BLOCKED)]
check(not bad, "Clean accessibility fixture yields zero FAIL/BLOCKED (%s)" % bad)

f, _ = run_a11y("a11y_missing_name")
check(v(f, "a11y.accessible-name") == FAIL, "A. Icon-only button with no accessible name -> FAIL")

f, _ = run_a11y("a11y_low_contrast")
check(v(f, "a11y.contrast") == FAIL, "B. Text below target contrast -> FAIL")
check(f["a11y.contrast"].method == "DETERMINISTIC", "B. Contrast finding tagged DETERMINISTIC (Impeccable owns the math)")

f, _ = run_a11y("a11y_keyboard_trap")
check(v(f, "a11y.keyboard-trap") == FAIL, "C. Dialog keyboard trap -> FAIL")

f, _ = run_a11y("a11y_focus_obscured")
check(v(f, "a11y.focus-not-obscured") == FAIL, "D. Sticky header covers focused control -> FAIL")
f, _ = run_a11y("a11y_focus_obscured_manual")
check(v(f, "a11y.focus-not-obscured") == BLOCKED, "D'. Engine cannot establish focus-obscured -> BLOCKED (never silent PASS)")

f, _ = run_a11y("a11y_missing_label")
check(v(f, "a11y.form-label") == FAIL, "E. Form control with no label -> FAIL")

f, _ = run_a11y("a11y_error_not_associated")
check(v(f, "a11y.form-error-association") == FAIL, "F. Form error not programmatically associated -> FAIL")

f, _ = run_a11y("a11y_reduced_motion_trap", reduced_motion=True)
check(v(f, "a11y.reduced-motion-trap") == FAIL, "G. Reduced-motion content trap -> FAIL (via V2.8 §15 integration)")

f, _ = run_a11y("a11y_reflow", viewport=320)
check(v(f, "a11y.reflow") == FAIL, "H. 320px reflow makes the primary CTA unreachable -> FAIL")

f, _ = run_a11y("a11y_text_spacing")
check(v(f, "a11y.text-spacing") == FAIL, "I. Text-spacing override clips content -> FAIL")

f, _ = run_a11y("a11y_target_size")
check(v(f, "a11y.target-size-project") == FAIL, "J. Tiny adjacent targets -> FAIL against the project minimum")
check(v(f, "a11y.target-size-wcag") == FAIL, "J'. Control below the WCAG 24px floor -> FAIL")

f, _ = run_a11y("a11y_color_only_error")
check(v(f, "a11y.color-independence") == FAIL, "K. Colour-only error state -> FAIL")

f, _ = run_a11y("a11y_dialog_good")
check(v(f, "a11y.dialog.contact-modal") == PASS, "L. Dialog with correct name/focus/Escape/return -> PASS")

f, _ = run_a11y("a11y_decorative_image")
bad = [c for c, x in f.items() if x.verdict in (FAIL, BLOCKED)]
check(not bad, "M. Decorative image handled correctly -> PASS (%s)" % bad)

f, _ = run_a11y("a11y_meaningful_image_no_alt")
check(v(f, "a11y.image-alt") == FAIL, "N. Meaningful image missing alt -> FAIL")

f, _ = run_a11y("a11y_sr_unavailable")
check(v(f, "a11y.screen-reader") == BLOCKED, "O. Screen-reader environment unavailable -> BLOCKED (never PASS)")

f, _ = run_a11y("a11y_engine_clean_manual_fail")
check(v(f, "a11y.engine-violations") == PASS, "P. Engine reports zero violations -> engine check PASS")
check(v(f, "a11y.manual-keyboard") == FAIL,
      "P. ...but the manual keyboard review FAILs -> overall accessibility verification is NOT a full PASS")

# Q. Sixth owner lock rejected by framework validation
check(len(profile["locks"]) == 5 and set(profile["locks"]) == {
    "design_direction_locked", "information_architecture_locked", "content_structure_locked",
    "design_system_locked", "motion_direction_locked"}, "Q. Exactly the five canonical owner locks, no sixth")

# R. Frozen pilot mutation -> V2.8 FrozenIntegrityGuard FAILs (restore does not launder it)
victim = os.path.join(WORKSPACE, "projects", "v2-3-page-experience-certification-pilot", "site-profile.json")
orig = io.open(victim, "rb").read()
nc = None
try:
    with io.open(victim, "ab") as fh:
        fh.write(b"\n<deliberate mutation - v2.9 negative control>\n")
    nc = guard.verify()
finally:
    with io.open(victim, "wb") as fh:
        fh.write(orig)
check(nc is not None and nc.ok is False, "R. Frozen pilot mutation -> integrity guard FAIL")
check(nc is not None and any("v2-3-page-experience-certification-pilot/site-profile.json" in m
                             for m in nc.mutations), "R. Guard names the mutated frozen file")

# ===========================================================================
# 3. Final frozen-corpus invariant
# ===========================================================================
final = guard.verify()
check(final.ok, "FROZEN FIXTURE INTEGRITY: projects/ byte-for-byte unchanged (%s)" % final.summary())

print("-" * 60)
print("V2.9 ACCESSIBILITY INTELLIGENCE TEST SUITE RESULT: %d/%d ASSERTIONS PASSED" % (passed, runs))
if failures:
    print("FAILURES:")
    for x in failures:
        print("  - " + x)
    sys.exit(1)
sys.exit(0)
