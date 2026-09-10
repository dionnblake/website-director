"""Focused synthetic controls for the locked visual-first architecture."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

from framework_validation.visual_first import (
    choose_anchor_policy,
    compile_hot_path_context,
    evaluate_common_design_pattern,
    evaluate_owner_visual_gate,
    evaluate_quality_authority,
    evaluate_structural_design_risks,
    evaluate_visual_direction_attempt,
    resolve_project_taste,
    route_visual_first,
    validate_concept_feasibility,
    validate_project_taste_isolation,
    validate_source_provenance,
    validate_specialist_activation,
    validate_typography_dependency_boundary,
)


ROOT = Path(__file__).resolve().parents[1]


def _contract(tier: str = "PREMIUM", project_id: str = "alpha-starts-now") -> dict:
    return {
        "project_id": project_id,
        "ambition_tier": tier,
        "project_category": "premium local contractor" if project_id != "alpha-starts-now" else "wellness brand",
        "design_lane": "editorial",
        "desired_emotional_character": "specific and composed",
        "approved_references": [],
        "rejected_references": [],
        "approved_reference_traits": ["clear hierarchy"],
        "rejected_reference_traits": ["generic template"],
        "anti_taste": ["unmotivated chrome"],
        "typography_lane": "source-neutral editorial sans",
        "typography_personality": "restrained",
        "material_language": "SUBTLE_TACTILE",
        "visual_world_strategy": "real subject-world imagery",
        "motion_appetite": "BRIEF_DEPENDENT",
        "visual_density": "airy",
        "design_variance": 6,
        "composition_preferences": ["editorial_multicolumn"],
        "signature_requirement": True,
        "owner_selected_visual_direction": None,
        "owner_visual_direction_confirmed": False,
    }


def _concept(concept_id: str, choice: str = "A", *, impossible: bool = False) -> dict:
    return {
        "concept_id": concept_id,
        "format": "HTML_CSS_PROTOTYPE",
        "semantic_regions": ["hero", "proof", "conversion"],
        "layout_tracks": ["12-column grid"],
        "media_layers": ["subject-world image"],
        "typography_planes": ["display", "body"],
        "interaction_layers": ["none"],
        "responsive_interpretation": "stacked mobile reading order",
        "pairwise_precheck": choice,
        "impossible_layout": impossible,
    }


def _load_outcome_replay():
    path = ROOT / "browser-qa" / "outcome_replay.py"
    spec = importlib.util.spec_from_file_location("website_director_outcome_replay", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class VisualFirstArchitectureTests(unittest.TestCase):
    def test_cross_client_taste_isolation(self) -> None:
        self.assertEqual(validate_project_taste_isolation("alpha-starts-now", _contract())["status"], "PASS")
        foreign = _contract(project_id="law-firm")
        self.assertEqual(validate_project_taste_isolation("alpha-starts-now", foreign)["status"], "FAIL")

    def test_premium_requires_visual_direction_gate(self) -> None:
        result = route_visual_first("WEBSITE", _contract())
        self.assertTrue(result["visual_direction_studio_required"])
        self.assertTrue(result["owner_visual_gate_required"])
        gate = evaluate_owner_visual_gate(_contract(), [_concept("direction-01"), _concept("direction-02")])
        self.assertEqual(gate["status"], "BLOCKED")
        self.assertFalse(gate["production_build_allowed"])

    def test_standard_does_not_require_image_generation(self) -> None:
        result = route_visual_first("WEBSITE", _contract("STANDARD"))
        self.assertEqual(result["image_generation_required"], False)
        self.assertEqual(result["image_generation_optional"], True)

    def test_technical_task_bypasses_taste_flow(self) -> None:
        result = route_visual_first("BUG_FIX")
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["taste_required"])
        self.assertTrue(result["production_build_allowed"])

    def test_owner_must_select_visual_direction(self) -> None:
        concepts = [_concept("direction-01"), _concept("direction-02")]
        blocked = evaluate_owner_visual_gate(_contract(), concepts, approved_visual_target={"id": "direction-01"})
        self.assertEqual(blocked["status"], "BLOCKED")
        passed = evaluate_owner_visual_gate(
            _contract(), concepts, selected_direction="direction-01", owner_confirmed=True,
            selection_actor="OWNER", approved_visual_target={"id": "direction-01"},
        )
        self.assertEqual(passed["status"], "PASS")

    def test_mediocre_concepts_do_not_reach_owner(self) -> None:
        concepts = [_concept("direction-01", "B"), _concept("direction-02", "B")]
        first = evaluate_visual_direction_attempt(_contract(), concepts, attempt=1)
        self.assertEqual(first["status"], "REGENERATE_ONCE")
        second = evaluate_visual_direction_attempt(_contract(), concepts, attempt=2)
        self.assertEqual(second["status"], "FAIL")
        self.assertEqual(second["owner_gate"], "NOT_REACHED")

    def test_concept_feasibility_blocks_impossible_layout(self) -> None:
        result = validate_concept_feasibility(_concept("impossible", impossible=True))
        self.assertEqual(result["status"], "FAIL")

    def test_numeric_telemetry_cannot_override_pairwise_fail(self) -> None:
        result = evaluate_quality_authority({"verdict": "B"}, numeric_score=99)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["authority"], "PAIRWISE")
        inconsistent = evaluate_quality_authority({"status": "FAIL", "verdict": "A"}, numeric_score=99)
        self.assertEqual(inconsistent["status"], "FAIL")

    def test_owner_rejection_cannot_be_overridden_by_machine_score(self) -> None:
        result = evaluate_quality_authority({"verdict": "A"}, numeric_score=100, owner_decision="REJECT")
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["authority"], "OWNER")

    def test_category_anchors_do_not_default_to_awwwards(self) -> None:
        result = choose_anchor_policy(_contract(project_id="contractor"))
        self.assertEqual(result["approved_anchor"], "CATEGORY_CALIBRATED_QUALITY")
        self.assertFalse(result["awwwards_universal"])
        self.assertFalse(result["awwwards_allowed"])

    def test_mengto_is_canonical_and_imba6_duplicate_is_skipped(self) -> None:
        records = [
            {"source_repository": "https://github.com/MengTo/Skills.git", "source_commit": "321c769", "source_path": "agent-skills/ui/design-first-ui-prompting/SKILL.md", "license": "MIT", "import_mode": "ADAPTED", "local_capability": "direction before code"},
            {"source_repository": "https://github.com/Imba6/AgentSkills.git", "source_commit": "NOT_USED", "source_path": "fork of MengTo", "license": "NOT_IMPORTED", "import_mode": "REJECTED", "local_capability": "duplicate skipped"},
        ]
        self.assertEqual(validate_source_provenance(records)["status"], "PASS")

    def test_event4u_typography_has_no_dangling_external_dependency(self) -> None:
        result = validate_typography_dependency_boundary({"methodology_source": "event4u", "runtime_dependencies": []})
        self.assertEqual(result["status"], "PASS")

    def test_gsap_webgl_threejs_remain_on_demand(self) -> None:
        self.assertEqual(validate_specialist_activation("GSAP", {})["status"], "BLOCKED")
        self.assertEqual(validate_specialist_activation("WEBGL", {"on_demand": True, "justification": "signature canvas is central"})["status"], "PASS")

    def test_visual_target_required_before_premium_build(self) -> None:
        result = evaluate_owner_visual_gate(
            _contract(), [_concept("direction-01"), _concept("direction-02")],
            selected_direction="direction-01", owner_confirmed=True, selection_actor="OWNER",
        )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertFalse(result["production_build_allowed"])

    def test_cold_path_content_is_not_loaded_into_unrelated_hot_phase(self) -> None:
        result = compile_hot_path_context(
            {"historical_seo_analysis": "old", "old_benchmark_reports": ["old"], "current_project_state": {"id": "demo"}},
            current_phase="IMPLEMENTATION", taste_contract=_contract(),
        )
        self.assertNotIn("historical_seo_analysis", result["context"])
        self.assertNotIn("old_benchmark_reports", result["context"])
        self.assertIsNone(result["metrics"]["token_count"])

    def test_project_taste_overrides_external_skill_default(self) -> None:
        result = resolve_project_taste(_contract(), {"material_language": "CHROMATIC_DEPTH", "typography_lane": "Inter default"})
        self.assertEqual(result["resolved"]["material_language"], "SUBTLE_TACTILE")
        self.assertEqual(result["resolved"]["typography_lane"], "source-neutral editorial sans")

    def test_common_design_pattern_is_not_automatically_slop(self) -> None:
        result = evaluate_common_design_pattern("cards", motivated=True)
        self.assertEqual(result["status"], "PASS")

    def test_declared_signature_without_rendered_proof_does_not_pass(self) -> None:
        result = evaluate_structural_design_risks({"signature_rendered_proof": False}, _contract())
        self.assertNotEqual(result["status"], "PASS")
        self.assertTrue(any(item["flag"] == "SIGNATURE_ONLY_DECLARED" for item in result["risks"]))

    def test_pairwise_receipt_requires_three_observable_reasons_and_respects_b(self) -> None:
        replay = _load_outcome_replay()
        receipt = {
            "numeric_score": 98,
            "dimensions": [
                {"dimension": "FIRST_IMPRESSION", "anchors": {"A": "approved.png", "B": "slop.png", "C": "candidate.png"}, "choice": "B", "discrepancies": ["spacing", "hierarchy", "image weight"]},
                {"dimension": "TYPOGRAPHY", "anchors": {"A": "approved.png", "B": "slop.png", "C": "candidate.png"}, "choice": "A", "discrepancies": ["scale", "leading", "contrast"]},
                {"dimension": "COMPOSITION", "anchors": {"A": "approved.png", "B": "slop.png", "C": "candidate.png"}, "choice": "A", "discrepancies": ["rail", "gutter", "rhythm"]},
                {"dimension": "VISUAL_WORLD_IMAGERY", "anchors": {"A": "approved.png", "B": "slop.png", "C": "candidate.png"}, "choice": "A", "discrepancies": ["crop", "subject", "tone"]},
                {"dimension": "CRAFT", "anchors": {"A": "approved.png", "B": "slop.png", "C": "candidate.png"}, "choice": "A", "discrepancies": ["finish", "alignment", "states"]},
                {"dimension": "MEMORABILITY", "anchors": {"A": "approved.png", "B": "slop.png", "C": "candidate.png"}, "choice": "A", "discrepancies": ["signature", "specificity", "recall"]},
            ],
        }
        result = replay.evaluate_pairwise_visual_gate(receipt)
        self.assertEqual(result["status"], replay.FAIL)
        self.assertEqual(result["verdict"], "CLOSER_TO_REJECTED")
        bad = dict(receipt)
        bad["dimensions"] = [dict(item) for item in receipt["dimensions"]]
        bad["dimensions"][0]["discrepancies"] = ["only two", "reasons"]
        self.assertEqual(replay.evaluate_pairwise_visual_gate(bad)["status"], replay.BLOCKED)


if __name__ == "__main__":
    unittest.main()
