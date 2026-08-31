"""Capability #9 Localization and Internationalization A-AF controls."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "browser-qa"))

from framework_validation import validator as framework_validator  # noqa: E402
from assertions import REQUIREMENT_SOURCES, evaluate  # noqa: E402
from engine.base import LocalizationObservation, PageObservation, load_engine  # noqa: E402
from guards.frozen_integrity_guard import FrozenIntegrityGuard  # noqa: E402
from localization import validator  # noqa: E402


SCENARIO_IDS = tuple(chr(code) for code in range(ord("A"), ord("Z") + 1)) + ("AA", "AB", "AC", "AD", "AE", "AF")
NEGATIVE_CONTROL_IDS = (
    "INVALID_LOCALE_CODE",
    "DUPLICATE_DEFAULT_LOCALE",
    "FALLBACK_CYCLE",
    "LOCALE_ROUTE_COLLISION",
    "HTML_LANG_MISMATCH",
    "HREFLANG_RECIPROCITY_MISSING",
    "CANONICAL_NOT_SELF_REFERENCING",
    "MACHINE_DRAFT_PUBLISHED",
    "UNREVIEWED_TRANSLATION_PUBLISHED",
    "TRANSLATION_STALE",
    "UI_STRING_CONCATENATION",
    "PLURALIZATION_UNSAFE",
    "HARDCODED_DATE_FORMAT",
    "CURRENCY_INFERRED_FROM_LANGUAGE",
    "RTL_DIRECTION_MISMATCH",
    "RTL_BRAND_MARK_MIRRORED",
    "PSEUDOLOCALIZATION_OVERFLOW",
    "LOCALE_FONT_COVERAGE_UNVERIFIED",
    "LOCALE_FONT_LICENSE_UNRESOLVED",
    "CLAIM_STRENGTHENED",
    "LEGAL_TRANSLATION_NOT_APPROVED",
    "REFERENCE_ASSET_NOT_PRODUCTION",
    "OWNER_LOCK_INVARIANT",
    "FROZEN_FIXTURE_MUTATION",
    "LOCALIZATION_AUTHORITY_CONFLICT",
    "UI_TRANSLATION_COVERAGE",
    "ANALYTICS_INTEGRATION_SHAPE",
    "LOCALIZED_SLUG_301",
    "REVIEW_STATUS_CONTRADICTION",
    "ACCESSIBILITY_BOOLEAN_SHAPE",
    "BROWSER_OBSERVATION_DEFAULTS",
)


def locale_record(
    locale: str,
    *,
    default: bool = False,
    source: bool = False,
    prefix: str | None = None,
    direction: str = "ltr",
    fallback: str | None = None,
    status: str = "PUBLISHED",
) -> dict:
    parsed = validator.parse_locale(locale)
    assert parsed is not None
    return {
        "locale": locale,
        "language": parsed["language"],
        "region": parsed["region"],
        "script": parsed["script"],
        "enabled": True,
        "default": default,
        "source": source,
        "route_prefix": prefix if prefix is not None else "/" + parsed["language"],
        "direction": direction,
        "status": status,
        "translation_owner": "owner",
        "fallback_locale": fallback,
        "seo_enabled": True,
        "content_coverage": "FULL",
        "review_status": "APPROVED",
    }


def valid_registry() -> dict:
    return {
        "required": True,
        "status": "READY",
        "source_locale": "en-US",
        "default_locale": "en-US",
        "supported_locales": ["en-US", "es-MX"],
        "route_strategy": "PATH_PREFIX",
        "default_locale_url_policy": "ROOT",
        "fallback_policy": "SOURCE_LOCALE_FALLBACK",
        "locales": [
            locale_record("en-US", default=True, source=True, prefix="/"),
            locale_record("es-MX", prefix="/es-mx", fallback="en-US"),
        ],
    }


def valid_state() -> dict:
    return {
        "required": True,
        "complete": True,
        "status": "READY",
        "source_locale": "en-US",
        "default_locale": "en-US",
        "supported_locales": ["en-US", "es-MX"],
        "route_strategy": "PATH_PREFIX",
        "fallback_policy_defined": True,
        "seo_localization_ready": True,
        "content_localization_ready": True,
        "rtl_required": False,
        "translation_review_required": True,
        "implementation_verified": False,
        "production_verified": False,
        "blocked_reason": None,
        "exception": {"applied": False, "reason": None},
    }


def valid_pages() -> list[dict]:
    return [
        {
            "page_id": "about-en",
            "content_id": "about",
            "locale": "en-US",
            "url": "/about",
            "canonical": "/about",
            "html_lang": "en-US",
            "title": "About Our Studio",
            "indexable": True,
            "hreflang_required": True,
            "hreflang": [
                {"hreflang": "en-US", "href": "/about"},
                {"hreflang": "es-MX", "href": "/es-mx/about"},
                {"hreflang": "x-default", "href": "/about"},
            ],
        },
        {
            "page_id": "about-es",
            "content_id": "about",
            "locale": "es-MX",
            "url": "/es-mx/about",
            "canonical": "/es-mx/about",
            "html_lang": "es-MX",
            "title": "Sobre Nuestro Estudio",
            "indexable": True,
            "hreflang_required": True,
            "hreflang": [
                {"hreflang": "en-US", "href": "/about"},
                {"hreflang": "es-MX", "href": "/es-mx/about"},
                {"hreflang": "x-default", "href": "/about"},
            ],
        },
    ]


def browser_localization_plan() -> dict:
    return {
        "localization": {
            "required": True,
            "supported_locales": ["en-US", "es-MX"],
            "switcher": {"required": True},
            "hreflang": {"required": True, "require_localized_canonical": True},
            "fallback": {"required": True, "locale": "en-US"},
            "metadata": {"title": True, "description": True, "og": True, "alt": True},
            "forms": {"required": True},
            "pseudo_localization": {"enabled": True, "minimum_ratio": 1.3},
            "rtl": {"required": False},
        },
        "routes": [{
            "path": "/es-mx/about",
            "locale": "es-MX",
            "direction": "ltr",
            "equivalent_route": "/about",
        }],
    }


def browser_localization_observation(**overrides) -> PageObservation:
    values = {
        "locale": "es-MX",
        "html_lang": "es-MX",
        "html_dir": "ltr",
        "route_resolves": True,
        "switcher_present": True,
        "switcher_accessible": True,
        "switcher_keyboard_operable": True,
        "switcher_labels": ["English", "Español"],
        "switcher_current_locale": "es-MX",
        "equivalent_route": "/about",
        "hreflang": [
            {"hreflang": "en-US", "reciprocal": True},
            {"hreflang": "es-MX", "reciprocal": True},
        ],
        "canonical": "https://example.test/es-mx/about",
        "canonical_is_self": True,
        "localized_title": True,
        "localized_description": True,
        "localized_og": True,
        "localized_alt": True,
        "fallback_explicit": True,
        "fallback_locale": "en-US",
        "localized_form_labels": True,
        "localized_form_errors": True,
        "text_expansion_ratio": 1.35,
    }
    values.update(overrides)
    obs = PageObservation(route="/es-mx/about", viewport=390, engine="simulation", browser="simulation")
    obs.localization = LocalizationObservation(**values)
    return obs


def valid_translation(**overrides: object) -> dict:
    record = {
        "translation_id": "about.summary.es-MX",
        "content_id": "about.summary",
        "source_locale": "en-US",
        "target_locale": "es-MX",
        "source_text_version": "1",
        "translation_method": "HUMAN",
        "review_status": "APPROVED",
        "reviewer": "owner",
        "status": "PUBLISHED",
        "published": True,
        "source_text": "Our studio can help.",
        "translated_text": "Nuestro estudio puede ayudar.",
        "translated_at": "2026-08-29T12:00:00+00:00",
    }
    record.update(overrides)
    return record


def valid_content_model() -> dict:
    return {
        "content_types": [
            {
                "type_id": "page",
                "fields": [
                    {"field_id": "title", "localizable": True},
                    {"field_id": "body", "localizable": True},
                    {"field_id": "stable_id", "localizable": False},
                ],
            }
        ]
    }


def valid_manifest() -> dict:
    return {
        "template_version": "2.14.0",
        "framework_version": "2.14.0",
        "project_name": "Synthetic Localization Pilot",
        "required": True,
        "status": "READY",
        "source_locale": "en-US",
        "default_locale": "en-US",
        "supported_locales": ["en-US", "es-MX"],
        "state": valid_state(),
        "locale_registry": valid_registry(),
        "formatting": {
            "date_strategy": "Intl.DateTimeFormat",
            "time_strategy": "Intl.DateTimeFormat with explicit timezone",
            "number_strategy": "Intl.NumberFormat",
            "currency_strategy": "explicit currency code",
            "unit_strategy": "canonical units with documented conversion",
            "pluralization_strategy": "CLDR plural categories",
            "interpolation_strategy": "named escaped variables",
            "currency_by_locale": {"en-US": "USD", "es-MX": "MXN"},
        },
        "logical_css": {"required": False, "uses_logical_properties": False},
        "ui_strings": [
            {
                "message_id": "nav.primary_label",
                "source_message": "Primary navigation",
                "translations": {"en-US": "Primary navigation", "es-MX": "Navegación principal"},
            },
            {
                "message_id": "results.item_count",
                "source_message": "{count} result",
                "count_variable": "count",
                "uses_plural_categories": True,
                "format": "ICU",
                "translations": {"en-US": "{count} result", "es-MX": "{count} resultado"},
            },
        ],
        "translations": [valid_translation()],
        "pages": valid_pages(),
        "fonts": [],
        "assets": [
            {
                "asset_id": "brand-photo",
                "production_status": "PRODUCTION",
                "locale_scope": "LOCALE_NEUTRAL",
                "provenance_ref": "prov-brand-photo",
            }
        ],
        "pseudolocalization": [],
        "content_ops": {
            "content_model_ref": "templates/content-model.json",
            "strategy": "FIELD_LEVEL_LOCALIZATION",
            "localizable_fields": ["title", "body"],
            "non_localizable_fields": ["stable_id"],
            "portability_reviewed": True,
        },
        "content_model": valid_content_model(),
        "accessibility": {
            "locale_switcher_required": True,
            "locale_switcher_accessible": True,
            "flag_only_selector": False,
            "keyboard_accessible": True,
            "screen_reader_accessible": True,
            "current_locale_exposed": True,
            "translated_form_errors": True,
            "translated_labels": True,
        },
        "analytics": {
            "locale_parameter_required": True,
            "locale_parameter": True,
            "events": [{"event_name": "form_submit", "locale": "es-MX"}],
        },
        "handoff": {
            "locale_list": ["en-US", "es-MX"],
            "source_locale": "en-US",
            "translation_workflow": "owner-reviewed",
            "cms_localization_model": "FIELD_LEVEL_LOCALIZATION",
            "review_responsibilities": "owner",
            "stale_translation_process": "mark stale and re-review",
            "localized_asset_responsibilities": "asset owner",
            "seo_localization_process": "reciprocal hreflang review",
            "provider_dependencies": [],
            "duplicates_v25_handoff": False,
        },
        "external_translation_provider_required": False,
    }


def neutral_manifest() -> dict:
    return {
        "template_version": "2.14.0",
        "framework_version": "2.14.0",
        "project_name": "English-only synthetic site",
        "required": False,
        "status": "NOT_REQUIRED",
        "state": {
            "required": False,
            "complete": False,
            "source_locale": None,
            "default_locale": None,
            "supported_locales": [],
            "route_strategy": None,
            "fallback_policy_defined": False,
            "seo_localization_ready": False,
            "content_localization_ready": False,
            "rtl_required": False,
            "translation_review_required": False,
            "implementation_verified": False,
            "production_verified": False,
            "blocked_reason": None,
            "exception": {"applied": False, "reason": None},
        },
        "locale_registry": {
            "required": False,
            "status": "NOT_REQUIRED",
            "source_locale": None,
            "default_locale": None,
            "route_strategy": "NO_PUBLIC_LOCALE_ROUTING",
            "fallback_policy": "NO_FALLBACK",
            "locales": [],
        },
        "external_translation_provider_required": False,
    }


class LocalizationScenarios(unittest.TestCase):
    """Synthetic A-AF coverage; no test writes under the repository projects/ tree."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.guard_tmp = tempfile.TemporaryDirectory(prefix="website-director-v214-guard-")
        cls.guard = FrozenIntegrityGuard(
            str(ROOT),
            protected_paths=["projects/"],
            ledger_path=str(Path(cls.guard_tmp.name) / "frozen-violations.log"),
            run_id="v2-14-localization",
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

    def test_a_english_only_is_not_required_and_has_no_bloat(self) -> None:
        assessment = validator.calculate_localization_requirement({
            "localization_required": False,
            "ip_address": "198.51.100.20",
            "browser_language": "es-MX",
        })
        self.assertEqual(assessment["status"], "NOT_REQUIRED")
        self.assertFalse(assessment["localization_required"])
        self.assertEqual(assessment["ignored_inference_inputs"], ["ip_address", "browser_language"])
        self.assertEqual(validator.validate_localization_manifest(neutral_manifest())["status"], "PASS")

    def test_b_english_and_spanish_registry_passes(self) -> None:
        report = validator.validate_localization_manifest(valid_manifest())
        self.assertEqual(report["status"], "PASS", report)

    def test_c_duplicate_default_fails(self) -> None:
        registry = valid_registry()
        registry["locales"].append(locale_record("fr-FR", default=True, prefix="/fr", fallback="en-US"))
        report = validator.validate_locale_registry(registry)
        self.assert_not_pass(report, "MULTIPLE_DEFAULT_LOCALES")

    def test_d_missing_source_fails(self) -> None:
        registry = valid_registry()
        registry["source_locale"] = None
        registry["locales"][0]["source"] = False
        report = validator.validate_locale_registry(registry)
        self.assert_not_pass(report, "SOURCE_LOCALE_REQUIRED")

    def test_e_invalid_locale_code_fails(self) -> None:
        registry = valid_registry()
        registry["locales"][1]["locale"] = "english_USA"
        report = validator.validate_locale_registry(registry)
        self.assert_not_pass(report, "INVALID_LOCALE_CODE")

    def test_f_parent_locale_fallback_passes(self) -> None:
        registry = valid_registry()
        registry["locales"].append(locale_record("es", prefix="/es", fallback="en-US"))
        registry["locales"][1]["fallback_locale"] = "es"
        report = validator.validate_locale_registry(registry)
        self.assertEqual(report["status"], "PASS", report)

    def test_g_fallback_cycle_fails(self) -> None:
        registry = valid_registry()
        registry["locales"].append(locale_record("fr-FR", prefix="/fr", fallback="es-MX"))
        registry["locales"][1]["fallback_locale"] = "fr-FR"
        report = validator.validate_locale_registry(registry)
        self.assert_not_pass(report, "FALLBACK_CYCLE")

    def test_h_route_collision_fails(self) -> None:
        registry = valid_registry()
        registry["locales"][1]["route_prefix"] = "/"
        report = validator.validate_locale_registry(registry)
        self.assert_not_pass(report, "LOCALE_ROUTE_COLLISION")

    def test_i_wrong_html_lang_fails(self) -> None:
        pages = valid_pages()
        pages[0]["html_lang"] = "es-MX"
        report = validator.validate_hreflang(pages, source_locale="en-US")
        self.assert_not_pass(report, "HTML_LANG_MISMATCH")

    def test_j_missing_hreflang_reciprocity_fails(self) -> None:
        pages = valid_pages()
        pages[1]["hreflang"] = [item for item in pages[1]["hreflang"] if item["hreflang"] != "en-US"]
        report = validator.validate_hreflang(pages, source_locale="en-US")
        self.assert_not_pass(report, "HREFLANG_RECIPROCITY_MISSING")

    def test_k_localized_canonical_to_source_fails(self) -> None:
        pages = valid_pages()
        pages[1]["canonical"] = "/about"
        report = validator.validate_hreflang(pages, source_locale="en-US")
        self.assert_not_pass(report, "CANONICAL_NOT_SELF_REFERENCING")

    def test_l_machine_draft_published_fails(self) -> None:
        record = valid_translation(status="MACHINE_DRAFT", review_status="HUMAN_REVIEW_REQUIRED")
        report = validator.validate_translation_record(record)
        self.assert_not_pass(report, "MACHINE_DRAFT_PUBLISHED")

    def test_m_human_reviewed_published_passes(self) -> None:
        report = validator.validate_translation_record(valid_translation())
        self.assertEqual(report["status"], "PASS", report)

    def test_n_source_change_marks_translation_stale(self) -> None:
        record = valid_translation(status="STALE", source_text_version="1")
        self.assertTrue(validator.detect_stale_translation(record, current_source_version="2"))
        report = validator.validate_translation_record(record, current_source_version="2")
        self.assert_code(report, "TRANSLATION_STALE_DETECTED")

    def test_o_stale_translation_treated_as_current_fails(self) -> None:
        record = valid_translation(status="REVIEWED", review_status="REVIEWED", published=False, source_text_version="1")
        report = validator.validate_translation_record(record, current_source_version="2")
        self.assert_not_pass(report, "TRANSLATION_STALE")

    def test_p_ui_concatenation_and_pluralization_fail(self) -> None:
        report = validator.validate_ui_strings([{
            "message_id": "results.item_count",
            "source_message": "{count} result",
            "count_variable": "count",
            "uses_concatenation": True,
            "format": "PLAIN",
        }])
        self.assert_not_pass(report, "UI_STRING_CONCATENATION")
        self.assert_code(report, "PLURALIZATION_UNSAFE")

    def test_q_hard_coded_date_format_fails(self) -> None:
        report = validator.validate_formatting({"date_strategy": "MM/DD/YYYY"})
        self.assert_not_pass(report, "HARDCODED_DATE_FORMAT")

    def test_r_currency_inferred_from_language_fails(self) -> None:
        report = validator.validate_formatting({"currency_inferred_from_language": True})
        self.assert_not_pass(report, "CURRENCY_INFERRED_FROM_LANGUAGE")

    def test_s_rtl_locale_declared_ltr_fails(self) -> None:
        registry = valid_registry()
        registry["locales"].append(locale_record("ar", prefix="/ar", direction="ltr", fallback="en-US"))
        report = validator.validate_locale_registry(registry)
        self.assert_not_pass(report, "RTL_DIRECTION_MISMATCH")

    def test_t_rtl_brand_logo_mirroring_fails(self) -> None:
        report = validator.validate_rtl([{
            "locale": "ar",
            "direction": "rtl",
            "mirror_policy": {"brand_logo": True},
        }])
        self.assert_not_pass(report, "RTL_BRAND_MARK_MIRRORED")

    def test_u_pseudo_localized_cta_overflow_fails(self) -> None:
        report = validator.validate_pseudolocalized_items([{
            "id": "cta.submit",
            "source": "Submit your commission inquiry",
            "max_chars": 10,
        }])
        self.assert_not_pass(report, "PSEUDOLOCALIZATION_OVERFLOW")

    def test_v_locale_without_script_font_is_blocked(self) -> None:
        report = validator.validate_typography(
            [{"locale": "ja", "direction": "ltr"}],
            [{"font_id": "latin-only", "supported_scripts": ["Latn"], "license_status": "VERIFIED", "redistribution_status": "PERMITTED"}],
        )
        self.assert_not_pass(report, "LOCALE_FONT_COVERAGE_UNVERIFIED")

    def test_w_unresolved_font_license_fails(self) -> None:
        report = validator.validate_typography(
            [{"locale": "ja", "direction": "ltr"}],
            [{"font_id": "japanese-font", "supported_scripts": ["Jpan"], "license_status": "UNKNOWN", "redistribution_status": "PERMITTED"}],
        )
        self.assert_not_pass(report, "LOCALE_FONT_LICENSE_UNRESOLVED")

    def test_x_translated_claim_cannot_strengthen_source(self) -> None:
        report = validator.validate_translation_record(valid_translation(
            status="REVIEWED",
            review_status="REVIEWED",
            published=False,
            source_claim_strength="MAY",
            translated_claim_strength="GUARANTEES",
            evidence_ref="claim-1",
        ))
        self.assert_not_pass(report, "CLAIM_STRENGTHENED")

    def test_y_machine_translated_legal_content_is_not_legal_approval(self) -> None:
        report = validator.validate_translation_record(valid_translation(
            content_id="privacy_policy",
            content_type="privacy_policy",
            status="REVIEWED",
            review_status="HUMAN_REVIEWED",
            published=False,
            translation_method="MACHINE",
            legally_approved=True,
            legal_reviewed=False,
        ))
        self.assert_not_pass(report, "LEGAL_TRANSLATION_NOT_APPROVED")

    def test_z_unreviewed_translation_published_fails(self) -> None:
        report = validator.validate_translation_record(valid_translation(
            status="PUBLISHED",
            review_status="NOT_REVIEWED",
            published=True,
        ))
        self.assert_not_pass(report, "UNREVIEWED_TRANSLATION_PUBLISHED")

    def test_aa_same_event_with_locale_parameter_passes(self) -> None:
        report = validator.validate_analytics_locale({
            "locale_parameter_required": True,
            "locale_parameter": True,
            "events": [{"event_name": "form_submit", "locale": "es-MX"}],
        })
        self.assertEqual(report["status"], "PASS", report)

    def test_ab_per_language_event_names_fail(self) -> None:
        report = validator.validate_analytics_locale({
            "locale_parameter": False,
            "events": [{"event_name": "signup_es"}],
        })
        self.assert_not_pass(report, "DUPLICATE_LOCALE_ANALYTICS_EVENT")

    def test_ac_localized_cms_record_retains_provenance_and_portability(self) -> None:
        report = validator.validate_content_ops_integration(
            valid_manifest()["content_ops"],
            content_model=valid_content_model(),
        )
        self.assertEqual(report["status"], "PASS", report)

    def test_ad_research_reference_cannot_be_production_media(self) -> None:
        report = validator.validate_assets([{
            "asset_id": "reference-1",
            "production_status": "PRODUCTION",
            "locale_scope": "LOCALE_NEUTRAL",
            "provenance_ref": "prov-reference-1",
            "source_url": "https://dribbble.com/shots/synthetic-reference",
        }])
        self.assert_not_pass(report, "REFERENCE_ASSET_NOT_PRODUCTION")

    def test_browser_qa_localization_uses_the_shared_assertion_catalogue(self) -> None:
        self.assertIn("LOCALIZATION_PLAN", REQUIREMENT_SOURCES)
        self.assertFalse((ROOT / "localization" / "runner.py").exists())
        findings = evaluate(browser_localization_observation(), browser_localization_plan())
        relevant = [finding for finding in findings if finding.check_id.startswith("localization.")]
        self.assertTrue(relevant)
        self.assertFalse([finding for finding in relevant if finding.verdict in ("FAIL", "BLOCKED")], relevant)

    def test_browser_qa_localization_catches_pseudo_and_rtl_runtime_failures(self) -> None:
        plan = browser_localization_plan()
        plan["localization"]["pseudo_localization"] = {"enabled": True, "minimum_ratio": 1.3}
        plan["localization"]["rtl"] = {"required": True}
        plan["routes"][0]["direction"] = "rtl"
        obs = browser_localization_observation(
            html_dir="ltr",
            rtl_layout_direction="ltr",
            text_expansion_ratio=1.05,
            text_overflow_refs=["cta.submit"],
            rtl_icon_mirror_policy="MIRROR_DIRECTIONAL_ONLY",
        )
        findings = {finding.check_id: finding for finding in evaluate(obs, plan)}
        self.assertEqual(findings["localization.text-expansion"].verdict, "FAIL")
        self.assertEqual(findings["localization.rtl-direction"].verdict, "FAIL")

    def test_browser_qa_localization_missing_observation_is_blocked(self) -> None:
        obs = PageObservation(route="/es-mx/about", viewport=390, engine="simulation", browser="simulation")
        findings = evaluate(obs, browser_localization_plan())
        blocked = {finding.check_id: finding for finding in findings if finding.check_id.startswith("localization.")}
        self.assertEqual(blocked["localization.observation"].verdict, "BLOCKED")

    def test_browser_qa_simulation_engine_materializes_localization_facts(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-v214-browser-fixture-") as directory:
            fixture = Path(directory) / "es-mx-about"
            fixture.mkdir()
            (fixture / "index.html").write_text(
                "<!doctype html><html lang='es-MX'><head><title>Sobre</title></head>"
                "<body><main><h1>Sobre</h1></main></body></html>",
                encoding="utf-8",
            )
            (fixture / "qa-fixture.json").write_text(json.dumps({
                "localization": {
                    "locale": "es-MX",
                    "html_lang": "es-MX",
                    "html_dir": "ltr",
                    "route_resolves": True,
                    "switcher_present": True,
                    "switcher_accessible": True,
                    "switcher_keyboard_operable": True,
                    "switcher_labels": ["English", "Español"],
                    "switcher_current_locale": "es-MX",
                    "equivalent_route": "/about",
                    "hreflang": [
                        {"hreflang": "en-US", "reciprocal": True},
                        {"hreflang": "es-MX", "reciprocal": True},
                    ],
                    "canonical": "https://example.test/es-mx/about",
                    "canonical_is_self": True,
                    "localized_title": True,
                    "localized_description": True,
                    "localized_og": True,
                    "localized_alt": True,
                    "fallback_explicit": True,
                    "fallback_locale": "en-US",
                    "localized_form_labels": True,
                    "localized_form_errors": True,
                    "text_expansion_ratio": 1.35,
                }
            }), encoding="utf-8")
            plan = browser_localization_plan()
            plan["routes"][0]["path"] = "es-mx-about"
            observations = load_engine("simulation", directory).observe("es-mx-about", 390)
            findings = evaluate(observations, plan)
            relevant = [finding for finding in findings if finding.check_id.startswith("localization.")]
            self.assertFalse([finding for finding in relevant if finding.verdict in ("FAIL", "BLOCKED")], relevant)

    def test_ae_framework_rejects_a_sixth_owner_lock(self) -> None:
        profile = {"locks": {name: False for name in framework_validator.CANONICAL_LOCKS}}
        profile["locks"]["localization_locked"] = False
        self.assertIn("OWNER_LOCK_INVARIANT", framework_validator.validate_owner_locks(profile))

    def test_af_frozen_integrity_guard_records_mutation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-v214-mutation-") as directory:
            root = Path(directory)
            project_file = root / "projects" / "fixture.txt"
            project_file.parent.mkdir(parents=True)
            project_file.write_text("before", encoding="utf-8")
            guard = FrozenIntegrityGuard(str(root), protected_paths=["projects/"], ledger_path="violations.log", run_id="scenario-af").snapshot()
            project_file.write_text("after", encoding="utf-8")
            result = guard.verify(record_violation=True)
            self.assertFalse(result.ok)
            self.assertIn("projects/fixture.txt", result.mutations)
            self.assertTrue(Path(result.ledger_path).is_file())

    def test_negative_missing_fallback_policy_is_blocked(self) -> None:
        registry = valid_registry()
        registry.pop("fallback_policy")
        report = validator.validate_locale_registry(registry)
        self.assert_not_pass(report, "FALLBACK_POLICY_MISSING")

    def test_negative_accessibility_flag_only_selector_fails(self) -> None:
        report = validator.validate_accessibility_integration({"flag_only_selector": True})
        self.assert_not_pass(report, "FLAG_ONLY_LOCALE_SELECTOR")

    def test_negative_duplicate_state_authority_fails(self) -> None:
        manifest = neutral_manifest()
        manifest["i18n"] = {"complete": False}
        report = validator.validate_localization_manifest(manifest)
        self.assert_not_pass(report, "DUPLICATE_LOCALIZATION_STATE")

    def test_negative_locale_authorities_cannot_disagree(self) -> None:
        manifest = valid_manifest()
        manifest["state"]["default_locale"] = "es-MX"
        report = validator.validate_localization_manifest(manifest)
        self.assert_not_pass(report, "LOCALIZATION_DEFAULT_LOCALE_CONFLICT")

    def test_negative_external_provider_requirement_is_blocked(self) -> None:
        manifest = valid_manifest()
        manifest["external_translation_provider_required"] = True
        report = validator.validate_localization_manifest(manifest)
        self.assert_not_pass(report, "EXTERNAL_TRANSLATION_PROVIDER_REQUIRED")

    def test_negative_nonlocalizable_field_cannot_be_translated(self) -> None:
        content_ops = valid_manifest()["content_ops"] | {"localizable_fields": ["title", "body", "stable_id"]}
        report = validator.validate_content_ops_integration(content_ops, content_model=valid_content_model())
        self.assert_not_pass(report, "NON_LOCALIZABLE_FIELD_TRANSLATED")

    def test_negative_locale_state_cannot_create_lock(self) -> None:
        state = valid_state()
        state["localization_locked"] = False
        report = validator.validate_localization_state(state)
        self.assert_not_pass(report, "LOCALIZATION_LOCK_FORBIDDEN")

    def test_negative_required_ui_translation_coverage_fails(self) -> None:
        report = validator.validate_ui_strings([{
            "message_id": "nav.primary_label",
            "source_message": "Primary navigation",
            "translations": {"en-US": "Primary navigation"},
        }], required_locales=["en-US", "es-MX"])
        self.assert_not_pass(report, "UI_TRANSLATION_MISSING")

    def test_negative_malformed_analytics_integration_is_blocked(self) -> None:
        report = validator.validate_analytics_locale([])
        self.assert_not_pass(report, "ANALYTICS_INTEGRATION_MISSING")

    def test_negative_localized_slug_requires_explicit_301_status(self) -> None:
        report = validator.validate_localized_slugs([{
            "slug_id": "about-es",
            "locale": "es-MX",
            "slug": "/es-mx/acerca-de",
            "previous_slug": "/es-mx/about",
            "redirect_ref": "redirect-record",
            "redirect_status": 302,
            "published": True,
        }])
        self.assert_not_pass(report, "LOCALIZED_SLUG_REDIRECT_MISSING")

    def test_negative_unreviewed_status_contradiction_cannot_publish(self) -> None:
        report = validator.validate_translation_record(valid_translation(
            status="REVIEWED",
            review_status="NOT_REVIEWED",
            published=True,
        ))
        self.assert_not_pass(report, "UNREVIEWED_TRANSLATION_PUBLISHED")

    def test_negative_malformed_accessibility_switcher_requirement_fails_closed(self) -> None:
        report = validator.validate_accessibility_integration({
            "locale_switcher_required": "yes",
            "locale_switcher_accessible": False,
        })
        self.assert_not_pass(report, "BOOLEAN_FIELD_INVALID")
        self.assert_code(report, "LOCALE_SWITCHER_INACCESSIBLE")

    def test_browser_observation_defaults_fail_closed(self) -> None:
        obs = PageObservation(route="/es-mx/about", viewport=390, engine="simulation", browser="simulation")
        obs.localization = LocalizationObservation()
        findings = evaluate(obs, browser_localization_plan())
        relevant = {finding.check_id: finding for finding in findings if finding.check_id.startswith("localization.")}
        self.assertEqual(relevant["localization.route-resolves"].verdict, "FAIL")
        self.assertEqual(relevant["localization.metadata-title"].verdict, "FAIL")
        self.assertEqual(relevant["localization.fallback-explicit"].verdict, "FAIL")

    def test_subdomain_hreflang_preserves_host_identity(self) -> None:
        pages = [
            {
                "page_id": "about-en",
                "content_id": "about",
                "locale": "en-US",
                "url": "https://en.example.test/about",
                "canonical": "https://en.example.test/about",
                "html_lang": "en-US",
                "title": "About",
                "hreflang_required": True,
                "hreflang": [
                    {"hreflang": "en-US", "href": "https://en.example.test/about"},
                    {"hreflang": "es-MX", "href": "https://es.example.test/about"},
                ],
            },
            {
                "page_id": "about-es",
                "content_id": "about",
                "locale": "es-MX",
                "url": "https://es.example.test/about",
                "canonical": "https://es.example.test/about",
                "html_lang": "es-MX",
                "title": "Acerca de",
                "hreflang_required": True,
                "hreflang": [
                    {"hreflang": "en-US", "href": "https://en.example.test/about"},
                    {"hreflang": "es-MX", "href": "https://es.example.test/about"},
                ],
            },
        ]
        report = validator.validate_hreflang(pages, source_locale="en-US")
        self.assertEqual(report["status"], "PASS", report)


if __name__ == "__main__":
    unittest.main()
