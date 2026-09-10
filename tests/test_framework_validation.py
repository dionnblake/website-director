"""Capability 6 regression and negative-control tests.

These tests exercise pure validator rules with synthetic data and keep all
mutation probes inside temporary directories. They do not treat missing
historical material as permission to regenerate it.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from framework_validation import validator


ROOT = Path(__file__).resolve().parents[1]
CURRENT_VERSION = json.loads((ROOT / "framework-version.json").read_text(encoding="utf-8"))["version"]

KERNEL_STAGES = (
    "UNDERSTAND",
    "RESEARCH",
    "DESIGN",
    "ASSETS",
    "BUILD",
    "VERIFY",
    "RELEASE",
)

KERNEL_CAPABILITIES = (
    "framework_validation",
    "website_director_core",
    "discovery_business_understanding",
    "owner_intent",
    "information_architecture",
    "content_structure",
    "seo",
    "visual_research",
    "external_inspiration_reference_research",
    "design_inspiration_adapter",
    "awwwards_showcase_benchmarking",
    "design_intelligence",
    "archetype_synthesis",
    "visual_direction",
    "visual_prototype",
    "design_system",
    "motion_direction",
    "measurement_analytics",
    "security_privacy",
    "accessibility",
    "asset_director",
    "provenance",
    "implementation_contract",
    "build_execution",
    "gsap_motion_engineering",
    "cinematic_integration",
    "signature_choreography",
    "content_cms_operations",
    "localization",
    "application_commerce_auth",
    "immersive_web",
    "rive",
    "page_experience",
    "browser_qa",
    "design_qa_impeccable",
    "website_gauntlet",
    "production_preflight",
    "launch_operations",
    "client_handoff",
)

ACTIVE_PROTOCOL_CAPABILITIES = {
    "FRAMEWORK_VALIDATION": "framework_validation",
    "WEBSITE_DIRECTOR_CORE": "website_director_core",
    "DESIGN_INSPIRATION_ADAPTER": "design_inspiration_adapter",
    "CONTENT_OPERATIONS_CMS": "content_cms_operations",
    "LOCALIZATION_INTERNATIONALIZATION": "localization",
    "EVIDENCE_PROVENANCE": "provenance",
    "APPLICATION_COMMERCE_AUTH": "application_commerce_auth",
}


def _kernel_routing_rows() -> list[dict[str, str]]:
    """Read the human-readable routing table without creating runtime state."""
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    start_marker = "<!-- KERNEL_CAPABILITY_ROUTING_START -->"
    end_marker = "<!-- KERNEL_CAPABILITY_ROUTING_END -->"
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker, start)
    rows: list[dict[str, str]] = []
    headers = (
        "Capability",
        "Current authority",
        "Primary stage",
        "Secondary dependencies",
        "Required or conditional",
        "Current state object",
        "Current gate",
        "Owner-lock interaction",
        "Rationale",
    )
    for line in text[start:end].splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != len(headers) or cells[0] in {"Capability", ":---"}:
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def _load_json(relative: str) -> object:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class FrameworkValidationTests(unittest.TestCase):
    def test_current_framework_contract_artifacts_pass(self) -> None:
        profile = _load_json("templates/site-profile.json")
        protocols = _load_json("schemas/protocols.json")
        gates = _load_json("schemas/gates.json")
        phases = _load_json("schemas/phases.json")
        states = _load_json("schemas/state-ownership.json")
        self.assertEqual(validator.validate_owner_locks(profile), [])
        self.assertEqual(validator.validate_protocol_registry(protocols), [])
        self.assertNotIn("CANONICAL_PROTOCOL_EXISTS", validator.validate_protocol_paths(protocols, ROOT))
        self.assertEqual(
            validator.validate_gate_registry(
                gates,
                protocol_ids=[entry["id"] for entry in protocols["protocols"]],
                phase_ids=[entry["phase"] for entry in phases["phases"]],
            ),
            [],
        )
        self.assertEqual(validator.validate_state_ownership_registry(states), [])
        self.assertEqual(
            validator.validate_template_references(
                ["templates/site-profile.json", "templates/framework-validation-review.md"], ROOT
            ),
            [],
        )

    def test_current_profile_has_exactly_five_owner_locks(self) -> None:
        profile = _load_json("templates/site-profile.json")
        self.assertIsInstance(profile, dict)
        self.assertEqual(validator.validate_owner_locks(profile), [])

    def test_seven_stage_kernel_routes_every_capability_once(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for number, stage in enumerate(KERNEL_STAGES, start=1):
            self.assertEqual(skill.count(f"## {number}. {stage}"), 1)
        self.assertNotRegex(skill, r"(?m)^#{1,6}\s+PHASE\s+\d")

        rows = _kernel_routing_rows()
        counts = Counter(row["Capability"] for row in rows)
        self.assertEqual(counts, Counter(KERNEL_CAPABILITIES))
        self.assertTrue(all(row["Primary stage"] in KERNEL_STAGES for row in rows))
        protocols = _load_json("schemas/protocols.json")
        for protocol in protocols["protocols"]:
            if protocol.get("status") == "ACTIVE":
                with self.subTest(protocol=protocol["id"]):
                    self.assertIn(protocol["id"], ACTIVE_PROTOCOL_CAPABILITIES)
                    self.assertIn(ACTIVE_PROTOCOL_CAPABILITIES[protocol["id"]], counts)

        profile = _load_json("templates/site-profile.json")
        self.assertEqual(
            set(profile["locks"]),
            {
                "design_direction_locked",
                "information_architecture_locked",
                "content_structure_locked",
                "design_system_locked",
                "motion_direction_locked",
            },
        )
        self.assertIn("OWNER_LOCK_COUNT = 5", skill)
        for lock in profile["locks"]:
            self.assertIn(f"| `{lock}` |", skill)
        self.assertNotIn("homepage_visual_locked", skill)
        self.assertNotRegex(skill, r"`kernel\.[^`]+`\s*=")

    def test_kernel_preserves_default_path_and_authority_boundaries(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        path = "UNDERSTAND -> RESEARCH -> DESIGN -> ASSETS -> BUILD -> VERIFY -> RELEASE"
        self.assertGreaterEqual(skill.count(path), 2)
        self.assertIn("DEFAULT_PATH_AUTHORITY_COUNT = 7", skill)
        self.assertIn("GATE BROWSER", skill)
        self.assertIn("[BROWSER_QA_PASS]", skill)
        self.assertIn("GATE LAUNCH", skill)
        self.assertIn("[RELEASE_READY]", skill)
        self.assertIn("RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED", skill)
        browser_position = skill.index("[BROWSER-REGRESSION-QA-PROTOCOL")
        gauntlet_position = skill.index("[WEBSITE-GAUNTLET-PROTOCOL")
        self.assertLess(browser_position, gauntlet_position)
        self.assertIn("Browser QA must not become Gauntlet", skill)
        self.assertIn("Gauntlet must not duplicate Browser QA", skill)
        self.assertIn("BUILDER != CRITIC", skill)

    def test_conditional_capabilities_use_existing_build_dispatch(self) -> None:
        rows = {row["Capability"]: row for row in _kernel_routing_rows()}
        for capability in (
            "content_cms_operations",
            "localization",
            "application_commerce_auth",
            "immersive_web",
            "rive",
            "cinematic_integration",
            "page_experience",
            "signature_choreography",
        ):
            with self.subTest(capability=capability):
                self.assertEqual(rows[capability]["Primary stage"], "BUILD")
                self.assertIn("Conditional", rows[capability]["Required or conditional"])

        for relative in (
            "schemas/protocols.json",
            "schemas/gates.json",
            "schemas/state-ownership.json",
            "templates/site-profile.json",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotRegex(text, r'"kernel(?:[._])')

    def test_agent_comprehension_routes_are_deterministic(self) -> None:
        rows = {row["Capability"]: row for row in _kernel_routing_rows()}

        visual_direction = rows["visual_prototype"]
        self.assertEqual(visual_direction["Primary stage"], "DESIGN")
        self.assertIn("VISUAL-PROTOTYPE-PROTOCOL.md", visual_direction["Current authority"])

        auth = rows["application_commerce_auth"]
        self.assertEqual(auth["Primary stage"], "BUILD")
        self.assertIn("APPLICATION-COMMERCE-AUTH-PROTOCOL.md", auth["Current authority"])

        keyboard_accessibility = rows["browser_qa"]
        self.assertEqual(keyboard_accessibility["Primary stage"], "VERIFY")
        self.assertIn("Accessibility", keyboard_accessibility["Secondary dependencies"])
        self.assertIn("keyboard smoke", (ROOT / "SKILL.md").read_text(encoding="utf-8"))
        self.assertEqual(rows["accessibility"]["Primary stage"], "DESIGN")

        hero_image = rows["asset_director"]
        self.assertEqual(hero_image["Primary stage"], "ASSETS")
        self.assertIn("Provenance", hero_image["Secondary dependencies"])
        self.assertEqual(rows["provenance"]["Primary stage"], "ASSETS")

        production_release = rows["launch_operations"]
        self.assertEqual(production_release["Primary stage"], "RELEASE")
        self.assertIn("LAUNCH-OPERATIONS-PROTOCOL.md", production_release["Current authority"])

        competitor_research = rows["visual_research"]
        self.assertEqual(competitor_research["Primary stage"], "RESEARCH")
        self.assertIn("VISUAL-RESEARCH-PROTOCOL.md", competitor_research["Current authority"])
        reference_research = rows["external_inspiration_reference_research"]
        self.assertEqual(reference_research["Primary stage"], "RESEARCH")
        self.assertIn("REFERENCE", reference_research["Current authority"])

        changed_brand_direction = rows["visual_direction"]
        self.assertEqual(changed_brand_direction["Primary stage"], "DESIGN")
        self.assertIn("owner change request", (ROOT / "SKILL.md").read_text(encoding="utf-8"))

    def test_resident_dox_rail_is_portable_and_lazy(self) -> None:
        root = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("`SKILL.md` is the canonical operator router.", root)
        self.assertNotIn("file:///c:/", root.lower())
        self.assertNotIn("### Validated Pilots", root)
        self.assertNotRegex(root, r"(?im)^\s*-\s+.*\bStatus:")
        stale_route_text = (root + skill).replace("→", "->")
        self.assertNotIn("BRIEF -> DIRECTION -> IA", stale_route_text)
        self.assertNotIn("FEATURE_FREEZE = ACTIVE", root + skill)
        self.assertNotIn("ACTIVATION_TABLE", skill)

        child_index = root.split("## Child DOX Index", 1)[1]
        child_entries = [line for line in child_index.splitlines() if line.startswith("- [")]
        self.assertGreaterEqual(len(child_entries), 10)
        self.assertLessEqual(max(map(len, child_entries)), 180)
        self.assertIn("KERNEL_CAPABILITY_ROUTING_START", skill)
        self.assertIn("KERNEL_CAPABILITY_ROUTING_END", skill)

    def test_existing_registered_suite_count_remains_thirteen(self) -> None:
        registry = _load_json("schemas/test-suites.json")
        active = [entry for entry in registry["suites"] if entry.get("status") == "ACTIVE"]
        self.assertEqual(len(active), 13)
        self.assertEqual(len({entry["id"] for entry in active}), 13)
        self.assertNotIn("kernel", json.dumps(registry).lower())

    def test_protected_inventory_matches_checked_out_projects(self) -> None:
        registry = _load_json("schemas/frozen-projects.json")
        self.assertIsInstance(registry, dict)
        entries = registry["projects"]
        self.assertEqual(registry["inventory"]["project_count"], len(entries))
        self.assertEqual(
            registry["inventory"]["protected_file_count"],
            sum(1 for path in (ROOT / "projects").rglob("*") if path.is_file()),
        )
        self.assertTrue(all((ROOT / entry["path"]).is_dir() for entry in entries))

    def test_sixth_owner_lock_is_rejected(self) -> None:
        profile = _load_json("templates/site-profile.json")
        self.assertIsInstance(profile, dict)
        profile["locks"]["measurement_locked"] = False
        self.assertIn("OWNER_LOCK_INVARIANT", validator.validate_owner_locks(profile))

    def test_duplicate_active_state_owner_is_rejected(self) -> None:
        registry = {
            "states": [
                {
                    "path": "measurement.complete",
                    "canonical_concept": "measurement",
                    "status": "ACTIVE",
                    "owner_protocol": "A",
                },
                {
                    "path": "cro.complete",
                    "canonical_concept": "measurement",
                    "status": "ACTIVE",
                    "owner_protocol": "B",
                },
            ]
        }
        self.assertIn("DUPLICATE_CANONICAL_COMPLETION_FLAG", validator.validate_state_ownership_registry(registry))

    def test_duplicate_active_protocol_state_owner_is_rejected(self) -> None:
        registry = {
            "protocols": [
                {
                    "id": "A",
                    "path": "a.md",
                    "status": "ACTIVE",
                    "domain": "a",
                    "phase": "0",
                    "state_owner": "shared.status",
                },
                {
                    "id": "B",
                    "path": "b.md",
                    "status": "ACTIVE",
                    "domain": "b",
                    "phase": "0",
                    "state_owner": "shared.status",
                },
            ]
        }
        self.assertIn("DUPLICATE_PROTOCOL_STATE_OWNER", validator.validate_protocol_registry(registry))

    def test_broken_protocol_path_is_rejected(self) -> None:
        registry = {
            "protocols": [
                {
                    "id": "MISSING",
                    "path": "does-not-exist.md",
                    "status": "ACTIVE",
                    "domain": "fixture",
                    "phase": "0",
                    "state_owner": "fixture",
                }
            ]
        }
        self.assertIn("CANONICAL_PROTOCOL_EXISTS", validator.validate_protocol_paths(registry, ROOT))

    def test_broken_template_path_is_rejected(self) -> None:
        self.assertIn(
            "BROKEN_TEMPLATE_REFERENCE",
            validator.validate_template_references(["templates/does-not-exist.md"], ROOT),
        )

    def test_invalid_json_is_rejected(self) -> None:
        self.assertIn("INVALID_JSON_ARTIFACT", validator.validate_json_content("{not json"))

    def test_invalid_current_schema_shape_is_rejected(self) -> None:
        profile = _load_json("templates/site-profile.json")
        profile["project_name"] = None
        self.assertIn(
            "CURRENT_PROFILE_FIELD_TYPE",
            validator.validate_site_profile(
                profile,
                current=True,
                current_version=CURRENT_VERSION,
                legacy_versions=["2.10.0", "2.11.0", "2.11.1"],
            ),
        )

    def test_malformed_registry_is_rejected(self) -> None:
        self.assertIn("PROTOCOL_REGISTRY_SHAPE", validator.validate_protocol_registry({}))

    def test_malformed_semver_is_rejected(self) -> None:
        self.assertIsNone(validator.parse_semver("2.11"))
        self.assertIsNone(validator.parse_semver("2.11.01"))
        self.assertIsNone(validator.parse_semver("2.11.0-01"))

    def test_semver_orders_prerelease_before_release(self) -> None:
        self.assertLess(validator.parse_semver("2.11.0-beta"), validator.parse_semver("2.11.0"))

    def test_version_document_drift_is_rejected(self) -> None:
        self.assertIn(
            "VERSION_DOCUMENT_CONSISTENCY",
            validator.validate_version_markers("<!-- FRAMEWORK_VERSION: 2.10.0 -->", CURRENT_VERSION),
        )

    def test_historical_profile_remains_compatible(self) -> None:
        profile = {"schema_version": "2.4.0", "project_name": "historical", "cro": {"complete": False}}
        self.assertEqual(
            validator.validate_site_profile(
                profile,
                current=False,
                current_version=CURRENT_VERSION,
                legacy_versions=["2.4.0", "2.10.0", "2.11.0", "2.11.1"],
            ),
            [],
        )

    def test_historical_schema_matrix_remains_compatible(self) -> None:
        fixtures = _load_json("tests/fixtures/historical-profiles.json")
        self.assertIsInstance(fixtures, list)
        for fixture in fixtures:
            with self.subTest(release=fixture["release"]):
                self.assertEqual(
                    validator.validate_site_profile(
                        fixture["profile"],
                        current=False,
                        current_version=CURRENT_VERSION,
                        legacy_versions=[
                            "1.0.0",
                            "1.1.0",
                            "1.2.0",
                            "1.3.0",
                            "2.4.0",
                            "2.5.0",
                            "2.5.1",
                            "2.6.0",
                            "2.7.0",
                            "2.8.0",
                            "2.9.0",
                            "2.10.0",
                            "2.11.0",
                            "2.11.1",
                        ],
                    ),
                    [],
                )

    def test_historical_client_handoff_profile_compatibility(self) -> None:
        self._assert_historical_profile({"schema_version": "2.5.0", "handoff": {"status": "not_started"}})

    def test_historical_signature_choreography_profile_compatibility(self) -> None:
        self._assert_historical_profile({"schema_version": "2.5.1", "signature_choreography": {"complete": False}})

    def test_historical_security_privacy_profile_compatibility(self) -> None:
        self._assert_historical_profile({"schema_version": "2.7.0", "security_privacy": {"complete": False}})

    def test_historical_browser_qa_profile_compatibility(self) -> None:
        self._assert_historical_profile({"schema_version": "2.8.0", "browser_qa": {"complete": False}})

    def test_historical_accessibility_profile_compatibility(self) -> None:
        self._assert_historical_profile({"schema_version": "2.9.0", "accessibility": {"complete": False}})

    def test_historical_launch_profile_compatibility(self) -> None:
        self._assert_historical_profile(
            {
                "schema_version": "2.10.0",
                "launch_ops": {
                    "status": "NOT_EVALUATED",
                    "status_history": ["NOT_EVALUATED", "PLANNING"],
                },
            }
        )

    def test_historical_baseline_profile_compatibility(self) -> None:
        self._assert_historical_profile({"project_name": "V1 baseline", "locks": {"design_direction_locked": False}})

    def test_historical_capability_fixture_remains_structurally_compatible(self) -> None:
        evidence = _load_json("tests/fixtures/historical-certification-evidence.json")
        self.assertIsInstance(evidence, dict)
        self.assertEqual(
            set(evidence),
            {
                "purpose", "asset_director", "immersive", "rive", "page_experience",
                "analytics", "signature_choreography", "client_handoff",
            },
        )
        expected_versions = {"2.0.0", "2.1.0", "2.2.0", "2.3.0", "2.4.0", "2.5.0", "2.5.1"}
        canonical_locks = {
            "design_direction_locked", "information_architecture_locked",
            "content_structure_locked", "design_system_locked", "motion_direction_locked",
        }
        for capability, record in evidence.items():
            if capability == "purpose":
                continue
            with self.subTest(capability=capability):
                profile = record["profile"]
                self.assertIn(profile["schema_version"], expected_versions)
                self.assertEqual(set(profile["locks"]), canonical_locks)
                self.assertEqual(len(profile["locks"]), 5)
                self.assertFalse(any("_locked" in key and key not in canonical_locks for key in profile["locks"]))

        current = _load_json("templates/site-profile.json")
        self.assertIn("measurement", current)
        self.assertNotIn("cro", current)

    def _assert_historical_profile(self, profile: dict[str, object]) -> None:
        self.assertEqual(
            validator.validate_site_profile(
                profile,
                current=False,
                current_version=CURRENT_VERSION,
                legacy_versions=[
                    "1.0.0",
                    "1.1.0",
                    "1.2.0",
                    "1.3.0",
                    "2.4.0",
                    "2.5.0",
                    "2.5.1",
                    "2.6.0",
                    "2.7.0",
                    "2.8.0",
                    "2.9.0",
                    "2.10.0",
                    "2.11.0",
                    "2.11.1",
                ],
            ),
            [],
        )

    def test_obsolete_current_state_is_rejected(self) -> None:
        profile = _load_json("templates/site-profile.json")
        self.assertIsInstance(profile, dict)
        profile["cro"] = {"complete": False}
        self.assertIn(
            "OBSOLETE_CURRENT_STATE",
            validator.validate_site_profile(
                profile,
                current=True,
                current_version=CURRENT_VERSION,
                legacy_versions=["2.10.0", "2.11.0", "2.11.1"],
            ),
        )

    def test_unknown_gate_owner_is_rejected(self) -> None:
        registry = {
            "gates": [
                {
                    "name": "FIXTURE_GATE",
                    "type": "VERIFICATION",
                    "authoritative_state": "fixture.status",
                    "phase": "0",
                    "owner_protocol": "UNKNOWN",
                    "owner_artifact": "framework-validation/reports/runtime/framework-validation-report.json",
                    "status": "ACTIVE",
                }
            ]
        }
        self.assertIn(
            "UNKNOWN_GATE_OWNER",
            validator.validate_gate_registry(registry, protocol_ids=["FRAMEWORK_VALIDATION"], phase_ids=["0"]),
        )

    def test_owner_lock_gate_classification_rejects_unapproved_lock(self) -> None:
        registry = {
            "gates": [
                {
                    "name": "DESIGN_DIRECTION_LOCKED",
                    "type": "OWNER_LOCK",
                    "authoritative_state": "locks.design_direction_locked",
                    "phase": "0",
                    "owner_protocol": "FRAMEWORK_VALIDATION",
                    "owner_artifact": "templates/site-profile.json",
                    "status": "ACTIVE",
                },
                {
                    "name": "MEASUREMENT_LOCKED",
                    "type": "OWNER_LOCK",
                    "authoritative_state": "measurement.complete",
                    "phase": "0",
                    "owner_protocol": "FRAMEWORK_VALIDATION",
                    "owner_artifact": "templates/site-profile.json",
                    "status": "ACTIVE",
                },
            ]
        }
        self.assertIn("OWNER_LOCK_INVARIANT", validator.validate_gate_registry(registry))

    def test_read_only_workflow_is_valid(self) -> None:
        workflow = (ROOT / ".github/workflows/framework-validation.yml").read_text(encoding="utf-8")
        self.assertEqual(validator.validate_workflow_text(workflow), [])

    def test_write_workflow_permission_is_rejected(self) -> None:
        workflow = "name: fixture\npermissions:\n  contents: write\njobs:\n  test:\n    runs-on: ubuntu-latest\n"
        self.assertIn("CI_READ_ONLY_PERMISSIONS", validator.validate_workflow_text(workflow))

    def test_frozen_integrity_guard_detects_mutation(self) -> None:
        guard_class = validator._load_guard(ROOT, "browser-qa/guards/frozen_integrity_guard.py")
        self.assertIsNotNone(guard_class)
        with tempfile.TemporaryDirectory(prefix="website-director-frozen-test-") as directory:
            root = Path(directory)
            frozen_file = root / "projects" / "fixture" / "state.json"
            frozen_file.parent.mkdir(parents=True)
            frozen_file.write_text("{}", encoding="utf-8")
            guard = guard_class(str(root), protected_paths=["projects/"], ledger_path="runtime/violations.log", run_id="test")
            guard.snapshot()
            frozen_file.write_text('{"mutated": true}', encoding="utf-8")
            result = guard.verify()
            self.assertFalse(result.ok)
            self.assertTrue(result.mutations)

    def test_mutation_probe_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-mutation-test-") as directory:
            root = Path(directory)
            source = root / "README.md"
            source.write_text("baseline\n", encoding="utf-8")

            def mutate(path: Path) -> None:
                (path / "README.md").write_text("mutated\n", encoding="utf-8")

            report = validator.validate_repository(
                root,
                run_suites=False,
                run_negative_controls=False,
                mutation_probe=mutate,
            )
            failed_rules = {check["rule_id"] for check in report["checks"] if check["status"] == "FAIL"}
            self.assertIn("MUTATION_EVIDENCE_READ_ONLY", failed_rules)

    def test_negative_controls_all_prove_real_signals(self) -> None:
        report = validator.validate_repository(ROOT, run_suites=False, run_negative_controls=True)
        self.assertTrue(report["negative_controls"])
        self.assertTrue(all(item["caught"] for item in report["negative_controls"]), report["negative_controls"])

    def test_report_contains_required_identity_and_finding_fields(self) -> None:
        report = validator.validate_repository(ROOT, run_suites=False, run_negative_controls=True)
        for key in ("framework_version", "commit_sha", "timestamp", "status", "checks_total", "findings"):
            self.assertIn(key, report)
        for finding in report["findings"]:
            self.assertEqual(
                set(finding),
                {"RULE_ID", "SEVERITY", "FILE", "LOCATION", "MESSAGE", "EXPECTED", "OBSERVED", "OWNER"},
            )


if __name__ == "__main__":
    unittest.main()
