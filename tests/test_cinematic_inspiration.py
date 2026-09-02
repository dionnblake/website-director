"""V2.15 cinematic intelligence, inspiration, and rendered-evidence controls.

The suite is deterministic and standard-library-only. It uses synthetic
reference records and screenshot receipts, and it never calls a provider,
launches a browser, or mutates ``projects/``.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "browser-qa"))

from framework_validation.cinematic_inspiration import (  # noqa: E402
    MODEL_ROLES,
    REQUIRED_RENDER_SURFACES,
    validate_inspiration_registry,
    validate_model_agnostic_routing,
    validate_owner_selected_reference,
    validate_provider_neutral_documents,
    validate_rendered_visual_evidence,
)
from guards.frozen_integrity_guard import FrozenIntegrityGuard  # noqa: E402


REGISTRY_PATH = ROOT / "templates" / "inspiration-source-registry.json"


def load_registry() -> dict[str, object]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def issue_codes(result: object) -> set[str]:
    if isinstance(result, dict):
        result = result.get("issues", [])
    return {str(item["code"]) for item in result if isinstance(item, dict)}


def owner_reference() -> dict[str, object]:
    return {
        "OWNER_SELECTED_REFERENCE": True,
        "SOURCE": "21ST_DEV",
        "URL": "https://21st.dev/example/hero",
        "REFERENCE_TYPE": "component",
        "ELEMENT_OR_SECTION": "hero interaction",
        "WHAT_I_LIKE": "The image expansion gives the hero a clear reveal.",
        "WHAT_I_DO_NOT_WANT": "Do not copy its colors, copy, or typography.",
        "ASSIGNED_DIMENSION": "Motion",
        "PATTERN_TO_LEARN": "Use a restrained image expansion to reveal hierarchy.",
        "OWNER_REQUESTED_ELEMENT": "hero image expansion",
        "WHAT_NOT_TO_COPY": "Source composition, colors, copy, and typography.",
        "REFERENCE_GRADE": "B",
        "LICENSE_STATUS": "NOT_REQUIRED_STUDY_ONLY",
        "IMPLEMENTATION_RISK": "MEDIUM",
        "ACCESSIBILITY_RISK": "MEDIUM",
        "PRODUCTION_PLAUSIBILITY": "HIGH",
        "REFERENCE_ONLY_STATUS": True,
        "WHY_IS_THIS_RELEVANT": "It supports the client's desired sense of material reveal and hierarchy.",
        "WHAT_SPECIFICALLY_WORKS": "The reveal gives the subject a clear first focal event.",
        "TRANSFERABLE_PRINCIPLE": "Reveal a meaningful subject before secondary detail.",
        "BRAND_ADAPTATION": "Use the locked project palette, type, and subject-specific imagery.",
        "IMPLEMENTATION_MODE": "STUDY_ONLY",
    }


def screenshot_set() -> list[dict[str, object]]:
    return [
        {
            "surface_id": surface_id,
            "route": "/",
            "viewport": 390 if surface_id.startswith("MOBILE_") else 1440,
            "browser": "chromium",
            "render_capture": "FULL_PAGE" if surface_id.endswith("FULL_PAGE") else "VIEWPORT",
            "actual_rendered": True,
            "engine_identity": "REAL_BROWSER",
            "screenshot_path": "rendered/%s.png" % surface_id.lower(),
            "screenshot_sha256": "a" * 64,
            "attempt": 1,
        }
        for surface_id in REQUIRED_RENDER_SURFACES
    ]


def valid_gauntlet_evidence() -> dict[str, object]:
    return {
        "required_surfaces": list(REQUIRED_RENDER_SURFACES),
        "screenshot_set": screenshot_set(),
        "screenshot_set_revision": 0,
        "current_build_sha": "build-1",
        "repairs": [],
        "critic": {
            "fresh_context": True,
            "fresh_context_id": "critic-1",
            "builder_context_id": "builder-1",
            "actual_screenshots": True,
            "actual_rendered_dom": True,
            "actual_css": True,
            "approved_design_direction": True,
            "approved_design_system": True,
            "owner_intent": True,
            "assigned_reference_bars": True,
            "actual_dom_ref": "rendered/home.html",
            "actual_css_ref": "rendered/home.css",
        },
    }


class CinematicInspirationTests(unittest.TestCase):
    def test_21ST_DEV_REGISTRY_PRESENT(self) -> None:
        registry = load_registry()
        source = next(item for item in registry["sources"] if item["source_id"] == "21ST_DEV")
        self.assertEqual(source["url"], "https://21st.dev/")
        self.assertEqual(source["role"], "COMPONENT_PATTERN_LIBRARY")

    def test_GODLY_REGISTRY_PRESENT(self) -> None:
        registry = load_registry()
        source = next(item for item in registry["sources"] if item["source_id"] == "GODLY")
        self.assertEqual(source["url"], "https://godly.design/")
        self.assertEqual(source["role"], "CURATED_SITE_AND_SECTION_DISCOVERY")

    def test_AWWWARDS_EXISTING_AUTHORITY_NOT_DUPLICATED(self) -> None:
        registry = load_registry()
        source = next(item for item in registry["sources"] if item["source_id"] == "AWWWARDS")
        self.assertEqual(source["authority_ref"], "AWWWARDS-SHOWCASE-INTELLIGENCE.md")
        self.assertFalse(source["duplicate_authority"])
        self.assertNotIn("AWWWARDS", issue_codes(validate_inspiration_registry(registry)))

    def test_MOTIONSITES_REGISTRY_PRESENT(self) -> None:
        registry = load_registry()
        source = next(item for item in registry["sources"] if item["source_id"] == "MOTIONSITES")
        self.assertEqual(source["url"], "https://motionsites.ai/")
        self.assertEqual(source["role"], "MOTION_PATTERN_AND_BACKGROUND_LIBRARY")

    def test_OWNER_REFERENCE_SELECTION_SUPPORTED(self) -> None:
        self.assertFalse(issue_codes(
            validate_owner_selected_reference(owner_reference(), load_registry())))

    def test_REFERENCE_ONLY_BOUNDARY_ENFORCED(self) -> None:
        reference = owner_reference()
        reference["REFERENCE_ONLY_STATUS"] = False
        self.assertIn(
            "REFERENCE_ONLY_BOUNDARY_ENFORCED",
            issue_codes(validate_owner_selected_reference(reference, load_registry())),
        )

    def test_LICENSE_CHECK_REQUIRED_FOR_SOURCE_REUSE(self) -> None:
        reference = owner_reference()
        reference["IMPLEMENTATION_MODE"] = "SOURCE_REUSE"
        reference["REFERENCE_ONLY_STATUS"] = False
        codes = issue_codes(validate_owner_selected_reference(reference, load_registry()))
        self.assertIn("LICENSE_CHECK_REQUIRED_FOR_SOURCE_REUSE", codes)

    def test_MODEL_AGNOSTIC_ROUTING(self) -> None:
        routing = " ".join(MODEL_ROLES)
        self.assertFalse(issue_codes(validate_model_agnostic_routing(routing)))

    def test_NO_CLAUDE_DEPENDENCY(self) -> None:
        self.assertFalse(issue_codes(validate_provider_neutral_documents(self._production_docs())))

    def test_NO_HIGGSFIELD_DEPENDENCY(self) -> None:
        self.assertFalse(issue_codes(validate_provider_neutral_documents(self._production_docs())))

    def test_NO_HOSTINGER_DEPENDENCY(self) -> None:
        self.assertFalse(issue_codes(validate_provider_neutral_documents(self._production_docs())))

    def test_NO_LOVABLE_DEPENDENCY(self) -> None:
        self.assertFalse(issue_codes(validate_provider_neutral_documents(self._production_docs())))

    def test_SOURCE_ONLY_VISUAL_PASS_REJECTED(self) -> None:
        evidence = {
            "status": "PASS",
            "source": "SOURCE_INSPECTION",
            "required_surfaces": list(REQUIRED_RENDER_SURFACES),
            "screenshot_set": [],
        }
        self.assertIn(
            "SOURCE_ONLY_VISUAL_PASS_REJECTED",
            issue_codes(validate_rendered_visual_evidence(evidence)),
        )

    def test_MISSING_SCREENSHOT_SET_REJECTED(self) -> None:
        evidence = {
            "status": "PASS",
            "required_surfaces": list(REQUIRED_RENDER_SURFACES),
            "screenshot_set": screenshot_set()[:1],
        }
        self.assertIn(
            "MISSING_SCREENSHOT_SET_REJECTED",
            issue_codes(validate_rendered_visual_evidence(evidence)),
        )

    def test_STALE_SCREENSHOT_AFTER_REPAIR_REJECTED(self) -> None:
        evidence = valid_gauntlet_evidence()
        evidence["repairs"] = [{"revision": 1, "summary": "tighten hero spacing"}]
        evidence["screenshot_set_revision"] = 2
        evidence["pre_repair_build_sha"] = "build-1"
        evidence["current_build_sha"] = "build-1"
        self.assertIn(
            "STALE_SCREENSHOT_AFTER_REPAIR_REJECTED",
            issue_codes(validate_rendered_visual_evidence(evidence, require_critic=True)),
        )

    def test_FRESH_CRITIC_REQUIRED(self) -> None:
        evidence = valid_gauntlet_evidence()
        evidence.pop("critic")
        self.assertIn(
            "FRESH_CRITIC_REQUIRED",
            issue_codes(validate_rendered_visual_evidence(evidence, require_critic=True)),
        )

    def test_RECAPTURE_AFTER_REPAIR_REQUIRED(self) -> None:
        evidence = valid_gauntlet_evidence()
        evidence["repairs"] = [{"revision": 1, "summary": "repair"}]
        evidence["screenshot_set_revision"] = 1
        evidence["recapture_after_repair"] = False
        self.assertIn(
            "RECAPTURE_AFTER_REPAIR_REQUIRED",
            issue_codes(validate_rendered_visual_evidence(evidence, require_critic=True)),
        )

    def test_complete_fresh_render_review_passes(self) -> None:
        result = validate_rendered_visual_evidence(
            valid_gauntlet_evidence(), require_critic=True)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["captured_surfaces"], sorted(REQUIRED_RENDER_SURFACES))

    def test_OWNER_LOCK_COUNT_REMAINS_5(self) -> None:
        profile = json.loads((ROOT / "templates" / "site-profile.json").read_text(encoding="utf-8"))
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
        self.assertEqual(len(profile["locks"]), 5)

    def test_FROZEN_MUTATIONS_0(self) -> None:
        guard = FrozenIntegrityGuard(ROOT, ["projects/"], run_id="v2_15_cinematic_evidence")
        guard.snapshot()
        result = guard.verify()
        self.assertTrue(result.ok, result.summary())

    @staticmethod
    def _production_docs() -> list[Path]:
        return [
            ROOT / "CINEMATIC-INTEGRATION-PROTOCOL.md",
            ROOT / "INSPIRATION-SOURCES.md",
            ROOT / "templates" / "inspiration-source-registry.json",
            ROOT / "templates" / "cinematic-brief.md",
        ]


if __name__ == "__main__":
    unittest.main()
