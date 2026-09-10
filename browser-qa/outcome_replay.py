"""Offline Website Director outcome replay.

This adapter evaluates already-recorded local artifacts.  It deliberately does
not start a browser, load a URL, call a provider, generate a site, or mutate a
project.  The existing Browser QA runner remains the only runtime runner;
``runner.py --mode artifact-replay`` is an explicit, opt-in branch that calls
this module.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import PureWindowsPath
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

REPORT_VERSION = "0.1.0"
MANIFEST_VERSION = "0.1.0"
QUALITY_RUBRIC_VERSION = "WD-QUALITY-V0.1"
PASS = "PASS"
FAIL = "FAIL"
BLOCKED = "BLOCKED"
NOT_APPLICABLE = "NOT_APPLICABLE"
NOT_RUN = "NOT_RUN"
INVALID = "INVALID"
VALID_ASSESSMENT_STATUSES = {PASS, FAIL, BLOCKED, NOT_APPLICABLE}
VALID_RESULT_STATUSES = VALID_ASSESSMENT_STATUSES | {NOT_RUN, INVALID}
QUALITY_FINDING_STATUSES = VALID_ASSESSMENT_STATUSES | {"PROVISIONAL_PASS"}
QUALITY_DIMENSIONS = (
    "BRIEF_AND_BRAND_FIDELITY",
    "VISUAL_HIERARCHY",
    "TYPOGRAPHY",
    "COMPOSITION_AND_ART_DIRECTION",
    "IMAGERY_AND_VISUAL_WORLD",
    "PREMIUM_DISTINCTIVENESS",
    "MEMORABILITY",
    "POLISH_AND_CRAFT",
    "RESPONSIVE_QUALITY",
    "CONVERSION_CLARITY",
    "MOTION_QUALITY",
)
PAIRWISE_DIMENSIONS = (
    "FIRST_IMPRESSION",
    "TYPOGRAPHY",
    "COMPOSITION",
    "VISUAL_WORLD_IMAGERY",
    "CRAFT",
    "MEMORABILITY",
    "INTERACTION",
)
PAIRWISE_DEFAULT_DIMENSIONS = PAIRWISE_DIMENSIONS[:-1]
PAIRWISE_CHOICES = {"A", "B", "AMBIGUOUS"}
DESIGN_PROPOSAL_COMPLETENESS = "DESIGN_PROPOSAL_COMPLETENESS"
RENDERED_DESIGN_DISTINCTIVENESS = "RENDERED_DESIGN_DISTINCTIVENESS"
CURRENTLY_EVIDENCE_VERIFIED_RESULT = "CURRENTLY_EVIDENCE_VERIFIED_RESULT"
LEGACY_UNSUBSTANTIATED_QUALITY_CLAIM = "LEGACY_UNSUBSTANTIATED_QUALITY_CLAIM"
HISTORICAL_RECORDED_CLAIM = "HISTORICAL_RECORDED_CLAIM"
_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")
_URL_PREFIXES = ("http:", "https:", "file:", "ftp:", "data:")


class ReplayInputError(ValueError):
    """The manifest or its integrity contract is malformed."""


class IntegrityError(ReplayInputError):
    """A supplied digest does not match a local input."""


class MissingEvidence(Exception):
    """A declared input is unavailable; this is a result-level BLOCKED state."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _run_id() -> str:
    return "outcome-replay-%s" % datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_within(path: str, parent: str) -> bool:
    try:
        return os.path.commonpath([os.path.normcase(os.path.abspath(path)),
                                   os.path.normcase(os.path.abspath(parent))]) == \
            os.path.normcase(os.path.abspath(parent))
    except ValueError:
        return False


def _reject_unsafe_path(raw: Any, field: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ReplayInputError("%s must be a non-empty relative path" % field)
    value = raw.strip()
    if "\x00" in value or value.lower().startswith(_URL_PREFIXES):
        raise ReplayInputError("%s must be a local relative path" % field)
    windows = PureWindowsPath(value)
    if os.path.isabs(value) or windows.is_absolute() or windows.drive or value.startswith(("/", "\\")):
        raise ReplayInputError("%s must not be absolute" % field)
    parts = value.replace("\\", "/").split("/")
    if any(part == ".." for part in parts):
        raise ReplayInputError("%s contains path traversal" % field)
    return value


def _require_sha(raw: Any, field: str) -> str:
    if not isinstance(raw, str) or not _SHA256.fullmatch(raw):
        raise ReplayInputError("%s must be a 64-character SHA-256 digest" % field)
    return raw.lower()


def _safe_roots(repo_root: str, values: Any) -> List[str]:
    if not isinstance(values, list) or not values:
        raise ReplayInputError("authorized_input_roots must be a non-empty list")
    roots: List[str] = []
    for index, raw in enumerate(values):
        rel = _reject_unsafe_path(raw, "authorized_input_roots[%d]" % index)
        root = os.path.realpath(os.path.join(repo_root, rel))
        if not _is_within(root, repo_root) or not os.path.isdir(root):
            raise ReplayInputError("authorized input root is unavailable or escapes the repository: %s" % raw)
        roots.append(root)
    return roots


def _resolve_local(repo_root: str, roots: Sequence[str], raw: Any, field: str,
                   required: bool = True) -> Optional[str]:
    rel = _reject_unsafe_path(raw, field)
    candidate = os.path.realpath(os.path.join(repo_root, rel))
    if not any(_is_within(candidate, root) for root in roots):
        raise ReplayInputError("%s is outside authorized input roots" % field)
    if not os.path.isfile(candidate):
        if required:
            raise MissingEvidence("missing local evidence: %s" % raw)
        return None
    return candidate


def _resolve_receipt_path(receipt_path: str, raw: Any, roots: Sequence[str], field: str,
                          required: bool = True) -> Optional[str]:
    rel = _reject_unsafe_path(raw, field)
    candidates = []
    base = os.path.dirname(receipt_path)
    for _ in range(4):
        candidates.append(os.path.realpath(os.path.join(base, rel)))
        base = os.path.dirname(base)
    for candidate in candidates:
        if any(_is_within(candidate, root) for root in roots) and os.path.isfile(candidate):
            return candidate
    if required:
        raise MissingEvidence("missing receipt evidence: %s" % raw)
    return None


def _read_json(path: str, field: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            value = json.load(fh)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ReplayInputError("%s is not readable JSON: %s" % (field, exc)) from exc
    if not isinstance(value, dict):
        raise ReplayInputError("%s must contain a JSON object" % field)
    return value


def _relative_to_repo(path: str, repo_root: str) -> str:
    try:
        return os.path.relpath(path, repo_root).replace(os.sep, "/")
    except ValueError:
        return path


def _prepare_output(path: str, repo_root: str) -> str:
    if not isinstance(path, str) or not path.strip():
        raise ReplayInputError("evidence output directory is required")
    output = os.path.realpath(os.path.abspath(os.path.expanduser(path)))
    if _is_within(output, repo_root):
        raise ReplayInputError("replay output must be outside the repository")
    if os.path.exists(output) and not os.path.isdir(output):
        raise ReplayInputError("replay output is not a directory")
    os.makedirs(output, exist_ok=True)
    if any(os.scandir(output)):
        raise ReplayInputError("replay output directory must be empty to prevent overwrites")
    return output


def _base_report(run_id: str, manifest_path: str, repo_root: str) -> Dict[str, Any]:
    return {
        "report_version": REPORT_VERSION,
        "run_id": run_id,
        "mode": "artifact-replay",
        "manifest_path": _relative_to_repo(manifest_path, repo_root),
        "repo_root": repo_root,
        "started_at": _utc_now(),
        "finished_at": None,
        "execution": {"status": PASS, "error_kind": None, "errors": []},
        "cases": [],
        "summary": {"real_cases": 0, "synthetic_cases": 0, "PASS": 0,
                     "FAIL": 0, "BLOCKED": 0, "NOT_APPLICABLE": 0,
                     "NOT_RUN": 0, "INVALID": 0},
        "quality_contract": {
            "rubric_version": QUALITY_RUBRIC_VERSION,
            "rendered_evidence_required": True,
            "dimensions": list(QUALITY_DIMENSIONS),
            "proposal_and_rendered_quality_separate": True,
        },
        "quality_summary": {"cases": 0, "evidence_verified": 0,
                            "FAIL": 0, "BLOCKED": 0, "NOT_APPLICABLE": 0},
        "provenance": {
            "adapter": "browser-qa/outcome_replay.py",
            "adapter_version": REPORT_VERSION,
            "network_calls": 0,
            "provider_calls": 0,
            "browser_navigation": 0,
            "website_generation": 0,
            "paid_eval_calls": 0,
            "input_mutation": False,
            "baseline_replacement": False,
            "owner_acceptance": "NOT_RUN",
        },
    }


def _invalid_case(case_id: str, reason: str) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "case_version": None,
        "specimen": {"id": None, "kind": "UNKNOWN", "hash_status": INVALID},
        "technical": {"status": NOT_RUN, "provenance": "NOT_RUN", "evidence": []},
        "requirements": [],
        "proposal_evaluation": {"status": NOT_RUN, "provenance": "NOT_RUN",
                                 "name": DESIGN_PROPOSAL_COMPLETENESS, "criteria": []},
        "qualitative": {"status": NOT_RUN, "provenance": "NOT_RUN", "criteria": [],
                         "independence": "UNKNOWN", "reason": reason},
        "quality_evaluation": {"status": NOT_RUN, "provenance": "NOT_RUN",
                                "claim_classification": "UNVERIFIED_QUALITY_CLAIM",
                                "criteria": [], "hard_gates": [], "reason": reason},
        "owner_acceptance": {"status": NOT_RUN, "reason": "No owner label was evaluated."},
        "baseline_comparison": {"status": NOT_RUN, "comparable": False,
                                 "reason": "No baseline was replaced or inferred."},
        "historical_reproduction": {"status": NOT_RUN, "reason": "Invalid case input."},
        "historical_claim_classification": {"status": NOT_APPLICABLE, "claims": []},
        "certification": {"technical_verification": NOT_RUN, "quality_evaluation": NOT_RUN,
                           "owner_acceptance": NOT_RUN, "production_certification": "NOT_GRANTED"},
        "missing_evidence": [reason],
        "outcome": {"status": INVALID, "reason": reason},
    }


def _validate_ref_list(raw: Any, field: str) -> List[Dict[str, Any]]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ReplayInputError("%s must be a list" % field)
    refs = []
    seen = set()
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ReplayInputError("%s[%d] must be an object" % (field, index))
        ref_id = item.get("id") or item.get("evidence_id")
        if not isinstance(ref_id, str) or not ref_id:
            raise ReplayInputError("%s[%d] needs an id" % (field, index))
        if ref_id in seen:
            raise ReplayInputError("duplicate reference id: %s" % ref_id)
        seen.add(ref_id)
        refs.append(dict(item, id=ref_id))
    return refs


def _bind_artifacts(repo_root: str, roots: Sequence[str], raw: Any) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, str]]:
    refs = _validate_ref_list(raw, "specimen.artifact_files")
    artifacts: Dict[str, Dict[str, Any]] = {}
    known: Dict[str, str] = {}
    for ref in refs:
        path = ref.get("path")
        digest = _require_sha(ref.get("sha256"), "artifact %s sha256" % ref["id"])
        try:
            resolved = _resolve_local(repo_root, roots, path, "artifact %s path" % ref["id"])
            actual = _sha256(resolved)
            if actual != digest:
                raise IntegrityError("artifact %s hash mismatch" % ref["id"])
            record = {"id": ref["id"], "path": path, "resolved_path": resolved,
                      "sha256": digest, "status": PASS, "kind": ref.get("kind", "source")}
        except MissingEvidence as exc:
            record = {"id": ref["id"], "path": path, "resolved_path": None,
                      "sha256": digest, "status": BLOCKED, "reason": str(exc),
                      "kind": ref.get("kind", "source")}
        artifacts[ref["id"]] = record
        known[ref["id"]] = ref["id"]
        known[str(path)] = ref["id"]
    return artifacts, known


