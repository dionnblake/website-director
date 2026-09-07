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
from typing import Any, Dict, List

from framework_validation.clean_room import (
    CleanRoomManifest,
    HistoricalQuarantineGuard,
    evaluate_morphology_divergence,
    enforce_cheap_concept_gate,
    prepare_blind_critic_package,
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


if __name__ == "__main__":
    unittest.main()
