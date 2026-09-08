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

import copy
import tempfile
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
from framework_validation.rendered_morphology import (
    CHEAP_CONCEPT_NOT_APPLICABLE_VECTOR_IDS,
    CHEAP_CONCEPT_VECTOR_IDS,
    MORPHOLOGY_VECTOR_IDS,
    compare_rendered_morphology,
    extract_rendered_morphology,
)
from framework_validation.morphology_recheck import update_owner_review_report


def _generic_morphology_evidence(
    *,
    surface_count: int = 2,
    container_count: int = 2,
    media_area_ratio: float = 0.10,
    font_family: str = "Georgia, serif",
    occupied_area_ratio: float = 0.62,
    hero_width: float = 1100,
    hero_height: float = 560,
    hero_axis: str = "HORIZONTAL",
    signature_width: float = 420,
    signature_height: float = 220,
    signature_orientation: str = "HORIZONTAL",
    cta_x: float = 80,
    cta_y: float = 430,
) -> Dict[str, Any]:
    """Build complete, business-neutral cheap-concept browser evidence."""

    viewport_width, viewport_height = 1440.0, 900.0
    document_height = 1500.0
    document_area = viewport_width * document_height
    computed_layout = {
        "display": "grid" if hero_axis == "HORIZONTAL" else "block",
        "position": "static",
        "grid_template_columns": "1fr 1fr" if hero_axis == "HORIZONTAL" else "none",
        "grid_template_rows": "none",
        "flex_direction": "row",
        "gap": "24px",
        "justify_content": "normal",
        "align_items": "normal",
    }
    hero_children = (
        [
            {"x": 80, "y": 100, "width": 420, "height": 300, "computed": dict(computed_layout)},
            {"x": 680, "y": 100, "width": 320, "height": 320, "computed": dict(computed_layout)},
        ]
        if hero_axis == "HORIZONTAL"
        else [
            {"x": 80, "y": 80, "width": 760, "height": 160, "computed": dict(computed_layout)},
            {"x": 80, "y": 300, "width": 760, "height": 160, "computed": dict(computed_layout)},
        ]
    )
    sections = [
        {
            "index": index,
            "x": 0,
            "y": index * (document_height / max(1, surface_count)),
            "width": viewport_width,
            "height": document_height / max(1, surface_count),
            "display": "grid" if hero_axis == "HORIZONTAL" else "block",
            "major_child_count": 2,
            "column_count": 2 if hero_axis == "HORIZONTAL" else 1,
            "column_alignment": "RIGHT" if index % 2 == 0 else "LEFT",
            "gap_before": 0,
            "position": "static",
            "grid_template_columns": computed_layout["grid_template_columns"],
            "grid_template_rows": "none",
            "flex_direction": "row",
            "gap": "24px",
            "justify_content": "normal",
            "align_items": "normal",
            "child_regions": [
                {
                    "x": 80,
                    "y": index * (document_height / max(1, surface_count)) + 80,
                    "width": 640,
                    "height": 240,
                    "computed": dict(computed_layout),
                }
            ],
        }
        for index in range(surface_count)
    ]
    media_area = document_area * media_area_ratio
    media_elements = [] if media_area == 0 else [
        {"x": 0, "y": 0, "width": 1000, "height": media_area / 1000, "media_kind": "FIGURE"}
    ]
    return {
        "evidence_kind": "BROWSER_LAYOUT",
        "measurement_schema_version": "2.0",
        "measurement_schema": [
            "viewport", "document", "hero", "hero.major_children", "sections",
            "sections.child_regions", "sections.computed_layout", "media_elements",
            "bordered_containers", "heading.computed_style", "whitespace.internal_occupancy",
            "signature_device.target_region", "cta.geometry_and_alignment",
        ],
        "evaluation_stage": "HERO_PLUS_SIGNATURE_DEVICE_ONLY",
        "viewport": {"width": viewport_width, "height": viewport_height, "area": viewport_width * viewport_height},
        "document": {"width": viewport_width, "height": document_height, "area": document_area},
        "hero": {
            "x": 0,
            "y": 0,
            "width": hero_width,
            "height": hero_height,
            "major_children": hero_children,
            "media_area": media_area * 0.45,
            **computed_layout,
        },
        "sections": sections,
        "bordered_containers": [
            {
                "x": 40 + index * 10,
                "y": 80,
                "width": 260,
                "height": 120,
                "border_widths": {"top": "1px", "right": "1px", "bottom": "1px", "left": "1px"},
            }
            for index in range(container_count)
        ],
        "media_elements": media_elements,
        "heading": {
            "target_found": True,
            "rect": {"x": 80, "y": 100, "width": 620, "height": 120},
            "font_family": font_family,
            "font_size": 60,
            "line_height": 66,
            "letter_spacing": 0,
            "line_count": 2,
        },
        "whitespace": {
            "occupied_area_ratio": occupied_area_ratio,
            "negative_space_ratio": 1 - occupied_area_ratio,
            "hero_occupied_area_ratio": occupied_area_ratio * 0.9,
            "major_region_gap_ratio": 0.12 if hero_axis == "HORIZONTAL" else 0.30,
        },
        "signature_device": {
            "target_found": True,
            "x": 120,
            "y": 700,
            "width": signature_width,
            "height": signature_height,
            "occupied_area_ratio": 0.70,
            "dominant_child_aspect_ratio": signature_width / signature_height,
            "dominant_child": {
                "x": 140,
                "y": 720,
                "width": signature_width * 0.8,
                "height": signature_height * 0.8,
                "computed": dict(computed_layout),
            },
            "structural_orientation": signature_orientation,
            "media_area": media_area * 0.2,
        },
        "cta": {
            "target_found": True,
            "source": "HERO_ACTION",
            "within_hero": True,
            "x": cta_x,
            "y": cta_y,
            "width": 180,
            "height": 52,
            "x_hero_ratio": cta_x / hero_width,
            "y_hero_ratio": cta_y / hero_height,
            "alignment": "LEFT" if cta_x < hero_width * 0.2 else "CENTER",
            "treatment": "EDGE_ALIGNED" if cta_x < hero_width * 0.1 else "CENTERED",
        },
        "scan_complete": {
            "viewport": True,
            "document": True,
            "hero": True,
            "sections": True,
            "media": True,
            "bordered_containers": True,
            "heading": True,
            "signature_device": True,
            "cta": True,
        },
    }


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

    def test_legacy_declared_morphology_missing_values_fail_closed(self) -> None:
        baseline = {vector: f"BASELINE_{vector}" for vector in MORPHOLOGY_VECTOR_IDS}
        candidate = {vector: f"CANDIDATE_{vector}" for vector in MORPHOLOGY_VECTOR_IDS}
        candidate.pop("MEDIA_DOMINANCE")

        result = evaluate_morphology_divergence(candidate, baseline)

        self.assertEqual(result["status"], "BLOCKED_INSUFFICIENT_EVIDENCE")
        self.assertEqual(result["vector_results"]["MEDIA_DOMINANCE"], "INSUFFICIENT_EVIDENCE")
        self.assertNotIn("MATCHES_HISTORICAL_BASELINE", result["vector_results"].values())

        for empty_value in ("", [], {}):
            with self.subTest(empty_value=empty_value):
                incomplete_candidate = dict(candidate)
                incomplete_candidate["MEDIA_DOMINANCE"] = empty_value
                incomplete_baseline = dict(baseline)
                incomplete_baseline["MEDIA_DOMINANCE"] = empty_value
                empty_result = evaluate_morphology_divergence(incomplete_candidate, incomplete_baseline)
                self.assertEqual(empty_result["status"], "BLOCKED_INSUFFICIENT_EVIDENCE")
                self.assertEqual(empty_result["vector_results"]["MEDIA_DOMINANCE"], "INSUFFICIENT_EVIDENCE")

    def test_rendered_morphology_cheap_stage_uses_seven_of_ten_vectors(self) -> None:
        result = compare_rendered_morphology(
            _generic_morphology_evidence(),
            _generic_morphology_evidence(),
            "HERO_PLUS_SIGNATURE_DEVICE_ONLY",
        )
        self.assertEqual(result["applicable_vectors"], list(CHEAP_CONCEPT_VECTOR_IDS))
        self.assertEqual(result["not_applicable_vectors"], list(CHEAP_CONCEPT_NOT_APPLICABLE_VECTOR_IDS))
        self.assertEqual(result["applicable_vector_count"], 7)
        self.assertEqual(result["not_applicable_vector_count"], 3)
        for vector in CHEAP_CONCEPT_NOT_APPLICABLE_VECTOR_IDS:
            self.assertEqual(result["vector_results"][vector]["VECTOR_VERDICT"], "NOT_APPLICABLE")

    def test_rendered_morphology_rejects_mismatched_embedded_stage(self) -> None:
        candidate = _generic_morphology_evidence()
        baseline = _generic_morphology_evidence()
        candidate["evaluation_stage"] = "FULL_HOMEPAGE"
        candidate["cta"]["within_hero"] = False

        result = compare_rendered_morphology(
            candidate,
            baseline,
            "HERO_PLUS_SIGNATURE_DEVICE_ONLY",
        )

        self.assertEqual(result["status"], "BLOCKED_INSUFFICIENT_EVIDENCE")
        self.assertIn("evaluation_stage:mismatch", result["candidate"]["missing_evidence_fields"])
        self.assertIn("cta.within_hero", result["candidate"]["missing_evidence_fields"])

    def test_full_homepage_repeated_grammar_vectors_fail_closed_on_missing_evidence(self) -> None:
        baseline = _generic_morphology_evidence(surface_count=4)
        baseline["evaluation_stage"] = "FULL_HOMEPAGE"
        mutations = {
            "SECTION_GEOMETRY": lambda item: item["sections"][0].pop("width"),
            "TWO_COLUMN_REPETITION": lambda item: item["sections"][0].pop("column_count"),
            "PAGE_RHYTHM": lambda item: item["sections"][1].pop("gap_before"),
        }
        complete = compare_rendered_morphology(baseline, baseline, "FULL_HOMEPAGE")
        self.assertEqual(complete["status"], "FAIL_DIVERGENCE")
        for vector, mutate in mutations.items():
            with self.subTest(vector=vector):
                candidate = copy.deepcopy(baseline)
                mutate(candidate)
                result = compare_rendered_morphology(candidate, baseline, "FULL_HOMEPAGE")
                self.assertEqual(result["status"], "BLOCKED_INSUFFICIENT_EVIDENCE")
                self.assertEqual(result["vector_results"][vector]["VECTOR_VERDICT"], "INSUFFICIENT_EVIDENCE")

    def test_rendered_morphology_missing_evidence_never_becomes_a_match(self) -> None:
        mutators = {
            "HERO_SILHOUETTE": lambda item: item["hero"].update({"major_children": []}),
            "CARD_CONTAINER_DENSITY": lambda item: item["scan_complete"].update({"bordered_containers": False}),
            "MEDIA_DOMINANCE": lambda item: item["scan_complete"].update({"media": False}),
            "TYPOGRAPHIC_SILHOUETTE": lambda item: item["heading"].update({"font_family": None}),
            "WHITESPACE_DENSITY": lambda item: item.update({"whitespace": {}}),
            "SIGNATURE_DEVICE": lambda item: item["signature_device"].update({"target_found": False}),
            "CTA_MORPHOLOGY": lambda item: item["cta"].update({"target_found": False}),
        }
        baseline = _generic_morphology_evidence()
        for vector, mutate in mutators.items():
            with self.subTest(vector=vector):
                candidate = copy.deepcopy(baseline)
                mutate(candidate)
                result = compare_rendered_morphology(candidate, baseline)
                self.assertEqual(result["status"], "BLOCKED_INSUFFICIENT_EVIDENCE")
                self.assertIn(vector, result["insufficient_evidence_vectors"])
                self.assertEqual(result["vector_results"][vector]["VECTOR_VERDICT"], "INSUFFICIENT_EVIDENCE")
                self.assertNotEqual(result["vector_results"][vector]["VECTOR_VERDICT"], "MATCHES_HISTORICAL_BASELINE")

        incomplete_scan = copy.deepcopy(baseline)
        incomplete_scan["scan_complete"]["heading"] = False
        incomplete_result = compare_rendered_morphology(incomplete_scan, baseline)
        self.assertEqual(incomplete_result["status"], "BLOCKED_INSUFFICIENT_EVIDENCE")
        self.assertIn("TYPOGRAPHIC_SILHOUETTE", incomplete_result["insufficient_evidence_vectors"])

    def test_partial_geometry_records_fail_closed_for_every_applicable_family(self) -> None:
        mutators = {
            "HERO_SILHOUETTE": lambda item: item["hero"]["major_children"][0].pop("width"),
            "CARD_CONTAINER_DENSITY": lambda item: item["bordered_containers"][0].pop("width"),
            "MEDIA_DOMINANCE": lambda item: item["media_elements"][0].pop("width"),
            "TYPOGRAPHIC_SILHOUETTE": lambda item: item["heading"]["rect"].pop("width"),
            "WHITESPACE_DENSITY": lambda item: item["whitespace"].pop("hero_occupied_area_ratio"),
            "SIGNATURE_DEVICE": lambda item: item["signature_device"]["dominant_child"].pop("width"),
            "CTA_MORPHOLOGY": lambda item: item["cta"].pop("width"),
        }
        baseline = _generic_morphology_evidence()
        for vector, mutate in mutators.items():
            with self.subTest(vector=vector):
                candidate = copy.deepcopy(baseline)
                mutate(candidate)
                result = compare_rendered_morphology(candidate, baseline)
                self.assertEqual(result["status"], "BLOCKED_INSUFFICIENT_EVIDENCE")
                self.assertEqual(result["vector_results"][vector]["VECTOR_VERDICT"], "INSUFFICIENT_EVIDENCE")

    def test_incomplete_persisted_schema_blocks_before_scoring(self) -> None:
        baseline = _generic_morphology_evidence()
        mutations = {
            "document.width": lambda item: item["document"].pop("width"),
            "sections[0].display": lambda item: item["sections"][0].pop("display"),
            "sections[0].child_regions": lambda item: item["sections"][0].pop("child_regions"),
        }
        for missing_path, mutate in mutations.items():
            with self.subTest(missing_path=missing_path):
                candidate = copy.deepcopy(baseline)
                mutate(candidate)
                result = compare_rendered_morphology(candidate, baseline)
                self.assertEqual(result["status"], "BLOCKED_INSUFFICIENT_EVIDENCE")
                self.assertFalse(result["evidence_schema_complete"])
                self.assertIn(missing_path, result["candidate"]["missing_evidence_fields"])

    def test_typography_uses_computed_font_family_and_arial_is_sans(self) -> None:
        evidence = _generic_morphology_evidence(font_family="Arial, Helvetica, sans-serif")
        extracted = extract_rendered_morphology(evidence)
        self.assertEqual(extracted["status"], "PASS")
        self.assertEqual(extracted["raw_measurements"]["TYPOGRAPHIC_SILHOUETTE"]["family_class"], "SANS")
        self.assertNotIn("SERIF", extracted["vectors"]["TYPOGRAPHIC_SILHOUETTE"])

    def test_normalized_measurements_drive_card_media_whitespace_and_signature(self) -> None:
        baseline = _generic_morphology_evidence(
            surface_count=4,
            container_count=4,
            media_area_ratio=0.118,
            occupied_area_ratio=0.75,
            signature_width=240,
            signature_height=240,
            signature_orientation="CENTRAL",
        )
        candidate = _generic_morphology_evidence(
            surface_count=2,
            container_count=4,
            media_area_ratio=0.012,
            occupied_area_ratio=0.25,
            signature_width=760,
            signature_height=120,
            signature_orientation="HORIZONTAL",
        )
        candidate["round_shape_count"] = 99
        baseline["round_shape_count"] = 0
        result = compare_rendered_morphology(candidate, baseline)
        for vector in (
            "CARD_CONTAINER_DENSITY",
            "MEDIA_DOMINANCE",
            "WHITESPACE_DENSITY",
            "SIGNATURE_DEVICE",
        ):
            self.assertEqual(result["vector_results"][vector]["VECTOR_VERDICT"], "DIVERGENT", vector)
            self.assertIsNotNone(result["vector_results"][vector]["NORMALIZED_DISTANCE_OR_SIMILARITY"])
        self.assertNotIn("round_shape_count", result["vector_results"]["SIGNATURE_DEVICE"]["RAW_CANDIDATE_MEASUREMENTS"])

    def test_generic_calibration_clone_divergence_missing_color_and_shared_cta(self) -> None:
        baseline = _generic_morphology_evidence()
        clone = copy.deepcopy(baseline)
        color_only = copy.deepcopy(baseline)
        color_only["unscored_visual_tokens"] = {"primary": "purple", "accent": "lime"}
        genuine = _generic_morphology_evidence(
            surface_count=2,
            container_count=7,
            media_area_ratio=0.38,
            font_family="Arial, Helvetica, sans-serif",
            occupied_area_ratio=0.20,
            hero_width=1440,
            hero_height=820,
            hero_axis="VERTICAL",
            signature_width=120,
            signature_height=680,
            signature_orientation="VERTICAL",
            cta_x=620,
            cta_y=160,
        )
        same_cta_otherwise_different = copy.deepcopy(genuine)
        same_cta_otherwise_different["cta"] = copy.deepcopy(baseline["cta"])
        missing = copy.deepcopy(genuine)
        missing["signature_device"] = {"target_found": False}

        self.assertEqual(compare_rendered_morphology(clone, baseline)["status"], "FAIL_DIVERGENCE")
        self.assertEqual(compare_rendered_morphology(color_only, baseline)["status"], "FAIL_DIVERGENCE")
        self.assertEqual(compare_rendered_morphology(genuine, baseline)["status"], "PASS_DIVERGENCE")
        missing_result = compare_rendered_morphology(missing, baseline)
        self.assertEqual(missing_result["status"], "BLOCKED_INSUFFICIENT_EVIDENCE")
        shared_cta_result = compare_rendered_morphology(same_cta_otherwise_different, baseline)
        self.assertEqual(shared_cta_result["vector_results"]["CTA_MORPHOLOGY"]["VECTOR_VERDICT"], "MATCHES_HISTORICAL_BASELINE")
        self.assertEqual(shared_cta_result["status"], "PASS_DIVERGENCE")
        self.assertGreaterEqual(shared_cta_result["divergence_ratio"], 0.60)

    def test_generic_candidates_share_one_complete_evidence_schema(self) -> None:
        concepts = [
            _generic_morphology_evidence(media_area_ratio=ratio)
            for ratio in (0.02, 0.08, 0.20)
        ]
        baseline = _generic_morphology_evidence()
        for concept in concepts:
            self.assertEqual(set(concept), set(baseline))
            self.assertEqual(concept["measurement_schema"], baseline["measurement_schema"])
            self.assertEqual(set(concept["viewport"]), set(baseline["viewport"]))
            self.assertEqual(set(concept["document"]), set(baseline["document"]))
            self.assertEqual(set(concept["heading"]), set(baseline["heading"]))
            self.assertEqual(set(concept["signature_device"]), set(baseline["signature_device"]))
            self.assertEqual(set(concept["cta"]), set(baseline["cta"]))
            self.assertEqual(set(concept["sections"][0]), set(baseline["sections"][0]))
            self.assertEqual(
                set(concept["sections"][0]["child_regions"][0]),
                set(baseline["sections"][0]["child_regions"][0]),
            )
            self.assertTrue(compare_rendered_morphology(concept, baseline)["evidence_schema_complete"])

    def test_owner_review_recheck_updates_reporting_rows_only(self) -> None:
        original = (
            '<section class="concept"><h2>CONCEPT A</h2><dl>'
            '<dt>MORPHOLOGY DIVERGENCE =</dt><dd>FAIL_DIVERGENCE; 4/10 vectors divergent</dd>'
            '<dt>BIGGEST VISIBLE WEAKNESS =</dt><dd>Keep this exact weakness.</dd>'
            '</dl></section>'
        )
        result = {
            "CONCEPT_A": {
                "status": "PASS_DIVERGENCE",
                "divergence_ratio": 6 / 7,
                "divergent_vectors": ["HERO_SILHOUETTE"],
                "matching_vectors": ["CTA_MORPHOLOGY"],
                "not_applicable_vectors": ["PAGE_RHYTHM"],
            }
        }
        with tempfile.TemporaryDirectory() as temporary:
            report = Path(temporary) / "owner-review.html"
            report.write_text(original, encoding="utf-8")
            update_owner_review_report(report, result)
            update_owner_review_report(report, result)
            updated = report.read_text(encoding="utf-8")
        self.assertIn("MORPHOLOGY VERDICT =", updated)
        self.assertIn("0.857", updated)
        self.assertIn("Keep this exact weakness.", updated)
        self.assertNotIn("4/10", updated)

    def test_owner_review_recheck_keeps_distinct_concept_results_in_their_sections(self) -> None:
        section = (
            '<section class="concept"><h2>{name}</h2><dl>'
            '<dt>MORPHOLOGY DIVERGENCE =</dt><dd>old</dd>'
            '<dt>BIGGEST VISIBLE WEAKNESS =</dt><dd>{name} weakness.</dd>'
            '</dl></section>'
        )
        original = "".join(section.format(name=f"CONCEPT {letter}") for letter in "ABC")
        results = {
            "CONCEPT_A": {
                "status": "PASS_DIVERGENCE", "divergence_ratio": 1.0,
                "divergent_vectors": ["HERO_SILHOUETTE"], "matching_vectors": [],
                "not_applicable_vectors": ["PAGE_RHYTHM"],
            },
            "CONCEPT_B": {
                "status": "PASS_DIVERGENCE", "divergence_ratio": 6 / 7,
                "divergent_vectors": ["MEDIA_DOMINANCE"], "matching_vectors": ["CTA_MORPHOLOGY"],
                "not_applicable_vectors": ["PAGE_RHYTHM"],
            },
            "CONCEPT_C": {
                "status": "FAIL_DIVERGENCE", "divergence_ratio": 2 / 7,
                "divergent_vectors": ["SIGNATURE_DEVICE"], "matching_vectors": ["WHITESPACE_DENSITY"],
                "not_applicable_vectors": ["PAGE_RHYTHM"],
            },
        }
        with tempfile.TemporaryDirectory() as temporary:
            report = Path(temporary) / "owner-review.html"
            report.write_text(original, encoding="utf-8")
            update_owner_review_report(report, results)
            updated = report.read_text(encoding="utf-8")
        sections = updated.split('<section class="concept">')[1:]
        self.assertIn("1.000", sections[0])
        self.assertIn("NONE", sections[0])
        self.assertIn("0.857", sections[1])
        self.assertIn("CTA_MORPHOLOGY", sections[1])
        self.assertIn("0.286", sections[2])
        self.assertIn("WHITESPACE_DENSITY", sections[2])
        self.assertIn("CONCEPT C weakness.", sections[2])

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
        rendered_evidence = result["candidate_render"]["rendered_morphology_evidence"]
        self.assertEqual(len(rendered_evidence["sections"]), 2)
        self.assertEqual(rendered_evidence["signature_device"]["source"], "EXPLICIT_SURFACE")
        self.assertTrue(rendered_evidence["cta"]["within_hero"])
        self.assertIn(rendered_evidence["cta"]["source"], {"EXPLICIT_CTA", "HERO_ACTION"})
        self.assertLessEqual(rendered_evidence["cta"]["y_hero_ratio"], 1.0)
        self.assertEqual(len(rendered_evidence["media_elements"]), 1)
        self.assertAlmostEqual(
            rendered_evidence["hero"]["media_area"],
            rendered_evidence["media_elements"][0]["area"],
            places=5,
        )
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
