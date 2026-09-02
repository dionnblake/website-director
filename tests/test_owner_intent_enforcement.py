"""Regression controls for owner authority, brand truth, and runtime motion.

The fixtures are synthetic and disposable. They prove the framework behavior
without rebuilding or modifying any Website Director pilot.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "browser-qa"))

from assertions import evaluate  # noqa: E402
from engine.base import BLOCKED, FAIL, PASS, load_engine  # noqa: E402
from framework_validation.owner_intent import (  # noqa: E402
    AUTHORITY_PRECEDENCE,
    audit_owner_requirement_compliance,
    detect_contradictions,
    resolve_authority_conflicts,
    resolve_motion_requirement,
    validate_brand_tokens,
    validate_motion_implementation_trace,
    validate_owner_intent_contract,
    validate_reference_translation_trace,
)
from guards.frozen_integrity_guard import FrozenIntegrityGuard  # noqa: E402


OWNER_CONTRACT = ROOT / "templates" / "alpha-starts-now-owner-intent.json"


def load_owner_contract() -> dict[str, object]:
    return json.loads(OWNER_CONTRACT.read_text(encoding="utf-8"))


def requirement(identifier: str, target: str, domain: str, value: object,
                *, authority: str, currentness: str = "CURRENT",
                requirement_class: str = "REQUIRED", **extra: object) -> dict[str, object]:
    return {
        "id": identifier,
        "target": target,
        "domain": domain,
        "class": requirement_class,
        "requirement": value,
        "values": value,
        "source": identifier,
        "currentness": currentness,
        "scope": "TEST_FIXTURE",
        "authority": authority,
        **extra,
    }


def cinematic_motion_fixture() -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    brief = {
        "cinematic_specialist_required": False,
        "sequences": [
            {"sequence_id": "hero-intro", "name": "Hero intro"},
            {"sequence_id": "subject-reveal", "name": "Subject reveal"},
        ],
    }
    implementation = {
        "sequences": [
            {"sequence_id": "hero-intro", "location": "src/motion/hero.ts", "family": "KINETIC_TYPE"},
            {"sequence_id": "subject-reveal", "location": "src/motion/reveal.ts", "family": "PARALLAX_MASK"},
        ],
    }
    runtime = {
        "engine_identity": "REAL_BROWSER",
        "runtime_observed": True,
        "motion_observations": [
            {"sequence_id": "hero-intro", "meaningful_state_change": True, "family": "KINETIC_TYPE"},
            {"sequence_id": "subject-reveal", "meaningful_state_change": True, "family": "PARALLAX_MASK"},
        ],
    }
    return brief, implementation, runtime


class OwnerIntentEnforcementTests(unittest.TestCase):
    def test_01_current_owner_wins_historical_brand(self) -> None:
        result = resolve_authority_conflicts([
            requirement("current-navy", "brand.primary", "brand", "navy blue",
                        authority="CURRENT_OWNER_INSTRUCTION"),
            requirement("historical-orange", "brand.primary", "brand", "orange",
                        authority="HISTORICAL_PROJECT_MATERIAL", currentness="HISTORICAL"),
        ])
        self.assertEqual(result["status"], PASS)
        resolution = result["resolutions"][0]
        self.assertEqual(resolution["winner"]["id"], "current-navy")
        self.assertEqual(resolution["losers"][0]["classification"], "LEGACY")

    def test_02_reference_signal_is_not_authority(self) -> None:
        result = resolve_authority_conflicts([
            requirement("current-navy", "brand.primary", "brand", "navy blue",
                        authority="CURRENT_OWNER_INSTRUCTION"),
            requirement("reference-cream", "brand.primary", "brand", "cream",
                        authority="REFERENCE_INSPIRATION_INTELLIGENCE", currentness="REFERENCE_ONLY"),
        ])
        self.assertEqual(result["status"], PASS)
        self.assertEqual(result["resolutions"][0]["winner"]["id"], "current-navy")
        self.assertEqual(result["resolutions"][0]["losers"][0]["classification"], "NON_AUTHORITATIVE")

    def test_03_explicit_cinematic_motion_beats_level_one_heuristic(self) -> None:
        result = resolve_motion_requirement([
            requirement("owner-cinematic", "motion.level", "motion", "cinematic animation-heavy direction",
                        authority="CURRENT_OWNER_INSTRUCTION", minimum_motion_level="MOTION_LEVEL_3"),
        ], heuristic_level="MOTION_LEVEL_1")
        self.assertEqual(result["owner_required_level"], "MOTION_LEVEL_3")
        self.assertEqual(result["recommended_level"], "MOTION_LEVEL_3")
        self.assertEqual(result["execution_level"], "MOTION_LEVEL_3")

    def test_04_level_three_without_runtime_evidence_fails_closed(self) -> None:
        result = validate_motion_implementation_trace(
            {"owner_required_level": "MOTION_LEVEL_3"},
            {"sequences": ["hero-intro"]},
            {"sequences": [{"sequence_id": "hero-intro", "location": "src/motion.ts", "family": "KINETIC_TYPE"}]},
            {"engine_identity": "REAL_BROWSER", "runtime_observed": False, "motion_observations": []},
        )
        self.assertNotEqual(result["status"], PASS)
        self.assertIn("MOTION_RUNTIME_EVIDENCE_REQUIRED", {item["code"] for item in result["issues"]})

    def test_05_gsap_or_named_sequence_without_state_change_fails(self) -> None:
        result = validate_motion_implementation_trace(
            {"owner_required_level": "MOTION_LEVEL_3"},
            {"sequences": ["hero-intro"]},
            {"sequences": [{"sequence_id": "hero-intro", "location": "src/gsap.ts", "family": "TIMELINE"}]},
            {"engine_identity": "REAL_BROWSER", "runtime_observed": True,
             "motion_observations": [{"sequence_id": "hero-intro", "state_changed": False}]},
        )
        self.assertNotEqual(result["status"], PASS)
        self.assertIn("MOTION_RUNTIME_STATE_CHANGE_MISSING", {item["code"] for item in result["issues"]})

    def test_06_generic_fade_only_motion_fails_diversity_guard(self) -> None:
        result = validate_motion_implementation_trace(
            {"owner_required_level": "MOTION_LEVEL_3"},
            {"sequences": ["one", "two"]},
            {"sequences": [
                {"sequence_id": "one", "location": "src/a.ts", "family": "FADE_UP"},
                {"sequence_id": "two", "location": "src/b.ts", "family": "GENERIC_REVEAL"},
            ]},
            {"engine_identity": "REAL_BROWSER", "runtime_observed": True,
             "motion_observations": [
                 {"sequence_id": "one", "meaningful_state_change": True},
                 {"sequence_id": "two", "meaningful_state_change": True},
             ]},
        )
        self.assertNotEqual(result["status"], PASS)
        self.assertIn("MOTION_GENERIC_FADE_DIVERSITY_REQUIRED", {item["code"] for item in result["issues"]})

    def test_07_meaningful_named_sequences_and_real_evidence_pass(self) -> None:
        brief, implementation, runtime = cinematic_motion_fixture()
        result = validate_motion_implementation_trace(
            {"owner_required_level": "MOTION_LEVEL_3"}, brief, implementation, runtime)
        self.assertEqual(result["status"], PASS)
        self.assertEqual(result["runtime_sequence_count"], 2)
        self.assertEqual(len(result["traces"]), 2)

    def test_08_no_explicit_high_motion_keeps_level_one(self) -> None:
        result = resolve_motion_requirement([], heuristic_level="MOTION_LEVEL_1")
        self.assertEqual(result["status"], PASS)
        self.assertIsNone(result["owner_required_level"])
        self.assertEqual(result["execution_level"], "MOTION_LEVEL_1")

    def test_owner_high_motion_cannot_select_level_one(self) -> None:
        brief, implementation, runtime = cinematic_motion_fixture()
        owner = {
            "requirements": [requirement(
                "owner-cinematic", "motion.level", "motion", "cinematic",
                authority="CURRENT_OWNER_INSTRUCTION", minimum_motion_level="MOTION_LEVEL_3")]
        }
        result = audit_owner_requirement_compliance(
            owner,
            {"execution_motion_level": "MOTION_LEVEL_1"},
            {"motion_brief": brief, "motion": implementation},
            runtime,
        )
        self.assertEqual(result["OWNER_REQUIREMENT_COMPLIANCE"], "FAIL")
        self.assertIn("OWNER_MOTION_DOWNGRADE_BLOCKED", {item["code"] for item in result["issues"]})

    def test_09_alpha_starts_now_orange_is_legacy_not_current(self) -> None:
        contract = load_owner_contract()
        self.assertEqual(validate_owner_intent_contract(contract)["status"], PASS)
        self.assertEqual(validate_brand_tokens(contract, {
            "color_roles": {"primary": "ASN_NAVY", "accent": "ASN_YELLOW"}
        })["status"], PASS)
        result = validate_brand_tokens(contract, {
            "color_roles": {"primary": "orange", "accent": "yellow"}
        })
        self.assertEqual(result["status"], FAIL)
        self.assertIn("UNAPPROVED_DOMINANT_BRAND_HUE", {item["code"] for item in result["issues"]})

    def test_10_frozen_historical_projects_are_not_mutated(self) -> None:
        guard = FrozenIntegrityGuard(ROOT, ["projects/"], run_id="owner-intent-regression")
        guard.snapshot()
        result = guard.verify()
        self.assertTrue(result.ok, result.summary())

    def test_11_neutral_accessibility_colors_remain_allowed(self) -> None:
        result = validate_brand_tokens(load_owner_contract(), {
            "color_roles": {
                "primary": "ASN_NAVY", "accent": "ASN_YELLOW",
                "background": "white", "text": "#111111", "border": "#d9d9d9",
            }
        })
        self.assertEqual(result["status"], PASS)

    def test_neutral_cannot_replace_an_approved_primary_brand_role(self) -> None:
        result = validate_brand_tokens(load_owner_contract(), {
            "color_roles": {"primary": "black", "accent": "white"}
        })
        self.assertEqual(result["status"], FAIL)
        self.assertIn("UNAPPROVED_DOMINANT_BRAND_HUE", {item["code"] for item in result["issues"]})

    def test_12_explicit_prohibition_violation_fails_compliance_audit(self) -> None:
        owner = {
            "requirements": [requirement(
                "no-orange", "brand.current_palette", "brand", ["orange"],
                authority="CURRENT_OWNER_INSTRUCTION", requirement_class="PROHIBITED")]
        }
        result = audit_owner_requirement_compliance(
            owner, {}, {"violations": ["orange"]}, {})
        self.assertEqual(result["OWNER_REQUIREMENT_COMPLIANCE"], "FAIL")
        self.assertIn("PROHIBITED_OWNER_CONSTRAINT_VIOLATION", {item["code"] for item in result["issues"]})

    def test_reference_translation_trace_requires_client_specific_implementation(self) -> None:
        result = validate_reference_translation_trace({
            "signal_class": "TRANSFERABLE_PRINCIPLE",
            "source_signal": "large subject reveal",
            "transferable_principle": "reveal the subject before secondary detail",
            "client_specific_interpretation": "use the approved Alpha Starts Now subject and palette",
            "implementation_ref": "src/motion/subject-reveal.ts",
            "non_copy_boundary": "do not copy source colors, type, or copy",
            "implemented": True,
        })
        self.assertEqual(result["status"], PASS)

    def test_disposable_fixture_static_screenshot_only_does_not_pass_motion(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-owner-intent-") as directory:
            fixture = Path(directory)
            (fixture / "index.html").write_text(
                "<!doctype html><html><body><main>Static page</main></body></html>",
                encoding="utf-8",
            )
            (fixture / "qa-fixture.json").write_text(json.dumps({
                "title": "Static fixture",
                "motion": {},
            }), encoding="utf-8")
            plan = {
                "routes": [{"path": ".", "viewports": [1440]}],
                "runtime_observations": {
                    "motion": {
                        "required": True,
                        "minimum_motion_level": "MOTION_LEVEL_3",
                        "sequences": ["hero-intro"],
                    }
                },
            }
            observation = load_engine("simulation", str(fixture)).observe(
                ".", 1440, browser="simulation")
            findings = evaluate(observation, plan)
            verdicts = {finding.check_id: finding.verdict for finding in findings}
            self.assertEqual(verdicts["motion.observation-coverage"], BLOCKED)
            self.assertNotEqual(all(value in (PASS, "NOT_APPLICABLE") for value in verdicts.values()), True)

    def test_browser_brand_assertion_rejects_rendered_historical_hue(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-brand-runtime-") as directory:
            fixture = Path(directory)
            (fixture / "index.html").write_text(
                "<!doctype html><html><body><main>Rendered fixture</main></body></html>",
                encoding="utf-8",
            )
            (fixture / "qa-fixture.json").write_text(json.dumps({
                "rendered_colors": [
                    {"value": "ASN_NAVY", "role": "primary", "area_ratio": 0.5},
                    {"value": "orange", "role": "accent", "area_ratio": 0.2},
                ]
            }), encoding="utf-8")
            observation = load_engine("simulation", str(fixture)).observe(".", 1440)
            findings = evaluate(observation, {
                "routes": [{"path": "."}],
                "owner_intent": load_owner_contract(),
            })
            result = next(finding for finding in findings if finding.check_id == "brand.current-palette")
            self.assertEqual(result.verdict, FAIL)

    def test_same_tier_contradiction_is_not_silently_averaged(self) -> None:
        result = detect_contradictions([
            requirement("owner-a", "motion.level", "motion", "MOTION_LEVEL_2",
                        authority="CURRENT_OWNER_INSTRUCTION"),
            requirement("owner-b", "motion.level", "motion", "MOTION_LEVEL_3",
                        authority="CURRENT_OWNER_INSTRUCTION"),
        ])
        self.assertEqual(result["status"], FAIL)
        self.assertTrue(result["contradictions"])


if __name__ == "__main__":
    unittest.main()
