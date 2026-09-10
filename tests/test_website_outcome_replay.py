"""Focused, dependency-free tests for the V0.1 offline outcome replay pilot."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "browser-qa"))

from outcome_replay import (  # noqa: E402
    BLOCKED,
    CURRENTLY_EVIDENCE_VERIFIED_RESULT,
    DESIGN_PROPOSAL_COMPLETENESS,
    FAIL,
    INVALID,
    QUALITY_RUBRIC_VERSION,
    NOT_APPLICABLE,
    PASS,
    RENDERED_DESIGN_DISTINCTIVENESS,
    exit_code,
    replay,
)


class WebsiteOutcomeReplayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="website-outcome-replay-")
        self.workspace = Path(self.temp.name) / "repo"
        (self.workspace / "evidence").mkdir(parents=True)
        self.outputs = Path(self.temp.name) / "outputs"
        self.outputs.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _write(self, relative: str, value: str | bytes) -> tuple[str, str]:
        path = self.workspace / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(value, bytes):
            path.write_bytes(value)
        else:
            path.write_text(value, encoding="utf-8")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return relative.replace("\\", "/"), digest

    def _manifest(self, cases: list[dict]) -> Path:
        path = self.workspace / "manifest.json"
        path.write_text(json.dumps({
            "manifest_version": "0.1.0",
            "mode": "artifact-replay",
            "authorized_input_roots": ["evidence"],
            "cases": cases,
        }, indent=2), encoding="utf-8")
        return path

    def _run(self, cases: list[dict]) -> dict:
        manifest = self._manifest(cases)
        output = self.outputs / ("run-%d" % len(list(self.outputs.iterdir())))
        return replay(str(manifest), str(output), repo_root=str(self.workspace))

    def _quality_config(self, criteria: list[dict], hard_gates: list[dict] | None = None) -> dict:
        return {
            "required": True,
            "rubric_version": QUALITY_RUBRIC_VERSION,
            "requires_independent": True,
            "critique_evidence_id": "critic",
            "quality_bar": {"minimum_score": 8},
            "criteria": criteria,
            "hard_gates": hard_gates or [],
        }

    def _write_quality_critique(self, case: dict, evidence_files: list[str],
                                findings: list[dict], hard_gates: list[dict] | None = None,
                                *, complete: bool = True) -> tuple[str, str]:
        receipt = {
            "critique_version": "0.1.0",
            "rubric_version": QUALITY_RUBRIC_VERSION,
            "case_id": case["id"],
            "case_version": case["case_version"],
            "specimen_id": case["specimen"]["id"],
            "specimen_hash": case["specimen"].get("specimen_hash", "a" * 64),
            "evidence_files": evidence_files,
            "criterion_breakdown": [item["criterion_id"] for item in findings],
            "criterion_findings": findings,
            "hard_gate_findings": hard_gates or [],
            "critic_context": {
                "context_id": "quality-critic-context",
                "builder_context_id": "builder-context",
                "input_scope": "brief, rubric, and hash-bound rendered evidence only",
            },
            "reviewer": {"role": "independent_quality_critic", "independence": "SEPARATE_CONTEXT"},
            "limitations": ["Synthetic evaluator fixture; not a real website-quality result."],
            "timestamp": "2026-09-05T00:00:00Z",
        }
        if not complete:
            receipt.pop("criterion_breakdown", None)
        path, digest = self._write("evidence/quality-critique.json", json.dumps(receipt))
        return path, digest

    def _render_evidence(self, evidence_id: str, relative: str, viewport: int,
                         surface_id: str) -> tuple[dict, str]:
        path, digest = self._write(relative, bytes.fromhex(
            "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
            "0000000d49444154789c6360000000020001e221bc330000000049454e44ae426082"))
        return ({"id": evidence_id, "kind": "rendered_capture", "path": path,
                 "sha256": digest, "actual_rendered": True, "engine_identity": "REAL_BROWSER",
                 "viewport": viewport, "surface_id": surface_id, "render_capture": "FULL_PAGE"}, digest)

    def _case(self, case_id: str, artifact_text: str = "Alpha Starts Now") -> tuple[dict, str]:
        path, digest = self._write("evidence/site.html", artifact_text)
        case = {
            "id": case_id,
            "case_version": "0.1.0",
            "specimen": {
                "id": case_id + "-specimen",
                "kind": "REAL_ARTIFACT",
                "artifact_files": [{"id": "site", "path": path, "sha256": digest}],
            },
            "evidence": [],
            "requirements": [],
            "qualitative": {"criteria": []},
        }
        return case, digest

    def test_technical_pass_does_not_override_brief_failure(self) -> None:
        case, digest = self._case("random-technical-pass-case", "Other brand")
        path, evidence_digest = self._write("evidence/qa.json", '{"status":"PASS"}')
        case["evidence"] = [{"id": "qa", "kind": "observation", "path": path, "sha256": evidence_digest}]
        case["technical_evidence_ids"] = ["qa"]
        case["quality_score"] = 99
        case["requirements"] = [{
            "id": "brand-truth",
            "class": "MANDATORY",
            "assertion": {"type": "artifact_text", "artifact_id": "site", "all_of": ["Alpha Starts Now"]},
        }]
        report = self._run([case])
        self.assertEqual(report["cases"][0]["technical"]["status"], PASS)
        self.assertEqual(report["cases"][0]["outcome"]["status"], FAIL)
        self.assertEqual(exit_code(report), 1)

    def test_cinematic_fail_and_insufficient_evidence_are_distinct(self) -> None:
        failing, _ = self._case("cinematic-negative", "Alpha Starts Now")
        fail_path, fail_digest = self._write(
            "evidence/cinematic-fail.json",
            json.dumps({"status": "FAIL", "detail": "Reference composition is absent", "evidence_refs": ["site"]}),
        )
        failing["evidence"] = [{"id": "cinematic", "kind": "observation", "path": fail_path, "sha256": fail_digest}]
        failing["requirements"] = [{
            "id": "cinematic-reference",
            "class": "MANDATORY",
            "assertion": {"type": "evidence_observation", "evidence_id": "cinematic"},
        }]

        blocked, _ = self._case("cinematic-insufficient", "Alpha Starts Now")
        blocked["evidence"] = [{"id": "cinematic", "kind": "reference", "source_url": "https://example.invalid/ref"}]
        blocked["requirements"] = [{
            "id": "cinematic-reference",
            "class": "MANDATORY",
            "assertion": {"type": "evidence_status", "evidence_id": "cinematic", "acceptable_statuses": [PASS]},
        }]
        report = self._run([failing, blocked])
        results = {case["case_id"]: case["outcome"]["status"] for case in report["cases"]}
        self.assertEqual(results, {"cinematic-negative": FAIL, "cinematic-insufficient": BLOCKED})
        self.assertEqual(report["summary"][FAIL], 1)
        self.assertEqual(report["summary"][BLOCKED], 1)
        self.assertEqual(exit_code(report), 1)

    def test_restrained_brief_explicitly_marks_cinematic_not_applicable(self) -> None:
        case, _ = self._case("restrained-control", "Northstar Performance Lab")
        case["requirements"] = [
            {"id": "brand-truth", "class": "MANDATORY",
             "assertion": {"type": "artifact_text", "artifact_id": "site", "all_of": ["Northstar"]}},
            {"id": "cinematic-reference", "class": "MANDATORY", "applicability": "NOT_APPLICABLE",
             "reason": "The restrained brief does not require cinematic matching."},
        ]
        report = self._run([case])
        rendered = report["cases"][0]
        self.assertEqual(rendered["outcome"]["status"], PASS)
        self.assertEqual(rendered["requirements"][1]["status"], NOT_APPLICABLE)
        self.assertEqual(exit_code(report), 0)

    def test_missing_reference_and_critique_do_not_become_na_or_pass(self) -> None:
        case, _ = self._case("missing-support", "Alpha Starts Now")
        case["evidence"] = [{"id": "reference", "kind": "reference", "source_url": "https://example.invalid/ref"}]
        case["requirements"] = [
            {"id": "reference-trace", "class": "MANDATORY",
             "assertion": {"type": "reference_presence", "evidence_ids": ["reference"]}},
            {"id": "cinematic-reference", "class": "MANDATORY", "applicability": "NOT_APPLICABLE",
             "reason": "No cinematic claim is made in this fixture."},
        ]
        case["qualitative"] = {"requires_independent": True, "criteria": [{"id": "brief-fit"}]}
        report = self._run([case])
        rendered = report["cases"][0]
        self.assertEqual(rendered["outcome"]["status"], BLOCKED)
        self.assertEqual(rendered["requirements"][0]["status"], BLOCKED)
        self.assertEqual(rendered["requirements"][1]["status"], NOT_APPLICABLE)
        self.assertEqual(rendered["qualitative"]["status"], BLOCKED)

    def test_stale_hash_is_invalid_and_never_passes(self) -> None:
        case, _ = self._case("stale-hash", "Alpha Starts Now")
        case["specimen"]["artifact_files"][0]["sha256"] = "0" * 64
        case["requirements"] = [{"id": "brand", "class": "MANDATORY",
                                  "assertion": {"type": "artifact_text", "artifact_id": "site", "all_of": ["Alpha"]}}]
        report = self._run([case])
        self.assertEqual(report["cases"][0]["outcome"]["status"], INVALID)
        self.assertEqual(report["execution"]["status"], FAIL)
        self.assertEqual(exit_code(report), 3)

    def test_path_traversal_is_invalid(self) -> None:
        case, _ = self._case("path-traversal", "Alpha Starts Now")
        case["specimen"]["artifact_files"][0]["path"] = "../outside.txt"
        case["requirements"] = [{"id": "brand", "class": "MANDATORY",
                                  "assertion": {"type": "artifact_text", "artifact_id": "site", "all_of": ["Alpha"]}}]
        report = self._run([case])
        self.assertEqual(report["cases"][0]["outcome"]["status"], INVALID)
        self.assertEqual(report["execution"]["status"], FAIL)

    def test_unknown_assertion_is_invalid(self) -> None:
        case, _ = self._case("unknown-requirement", "Alpha Starts Now")
        case["requirements"] = [{"id": "unknown", "class": "MANDATORY",
                                  "assertion": {"type": "invented_quality_detector"}}]
        report = self._run([case])
        self.assertEqual(report["cases"][0]["outcome"]["status"], INVALID)
        self.assertEqual(report["execution"]["status"], FAIL)

    def test_critique_unknown_citation_is_invalid(self) -> None:
        case, _ = self._case("unsupported-critique-citation", "Alpha Starts Now")
        critique_path, critique_digest = self._write("evidence/critique.json", json.dumps({
            "critique_version": "0.1.0",
            "rubric_version": "pilot-0.1",
            "case_id": case["id"],
            "case_version": case["case_version"],
            "specimen_id": case["specimen"]["id"],
            "reviewer": {"role": "independent_reviewer", "independence": "INDEPENDENT"},
            "findings": [{"criterion_id": "brief-fit", "status": PASS, "evidence_refs": ["missing-ref"]}],
        }))
        case["evidence"] = [{"id": "critique", "kind": "critique", "path": critique_path, "sha256": critique_digest}]
        case["qualitative"] = {"requires_independent": True, "critique_evidence_id": "critique",
                                "criteria": [{"id": "brief-fit"}]}
        case["requirements"] = [{"id": "brand", "class": "MANDATORY",
                                  "assertion": {"type": "artifact_text", "artifact_id": "site", "all_of": ["Alpha"]}}]
        report = self._run([case])
        self.assertEqual(report["cases"][0]["outcome"]["status"], INVALID)
        self.assertEqual(report["execution"]["status"], FAIL)

    def test_self_issued_critique_is_not_independent_or_owner_approved(self) -> None:
        case, _ = self._case("self-issued-critique", "Alpha Starts Now")
        critique_path, critique_digest = self._write("evidence/critique.json", json.dumps({
            "critique_version": "0.1.0",
            "rubric_version": "pilot-0.1",
            "case_id": case["id"],
            "case_version": case["case_version"],
            "specimen_id": case["specimen"]["id"],
            "reviewer": {"role": "builder", "independence": "UNKNOWN"},
            "findings": [{"criterion_id": "brief-fit", "status": PASS, "evidence_refs": ["site"]}],
        }))
        case["evidence"] = [{"id": "critique", "kind": "critique", "path": critique_path, "sha256": critique_digest}]
        case["qualitative"] = {"requires_independent": True, "critique_evidence_id": "critique",
                                "criteria": [{"id": "brief-fit"}]}
        case["requirements"] = [{"id": "brand", "class": "MANDATORY",
                                  "assertion": {"type": "artifact_text", "artifact_id": "site", "all_of": ["Alpha"]}}]
        report = self._run([case])
        rendered = report["cases"][0]
        self.assertEqual(rendered["qualitative"]["independence"], "UNKNOWN")
        self.assertEqual(rendered["qualitative"]["status"], BLOCKED)
        self.assertEqual(rendered["owner_acceptance"]["status"], "NOT_RUN")
        self.assertEqual(rendered["outcome"]["status"], BLOCKED)

    def test_report_proves_offline_boundaries_and_does_not_mutate_input(self) -> None:
        case, _ = self._case("offline-boundary", "Alpha Starts Now")
        case["requirements"] = [{"id": "brand", "class": "MANDATORY",
                                  "assertion": {"type": "artifact_text", "artifact_id": "site", "all_of": ["Alpha"]}}]
        before = (self.workspace / "evidence/site.html").read_bytes()
        report = self._run([case])
        self.assertEqual(report["execution"]["status"], PASS)
        self.assertEqual(report["provenance"]["network_calls"], 0)
        self.assertEqual(report["provenance"]["provider_calls"], 0)
        self.assertEqual(report["provenance"]["browser_navigation"], 0)
        self.assertEqual(report["provenance"]["website_generation"], 0)
        self.assertFalse(report["provenance"]["input_mutation"])
        self.assertEqual((self.workspace / "evidence/site.html").read_bytes(), before)

    def test_case_ids_do_not_select_outcomes(self) -> None:
        first, _ = self._case("arbitrary-case-a", "Wrong")
        second, _ = self._case("arbitrary-case-b", "Wrong")
        for case in (first, second):
            case["requirements"] = [{"id": "brand", "class": "MANDATORY",
                                      "assertion": {"type": "artifact_text", "artifact_id": "site", "all_of": ["Alpha"]}}]
        report = self._run([first, second])
        self.assertEqual([case["outcome"]["status"] for case in report["cases"]], [FAIL, FAIL])

    def test_proposal_keywords_do_not_prove_rendered_distinctiveness(self) -> None:
        case, _ = self._case("proposal-vs-rendered", "subject_world hero_thesis signature_element")
        case["specimen"]["specimen_hash"] = "a" * 64
        case["requirements"] = [{"id": "brief-text", "class": "MANDATORY",
                                  "assertion": {"type": "artifact_text", "artifact_id": "site",
                                                 "all_of": ["subject_world"]}}]
        case["design_proposal"] = {
            "required": True,
            "criteria": [
                {"id": "subject-world", "assertion": {"type": "artifact_text", "artifact_id": "site", "all_of": ["subject_world"]}},
                {"id": "hero-thesis", "assertion": {"type": "artifact_text", "artifact_id": "site", "all_of": ["hero_thesis"]}},
                {"id": "signature-element", "assertion": {"type": "artifact_text", "artifact_id": "site", "all_of": ["signature_element"]}},
            ],
        }
        case["quality"] = self._quality_config([
            {"id": "distinctiveness", "dimension": RENDERED_DESIGN_DISTINCTIVENESS},
        ])
        path, digest = self._write_quality_critique(case, [], [{
            "criterion_id": "distinctiveness", "status": PASS, "score": 10,
            "observation": "Declared signature language exists.", "evidence_refs": [],
        }])
        case["evidence"] = [{"id": "critic", "kind": "critique", "path": path, "sha256": digest}]
        report = self._run([case])
        rendered = report["cases"][0]
        self.assertEqual(rendered["proposal_evaluation"]["status"], PASS)
        self.assertEqual(rendered["proposal_evaluation"]["name"], DESIGN_PROPOSAL_COMPLETENESS)
        self.assertEqual(rendered["quality_evaluation"]["status"], BLOCKED)
        self.assertEqual(rendered["quality_evaluation"]["criteria"][0]["status"], BLOCKED)
        self.assertIsNone(rendered["quality_evaluation"]["criteria"][0]["score"])
        self.assertEqual(rendered["outcome"]["status"], BLOCKED)

    def test_signature_declaration_without_render_evidence_is_blocked(self) -> None:
        case, _ = self._case("signature-without-render", "signature_element=true")
        case["specimen"]["specimen_hash"] = "b" * 64
        case["requirements"] = [{"id": "brief-text", "class": "MANDATORY",
                                  "assertion": {"type": "artifact_text", "artifact_id": "site",
                                                 "all_of": ["signature_element"]}}]
        case["design_proposal"] = {"criteria": [{
            "id": "signature", "assertion": {"type": "artifact_text", "artifact_id": "site", "all_of": ["signature_element"]},
        }]}
        case["quality"] = self._quality_config([{
            "id": "rendered-signature", "dimension": RENDERED_DESIGN_DISTINCTIVENESS,
        }])
        path, digest = self._write_quality_critique(case, [], [{
            "criterion_id": "rendered-signature", "status": PASS, "score": 9,
            "observation": "Signature element is declared.", "evidence_refs": [],
        }])
        case["evidence"] = [{"id": "critic", "kind": "critique", "path": path, "sha256": digest}]
        report = self._run([case])
        self.assertEqual(report["cases"][0]["quality_evaluation"]["status"], BLOCKED)
        self.assertNotEqual(report["cases"][0]["quality_evaluation"]["claim_classification"], CURRENTLY_EVIDENCE_VERIFIED_RESULT)

    def test_asset_claim_without_resolvable_artifact_cannot_pass_imagery(self) -> None:
        case, _ = self._case("missing-asset-artifact", "ASSET_VERIFIED = true")
        case["specimen"]["specimen_hash"] = "c" * 64
        case["requirements"] = [{"id": "brief-text", "class": "MANDATORY",
                                  "assertion": {"type": "artifact_text", "artifact_id": "site",
                                                 "all_of": ["ASSET_VERIFIED"]}}]
        render, _ = self._render_evidence("desktop", "evidence/desktop.png", 1440, "DESKTOP_FULL_PAGE")
        missing_asset = {"id": "hero-asset", "kind": "image_asset", "path": "evidence/missing-hero.svg",
                         "sha256": "0" * 64}
        case["evidence"] = [render, missing_asset]
        case["quality"] = self._quality_config([{
            "id": "imagery", "dimension": "IMAGERY_AND_VISUAL_WORLD",
            "required_evidence_types": ["rendered_capture", "image_asset"],
        }])
        path, digest = self._write_quality_critique(case, ["desktop", "hero-asset"], [{
            "criterion_id": "imagery", "status": PASS, "score": 10,
            "observation": "Hero asset is declared verified.", "evidence_refs": ["desktop", "hero-asset"],
        }])
        case["evidence"].append({"id": "critic", "kind": "critique", "path": path, "sha256": digest})
        report = self._run([case])
        criterion = report["cases"][0]["quality_evaluation"]["criteria"][0]
        self.assertEqual(criterion["status"], BLOCKED)
        self.assertIsNone(criterion["score"])
        self.assertEqual(report["cases"][0]["quality_evaluation"]["status"], BLOCKED)

    def test_generic_basic_page_fails_hard_gate_despite_clear_hierarchy(self) -> None:
        case, _ = self._case("generic-basic-page", "headline buttons three generic cards")
        case["specimen"]["specimen_hash"] = "d" * 64
        case["requirements"] = [{"id": "brief-text", "class": "MANDATORY",
                                  "assertion": {"type": "artifact_text", "artifact_id": "site",
                                                 "all_of": ["headline"]}}]
        render, _ = self._render_evidence("desktop", "evidence/desktop.png", 1440, "DESKTOP_FULL_PAGE")
        case["evidence"] = [render]
        case["quality"] = self._quality_config([
            {"id": "hierarchy", "dimension": "VISUAL_HIERARCHY"},
            {"id": "conversion", "dimension": "CONVERSION_CLARITY"},
            {"id": "distinctiveness", "dimension": RENDERED_DESIGN_DISTINCTIVENESS},
        ], [{"id": "generic-template", "required_evidence_types": ["rendered_capture"]}])
        findings = [{"criterion_id": item, "status": PASS, "score": 9,
                     "observation": "Clear but ordinary.", "evidence_refs": ["desktop"]}
                    for item in ("hierarchy", "conversion", "distinctiveness")]
        gates = [{"gate_id": "generic-template", "status": FAIL, "observation": "Three generic cards and no authored visual device.",
                  "evidence_refs": ["desktop"]}]
        path, digest = self._write_quality_critique(case, ["desktop"], findings, gates)
        case["evidence"].append({"id": "critic", "kind": "critique", "path": path, "sha256": digest})
        report = self._run([case])
        quality = report["cases"][0]["quality_evaluation"]
        self.assertEqual(quality["status"], FAIL)
        self.assertEqual(quality["quality_bar_status"], "NOT_MET")
        self.assertEqual(quality["hard_gates"][0]["status"], FAIL)
        self.assertEqual(report["cases"][0]["outcome"]["status"], FAIL)

    def test_missing_required_visual_evidence_is_blocked_not_fabricated_pass(self) -> None:
        case, _ = self._case("missing-visual-evidence", "Asterion")
        case["specimen"]["specimen_hash"] = "e" * 64
        case["requirements"] = [{"id": "brief-text", "class": "MANDATORY",
                                  "assertion": {"type": "artifact_text", "artifact_id": "site",
                                                 "all_of": ["Asterion"]}}]
        case["quality"] = self._quality_config([{
            "id": "composition", "dimension": "COMPOSITION_AND_ART_DIRECTION",
        }])
        case["evidence"] = []
        report = self._run([case])
        quality = report["cases"][0]["quality_evaluation"]
        self.assertEqual(quality["status"], BLOCKED)
        self.assertEqual(quality["quality_bar_status"], "BLOCKED")
        self.assertEqual(report["cases"][0]["outcome"]["status"], BLOCKED)

    def test_positive_evidence_bound_quality_fixture_reaches_assessment(self) -> None:
        case, _ = self._case("positive-quality-fixture", "Asterion Private Performance")
        case["specimen"]["kind"] = "SYNTHETIC_FIXTURE"
        case["specimen"]["specimen_hash"] = "f" * 64
        case["requirements"] = [{"id": "brief-text", "class": "MANDATORY",
                                  "assertion": {"type": "artifact_text", "artifact_id": "site",
                                                 "all_of": ["Asterion Private Performance"]}}]
        desktop, _ = self._render_evidence("desktop", "evidence/desktop.png", 1440, "DESKTOP_FULL_PAGE")
        tablet, _ = self._render_evidence("tablet", "evidence/tablet.png", 768, "TABLET_FULL_PAGE")
        mobile, _ = self._render_evidence("mobile", "evidence/mobile.png", 375, "MOBILE_FULL_PAGE")
        asset_path, asset_digest = self._write("evidence/asterion-orbit.svg", "<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10'></svg>")
        asset = {"id": "hero-asset", "kind": "image_asset", "path": asset_path, "sha256": asset_digest}
        case["evidence"] = [desktop, tablet, mobile, asset]
        criteria = []
        findings = []
        for dimension in (
            "BRIEF_AND_BRAND_FIDELITY", "VISUAL_HIERARCHY", "TYPOGRAPHY",
            "COMPOSITION_AND_ART_DIRECTION", "IMAGERY_AND_VISUAL_WORLD",
            "PREMIUM_DISTINCTIVENESS", "MEMORABILITY", "POLISH_AND_CRAFT",
            "RESPONSIVE_QUALITY", "CONVERSION_CLARITY", "MOTION_QUALITY",
        ):
            criterion_id = dimension.lower().replace("_", "-")
            criterion = {"id": criterion_id, "dimension": dimension}
            refs = ["desktop", "tablet", "mobile"]
            if dimension == "IMAGERY_AND_VISUAL_WORLD":
                refs.append("hero-asset")
            if dimension == "MOTION_QUALITY":
                criterion["applicability"] = NOT_APPLICABLE
                refs = []
                status = NOT_APPLICABLE
                score = None
            else:
                status = PASS
                score = 9
            if dimension == "RESPONSIVE_QUALITY":
                criterion["required_surfaces"] = ["DESKTOP_FULL_PAGE", "TABLET_FULL_PAGE", "MOBILE_FULL_PAGE"]
            criteria.append(criterion)
            findings.append({"criterion_id": criterion_id, "status": status, "score": score,
                             "observation": "Evidence-bound synthetic observation.", "evidence_refs": refs})
        case["quality"] = self._quality_config(criteria, [{"id": "generic-template"}])
        path, digest = self._write_quality_critique(case, ["desktop", "tablet", "mobile", "hero-asset"], findings,
                                                    [{"gate_id": "generic-template", "status": PASS,
                                                      "observation": "No generic-template hard gate observed in the fixture.",
                                                      "evidence_refs": ["desktop"]}])
        case["evidence"].append({"id": "critic", "kind": "critique", "path": path, "sha256": digest})
        report = self._run([case])
        rendered = report["cases"][0]
        self.assertEqual(rendered["quality_evaluation"]["status"], PASS)
        self.assertEqual(rendered["quality_evaluation"]["quality_bar_status"], "MET")
        self.assertEqual(rendered["quality_evaluation"]["claim_classification"], CURRENTLY_EVIDENCE_VERIFIED_RESULT)
        self.assertEqual(rendered["specimen"]["quality_claim"], "SYNTHETIC_FIXTURE_ONLY")
        self.assertEqual(rendered["outcome"]["status"], PASS)
        self.assertEqual(exit_code(report), 0)


if __name__ == "__main__":
    unittest.main()