def _inspect_browser_qa(record: Dict[str, Any], roots: Sequence[str]) -> Dict[str, Any]:
    if record["status"] != PASS:
        return {"status": BLOCKED, "reason": record.get("reason", "Browser QA receipt unavailable")}
    raw = _read_json(record["resolved_path"], "browser QA receipt %s" % record["id"])
    overall = raw.get("overall")
    if overall not in {PASS, FAIL, BLOCKED}:
        raise ReplayInputError("browser QA receipt %s has no supported overall status" % record["id"])
    checks = {"receipt_sha256": record["sha256"], "overall": overall,
              "engine": raw.get("engine"), "real_browser": raw.get("engine_real_browser") is True,
              "screenshot_files": 0, "screenshot_status": NOT_RUN}
    visual = raw.get("visual_evidence")
    if isinstance(visual, dict) and visual.get("required") is True:
        surfaces = visual.get("required_surfaces") or []
        screenshot_set = visual.get("screenshot_set") or []
        by_surface = {item.get("surface_id"): item for item in screenshot_set if isinstance(item, dict)}
        missing = []
        for surface in surfaces:
            item = by_surface.get(surface)
            if not item or not item.get("screenshot_path") or not item.get("screenshot_sha256"):
                missing.append(surface)
                continue
            expected = _require_sha(item["screenshot_sha256"], "browser screenshot %s sha256" % surface)
            try:
                shot = _resolve_receipt_path(record["resolved_path"], item["screenshot_path"],
                                             roots, "browser screenshot %s path" % surface)
            except MissingEvidence:
                missing.append(surface)
                continue
            if _sha256(shot) != expected:
                raise IntegrityError("browser screenshot %s hash mismatch" % surface)
            checks["screenshot_files"] += 1
        checks["screenshot_status"] = PASS if not missing else BLOCKED
        if missing:
            return {"status": BLOCKED, "reason": "missing rendered screenshot evidence: %s" % ", ".join(missing),
                    "checks": checks, "overall": overall}
    if not checks["real_browser"]:
        return {"status": BLOCKED, "reason": "receipt is not declared REAL_BROWSER", "checks": checks,
                "overall": overall}
    return {"status": overall, "reason": "Imported historical Browser QA receipt; no browser was started.",
            "checks": checks, "overall": overall}


def _inspect_motion(record: Dict[str, Any], roots: Sequence[str]) -> Dict[str, Any]:
    if record["status"] != PASS:
        return {"status": BLOCKED, "reason": record.get("reason", "motion receipt unavailable")}
    raw = _read_json(record["resolved_path"], "motion receipt %s" % record["id"])
    if raw.get("engine") != "playwright" or raw.get("browser") not in {"chromium", "chrome"}:
        return {"status": BLOCKED, "reason": "motion receipt is not declared real-browser Chromium evidence"}
    checks = {"receipt_sha256": record["sha256"], "video": NOT_RUN, "frames": 0,
              "steps": len(raw.get("steps") or [])}
    video = raw.get("video") if isinstance(raw.get("video"), dict) else None
    if not video or not video.get("path") or not video.get("sha256"):
        return {"status": BLOCKED, "reason": "motion receipt has no hash-bound video", "checks": checks}
    expected = _require_sha(video["sha256"], "motion video sha256")
    try:
        video_path = _resolve_receipt_path(record["resolved_path"], video["path"], roots,
                                           "motion video path")
    except MissingEvidence as exc:
        return {"status": BLOCKED, "reason": str(exc), "checks": checks}
    if _sha256(video_path) != expected:
        raise IntegrityError("motion video hash mismatch")
    checks["video"] = PASS
    for step in raw.get("steps") or []:
        if not isinstance(step, dict) or not step.get("frame") or not step.get("frame_sha256"):
            return {"status": BLOCKED, "reason": "motion step lacks a hash-bound frame", "checks": checks}
        frame_hash = _require_sha(step["frame_sha256"], "motion frame sha256")
        try:
            frame_path = _resolve_receipt_path(record["resolved_path"], step["frame"], roots,
                                               "motion frame path")
        except MissingEvidence as exc:
            return {"status": BLOCKED, "reason": str(exc), "checks": checks}
        if _sha256(frame_path) != frame_hash:
            raise IntegrityError("motion frame hash mismatch: %s" % step["frame"])
        checks["frames"] += 1
    if checks["steps"] == 0:
        return {"status": BLOCKED, "reason": "motion receipt contains no timeline steps", "checks": checks}
    return {"status": PASS, "reason": "Imported historical motion receipt; no browser was started.",
            "checks": checks}


def _bind_evidence(repo_root: str, roots: Sequence[str], raw: Any) -> Dict[str, Dict[str, Any]]:
    refs = _validate_ref_list(raw, "evidence")
    evidence: Dict[str, Dict[str, Any]] = {}
    for ref in refs:
        path = ref.get("path")
        kind = str(ref.get("kind", "artifact")).lower()
        source_url = ref.get("source_url")
        if source_url and not path:
            if not isinstance(source_url, str) or not source_url.lower().startswith(_URL_PREFIXES[:2]):
                raise ReplayInputError("evidence %s has an unsupported source URL" % ref["id"])
            evidence[ref["id"]] = {**ref, "id": ref["id"], "kind": kind, "path": None,
                                    "status": BLOCKED, "reason": "URL-only reference was not fetched.",
                                    "source_url": source_url}
            continue
        if not path:
            evidence[ref["id"]] = {**ref, "id": ref["id"], "kind": kind, "path": None,
                                    "status": BLOCKED, "reason": "No local evidence path was supplied."}
            continue
        digest = _require_sha(ref.get("sha256"), "evidence %s sha256" % ref["id"])
        try:
            resolved = _resolve_local(repo_root, roots, path, "evidence %s path" % ref["id"])
            actual = _sha256(resolved)
            if actual != digest:
                raise IntegrityError("evidence %s hash mismatch" % ref["id"])
            record = {**ref, "id": ref["id"], "kind": kind, "path": path,
                      "resolved_path": resolved, "sha256": digest, "status": PASS}
        except MissingEvidence as exc:
            record = {**ref, "id": ref["id"], "kind": kind, "path": path,
                      "resolved_path": None, "sha256": digest, "status": BLOCKED,
                      "reason": str(exc)}
        if record["status"] == PASS and kind in {"browser_qa", "browser-qa", "qa"}:
            record.update(_inspect_browser_qa(record, roots))
        elif record["status"] == PASS and kind in {"motion", "motion_receipt"}:
            record.update(_inspect_motion(record, roots))
        elif record["status"] == PASS and kind in {"observation", "assessment", "critique"}:
            record["status"] = PASS
        evidence[ref["id"]] = record
    return evidence


def _looks_like_image(path: Optional[str]) -> bool:
    """Recognize a local image artifact without depending on an image library."""

    if not path:
        return False
    try:
        with open(path, "rb") as fh:
            head = fh.read(512)
    except OSError:
        return False
    if head.startswith(b"\x89PNG\r\n\x1a\n") or head.startswith(b"\xff\xd8\xff"):
        return True
    if head.startswith((b"GIF87a", b"GIF89a")):
        return True
    if head.startswith(b"RIFF") and b"WEBP" in head[:16]:
        return True
    if os.path.splitext(path)[1].lower() == ".svg":
        try:
            text = head.decode("utf-8", errors="ignore").casefold()
        except UnicodeError:
            return False
        return "<svg" in text
    return False


