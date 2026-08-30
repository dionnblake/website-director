"""Capability #8 Content Operations and CMS Architecture A-V controls."""

from __future__ import annotations

import copy
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "content-ops"))
sys.path.insert(0, str(ROOT / "browser-qa"))

import validator  # noqa: E402
from framework_validation import validator as framework_validator  # noqa: E402
from guards.frozen_integrity_guard import FrozenIntegrityGuard  # noqa: E402


SCENARIO_IDS = tuple(chr(code) for code in range(ord("A"), ord("V") + 1))
NEGATIVE_CONTROL_IDS = (
    "PRESENTATION_COUPLED_FIELD",
    "DUPLICATE_CONTENT_TYPE_ID",
    "RELATIONSHIP_TARGET_INVALID",
    "DRAFT_PUBLIC_LEAK",
    "PUBLISHED_SLUG_REDIRECT_MISSING",
    "UNSAFE_RICH_TEXT",
    "CLAIM_PROVENANCE_REQUIRED",
    "REFERENCE_ASSET_NOT_PRODUCTION",
    "AGENT_PUBLISHING_FORBIDDEN",
    "CONTENT_OPS_LOCK_FORBIDDEN",
    "FROZEN_FIXTURE_MUTATION",
)


def content_model() -> dict:
    return {
        "template": False,
        "cms_requirement": "STATIC_STRUCTURED_CONTENT",
        "content_types": [
            {
                "type_id": "article",
                "name": "Article",
                "purpose": "Reusable editorial article",
                "content_owner": "owner",
                "routes_used": ["/journal/:slug"],
                "fields": [
                    {"field_id": "headline", "label": "Headline", "type": "TEXT", "required": True, "validation": "non_empty"},
                    {"field_id": "slug", "label": "Slug", "type": "SLUG", "required": True, "validation": "lowercase_kebab_case"},
                    {"field_id": "body", "label": "Body", "type": "RICH_TEXT", "required": False, "validation": "semantic_allowlist"},
                    {"field_id": "hero_image", "label": "Hero image", "type": "IMAGE_REF", "required": False, "validation": "asset_and_provenance_ref"},
                    {"field_id": "seo_title", "label": "SEO title", "type": "TEXT", "required": False, "validation": "unique_title"},
                ],
                "required_fields": ["headline", "slug"],
                "optional_fields": ["body", "hero_image", "seo_title"],
                "relationships": [],
                "seo_fields": ["seo_title"],
                "media_fields": ["hero_image"],
                "provenance_fields": ["hero_image"],
                "editorial_status": ["DRAFT", "IN_REVIEW", "APPROVED", "SCHEDULED", "PUBLISHED", "ARCHIVED"],
                "slug_policy": {"unique": True, "published_change_requires_301": True},
                "archive_policy": {"listing": False, "redirects_retained": True},
            }
        ],
        "editable_surfaces": [
            {"surface_id": "article_headline", "classification": "EDITOR_EDITABLE", "editable_by": ["EDITOR"]},
            {"surface_id": "article_body", "classification": "EDITOR_EDITABLE", "editable_by": ["EDITOR"]},
            {"surface_id": "analytics_runtime", "classification": "SYSTEM_GENERATED", "editable_by": [], "editable": False},
        ],
        "roles": [
            {"role_id": "editor", "capabilities": ["CAN_EDIT", "CAN_REVIEW"]},
            {"role_id": "publisher", "capabilities": ["CAN_PUBLISH", "CAN_ARCHIVE"]},
            {"role_id": "owner", "capabilities": ["CAN_EDIT", "CAN_REVIEW", "CAN_PUBLISH", "CAN_ARCHIVE", "CAN_DELETE"]},
        ],
        "lifecycle": {
            "states": ["DRAFT", "IN_REVIEW", "APPROVED", "SCHEDULED", "PUBLISHED", "ARCHIVED"],
            "transitions": [
                {"from": "DRAFT", "to": "IN_REVIEW", "required_capability": "CAN_REVIEW"},
                {"from": "APPROVED", "to": "PUBLISHED", "required_capability": "CAN_PUBLISH"},
            ],
        },
        "preview": {"required": True, "renderer": "real_design_system_route_composition"},
        "scheduling": {
            "required": True,
            "SCHEDULED_AT": "content_item.scheduled_at",
            "TIMEZONE": "IANA timezone",
            "PUBLISHING_SYSTEM": "owner-approved publishing boundary",
            "FAILURE_BEHAVIOR": "record_and_hold",
        },
        "seo": {"structured_data_editable": False, "strategy_source": "SEO-INTELLIGENCE-PROTOCOL.md"},
        "portability": {
            "export_format": "JSON",
            "media_export": "ASSET_ID_AND_PROVENANCE_REF",
            "relationship_export": "TYPE_ID_AND_FIELD_ID",
            "slug_export": "SOURCE_AND_TARGET",
            "provenance_export": "PROVENANCE_REF",
        },
        "migration": {"required": False, "inventory": []},
    }


