"""Capability #10 conditional application architecture A-AV controls."""

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

from application import validator  # noqa: E402
from framework_validation import validator as framework_validator  # noqa: E402
from assertions import evaluate  # noqa: E402
from engine.base import ApplicationObservation, PageObservation  # noqa: E402
from guards.frozen_integrity_guard import FrozenIntegrityGuard  # noqa: E402


SCENARIO_IDS = tuple(chr(code) for code in range(ord("A"), ord("Z") + 1)) + (
    "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV"
)


def _registry() -> dict:
    with (ROOT / "templates/application-module-registry.json").open(encoding="utf-8") as fh:
        return json.load(fh)


def _state(required: bool, modules: list[str], classifications: list[str]) -> dict:
    return {
        "required": required,
        "complete": False,
        "status": "REQUIRED" if required else "NOT_REQUIRED",
        "classifications": classifications,
        "modules_required": modules,
        "modules_ready": [],
        "authentication_required": "AUTHENTICATION" in modules,
        "commerce_required": bool(set(modules) & {"CATALOG", "CART", "CHECKOUT", "PAYMENT", "ORDER_MANAGEMENT", "SUBSCRIPTION"}),
        "database_required": "DATABASE" in modules,
        "external_integrations": [],
        "high_risk_operations": [],
        "implementation_verified": False,
        "production_verified": False,
        "blocked_reason": None,
        "exception": {"applied": False, "reason": None},
    }


def _authentication() -> dict:
    return {
        "password": {"hash_algorithm": "ARGON2ID", "plaintext": False},
        "recovery": {"defined": True, "single_use": True, "expires": True, "user_enumeration": False},
        "session": {"secure_cookie": True, "http_only": True, "same_site": True, "rotation": True},
        "provider_required": False,
        "provider_available": True,
        "mfa_required": False,
    }


def _authorization() -> dict:
    return {
        "server_enforced": True,
        "client_role_trusted": False,
        "object_access_required": True,
        "object_level_enforced": True,
        "roles_required": True,
        "roles": ["USER", "ADMIN"],
        "default_allow": False,
        "admin_route_required": False,
        "admin_route_server_protected": True,
    }


def _dashboard() -> dict:
    modules = ["AUTHENTICATION", "AUTHORIZATION", "DATABASE", "API"]
    app = _state(True, modules, ["AUTHENTICATED_APP"])
    app.update({
        "user_stories": [{"story_id": "S-DASH", "auth_required": True, "state_change": True}],
        "actors": [{"actor_id": "user", "trust_boundary": "browser-to-server"}],
        "authentication": _authentication(),
        "authorization": _authorization(),
        "database": {"migrations_defined": True, "backup_recovery_defined": True, "transactions_required": True, "transactions_defined": True},
        "api": {"input_validation": True, "output_allowlist": True, "error_contract": True, "rate_limiting": True},
        "measurement": {},
        "seo": {"private_route_indexable": False},
        "provider_available": True,
        "live_payment_attempted": False,
        "live_user_created": False,
    })
    return {"application": app}