def _normalized_evidence_id(raw: Any, evidence: Mapping[str, Any]) -> Optional[str]:
    if not isinstance(raw, str):
        return None
    if raw in evidence:
        return raw
    for prefix in ("evidence:", "artifact:"):
        if raw.startswith(prefix) and raw.removeprefix(prefix) in evidence:
            return raw.removeprefix(prefix)
    return None


def _quality_evidence_status(item: Mapping[str, Any], evidence_type: str) -> Tuple[str, str]:
    """Return whether one evidence item can support a quality claim.

    A hash-bound file is traceability, not rendered proof. Render evidence also
    needs a real-browser identity, a viewport/surface identity, and an image
    payload. Browser-QA receipts must independently report a complete real-
    browser screenshot set.
    """

    if item.get("status") != PASS:
        return BLOCKED, str(item.get("reason", "evidence is unavailable"))
    kind = str(item.get("kind", "")).casefold().replace("-", "_")
    requested = str(evidence_type).casefold().replace("-", "_")
    if requested in {"rendered_capture", "rendered_screenshot", "rendered_visual"}:
        if kind in {"browser_qa", "browserqa", "qa"}:
            checks = item.get("checks") if isinstance(item.get("checks"), dict) else {}
            if checks.get("real_browser") is True and checks.get("screenshot_status") == PASS:
                return PASS, "real-browser Browser QA receipt includes a complete screenshot set"
            return BLOCKED, "Browser QA receipt is not a complete real-browser screenshot set"
        if kind not in {"rendered_capture", "rendered_screenshot", "screenshot",
                        "visual_evidence", "visual"}:
            return BLOCKED, "evidence kind is not a rendered capture"
        if item.get("actual_rendered") is not True:
            return BLOCKED, "rendered capture is not marked actual_rendered"
        if str(item.get("engine_identity", "")).upper() != "REAL_BROWSER":
            return BLOCKED, "rendered capture is not identified as REAL_BROWSER evidence"
        if not isinstance(item.get("viewport"), int) or item.get("viewport") <= 0:
            return BLOCKED, "rendered capture has no positive viewport identity"
        if not item.get("surface_id"):
            return BLOCKED, "rendered capture has no named surface identity"
        if not _looks_like_image(item.get("resolved_path")):
            return BLOCKED, "rendered capture does not resolve to an image artifact"
        return PASS, "hash-bound real-browser rendered capture"
    if requested in {"image_asset", "asset", "visible_asset"}:
        if kind not in {"image_asset", "asset", "image", "svg_asset"}:
            return BLOCKED, "evidence kind is not a local image asset"
        if not _looks_like_image(item.get("resolved_path")):
            return BLOCKED, "image asset does not resolve to a readable image artifact"
        return PASS, "hash-bound local image asset artifact"
    if requested in {"motion_recording", "motion", "motion_receipt"}:
        if kind not in {"motion", "motion_receipt", "motion_recording"}:
            return BLOCKED, "evidence kind is not a motion recording/receipt"
        checks = item.get("checks") if isinstance(item.get("checks"), dict) else {}
        if checks.get("video") != PASS and kind != "motion_recording":
            return BLOCKED, "motion receipt has no hash-bound recording"
        return PASS, "hash-bound motion evidence"
    raise ReplayInputError("unsupported quality evidence type: %s" % evidence_type)


def _quality_refs_for_type(refs: Sequence[str], evidence: Mapping[str, Any], evidence_type: str) -> List[str]:
    supported = []
    for raw in refs:
        evidence_id = _normalized_evidence_id(raw, evidence)
        if evidence_id is None:
            continue
        status, _ = _quality_evidence_status(evidence[evidence_id], evidence_type)
        if status == PASS:
            supported.append(evidence_id)
    return supported


def _canonical_dimension(raw: Any) -> str:
    value = str(raw or "").strip().upper().replace("-", "_").replace(" ", "_")
    aliases = {
        "BRIEF_AND_BRAND": "BRIEF_AND_BRAND_FIDELITY",
        "BRAND_FIDELITY": "BRIEF_AND_BRAND_FIDELITY",
        "TYPOGRAPHY_QUALITY": "TYPOGRAPHY",
        "COMPOSITION": "COMPOSITION_AND_ART_DIRECTION",
        "ART_DIRECTION": "COMPOSITION_AND_ART_DIRECTION",
        "IMAGERY": "IMAGERY_AND_VISUAL_WORLD",
        "VISUAL_WORLD": "IMAGERY_AND_VISUAL_WORLD",
        "RENDERED_DESIGN_DISTINCTIVENESS": "PREMIUM_DISTINCTIVENESS",
        "DISTINCTIVENESS": "PREMIUM_DISTINCTIVENESS",
        "MEMORY": "MEMORABILITY",
        "POLISH": "POLISH_AND_CRAFT",
        "RESPONSIVE": "RESPONSIVE_QUALITY",
        "CONVERSION": "CONVERSION_CLARITY",
        "MOTION": "MOTION_QUALITY",
    }
    return aliases.get(value, value)


def _canonical_pairwise_dimension(raw: Any) -> str:
    value = str(raw or "").strip().upper().replace("-", "_").replace(" ", "_")
    aliases = {
        "FIRST_IMPRESSION_QUALITY": "FIRST_IMPRESSION",
        "VISUAL_WORLD": "VISUAL_WORLD_IMAGERY",
        "VISUAL_WORLD_AND_IMAGERY": "VISUAL_WORLD_IMAGERY",
        "POLISH_AND_CRAFT": "CRAFT",
        "INTERACTION_QUALITY": "INTERACTION",
    }
    return aliases.get(value, value)


def evaluate_pairwise_visual_gate(
    receipt: Mapping[str, Any],
    required_dimensions: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    """Validate the forced-choice A/B/AMBIGUOUS visual-gate receipt.

    This is evidence validation, not a model or browser call.  A receipt must
    name the approved anchor (A), rejected anchor (B), and candidate render (C)
    for every applicable dimension and provide exactly three observable
    discrepancies.  Numeric scores may be carried as telemetry but never
    change the pairwise verdict.
    """

    if not isinstance(receipt, Mapping):
        return {"status": BLOCKED, "provenance": "MISSING", "verdict": "UNASSESSED",
                "issues": ["pairwise visual receipt must be an object"]}
    requested = required_dimensions or receipt.get("required_dimensions") or PAIRWISE_DEFAULT_DIMENSIONS
    if not isinstance(requested, Sequence) or isinstance(requested, (str, bytes)):
        return {"status": INVALID, "provenance": "INVALID", "verdict": "UNASSESSED",
                "issues": ["required_dimensions must be a list"]}
    dimensions = receipt.get("dimensions")
    if not isinstance(dimensions, list):
        return {"status": BLOCKED, "provenance": "MISSING", "verdict": "UNASSESSED",
                "issues": ["pairwise receipt must contain dimensions"]}
    by_dimension: Dict[str, Mapping[str, Any]] = {}
    issues: List[str] = []
    for item in dimensions:
        if not isinstance(item, Mapping):
            issues.append("pairwise dimension must be an object")
            continue
        dimension = _canonical_pairwise_dimension(item.get("dimension") or item.get("id"))
        if dimension not in PAIRWISE_DIMENSIONS:
            issues.append("unsupported pairwise dimension: %s" % dimension)
            continue
        if dimension in by_dimension:
            issues.append("duplicate pairwise dimension: %s" % dimension)
            continue
        by_dimension[dimension] = item
    applicable = []
    for raw_dimension in requested:
        dimension = _canonical_pairwise_dimension(raw_dimension)
        item = by_dimension.get(dimension)
        if item is None:
            issues.append("missing pairwise dimension: %s" % dimension)
            continue
        if item.get("applicable", True) is False:
            continue
        applicable.append(dimension)
        anchors = item.get("anchors")
        if not isinstance(anchors, Mapping):
            anchors = {"A": item.get("image_a"), "B": item.get("image_b"), "C": item.get("image_c")}
        if any(not isinstance(anchors.get(key), str) or not anchors.get(key).strip() for key in ("A", "B", "C")):
            issues.append("%s must name image A, image B, and candidate image C" % dimension)
        choice = str(item.get("choice") or item.get("verdict") or "").strip().upper()
        if choice not in PAIRWISE_CHOICES:
            issues.append("%s must return A, B, or AMBIGUOUS" % dimension)
        discrepancies = item.get("discrepancies")
        if not isinstance(discrepancies, list) or len(discrepancies) != 3 or any(not isinstance(value, str) or not value.strip() for value in discrepancies):
            issues.append("%s must contain exactly 3 observable discrepancies" % dimension)
    if not applicable and not issues:
        issues.append("pairwise receipt has no applicable dimensions")
    if issues:
        return {"status": INVALID if any(item.startswith("unsupported") or item.startswith("duplicate") for item in issues) else BLOCKED,
                "provenance": "INVALID" if any(item.startswith("unsupported") or item.startswith("duplicate") for item in issues) else "INCOMPLETE",
                "verdict": "UNASSESSED", "issues": issues,
                "numeric_telemetry": receipt.get("numeric_score")}
    choices = [str(by_dimension[dimension].get("choice") or by_dimension[dimension].get("verdict")).strip().upper() for dimension in applicable]
    if "B" in choices:
        verdict = "CLOSER_TO_REJECTED"
        status = FAIL
    elif "AMBIGUOUS" in choices:
        verdict = "AMBIGUOUS"
        status = BLOCKED
    else:
        verdict = "CLOSER_TO_APPROVED"
        status = PASS
    return {
        "status": status,
        "provenance": "EVIDENCE_BOUND_PAIRWISE",
        "verdict": verdict,
        "dimensions": applicable,
        "choices": dict((dimension, str(by_dimension[dimension].get("choice") or by_dimension[dimension].get("verdict")).strip().upper()) for dimension in applicable),
        "numeric_telemetry": receipt.get("numeric_score"),
        "issues": [],
    }


def _historical_claim_classification(case: Mapping[str, Any]) -> Dict[str, Any]:
    raw = case.get("historical_quality_claims")
    if raw is None:
        raw = case.get("historical_claims")
    if raw is None:
        inferred = []
        for field in ("quality_score", "quality_verdict", "design_qa_score", "design_qa_verdict",
                      "gauntlet_status", "asset_verified", "distinctiveness_complete",
                      "signature_element_declared"):
            if field in case:
                inferred.append({"field": field, "value": case[field],
                                 "classification": LEGACY_UNSUBSTANTIATED_QUALITY_CLAIM,
                                 "reason": "Recorded declaration has no current evidence-bound quality receipt."})
        raw = inferred
    if not isinstance(raw, list):
        raise ReplayInputError("historical_quality_claims must be a list")
    claims = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict) or not isinstance(item.get("field"), str):
            raise ReplayInputError("historical_quality_claims[%d] needs a field" % index)
        classification = item.get("classification", HISTORICAL_RECORDED_CLAIM)
        if not isinstance(classification, str) or not classification:
            raise ReplayInputError("historical_quality_claims[%d] has no classification" % index)
        claims.append({**item, "classification": classification,
                       "trust": "NOT_CURRENT_EVAL_BASELINE"})
    if not claims:
        return {"status": NOT_APPLICABLE, "claims": [],
                "reason": "No historical quality claims were supplied."}
    return {
        "status": HISTORICAL_RECORDED_CLAIM,
        "claims": claims,
        "reason": "Historical values are preserved for auditability and are not trusted as current quality baselines.",
    }


