"""Re-evaluate existing Clean-Room renders without invoking concept generation."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence

from .clean_room import BLIND_CRITIC_SENTINELS
from .rendered_morphology import HERO_PLUS_SIGNATURE_DEVICE_ONLY, compare_rendered_morphology


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _capture_existing_render(
    html_path: Path,
    *,
    evaluation_stage: str,
    signature_device_selector: str | None,
    viewport: int,
) -> Dict[str, Any]:
    if not html_path.is_file():
        raise FileNotFoundError(html_path)
    browser_root = str(Path(__file__).resolve().parents[1] / "browser-qa")
    if browser_root not in sys.path:
        sys.path.insert(0, browser_root)
    from engine.base import load_engine  # type: ignore[import-not-found]

    engine = load_engine(
        "playwright",
        str(html_path.parent),
        {
            "serve_dir": ".",
            "capture_morphology_evidence": True,
            "morphology_evaluation_stage": evaluation_stage,
            "morphology_signature_device_selector": signature_device_selector,
        },
    )
    if not engine.available():
        raise RuntimeError("PLAYWRIGHT_ENGINE_UNAVAILABLE")
    engine.start()
    try:
        observation = engine.observe(f"/{html_path.name}", viewport, capture="VIEWPORT")
        evidence = observation.raw.get("rendered_morphology_evidence")
        if not isinstance(evidence, Mapping):
            raise RuntimeError("RENDERED_MORPHOLOGY_EVIDENCE_MISSING")
        return dict(evidence)
    finally:
        engine.stop()


def _parse_key_value(values: Sequence[str], option: str) -> Dict[str, str]:
    parsed: Dict[str, str] = {}
    for value in values:
        key, separator, item = value.partition("=")
        if not separator or not key.strip() or not item.strip():
            raise ValueError(f"{option} values must use ID=value")
        parsed[key.strip()] = item.strip()
    return parsed


def _format_vector_list(values: Sequence[str]) -> str:
    return ", ".join(values) if values else "NONE"


def update_owner_review_report(
    report_path: Path,
    results: Mapping[str, Mapping[str, Any]],
) -> None:
    """Replace only morphology rows in an existing owner-review report."""

    html = report_path.read_text(encoding="utf-8")
    for concept_id, result in results.items():
        display_name = concept_id.replace("_", " ")
        section_pattern = re.compile(
            rf'(<section class="concept">(?:(?!<section class="concept">).)*?'
            rf'<h2>{re.escape(display_name)}</h2>(?:(?!<section class="concept">).)*?</section>)',
            re.DOTALL,
        )
        match = section_pattern.search(html)
        if not match:
            raise ValueError(f"owner-review section missing for {concept_id}")
        section = match.group(1)
        old_row = re.compile(
            r"(?:<dt>MORPHOLOGY DIVERGENCE =</dt><dd>.*?</dd>|"
            r"<dt>MORPHOLOGY VERDICT =</dt><dd>.*?</dd>"
            r"<dt>DIVERGENCE RATIO =</dt><dd>.*?</dd>"
            r"<dt>DIVERGENT VECTORS =</dt><dd>.*?</dd>"
            r"<dt>MATCHING VECTORS =</dt><dd>.*?</dd>"
            r"<dt>NOT APPLICABLE VECTORS =</dt><dd>.*?</dd>)",
            re.DOTALL,
        )
        ratio = result.get("divergence_ratio")
        ratio_text = "NOT_AVAILABLE" if ratio is None else f"{float(ratio):.3f}"
        rows = (
            f"<dt>MORPHOLOGY VERDICT =</dt><dd>{result['status']}</dd>"
            f"<dt>DIVERGENCE RATIO =</dt><dd>{ratio_text}</dd>"
            f"<dt>DIVERGENT VECTORS =</dt><dd>{_format_vector_list(result.get('divergent_vectors', []))}</dd>"
            f"<dt>MATCHING VECTORS =</dt><dd>{_format_vector_list(result.get('matching_vectors', []))}</dd>"
            f"<dt>NOT APPLICABLE VECTORS =</dt><dd>{_format_vector_list(result.get('not_applicable_vectors', []))}</dd>"
        )
        updated, count = old_row.subn(rows, section, count=1)
        if count != 1:
            raise ValueError(f"owner-review morphology row missing for {concept_id}")
        html = html[: match.start()] + updated + html[match.end() :]
    report_path.write_text(html, encoding="utf-8")


def _blind_critic_package(
    run_root: Path,
    results: Mapping[str, Mapping[str, Any]],
    receipt: Mapping[str, Any],
) -> Dict[str, Any] | None:
    passing = [concept_id for concept_id, result in results.items() if result.get("status") == "PASS_DIVERGENCE"]
    if not passing:
        return None
    inventory_path = run_root / "evidence" / "rendered-concept-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    records = {
        str(item.get("concept_id")): item
        for item in inventory.get("concepts", [])
        if isinstance(item, Mapping)
    }
    generator_package = receipt.get("generator_package", {})
    if not isinstance(generator_package, Mapping):
        generator_package = {}
    references = sorted(
        str(path.relative_to(run_root)).replace("\\", "/")
        for path in (run_root / "external-references").glob("*.png")
    )
    business_brief = generator_package.get("business_brief")
    brand_brief = generator_package.get("brand_brief")
    if not references or not isinstance(business_brief, str) or not business_brief.strip():
        raise RuntimeError("BLIND_CRITIC_INPUT_EVIDENCE_INCOMPLETE")
    if not isinstance(brand_brief, str) or not brand_brief.strip():
        raise RuntimeError("BLIND_CRITIC_INPUT_EVIDENCE_INCOMPLETE")
    concepts = []
    for concept_id in passing:
        item = records.get(concept_id, {})
        screenshots = [item.get("hero"), item.get("signature_device")]
        if any(not isinstance(path, str) or not (run_root / path).is_file() for path in screenshots):
            raise RuntimeError(f"BLIND_CRITIC_SCREENSHOT_EVIDENCE_INCOMPLETE: {concept_id}")
        concepts.append(
            {
                "concept_id": concept_id,
                "candidate_screenshots": screenshots,
                "external_reference_screenshots": references,
                "business_brief": business_brief,
                "brand_brief": brand_brief,
                "rendered_morphology_evidence": results[concept_id].get("candidate_evidence"),
                "morphology_verdict": results[concept_id].get("status"),
            }
        )
    package = {
        "package_kind": "BLIND_CRITIC_INPUT",
        "critic_execution": "NOT_EXECUTED",
        "concepts": concepts,
        "html_source": None,
        "css_source": None,
        "class_names": None,
        "direction_name": None,
        "builder_commentary": None,
        "self_awarded_scores": None,
        "previous_asn_screenshots": None,
    }
    serialized = json.dumps(package, sort_keys=True)
    leaks = [sentinel for sentinel in BLIND_CRITIC_SENTINELS if sentinel in serialized]
    if leaks:
        raise RuntimeError(f"BLIND_CRITIC_SENTINEL_LEAK: {', '.join(leaks)}")
    return package


def recheck_existing_clean_room_run(
    *,
    run_root: Path,
    baseline_path: Path,
    candidates: Mapping[str, Path],
    candidate_selectors: Mapping[str, str],
    baseline_selector: str | None = None,
    evaluation_stage: str = HERO_PLUS_SIGNATURE_DEVICE_ONLY,
    viewport: int = 1440,
) -> Dict[str, Any]:
    """Measure and report existing artifacts without calling a generator."""

    run_root = run_root.resolve()
    baseline_path = baseline_path.resolve()
    resolved_candidates = {key: path.resolve() for key, path in candidates.items()}
    for path in resolved_candidates.values():
        path.relative_to(run_root)
    creative_hashes_before = {key: _sha256(path) for key, path in resolved_candidates.items()}

    baseline_evidence = _capture_existing_render(
        baseline_path,
        evaluation_stage=evaluation_stage,
        signature_device_selector=baseline_selector,
        viewport=viewport,
    )
    results: Dict[str, Dict[str, Any]] = {}
    for concept_id, path in resolved_candidates.items():
        candidate_evidence = _capture_existing_render(
            path,
            evaluation_stage=evaluation_stage,
            signature_device_selector=candidate_selectors.get(concept_id),
            viewport=viewport,
        )
        comparison = compare_rendered_morphology(candidate_evidence, baseline_evidence, evaluation_stage)
        results[concept_id] = {
            **comparison,
            "candidate_path": str(path),
            "candidate_sha256": creative_hashes_before[concept_id],
            "candidate_evidence": candidate_evidence,
        }

    creative_hashes_after = {key: _sha256(path) for key, path in resolved_candidates.items()}
    if creative_hashes_after != creative_hashes_before:
        raise RuntimeError("CREATIVE_FILES_CHANGED_DURING_EVIDENCE_RECAPTURE")
    output = {
        "evaluation_stage": evaluation_stage,
        "baseline_evidence_path": str(baseline_path),
        "baseline_evidence_sha256": _sha256(baseline_path),
        "negative_baseline_role": "NEGATIVE_BASELINE_ONLY",
        "baseline_evidence": baseline_evidence,
        "evidence_schema_complete": all(result.get("evidence_schema_complete") for result in results.values()),
        "new_concept_generation": 0,
        "creative_files_changed": 0,
        "results": results,
    }
    evidence_root = run_root / "evidence"
    _write_json(evidence_root / "morphology-divergence.json", output)
    update_owner_review_report(run_root / "candidate-output" / "owner-review.html", results)

    receipt_path = evidence_root / "clean-room-execution-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    package = _blind_critic_package(run_root, results, receipt)
    package_path = evidence_root / "blind-critic-package.json"
    if package is not None:
        _write_json(package_path, package)
    elif package_path.exists():
        package_path.unlink()

    final_status_path = evidence_root / "final-status.json"
    final_status = json.loads(final_status_path.read_text(encoding="utf-8"))
    for concept_id, result in results.items():
        final_status[f"{concept_id}_MORPHOLOGY_DIVERGENCE"] = result.get("status")
        final_status[f"{concept_id}_DIVERGENCE_RATIO"] = result.get("divergence_ratio")
    final_status.update(
        {
            "BLIND_CRITIC_PACKAGE_PREPARED": package is not None,
            "CREATIVE_FILES_CHANGED": 0,
            "EVIDENCE_SCHEMA_COMPLETE": output["evidence_schema_complete"],
            "GAUNTLET_EXECUTION_MODE": "NOT_EXECUTED",
            "NEW_CONCEPT_GENERATION": 0,
            "OWNER_CONCEPT_SELECTION": "PENDING",
            "FULL_HOMEPAGE_DESIGN": "BLOCKED",
            "RUNTIME_STATUS": "PASS" if all(result.get("status") == "PASS_DIVERGENCE" for result in results.values()) else "FAIL",
            "WORKFLOW_STATUS": "OWNER_CONCEPT_SELECTION_PENDING" if package is not None else "RENDER_DERIVED_MORPHOLOGY_FAILED",
        }
    )
    _write_json(final_status_path, final_status)
    output["blind_critic_package_prepared"] = package is not None
    output["gauntlet_execution_mode"] = "NOT_EXECUTED"
    return output


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", required=True)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--baseline-selector")
    parser.add_argument("--candidate", action="append", default=[], help="ID=HTML_PATH; repeat per candidate")
    parser.add_argument("--candidate-selector", action="append", default=[], help="ID=CSS_SELECTOR")
    parser.add_argument("--stage", default=HERO_PLUS_SIGNATURE_DEVICE_ONLY)
    parser.add_argument("--viewport", type=int, default=1440)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    run_root = Path(args.run_root).resolve()
    candidate_values = _parse_key_value(args.candidate, "--candidate")
    if not candidate_values:
        raise ValueError("at least one --candidate is required")
    selectors = _parse_key_value(args.candidate_selector, "--candidate-selector")
    candidates = {
        concept_id: (Path(path) if Path(path).is_absolute() else run_root / path)
        for concept_id, path in candidate_values.items()
    }
    output = recheck_existing_clean_room_run(
        run_root=run_root,
        baseline_path=Path(args.baseline),
        candidates=candidates,
        candidate_selectors=selectors,
        baseline_selector=args.baseline_selector,
        evaluation_stage=args.stage,
        viewport=args.viewport,
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["recheck_existing_clean_room_run", "update_owner_review_report"]
