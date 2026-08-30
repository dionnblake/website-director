"""Capability 6 regression and negative-control tests.

These tests exercise pure validator rules with synthetic data and keep all
mutation probes inside temporary directories. They do not treat missing
historical material as permission to regenerate it.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from framework_validation import validator


ROOT = Path(__file__).resolve().parents[1]
CURRENT_VERSION = "2.13.0"


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

    def test_frozen_inventory_matches_checked_out_corpus(self) -> None:
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

    def test_v2_5_client_handoff_compatibility(self) -> None:
        self._assert_historical_profile({"schema_version": "2.5.0", "handoff": {"status": "not_started"}})

    def test_v2_5_1_signature_choreography_compatibility(self) -> None:
        self._assert_historical_profile({"schema_version": "2.5.1", "signature_choreography": {"complete": False}})

    def test_v2_7_security_privacy_compatibility(self) -> None:
        self._assert_historical_profile({"schema_version": "2.7.0", "security_privacy": {"complete": False}})

    def test_v2_8_browser_regression_qa_compatibility(self) -> None:
        self._assert_historical_profile({"schema_version": "2.8.0", "browser_qa": {"complete": False}})

    def test_v2_9_accessibility_compatibility(self) -> None:
        self._assert_historical_profile({"schema_version": "2.9.0", "accessibility": {"complete": False}})

    def test_v2_10_launch_operations_compatibility(self) -> None:
        self._assert_historical_profile(
            {
                "schema_version": "2.10.0",
                "launch_ops": {
                    "status": "NOT_EVALUATED",
                    "status_history": ["NOT_EVALUATED", "PLANNING"],
                },
            }
        )

    def test_examples_runner_compatibility(self) -> None:
        self._assert_historical_profile({"project_name": "V1 baseline", "locks": {"design_direction_locked": False}})

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

    def test_invalid_state_transition_is_rejected(self) -> None:
        self.assertFalse(validator.validate_transition_path(["NOT_EVALUATED", "STABILIZED"]))

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