def _evaluate_design_proposal(case: Mapping[str, Any], artifacts: Mapping[str, Any],
                              evidence: Mapping[str, Any], known: set) -> Dict[str, Any]:
    config = case.get("design_proposal")
    if config is None:
        config = case.get("proposal")
    if config is None:
        return {"status": NOT_APPLICABLE, "provenance": "NOT_APPLICABLE",
                "criteria": [], "name": DESIGN_PROPOSAL_COMPLETENESS,
                "reason": "No design-proposal completeness assessment was declared."}
    if not isinstance(config, dict):
        raise ReplayInputError("design_proposal must be an object")
    criteria = config.get("criteria") or config.get("requirements")
    if not isinstance(criteria, list) or not criteria:
        raise ReplayInputError("design_proposal.criteria must be a non-empty list")
    rendered = []
    status = PASS
    ids = set()
    for index, criterion in enumerate(criteria):
        if not isinstance(criterion, dict) or not isinstance(criterion.get("id"), str):
            raise ReplayInputError("design_proposal criterion %d needs an id" % index)
        criterion_id = criterion["id"]
        if criterion_id in ids:
            raise ReplayInputError("duplicate design_proposal criterion: %s" % criterion_id)
        ids.add(criterion_id)
        criterion_status, detail, refs = _evaluate_assertion(
            criterion.get("assertion"), artifacts, evidence, known)
        rendered.append({"criterion_id": criterion_id, "status": criterion_status,
                         "detail": detail, "evidence_refs": refs})
        if criterion_status == FAIL:
            status = FAIL
        elif criterion_status == BLOCKED and status != FAIL:
            status = BLOCKED
    if not config.get("required", True):
        status = NOT_APPLICABLE
    return {
        "status": status,
        "provenance": "DECLARED_PROPOSAL_ARTIFACTS",
        "name": DESIGN_PROPOSAL_COMPLETENESS,
        "criteria": rendered,
        "reason": "Proposal structure is evaluated separately and cannot establish rendered distinctiveness.",
    }


def _quality_score(raw: Any, field: str) -> Optional[int]:
    if raw is None:
        return None
    if isinstance(raw, bool) or not isinstance(raw, int) or raw < 0 or raw > 10:
        raise ReplayInputError("%s must be an integer from 0 to 10" % field)
    return raw


def _breakdown_ids(raw: Any) -> List[str]:
    if isinstance(raw, dict):
        return [str(key) for key in raw]
    if isinstance(raw, list):
        ids = []
        for item in raw:
            if isinstance(item, str):
                ids.append(item)
            elif isinstance(item, dict) and isinstance(item.get("criterion_id") or item.get("id"), str):
                ids.append(item.get("criterion_id") or item.get("id"))
            else:
                raise ReplayInputError("criterion_breakdown entries need criterion ids")
        return ids
    raise ReplayInputError("criterion_breakdown must be an object or list")


