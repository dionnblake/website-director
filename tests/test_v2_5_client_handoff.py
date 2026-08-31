# Website Director V2.5 Client CMS & Handoff System Test Harness
#
# Repaired under V2.8 (BROWSER-REGRESSION-QA-PROTOCOL.md sec 0, sec 22, sec 23):
#   * Every mutable CMS operation now runs against a disposable temp copy of the
#     pilot. Nothing under projects/ is written, ever.
#   * A FrozenIntegrityGuard snapshots projects/ before the run and asserts it is
#     byte-for-byte unchanged afterwards -- a passing test that mutated a frozen
#     fixture is treated as a FAILED QA architecture.
#   * A negative control deliberately mutates a protected file and proves the
#     guard catches it, that a later restore does not turn the mutating run into
#     a PASS, and that the violation is recorded in an append-only ledger.
#
# Run: python tests/test_v2_5_client_handoff.py   (exit 0 = pass)

import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PILOT_REL = os.path.join("projects", "v2-5-client-handoff-certification-pilot")
CANONICAL_PILOT_DIR = os.path.join(WORKSPACE_DIR, PILOT_REL)

sys.path.insert(0, os.path.join(WORKSPACE_DIR, "browser-qa"))
from guards.frozen_integrity_guard import FrozenIntegrityGuard  # noqa: E402

assertions_run = 0
assertions_passed = 0
failures = []


def check(cond, msg):
    global assertions_run, assertions_passed
    assertions_run += 1
    if cond:
        assertions_passed += 1
        print("[PASS] " + msg)
    else:
        failures.append(msg)
        print("[FAIL] " + msg)


