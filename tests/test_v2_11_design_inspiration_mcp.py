"""Deterministic V2.11.1 Design Inspiration MCP adapter controls.

The suite uses only synthetic structured results. It does not need a live
Serper key, invoke the upstream Node server, access the network, download an
image, or modify the frozen project corpus.
"""

from __future__ import annotations

import ast
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER_ROOT = ROOT / "integrations" / "design-inspiration" / "adapter"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ADAPTER_ROOT))
sys.path.insert(0, str(ROOT / "browser-qa"))

from adapter import (  # noqa: E402
    PLATFORMS,
    REFERENCE_ONLY,
    RUBRIC_DIMENSIONS,
    SEARCH_TOOLS,
    TOKEN_EXTRACTION_MODE,
    UPSTREAM_COMMIT,
    bound_search_count,
    canonicalize_url,
    credential_state,
    enforce_originality_request,
    enforce_production_asset_boundary,
    evaluate_reference,
    generate_design_query,
    infer_platform,
    normalize_mcp_results,
    prepare_search_request,
    token_extraction_status,
    validate_query,
    validate_upstream_pin,
)
from guards.frozen_integrity_guard import FrozenIntegrityGuard  # noqa: E402
from framework_validation import validator  # noqa: E402


FIXTURE_PATH = ROOT / "integrations" / "design-inspiration" / "fixtures" / "synthetic-mcp-results.json"
UPSTREAM_PATH = ROOT / "integrations" / "design-inspiration" / "upstream.json"


def load_fixture() -> dict[str, object]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


class DesignInspirationMCPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = load_fixture()
        cls.normalized = normalize_mcp_results(
            "design_search_images",
            {"images": cls.fixture["images"]},
            "architecture material systems restrained editorial interface",
            str(cls.fixture["retrieved_at"]),
            max_results=12,
        )

    def test_a_dribbble_platform_and_required_fields(self) -> None:
        self.assertEqual(infer_platform("https://dribbble.com/shots/1001/precision"), "Dribbble")
        result = next(item for item in self.normalized["results"] if item["source_platform"] == "Dribbble")
        for field in (
            "source_platform",
            "source_url",
            "title",
            "image_url",
            "query",
            "pattern_type",
            "visual_notes",
            "production_plausibility",
            "reference_grade",
            "why_selected",
            "pattern_to_learn",
            "what_not_to_copy",
            "accessibility_risk",
            "implementation_risk",
            "copyright_boundary",
            "retrieved_at",
            "provider",
            "upstream_commit",
        ):
            self.assertIn(field, result)
        self.assertEqual(result["copyright_boundary"], REFERENCE_ONLY)

    def test_b_behance_platform(self) -> None:
        self.assertEqual(infer_platform("https://www.behance.net/gallery/2002/material-systems"), "Behance")
        self.assertTrue(any(item["source_platform"] == "Behance" for item in self.normalized["results"]))

    def test_c_awwwards_keeps_existing_interpretation_authority(self) -> None:
        result = next(item for item in self.normalized["results"] if item["source_platform"] == "Awwwards")
        self.assertEqual(result["interpretation_authority"], "AWWWARDS-SHOWCASE-INTELLIGENCE")
        self.assertEqual(result["pattern_type"], "showcase-benchmark")

    def test_d_mobbin_is_a_product_flow_signal(self) -> None:
        result = next(item for item in self.normalized["results"] if item["source_platform"] == "Mobbin")
        self.assertEqual(result["pattern_type"], "product-flow")

    def test_e_pinterest_is_a_mood_signal(self) -> None:
        result = next(item for item in self.normalized["results"] if item["source_platform"] == "Pinterest")
        self.assertEqual(result["pattern_type"], "moodboard-signal")

    def test_f_duplicate_canonical_source_is_removed(self) -> None:
        self.assertEqual(len(self.normalized["results"]), 5)
        self.assertGreaterEqual(self.normalized["dropped_count"], 1)
        self.assertEqual(
            canonicalize_url("https://dribbble.com/shots/1001/precision?utm_source=one"),
            canonicalize_url("https://www.dribbble.com/shots/1001/precision?utm_medium=two"),
        )

    def test_g_missing_key_is_blocked_without_crash(self) -> None:
        state = credential_state(env={})
        self.assertEqual(state["status"], "BLOCKED_CREDENTIAL_MISSING")
        request = prepare_search_request(
            "design_search_images",
            "architecture material systems restrained editorial interface",
            sites=PLATFORMS,
            env={},
        )
        self.assertEqual(request["status"], "BLOCKED_CREDENTIAL_MISSING")
        self.assertNotIn("sk_live", json.dumps(request))

    def test_h_image_is_reference_only_and_not_a_production_asset(self) -> None:
        result = self.normalized["results"][0]
        boundary = enforce_production_asset_boundary(result)
        self.assertEqual(boundary["status"], "PRODUCTION_ASSET_REFUSED")
        self.assertFalse(boundary["allowed"])
        self.assertEqual(boundary["copyright_boundary"], REFERENCE_ONLY)

    def test_i_generic_query_is_rejected(self) -> None:
        result = validate_query("good design")
        self.assertEqual(result["status"], "QUERY_REJECTED_GENERIC")
        self.assertIsNone(result["query"])

    def test_j_specific_query_is_accepted_and_context_generates_specific_query(self) -> None:
        result = validate_query("architecture material systems restrained editorial interface")
        self.assertEqual(result["status"], "QUERY_ACCEPTED")
        generated = generate_design_query(
            {
                "project_brief": "Architecture practice seeking permanent civic commissions",
                "positioning": "Material precision and restrained editorial authority",
                "audience": "Civic commissioners and cultural institution directors",
                "design_ambition": "premium",
            }
        )
        self.assertLessEqual(len(generated), 200)
        self.assertNotEqual(validate_query("nice website", {"positioning": "material precision civic architecture"})["status"], "QUERY_REJECTED_GENERIC")

    def test_k_high_craft_low_utility_is_dribbble_fantasy_d(self) -> None:
        scores = {dimension: 4 for dimension in RUBRIC_DIMENSIONS}
        scores.update(
            {
                "VISUAL_CRAFT": 5,
                "RESPONSIVE_PLAUSIBILITY": 1,
                "ACCESSIBILITY_PLAUSIBILITY": 1,
                "IMPLEMENTABILITY": 1,
            }
        )
        result = evaluate_reference(self.normalized["results"][0], scores)
        self.assertEqual(result["reference_grade"], "D")
        self.assertEqual(result["production_plausibility"], "LOW")
        self.assertIn("Dribbble fantasy", result["grade_reason"])

    def test_l_realistic_references_can_be_a_or_b(self) -> None:
        high_scores = {dimension: 4 for dimension in RUBRIC_DIMENSIONS}
        high_scores.update({"VISUAL_CRAFT": 5, "SUBJECT_RELEVANCE": 5, "BRAND_FIT": 5})
        high = evaluate_reference(self.normalized["results"][1], high_scores)
        self.assertEqual(high["reference_grade"], "A")
        medium_scores = {dimension: 3 for dimension in RUBRIC_DIMENSIONS}
        medium = evaluate_reference(self.normalized["results"][1], medium_scores)
        self.assertEqual(medium["reference_grade"], "B")

    def test_m_exact_copy_request_is_refused(self) -> None:
        result = enforce_originality_request("make a pixel-perfect clone of this page")
        self.assertEqual(result["status"], "CLONE_REQUEST_REFUSED")
        self.assertFalse(result["allowed"])

    def test_n_token_extraction_is_blocked_but_search_is_unaffected(self) -> None:
        token_result = token_extraction_status(
            "https://example.com/reference",
            mode=TOKEN_EXTRACTION_MODE,
            deliberate=True,
            authorized=True,
            dembrandt_available=False,
        )
        self.assertEqual(token_result["status"], "TOKEN_EXTRACTION_BLOCKED")
        self.assertIsNone(token_result["tokens"])
        self.assertEqual(len(self.normalized["results"]), 5)

    def test_o_secret_query_is_rejected_and_not_echoed(self) -> None:
        secret = "VALUE_MUST_NOT_LEAK"
        result = validate_query(f"architecture api_key={secret}")
        serialized = json.dumps(result)
        self.assertEqual(result["status"], "QUERY_REJECTED_SENSITIVE")
        self.assertNotIn(secret, serialized)
        self.assertNotIn("api_key=", serialized)

    def test_p_unpinned_upstream_fails_closed(self) -> None:
        metadata = json.loads(UPSTREAM_PATH.read_text(encoding="utf-8"))
        metadata["upstream_commit_sha"] = "main"
        result = validate_upstream_pin(metadata)
        self.assertEqual(result["status"], "UPSTREAM_PIN_INVALID")
        self.assertFalse(result["ok"])

    def test_q_existing_validator_rejects_a_sixth_owner_lock(self) -> None:
        bad_profile = {"locks": {name: False for name in validator.CANONICAL_LOCKS}}
        bad_profile["locks"]["measurement_locked"] = False
        self.assertIn("OWNER_LOCK_INVARIANT", validator.validate_owner_locks(bad_profile))

    def test_r_frozen_integrity_guard_detects_mutation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="website-director-mcp-frozen-") as directory:
            root = Path(directory)
            protected = root / "projects" / "fixture" / "state.json"
            protected.parent.mkdir(parents=True)
            protected.write_text("{}", encoding="utf-8")
            guard = FrozenIntegrityGuard(
                str(root),
                protected_paths=["projects/"],
                ledger_path="runtime/violations.log",
                run_id="v2-11-mcp-negative-control",
            )
            guard.snapshot()
            protected.write_text('{"mutated": true}', encoding="utf-8")
            result = guard.verify()
            self.assertFalse(result.ok)
            self.assertEqual(result.mutations, ["projects/fixture/state.json"])
            self.assertTrue((root / "runtime" / "violations.log").exists())

    def test_registered_tools_are_search_only_and_adapter_has_no_io_imports(self) -> None:
        self.assertEqual(
            SEARCH_TOOLS,
            ("design_search_images", "design_search_references", "design_search_styles"),
        )
        tree = ast.parse((ADAPTER_ROOT / "adapter.py").read_text(encoding="utf-8"))
        imports = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imports.update(
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            for alias in node.names
            if node.module
        )
        self.assertNotIn("subprocess", imports)
        self.assertNotIn("requests", imports)
        self.assertNotIn("httpx", imports)
        self.assertNotIn("socket", imports)
        self.assertNotIn("urllib", imports)

    def test_upstream_pin_record_and_platform_contract_are_complete(self) -> None:
        metadata = json.loads(UPSTREAM_PATH.read_text(encoding="utf-8"))
        self.assertTrue(validate_upstream_pin(metadata)["ok"])
        self.assertEqual(metadata["upstream_commit_sha"], UPSTREAM_COMMIT)
        self.assertEqual(metadata["exposed_search_tools"], list(SEARCH_TOOLS))
        self.assertEqual(metadata["disabled_tools"], ["design_extract_tokens"])
        self.assertEqual(metadata["license"], "MIT")
        self.assertEqual(set(PLATFORMS), {"Dribbble", "Behance", "Awwwards", "Mobbin", "Pinterest"})

    def test_search_budget_is_bounded_by_stage(self) -> None:
        self.assertEqual(bound_search_count(99, "initial"), 12)
        self.assertEqual(bound_search_count(1, "initial"), 6)
        self.assertEqual(bound_search_count(99, "shortlist"), 6)
        self.assertEqual(bound_search_count(1, "shortlist"), 3)
        self.assertEqual(bound_search_count(99, "deep"), 3)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DesignInspirationMCPTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(
        "DESIGN_INSPIRATION_MCP_TESTS = %s (%d/%d)"
        % ("PASS" if result.wasSuccessful() else "FAIL", result.testsRun - len(result.failures) - len(result.errors), result.testsRun)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
