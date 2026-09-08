"""Tests for Website Director Clean-Room Creative Mode (Phase 10 & 11 regression fixtures).

Validates:
1. Structural input quarantine (projects/** and review-workspaces/** blocked).
2. Owner asset allowlisting (individual allowed vs bulk-copy blocked).
3. External reference provenance enforcement.
4. Historical baseline ordering (pre-render blocked, post-render allowed).
5. Cheap concept gate (hero + signature device only, 3 concepts required).
6. Morphology divergence evaluation (renaming components fails; true divergence passes).
7. Zero ASN generation invariant.
"""

from __future__ import annotations

import unittest
from pathlib import Path
from typing import Any, Dict, List

from framework_validation.clean_room import (
    CleanRoomManifest,
    CleanRoomExecutionAdapters,
    CleanRoomExecutionRequest,
    EXECUTION_STAGE_SEQUENCE,
    HistoricalQuarantineGuard,
    execute_clean_room_workflow,
    evaluate_morphology_divergence,
    enforce_cheap_concept_gate,
    prepare_blind_critic_package,
    run_synthetic_clean_room,
    validate_pre_generation_scope,
    verify_reference_provenance,
)


class CleanRoomCreativeModeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.allowlist = [
            {"asset_id": "ASN_LOGO", "source_path": "projects/alpha-starts-now/logo.svg", "authorized": True}
        ]
        self.guard = HistoricalQuarantineGuard(mode="CLEAN_ROOM", allowlist=self.allowlist)

    def test_unauthorized_historical_path_blocked(self) -> None:
        result = self.guard.check_input_path("projects/alpha-starts-now-flagship-proof/assets/hero-dawn-man.jpg")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["violation"], "CLEAN_ROOM_INPUT_VIOLATION")

    def test_absolute_historical_path_blocked(self) -> None:
        result = self.guard.check_input_path(r"C:\workspace\projects\previous-generated-direction\index.html")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["violation"], "CLEAN_ROOM_INPUT_VIOLATION")

    def test_bulk_historical_asset_reuse_blocked(self) -> None:
        result = self.guard.check_asset_reuse(asset_id=None, source_path="projects/alpha-starts-now-visual-convergence", is_bulk=True)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["violation"], "HISTORICAL_ASSET_BULK_REUSE")

    def test_authorized_owner_asset_passes(self) -> None:
        result = self.guard.check_asset_reuse(asset_id="ASN_LOGO", source_path="projects/alpha-starts-now/logo.svg")
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["authorized"])

    def test_approved_external_reference_passes(self) -> None:
        references = [
            {"reference_id": "EXT_01", "classification": "EXTERNAL_GOLD_STANDARD", "url": "https://example.com/ref1"},
            {"reference_id": "EXT_02", "classification": "OWNER_SUPPLIED_EXTERNAL_REFERENCE", "url": "https://example.com/ref2"},
        ]
        result = verify_reference_provenance(references)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["valid_references_count"], 2)

    def test_missing_or_historical_external_reference_blocked(self) -> None:
        # Test missing reference package
        result_empty = verify_reference_provenance([])
        self.assertEqual(result_empty["status"], "BLOCKED")
        self.assertEqual(result_empty["violation"], "EXTERNAL_REFERENCE_PACKAGE_MISSING")

        # Test forbidden historical reference classification
        forbidden = [
            {"reference_id": "PREV_01", "classification": "PREVIOUS_WEBSITE_DIRECTOR_OUTPUT", "url": "projects/alpha-starts-now"}
        ]
        result_forbidden = verify_reference_provenance(forbidden)
        self.assertEqual(result_forbidden["status"], "BLOCKED")
        self.assertEqual(result_forbidden["violation"], "HISTORICAL_POSITIVE_REFERENCE_FORBIDDEN")

    def test_historical_baseline_ordering_enforcement(self) -> None:
        # Pre-render request to historical path -> BLOCKED
        pre_render = self.guard.check_input_path("projects/alpha-starts-now-flagship-proof", is_post_render_negative_baseline=False)
        self.assertEqual(pre_render["status"], "BLOCKED")

        # Post-render request for negative baseline comparison -> PASS
        post_render = self.guard.check_input_path("projects/alpha-starts-now-flagship-proof", is_post_render_negative_baseline=True)
        self.assertEqual(post_render["status"], "PASS")
        self.assertEqual(post_render["role"], "NEGATIVE_BASELINE_ONLY")

    def test_cheap_concept_gate_enforcement(self) -> None:
        # Valid cheap concept package (3 concepts, hero + signature device only)
        valid_package = {
            "concepts": [
                {"name": "Concept A", "built_surfaces": ["desktop_hero", "signature_device"]},
                {"name": "Concept B", "built_surfaces": ["desktop_hero", "signature_device"]},
                {"name": "Concept C", "built_surfaces": ["desktop_hero", "signature_device"]},
            ]
        }
        res_valid = enforce_cheap_concept_gate(valid_package)
        self.assertEqual(res_valid["status"], "PASS")
        self.assertEqual(res_valid["scope"], "HERO_PLUS_SIGNATURE_DEVICE_ONLY")

        # Invalid cheap concept package (full homepage surfaces built prematurely)
        invalid_package = {
            "concepts": [
                {"name": "Concept A", "built_surfaces": ["desktop_hero", "full_homepage", "footer"]},
                {"name": "Concept B", "built_surfaces": ["desktop_hero"]},
                {"name": "Concept C", "built_surfaces": ["desktop_hero"]},
            ]
        }
        res_invalid = enforce_cheap_concept_gate(invalid_package)
        self.assertEqual(res_invalid["status"], "FAIL")

    def test_morphology_divergence_fixture_a_semantic_renaming_fails(self) -> None:
        """Fixture A: Candidate renames component classes ('card' -> 'cinematic chapter') but keeps same geometry -> FAIL."""
        historical_baseline = {
            "HERO_SILHOUETTE": "CENTERED_SPLIT_HERO",
            "SECTION_GEOMETRY": "ALTERNATING_TWO_COLUMN_GRID",
            "TWO_COLUMN_REPETITION": True,
            "CARD_CONTAINER_DENSITY": "HIGH_BORDERED_BOXES",
            "MEDIA_DOMINANCE": "COMPACT_MEDIA_PANEL",
            "TYPOGRAPHIC_SILHOUETTE": "NAVY_GOLD_SERIF",
            "WHITESPACE_DENSITY": "COMPACT",
            "PAGE_RHYTHM": "REGULAR_CARD_CADENCE",
            "SIGNATURE_DEVICE": "CIRCADIAN_GAUGE",
            "CTA_MORPHOLOGY": "CENTERED_CONTAINED_BUTTON",
            "semantic_rename_only": True, # Renamed "card" to "cinematic chapter"
        }

        candidate = {
            "HERO_SILHOUETTE": "CENTERED_SPLIT_HERO",
            "SECTION_GEOMETRY": "ALTERNATING_TWO_COLUMN_GRID",
            "TWO_COLUMN_REPETITION": True,
            "CARD_CONTAINER_DENSITY": "HIGH_BORDERED_BOXES",
            "MEDIA_DOMINANCE": "COMPACT_MEDIA_PANEL",
            "TYPOGRAPHIC_SILHOUETTE": "NAVY_GOLD_SERIF",
            "WHITESPACE_DENSITY": "COMPACT",
            "PAGE_RHYTHM": "REGULAR_CARD_CADENCE",
            "SIGNATURE_DEVICE": "CIRCADIAN_GAUGE",
            "CTA_MORPHOLOGY": "CENTERED_CONTAINED_BUTTON",
            "semantic_rename_only": True,
        }

        res = evaluate_morphology_divergence(candidate, historical_baseline)
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["divergence"], "MORPHOLOGY_DIVERGENCE_FAIL")
        self.assertTrue(res["semantic_rename_detected"])

    def test_morphology_divergence_fixture_b_genuine_divergence_passes(self) -> None:
        """Fixture B: Candidate uses genuinely different hero silhouette, section topology, and spatial rhythm -> PASS."""
        historical_baseline = {
            "HERO_SILHOUETTE": "CENTERED_SPLIT_HERO",
            "SECTION_GEOMETRY": "ALTERNATING_TWO_COLUMN_GRID",
            "TWO_COLUMN_REPETITION": True,
            "CARD_CONTAINER_DENSITY": "HIGH_BORDERED_BOXES",
            "MEDIA_DOMINANCE": "COMPACT_MEDIA_PANEL",
            "TYPOGRAPHIC_SILHOUETTE": "NAVY_GOLD_SERIF",
            "WHITESPACE_DENSITY": "COMPACT",
            "PAGE_RHYTHM": "REGULAR_CARD_CADENCE",
            "SIGNATURE_DEVICE": "CIRCADIAN_GAUGE",
            "CTA_MORPHOLOGY": "CENTERED_CONTAINED_BUTTON",
            "semantic_rename_only": False,
        }

        candidate = {
            "HERO_SILHOUETTE": "FULL_BLEED_ASYMMETRIC_EDITORIAL",
            "SECTION_GEOMETRY": "SINGLE_COLUMN_NARRATIVE_STREAM",
            "TWO_COLUMN_REPETITION": False,
            "CARD_CONTAINER_DENSITY": "ZERO_BORDER_OPEN_TYPOGRAPHY",
            "MEDIA_DOMINANCE": "FULL_VIEWPORT_CANVAS",
            "TYPOGRAPHIC_SILHOUETTE": "MONOCHROME_INDUSTRIAL_MONO",
            "WHITESPACE_DENSITY": "EXPANSIVE_80VH",
            "PAGE_RHYTHM": "ASYMMETRIC_BREAKS",
            "SIGNATURE_DEVICE": "INTERACTIVE_CHRONOMETRIC_SCRUBBER",
            "CTA_MORPHOLOGY": "PINNED_ACCESSIBLE_BAR",
            "semantic_rename_only": False,
        }

        res = evaluate_morphology_divergence(candidate, historical_baseline)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["divergence"], "MORPHOLOGY_DIVERGENCE_PASS")
        self.assertFalse(res["semantic_rename_detected"])

    def test_blind_critic_package_contains_no_implementation_source(self) -> None:
        pkg = prepare_blind_critic_package(
            candidate_screenshot="evidence/candidate.png",
            external_references=["evidence/ref1.png"],
            business_brief="Business Brief Content",
            brand_brief="Brand Brief Content"
        )
        self.assertIsNone(pkg["html_source"])
        self.assertIsNone(pkg["css_source"])
        self.assertIsNone(pkg["class_names"])
        self.assertIsNone(pkg["direction_name"])
        self.assertIsNone(pkg["builder_commentary"])
        self.assertIsNone(pkg["self_awarded_scores"])
        self.assertIsNone(pkg["previous_asn_screenshots"])

    def test_execution_wires_required_stages_and_stops_for_owner_selection(self) -> None:
        events: List[str] = []
        vectors = (
            "HERO_SILHOUETTE",
            "SECTION_GEOMETRY",
            "TWO_COLUMN_REPETITION",
            "CARD_CONTAINER_DENSITY",
            "MEDIA_DOMINANCE",
            "TYPOGRAPHIC_SILHOUETTE",
            "WHITESPACE_DENSITY",
            "PAGE_RHYTHM",
            "SIGNATURE_DEVICE",
            "CTA_MORPHOLOGY",
        )
        candidate_morphology = {vector: f"CANDIDATE_{vector}" for vector in vectors}
        baseline_morphology = {vector: f"BASELINE_{vector}" for vector in vectors}
        manifest = CleanRoomManifest(
            business_understanding_ref="synthetic/project-brief.md",
            owner_intent_ref="synthetic/creative-intent-contract.md",
            conversion_requirements_ref="synthetic/measurement-plan.md",
            content_truth_ref="synthetic/content-plan.md",
            external_references=[
                {
                    "reference_id": "EXT_01",
                    "classification": "EXTERNAL_GOLD_STANDARD",
                    "url": "https://example.test/reference",
                }
            ],
        )

        def generate(_manifest: CleanRoomManifest) -> Dict[str, Any]:
            events.append("generate_concepts")
            return {
                "concepts": [
                    {"concept_id": "A", "built_surfaces": ["desktop_hero", "signature_device"]},
                    {"concept_id": "B", "built_surfaces": ["desktop_hero", "signature_device"]},
                    {"concept_id": "C", "built_surfaces": ["desktop_hero", "signature_device"]},
                ]
            }

        def render(_package: Dict[str, Any]) -> Dict[str, Any]:
            events.append("render_candidate")
            return {
                "candidate_screenshot": "synthetic://candidate.png",
                "morphology": candidate_morphology,
            }

        def load_baseline(path: str) -> Dict[str, Any]:
            self.assertEqual(events, ["generate_concepts", "render_candidate"])
            self.assertEqual(path, "projects/historical-negative-baseline")
            events.append("load_negative_baseline")
            return {"morphology": baseline_morphology}

        def critic(package: Dict[str, Any]) -> Dict[str, Any]:
            events.append("run_blind_critic")
            self.assertIsNone(package["html_source"])
            self.assertIsNone(package["previous_asn_screenshots"])
            return {"status": "PASS", "review_id": "synthetic-review"}

        request = CleanRoomExecutionRequest(
            manifest=manifest,
            adapters=CleanRoomExecutionAdapters(generate, render, load_baseline, critic),
            negative_baseline_path="projects/historical-negative-baseline",
            business_brief="Synthetic business brief.",
            brand_brief="Synthetic brand brief.",
            positive_input_paths=("synthetic/project-brief.md",),
            external_reference_screenshots=("synthetic://external-reference.png",),
            run_id="test-clean-room-execution",
        )

        result = execute_clean_room_workflow(request)

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["workflow_status"], "OWNER_CONCEPT_SELECTION_PENDING")
        self.assertEqual(result["owner_concept_selection"], "PENDING")
        self.assertEqual(result["stage_sequence"], list(EXECUTION_STAGE_SEQUENCE))
        self.assertEqual(
            events,
            ["generate_concepts", "render_candidate", "load_negative_baseline", "run_blind_critic"],
        )
        self.assertTrue(result["controls"]["negative_baseline_read_after_render"])
        self.assertFalse(result["controls"]["negative_baseline_read_before_render"])
        self.assertFalse(result["controls"]["asn_generation_attempted"])
        self.assertEqual(result["controls"]["project_files_written"], 0)

    def test_execution_blocks_historical_positive_input_before_any_adapter_runs(self) -> None:
        events: List[str] = []

        def unexpected(*_args: Any) -> Dict[str, Any]:
            events.append("unexpected")
            raise AssertionError("adapter must not run after a positive historical-input block")

        request = CleanRoomExecutionRequest(
            manifest=CleanRoomManifest(
                external_references=[
                    {
                        "reference_id": "EXT_01",
                        "classification": "EXTERNAL_GOLD_STANDARD",
                        "url": "https://example.test/reference",
                    }
                ]
            ),
            adapters=CleanRoomExecutionAdapters(unexpected, unexpected, unexpected, unexpected),
            negative_baseline_path="projects/historical-negative-baseline",
            business_brief="Synthetic business brief.",
            brand_brief="Synthetic brand brief.",
            positive_input_paths=("projects/previous-generated-direction/index.html",),
        )

        result = execute_clean_room_workflow(request)

        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["workflow_status"], "INPUT_PREFLIGHT_BLOCKED")
        self.assertEqual(result["failure"], "CLEAN_ROOM_INPUT_VIOLATION")
        self.assertEqual(events, [])

    def test_pre_generation_scope_blocks_forbidden_surface_before_builder(self) -> None:
        events: List[str] = []

        def unexpected(*_args: Any) -> Dict[str, Any]:
            events.append("builder")
            raise AssertionError("builder must not run for a forbidden pre-generation surface")

        scope = {
            "allowed_surfaces": ["DESKTOP_HERO", "SIGNATURE_DEVICE", "FULL_HOMEPAGE"],
            "concepts": [
                {"concept_id": "A", "allowed_surfaces": ["DESKTOP_HERO", "SIGNATURE_DEVICE"]},
                {"concept_id": "B", "allowed_surfaces": ["DESKTOP_HERO", "SIGNATURE_DEVICE"]},
                {"concept_id": "C", "allowed_surfaces": ["DESKTOP_HERO", "SIGNATURE_DEVICE"]},
            ],
        }
        self.assertEqual(validate_pre_generation_scope(scope)["status"], "FAIL")
        request = CleanRoomExecutionRequest(
            manifest=CleanRoomManifest(
                business_understanding_ref="synthetic/brief.json",
                owner_intent_ref="synthetic/intent.json",
                external_references=[
                    {
                        "reference_id": "EXT_01",
                        "classification": "EXTERNAL_GOLD_STANDARD",
                        "url": "https://example.test/reference",
                    }
                ],
            ),
            adapters=CleanRoomExecutionAdapters(unexpected, unexpected, unexpected, unexpected),
            negative_baseline_path="projects/historical-negative-baseline",
            business_brief="Synthetic business brief.",
            brand_brief="Synthetic brand brief.",
            concept_scope=scope,
        )

        result = execute_clean_room_workflow(request)

        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["workflow_status"], "PRE_GENERATION_SCOPE_FAILED")
        self.assertEqual(events, [])
        self.assertFalse(result["pre_generation_scope"].get("builder_task_emitted", False))

    def test_synthetic_end_to_end_entrypoint_is_not_a_validator_only(self) -> None:
        result = run_synthetic_clean_room("test-synthetic-end-to-end")

        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["synthetic"])
        self.assertEqual(
            result["adapter_events"],
            ["generate_concepts", "render_candidate", "load_negative_baseline", "run_blind_critic"],
        )
        self.assertEqual(result["workflow_status"], "FULL_HOMEPAGE_AUTHORIZED")
        self.assertEqual(result["controls"]["staged_input_file_count"], 7)
        self.assertEqual(result["controls"]["staged_historical_output_files"], 0)
        self.assertEqual(result["controls"]["generator_package_historical_sentinels"], 0)
        self.assertEqual(result["controls"]["blind_critic_sentinel_leaks"], 0)
        self.assertEqual(result["controls"]["negative_baseline_access_before_render"], "BLOCKED")
        self.assertTrue(result["controls"]["negative_baseline_read_after_render"])
        self.assertEqual(result["pre_generation_scope"]["status"], "PASS")
        self.assertEqual(result["post_generation_scope_verification"]["status"], "PASS")
        self.assertEqual(result["owner_selection"]["before_full_homepage_design"], "BLOCKED")
        self.assertEqual(result["owner_selection"]["after_full_homepage_design"], "AUTHORIZED")
        self.assertEqual(result["owner_selection"]["new_owner_lock_created"], False)
        self.assertEqual(result["render_derived_morphology"]["status"], "PASS_DIVERGENCE")
        self.assertEqual(
            result["rendered_fixture_comparisons"]["SEMANTIC_RENAME_RENDER_FIXTURE"]["status"],
            "FAIL_DIVERGENCE",
        )
        self.assertEqual(
            result["rendered_fixture_comparisons"]["GENUINE_DIVERGENCE_RENDER_FIXTURE"]["status"],
            "PASS_DIVERGENCE",
        )

        stage_root = Path(result["stage_root"])
        for directory in (
            "manifest",
            "business",
            "brand",
            "approved-assets",
            "external-references",
            "candidate-output",
            "evidence",
        ):
            self.assertTrue((stage_root / directory).is_dir(), directory)
        for historical_path in (
            "historical-project/old-site.html",
            "historical-project/old-style.css",
            "historical-project/old-hero.jpg",
            "historical-project/rejected-screenshot.png",
        ):
            self.assertFalse((stage_root / historical_path).exists(), historical_path)

        package_text = (stage_root / "manifest" / "concept-generation-package.json").read_text(encoding="utf-8")
        inventory_text = (stage_root / "evidence" / "staged-input-inventory.json").read_text(encoding="utf-8")
        audit_by_path = {
            item["source_path"]: item["status"] for item in result["requested_input_audit"]
        }
        self.assertEqual(audit_by_path["historical-project/old-site.html"], "BLOCKED")
        self.assertEqual(audit_by_path["historical-project/old-style.css"], "BLOCKED")
        self.assertEqual(audit_by_path["historical-project/old-hero.jpg"], "BLOCKED")
        self.assertEqual(audit_by_path["historical-project/rejected-screenshot.png"], "BLOCKED")
        self.assertEqual(audit_by_path["brand/allowed-logo.svg"], "PASS")
        self.assertEqual(audit_by_path["external-references/reference-01.png"], "PASS")
        self.assertEqual(audit_by_path["external-references/reference-02.png"], "PASS")
        for sentinel in ("NEVER_SHOW_THIS_TO_GENERATOR", "old-two-column-card", "old-hero.jpg"):
            self.assertNotIn(sentinel, package_text)
            self.assertNotIn(sentinel, inventory_text)
        self.assertNotIn("SECRET_BUILDER_SCORE", str(result["blind_critic_package"]))
        self.assertNotIn("cinematic-masterpiece", str(result["blind_critic_package"]))
        self.assertFalse(result["controls"]["asn_generation_attempted"])


if __name__ == "__main__":
    unittest.main()
