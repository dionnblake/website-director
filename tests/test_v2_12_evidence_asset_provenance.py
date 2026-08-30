"""Capability 7 Evidence, Claim and Asset Provenance A-V controls plus W-AK fail-closed edges.

All records and mutation probes are synthetic. The suite never writes under
the repository projects/ directory and uses temporary files for hash checks.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "browser-qa"))

from guards.frozen_integrity_guard import FrozenIntegrityGuard
from framework_validation import validator as framework_validator
from provenance import validator


def source(source_id: str = "src-primary", source_type: str = "PRIMARY_SOURCE") -> dict[str, object]:
    return {
        "source_id": source_id,
        "source_type": source_type,
        "title": "Synthetic evidence record",
        "url_or_ref": "https://example.invalid/evidence/" + source_id,
        "source_date": "2026-08-01",
        "retrieved_date": "2026-08-02",
        "evidence_excerpt": "The synthetic record supports the exact proposition under test.",
    }


def claim(
    claim_id: str = "claim-001",
    *,
    claim_type: str = "QUANTITATIVE",
    source_ref: str = "src-primary",
    text: str = "87 percent of the synthetic cohort completed the test.",
) -> dict[str, object]:
    return {
        "claim_id": claim_id,
        "claim_text": text,
        "claim_type": claim_type,
        "route": "/",
        "component": "proof",
        "source_ref": source_ref,
        "source_type": "PRIMARY_SOURCE",
        "source_url_or_ref": "https://example.invalid/evidence/" + source_ref,
        "source_date": "2026-08-01",
        "verified_date": "2026-08-02",
        "evidence_strength": "PRIMARY_SOURCE",
        "owner": "Synthetic owner",
        "expiration_or_review_date": "2027-08-01",
        "disclosure_required": False,
        "evidence_ref": source_ref,
        "evidence_match": True,
        "claim_status": "SUPPORTED",
        "production_status": "PRODUCTION",
    }


def ledger() -> dict[str, object]:
    return {
        "schema_version": "2.12.0",
        "project_name": "Synthetic Capability 7 Fixture",
        "sources": [],
        "claims": [],
        "testimonials": [],
        "certifications": [],
        "research_references": [],
        "assets": [],
    }


def asset(
    asset_id: str,
    *,
    origin: str = "ORIGINAL_CREATED",
    path: str = "assets/output.bin",
    sha256: str | None = None,
    asset_type: str = "image",
    **extra: object,
) -> dict[str, object]:
    record: dict[str, object] = {
        "asset_id": asset_id,
        "file": path,
        "asset_type": asset_type,
        "origin": origin,
        "creator": "Synthetic creator",
        "owner": "Synthetic owner",
        "production_status": "PRODUCTION_APPROVED",
        "production_approved": True,
        "sha256": sha256,
        "authorized_uses": ["website"],
    }
    record.update(extra)
    return record


class EvidenceAssetProvenanceTests(unittest.TestCase):
    def assert_not_pass(self, result: dict[str, object], code: str | None = None) -> None:
        self.assertNotEqual(result["status"], "PASS")
        if code:
            self.assertIn(code, {issue["code"] for issue in result["issues"]})

    def test_a_supported_statistic_passes(self) -> None:
        data = ledger()
        data["sources"] = [source()]
        data["claims"] = [claim()]
        result = validator.validate_ledger(data, as_of="2026-08-30")
        self.assertEqual(result["status"], "PASS")

    def test_b_invented_statistic_fails_closed(self) -> None:
        data = ledger()
        invented = claim(source_ref="missing-source", text="99.9 percent of all customers prefer this.")
        invented["evidence_match"] = False
        data["claims"] = [invented]
        self.assert_not_pass(validator.validate_ledger(data), "EVIDENCE_REFERENCE_MISSING")

    def test_c_testimonial_without_source_or_authority_is_blocked(self) -> None:
        data = ledger()
        data["testimonials"] = [{
            "testimonial_id": "testimonial-001",
            "text": "Synthetic praise.",
            "production_status": "PRODUCTION",
            "production_approved": True,
            "consent_status": "GRANTED",
        }]
        self.assert_not_pass(validator.validate_ledger(data), "EVIDENCE_REQUIRED")

    def test_d_certification_without_issuer_is_blocked(self) -> None:
        data = ledger()
        data["certifications"] = [{
            "certification_id": "cert-001",
            "evidence_ref": "missing-cert-source",
            "validity": "2026",
            "authorized_display": True,
            "production_status": "PRODUCTION",
        }]
        self.assert_not_pass(validator.validate_ledger(data), "CERTIFICATION_FIELD_MISSING")

    def test_e_owner_provided_attested_asset_passes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-cap7-") as directory:
            root = Path(directory)
            output = root / "assets" / "owner.bin"
            output.parent.mkdir()
            output.write_bytes(b"owner-provided-fixture")
            data = ledger()
            data["assets"] = [asset(
                "asset-owner",
                path="assets/owner.bin",
                sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                origin="OWNER_PROVIDED",
                usage_authority="OWNER_ATTESTED",
            )]
            result = validator.validate_ledger(data, root=root)
            self.assertEqual(result["status"], "PASS")

    def test_f_research_reference_cannot_be_hero_asset(self) -> None:
        data = ledger()
        data["research_references"] = [{
            "reference_id": "ref-dribbble",
            "platform": "Dribbble",
            "source_url": "https://example.invalid/reference",
            "query": "synthetic editorial layouts",
            "retrieved_at": "2026-08-02T00:00:00Z",
            "reference_purpose": "pattern study",
            "grade": "A",
            "pattern_to_learn": "editorial pacing",
            "what_not_to_copy": "brand imagery",
            "upstream_sha256": "a" * 64,
            "reference_only": True,
            "production_status": "PRODUCTION_READY",
        }]
        self.assert_not_pass(validator.validate_ledger(data), "RESEARCH_REFERENCE_PROMOTION")

    def test_g_screenshot_reference_cannot_be_promoted(self) -> None:
        data = ledger()
        data["assets"] = [asset("asset-screenshot", origin="SCREENSHOT_REFERENCE")]
        self.assert_not_pass(validator.validate_ledger(data), "REFERENCE_ASSET_PROMOTION")

    def test_h_licensed_stock_with_license_evidence_passes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-cap7-") as directory:
            root = Path(directory)
            output = root / "stock.jpg"
            output.write_bytes(b"licensed-stock-fixture")
            data = ledger()
            data["sources"] = [source("src-stock-license", "PRIMARY_SOURCE")]
            data["assets"] = [asset(
                "asset-stock",
                origin="LICENSED_STOCK",
                path="stock.jpg",
                sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                provider="Synthetic stock provider",
                source_url="https://example.invalid/stock/license",
                license="Synthetic commercial stock license",
                license_evidence_ref="src-stock-license",
                authorized_uses=["website", "marketing"],
            )]
            self.assertEqual(validator.validate_ledger(data, root=root)["status"], "PASS")

    def test_i_stock_without_license_is_blocked(self) -> None:
        data = ledger()
        data["assets"] = [asset("asset-stock-unknown", origin="LICENSED_STOCK")]
        self.assert_not_pass(validator.validate_ledger(data), "LICENSE_IDENTITY_MISSING")

    def test_j_font_without_license_is_blocked(self) -> None:
        data = ledger()
        data["assets"] = [asset("asset-font-unknown", asset_type="font")]
        self.assert_not_pass(validator.validate_ledger(data), "FONT_LICENSE_MISSING")

    def test_k_open_license_font_with_evidence_passes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-cap7-") as directory:
            root = Path(directory)
            output = root / "font.woff2"
            output.write_bytes(b"open-license-font-fixture")
            data = ledger()
            data["sources"] = [source("src-font-license", "PRIMARY_SOURCE")]
            data["assets"] = [asset(
                "asset-font-open",
                origin="OPEN_LICENSE",
                asset_type="font",
                path="font.woff2",
                sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                license="OFL-1.1 synthetic record",
                license_evidence_ref="src-font-license",
                authorized_uses=["website"],
            )]
            self.assertEqual(validator.validate_ledger(data, root=root)["status"], "PASS")

    def test_l_partner_logo_without_authorization_requires_review(self) -> None:
        data = ledger()
        data["assets"] = [asset(
            "asset-partner-logo",
            origin="THIRD_PARTY_BRAND",
            mark_owner="Synthetic partner",
            authorization_status="UNKNOWN",
        )]
        self.assert_not_pass(validator.validate_ledger(data), "BRAND_AUTHORIZATION_REVIEW_REQUIRED")

    def test_m_ai_media_metadata_and_hash_pass(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-cap7-") as directory:
            root = Path(directory)
            output = root / "ai-image.png"
            output.write_bytes(b"ai-generated-fixture")
            data = ledger()
            data["assets"] = [asset(
                "asset-ai",
                origin="AI_GENERATED",
                path="ai-image.png",
                sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                provider="Synthetic image tool",
                generation_date="2026-08-02",
                source_inputs=[],
            )]
            self.assertEqual(validator.validate_ledger(data, root=root)["status"], "PASS")

    def test_n_ai_rights_assertion_is_rejected(self) -> None:
        data = ledger()
        data["assets"] = [asset(
            "asset-ai-assertion",
            origin="AI_GENERATED",
            provider="Synthetic image tool",
            generation_date="2026-08-02",
            source_inputs=[],
            copyright_cleared=True,
        )]
        self.assert_not_pass(validator.validate_ledger(data), "UNSUPPORTED_LEGAL_ASSERTION")

    def test_o_changed_asset_hash_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-cap7-") as directory:
            root = Path(directory)
            output = root / "changed.bin"
            output.write_bytes(b"original")
            expected = hashlib.sha256(output.read_bytes()).hexdigest()
            output.write_bytes(b"changed")
            data = ledger()
            data["assets"] = [asset("asset-changed", path="changed.bin", sha256=expected)]
            self.assert_not_pass(validator.validate_ledger(data, root=root), "ASSET_HASH_MISMATCH")

    def test_p_required_attribution_cannot_be_omitted(self) -> None:
        data = ledger()
        data["sources"] = [source("src-attribution")]
        data["assets"] = [asset(
            "asset-attribution",
            origin="LICENSED_STOCK",
            license="Synthetic license",
            license_evidence_ref="src-attribution",
            authorized_uses=["website"],
            attribution_required=True,
        )]
        self.assert_not_pass(validator.validate_ledger(data), "ATTRIBUTION_MISSING")

    def test_q_affiliate_merchant_performance_claim_requires_classification(self) -> None:
        data = ledger()
        data["sources"] = [source()]
        affiliate = claim(claim_type="AFFILIATE_PRODUCT", text="This merchant product improves performance.")
        affiliate["affiliate"] = True
        data["claims"] = [affiliate]
        self.assert_not_pass(validator.validate_ledger(data), "AFFILIATE_ORIGIN_UNCLASSIFIED")

    def test_r_expired_claim_is_blocked(self) -> None:
        data = ledger()
        data["sources"] = [source()]
        expired = claim()
        expired["expiration_or_review_date"] = "2026-01-01"
        data["claims"] = [expired]
        self.assert_not_pass(validator.validate_ledger(data, as_of="2026-08-30"), "CLAIM_EXPIRED")

    def test_s_duplicate_provenance_id_fails(self) -> None:
        data = ledger()
        data["sources"] = [source("duplicate-id")]
        data["claims"] = [claim(claim_id="duplicate-id", source_ref="duplicate-id")]
        self.assert_not_pass(validator.validate_ledger(data), "DUPLICATE_PROVENANCE_ID")

    def test_t_production_manifest_requires_provenance_ref(self) -> None:
        result = validator.validate_asset_manifest(
            {"assets": [{"asset_id": "asset-production", "status": "PRODUCTION_READY"}]},
            ledger(),
        )
        self.assert_not_pass(result, "MISSING_PRODUCTION_PROVENANCE_REF")

    def test_u_sixth_owner_lock_remains_forbidden(self) -> None:
        profile = json.loads((ROOT / "templates/site-profile.json").read_text(encoding="utf-8"))
        profile["locks"]["provenance_locked"] = False
        self.assertIn("OWNER_LOCK_INVARIANT", framework_validator.validate_owner_locks(profile))
        self.assertEqual(len(profile["locks"]) - 1, 5)

    def test_v_frozen_fixture_mutation_guard_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-cap7-frozen-") as directory:
            root = Path(directory)
            frozen = root / "projects" / "fixture" / "state.json"
            frozen.parent.mkdir(parents=True)
            frozen.write_text("baseline", encoding="utf-8")
            guard = FrozenIntegrityGuard(
                str(root),
                protected_paths=["projects/"],
                ledger_path="runtime/violations.log",
                run_id="cap7-negative-control",
            ).snapshot()
            frozen.write_text("mutated", encoding="utf-8")
            result = guard.verify()
            self.assertFalse(result.ok)
            self.assertEqual(result.mutations, ["projects/fixture/state.json"])

    def test_current_capability_wiring_and_neutral_state(self) -> None:
        profile = json.loads((ROOT / "templates/site-profile.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas/evidence-ledger.schema.json").read_text(encoding="utf-8"))
        protocols = json.loads((ROOT / "schemas/protocols.json").read_text(encoding="utf-8"))
        gates = json.loads((ROOT / "schemas/gates.json").read_text(encoding="utf-8"))
        phases = json.loads((ROOT / "schemas/phases.json").read_text(encoding="utf-8"))
        self.assertEqual(profile["schema_version"], "2.13.0")
        self.assertFalse(profile["provenance"]["complete"])
        self.assertEqual(schema["$id"], "https://website-director.local/schemas/evidence-ledger.schema.json")
        self.assertTrue(any(item["id"] == "EVIDENCE_PROVENANCE" for item in protocols["protocols"]))
        self.assertTrue(any(item["name"] == "EVIDENCE_PROVENANCE_READY" and item["type"] == "READINESS" for item in gates["gates"]))
        self.assertTrue(any(item["phase"] == "6.95" for item in phases["phases"]))
        self.assertEqual(len(profile["locks"]), 5)

    def test_complete_state_requires_passing_ledger_and_no_unresolved_items(self) -> None:
        passing = validator.validate_provenance_state({
            "complete": True,
            "ledger_ref": "evidence-ledger.json",
            "claim_inventory_complete": True,
            "asset_inventory_complete": True,
            "research_reference_inventory_complete": True,
            "license_review_complete": True,
            "attribution_review_complete": True,
            "unresolved_items": [],
            "high_risk_items": [],
        }, ledger_result={"status": "PASS", "ledger_ref": "evidence-ledger.json"})
        self.assertEqual(passing["status"], "PASS")
        blocked = validator.validate_provenance_state({
            "complete": True,
            "ledger_ref": "evidence-ledger.json",
            "claim_inventory_complete": True,
            "asset_inventory_complete": True,
            "research_reference_inventory_complete": True,
            "license_review_complete": True,
            "attribution_review_complete": True,
            "unresolved_items": ["asset-unknown"],
            "high_risk_items": [],
        }, ledger_result={"status": "PASS", "ledger_ref": "evidence-ledger.json"})
        self.assert_not_pass(blocked, "PROVENANCE_UNRESOLVED_ITEMS")

    def test_provenance_state_cannot_create_a_lock(self) -> None:
        result = validator.validate_provenance_state({"complete": False, "provenance_locked": False})
        self.assert_not_pass(result, "PROVENANCE_LOCK_FORBIDDEN")

    def test_manifest_reference_resolves_to_ledger_asset(self) -> None:
        data = ledger()
        data["assets"] = [asset("asset-linked", origin="ORIGINAL_CREATED")]
        result = validator.validate_asset_manifest(
            {"assets": [{
                "asset_id": "asset-linked",
                "status": "PRODUCTION_READY",
                "provenance_ref": "asset-linked",
            }]},
            data,
        )
        self.assertEqual(result["status"], "PASS")

    def test_w_complete_state_requires_a_validated_ledger_result(self) -> None:
        result = validator.validate_provenance_state({
            "complete": True,
            "ledger_ref": "evidence-ledger.json",
            "claim_inventory_complete": True,
            "asset_inventory_complete": True,
            "research_reference_inventory_complete": True,
            "license_review_complete": True,
            "attribution_review_complete": True,
        })
        self.assert_not_pass(result, "PROVENANCE_LEDGER_RESULT_MISSING")

    def test_x_unknown_validation_mode_fails_closed(self) -> None:
        result = validator.validate_ledger(ledger(), mode="invented-mode")
        self.assert_not_pass(result, "VALIDATION_MODE_INVALID")

    def test_y_contradictory_production_approval_is_rejected(self) -> None:
        data = ledger()
        data["assets"] = [asset("asset-conflict", production_status="PRODUCTION", production_approved=False)]
        self.assert_not_pass(validator.validate_ledger(data), "PRODUCTION_STATUS_CONFLICT")

    def test_z_unverified_source_cannot_be_overstated_as_primary(self) -> None:
        data = ledger()
        unverified = source()
        unverified["source_type"] = "UNVERIFIED"
        data["sources"] = [unverified]
        overstated = claim(source_ref="src-primary")
        overstated["source_type"] = "PRIMARY_SOURCE"
        data["claims"] = [overstated]
        self.assert_not_pass(validator.validate_ledger(data), "SOURCE_TYPE_CONFLICT")

    def test_aa_explicit_false_evidence_match_overrides_excerpt(self) -> None:
        data = ledger()
        data["sources"] = [source()]
        contradicted = claim()
        contradicted["evidence_match"] = False
        data["claims"] = [contradicted]
        self.assert_not_pass(validator.validate_ledger(data), "CLAIM_EVIDENCE_CONTRADICTION")

    def test_ab_time_sensitive_claim_requires_freshness_date(self) -> None:
        data = ledger()
        data["sources"] = [source()]
        current_stat = claim()
        current_stat.pop("expiration_or_review_date")
        data["claims"] = [current_stat]
        self.assert_not_pass(validator.validate_ledger(data), "CLAIM_FRESHNESS_MISSING")

    def test_ac_source_url_is_not_license_evidence(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-cap7-") as directory:
            root = Path(directory)
            output = root / "stock.jpg"
            output.write_bytes(b"stock-without-license-record")
            data = ledger()
            data["assets"] = [asset(
                "asset-stock-no-license-ref",
                origin="LICENSED_STOCK",
                path="stock.jpg",
                sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                provider="Synthetic stock provider",
                source_url="https://example.invalid/stock/asset",
                license="Synthetic stock license name",
                authorized_uses=["website"],
            )]
            self.assert_not_pass(validator.validate_ledger(data, root=root), "LICENSE_EVIDENCE_MISSING")

    def test_ad_production_hash_requires_a_validation_root(self) -> None:
        data = ledger()
        data["assets"] = [asset("asset-hash-unverified", sha256="a" * 64)]
        self.assert_not_pass(validator.validate_ledger(data), "ASSET_HASH_VALIDATION_UNAVAILABLE")

    def test_ae_empty_production_testimonial_is_blocked(self) -> None:
        data = ledger()
        data["sources"] = [source("src-testimonial")]
        data["testimonials"] = [{
            "testimonial_id": "testimonial-empty",
            "source_ref": "src-testimonial",
            "authority": "Synthetic customer",
            "consent_status": "GRANTED",
            "quote_status": "VERIFIED",
            "date": "2026-08-01",
            "production_status": "PRODUCTION",
            "production_approved": True,
        }]
        self.assert_not_pass(validator.validate_ledger(data), "TESTIMONIAL_FIELD_MISSING")

    def test_af_prototype_exception_cannot_mask_production_status(self) -> None:
        data = ledger()
        data["assets"] = [asset(
            "asset-exception-conflict",
            production_status="PRODUCTION",
            production_approved=False,
            exception={"applied": True, "reason": "internal prototype"},
        )]
        self.assert_not_pass(validator.validate_ledger(data), "PRODUCTION_STATUS_CONFLICT")

    def test_ag_direct_url_cannot_bypass_source_register(self) -> None:
        data = ledger()
        direct_url_claim = claim(source_ref="https://example.invalid/unregistered-source")
        data["claims"] = [direct_url_claim]
        self.assert_not_pass(validator.validate_ledger(data), "EVIDENCE_REFERENCE_MISSING")

    def test_ah_free_text_license_evidence_cannot_pass(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-cap7-") as directory:
            root = Path(directory)
            output = root / "stock.jpg"
            output.write_bytes(b"stock-with-free-text-license")
            data = ledger()
            data["assets"] = [asset(
                "asset-free-text-license",
                origin="LICENSED_STOCK",
                path="stock.jpg",
                sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                provider="Synthetic stock provider",
                source_url="https://example.invalid/stock/asset",
                license="Synthetic stock license name",
                license_evidence="terms checked by owner",
                authorized_uses=["website"],
            )]
            self.assert_not_pass(validator.validate_ledger(data, root=root), "LICENSE_EVIDENCE_MISSING")

    def test_ai_active_certification_passes_with_registered_evidence(self) -> None:
        data = ledger()
        data["sources"] = [source("src-certification")]
        data["certifications"] = [{
            "certification_id": "cert-active",
            "issuer": "Synthetic certifying body",
            "status": "ACTIVE",
            "evidence_ref": "src-certification",
            "validity": "2026",
            "valid_until": "2027-12-31",
            "authorized_display": True,
            "production_status": "PRODUCTION",
        }]
        self.assertEqual(validator.validate_ledger(data, as_of="2026-08-30")["status"], "PASS")

    def test_aj_revoked_certification_is_blocked(self) -> None:
        data = ledger()
        data["sources"] = [source("src-revoked-certification")]
        data["certifications"] = [{
            "certification_id": "cert-revoked",
            "issuer": "Synthetic certifying body",
            "status": "REVOKED",
            "evidence_ref": "src-revoked-certification",
            "validity": "2026",
            "valid_until": "2027-12-31",
            "authorized_display": True,
            "production_status": "PRODUCTION",
        }]
        self.assert_not_pass(validator.validate_ledger(data), "CERTIFICATION_STATUS_NOT_RELEASE_READY")

    def test_ak_unverified_affiliate_origin_is_blocked(self) -> None:
        data = ledger()
        data["sources"] = [source()]
        affiliate = claim(claim_type="AFFILIATE_PRODUCT", text="This product has a synthetic documented feature.")
        affiliate["affiliate"] = True
        affiliate["claim_origin"] = "UNVERIFIED"
        data["claims"] = [affiliate]
        self.assert_not_pass(validator.validate_ledger(data), "AFFILIATE_ORIGIN_UNCLASSIFIED")

    def test_frozen_repository_corpus_is_read_only_during_capability_7_checks(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-cap7-guard-") as directory:
            violation_log = Path(directory) / "violations.log"
            guard = FrozenIntegrityGuard(
                str(ROOT),
                protected_paths=["projects/"],
                ledger_path=str(violation_log),
                run_id="cap7-read-only-corpus",
            ).snapshot()
            result = guard.verify(record_violation=False)
            self.assertTrue(result.ok)
            self.assertGreater(result.checked_files, 0)


if __name__ == "__main__":
    unittest.main()