def _ecommerce() -> dict:
    modules = ["DATABASE", "API", "CATALOG", "CART", "CHECKOUT", "PAYMENT", "ORDER_MANAGEMENT", "WEBHOOKS"]
    app = _state(True, modules, ["ECOMMERCE"])
    app.update({
        "user_stories": [{"story_id": "S-PURCHASE", "purchase": True, "state_change": True}],
        "actors": [{"actor_id": "buyer", "trust_boundary": "browser-to-server"}],
        "database": {"migrations_defined": True, "backup_recovery_defined": True, "transactions_required": True, "transactions_defined": True},
        "api": {"input_validation": True, "output_allowlist": True, "error_contract": True, "rate_limiting": True},
        "commerce": {
            "checkout_required": True,
            "price": {"authority": "SERVER", "canonical_price_verified": True},
            "checkout_click_marks_paid": False,
            "payment_confirmation_source": "WEBHOOK",
            "product_type": "DIGITAL",
            "shipping": {"required": False},
            "payment": {
                "provider_available": True,
                "hosted_or_tokenized": True,
                "raw_card_stored": False,
                "statuses": ["REQUIRES_PAYMENT", "PROCESSING", "SUCCEEDED", "FAILED", "CANCELED", "REFUNDED"],
            },
            "order": {"statuses": ["DRAFT", "PENDING_PAYMENT", "PAID", "FULFILLING", "FULFILLED", "CANCELED", "REFUNDED"]},
            "webhook": {"signature_verified": True, "idempotent": True, "duplicate_side_effect_created": False},
        },
        "measurement": {"purchase_event_required": True, "purchase_event_authoritative": True, "purchase_event_from_click": False},
        "seo": {"private_route_indexable": False},
        "provider_available": True,
        "live_payment_attempted": False,
        "live_user_created": False,
    })
    return {"application": app}


def _subscription() -> dict:
    manifest = _ecommerce()
    app = manifest["application"]
    app["modules_required"] += ["AUTHENTICATION", "AUTHORIZATION", "SUBSCRIPTION", "ENTITLEMENT"]
    app["authentication_required"] = True
    app["authentication"] = _authentication()
    app["authorization"] = _authorization()
    app["subscription"] = {"entitlements_separate": True, "cancellation_defined": True, "payment_failed_entitlement_active": False}
    app["classifications"] = ["SUBSCRIPTION_COMMERCE", "AUTHENTICATED_APP"]
    return manifest


def _booking() -> dict:
    manifest = _dashboard()
    app = manifest["application"]
    app["modules_required"] = ["DATABASE", "API", "BOOKING"]
    app["authentication_required"] = False
    app["booking"] = {"overlap_prevented": True, "timezone": "America/Denver"}
    app["classifications"] = ["BOOKING"]
    return manifest


def _uploads() -> dict:
    manifest = _dashboard()
    app = manifest["application"]
    app["modules_required"] = ["AUTHENTICATION", "AUTHORIZATION", "DATABASE", "API", "STORAGE", "FILE_UPLOAD"]
    app["uploads"] = {"allowlist_enforced": True, "executable_upload_accepted": False, "private_required": True, "private_storage_authorized": True, "private_file_public": False}
    app["classifications"] = ["AUTHENTICATED_APP"]
    return manifest


def _ugc() -> dict:
    manifest = _dashboard()
    app = manifest["application"]
    app["modules_required"] = ["AUTHENTICATION", "AUTHORIZATION", "DATABASE", "API", "USER_GENERATED_CONTENT"]
    app["user_generated_content"] = {"sanitized": True, "script_executed": False}
    app["classifications"] = ["COMMUNITY", "USER_GENERATED_CONTENT", "AUTHENTICATED_APP"]
    return manifest


def _email() -> dict:
    manifest = _dashboard()
    app = manifest["application"]
    app["modules_required"] = ["DATABASE", "API", "TRANSACTIONAL_EMAIL"]
    app["messaging"] = {"required": True, "delivery_status_observable": True, "failure_reported_as_success": False}
    app["classifications"] = ["LEAD_GENERATION"]
    return manifest


def _integration() -> dict:
    manifest = _dashboard()
    app = manifest["application"]
    app["modules_required"] = ["DATABASE", "API", "THIRD_PARTY_INTEGRATION"]
    app["integrations"] = {"inventory_complete": True, "unknown_integrations": [], "secret_exposed_client": False}
    app["classifications"] = ["AUTHENTICATED_APP"]
    return manifest


def _validate(manifest: dict) -> dict:
    return validator.validate_application_architecture(manifest, module_registry=_registry())


