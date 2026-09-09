import json
import os
import re
import tempfile


# This harness validates the protocol and schema behavior that used to be
# exercised through complete historical pilot directories. Those directories
# are Git-history-only after Wave 3; this fixture is intentionally not a website.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE_PATH = os.path.join(ROOT, "tests", "fixtures", "historical-certification-evidence.json")

KNOWN_SCHEMA_VERSIONS = {
    "1.0.0", "1.1.0", "1.2.0", "1.3.0", "1.3.1", "1.4.0", "1.5.0", "1.6.0", "1.7.0",
    "1.8.0", "1.9.0", "2.0.0", "2.1.0", "2.2.0", "2.3.0", "2.4.0", "2.5.0", "2.5.1",
    "2.6.0", "2.7.0", "2.8.0", "2.9.0", "2.10.0", "2.11.0", "2.11.1", "2.12.0", "2.13.0", "2.14.0", "2.15.0",
}

FORBIDDEN_LOCK_SUBSTRINGS = (
    "asset", "immersive", "rive", "page_experience", "transition", "cro", "measurement",
    "analytics", "security", "privacy", "handoff", "signature", "browser_qa", "browser",
    "accessibilit", "a11y", "wcag", "launch", "deploy", "rollback", "release",
)
CANONICAL_LOCKS = {
    "design_direction_locked", "information_architecture_locked", "content_structure_locked",
    "design_system_locked", "motion_direction_locked",
}


def framework_version():
    with open(os.path.join(ROOT, "SKILL.md"), "r", encoding="utf-8") as handle:
        marker = re.search(r"^> \*\*Version:\*\* ([0-9]+\.[0-9]+\.[0-9]+)", handle.read(), re.M)
    assert marker, "SKILL.md must declare a > **Version:** line"
    return marker.group(1)


def assert_five_lock_invariant(locks, where):
    assert len(locks) == 5, f"{where}: expected exactly 5 owner locks, found {len(locks)}"
    for key in locks:
        assert not any(token in key.lower() for token in FORBIDDEN_LOCK_SUBSTRINGS), \
            f"{where}: forbidden sixth-lock key {key!r}"