def article_item(status: str = "DRAFT", publicly_visible: bool | None = None, **values: object) -> dict:
    item = {
        "content_type_id": "article",
        "editorial_status": status,
        "publicly_visible": status == "PUBLISHED" if publicly_visible is None else publicly_visible,
        "listed": status == "PUBLISHED",
        "headline": "A synthetic article",
        "slug": "synthetic-article",
    }
    item.update(values)
    return item


class ContentOperationsScenarios(unittest.TestCase):
    """Synthetic A-V coverage; no test writes under the repository projects/ tree."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.guard_tmp = tempfile.TemporaryDirectory(prefix="website-director-v213-guard-")
        cls.guard = FrozenIntegrityGuard(
            str(ROOT),
            protected_paths=["projects/"],
            ledger_path=str(Path(cls.guard_tmp.name) / "frozen-violations.log"),
            run_id="v2-13-content-operations",
        ).snapshot()

    @classmethod
    def tearDownClass(cls) -> None:
        result = cls.guard.verify(record_violation=True)
        cls.guard_tmp.cleanup()
        if not result.ok:
            raise AssertionError(result.summary())

    def assert_code(self, report: dict, code: str) -> None:
        codes = {issue.get("code") for issue in report.get("issues", [])}
        self.assertIn(code, codes, report)

    def assert_not_pass(self, report: dict, code: str | None = None) -> None:
        self.assertNotEqual(report.get("status"), "PASS", report)
        if code:
            self.assert_code(report, code)

    def test_a_simple_brochure_does_not_need_a_cms(self) -> None:
        assessment = validator.calculate_cms_necessity({
            "content_volume": 5,
            "update_frequency": "YEARLY",
            "number_of_editors": 1,
            "editor_technical_level": "TECHNICAL",
            "content_relationships": False,
            "preview_requirements": False,
            "scheduling_requirements": False,
            "multi_channel_requirements": False,
            "approval_workflow": False,
        })
        self.assertEqual(assessment["cms_requirement"], "NO_CMS_REQUIRED")
        self.assertFalse(assessment["cms_required"])

    def test_b_large_nontechnical_editorial_corpus_needs_a_cms(self) -> None:
        assessment = validator.calculate_cms_necessity({
            "content_volume": 500,
            "update_frequency": "WEEKLY",
            "number_of_editors": 5,
            "editor_technical_level": "NONTECHNICAL",
            "content_relationships": True,
            "preview_requirements": True,
            "scheduling_requirements": True,
            "approval_workflow": True,
        })
        self.assertTrue(assessment["cms_required"])
        self.assertIn(assessment["cms_requirement"], {"DATABASE_BACKED_CONTENT", "TRADITIONAL_CMS", "HEADLESS_CMS"})

    def test_b1_portability_is_recorded_as_a_necessity_factor(self) -> None:
        assessment = validator.calculate_cms_necessity({"portability_requirements": True})
        self.assertIn("portability requirements", assessment["rationale"])
        self.assertEqual(assessment["factors"]["portability_requirements"], True)

    def test_c_repeated_content_must_be_modeled(self) -> None:
        model = content_model()
        model["repeated_content"] = [{"mode": "HARD_CODED_INDIVIDUAL", "count": 3}]
        report = validator.validate_content_model(model)
        self.assert_not_pass(report, "REPEATED_CONTENT_HARD_CODED")

    def test_d_presentation_coupled_field_fails(self) -> None:
        model = content_model()
        model["content_types"][0]["fields"][0]["field_id"] = "hero_text_line_2_blue"
        report = validator.validate_content_model(model)
        self.assert_not_pass(report, "PRESENTATION_COUPLED_FIELD")

    def test_e_semantic_headline_field_passes(self) -> None:
        report = validator.validate_content_model(content_model())
        self.assertEqual(report["status"], "PASS", report)

    def test_f_draft_exposed_publicly_fails(self) -> None:
        report = validator.validate_content_model(content_model(), [article_item("DRAFT", publicly_visible=True)])
        self.assert_not_pass(report, "DRAFT_PUBLIC_LEAK")

    def test_g_published_article_visible_passes(self) -> None:
        report = validator.validate_content_model(content_model(), [article_item("PUBLISHED", publicly_visible=True)])
        self.assertEqual(report["status"], "PASS", report)

    def test_h_editor_cannot_edit_analytics_event_name(self) -> None:
        surfaces = copy.deepcopy(content_model()["editable_surfaces"])
        surfaces.append({"surface_id": "analytics_event_name", "classification": "EDITOR_EDITABLE", "editable_by": ["EDITOR"]})
        report = validator.validate_editable_surfaces(surfaces)
        self.assert_not_pass(report, "PROTECTED_SURFACE_EDITABLE")

    def test_i_editor_cannot_edit_design_tokens(self) -> None:
        surfaces = copy.deepcopy(content_model()["editable_surfaces"])
        surfaces.append({"surface_id": "design_tokens", "classification": "EDITOR_EDITABLE", "editable_by": ["EDITOR"]})
        report = validator.validate_editable_surfaces(surfaces)
        self.assert_not_pass(report, "PROTECTED_SURFACE_EDITABLE")

    def test_j_published_slug_change_requires_redirect(self) -> None:
        report = validator.validate_slug_change("old-article", "new-article", status="PUBLISHED", redirects=[])
        self.assert_not_pass(report, "PUBLISHED_SLUG_REDIRECT_MISSING")

    def test_k_archived_slug_change_with_301_passes(self) -> None:
        report = validator.validate_slug_change(
            "old-article",
            "new-article",
            status="ARCHIVED",
            redirects=[{"source": "old-article", "destination": "new-article", "status": 301}],
        )
        self.assertEqual(report["status"], "PASS", report)

    def test_l_high_risk_claim_without_provenance_fails(self) -> None:
        item = article_item("DRAFT", claims=[{"claim_id": "claim-financial", "claim_type": "FINANCIAL", "text": "Synthetic performance claim"}])
        report = validator.validate_content_model(content_model(), [item])
        self.assert_not_pass(report, "CLAIM_PROVENANCE_REQUIRED")

    def test_m_asset_director_and_provenance_media_reference_passes(self) -> None:
        item = article_item("DRAFT", hero_image={"media_id": "media-1", "asset_id": "asset-1", "provenance_ref": "prov-asset-1", "alt_text": "Synthetic image"})
        report = validator.validate_content_model(
            content_model(),
            [item],
            asset_manifest={"assets": [{"asset_id": "asset-1", "production_status": "PRODUCTION"}]},
            provenance_ledger={"assets": [{"asset_id": "prov-asset-1", "provenance_id": "prov-asset-1"}]},
        )
        self.assertEqual(report["status"], "PASS", report)

    def test_m1_media_reference_without_ledgers_is_blocked(self) -> None:
        report = validator.validate_media_reference({
            "media_id": "media-unverified",
            "asset_id": "asset-unverified",
            "provenance_ref": "prov-unverified",
        })
        self.assert_not_pass(report, "MEDIA_ASSET_UNRESOLVED")
        self.assert_code(report, "MEDIA_PROVENANCE_UNRESOLVED")

    def test_n_research_reference_cannot_be_production_media(self) -> None:
        report = validator.validate_media_reference({
            "media_id": "reference-1",
            "asset_id": "reference-asset",
            "provenance_ref": "reference-provenance",
            "source_url": "https://dribbble.com/shots/synthetic-reference",
        })
        self.assert_not_pass(report, "REFERENCE_ASSET_NOT_PRODUCTION")

    def test_o_unsafe_rich_text_fails(self) -> None:
        report = validator.validate_rich_text('<p>safe-looking</p><script>alert("x")</script>')
        self.assert_not_pass(report, "UNSAFE_RICH_TEXT")

    def test_o1_rich_text_data_url_fails(self) -> None:
        report = validator.validate_rich_text('<a href="data:text/html,unsafe">link</a>')
        self.assert_not_pass(report, "UNSAFE_RICH_TEXT_URL")

    def test_p_static_markdown_source_is_justified(self) -> None:
        report = validator.validate_cms_decision({
            "cms_required": False,
            "cms_requirement": "STATIC_STRUCTURED_CONTENT",
            "storage": {"format": "Markdown"},
            "export_capability": True,
            "cost_model": "KNOWN",
        })
        self.assertEqual(report["status"], "PASS", report)

    def test_q_unavailable_cms_provider_is_blocked(self) -> None:
        report = validator.validate_cms_decision({
            "cms_required": True,
            "cms_requirement": "HEADLESS_CMS",
            "selected_provider": "synthetic-provider",
            "provider_status": "UNAVAILABLE",
        })
        self.assertEqual(report["status"], "BLOCKED", report)
        self.assert_code(report, "CMS_PROVIDER_UNAVAILABLE")

    def test_r_agent_content_cannot_be_published_directly(self) -> None:
        report = validator.validate_agent_publishing({"generated_by_agent": True, "status": "PUBLISHED"})
        self.assert_not_pass(report, "AGENT_PUBLISHING_FORBIDDEN")

    def test_s_agent_content_defaults_to_draft(self) -> None:
        report = validator.validate_agent_publishing({"generated_by_agent": True, "status": "DRAFT"})
        self.assertEqual(report["status"], "PASS", report)

    def test_t_proprietary_provider_without_export_is_visible_warning(self) -> None:
        report = validator.validate_cms_decision({
            "cms_required": True,
            "cms_requirement": "TRADITIONAL_CMS",
            "selected_provider": "proprietary-provider",
            "export_capability": False,
            "lock_in_risk": "PROPRIETARY",
            "cost_model": "UNKNOWN",
        })
        self.assertEqual(report["status"], "PASS", report)
        self.assertGreaterEqual(report["counts"]["warnings"], 1)
        self.assert_code(report, "CMS_EXPORT_UNAVAILABLE")

    def test_t1_required_preview_and_scheduling_are_architecture_contracts(self) -> None:
        preview = validator.validate_preview({"required": True, "raw_json_is_preview": True, "renderer": "raw JSON dump"})
        self.assert_not_pass(preview, "RAW_JSON_PREVIEW_FORBIDDEN")
        scheduling = validator.validate_scheduling({"required": True, "failure_behavior": "record_and_hold"})
        self.assert_not_pass(scheduling, "SCHEDULING_FIELD_MISSING")

    def test_t2_neutral_exception_state_is_valid(self) -> None:
        report = validator.validate_content_ops_state({
            "complete": False,
            "cms_requirement": "UNASSESSED",
            "exception": {"applied": False, "reason": None},
        })
        self.assertEqual(report["status"], "PASS", report)

    def test_t3_complete_state_requires_model_and_decision_inputs(self) -> None:
        report = validator.validate_content_operations(state={
            "complete": True,
            "cms_requirement": "NO_CMS_REQUIRED",
            "content_model_ready": True,
            "editable_surfaces_defined": True,
            "editorial_workflow_defined": True,
            "publishing_authority_defined": True,
            "slug_policy_defined": True,
            "portability_reviewed": True,
            "migration_required": False,
            "selected_architecture": None,
            "exception": {"applied": False, "reason": None},
        })
        self.assert_not_pass(report, "CONTENT_MODEL_MISSING")
        self.assert_code(report, "CMS_DECISION_MISSING")

    def test_u_content_ops_cannot_create_a_sixth_owner_lock(self) -> None:
        profile = {"locks": {name: False for name in framework_validator.CANONICAL_LOCKS}}
        profile["locks"]["content_ops_locked"] = False
        self.assertIn("OWNER_LOCK_INVARIANT", framework_validator.validate_owner_locks(profile))

    def test_v_frozen_integrity_guard_records_mutation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-v213-mutation-") as directory:
            root = Path(directory)
            project_file = root / "projects" / "fixture.txt"
            project_file.parent.mkdir(parents=True)
            project_file.write_text("before", encoding="utf-8")
            guard = FrozenIntegrityGuard(str(root), protected_paths=["projects/"], ledger_path="violations.log", run_id="scenario-v").snapshot()
            project_file.write_text("after", encoding="utf-8")
            result = guard.verify(record_violation=True)
            self.assertFalse(result.ok)
            self.assertIn("projects/fixture.txt", result.mutations)
            self.assertTrue(Path(result.ledger_path).is_file())

    def test_negative_duplicate_content_type_id(self) -> None:
        model = content_model()
        model["content_types"].append(copy.deepcopy(model["content_types"][0]))
        report = validator.validate_content_model(model)
        self.assert_not_pass(report, "DUPLICATE_CONTENT_TYPE_ID")

    def test_negative_broken_relationship_reference(self) -> None:
        model = content_model()
        model["content_types"][0]["relationships"] = [{"field": "related", "target_type": "missing_type"}]
        report = validator.validate_content_model(model)
        self.assert_not_pass(report, "RELATIONSHIP_TARGET_INVALID")


if __name__ == "__main__":
    unittest.main()
