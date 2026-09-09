"""Regression controls for owner authority, brand truth, and runtime motion.

The fixtures are synthetic and disposable. They prove the framework behavior
without rebuilding or modifying any Website Director pilot.
"""

from __future__ import annotations

import contextlib
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "browser-qa"))

from assertions import evaluate  # noqa: E402
from engine.base import BLOCKED, FAIL, PASS, PageObservation, load_engine  # noqa: E402
from framework_validation.owner_intent import (  # noqa: E402
    AUTHORITY_PRECEDENCE,
    audit_owner_requirement_compliance,
    detect_contradictions,
    resolve_approved_motion_downgrade,
    resolve_authority_conflicts,
    resolve_motion_requirement,
    resolve_owner_authority,
    validate_brand_tokens,
    validate_motion_implementation_trace,
    validate_owner_intent_contract,
    validate_reference_translation_trace,
)
from guards.frozen_integrity_guard import FrozenIntegrityGuard  # noqa: E402
import runner as bqa_runner  # noqa: E402


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



@contextlib.contextmanager
def static_fixture():
    """A disposable static page with no motion of any kind."""
    with tempfile.TemporaryDirectory(prefix="website-director-static-") as directory:
        fixture = Path(directory)
        (fixture / "index.html").write_text(
            "<!doctype html><html><body><main>Static page</main></body></html>", encoding="utf-8")
        (fixture / "qa-fixture.json").write_text(json.dumps({"title": "Static fixture"}),
                                                 encoding="utf-8")
        yield fixture


def motion_observation(rows, *, engine="playwright", identity="REAL_BROWSER",
                       reduced_motion=False, route="."):
    return PageObservation(
        route=route, viewport=1440, engine=engine, browser="chromium",
        reduced_motion=reduced_motion, motion_observations=list(rows),
        raw={"motion_observations": list(rows), "engine_identity": identity},
    )


def scroll_only_row(sequence_id="hero-intro", *, family=None, scroll=6156.0):
    """A tall static page that merely scrolled.

    Every flag a naive reader might accept is present and truthful about the
    stimulus; nothing about the element itself changed.
    """
    row = {
        "sequence_id": sequence_id,
        "engine_identity": "REAL_BROWSER",
        "runtime_observed": True,
        "observation_supported": True,
        "target_count": 12,
        "trigger": "scroll_to",
        "trigger_applied": True,
        "changed_properties": [],
        "max_geometry_delta": 0.0,
        "max_opacity_delta": 0.0,
        "max_transform_delta": 0.0,
        "max_media_time_delta": 0.0,
        "raw_viewport_geometry_delta": scroll,
        "stimulus_scroll_delta": scroll,
        "scroll_delta": scroll,
        "state_changed": False,
        "meaningful_state_change": False,
        "motion_state_changes": 0,
        "observed_states": ["START"],
        "family_source": "MEASURED",
        "family": family or "MEASURED_NONE",
        "runtime_evidence_ref": "REAL_BROWSER:%s" % sequence_id,
    }
    return row