class ApplicationArchitectureScenarios(unittest.TestCase):
    def test_scenario_ids_are_complete(self):
        self.assertEqual(len(SCENARIO_IDS), 48)
        self.assertEqual(SCENARIO_IDS[-1], "AV")

    def test_A_static_marketing_has_no_infrastructure(self):
        app = _state(False, [], ["STATIC_MARKETING"])
        self.assertTrue(_validate({"application": app})["ok"])

    def test_B_public_blog_has_no_application_modules(self):
        app = _state(False, [], ["CONTENT_PUBLISHER"])
        app["user_stories"] = [{"story_id": "BLOG", "public_content": True}]
        self.assertTrue(_validate({"application": app})["ok"])

    def test_C_dashboard_auth_authorization_and_data_pass(self):
        self.assertTrue(_validate(_dashboard())["ok"])

    def test_D_missing_authorization_fails(self):
        manifest = _dashboard(); manifest["application"]["authorization"]["server_enforced"] = False
        self.assertFalse(_validate(manifest)["ok"])

    def test_E_object_access_fails(self):
        manifest = _dashboard(); manifest["application"]["authorization"]["object_level_enforced"] = False
        self.assertFalse(_validate(manifest)["ok"])

    def test_F_client_role_trust_fails(self):
        manifest = _dashboard(); manifest["application"]["authorization"]["client_role_trusted"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_G_plaintext_password_fails(self):
        manifest = _dashboard(); manifest["application"]["authentication"]["password"]["plaintext"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_H_exposed_hash_fails(self):
        manifest = _dashboard(); manifest["application"]["authentication"]["password_hash_exposed"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_I_missing_recovery_fails(self):
        manifest = _dashboard(); manifest["application"]["authentication"]["recovery"]["defined"] = False
        self.assertFalse(_validate(manifest)["ok"])

    def test_J_hidden_admin_route_fails(self):
        manifest = _dashboard(); manifest["application"]["modules_required"].append("ADMIN_INTERFACE")
        manifest["application"]["authorization"]["admin_route_required"] = True
        manifest["application"]["authorization"]["admin_route_server_protected"] = False
        self.assertFalse(_validate(manifest)["ok"])

    def test_K_valid_ecommerce_passes(self):
        self.assertTrue(_validate(_ecommerce())["ok"])

    def test_L_client_price_trust_fails(self):
        manifest = _ecommerce(); manifest["application"]["commerce"]["price"]["authority"] = "CLIENT"
        self.assertFalse(_validate(manifest)["ok"])

    def test_M_checkout_button_paid_fails(self):
        manifest = _ecommerce(); manifest["application"]["commerce"]["checkout_click_marks_paid"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_N_success_without_confirmation_fails(self):
        manifest = _ecommerce(); manifest["application"]["commerce"]["success_route_without_payment_confirmation"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_O_verified_webhook_passes(self):
        self.assertTrue(_validate(_ecommerce())["ok"])

    def test_P_missing_webhook_signature_fails(self):
        manifest = _ecommerce(); manifest["application"]["commerce"]["webhook"]["signature_verified"] = False
        self.assertFalse(_validate(manifest)["ok"])

    def test_Q_duplicate_webhook_side_effect_fails(self):
        manifest = _ecommerce(); manifest["application"]["commerce"]["webhook"]["duplicate_side_effect_created"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_R_idempotent_duplicate_passes(self):
        self.assertTrue(_validate(_ecommerce())["ok"])

    def test_S_raw_card_storage_fails(self):
        manifest = _ecommerce(); manifest["application"]["commerce"]["payment"]["raw_card_stored"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_T_hosted_tokenized_payment_passes(self):
        self.assertTrue(_validate(_ecommerce())["ok"])

    def test_U_subscription_entitlement_passes(self):
        self.assertTrue(_validate(_subscription())["ok"])

    def test_V_failed_payment_entitlement_active_fails(self):
        manifest = _subscription(); manifest["application"]["subscription"]["payment_failed_entitlement_active"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_W_digital_shipping_bloat_fails(self):
        manifest = _ecommerce(); manifest["application"]["commerce"]["shipping"]["required"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_X_physical_goods_without_shipping_fails(self):
        manifest = _ecommerce(); manifest["application"]["commerce"]["product_type"] = "PHYSICAL"
        self.assertFalse(_validate(manifest)["ok"])

    def test_Y_overlapping_booking_fails(self):
        manifest = _booking(); manifest["application"]["booking"]["overlap_prevented"] = False
        self.assertFalse(_validate(manifest)["ok"])

    def test_Z_ambiguous_timezone_fails(self):
        manifest = _booking(); manifest["application"]["booking"]["timezone"] = "LOCAL"
        self.assertFalse(_validate(manifest)["ok"])

    def test_AA_executable_upload_fails(self):
        manifest = _uploads(); manifest["application"]["uploads"]["executable_upload_accepted"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_AB_private_upload_public_url_fails(self):
        manifest = _uploads(); manifest["application"]["uploads"]["private_file_public"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_AC_ugc_script_fails(self):
        manifest = _ugc(); manifest["application"]["user_generated_content"]["script_executed"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_AD_email_failure_reported_success_fails(self):
        manifest = _email(); manifest["application"]["messaging"]["failure_reported_as_success"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_AE_unknown_integration_fails(self):
        manifest = _integration(); manifest["application"]["integrations"]["unknown_integrations"] = ["unknown"]
        self.assertFalse(_validate(manifest)["ok"])

    def test_AF_client_secret_fails(self):
        manifest = _integration(); manifest["application"]["integrations"]["secret_exposed_client"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_AG_purchase_event_from_button_fails(self):
        manifest = _ecommerce(); manifest["application"]["measurement"]["purchase_event_from_click"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_AH_authoritative_purchase_passes(self):
        self.assertTrue(_validate(_ecommerce())["ok"])

    def test_AI_duplicate_spanish_event_fails(self):
        manifest = _dashboard(); manifest["application"]["measurement"] = {"duplicate_locale_events": True}
        self.assertFalse(_validate(manifest)["ok"])

    def test_AJ_canonical_locale_event_passes(self):
        manifest = _dashboard(); manifest["application"]["measurement"] = {"localized_measurement_required": True, "canonical_event_with_locale": True}
        self.assertTrue(_validate(manifest)["ok"])

    def test_AK_private_route_indexable_fails(self):
        manifest = _dashboard(); manifest["application"]["seo"]["private_route_indexable"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_AL_simple_marketing_forced_infrastructure_fails(self):
        app = _state(False, ["AUTHENTICATION"], ["STATIC_MARKETING"])
        self.assertFalse(_validate({"application": app})["ok"])

    def test_AM_live_payment_attempt_fails(self):
        manifest = _ecommerce(); manifest["application"]["live_payment_attempted"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_AN_real_user_attempt_fails(self):
        manifest = _dashboard(); manifest["application"]["live_user_created"] = True
        self.assertFalse(_validate(manifest)["ok"])

    def test_AO_sixth_lock_is_rejected(self):
        profile = {"locks": {name: False for name in framework_validator.CANONICAL_LOCKS}}
        profile["locks"]["application_locked"] = False
        self.assertIn("OWNER_LOCK_INVARIANT", framework_validator.validate_owner_locks(profile))

    def test_AP_application_locked_is_rejected(self):
        state = _state(False, [], ["STATIC_MARKETING"])
        state["application_locked"] = False
        result = validator.validate_application_state(state)
        self.assertFalse(result["ok"])

    def test_AQ_frozen_integrity_guard_detects_mutation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            protected = root / "projects" / "fixture.txt"
            protected.parent.mkdir()
            protected.write_text("before", encoding="utf-8")
            guard = FrozenIntegrityGuard(str(root), ["projects/"], ledger_path="ledger.log", run_id="AQ")
            guard.snapshot()
            protected.write_text("after", encoding="utf-8")
            result = guard.verify(record_violation=False)
            self.assertFalse(result.ok)
            self.assertEqual(result.mutations, ["projects/fixture.txt"])

    def test_AR_nonexistent_dependency_fails(self):
        registry = _registry()
        registry["modules"][0]["dependencies"] = ["DOES_NOT_EXIST"]
        self.assertFalse(validator.validate_module_registry(registry)["ok"])

    def test_dependency_cycle_fails(self):
        registry = _registry()
        registry["modules"][0]["dependencies"] = ["AUTHORIZATION"]
        registry["modules"][1]["dependencies"] = ["AUTHENTICATION"]
        self.assertFalse(validator.validate_module_registry(registry)["ok"])

    def test_AS_duplicate_module_fails(self):
        registry = _registry()
        registry["modules"].append(copy.deepcopy(registry["modules"][0]))
        self.assertFalse(validator.validate_module_registry(registry)["ok"])

    def test_full_profile_owner_locks_are_not_application_locks(self):
        with (ROOT / "templates/site-profile.json").open(encoding="utf-8") as fh:
            profile = json.load(fh)
        self.assertTrue(_validate(profile)["ok"])

    def test_missing_session_policy_fails(self):
        manifest = _dashboard()
        manifest["application"]["authentication"]["session"] = {}
        self.assertFalse(_validate(manifest)["ok"])

    def test_AT_missing_high_risk_verification_blocks(self):
        manifest = _dashboard(); manifest["application"]["high_risk_operations"] = [{"operation": "ADMIN_DELETE", "verification_complete": False}]
        result = _validate(manifest)
        self.assertEqual(result["status"], "BLOCKED")

    def test_AU_auth_provider_unavailable_blocks(self):
        manifest = _dashboard(); auth = manifest["application"]["authentication"]
        auth["provider_required"] = True; auth["provider_available"] = False
        result = _validate(manifest)
        self.assertEqual(result["status"], "BLOCKED")

    def test_AV_payment_provider_unavailable_blocks(self):
        manifest = _ecommerce(); manifest["application"]["commerce"]["payment"]["provider_available"] = False
        result = _validate(manifest)
        self.assertEqual(result["status"], "BLOCKED")


class ApplicationArchitectureBrowserQA(unittest.TestCase):
    def test_browser_qa_application_observation_passes_valid_ecommerce(self):
        observation = ApplicationObservation(
            authenticated=True,
            authorization_enforced=True,
            client_role_trusted=False,
            client_price_trusted=False,
            canonical_price_verified=True,
            checkout_click_marks_paid=False,
            payment_confirmed=True,
            webhook_signature_verified=True,
            webhook_idempotent=True,
            duplicate_side_effect_created=False,
            raw_card_stored=False,
            hosted_or_tokenized_payment=True,
            purchase_event_authoritative=True,
            purchase_event_from_click=False,
            provider_available=True,
            live_payment_attempted=False,
            live_user_created=False,
        )
        page = PageObservation(route="/checkout", viewport=390, engine="simulation", browser="simulation", application=observation)
        plan = {"application": {"required": True, "modules_required": ["PAYMENT", "WEBHOOKS"], "forbid_live_side_effects": True}}
        findings = evaluate(page, plan)
        self.assertTrue(findings)
        self.assertTrue(all(item.verdict == "PASS" for item in findings), findings)

    def test_browser_qa_missing_required_observation_blocks(self):
        page = PageObservation(route="/admin", viewport=390, engine="simulation", browser="simulation")
        plan = {"application": {"required": True, "modules_required": ["AUTHORIZATION"]}}
        findings = evaluate(page, plan)
        app_findings = [item for item in findings if item.check_id == "application.observation"]
        self.assertEqual(len(app_findings), 1)
        self.assertEqual(app_findings[0].verdict, "BLOCKED")


if __name__ == "__main__":
    unittest.main()
