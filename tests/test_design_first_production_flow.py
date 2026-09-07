"""Deterministic tests for the bounded design-first production flow."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "browser-qa"))

from framework_validation.design_first_flow import (  # noqa: E402
    BUSINESS_UNDERSTANDING_FIELDS,
    CANONICAL_LOCKS,
    DESIGN_SIGNALS,
    DESIGN_SYSTEM_DERIVATION_FIELDS,
    DISCOVERY_MODES,
    FIGMA_IN_DESIGN_FIRST_FLOW,
    FULL_HOMEPAGE_SECTIONS,
    HOMEPAGE_REVIEW_SURFACES,
    OPERATING_FLOW,
    extract_client_voice,
    validate_ambition_policy,
    validate_asset_intent,
    validate_business_understanding,
    validate_client_voice_fidelity,
    validate_component_routing,
    validate_design_system_derivation,
    validate_discovery_mode,
    validate_downstream_authorities,
    validate_homepage_approval,
    validate_homepage_design,
    validate_inspiration_records,
    validate_operating_flow,
    validate_owner_lock_contract,
    validate_production_gate,
)
from framework_validation.cinematic_inspiration import (  # noqa: E402
    resolve_screenshot_receipt,
    validate_rendered_visual_evidence,
)
from guards.frozen_integrity_guard import FrozenIntegrityGuard  # noqa: E402
import runner as bqa_runner  # noqa: E402


def issue_codes(result: object) -> set[str]:
    if isinstance(result, dict):
        result = result.get("issues", [])
    return {str(item["code"]) for item in result if isinstance(item, dict)}



def write_homepage_receipts(root: Path) -> list[dict[str, object]]:
    """Write real PNG bytes and return receipts that identify them.

    Synthetic and disposable: these prove the evidence reader opens files and
    recomputes digests.  They are never written into a project or an approval
    record.
    """
    rendered = root / "rendered"
    rendered.mkdir(parents=True, exist_ok=True)
    receipts: list[dict[str, object]] = []
    for index, surface in enumerate(HOMEPAGE_REVIEW_SURFACES):
        width, height = (1440, 9781) if "DESKTOP" in surface else (390, 14311)
        payload = _png_bytes(width, height, index)
        path = rendered / (surface.lower() + ".png")
        path.write_bytes(payload)
        receipts.append({
            "surface_id": surface,
            "actual_rendered": True,
            "engine_identity": "REAL_BROWSER",
            "render_capture": "FULL_PAGE",
            "screenshot_path": "rendered/" + path.name,
            "screenshot_sha256": hashlib.sha256(payload).hexdigest(),
            "capture_verification": {"verdict": "VERIFIED", "image_width": width,
                                     "image_height": height, "document_height": height,
                                     "issues": []},
        })
    return receipts


def _png_bytes(width: int, height: int, salt: int) -> bytes:
    """A minimal, structurally valid PNG header plus disposable padding."""
    import struct
    import zlib

    def chunk(kind: bytes, payload: bytes) -> bytes:
        return (struct.pack(">I", len(payload)) + kind + payload
                + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))

    header = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)
    return (bytes([137, 80, 78, 71, 13, 10, 26, 10])
            + chunk(b"IHDR", header)
            + chunk(b"tEXt", b"disposable-test-fixture-%d" % salt)
            + chunk(b"IEND", b""))


def business_pack() -> dict[str, object]:
    return {
        "BUSINESS": "Northline Workshop helps independent manufacturers improve their quoting process.",
        "TARGET_CUSTOMER": "Owner-led manufacturers with a small sales team.",
        "PRIMARY_CUSTOMER_PROBLEM": "Quotes take too long and important context gets lost between sales and production.",
        "SERVICES": ["Quoting workflow review", "Sales enablement workshop"],
        "NOT_OFFERED": ["We do not provide legal or accounting advice."],
        "DIFFERENTIATOR": "The work connects shop-floor reality to a practical quoting system.",
        "OWNER_ORIGIN_STORY": "UNKNOWN",
        "CLIENT_VOICE": "Plain, direct, practical, and calm.",
        "BRAND_PERSONALITY": ["precise", "human", "confident"],
        "PRIMARY_CONVERSION": "Schedule a quoting review.",
        "SECONDARY_CONVERSIONS": ["Download the workflow checklist."],
        "PRIMARY_OBJECTIONS": ["Will this fit our existing process?", "How much disruption will this cause?"],
        "TRUST_REQUIREMENTS": ["Show the method clearly", "Do not overclaim outcomes"],
        "PROOF_AVAILABLE": "NOT_PROVIDED",
        "DESIGN_PREFERENCES": ["Editorial structure", "Visible material detail"],
        "ANTI_PREFERENCES": ["No generic dashboard imagery", "No fake proof"],
        "OWNER_SELECTED_REFERENCE_URLS": ["https://example.com/reference"],
        "OWNER_REFERENCE_DESCRIPTIONS": ["Study the calm information hierarchy, not the visual treatment."],
        "OWNER_ASSETS": "NOT_PROVIDED",
        "REQUIRED_ASSETS": ["Owner-provided workshop photography if available"],
        "REFERENCE_ONLY_ASSETS": ["Research screenshots remain reference-only."],
        "BRAND_GUIDELINES": "NOT_PROVIDED",
        "OWNER_NON_NEGOTIABLES": ["Keep the language plain", "Do not imply proof that was not supplied"],
        "UNKNOWN_OR_UNVERIFIED_FACTS": ["Founding year is UNKNOWN", "Case-study metrics are UNVERIFIED"],
    }


def homepage_design() -> dict[str, object]:
    return {
        "FULL_HOMEPAGE_VISUAL_DESIGN": True,
        "ARTIFACT_KIND": "FULL_HOMEPAGE",
        "SECTIONS": {section: f"Specific {section.lower()} treatment grounded in the business." for section in FULL_HOMEPAGE_SECTIONS},
        "RENDERED_SURFACES": list(HOMEPAGE_REVIEW_SURFACES),
        "LOWER_HALF_QUALITY": "SPECIFIC_AND_AUTHENTIC",
        "CLIENT_VOICE_FIDELITY": "PASS",
        "CLIENT_VOICE_FIDELITY_EVIDENCE": "Uses the owner's words 'practical' and 'calm' from the discovery notes.",
        **{field: f"Approved {field.lower()} direction" for field in DESIGN_SIGNALS},
    }


def homepage_approval() -> dict[str, object]:
    return {
        "STATE_LOCATION": "visual_prototypes.homepage_visual_approved",
        "HOMEPAGE_VISUAL_APPROVED": True,
        "OWNER_APPROVED": True,
        "OWNER_ACTION": "APPROVE",
        "APPROVED_BY": "OWNER",
        "RENDERED_SURFACES": list(HOMEPAGE_REVIEW_SURFACES),
        "REVIEWED": True,
        "PROSE_ONLY": False,
        "CRITIC_RECOMMENDATION": "Keep the lower-half proof treatment specific.",
    }


def design_system() -> dict[str, object]:
    return {
        "HOMEPAGE_SOURCE": "APPROVED_HOMEPAGE",
        "SOURCE_APPROVAL_REF": "visual_prototypes.homepage_visual_approved:owner-review-001",
        **{field: f"Derived {field.lower()} rules" for field in DESIGN_SYSTEM_DERIVATION_FIELDS},
        "REINTERPRETS_AESTHETIC": False,
        "CONTRADICTS_HOMEPAGE": False,
    }


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


class DesignFirstProductionFlowTests(unittest.TestCase):
    def test_operating_flow_and_invariants_are_bounded(self) -> None:
        result = validate_operating_flow(list(OPERATING_FLOW))
        self.assertTrue(result["ok"])
        self.assertEqual(result["flow"], list(OPERATING_FLOW))
        self.assertEqual(
            result["invariants"],
            [
                "UNDERSTANDING_PRECEDES_DESIGN",
                "DESIGN_PRECEDES_IMPLEMENTATION",
                "OWNER_SEES_RENDERED_DESIGN_BEFORE_FULL_BUILD",
                "APPROVED_HOMEPAGE_DEFINES_THE_SITE_SYSTEM",
            ],
        )

    def test_invalid_operating_order_is_rejected(self) -> None:
        result = validate_operating_flow(["UNDERSTAND_BUSINESS", "IMPLEMENT_REST"])
        self.assertFalse(result["ok"])
        self.assertIn("DESIGN_FIRST_SEQUENCE_INVALID", issue_codes(result))

    def test_business_understanding_pack_requires_all_semantic_fields(self) -> None:
        result = validate_business_understanding(business_pack())
        self.assertTrue(result["ok"])
        self.assertEqual(result["required_fields"], list(BUSINESS_UNDERSTANDING_FIELDS))

    def test_unknown_facts_are_explicit_and_not_fabricated(self) -> None:
        artifact = business_pack()
        artifact["PROOF_AVAILABLE"] = "UNKNOWN"
        artifact["OWNER_ORIGIN_STORY"] = "UNVERIFIED"
        result = validate_business_understanding(artifact)
        self.assertTrue(result["ok"])
        self.assertIn("PROOF_AVAILABLE", result["unknown_fields"])
        self.assertIn("OWNER_ORIGIN_STORY", result["unknown_fields"])

    def test_fabricated_business_claim_is_rejected(self) -> None:
        artifact = business_pack()
        artifact["PROOF_AVAILABLE"] = "fake testimonial from a famous customer"
        result = validate_business_understanding(artifact)
        self.assertFalse(result["ok"])
        self.assertIn("FABRICATED_BUSINESS_FACT", issue_codes(result))

    def test_all_discovery_modes_are_explicit_and_transcript_is_optional(self) -> None:
        self.assertEqual(set(DISCOVERY_MODES), {
            "QUESTIONNAIRE_ONLY",
            "QUESTIONNAIRE_PLUS_TRANSCRIPT",
            "TRANSCRIPT_LED_DISCOVERY",
            "OWNER_SUPPLIED_DISCOVERY_NOTES",
        })
        self.assertTrue(validate_discovery_mode("QUESTIONNAIRE_ONLY")["ok"])
        self.assertTrue(validate_discovery_mode("OWNER_SUPPLIED_DISCOVERY_NOTES")["ok"])
        self.assertFalse(validate_discovery_mode("QUESTIONNAIRE_PLUS_TRANSCRIPT")["ok"])
        self.assertIn("TRANSCRIPT_REQUIRED_FOR_SELECTED_MODE", issue_codes(validate_discovery_mode("TRANSCRIPT_LED_DISCOVERY")))

    def test_client_voice_extraction_preserves_owner_language_without_transcript_requirement(self) -> None:
        absent = extract_client_voice({"mode": "QUESTIONNAIRE_ONLY"})
        self.assertEqual(absent["status"], "NOT_PROVIDED")
        extracted = extract_client_voice({
            "mode": "QUESTIONNAIRE_PLUS_TRANSCRIPT",
            "transcript": "We make complex planning feel calm. The work must stay practical and direct. We help owners shorten the quoting loop.",
        })
        self.assertTrue(extracted["ok"])
        voice = extracted["client_voice"]
        self.assertIn("We make complex planning feel calm.", voice["verbatim_or_near_verbatim"])
        self.assertIn("calm", voice["brand_register"])
        self.assertTrue(voice["service_explanations"])
        self.assertTrue(voice["owner_priorities"])

    def test_client_voice_fidelity_question_is_explicit(self) -> None:
        self.assertTrue(validate_client_voice_fidelity(homepage_design())["ok"])
        result = validate_client_voice_fidelity({"CLIENT_VOICE_FIDELITY": "FAIL", "CLIENT_VOICE_FIDELITY_EVIDENCE": "generic copy"})
        self.assertFalse(result["ok"])
        self.assertIn("CLIENT_VOICE_FIDELITY_FAIL", issue_codes(result))

    def test_ambition_policy_requires_full_homepage_for_premium_showcase_and_experimental(self) -> None:
        self.assertTrue(validate_ambition_policy("PREMIUM", homepage_design())["ok"])
        self.assertTrue(validate_ambition_policy("SHOWCASE", homepage_design())["ok"])
        self.assertIn("FULL_HOMEPAGE_VISUAL_DESIGN_REQUIRED", issue_codes(validate_ambition_policy("SHOWCASE", {"ARTIFACT_KIND": "HERO_ONLY"})))
        exception = {"ARTIFACT_KIND": "HERO_ONLY", "BOUNDED_ARTIFACT_EXCEPTION": True, "EXCEPTION_REASON": "Disposable internal concept only."}
        self.assertTrue(validate_ambition_policy("EXPERIMENTAL", exception)["ok"])
        self.assertTrue(validate_ambition_policy("STANDARD", {"ARTIFACT_KIND": "SELECTED_DIRECTION_PLUS_COMPLETE_HOMEPAGE"})["ok"])

    def test_complete_homepage_requires_real_surfaces_and_visual_language(self) -> None:
        result = validate_homepage_design("PREMIUM", homepage_design())
        self.assertTrue(result["ok"])
        broken = copy.deepcopy(homepage_design())
        broken["RENDERED_SURFACES"] = ["DESKTOP_FULL_HOMEPAGE"]
        result = validate_homepage_design("PREMIUM", broken)
        self.assertFalse(result["ok"])
        self.assertIn("FULL_HOMEPAGE_RENDER_REQUIRED", issue_codes(result))

    def test_generic_lower_half_is_rejected(self) -> None:
        broken = homepage_design()
        broken["LOWER_HALF_QUALITY"] = "GENERIC_FILLER"
        result = validate_homepage_design("PREMIUM", broken)
        self.assertFalse(result["ok"])
        self.assertIn("HOMEPAGE_LOWER_HALF_QUALITY", issue_codes(result))

    def test_prose_only_homepage_is_rejected(self) -> None:
        broken = homepage_design()
        broken["PROSE_ONLY"] = True
        result = validate_homepage_design("STANDARD", broken)
        self.assertFalse(result["ok"])
        self.assertIn("PROSE_ONLY_DIRECTION_REJECTED", issue_codes(result))

    def test_fabricated_homepage_copy_is_rejected(self) -> None:
        broken = homepage_design()
        broken["SECTIONS"]["PROOF_AND_TRUST"] = "Fake testimonial and guaranteed results."
        result = validate_homepage_design("PREMIUM", broken)
        self.assertFalse(result["ok"])
        self.assertIn("FABRICATED_OR_PLACEHOLDER_HOMEPAGE_COPY", issue_codes(result))

    def test_owner_approval_requires_rendered_desktop_and_mobile_homepage(self) -> None:
        result = validate_homepage_approval(homepage_approval())
        self.assertTrue(result["ok"])
        broken = homepage_approval()
        broken["RENDERED_SURFACES"] = ["DESKTOP_FULL_HOMEPAGE"]
        self.assertIn("FULL_HOMEPAGE_RENDER_REQUIRED", issue_codes(validate_homepage_approval(broken)))
        missing_action = homepage_approval()
        del missing_action["OWNER_ACTION"]
        self.assertIn("OWNER_APPROVAL_REQUIRED", issue_codes(validate_homepage_approval(missing_action)))
        missing_state = homepage_approval()
        del missing_state["STATE_LOCATION"]
        self.assertIn("HOMEPAGE_APPROVAL_MUST_USE_EXISTING_STATE", issue_codes(validate_homepage_approval(missing_state)))

    def test_critic_cannot_approve_and_prose_cannot_approve(self) -> None:
        critic = homepage_approval()
        critic["APPROVED_BY"] = "INTERNAL_CRITIC"
        result = validate_homepage_approval(critic)
        self.assertFalse(result["ok"])
        self.assertIn("OWNER_APPROVAL_CANNOT_BE_SET_BY_CRITIC", issue_codes(result))
        prose = homepage_approval()
        prose["PROSE_ONLY"] = True
        self.assertIn("PROSE_ONLY_DIRECTION_REJECTED", issue_codes(validate_homepage_approval(prose)))

    def test_production_gate_requires_business_to_design_evidence_chain(self) -> None:
        with tempfile.TemporaryDirectory(prefix="wd-gate-") as directory:
            receipts = write_homepage_receipts(Path(directory))
            evidence = {
                "BUSINESS_UNDERSTANDING_COMPLETE": True,
                "OWNER_INTENT_CAPTURED": True,
                "REQUIRED_ASSETS_IDENTIFIED": True,
                "REFERENCES_INTERPRETED": True,
                "HOMEPAGE_RENDERED_AND_REVIEWED": True,
                "OWNER_APPROVAL_RECORDED": True,
                "DESIGN_SYSTEM_DERIVED_AND_READY": True,
                "HOMEPAGE_APPROVAL": {**homepage_approval(), "RENDERED_SURFACES": receipts},
            }
            self.assertTrue(validate_production_gate(evidence, evidence_root=directory)["ok"])
            blocked = dict(evidence)
            blocked["BUSINESS_UNDERSTANDING_COMPLETE"] = False
            blocked["PRODUCTION_STARTED"] = True
            result = validate_production_gate(blocked, evidence_root=directory)
            self.assertFalse(result["ok"])
            self.assertIn("PRODUCTION_STARTED_BEFORE_HOMEPAGE_APPROVAL", issue_codes(result))

    def test_bare_surface_names_cannot_authorize_production_entry(self) -> None:
        """R4-C1: seven true flags plus named-but-unevidenced surfaces."""
        evidence = {field: True for field in (
            "BUSINESS_UNDERSTANDING_COMPLETE", "OWNER_INTENT_CAPTURED", "REQUIRED_ASSETS_IDENTIFIED",
            "REFERENCES_INTERPRETED", "HOMEPAGE_RENDERED_AND_REVIEWED", "OWNER_APPROVAL_RECORDED",
            "DESIGN_SYSTEM_DERIVED_AND_READY")}
        evidence["HOMEPAGE_APPROVAL"] = homepage_approval()
        result = validate_production_gate(evidence)
        self.assertFalse(result["ok"])
        self.assertFalse(result["can_start_production"])
        self.assertIn("PRODUCTION_ENTRY_EVIDENCE_NOT_BOUND", issue_codes(result))
        # The approval-shape validator keeps its documented behaviour.
        self.assertTrue(validate_homepage_approval(homepage_approval())["ok"])

    def test_underlying_design_failures_survive_true_flags(self) -> None:
        with tempfile.TemporaryDirectory(prefix="wd-gate-under-") as directory:
            receipts = write_homepage_receipts(Path(directory))
            broken_homepage = homepage_design()
            broken_homepage["SECTIONS"] = {}
            evidence = {field: True for field in (
                "BUSINESS_UNDERSTANDING_COMPLETE", "OWNER_INTENT_CAPTURED", "REQUIRED_ASSETS_IDENTIFIED",
                "REFERENCES_INTERPRETED", "HOMEPAGE_RENDERED_AND_REVIEWED", "OWNER_APPROVAL_RECORDED",
                "DESIGN_SYSTEM_DERIVED_AND_READY")}
            evidence["HOMEPAGE_APPROVAL"] = {**homepage_approval(), "RENDERED_SURFACES": receipts}
            evidence["HOMEPAGE_DESIGN"] = broken_homepage
            evidence["DESIGN_SYSTEM"] = {**design_system(), "HOMEPAGE_SOURCE": "COMPONENT_LIBRARY"}
            result = validate_production_gate(evidence, evidence_root=directory)
            self.assertFalse(result["ok"])
            self.assertIn("FULL_HOMEPAGE_SECTIONS_INCOMPLETE", issue_codes(result))
            self.assertIn("DESIGN_SYSTEM_SOURCE_NOT_APPROVED_HOMEPAGE", issue_codes(result))
            self.assertEqual(result["underlying_status"]["HOMEPAGE_DESIGN"], "BLOCKED")

    def test_missing_files_wrong_digests_and_wrong_build_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="wd-gate-evidence-") as directory:
            root = Path(directory)
            receipts = write_homepage_receipts(root)
            base = {field: True for field in (
                "BUSINESS_UNDERSTANDING_COMPLETE", "OWNER_INTENT_CAPTURED", "REQUIRED_ASSETS_IDENTIFIED",
                "REFERENCES_INTERPRETED", "HOMEPAGE_RENDERED_AND_REVIEWED", "OWNER_APPROVAL_RECORDED",
                "DESIGN_SYSTEM_DERIVED_AND_READY")}

            nonexistent = copy.deepcopy(receipts)
            nonexistent[0]["screenshot_path"] = "rendered/not-written.png"
            result = validate_production_gate(
                {**base, "HOMEPAGE_APPROVAL": {**homepage_approval(), "RENDERED_SURFACES": nonexistent}},
                evidence_root=directory)
            self.assertIn("PRODUCTION_ENTRY_EVIDENCE_NOT_BOUND", issue_codes(result))
            self.assertTrue(any("SCREENSHOT_FILE_MISSING" in item["message"]
                                for item in result["issues"]))

            wrong_digest = copy.deepcopy(receipts)
            wrong_digest[1]["screenshot_sha256"] = "0" * 64
            result = validate_production_gate(
                {**base, "HOMEPAGE_APPROVAL": {**homepage_approval(), "RENDERED_SURFACES": wrong_digest}},
                evidence_root=directory)
            self.assertTrue(any("SCREENSHOT_DIGEST_MISMATCH" in item["message"]
                                for item in result["issues"]))

            outside = copy.deepcopy(receipts)
            outside[0]["screenshot_path"] = "../escaped.png"
            result = validate_production_gate(
                {**base, "HOMEPAGE_APPROVAL": {**homepage_approval(), "RENDERED_SURFACES": outside}},
                evidence_root=directory)
            self.assertTrue(any("SCREENSHOT_PATH_OUT_OF_SCOPE" in item["message"]
                                or "SCREENSHOT_FILE_MISSING" in item["message"]
                                for item in result["issues"]))

            approval = {**homepage_approval(), "RENDERED_SURFACES": receipts,
                        "PROJECT": "other-project", "BUILD_ID": "build-a"}
            result = validate_production_gate(
                {**base, "HOMEPAGE_APPROVAL": approval}, evidence_root=directory,
                expected_project="alpha-starts-now", expected_build="build-b")
            messages = " ".join(item["message"] for item in result["issues"])
            self.assertIn("EVIDENCE_PROJECT_MISMATCH", messages)
            self.assertIn("STALE_EVIDENCE_REJECTED", messages)

    def test_real_files_and_consistent_receipts_pass_without_granting_approval(self) -> None:
        with tempfile.TemporaryDirectory(prefix="wd-gate-ok-") as directory:
            receipts = write_homepage_receipts(Path(directory))
            result = validate_rendered_visual_evidence(
                {"screenshot_set": receipts, "build_id": "test-build"},
                list(HOMEPAGE_REVIEW_SURFACES), evidence_root=directory,
                expected_build="test-build")
            self.assertEqual(result["status"], "PASS")
            self.assertTrue(result["receipts_resolved_on_disk"])
            # Valid hashes prove identity, never owner acceptance.
            self.assertNotIn("OWNER_FINAL_ACCEPTANCE", result)
            self.assertNotIn("owner_approved", result)

    def test_both_full_page_conventions_capture_the_whole_page(self) -> None:
        """R1 promoted: design-first homepage surfaces are not viewport crops."""
        plan = {
            "routes": [{"path": "/", "viewports": [1440]}],
            "visual_evidence": {
                "required": True,
                "required_surfaces": list(HOMEPAGE_REVIEW_SURFACES)
                + ["DESKTOP_FULL_PAGE", "MOBILE_FULL_PAGE", "DESKTOP_HERO"],
            },
        }
        captures = {job["surface_id"]: job["capture"]
                    for job in bqa_runner._matrix(plan, "smoke") if job.get("surface_id")}
        for surface in list(HOMEPAGE_REVIEW_SURFACES) + ["DESKTOP_FULL_PAGE", "MOBILE_FULL_PAGE"]:
            self.assertEqual(captures[surface], "FULL_PAGE", surface)
        self.assertEqual(captures["DESKTOP_HERO"], "VIEWPORT")

    def test_viewport_override_on_a_whole_page_surface_is_rejected(self) -> None:
        plan = {
            "routes": [{"path": "/", "viewports": [1440]}],
            "visual_evidence": {
                "required": True,
                "required_surfaces": [
                    {"surface_id": "DESKTOP_FULL_HOMEPAGE", "capture": "VIEWPORT"},
                    {"surface_id": "DESKTOP_HERO", "capture": "VIEWPORT"},
                ],
            },
        }
        jobs = {job["surface_id"]: job for job in bqa_runner._matrix(plan, "smoke")
                if job.get("surface_id")}
        self.assertEqual(jobs["DESKTOP_FULL_HOMEPAGE"]["capture"], "FULL_PAGE")
        self.assertEqual(jobs["DESKTOP_FULL_HOMEPAGE"]["capture_override_rejected"], "VIEWPORT")
        self.assertEqual(jobs["DESKTOP_HERO"]["capture"], "VIEWPORT")
        self.assertIsNone(jobs["DESKTOP_HERO"]["capture_override_rejected"])
        receipt = resolve_screenshot_receipt(
            {"surface_id": "DESKTOP_FULL_HOMEPAGE", "screenshot_path": "x.png",
             "screenshot_sha256": "0" * 64, "render_capture": "VIEWPORT"}, ".")
        self.assertIn("CAPTURE_LABEL_CONFLICT", issue_codes(receipt))

    def test_design_system_is_derived_from_approved_homepage(self) -> None:
        self.assertTrue(validate_design_system_derivation(design_system())["ok"])
        broken = design_system()
        broken["HOMEPAGE_SOURCE"] = "COMPONENT_LIBRARY"
        broken["CONTRADICTS_HOMEPAGE"] = True
        result = validate_design_system_derivation(broken)
        self.assertFalse(result["ok"])
        self.assertIn("DESIGN_SYSTEM_SOURCE_NOT_APPROVED_HOMEPAGE", issue_codes(result))
        self.assertIn("DESIGN_SYSTEM_CONTRADICTS_APPROVED_HOMEPAGE", issue_codes(result))

    def test_component_sources_are_downstream_and_stack_agnostic(self) -> None:
        valid = {
            "DESIGN_AUTHORITY": "DESIGN_SYSTEM",
            "COMPONENT_SOURCE": "CodeStitch",
            "MODEL_REQUIRED": False,
            "FRAMEWORK_REQUIRED": False,
        }
        result = validate_component_routing(valid)
        self.assertTrue(result["ok"])
        self.assertFalse(FIGMA_IN_DESIGN_FIRST_FLOW)
        self.assertFalse(result["figma_in_design_first_flow"])
        broken = dict(valid)
        broken["DESIGN_AUTHORITY"] = "COMPONENT_LIBRARY"
        result = validate_component_routing(broken)
        self.assertFalse(result["ok"])
        self.assertIn("COMPONENT_LIBRARY_NOT_AUTHORITY", issue_codes(result))
        external = dict(valid)
        external["DESIGN_AUTHORITY"] = "EXTERNAL_DESIGN_APPLICATION"
        self.assertIn("COMPONENT_AUTHORITY_MISSING", issue_codes(validate_component_routing(external)))

    def test_existing_inspiration_architecture_is_consumed_as_reference_only(self) -> None:
        registry = json.loads((ROOT / "templates" / "inspiration-source-registry.json").read_text(encoding="utf-8"))
        self.assertTrue(validate_inspiration_records([owner_reference()], registry)["ok"])
        clone = owner_reference()
        clone["LITERAL_CLONE"] = True
        result = validate_inspiration_records([clone])
        self.assertFalse(result["ok"])
        self.assertIn("REFERENCE_CLONE_REJECTED", issue_codes(result))

    def test_asset_classes_keep_reference_only_material_out_of_production(self) -> None:
        valid = [
            {"CLASSIFICATION": "REQUIRED_ASSET", "PROVENANCE_REF": "evidence://asset-1"},
            {"CLASSIFICATION": "REFERENCE_INSPIRATION_ONLY", "PROMOTED_TO_PRODUCTION": False},
            {"CLASSIFICATION": "SUPPORTING_MATERIAL"},
        ]
        self.assertTrue(validate_asset_intent(valid)["ok"])
        promoted = [dict(valid[1], PROMOTED_TO_PRODUCTION=True)]
        result = validate_asset_intent(promoted)
        self.assertFalse(result["ok"])
        self.assertIn("REFERENCE_ONLY_ASSET_NOT_PROMOTED", issue_codes(result))

    def test_browser_qa_behavior_authority_precedes_visual_gauntlet(self) -> None:
        valid = {
            "SEQUENCE": ["IMPLEMENT_REST", "BROWSER_QA", "VISUAL_GAUNTLET"],
            "AUTHORITIES": {"BROWSER_QA": "BEHAVIOR_AUTHORITY", "VISUAL_GAUNTLET": "QUALITATIVE_AUTHORITY"},
        }
        self.assertTrue(validate_downstream_authorities(valid)["ok"])
        broken = copy.deepcopy(valid)
        broken["SEQUENCE"] = ["IMPLEMENT_REST", "VISUAL_GAUNTLET", "BROWSER_QA"]
        self.assertIn("BROWSER_QA_BEFORE_GAUNTLET_REQUIRED", issue_codes(validate_downstream_authorities(broken)))
        self.assertIn("BROWSER_QA_BEFORE_GAUNTLET_REQUIRED", issue_codes(validate_downstream_authorities({"AUTHORITIES": valid["AUTHORITIES"]})))

    def test_exactly_five_owner_locks_and_no_homepage_lock(self) -> None:
        profile = {"locks": {name: False for name in CANONICAL_LOCKS}, "visual_prototypes": {"homepage_visual_approved": True}}
        self.assertTrue(validate_owner_lock_contract(profile)["ok"])
        broken = {"locks": {**profile["locks"], "homepage_visual_locked": True}}
        result = validate_owner_lock_contract(broken)
        self.assertFalse(result["ok"])
        self.assertIn("NO_SIXTH_OWNER_LOCK", issue_codes(result))

    def test_frozen_projects_remain_unchanged(self) -> None:
        guard = FrozenIntegrityGuard(
            str(ROOT),
            protected_paths=["projects/"],
            ledger_path="framework-validation/reports/runtime/design-first-frozen-integrity.log",
            run_id="design-first-production-flow-tests",
        )
        guard.snapshot()
        result = guard.verify()
        self.assertTrue(result.ok, result.summary())
        self.assertEqual(result.mutations, [])
        self.assertEqual(result.additions, [])
        self.assertEqual(result.deletions, [])

    def test_contract_artifacts_are_documented_without_new_state_or_lock(self) -> None:
        flow_doc = (ROOT / "DESIGN-FIRST-PRODUCTION-FLOW.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        implementation_contract = (ROOT / "IMPLEMENTATION-CONTRACT.md").read_text(encoding="utf-8")
        visual_prototype_protocol = (ROOT / "VISUAL-PROTOTYPE-PROTOCOL.md").read_text(encoding="utf-8")
        visual_prototype_template = (ROOT / "templates" / "visual-prototype-review.md").read_text(encoding="utf-8")
        state_registry = (ROOT / "schemas" / "state-ownership.json").read_text(encoding="utf-8")
        self.assertIn("UNDERSTANDING_PRECEDES_DESIGN", flow_doc)
        self.assertIn("APPROVED_HOMEPAGE_DEFINES_THE_SITE_SYSTEM", skill)
        self.assertIn("FIGMA_IN_DESIGN_FIRST_FLOW = NO", flow_doc)
        for text in (implementation_contract, visual_prototype_protocol, visual_prototype_template):
            self.assertNotIn("figma", text.lower())
        self.assertIn("homepage_visual_approved", skill)
        self.assertNotIn('"homepage_visual_approved"', state_registry)
        self.assertNotIn("V2.16", flow_doc + skill)
        self.assertNotIn("Capability #11", flow_doc + skill)


if __name__ == "__main__":
    unittest.main()