def _quality_critique(case: Mapping[str, Any], config: Mapping[str, Any],
                      evidence: Mapping[str, Any], known: set) -> Dict[str, Any]:
    criteria = config.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        raise ReplayInputError("quality.criteria must be a non-empty list")
    normalized_criteria = []
    criterion_ids = set()
    for index, criterion in enumerate(criteria):
        if not isinstance(criterion, dict) or not isinstance(criterion.get("id"), str):
            raise ReplayInputError("quality criterion %d needs an id" % index)
        criterion_id = criterion["id"]
        if criterion_id in criterion_ids:
            raise ReplayInputError("duplicate quality criterion: %s" % criterion_id)
        dimension = _canonical_dimension(criterion.get("dimension") or criterion_id)
        if dimension not in QUALITY_DIMENSIONS:
            raise ReplayInputError("unsupported quality dimension: %s" % dimension)
        criterion_ids.add(criterion_id)
        applicable = str(criterion.get("applicability", "REQUIRED")).upper()
        if applicable in {"N/A", "NOT_APPLICABLE"}:
            applicable = NOT_APPLICABLE
        elif applicable not in {"REQUIRED", "OPTIONAL"}:
            raise ReplayInputError("quality criterion %s has unsupported applicability" % criterion_id)
        required_types = criterion.get("required_evidence_types")
        if required_types is None:
            required_types = criterion.get("evidence_types")
        if required_types is None:
            required_types = [] if applicable == NOT_APPLICABLE else ["rendered_capture"]
        if not isinstance(required_types, list) or any(not isinstance(item, str) for item in required_types):
            raise ReplayInputError("quality criterion %s required_evidence_types must be a list" % criterion_id)
        if dimension == "MOTION_QUALITY" and applicable != NOT_APPLICABLE and not required_types:
            required_types = ["motion_recording"]
        exception = criterion.get("owner_approved_exception")
        if dimension == "IMAGERY_AND_VISUAL_WORLD" and applicable != NOT_APPLICABLE and not exception:
            if "image_asset" not in required_types:
                required_types = list(required_types) + ["image_asset"]
        normalized_criteria.append({
            **criterion,
            "id": criterion_id,
            "dimension": dimension,
            "applicability": applicable,
            "required": criterion.get("required", criterion.get("class", "MANDATORY") == "MANDATORY"),
            "required_evidence_types": required_types,
            "required_surfaces": criterion.get("required_surfaces") or [],
        })

    rubric_version = config.get("rubric_version", QUALITY_RUBRIC_VERSION)
    if not isinstance(rubric_version, str) or not rubric_version:
        raise ReplayInputError("quality.rubric_version is required")
    if rubric_version != QUALITY_RUBRIC_VERSION:
        raise ReplayInputError("unsupported quality rubric version: %s" % rubric_version)
    critique_id = config.get("critique_evidence_id")
    if not isinstance(critique_id, str) or critique_id not in evidence:
        return {"status": BLOCKED, "provenance": "MISSING", "criteria": [], "hard_gates": [],
                "rubric_version": rubric_version, "claim_classification": "UNVERIFIED_QUALITY_CLAIM",
                "quality_bar_status": "BLOCKED",
                "reason": "No hash-bound quality critic receipt was supplied."}
    critique_ref = evidence[critique_id]
    if critique_ref.get("status") != PASS:
        return {"status": BLOCKED, "provenance": "MISSING", "criteria": [], "hard_gates": [],
                "rubric_version": rubric_version, "claim_classification": "UNVERIFIED_QUALITY_CLAIM",
                "quality_bar_status": "BLOCKED", "critic_receipt_id": critique_id,
                "reason": critique_ref.get("reason", "quality critic receipt is unavailable")}
    raw = _read_json(critique_ref["resolved_path"], "quality critique %s" % critique_id)
    if raw.get("critique_version") is None:
        raise ReplayInputError("quality critique is missing critique_version")
    if raw.get("rubric_version") != rubric_version:
        raise ReplayInputError("quality critique rubric_version does not match the manifest")
    if raw.get("case_id") != case.get("id") or raw.get("case_version") != case.get("case_version"):
        raise ReplayInputError("quality critique case identity does not match the manifest")
    if raw.get("specimen_id") != (case.get("specimen") or {}).get("id"):
        raise ReplayInputError("quality critique specimen identity does not match the manifest")

    pairwise_config = config.get("pairwise_visual_gate")
    pairwise_required = False
    pairwise_dimensions = None
    if pairwise_config is not None:
        if isinstance(pairwise_config, bool):
            pairwise_required = pairwise_config
        elif isinstance(pairwise_config, dict):
            pairwise_required = pairwise_config.get("required", True)
            if not isinstance(pairwise_required, bool):
                raise ReplayInputError("quality.pairwise_visual_gate.required must be boolean")
            pairwise_dimensions = pairwise_config.get("dimensions") or pairwise_config.get("required_dimensions")
            if pairwise_dimensions is not None and (not isinstance(pairwise_dimensions, list)
                                                     or any(not isinstance(item, str) for item in pairwise_dimensions)):
                raise ReplayInputError("quality.pairwise_visual_gate dimensions must be a list of strings")
        else:
            raise ReplayInputError("quality.pairwise_visual_gate must be an object or boolean")
    pairwise_result = None
    if pairwise_required:
        pairwise_receipt = raw.get("pairwise_visual_gate")
        if isinstance(pairwise_receipt, dict) and isinstance(pairwise_receipt.get("receipt"), dict):
            pairwise_receipt = pairwise_receipt["receipt"]
        pairwise_result = evaluate_pairwise_visual_gate(pairwise_receipt, required_dimensions=pairwise_dimensions)

    provenance_missing = []
    critic_identity = raw.get("specimen_hash") or raw.get("evidence_identity")
    expected_identity = (case.get("specimen") or {}).get("specimen_hash")
    if not isinstance(critic_identity, str) or not critic_identity.strip():
        provenance_missing.append("specimen_hash_or_evidence_identity")
    elif expected_identity and critic_identity != expected_identity:
        raise IntegrityError("quality critique specimen/evidence identity does not match the manifest")
    evidence_files = raw.get("evidence_files")
    if not isinstance(evidence_files, list) or not evidence_files:
        provenance_missing.append("evidence_files")
        evidence_files = []
    else:
        evidence_files = _check_citations(evidence_files, known, "quality critique evidence_files")
    breakdown = raw.get("criterion_breakdown")
    if breakdown is None:
        provenance_missing.append("criterion_breakdown")
    else:
        breakdown_ids = _breakdown_ids(breakdown)
        if set(breakdown_ids) != criterion_ids or len(breakdown_ids) != len(criterion_ids):
            raise ReplayInputError("quality critique criterion_breakdown does not cover the manifest")
    findings = raw.get("criterion_findings")
    if findings is None:
        findings = raw.get("findings")
    if not isinstance(findings, list):
        raise ReplayInputError("quality critique criterion_findings must be a list")
    critic_context = raw.get("critic_context")
    if not isinstance(critic_context, dict) or not isinstance(critic_context.get("context_id"), str) \
            or not critic_context.get("context_id").strip():
        provenance_missing.append("critic_context")
        critic_context = critic_context if isinstance(critic_context, dict) else {}
    limitations = raw.get("limitations")
    if not isinstance(limitations, list) or any(not isinstance(item, str) for item in limitations):
        provenance_missing.append("limitations")
        limitations = []
    if not isinstance(raw.get("timestamp"), str) or not raw.get("timestamp").strip():
        provenance_missing.append("timestamp")

    by_id = {}
    for finding in findings:
        if not isinstance(finding, dict):
            raise ReplayInputError("quality critique findings must be objects")
        finding_id = finding.get("criterion_id") or finding.get("id")
        if finding_id not in criterion_ids:
            raise ReplayInputError("quality critique cites an unknown criterion")
        if finding_id in by_id:
            raise ReplayInputError("duplicate quality critique finding: %s" % finding_id)
        finding_status = finding.get("status")
        if finding_status not in QUALITY_FINDING_STATUSES:
            raise ReplayInputError("quality critique finding has an unsupported status")
        refs = finding.get("evidence_refs")
        if refs is None:
            refs = []
        refs = _check_citations(refs, known, "quality critique %s evidence_refs" % finding_id)
        by_id[finding_id] = dict(finding, criterion_id=finding_id, evidence_refs=refs)
    missing_findings = sorted(criterion_ids - set(by_id))
    if missing_findings:
        raise ReplayInputError("quality critique is missing criteria: %s" % ", ".join(missing_findings))

    reviewer = raw.get("reviewer") if isinstance(raw.get("reviewer"), dict) else {}
    role = str(reviewer.get("role", "")).casefold()
    independence = reviewer.get("independence")
    independent_values = {"INDEPENDENT", "DECLARED_INDEPENDENT", "SEPARATE_CONTEXT"}
    independent = independence in independent_values and role not in {"builder", "owner", "builder_agent"}
    builder_context = raw.get("builder_context_id") or critic_context.get("builder_context_id")
    if builder_context and builder_context == critic_context.get("context_id"):
        independent = False
    if config.get("requires_independent", True) and not independent:
        provenance_missing.append("independent_critic_context")

    minimum = 8
    quality_bar = config.get("quality_bar")
    if isinstance(quality_bar, dict) and quality_bar.get("minimum_score") is not None:
        minimum = quality_bar.get("minimum_score")
    if isinstance(minimum, bool) or not isinstance(minimum, int) or minimum < 0 or minimum > 10:
        raise ReplayInputError("quality_bar.minimum_score must be an integer from 0 to 10")

    rendered = []
    for criterion in normalized_criteria:
        finding = by_id[criterion["id"]]
        raw_status = finding["status"]
        refs = finding["evidence_refs"]
        detail = finding.get("observation") or finding.get("detail") or finding.get("reason") or ""
        limitation = finding.get("limitation") or ""
        missing_types = []
        supported_types = {}
        for evidence_type in criterion["required_evidence_types"]:
            supported = _quality_refs_for_type(refs, evidence, evidence_type)
            supported_types[evidence_type] = supported
            if not supported and criterion["applicability"] != NOT_APPLICABLE:
                missing_types.append(evidence_type)
        missing_surfaces = []
        if criterion["required_surfaces"]:
            available_surfaces = {
                evidence[ref_id].get("surface_id")
                for ref_id in {_normalized_evidence_id(ref, evidence) for ref in refs}
                if ref_id and evidence[ref_id].get("status") == PASS
            }
            missing_surfaces = [surface for surface in criterion["required_surfaces"]
                                if surface not in available_surfaces]
        effective_status = raw_status
        score = None
        evidence_blocked = bool(missing_types or missing_surfaces or not refs)
        if criterion["applicability"] == NOT_APPLICABLE:
            effective_status = NOT_APPLICABLE
            detail = detail or criterion.get("reason", "Explicitly not applicable.")
        elif evidence_blocked:
            effective_status = BLOCKED
            score = None
            reasons = []
            if not refs:
                reasons.append("no evidence_refs")
            if missing_types:
                reasons.append("missing evidence types: " + ", ".join(missing_types))
            if missing_surfaces:
                reasons.append("missing surfaces: " + ", ".join(missing_surfaces))
            detail = "; ".join(reasons)
        elif raw_status == BLOCKED:
            effective_status = BLOCKED
            score = None
        elif raw_status == NOT_APPLICABLE:
            effective_status = BLOCKED
            score = None
            detail = "Applicable quality criterion cannot be marked NOT_APPLICABLE."
        else:
            score = _quality_score(finding.get("score"), "quality finding %s score" % criterion["id"])
            if score is None:
                raise ReplayInputError("quality finding %s needs a score" % criterion["id"])
            if raw_status in {PASS, "PROVISIONAL_PASS"} and criterion["required"] and score < minimum:
                effective_status = FAIL
                detail = (detail + " " if detail else "") + \
                    "score is below the required %d/10 quality bar" % minimum
            else:
                effective_status = raw_status
        rendered.append({
            "criterion_id": criterion["id"],
            "dimension": criterion["dimension"],
            "required": bool(criterion["required"]),
            "applicability": criterion["applicability"],
            "status": effective_status,
            "score": score,
            "evidence_refs": [critique_id] + list(refs),
            "evidence_types": {key: value for key, value in supported_types.items() if value},
            "observation": finding.get("observation") or finding.get("detail") or "",
            "reason": finding.get("reason") or detail,
            "limitation": limitation,
            "missing_evidence": missing_types + missing_surfaces,
        })

    gate_config = config.get("hard_gates") or []
    if not isinstance(gate_config, list):
        raise ReplayInputError("quality.hard_gates must be a list")
    raw_gates = raw.get("hard_gate_findings")
    if raw_gates is None:
        raw_gates = raw.get("hard_gates") or []
    if not isinstance(raw_gates, list):
        raise ReplayInputError("quality critique hard_gate_findings must be a list")
    by_gate = {}
    for finding in raw_gates:
        if not isinstance(finding, dict) or not isinstance(finding.get("gate_id") or finding.get("id"), str):
            raise ReplayInputError("quality hard-gate findings need gate ids")
        gate_id = finding.get("gate_id") or finding.get("id")
        if gate_id in by_gate:
            raise ReplayInputError("duplicate quality hard-gate finding: %s" % gate_id)
        if finding.get("status") not in {PASS, FAIL, BLOCKED, NOT_APPLICABLE}:
            raise ReplayInputError("quality hard-gate finding has an unsupported status")
        refs = _check_citations(finding.get("evidence_refs") or [], known,
                                "quality hard-gate %s evidence_refs" % gate_id)
        by_gate[gate_id] = dict(finding, gate_id=gate_id, evidence_refs=refs)
    gates = []
    for gate in gate_config:
        if not isinstance(gate, dict) or not isinstance(gate.get("id"), str):
            raise ReplayInputError("quality hard-gates need ids")
        gate_id = gate["id"]
        finding = by_gate.get(gate_id)
        required_types = gate.get("required_evidence_types") or ["rendered_capture"]
        if finding is None:
            gates.append({"gate_id": gate_id, "status": BLOCKED, "evidence_refs": [critique_id],
                          "reason": "No hard-gate finding was supplied."})
            continue
        refs = finding["evidence_refs"]
        missing_gate_types = [kind for kind in required_types
                              if not _quality_refs_for_type(refs, evidence, kind)]
        gate_status = finding["status"]
        reason = finding.get("observation") or finding.get("detail") or finding.get("reason") or ""
        if not refs or missing_gate_types:
            gate_status = BLOCKED
            reason = "missing hard-gate evidence: " + ", ".join(missing_gate_types or ["evidence_refs"])
        gates.append({"gate_id": gate_id, "status": gate_status, "evidence_refs": [critique_id] + refs,
                      "reason": reason, "limitation": finding.get("limitation") or ""})
    for extra in sorted(set(by_gate) - {gate["id"] for gate in gate_config if isinstance(gate, dict)}):
        raise ReplayInputError("quality critique cites an unknown hard gate: %s" % extra)

    if provenance_missing:
        status = BLOCKED
        bar_status = "BLOCKED"
        reason = "Quality score provenance is incomplete: " + ", ".join(sorted(set(provenance_missing)))
    elif pairwise_result is not None and pairwise_result.get("status") in {BLOCKED, INVALID}:
        status = BLOCKED
        bar_status = "BLOCKED"
        reason = "Pairwise visual taste evidence is incomplete or invalid."
    elif pairwise_result is not None and pairwise_result.get("status") == FAIL:
        status = FAIL
        bar_status = "NOT_MET"
        reason = "Pairwise visual taste gate placed the candidate closer to the rejected anchor."
    elif any(item["status"] == FAIL for item in rendered) or any(item["status"] == FAIL for item in gates):
        status = FAIL
        bar_status = "NOT_MET"
        reason = "At least one quality criterion or hard gate failed with evidence."
    elif any(item["status"] == BLOCKED for item in rendered) or any(item["status"] == BLOCKED for item in gates):
        status = BLOCKED
        bar_status = "BLOCKED"
        reason = "Required rendered evidence or hard-gate evidence is unavailable."
    else:
        status = PASS
        bar_status = "MET"
        reason = "All applicable required dimensions met the no-averaging quality bar."
    claim = CURRENTLY_EVIDENCE_VERIFIED_RESULT if status in {PASS, FAIL} else "UNVERIFIED_QUALITY_CLAIM"
    return {
        "status": status,
        "provenance": "EVIDENCE_BOUND_CRITIQUE" if not provenance_missing else "BLOCKED_MISSING_PROVENANCE",
        "claim_classification": claim,
        "rubric_version": rubric_version,
        "critic_receipt_id": critique_id,
        "critic_receipt_sha256": critique_ref.get("sha256"),
        "specimen_hash": critic_identity,
        "evidence_files": evidence_files,
        "criterion_breakdown": breakdown,
        "criteria": rendered,
        "hard_gates": gates,
        "critic_context": critic_context,
        "reviewer": reviewer,
        "limitations": limitations,
        "pairwise_visual_gate": pairwise_result,
        "quality_bar": {
            "minimum_score": minimum,
            "no_averaging": True,
            "pairwise_authority": pairwise_required,
            "numeric_score_telemetry_only": pairwise_required,
        },
        "quality_bar_status": bar_status,
        "reason": reason,
    }