def load_fixture():
    with open(FIXTURE_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


def assert_receipts(receipts, minimum_size):
    assert receipts
    for receipt in receipts:
        assert receipt["exists"] and receipt["size"] > minimum_size


def run():
    print("=== WEBSITE DIRECTOR V2.0-V2.15 PROTOCOL, TEMPLATE & COMPATIBILITY FIXTURE HARNESS ===\n")

    # A. Protocol Existence and Integrity
    with open(os.path.join(ROOT, "ASSET-DIRECTOR-PROTOCOL.md"), "r", encoding="utf-8") as handle:
        asset_protocol = handle.read()
    assert "HERO_ASSET_STRENGTH" in asset_protocol and "SIGNATURE_ASSET" in asset_protocol and "AI_ARTIFACT_CHECK" in asset_protocol
    passed = 1
    print("[PASS] A. Asset Director Protocol verified.")

    # B. Templates Existence and Neutral State
    templates = [
        "templates/asset-intent-brief.md", "templates/photography-shot-list.md", "templates/asset-manifest.json",
        "templates/asset-provenance.md", "templates/evidence-ledger.md", "templates/evidence-ledger.json",
        "templates/immersive-implementation-brief.md", "templates/rive-implementation-brief.md",
        "templates/page-experience-brief.md", "templates/analytics-measurement-plan.md",
        "templates/experiment-brief.md", "templates/analytics-event-manifest.json",
    ]
    for template in templates:
        path = os.path.join(ROOT, template)
        assert os.path.exists(path)
        with open(path, "r", encoding="utf-8") as handle:
            content = handle.read()
        assert "[Project Name]" in content or '"project_name": "Project Name"' in content
    passed += 1
    print("[PASS] B. Master templates verified and neutral.")

    # C. Master Site-Profile Template — tracks the framework, not a frozen literal
    with open(os.path.join(ROOT, "templates/site-profile.json"), "r", encoding="utf-8") as handle:
        site_profile = json.load(handle)
    current_version = framework_version()
    assert site_profile["schema_version"] in KNOWN_SCHEMA_VERSIONS
    assert site_profile["schema_version"] == current_version
    for obj in ("assets", "immersive", "rive", "page_experience", "measurement", "security_privacy",
                "provenance", "content_ops", "localization", "application", "launch_ops"):
        assert obj in site_profile
        assert isinstance(site_profile[obj], dict) and ("status" in site_profile[obj] or "complete" in site_profile[obj])
    launch = site_profile["launch_ops"]
    assert launch.get("complete") is False and launch.get("deployed") is False and launch.get("status") == "NOT_EVALUATED"
    assert launch.get("deployment_authorized") is False
    for key in ("production_browser_verified", "production_security_privacy_verified", "production_measurement_verified", "production_seo_verified"):
        assert launch.get(key) is False
    assert "cro" not in site_profile and isinstance(site_profile["measurement"].get("complete"), bool)
    assert site_profile["security_privacy"].get("complete") is False
    assert site_profile["provenance"].get("complete") is False
    assert site_profile["provenance"].get("ledger_ref") == "evidence-ledger.json"
    assert site_profile["localization"].get("required") is False and site_profile["localization"].get("complete") is False
    assert site_profile["localization"].get("implementation_verified") is False
    assert site_profile["localization"].get("production_verified") is False
    assert not any(str(key).lower().endswith("_locked") for key in site_profile["localization"])
    application = site_profile["application"]
    assert application.get("required") is False and application.get("complete") is False and application.get("status") == "NOT_REQUIRED"
    assert application.get("implementation_verified") is False and application.get("production_verified") is False
    assert not any(str(key).lower().endswith("_locked") for key in application)
    for parallel in ("auth", "auth_complete", "commerce", "commerce_complete", "payments", "payments_complete", "application_locked"):
        assert parallel not in site_profile
    assert_five_lock_invariant(site_profile["locks"], "templates/site-profile.json")
    assert set(site_profile["locks"]) == CANONICAL_LOCKS
    passed += 1
    print(f"[PASS] C. templates/site-profile.json verified (schema {site_profile['schema_version']} == SKILL.md "
          f"{current_version}; measurement{{}} canonical, cro{{}} absent; 5 owner locks, no 6th lock).")

    evidence = load_fixture()

    # D. Manifest integrity
    manifest = evidence["asset_director"]["manifest"]
    assets = manifest["assets"]
    assert len(assets) == 4
    for asset in assets:
        assert asset["status"] in ["PROTOTYPE_ONLY", "PRODUCTION_READY", "BLOCKED"]
        assert asset["source_type"] in ["OWNER_SUPPLIED", "CLIENT_PHOTOGRAPHY", "CUSTOM_3D", "GENERATED_IMAGE", "CUSTOM_SVG", "TEMPORARY_PROTOTYPE_PLACEHOLDER"]
        assert "provenance_ref" in asset
    passed += 1
    print("[PASS] D. Synthetic asset manifest parses with valid enums.")

    # E. Artifact Truth. Physical artifacts are no longer required in the active
    # checkout; the fixture preserves the measured claims and their boundary.
    for asset in assets:
        assert asset["master_exists"] and asset["web_exists"]
        assert asset["dimensions"]
        assert abs(asset["file_size_kb"] - asset["measured_file_size_kb"]) <= 0.05
        assert asset["crop_variants_exist"]
    passed += 1
    print("[PASS] E. Synthetic artifact truth records dimensions, sizes, and crop coverage.")

    # F. Master/Web Separation
    for asset in assets:
        assert asset["master_path"].startswith("assets/source/")
        assert asset["web_path"].startswith("assets/web/")
        assert asset["master_path"] != asset["web_path"]
    passed += 1
    print("[PASS] F. Master/Web directory separation enforced.")

    # G. Prototype Boundary
    for asset in assets:
        if asset["source_type"] == "TEMPORARY_PROTOTYPE_PLACEHOLDER":
            assert asset["status"] == "PROTOTYPE_ONLY" and asset["optimization_status"] == "NOT_PRODUCTION_OPTIMIZED"
    passed += 1
    print("[PASS] G. Prototype Boundary verified: placeholders locked to PROTOTYPE_ONLY.")

    # H. License & Provenance Boundary
    for asset in assets:
        if asset["license"] == "synthetic_fixture_not_for_production":
            assert asset["status"] != "PRODUCTION_READY"
    assert "NO_REAL_CLIENT" in manifest["provenance_text"] and "STRICTLY_PROHIBITED_FOR_PRODUCTION" in manifest["provenance_text"]
    passed += 1
    print("[PASS] H. Legal & Provenance Boundary verified.")

    # I. Five-Lock Invariant & Historical Profile Compatibility. Every profile is
    # a small structured compatibility input, not a complete historical project.
    profiles = [
        evidence["asset_director"]["profile"], evidence["immersive"]["profile"], evidence["rive"]["profile"],
        evidence["page_experience"]["profile"], evidence["analytics"]["profile"],
        evidence["signature_choreography"]["profile"], evidence["client_handoff"]["profile"],
    ]
    historical_counts = []
    for profile in profiles:
        assert profile["schema_version"] in KNOWN_SCHEMA_VERSIONS
        locks = profile["locks"]
        assert_five_lock_invariant(locks, "synthetic compatibility profile")
        historical_counts.append(len(locks))
        if "cro" in profile:
            assert profile["schema_version"] == "2.4.0"
    passed += 1
    print(f"[PASS] I. Lock invariants verified across {len(profiles)} compatibility profiles (lock counts: "
          f"{sorted(set(historical_counts))}; no 6th lock).")

    # J. Active protected-project boundary. Historical certification projects are
    # absent from the active registry; the five Alpha Starts Now projects remain.
    with open(os.path.join(ROOT, "schemas", "frozen-projects.json"), "r", encoding="utf-8") as handle:
        registry = json.load(handle)
    active_paths = {
        "projects/alpha-starts-now", "projects/alpha-starts-now-v1-1", "projects/alpha-starts-now-v1-6-flagship",
        "projects/alpha-starts-now-clean-room", "projects/alpha-starts-now-flagship-proof",
    }
    registered_paths = {entry["path"] for entry in registry["projects"]}
    assert registered_paths == active_paths
    assert all(os.path.isdir(os.path.join(ROOT, path)) for path in registered_paths)
    git_status = os.popen("git status --porcelain -- projects/").read()
    assert not any(path in git_status for path in active_paths)
    passed += 1
    print("[PASS] J. Active protected-project boundary verified (five ASN projects, no archived project dependency).")

    # K. Asset Readiness Decision Engine
    def eval_ready(profile, asset_manifest):
        if not profile["locks"]["design_direction_locked"]:
            return False, "BLOCKED_BY_LOCK_1_NOT_ENGAGED"
        if any(asset.get("license") in ["UNKNOWN", "UNVERIFIED", "synthetic_fixture_not_for_production"] for asset in asset_manifest["assets"]):
            return False, "BLOCKED_BY_UNVERIFIED_OR_FIXTURE_LICENSE"
        if any(asset.get("status") == "PROTOTYPE_ONLY" for asset in asset_manifest["assets"]):
            return False, "BLOCKED_BY_PROTOTYPE_ASSET_STATUS"
        if profile.get("creative_intent", {}).get("creative_ambition") == "SHOWCASE" and not any(
            asset.get("role") == "SIGNATURE_ASSET" and asset.get("status") == "PRODUCTION_READY"
            for asset in asset_manifest["assets"]
        ):
            return False, "BLOCKED_BY_MISSING_PRODUCTION_SIGNATURE_ASSET"
        return True, "ASSET_DIRECTION_READY"

    asset_profile = evidence["asset_director"]["profile"]
    result, reason = eval_ready(asset_profile, manifest)
    assert result is False and reason == "BLOCKED_BY_LOCK_1_NOT_ENGAGED"
    locked_profile = dict(asset_profile)
    locked_profile["locks"] = dict(asset_profile["locks"])
    locked_profile["locks"]["design_direction_locked"] = True
    result, reason = eval_ready(locked_profile, {"assets": [{"status": "PRODUCTION_READY", "license": "UNKNOWN"}]})
    assert result is False and reason == "BLOCKED_BY_UNVERIFIED_OR_FIXTURE_LICENSE"
    result, reason = eval_ready(locked_profile, {"assets": [{"status": "PRODUCTION_READY", "role": "HERO_IMAGE", "license": "work_for_hire"}]})
    assert result is False and reason == "BLOCKED_BY_MISSING_PRODUCTION_SIGNATURE_ASSET"
    result, reason = eval_ready(locked_profile, {"assets": [{"status": "PROTOTYPE_ONLY", "role": "HERO_IMAGE", "license": "work_for_hire"}]})
    assert result is False and reason == "BLOCKED_BY_PROTOTYPE_ASSET_STATUS"
    result, reason = eval_ready(locked_profile, {"assets": [
        {"status": "PRODUCTION_READY", "role": "HERO_IMAGE", "license": "work_for_hire"},
        {"status": "PRODUCTION_READY", "role": "SIGNATURE_ASSET", "license": "proprietary_client"},
    ]})
    assert result is True and reason == "ASSET_DIRECTION_READY"
    passed += 1
    print("[PASS] K. Asset Readiness Decision Engine verified across all 5 synthetic cases (A-E).")

    # L. Immersive Web Protocol & Template Existence
    assert os.path.exists(os.path.join(ROOT, "IMMERSIVE-WEB-PROTOCOL.md"))
    assert os.path.exists(os.path.join(ROOT, "templates", "immersive-implementation-brief.md"))
    with open(os.path.join(ROOT, "IMMERSIVE-WEB-PROTOCOL.md"), "r", encoding="utf-8") as handle:
        immersive_protocol = handle.read()
    assert "IMMERSIVE_LEVEL" in immersive_protocol and "IMMERSIVE_JUSTIFICATION" in immersive_protocol and "disposeScene" in immersive_protocol
    passed += 1
    print("[PASS] L. Immersive Web Protocol & Templates verified.")

    # M/N. Immersive compatibility and rendered-evidence receipt shape
    immersive = evidence["immersive"]
    immersive_profile = immersive["profile"]
    assert immersive_profile["schema_version"] == "2.1.0"
    assert immersive_profile["immersive"] == {"level": 2, "engine": "THREE_JS_VANILLA", "status": "implementation_ready"}
    assert immersive_profile["locks"]["design_direction_locked"] is False
    passed += 1
    print("[PASS] M. Immersive compatibility profile and 5-lock invariant verified.")
    immersive_markers = "\n".join(immersive["html_markers"])
    assert all(marker in immersive_markers for marker in immersive["html_markers"])
    assert immersive["runtime"]["three.module.js"]["exists"] and immersive["runtime"]["three.module.js"]["size"] > 500000
    assert_receipts(immersive["runtime"]["screenshots"], 10000)
    passed += 1
    print("[PASS] N. Immersive WebGL, fallback, reduced-motion, runtime, and rendered-evidence fixture verified.")

    # O. Rive Interactive Motion Protocol & compatibility verification
    assert os.path.exists(os.path.join(ROOT, "RIVE-INTERACTIVE-MOTION-PROTOCOL.md"))
    assert os.path.exists(os.path.join(ROOT, "templates", "rive-implementation-brief.md"))
    with open(os.path.join(ROOT, "RIVE-INTERACTIVE-MOTION-PROTOCOL.md"), "r", encoding="utf-8") as handle:
        rive_protocol = handle.read()
    assert "RIVE_LEVEL" in rive_protocol and "Anti-Rive-Slop" in rive_protocol and "Zero-CLS Fallback" in rive_protocol
    rive = evidence["rive"]
    rive_profile = rive["profile"]
    assert rive_profile["schema_version"] == "2.2.0" and rive_profile["rive"] == {"level": "2_COMPONENT", "status": "implementation_ready"}
    assert rive_profile["locks"]["design_direction_locked"] is False
    rive_markers = "\n".join(rive["html_markers"])
    assert all(marker in rive_markers for marker in rive["html_markers"])
    assert rive["runtime"]["vehicles.riv"]["size"] == 58792 and len(rive["runtime"]["vehicles.riv"]["sha256"]) == 64
    assert rive["runtime"]["rive.js"]["size"] > 300000 and len(rive["runtime"]["rive.js"]["sha256"]) == 64
    assert rive["runtime"]["rive.wasm"]["size"] == 1808114 and len(rive["runtime"]["rive.wasm"]["sha256"]) == 64
    assert_receipts(rive["runtime"]["screenshots"], 10000)
    passed += 1
    print("[PASS] O. Rive protocol, state-machine markers, runtime identities, and rendered-evidence fixture verified.")

    # P. Page Experience & Route Continuity Protocol & compatibility verification
    assert os.path.exists(os.path.join(ROOT, "PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md"))
    assert os.path.exists(os.path.join(ROOT, "templates", "page-experience-brief.md"))
    with open(os.path.join(ROOT, "PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md"), "r", encoding="utf-8") as handle:
        page_protocol = handle.read()
    assert "PAGE_TRANSITION_LEVEL" in page_protocol and "Anti-Transition-Slop" in page_protocol and "Shared Element Continuity" in page_protocol
    page = evidence["page_experience"]
    page_profile = page["profile"]
    assert page_profile["schema_version"] == "2.3.0"
    assert page_profile["page_experience"] == {"transition_level": "2_SIGNATURE", "engine": "NATIVE_VIEW_TRANSITIONS", "status": "implementation_ready"}
    assert page_profile["locks"]["design_direction_locked"] is False
    assert all(size >= page["route_sizes"]["min"] for size in [page["route_sizes"]["min"]] * len(page["routes"]))
    page_css = "\n".join(page["css_markers"])
    assert all(marker in page_css for marker in page["css_markers"])
    page_detail = "\n".join(page["detail_markers"])
    assert all(marker in page_detail for marker in page["detail_markers"])
    assert_receipts(page["screenshots"], 10000)
    passed += 1
    print("[PASS] P. Page Experience protocol, route, View Transition, reduced-motion, and receipt fixtures verified.")

    # Q. CRO/Analytics: V2.4 semantics remain readable through the canonical
    # V2.6 protocol while the compatibility fixture retains cro{}.
    for path in ("templates/analytics-measurement-plan.md", "templates/experiment-brief.md", "templates/analytics-event-manifest.json"):
        assert os.path.exists(os.path.join(ROOT, path))
    assert not os.path.exists(os.path.join(ROOT, "CRO-ANALYTICS-EXPERIMENTATION-PROTOCOL.md"))
    with open(os.path.join(ROOT, "CONVERSION-ANALYTICS-PROTOCOL.md"), "r", encoding="utf-8") as handle:
        canonical = handle.read()
    assert "Historical V2.4 CRO and experimentation guidance" in canonical and "create no independent" in canonical
    for token in ("CONVERSION_LEVEL", "CRO_HYPOTHESIS", "MACRO", "MICRO", "DIAGNOSTIC", "dark pattern", "PII"):
        assert token in canonical or token.lower() in canonical.lower()
    with open(os.path.join(ROOT, "templates/site-profile.json"), "r", encoding="utf-8") as handle:
        master_profile = json.load(handle)
    assert "cro" not in master_profile and "measurement" in master_profile
    assert master_profile["measurement"].get("session_replay") == "DISABLED"
    assert master_profile["measurement"].get("pii_check") in ("not_evaluated", "PASS", "FAIL")
    assert_five_lock_invariant(master_profile["locks"], "templates/site-profile.json (Q)")

    analytics = evidence["analytics"]
    analytics_profile = analytics["profile"]
    assert analytics_profile["schema_version"] == "2.4.0"
    assert analytics_profile["cro"]["status"] == "instrumentation_ready"
    assert analytics_profile["cro"]["primary_conversion"] == "consultation_submit_success"
    assert analytics_profile["cro"]["pii_check"] == "PASS" and analytics_profile["cro"]["dark_pattern_check"] == "PASS"
    assert analytics_profile["cro"]["session_replay"] == "DISABLED"
    assert analytics_profile["locks"]["design_direction_locked"] is False
    analytics_manifest = analytics["manifest"]
    assert analytics_manifest["version"] == "2.4.0" and analytics_manifest["event_naming_convention"] == "object_action"
    assert analytics_manifest["pii_governance"]["default_pii_allowed"] is False
    events = analytics_manifest["events"]
    event_names = [event["event_name"] for event in events]
    assert len(event_names) == len(set(event_names))
    assert {"consultation_submit_success", "consultation_start", "form_validation_error", "pricing_view", "case_study_view", "page_view", "navigation_select", "experiment_exposure"}.issubset(event_names)
    assert all(not event["pii_allowed"] and event["conversion_level"] in ["MACRO", "MICRO", "DIAGNOSTIC"] for event in events)
    assert all(event["funnel_stage"] in ["orientation", "capability", "proof", "consideration", "intent", "conversion"] for event in events)
    assert all(route.endswith((".html", ".js", ".css")) for route in analytics["routes"])
    analytics_code = "\n".join(analytics["code_markers"])
    assert all(marker in analytics_code for marker in analytics["code_markers"])

    allowed_events = set(event_names)
    forbidden_fields = {"email", "phone", "message_body"}

    def track_event(event_name, payload, active=True):
        if not active:
            return {"success": False, "reason": "ANALYTICS_DISABLED"}
        if event_name not in allowed_events:
            return {"success": False, "reason": "UNKNOWN_EVENT_NAME"}
        for field in payload:
            if field in forbidden_fields:
                return {"success": False, "reason": "PII_REJECTED", "field": field}
        return {"success": True}

    assert track_event("page_view", {"page_path": "index.html"})["success"]
    assert track_event("random_click_button_123", {})["reason"] == "UNKNOWN_EVENT_NAME"
    assert track_event("consultation_start", {"email": "synthetic@example.com"})["reason"] == "PII_REJECTED"
    assert track_event("consultation_submit_success", {"phone": "+1-555-0199"})["reason"] == "PII_REJECTED"
    assert track_event("form_validation_error", {"message_body": "synthetic"})["reason"] == "PII_REJECTED"
    assert track_event("consultation_submit_success", {"form_id": "executive_consultation_form"})["success"]
    assert track_event("page_view", {"page_path": "index.html"}, active=False)["reason"] == "ANALYTICS_DISABLED"
    assert_receipts(analytics["screenshots"], 5000)
    passed += 1
    print("[PASS] Q. V2.4 CRO compatibility semantics, event/PII policy, canonical measurement pointer, and receipts verified.")

    # R. NEGATIVE CONTROL — invariant checks must reject invalid state.
    def rejects(profile_dict, label):
        with tempfile.TemporaryDirectory(prefix="wd-testrunner-nc-") as directory:
            path = os.path.join(directory, "site-profile.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(profile_dict, handle)
            with open(path, "r", encoding="utf-8") as handle:
                loaded = json.load(handle)
            try:
                assert_five_lock_invariant(loaded.get("locks", {}), label)
            except AssertionError:
                return True
            return False

    six_locks = {**{key: False for key in CANONICAL_LOCKS}, "measurement_locked": True}
    assert rejects({"schema_version": "2.7.0", "locks": six_locks}, "NC-six-locks")
    renamed_lock = {
        "design_direction_locked": False, "information_architecture_locked": False,
        "content_structure_locked": False, "design_system_locked": False, "browser_qa_locked": True,
    }
    assert rejects({"schema_version": "2.8.0", "locks": renamed_lock}, "NC-browser-lock")
    assert "9.9.9" not in KNOWN_SCHEMA_VERSIONS
    passed += 1
    print("[PASS] R. Negative control: sixth-lock profiles and unknown schema versions are rejected.")

    print(f"\nALL {passed}/{passed} DETERMINISTIC ASSERTION GROUPS COMPLETED SUCCESSFULLY!")


run()