def responding_row(sequence_id="hero-intro", *, family="PARALLAX_MASK"):
    return {
        "sequence_id": sequence_id,
        "engine_identity": "REAL_BROWSER",
        "runtime_observed": True,
        "observation_supported": True,
        "target_count": 3,
        "trigger": "scroll_to",
        "trigger_applied": True,
        "changed_properties": ["transform", "clip"],
        "max_geometry_delta": 42.0,
        "max_opacity_delta": 0.0,
        "max_transform_delta": 1.0,
        "max_media_time_delta": 0.0,
        "raw_viewport_geometry_delta": 900.0,
        "stimulus_scroll_delta": 900.0,
        "scroll_delta": 900.0,
        "state_changed": True,
        "meaningful_state_change": True,
        "motion_state_changes": 0,
        "observed_states": ["START", "CHANGE", "SETTLE"],
        "family_source": "DECLARED",
        "family": family,
        "runtime_evidence_ref": "REAL_BROWSER:%s" % sequence_id,
    }


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

    # ------------------------------------------------------------------
    # Candidate repair controls: owner requirements reach the boundary.
    # Every owner/approval record below is synthetic, TEST_ONLY, and is
    # never written into a project or an approval history.
    # ------------------------------------------------------------------
    def test_stale_or_mixed_loaded_harness_is_detected_before_verification(self) -> None:
        healthy = bqa_runner.harness_identity({})
        self.assertEqual(healthy["status"], "PASS")
        self.assertTrue(all(item["sha256"] for item in healthy["modules"]
                            if item["status"] == "LOADED" and item["path"]))
        stale = types.SimpleNamespace(
            __name__="stale.catalog", __file__=None, ALL_CHECKS=[],
            check_observation_coverage=lambda obs, plan: None,
            check_reduced_motion=lambda obs, plan: None,
            check_forms=lambda obs, plan: None,
            check_accessibility=lambda obs, plan: None,
        )
        result = bqa_runner.harness_identity({}, catalog_module=stale)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("check_motion", result["missing_checks"])
        self.assertIn("check_brand_tokens", result["missing_checks"])
        mixed = types.SimpleNamespace(
            __name__="mixed.catalog", __file__=None,
            ALL_CHECKS=[],
            **{name: (lambda obs, plan: None) for name in bqa_runner.REQUIRED_CHECK_FUNCTIONS})
        mixed_result = bqa_runner.harness_identity({}, catalog_module=mixed)
        self.assertEqual(mixed_result["status"], "PASS")
        design_first = bqa_runner.harness_identity(
            {"visual_evidence": {"required_surfaces": ["DESKTOP_FULL_HOMEPAGE"]}})
        self.assertIn("framework_validation.design_first_flow",
                      [item["module"] for item in design_first["modules"]])

    def test_current_level_three_with_omitted_motion_block_is_never_none_or_pass(self) -> None:
        for plan in (
            {"routes": [{"path": "."}], "owner_intent": load_owner_contract()},
            {"routes": [{"path": "."}], "owner_intent_ref": str(OWNER_CONTRACT),
             "project_currentness": "CURRENT"},
        ):
            with static_fixture() as fixture:
                observation = load_engine("simulation", str(fixture)).observe(".", 1440)
                findings = evaluate(observation, plan)
            motion = {finding.check_id: finding.verdict for finding in findings
                      if finding.check_id.startswith("motion.")}
            self.assertIn("motion.observation-coverage", motion)
            self.assertEqual(motion["motion.observation-coverage"], BLOCKED)
            self.assertNotIn(PASS, set(motion.values()))

    def test_removing_the_owner_block_cannot_remove_project_requirements(self) -> None:
        # The manifest carries no owner_intent, motion, runtime_observations or
        # visual_evidence block - only the fact that this is a current candidate.
        authority = resolve_owner_authority(
            {"project_currentness": "CURRENT", "owner_intent_ref": str(OWNER_CONTRACT)})
        self.assertEqual(authority["status"], "PASS")
        self.assertEqual(authority["coverage"]["motion"], "REQUIRED")
        self.assertEqual(authority["coverage"]["visual_evidence"], "REQUIRED")
        self.assertEqual(authority["motion"]["required_level"], "MOTION_LEVEL_3")
        # A current candidate that names no contract at all blocks; it does not
        # quietly become "no owner level".
        unresolved = resolve_owner_authority({"project_currentness": "CURRENT"})
        self.assertEqual(unresolved["status"], "BLOCKED")
        self.assertIn("OWNER_CONTRACT_NOT_RESOLVED", str(unresolved["blocked_reason"]))
        # A silent legacy manifest still infers nothing.
        self.assertEqual(resolve_owner_authority({"routes": []})["status"], "NOT_DECLARED")

    def test_lower_plan_level_cannot_downgrade_a_required_owner_level(self) -> None:
        plan = {
            "routes": [{"path": "."}],
            "owner_intent": load_owner_contract(),
            "runtime_observations": {"motion": {
                "required": True, "minimum_motion_level": "MOTION_LEVEL_1",
                "sequences": [{"sequence_id": "hero-intro"}]}},
        }
        observation = motion_observation([scroll_only_row("hero-intro")])
        findings = {finding.check_id: finding for finding in evaluate(observation, plan)}
        # At the plan's own MOTION_LEVEL_1 none of these Level 2/3 checks would
        # exist at all; the owner level is what put them on the run.
        self.assertEqual(findings["motion.real-browser-runtime"].evidence["required_level"], 3)
        self.assertEqual(findings["motion.real-browser-runtime"].evidence["required_level_source"], "OWNER")
        self.assertEqual(findings["motion.runtime-state-change"].verdict, FAIL)
        # A simulation engine cannot satisfy the raised level either.
        simulated = motion_observation([scroll_only_row("hero-intro")],
                                       engine="simulation", identity="SIMULATION")
        simulated_findings = {finding.check_id: finding.verdict
                              for finding in evaluate(simulated, plan)}
        self.assertEqual(simulated_findings["motion.real-browser-runtime"], BLOCKED)

    def test_contract_resolution_error_blocks_instead_of_downgrading(self) -> None:
        plan = {"routes": [{"path": "."}], "owner_intent_ref": "does/not/exist.json"}
        observation = motion_observation([])
        verdicts = {finding.check_id: finding.verdict for finding in evaluate(observation, plan)}
        self.assertEqual(verdicts["motion.owner-authority"], BLOCKED)
        self.assertEqual(verdicts["brand.owner-authority"], BLOCKED)
        malformed = resolve_owner_authority({"owner_intent": "not-an-object"})
        self.assertEqual(malformed["status"], "BLOCKED")
        self.assertIn("OWNER_CONTRACT_MALFORMED", str(malformed["blocked_reason"]))

    def test_historical_scope_preserves_documented_compatibility(self) -> None:
        plan = {"routes": [{"path": "."}], "owner_intent": load_owner_contract(),
                "project_currentness": "HISTORICAL"}
        authority = resolve_owner_authority(plan)
        self.assertEqual(authority["status"], "HISTORICAL")
        self.assertEqual(authority["coverage"], {"motion": "NOT_REQUIRED", "brand": "NOT_REQUIRED",
                                                 "visual_evidence": "NOT_REQUIRED"})
        observation = motion_observation([])
        self.assertFalse([finding for finding in evaluate(observation, plan)
                          if finding.check_id.startswith(("motion.", "brand."))])

    def test_only_a_genuine_owner_downgrade_record_is_honoured(self) -> None:
        approved = {
            "approved_downgrade": True,
            "approved_by": "OWNER",
            "owner_event_ref": "TEST_ONLY-synthetic-owner-event-001",
            "scope": "ALPHA_STARTS_NOW_CURRENT_CANDIDATE",
        }
        authority = resolve_owner_authority(
            {"owner_intent": load_owner_contract(),
             "locked_decisions": {"heuristic_motion_level": "MOTION_LEVEL_1",
                                  "approved_motion_downgrade": approved}})
        self.assertTrue(authority["motion"]["approved_downgrade"])
        self.assertEqual(authority["motion"]["execution_level"], "MOTION_LEVEL_1")
        self.assertEqual(authority["motion"]["required_level"], "MOTION_LEVEL_3")

        for fabricated in (
            {"approved_downgrade": True},
            {"approved_downgrade": True, "approved_by": "INTERNAL_CRITIC",
             "owner_event_ref": "TEST_ONLY-x"},
            {"approved_downgrade": True, "approved_by": "OWNER",
             "owner_event_ref": "TEST_ONLY-x", "scope": "A_DIFFERENT_PROJECT"},
        ):
            result = resolve_approved_motion_downgrade(
                {"locked_decisions": {"approved_motion_downgrade": fabricated}},
                None, "ALPHA_STARTS_NOW_CURRENT_CANDIDATE")
            self.assertFalse(result["approved"])
            self.assertTrue(result["issues"])
        blocked = resolve_owner_authority(
            {"owner_intent": load_owner_contract(),
             "motion": {"approved_downgrade": True}})
        self.assertEqual(blocked["status"], "BLOCKED")

    def test_preferred_or_optional_motion_never_becomes_required(self) -> None:
        contract = load_owner_contract()
        for requirement_class, expected in (("PREFERRED", "OPTIONAL"), ("OPTIONAL", "OPTIONAL")):
            softened = json.loads(json.dumps(contract))
            for item in softened["requirements"]:
                if item["id"] == "motion.owner-cinematic":
                    item["class"] = requirement_class
            authority = resolve_owner_authority({"owner_intent": softened})
            self.assertEqual(authority["coverage"]["motion"], expected)
            plan = {"routes": [{"path": "."}], "owner_intent": softened}
            observation = motion_observation([])
            self.assertFalse([finding for finding in evaluate(observation, plan)
                              if finding.check_id.startswith("motion.")])

    def test_historical_signature_choreography_fixture_remains_compatible(self) -> None:
        """Keep the retired choreography contract under the current motion suite."""
        registry = json.loads(
            (ROOT / "templates" / "signature-interaction-registry.json").read_text(encoding="utf-8")
        )
        self.assertEqual(registry.get("schema_version"), "2.5.1")
        patterns = registry.get("patterns", [])
        self.assertGreaterEqual(len(patterns), 18)
        pattern_ids = [pattern["pattern_id"] for pattern in patterns]
        self.assertEqual(len(pattern_ids), len(set(pattern_ids)))
        required_fields = {
            "pattern_id", "pattern_name", "family", "description", "narrative_purpose",
            "best_for", "avoid_when", "primary_technique", "mobile_strategy",
            "reduced_motion_strategy", "accessibility_risk", "performance_risk",
            "novelty_level", "complexity_level", "content_requirements", "signature_potential",
        }
        self.assertTrue(all(required_fields <= set(pattern) for pattern in patterns))

        fixture = json.loads(
            (ROOT / "tests" / "fixtures" / "historical-certification-evidence.json").read_text(
                encoding="utf-8"
            )
        )
        signature = fixture["signature_choreography"]
        profile = signature["profile"]
        self.assertEqual(profile.get("schema_version"), "2.5.1")
        self.assertEqual(len(profile.get("locks", {})), 5)
        self.assertNotIn("signature_choreography_locked", profile["locks"])
        self.assertEqual(
            profile["signature_choreography"],
            {
                "primary_pattern": "PINNED_HORIZONTAL_SCROLLYTELLING",
                "supporting_pattern": "SCROLL_DRIVEN_ASSEMBLY",
                "interaction_level": "2_FEATURE",
                "mobile_strategy": "REFLOWED",
            },
        )

        html = "\n".join(signature["html_markers"])
        self.assertIn('id="atelier-scrollytelling"', html)
        self.assertIn('id="chapter-01"', html)
        self.assertIn('id="chapter-05"', html)
        self.assertIn('id="assembly-container"', html)
        self.assertIn('id="capabilities"', html)
        css = "\n".join(signature["css_markers"])
        self.assertIn("@media (max-width: 768px)", css)
        self.assertIn("width: 100%", css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        js = "\n".join(signature["js_markers"])
        self.assertIn("ScrollTrigger", js)
        self.assertIn("gsap.to", js)
        self.assertIn("prefers-reduced-motion", js)
        self.assertTrue(signature["source_hashes_present"])
        for legacy_profile in signature["legacy_profiles"]:
            with self.subTest(profile=legacy_profile["name"]):
                self.assertNotIn("signature_choreography", legacy_profile)


if __name__ == "__main__":
    unittest.main()