def _evaluate_quality(case: Mapping[str, Any], artifacts: Mapping[str, Any],
                      evidence: Mapping[str, Any], known: set) -> Dict[str, Any]:
    config = case.get("quality")
    if config is None:
        config = case.get("quality_evaluation")
    if config is None:
        return {"status": NOT_APPLICABLE, "provenance": "NOT_APPLICABLE",
                "claim_classification": "NOT_APPLICABLE", "rubric_version": None,
                "criteria": [], "hard_gates": [], "reason": "No premium quality evaluation was declared."}
    if not isinstance(config, dict):
        raise ReplayInputError("quality must be an object")
    if config.get("required", True) is False:
        return {"status": NOT_APPLICABLE, "provenance": "NOT_APPLICABLE",
                "claim_classification": "NOT_APPLICABLE", "rubric_version": config.get("rubric_version"),
                "criteria": [], "hard_gates": [], "reason": "Quality evaluation is explicitly not required."}
    return _quality_critique(case, config, evidence, known)


def _known_refs(artifacts: Mapping[str, Any], evidence: Mapping[str, Any]) -> set:
    return set(artifacts) | set(evidence) | {"artifact:%s" % key for key in artifacts} | \
        {"evidence:%s" % key for key in evidence}


def _check_citations(values: Any, known: set, field: str) -> List[str]:
    if values is None:
        return []
    if not isinstance(values, list) or any(not isinstance(item, str) for item in values):
        raise ReplayInputError("%s must be a list of reference ids" % field)
    def supported(item: str) -> bool:
        if item in known:
            return True
        if item.startswith("artifact:"):
            return item.removeprefix("artifact:") in known
        if item.startswith("evidence:"):
            return item.removeprefix("evidence:") in known
        return False

    unknown = [item for item in values if not supported(item)]
    if unknown:
        raise ReplayInputError("%s cites unsupported evidence: %s" % (field, ", ".join(unknown)))
    return values


def _artifact_for_assertion(assertion: Mapping[str, Any], artifacts: Mapping[str, Any]) -> Dict[str, Any]:
    artifact_id = assertion.get("artifact_id")
    if not isinstance(artifact_id, str) or artifact_id not in artifacts:
        raise ReplayInputError("artifact_text assertion cites an unknown artifact")
    return artifacts[artifact_id]


def _evaluate_assertion(assertion: Any, artifacts: Mapping[str, Any], evidence: Mapping[str, Any],
                        known: set) -> Tuple[str, str, List[str]]:
    if not isinstance(assertion, dict):
        raise ReplayInputError("requirement assertion must be an object")
    kind = assertion.get("type")
    if kind == "artifact_text":
        artifact = _artifact_for_assertion(assertion, artifacts)
        if artifact["status"] != PASS:
            return BLOCKED, artifact.get("reason", "artifact unavailable"), [artifact["id"]]
        try:
            with open(artifact["resolved_path"], "r", encoding="utf-8") as fh:
                text = fh.read()
        except (OSError, UnicodeError) as exc:
            return BLOCKED, "artifact could not be read: %s" % exc, [artifact["id"]]
        folded = text.casefold()
        required = assertion.get("all_of", [])
        forbidden = assertion.get("none_of", [])
        if not isinstance(required, list) or not isinstance(forbidden, list):
            raise ReplayInputError("artifact_text all_of/none_of must be lists")
        missing = [term for term in required if not isinstance(term, str) or term.casefold() not in folded]
        present = [term for term in forbidden if not isinstance(term, str) or term.casefold() in folded]
        if present:
            return FAIL, "forbidden brief/brand text present: %s" % ", ".join(map(str, present)), [artifact["id"]]
        if missing:
            return FAIL, "required brief/brand text missing: %s" % ", ".join(map(str, missing)), [artifact["id"]]
        return PASS, "artifact text matched the declared requirement", [artifact["id"]]
    if kind == "evidence_status":
        evidence_id = assertion.get("evidence_id")
        if evidence_id not in evidence:
            raise ReplayInputError("evidence_status cites unknown evidence: %s" % evidence_id)
        item = evidence[evidence_id]
        status = item.get("status", BLOCKED)
        acceptable = assertion.get("acceptable_statuses", [PASS])
        if not isinstance(acceptable, list):
            raise ReplayInputError("acceptable_statuses must be a list")
        if status == PASS and PASS in acceptable:
            return PASS, item.get("reason", "evidence status PASS"), [evidence_id]
        if status == FAIL or item.get("overall") == FAIL:
            return FAIL, item.get("reason", "imported evidence reported FAIL"), [evidence_id]
        if status == NOT_APPLICABLE:
            return NOT_APPLICABLE, item.get("reason", "evidence not applicable"), [evidence_id]
        return BLOCKED, item.get("reason", "required evidence is unavailable or blocked"), [evidence_id]
    if kind == "evidence_presence":
        ids = assertion.get("evidence_ids")
        if not isinstance(ids, list) or not ids:
            raise ReplayInputError("evidence_presence needs evidence_ids")
        for evidence_id in ids:
            if evidence_id not in evidence:
                raise ReplayInputError("evidence_presence cites unknown evidence: %s" % evidence_id)
        blocked = [evidence_id for evidence_id in ids if evidence[evidence_id].get("status") != PASS]
        if blocked:
            return BLOCKED, "required evidence is unavailable: %s" % ", ".join(blocked), ids
        return PASS, "all declared evidence files are hash-bound", ids
    if kind == "reference_presence":
        ids = assertion.get("evidence_ids")
        if not isinstance(ids, list) or not ids:
            raise ReplayInputError("reference_presence needs evidence_ids")
        for evidence_id in ids:
            if evidence_id not in evidence:
                raise ReplayInputError("reference_presence cites unknown evidence: %s" % evidence_id)
        blocked = [evidence_id for evidence_id in ids if evidence[evidence_id].get("status") != PASS]
        if blocked:
            return BLOCKED, "reference evidence is missing or URL-only: %s" % ", ".join(blocked), ids
        return PASS, "reference evidence is locally available and hash-bound", ids
    if kind == "evidence_observation":
        evidence_id = assertion.get("evidence_id")
        if evidence_id not in evidence:
            raise ReplayInputError("evidence_observation cites unknown evidence: %s" % evidence_id)
        item = evidence[evidence_id]
        if item.get("status") != PASS:
            return BLOCKED, item.get("reason", "observation unavailable"), [evidence_id]
        raw = _read_json(item["resolved_path"], "observation %s" % evidence_id)
        status = raw.get("status") or raw.get("observation_status") or raw.get("verdict")
        if status not in VALID_ASSESSMENT_STATUSES:
            raise ReplayInputError("observation %s has no supported status" % evidence_id)
        citations = _check_citations(raw.get("evidence_refs"), known, "observation %s evidence_refs" % evidence_id)
        refs = [evidence_id] + citations
        detail = raw.get("detail") or raw.get("reason") or "Imported observation status: %s" % status
        return status, detail, refs
    raise ReplayInputError("unsupported assertion type: %s" % kind)