def load_cms_class(temp_pilot_dir):
    """Import SyntheticCMS from the DISPOSABLE copy, never from projects/."""
    engine_path = os.path.join(temp_pilot_dir, "scripts", "cms_engine.py")
    spec = importlib.util.spec_from_file_location("cms_engine_isolated", engine_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.SyntheticCMS


# ---------------------------------------------------------------------------
# 0. Snapshot the frozen certification corpus BEFORE anything runs
# ---------------------------------------------------------------------------
guard = FrozenIntegrityGuard(WORKSPACE_DIR, protected_paths=["projects/"], run_id="v2_5_client_handoff")
guard.snapshot()
print("[INFO] Frozen integrity baseline: %d files under projects/" % len(guard._baseline))

# ---------------------------------------------------------------------------
# 1. Build a disposable working copy of the pilot
# ---------------------------------------------------------------------------
temp_root = tempfile.mkdtemp(prefix="wd-v2_5-cms-")
temp_pilot = os.path.join(temp_root, "pilot")
shutil.copytree(CANONICAL_PILOT_DIR, temp_pilot,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

try:
    SyntheticCMS = load_cms_class(temp_pilot)
    cms = SyntheticCMS(temp_pilot)

    # -- protocol + schema -------------------------------------------------
    check(os.path.exists(os.path.join(WORKSPACE_DIR, "CLIENT-CMS-HANDOFF-PROTOCOL.md")),
          "CLIENT-CMS-HANDOFF-PROTOCOL.md exists")

    pf = json.load(io.open(os.path.join(CANONICAL_PILOT_DIR, "site-profile.json"), encoding="utf-8"))
    check(pf.get("schema_version") == "2.5.0", "schema_version is 2.5.0")

    locks = pf.get("locks", {})
    check(len(locks) == 5, "Exactly 5 owner locks exist in locks{}")
    check("handoff_locked" not in locks, "No sixth handoff owner lock")

    # -- permission matrix ----------------------------------------------
    check(cms.check_permission("EDITOR", "can_edit_content") is True, "EDITOR can edit content")
    check(cms.check_permission("EDITOR", "can_manage_infrastructure") is False,
          "EDITOR cannot manage infrastructure")
    check(cms.check_permission("EDITOR", "can_change_design_tokens") is False,
          "EDITOR cannot change design tokens")
    check(cms.check_permission("VIEW_ONLY", "can_edit_content") is False,
          "VIEW_ONLY cannot edit content")
    check(cms.check_permission("OWNER", "can_edit_content") is True, "OWNER can manage synthetic content")

    k_safe, msg = cms.attempt_design_change("EDITOR", "BORDER_RADIUS", "20px")
    check(not k_safe and ("CMS_OPERATION_REJECTED" in msg), "Design token change by editor rejected")

    # -- content validation --------------------------------------------
    invalid_prj = {"slug": "test-prime", "summary": "Test", "status": "DRAFT", "hero_image": {},
                   "industry": "Civic", "lead_architect": "team-01"}
    valid, msg = cms.validate_item("project", invalid_prj)
    check(not valid and ("Missing required field" in msg), "Missing required field rejected")

    existing_prjs = cms.load_content("project")
    dur_prj = {"id": "prj-99", "title": "Duplicate Project", "slug": "lumina-pavilion", "summary": "Test",
               "status": "DRAFT", "hero_image": {}, "industry": "Civic", "lead_architect": "team-01"}
    valid, msg = cms.validate_item("project", dur_prj, existing_prjs)
    check(not valid and ("Duplicate slug rejected" in msg), "Duplicate slug rejected")

    unk_prj = {"id": "prj-99", "title": "Test", "slug": "unique-slug", "summary": "Test", "status": "DRAFT",
               "hero_image": {}, "industry": "Civic", "lead_architect": "team-01", "arbitrary_data": 123}
    valid, msg = cms.validate_item("project", unk_prj)
    check(not valid and ("Unknown field rejected" in msg), "Unknown content field rejected")

    # -- edit / publish / archive lifecycle (all on the temp copy) -----
    k_succ, msg = cms.edit_item("EDITOR", "project", "prj-01", {"summary": "Updated alpine daylight summary"})
    check(k_succ, "Safe edit of project summary succeeded")

    draft_item = {"id": "prj-03", "title": "Cantonal Journal Design", "slug": "cantonal-journal",
                  "summary": "Unbuilt monolithic archive study",
                  "status": "DRAFT",
                  "hero_image": {"src": "/assets/projects/cantonal.webp", "aspect_ratio": "16:9",
                                 "min_width": 1920, "min_height": 1080, "alt_text": "Plan"},
                  "industry": "Cultural", "lead_architect": "team-01"}
    prjs = cms.load_content("project")
    prjs.append(draft_item)
    cms.save_content("project", prjs)

    is_public = cms.get_public_listing("project")
    check(all(it.get("id") != "prj-03" for it in is_public), "Draft content is not visible in public listing")

    k_succ, msg = cms.edit_item("EDITOR", "project", "prj-03", {"status": "PUBLISHED"})
    check(k_succ, "Publishing draft succeeded")
    is_public_2 = cms.get_public_listing("project")
    check(any(it.get("id") == "prj-03" for it in is_public_2), "Published content appears in public listing")

    k_succ, msg = cms.edit_item("EDITOR", "project", "prj-03", {"status": "ARCHIVED"})
    check(k_succ, "Archiving project succeeded")
    is_public_3 = cms.get_public_listing("project")
    check(all(it.get("id") != "prj-03" for it in is_public_3), "Archived record removed from public listing")
    check(any(it.get("id") == "prj-03" for it in cms.load_content("project")),
          "Archived record preserved in content database")

    k_succ, msg = cms.edit_item("EDITOR", "project", "prj-02", {"slug": "aethel-atelier-workshop"})
    check(k_succ, "Slug change succeeded")
    redis_path = os.path.join(temp_pilot, "content", "redirects.json")
    with io.open(redis_path, "r", encoding="utf-8") as f:
        redirects = json.load(f)
    check(any(r.get("source_path") == "/project/aethel-atelier"
              and r.get("destination_path") == "/project/aethel-atelier-workshop" for r in redirects),
          "Redirect registry recorded 301 redirect")

    # -- backup / restore SHA-256 proof (temp copy) --------------------
    backup_hash, backup_path = cms.create_backup("snapshot-regression")
    check(backup_hash is not None and len(backup_hash) == 64, "Backup created with valid SHA-256")

    prjs = cms.load_content("project")
    prjs[0]["wummary"] = "MUTATED DELIBERATELY"
    cms.save_content("project", prjs)

    k_succ, msg, restore_hash = cms.restore_backup("snapshot-regression")
    check(k_succ, "Restore executed successfully")
    check(restore_hash == backup_hash, "RESTORE_HASH_MATCH == TRUE")

    # -- handoff governance documents (read canonical, no writes) ------
    owner_reg_path = os.path.join(CANONICAL_PILOT_DIR, "DIGITAL-OWNERSHIP-REGISTER.md")
    owner_text = io.open(owner_reg_path, "r", encoding="utf-8").read()
    check("CRITICAL_SYSTEMS_OWNED_BY_DEVELOPER_PERSONAL_ACCOUNT = 0" in owner_text,
          "Zero personal developer accounts recorded")

    secret_values_found = 0
    for fn in os.listdir(CANONICAL_PILOT_DIR):
        if fn.endswith(".md"):
            cont = io.open(os.path.join(CANONICAL_PILOT_DIR, fn), "r", encoding="utf-8").read()
            if 'api_key = "' in cont or 'secret = "' in cont or 'password = "' in cont:
                secret_values_found += 1
    check(secret_values_found == 0, "Zero secret values in handoff documentation")

    k_pf_handoff = pf.get("handoff", {})
    check(k_pf_handoff.get("client_independence_test") in ("PASS_7_OF_7", "PASS"),
          "Client independence test PASS")
    check(k_pf_handoff.get("bus_factor_test") == "PASS", "Bus factor test PASS")
    check(k_pf_handoff.get("acceptance_status") == "READY_FOR_REVIEW",
          "Handoff acceptance status is READY_FOR_REVIEW")

    # -- legacy pilots keep their own schema_version -------------------
    legacy_pilots = ["alpha-starts-now", "v1-9-visual-prototype-certification-pilot",
                     "v2-0-asset-director-pilot", "v2-1-immersive-web-certification-pilot",
                     "v2-2-rive-certification-pilot", "v2-3-page-experience-certification-pilot",
                     "v2-4-cro-analytics-certification-pilot"]
    for lp in legacy_pilots:
        lc_json = os.path.join(WORKSPACE_DIR, "projects", lp, "site-profile.json")
        if os.path.exists(lc_json):
            data = json.load(io.open(lc_json, "r", encoding="utf-8"))
            check(data.get("schema_version") != "2.5.0",
                  "Legacy pilot " + lp + " preserved without V2.5 mutations")

    # -----------------------------------------------------------------
    # NEGATIVE CONTROL -- prove the integrity guard actually fails
    # -----------------------------------------------------------------
    victim_rel = os.path.join(PILOT_REL, "content", "projects.json")
    victim_abs = os.path.join(WORKSPACE_DIR, victim_rel)
    original_bytes = io.open(victim_abs, "rb").read()
    nc_result = None
    try:
        with io.open(victim_abs, "ab") as f:
            f.write(b"\n<deliberate frozen-fixture mutation for negative control>\n")
        nc_result = guard.verify()  # records to the append-only ledger
    finally:
        with io.open(victim_abs, "wb") as f:
            f.write(original_bytes)

    check(nc_result is not None and nc_result.ok is False,
          "NEGATIVE CONTROL: guard.verify() FAILS on a deliberate frozen-fixture mutation")
    check(nc_result is not None and victim_rel.replace(os.sep, "/") in nc_result.mutations,
          "NEGATIVE CONTROL: guard names the exact mutated file")
    check(nc_result is not None and nc_result.git_status_changed is True,
          "NEGATIVE CONTROL: guard also flags the git working-tree change")

    # restoring the file must NOT convert the run into a PASS
    ledger = os.path.join(WORKSPACE_DIR, "browser-qa", "evidence", "frozen-integrity-violations.log")
    check(os.path.exists(ledger), "NEGATIVE CONTROL: violation ledger was written")
    if os.path.exists(ledger):
        ledger_text = io.open(ledger, "r", encoding="utf-8").read()
        check("v2_5_client_handoff" in ledger_text and "FROZEN_FIXTURE_MUTATION" in ledger_text,
              "NEGATIVE CONTROL: restore-after-the-fact did not erase the recorded violation")

    # -----------------------------------------------------------------
    # FINAL INVARIANT -- the real run touched nothing frozen
    # -----------------------------------------------------------------
    final = guard.verify(record_violation=True)
    check(final.ok, "FROZEN FIXTURE INTEGRITY: projects/ is byte-for-byte unchanged (%s)" % final.summary())

finally:
    shutil.rmtree(temp_root, ignore_errors=True)

print("-" * 60)
print("V2.5 CLIENT CMS & HANDOFF TEST SUITE COMPLETE: %d/%d ASSERTIONS PASSED"
      % (assertions_passed, assertions_run))
if failures:
    print("FAILURES:")
    for f in failures:
        print("  - " + f)
    sys.exit(1)
sys.exit(0)