def _evaluate_qualitative(case: Mapping[str, Any], artifacts: Mapping[str, Any],
                          evidence: Mapping[str, Any], known: set) -> Dict[str, Any]:
    config = case.get("qualitative") or {}
    if not isinstance(config, dict):
        raise ReplayInputError("qualitative must be an object")
    criteria = config.get("criteria") or []
    if not isinstance(criteria, list):
        raise ReplayInputError("qualitative.criteria must be a list")
    if not criteria:
        return {"status": NOT_APPLICABLE, "provenance": "NOT_APPLICABLE", "criteria": [],
                "independence": "UNKNOWN", "reason": "No qualitative criteria declared."}
    criterion_ids = []
    for item in criteria:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ReplayInputError("each qualitative criterion needs an id")
        if item["id"] in criterion_ids:
            raise ReplayInputError("duplicate qualitative criterion: %s" % item["id"])
        criterion_ids.append(item["id"])
    critique_id = config.get("critique_evidence_id")
    if not critique_id:
        return {"status": BLOCKED, "provenance": "MISSING", "criteria": [], "independence": "UNKNOWN",
                "reason": "No critique receipt was supplied."}
    if critique_id not in evidence:
        raise ReplayInputError("qualitative cites unknown critique evidence: %s" % critique_id)
    critique_ref = evidence[critique_id]
    if critique_ref.get("status") != PASS:
        return {"status": BLOCKED, "provenance": "MISSING", "criteria": [], "independence": "UNKNOWN",
                "reason": critique_ref.get("reason", "critique receipt unavailable")}
    raw = _read_json(critique_ref["resolved_path"], "critique %s" % critique_id)
    if not isinstance(raw.get("critique_version"), str) or not raw.get("critique_version"):
        raise ReplayInputError("critique is missing critique_version")
    if not isinstance(raw.get("rubric_version"), str) or not raw.get("rubric_version"):
        raise ReplayInputError("critique is missing rubric_version")
    if raw.get("case_id") != case.get("id") or raw.get("case_version") != case.get("case_version"):
        raise ReplayInputError("critique case identity does not match the manifest")
    if raw.get("specimen_id") != (case.get("specimen") or {}).get("id"):
        raise ReplayInputError("critique specimen identity does not match the manifest")
    findings = raw.get("findings")
    if not isinstance(findings, list):
        raise ReplayInputError("critique findings must be a list")
    by_id = {}
    for finding in findings:
        if not isinstance(finding, dict) or finding.get("criterion_id") not in criterion_ids:
            raise ReplayInputError("critique cites an unknown qualitative criterion")
        if finding["criterion_id"] in by_id:
            raise ReplayInputError("duplicate critique finding: %s" % finding["criterion_id"])
        status = finding.get("status")
        if status not in VALID_ASSESSMENT_STATUSES:
            raise ReplayInputError("critique finding has an unsupported status")
        citations = _check_citations(finding.get("evidence_refs"), known,
                                     "critique %s evidence_refs" % finding["criterion_id"])
        by_id[finding["criterion_id"]] = dict(finding, evidence_refs=citations)
    reviewer = raw.get("reviewer") if isinstance(raw.get("reviewer"), dict) else {}
    role = str(reviewer.get("role", "")).lower()
    independence = reviewer.get("independence")
    declared_independent = independence in {"INDEPENDENT", "DECLARED_INDEPENDENT"} and role not in {"builder", "owner"}
    independence_status = "DECLARED" if declared_independent else "UNKNOWN"
    rendered = []
    status = PASS
    for criterion in criteria:
        cid = criterion["id"]
        finding = by_id.get(cid)
        if not finding:
            finding_status = BLOCKED
            detail = "No critique finding was supplied."
            refs = [critique_id]
        else:
            finding_status = finding["status"]
            detail = finding.get("detail") or "Imported critique finding: %s" % finding_status
            refs = [critique_id] + finding.get("evidence_refs", [])
        rendered.append({"criterion_id": cid, "status": finding_status, "detail": detail,
                         "evidence_refs": refs})
        if finding_status == FAIL:
            status = FAIL
        elif finding_status == BLOCKED and status != FAIL:
            status = BLOCKED
    if config.get("requires_independent", True) and independence_status != "DECLARED":
        status = BLOCKED
        reason = "Critique provenance is not independently declared; it cannot become owner approval."
    else:
        reason = "Imported critique validated; it remains calibration input, not ground truth."
    return {"status": status, "provenance": "IMPORTED_CRITIQUE", "criteria": rendered,
            "independence": independence_status, "reviewer": reviewer, "reason": reason}


def _evaluate_case(case: Mapping[str, Any], repo_root: str, roots: Sequence[str]) -> Dict[str, Any]:
    if not isinstance(case, dict) or not isinstance(case.get("id"), str) or not case.get("id"):
        raise ReplayInputError("each case needs a non-empty id")
    case_version = case.get("case_version")
    if not isinstance(case_version, str) or not case_version:
        raise ReplayInputError("case %s needs case_version" % case["id"])
    specimen = case.get("specimen")
    if not isinstance(specimen, dict) or not isinstance(specimen.get("id"), str):
        raise ReplayInputError("case %s needs a specimen id" % case["id"])
    kind = specimen.get("kind", "REAL_ARTIFACT")
    if kind not in {"REAL_ARTIFACT", "SYNTHETIC_FIXTURE"}:
        raise ReplayInputError("case %s has unsupported specimen kind" % case["id"])
    artifacts, _ = _bind_artifacts(repo_root, roots, specimen.get("artifact_files"))
    evidence = _bind_evidence(repo_root, roots, case.get("evidence"))
    known = _known_refs(artifacts, evidence)
    requirements = case.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        raise ReplayInputError("case %s needs requirements" % case["id"])
    req_ids = set()
    rendered_requirements = []
    for requirement in requirements:
        if not isinstance(requirement, dict) or not isinstance(requirement.get("id"), str):
            raise ReplayInputError("case %s has a malformed requirement" % case["id"])
        rid = requirement["id"]
        if rid in req_ids:
            raise ReplayInputError("case %s has duplicate requirement %s" % (case["id"], rid))
        req_ids.add(rid)
        req_class = requirement.get("class", "MANDATORY")
        if req_class not in {"MANDATORY", "OPTIONAL"}:
            raise ReplayInputError("requirement %s has unsupported class" % rid)
        applicability = requirement.get("applicability", "REQUIRED")
        if applicability in {"NOT_APPLICABLE", "N/A"}:
            rendered_requirements.append({"id": rid, "class": req_class, "applicability": NOT_APPLICABLE,
                                          "status": NOT_APPLICABLE,
                                          "detail": requirement.get("reason", "Explicitly not applicable."),
                                          "evidence_refs": []})
            continue
        status, detail, refs = _evaluate_assertion(requirement.get("assertion"), artifacts, evidence, known)
        rendered_requirements.append({"id": rid, "class": req_class, "applicability": applicability,
                                      "status": status, "detail": detail, "evidence_refs": refs})
    proposal = _evaluate_design_proposal(case, artifacts, evidence, known)
    qualitative = _evaluate_qualitative(case, artifacts, evidence, known)
    quality = _evaluate_quality(case, artifacts, evidence, known)
    historical_claims = _historical_claim_classification(case)
    technical_ids = case.get("technical_evidence_ids") or []
    if not isinstance(technical_ids, list):
        raise ReplayInputError("technical_evidence_ids must be a list")
    technical_items = []
    technical_status = NOT_RUN
    for evidence_id in technical_ids:
        if evidence_id not in evidence:
            raise ReplayInputError("technical evidence id is unknown: %s" % evidence_id)
        item = evidence[evidence_id]
        technical_items.append({"id": evidence_id, "status": item.get("status", BLOCKED),
                                "reason": item.get("reason")})
        item_status = item.get("status", BLOCKED)
        if item_status == FAIL:
            technical_status = FAIL
        elif item_status == BLOCKED and technical_status != FAIL:
            technical_status = BLOCKED
        elif item_status == PASS and technical_status == NOT_RUN:
            technical_status = PASS
    owner_config = case.get("owner_acceptance") or {}
    owner_acceptance = {"status": NOT_RUN,
                        "reason": "Owner calibration/acceptance was not run by offline replay."}
    if owner_config and owner_config.get("status") not in {None, NOT_RUN}:
        raise ReplayInputError("owner acceptance cannot be inferred by replay")
    baseline_config = case.get("baseline_comparison") or {}
    baseline = {"status": baseline_config.get("status", NOT_RUN),
                "comparable": bool(baseline_config.get("comparable", False)),
                "reason": baseline_config.get("reason", "No baseline was replaced or inferred.")}
    if baseline["status"] not in VALID_RESULT_STATUSES:
        raise ReplayInputError("baseline comparison has unsupported status")
    historical = case.get("historical_reproduction") or {}
    historical_status = historical.get("status", NOT_RUN)
    if historical_status not in VALID_RESULT_STATUSES:
        raise ReplayInputError("historical reproduction has unsupported status")
    missing = []
    for item in rendered_requirements:
        if item["status"] == BLOCKED:
            missing.append({"requirement_id": item["id"], "reason": item["detail"]})
    if qualitative["status"] == BLOCKED:
        missing.append({"requirement_id": "qualitative", "reason": qualitative.get("reason")})
    if proposal["status"] == BLOCKED:
        missing.append({"requirement_id": DESIGN_PROPOSAL_COMPLETENESS,
                        "reason": proposal.get("reason")})
    if quality["status"] == BLOCKED:
        missing.append({"requirement_id": RENDERED_DESIGN_DISTINCTIVENESS,
                        "reason": quality.get("reason")})
    if case.get("technical_required") and technical_status == BLOCKED:
        missing.append({"requirement_id": "technical", "reason": "Required technical evidence is blocked."})
    mandatory = [item for item in rendered_requirements
                 if item["class"] == "MANDATORY" and item["applicability"] != NOT_APPLICABLE]
    outcome_status = PASS
    if any(item["status"] == FAIL for item in mandatory) or qualitative["status"] == FAIL \
            or proposal["status"] == FAIL or quality["status"] == FAIL \
            or (case.get("technical_required") and technical_status == FAIL):
        outcome_status = FAIL
    elif any(item["status"] == BLOCKED for item in mandatory) or qualitative["status"] == BLOCKED \
            or proposal["status"] == BLOCKED or quality["status"] == BLOCKED \
            or (case.get("technical_required") and technical_status == BLOCKED):
        outcome_status = BLOCKED
    outcome_reason = {
        PASS: "All applicable mandatory requirements and declared quality assessments passed provisionally.",
        FAIL: "At least one mandatory requirement, qualitative criterion, proposal check, or quality criterion failed.",
        BLOCKED: "Required evidence, proposal support, or evidence-bound quality critique is missing or blocked.",
    }[outcome_status]
    return {
        "case_id": case["id"],
        "case_version": case_version,
        "brief": case.get("brief", ""),
        "specimen": {"id": specimen["id"], "kind": kind,
                      "quality_claim": "SYNTHETIC_FIXTURE_ONLY" if kind == "SYNTHETIC_FIXTURE"
                                       else "REAL_ARTIFACT_REPLAY_RESULT",
                      "source_revision": specimen.get("source_revision", {}),
                      "artifact_files": list(artifacts.values()),
                      "hash_status": PASS},
        "technical": {"status": technical_status,
                       "provenance": "IMPORTED_HISTORICAL" if technical_ids else "NOT_RUN",
                       "evidence": technical_items},
        "requirements": rendered_requirements,
        "proposal_evaluation": proposal,
        "qualitative": qualitative,
        "quality_evaluation": quality,
        "owner_acceptance": owner_acceptance,
        "calibration": {"status": BLOCKED if owner_acceptance["status"] == NOT_RUN else PASS,
                        "reason": "Owner label and calibration remain separate from replay."},
        "baseline_comparison": baseline,
        "historical_reproduction": {"status": historical_status,
                                      "reason": historical.get("reason", "Historical reproduction was not rerun.")},
        "historical_claim_classification": historical_claims,
        "certification": {
            "technical_verification": technical_status,
            "quality_evaluation": quality["status"],
            "owner_acceptance": owner_acceptance["status"],
            "production_certification": "NOT_GRANTED",
        },
        "missing_evidence": missing,
        "outcome": {"status": outcome_status, "reason": outcome_reason,
                     "provisional": True, "owner_approved": False},
    }


def _evaluate_manifest(manifest: Mapping[str, Any], repo_root: str, report: Dict[str, Any]) -> None:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ReplayInputError("manifest_version must be %s" % MANIFEST_VERSION)
    if manifest.get("mode") != "artifact-replay":
        raise ReplayInputError("manifest mode must be artifact-replay")
    roots = _safe_roots(repo_root, manifest.get("authorized_input_roots"))
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ReplayInputError("manifest cases must be a non-empty list")
    seen = set()
    for raw_case in cases:
        case_id = raw_case.get("id") if isinstance(raw_case, dict) else "<malformed>"
        if case_id in seen:
            raise ReplayInputError("duplicate case id: %s" % case_id)
        seen.add(case_id)
        try:
            rendered = _evaluate_case(raw_case, repo_root, roots)
        except ReplayInputError as exc:
            rendered = _invalid_case(case_id, str(exc))
            report["execution"]["status"] = FAIL
            report["execution"]["error_kind"] = "INPUT_INVALID"
            report["execution"]["errors"].append({"case_id": case_id, "error": str(exc)})
        report["cases"].append(rendered)
    for rendered in report["cases"]:
        kind = rendered.get("specimen", {}).get("kind")
        if kind == "SYNTHETIC_FIXTURE":
            report["summary"]["synthetic_cases"] += 1
        else:
            report["summary"]["real_cases"] += 1
        status = rendered.get("outcome", {}).get("status", INVALID)
        report["summary"][status] = report["summary"].get(status, 0) + 1
        quality = rendered.get("quality_evaluation", {})
        quality_status = quality.get("status", NOT_APPLICABLE)
        if quality_status != NOT_APPLICABLE:
            report["quality_summary"]["cases"] += 1
            if quality_status in {PASS, FAIL} and quality.get("provenance") == "EVIDENCE_BOUND_CRITIQUE":
                report["quality_summary"]["evidence_verified"] += 1
            if quality_status in {FAIL, BLOCKED}:
                report["quality_summary"][quality_status] += 1
        elif quality_status == NOT_APPLICABLE:
            report["quality_summary"]["NOT_APPLICABLE"] += 1
    if report["summary"].get(INVALID):
        report["execution"]["status"] = FAIL
        report["execution"]["error_kind"] = report["execution"].get("error_kind") or "INPUT_INVALID"


def _markdown(report: Mapping[str, Any]) -> str:
    lines = ["# Website Director Offline Outcome Replay", "",
             "- run: `%s`" % report["run_id"],
             "- manifest: `%s`" % report["manifest_path"],
             "- execution: **%s**" % report["execution"]["status"],
             "- result counts: `%s`" % json.dumps(report["summary"], sort_keys=True),
             "- quality contract: `%s`; rendered evidence required: **%s**" %
             (report.get("quality_contract", {}).get("rubric_version"),
              report.get("quality_contract", {}).get("rendered_evidence_required")),
             "- network/provider/browser navigation/generation calls: `0 / 0 / 0 / 0`", "",
             "## Cases", ""]
    for case in report.get("cases", []):
        outcome = case.get("outcome", {})
        specimen = case.get("specimen", {})
        lines.append("### `%s` — **%s**" % (case.get("case_id"), outcome.get("status")))
        lines.append("- specimen: `%s` (%s)" % (specimen.get("id"), specimen.get("kind")))
        lines.append("- technical: **%s**; qualitative: **%s**; owner acceptance: **%s**" %
                     (case.get("technical", {}).get("status"), case.get("qualitative", {}).get("status"),
                      case.get("owner_acceptance", {}).get("status")))
        quality = case.get("quality_evaluation", {})
        lines.append("- proposal completeness: **%s**; rendered quality: **%s**; quality bar: **%s**" %
                     (case.get("proposal_evaluation", {}).get("status"), quality.get("status"),
                      quality.get("quality_bar_status", "NOT_APPLICABLE")))
        legacy = case.get("historical_claim_classification", {})
        if legacy.get("claims"):
            lines.append("- historical quality claims: **PRESERVED_NOT_TRUSTED** (%d)" % len(legacy["claims"]))
        lines.append("- reason: %s" % outcome.get("reason", ""))
        missing = case.get("missing_evidence") or []
        if missing:
            lines.append("- missing evidence: %s" % "; ".join(
                (item.get("reason", "") if isinstance(item, dict) else str(item)) for item in missing))
        lines.append("")
    lines += ["## Boundaries", "", "- Imported receipts were validated locally and were not rerun.",
              "- Synthetic fixtures are labeled and are not real website-quality results.",
              "- Proposal completeness is declaration/structure evidence; rendered distinctiveness and premium quality require hash-bound real-browser evidence.",
              "- Historical quality claims are preserved as recorded claims and never promoted to current baselines.",
              "- Owner calibration, baseline replacement, generation, deployment, and production verification were not attempted.", ""]
    return "\n".join(lines)


def replay(manifest_path: str, evidence_dir: str, repo_root: Optional[str] = None) -> Dict[str, Any]:
    """Evaluate one manifest and write a new JSON/Markdown report directory."""
    root = os.path.realpath(repo_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    run_id = _run_id()
    report = _base_report(run_id, os.path.abspath(manifest_path), root)
    output: Optional[str] = None
    try:
        manifest_abs = os.path.realpath(os.path.abspath(manifest_path))
        if not _is_within(manifest_abs, root):
            raise ReplayInputError("case manifest must be inside the repository")
        output = _prepare_output(evidence_dir, root)
        manifest = _read_json(manifest_abs, "case manifest")
        report["manifest_sha256"] = _sha256(manifest_abs)
        _evaluate_manifest(manifest, root, report)
    except ReplayInputError as exc:
        report["execution"] = {"status": FAIL, "error_kind": "INPUT_INVALID", "errors": [{"error": str(exc)}]}
        report["summary"][INVALID] = max(1, report["summary"].get(INVALID, 0))
    report["finished_at"] = _utc_now()
    if output:
        json_path = os.path.join(output, "outcome-replay.json")
        md_path = os.path.join(output, "outcome-replay.md")
        report["output"] = {"directory": output, "json": json_path, "markdown": md_path}
        with open(json_path, "x", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, sort_keys=True)
            fh.write("\n")
        with open(md_path, "x", encoding="utf-8") as fh:
            fh.write(_markdown(report))
    return report


def exit_code(report: Mapping[str, Any]) -> int:
    if report.get("execution", {}).get("status") != PASS:
        return 3
    counts = report.get("summary", {})
    if counts.get(FAIL, 0):
        return 1
    if counts.get(BLOCKED, 0) or counts.get(NOT_RUN, 0) or counts.get(INVALID, 0):
        return 2
    return 0


def run_replay(manifest_path: str, evidence_dir: str, repo_root: Optional[str] = None) -> int:
    report = replay(manifest_path, evidence_dir, repo_root=repo_root)
    output = report.get("output", {})
    print(json.dumps({"run_id": report["run_id"], "execution": report["execution"],
                      "summary": report["summary"], "json": output.get("json"),
                      "markdown": output.get("markdown")}, sort_keys=True))
    return exit_code(report)


__all__ = ["BLOCKED", "CURRENTLY_EVIDENCE_VERIFIED_RESULT", "DESIGN_PROPOSAL_COMPLETENESS",
           "FAIL", "HISTORICAL_RECORDED_CLAIM", "INVALID",
           "LEGACY_UNSUBSTANTIATED_QUALITY_CLAIM", "NOT_APPLICABLE", "NOT_RUN", "PASS",
           "PAIRWISE_CHOICES", "PAIRWISE_DEFAULT_DIMENSIONS", "PAIRWISE_DIMENSIONS",
           "QUALITY_DIMENSIONS", "QUALITY_RUBRIC_VERSION", "RENDERED_DESIGN_DISTINCTIVENESS",
           "evaluate_pairwise_visual_gate",
           "exit_code", "replay", "run_replay"]
