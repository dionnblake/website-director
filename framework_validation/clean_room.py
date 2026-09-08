"""Clean-Room Creative Mode Engine and Verification Rules for Website Director.

This module provides the deterministic clean-room creative input firewall,
historical quarantine checks, asset allowlisting, reference provenance verification,
cheap concept gate enforcement, blind critic packaging, and morphology divergence checks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence

from .rendered_morphology import compare_rendered_morphology

QUARANTINED_PATH_PREFIXES = (
    "projects/",
    "review-workspaces/",
    "historical-project/",
)

CLEAN_ROOM_STAGE_DIRECTORIES = (
    "manifest",
    "business",
    "brand",
    "approved-assets",
    "external-references",
    "candidate-output",
    "evidence",
)

STAGE_INPUT_ROOTS = {"business", "brand", "approved-assets", "external-references"}

HISTORICAL_SENTINELS = (
    "NEVER_SHOW_THIS_TO_GENERATOR",
    "old-two-column-card",
    "old-hero.jpg",
)

BLIND_CRITIC_SENTINELS = (
    "SECRET_BUILDER_SCORE",
    "SECRET_CLASS_NAME",
    "SECRET_BUILDER_COMMENT",
    "cinematic-masterpiece",
    "definitely premium",
)

FORBIDDEN_PRE_GENERATION_SURFACES = {
    "FULL_HOMEPAGE",
    "MOBILE_FULL_PAGE",
    "FOOTER",
    "MULTI_ROUTE",
    "FULL_BROWSER_QA",
    "MOTION_CERTIFICATION",
}

PROGRAMMATIC_GAUNTLET_ENTRYPOINT = "ABSENT"
CLEAN_ROOM_RUNTIME_ENTRYPOINT = "framework_validation.clean_room.prepare_clean_room_concept_run"

HISTORICAL_ASSET_EXTENSIONS = (
    ".jpg", ".jpeg", ".png", ".webp", ".avif", ".svg", ".mp4", ".webm", ".gif"
)

ALLOWED_POSITIVE_REFERENCE_CLASSES = {
    "EXTERNAL_GOLD_STANDARD",
    "OWNER_SUPPLIED_EXTERNAL_REFERENCE",
    "OWNER_APPROVED_BRAND_ASSET",
}

FORBIDDEN_POSITIVE_REFERENCE_CLASSES = {
    "PREVIOUS_WEBSITE_DIRECTOR_OUTPUT",
    "PREVIOUS_ASN_PROTOTYPE",
    "PREVIOUS_ASN_SCREENSHOT",
    "PREVIOUS_GENERATED_DIRECTION",
    "PREVIOUS_GENERATED_DESIGN_SYSTEM",
}


@dataclass
class CleanRoomManifest:
    mode: str = "CLEAN_ROOM"
    business_understanding_ref: str = "project-brief.md"
    owner_intent_ref: str = "creative-intent-contract.md"
    brand_constants: Dict[str, Any] = field(default_factory=dict)
    reusable_assets: List[Dict[str, Any]] = field(default_factory=list)
    external_references: List[Dict[str, Any]] = field(default_factory=list)
    conversion_requirements_ref: str = "measurement-plan.md"
    content_truth_ref: str = "content-plan.md"
    staged_inputs: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CleanRoomManifest":
        """Build a manifest from a machine-readable mapping without accepting unknown state."""
        if not isinstance(value, Mapping):
            raise TypeError("clean-room manifest must be an object")
        return cls(
            mode=str(value.get("mode", "CLEAN_ROOM")),
            business_understanding_ref=str(value.get("business_understanding_ref", "")),
            owner_intent_ref=str(value.get("owner_intent_ref", "")),
            brand_constants=dict(value.get("brand_constants", {}) or {}),
            reusable_assets=list(value.get("reusable_assets", []) or []),
            external_references=list(value.get("external_references", []) or []),
            conversion_requirements_ref=str(value.get("conversion_requirements_ref", "")),
            content_truth_ref=str(value.get("content_truth_ref", "")),
            staged_inputs=list(value.get("staged_inputs", []) or []),
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "business_understanding_ref": self.business_understanding_ref,
            "owner_intent_ref": self.owner_intent_ref,
            "brand_constants": dict(self.brand_constants),
            "reusable_assets": [dict(item) for item in self.reusable_assets],
            "external_references": [dict(item) for item in self.external_references],
            "conversion_requirements_ref": self.conversion_requirements_ref,
            "content_truth_ref": self.content_truth_ref,
            "staged_inputs": [dict(item) for item in self.staged_inputs],
        }

    def is_valid(self) -> bool:
        return self.mode == "CLEAN_ROOM" and bool(self.business_understanding_ref) and bool(self.owner_intent_ref)


class HistoricalQuarantineGuard:
    """Enforces structural quarantine against historical project outputs during concept generation."""

    def __init__(self, mode: str = "CLEAN_ROOM", allowlist: Optional[List[Dict[str, Any]]] = None) -> None:
        self.mode = mode
        self.allowlist: Dict[str, Dict[str, Any]] = {}
        if allowlist:
            for item in allowlist:
                if isinstance(item, dict) and item.get("authorized"):
                    asset_id = item.get("asset_id")
                    if asset_id:
                        self.allowlist[asset_id] = item

    def check_input_path(self, path_str: str, is_post_render_negative_baseline: bool = False) -> Dict[str, Any]:
        """Check if an input path is accessible under clean-room creative rules."""
        if self.mode != "CLEAN_ROOM":
            return {"status": "PASS", "path": path_str}

        normalized = str(path_str).replace("\\", "/")
        is_uri = "://" in normalized or normalized.casefold().startswith(("data:", "blob:"))
        path_parts = [part for part in normalized.split("/") if part not in ("", ".")]

        # Check quarantine prefixes
        is_historical = not is_uri and any(
            part.casefold() in {prefix.rstrip("/").casefold() for prefix in QUARANTINED_PATH_PREFIXES}
            for part in path_parts
        )
        if not is_uri:
            normalized = normalized.lstrip("./")

        if is_historical:
            if is_post_render_negative_baseline:
                return {
                    "status": "PASS",
                    "path": normalized,
                    "role": "NEGATIVE_BASELINE_ONLY",
                    "allowed_pre_render": False,
                }
            else:
                return {
                    "status": "BLOCKED",
                    "violation": "CLEAN_ROOM_INPUT_VIOLATION",
                    "path": normalized,
                    "reason": f"Historical output at '{normalized}' is structurally quarantined from concept generation.",
                }

        return {"status": "PASS", "path": normalized}

    def check_asset_reuse(self, asset_id: Optional[str], source_path: str, is_bulk: bool = False) -> Dict[str, Any]:
        """Check if a reusable owner asset is authorized."""
        if self.mode != "CLEAN_ROOM":
            return {"status": "PASS"}

        if is_bulk:
            return {
                "status": "BLOCKED",
                "violation": "HISTORICAL_ASSET_BULK_REUSE",
                "reason": "Bulk asset copying from historical projects is prohibited in CLEAN_ROOM mode.",
            }

        normalized = str(source_path).replace("\\", "/")
        is_uri = "://" in normalized or normalized.casefold().startswith(("data:", "blob:"))
        path_parts = [part for part in normalized.split("/") if part not in ("", ".")]
        is_historical = not is_uri and any(
            part.casefold() in {prefix.rstrip("/").casefold() for prefix in QUARANTINED_PATH_PREFIXES}
            for part in path_parts
        )
        if not is_uri:
            normalized = normalized.lstrip("./")

        if is_historical:
            if asset_id and asset_id in self.allowlist:
                return {"status": "PASS", "asset_id": asset_id, "authorized": True}
            return {
                "status": "BLOCKED",
                "violation": "CLEAN_ROOM_INPUT_VIOLATION",
                "path": normalized,
                "reason": f"Asset '{source_path}' (id: {asset_id}) is not explicitly authorized on the owner allowlist.",
            }

        return {"status": "PASS"}


def verify_reference_provenance(references: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Verify that all positive creative references have valid external provenance."""
    if not references:
        return {
            "status": "BLOCKED",
            "violation": "EXTERNAL_REFERENCE_PACKAGE_MISSING",
            "reason": "No valid external reference package provided for clean-room concept generation.",
        }

    valid_refs = []
    for ref in references:
        classification = ref.get("classification", "")
        if classification in FORBIDDEN_POSITIVE_REFERENCE_CLASSES:
            return {
                "status": "BLOCKED",
                "violation": "HISTORICAL_POSITIVE_REFERENCE_FORBIDDEN",
                "reference_id": ref.get("reference_id"),
                "classification": classification,
                "reason": f"Classification '{classification}' cannot be used as a positive creative reference.",
            }
        if classification in ALLOWED_POSITIVE_REFERENCE_CLASSES:
            valid_refs.append(ref)

    if not valid_refs:
        return {
            "status": "BLOCKED",
            "violation": "EXTERNAL_REFERENCE_PACKAGE_MISSING",
            "reason": "Zero valid external references found after classification verification.",
        }

    return {"status": "PASS", "valid_references_count": len(valid_refs)}


def enforce_cheap_concept_gate(concept_package: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure clean-room concepts initially build only desktop hero + signature device."""
    concepts = concept_package.get("concepts", [])
    if len(concepts) != 3:
        return {
            "status": "FAIL",
            "reason": f"Clean-room concept stage requires exactly 3 concepts, found {len(concepts)}.",
        }

    for idx, c in enumerate(concepts):
        built_surfaces = c.get("built_surfaces", [])
        disallowed = [s for s in built_surfaces if s not in ("desktop_hero", "signature_device")]
        if disallowed:
            return {
                "status": "FAIL",
                "concept_index": idx,
                "disallowed_surfaces": disallowed,
                "reason": f"Concept {idx} built disallowed full-homepage surfaces prior to owner selection: {disallowed}",
            }

    return {
        "status": "PASS",
        "scope": "HERO_PLUS_SIGNATURE_DEVICE_ONLY",
        "owner_concept_selection_required": True,
    }


def prepare_blind_critic_package(
    candidate_screenshot: str,
    external_references: List[str],
    business_brief: str,
    brand_brief: str,
    rendered_dom_ref: Optional[str] = None,
    rendered_css_ref: Optional[str] = None,
    morphology_evidence: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Prepare a stripped, blind evaluation package for the Website Gauntlet critic."""
    return {
        "candidate_screenshot": candidate_screenshot,
        "external_reference_screenshots": external_references,
        "business_brief": business_brief,
        "brand_brief": brand_brief,
        "actual_screenshots": [candidate_screenshot],
        "actual_rendered_dom_ref": rendered_dom_ref,
        "actual_css_ref": rendered_css_ref,
        "morphology_evidence": dict(morphology_evidence or {}),
        "critic_authority": "WEBSITE-GAUNTLET-PROTOCOL.md",
        "programmatic_gauntlet_entrypoint": PROGRAMMATIC_GAUNTLET_ENTRYPOINT,
        # Explicitly excluded fields to guarantee blind review
        "html_source": None,
        "css_source": None,
        "class_names": None,
        "direction_name": None,
        "builder_commentary": None,
        "self_awarded_scores": None,
        "previous_asn_screenshots": None,
    }


def evaluate_morphology_divergence(
    candidate_morphology: Dict[str, Any],
    historical_baseline_morphology: Dict[str, Any]
) -> Dict[str, Any]:
    """Evaluate complete legacy declarations; missing values fail closed.

    New browser-derived evaluations use :func:`compare_rendered_morphology`.
    This compatibility path cannot normalize geometry, but it must never turn
    absent declarations into either similarity or divergence evidence.
    """
    divergence_vectors = [
        "HERO_SILHOUETTE",
        "SECTION_GEOMETRY",
        "TWO_COLUMN_REPETITION",
        "CARD_CONTAINER_DENSITY",
        "MEDIA_DOMINANCE",
        "TYPOGRAPHIC_SILHOUETTE",
        "WHITESPACE_DENSITY",
        "PAGE_RHYTHM",
        "SIGNATURE_DEVICE",
        "CTA_MORPHOLOGY",
    ]

    def meaningful(value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, (list, tuple, dict, set)):
            return bool(value)
        return True

    insufficient = [
        vector for vector in divergence_vectors
        if not meaningful(candidate_morphology.get(vector))
        or not meaningful(historical_baseline_morphology.get(vector))
    ]
    if insufficient:
        return {
            "status": "BLOCKED_INSUFFICIENT_EVIDENCE",
            "divergence": "MORPHOLOGY_DIVERGENCE_BLOCKED_INSUFFICIENT_EVIDENCE",
            "insufficient_evidence_vectors": insufficient,
            "failures": [],
            "semantic_rename_detected": bool(candidate_morphology.get("semantic_rename_only", False)),
            "vector_results": {
                vector: "INSUFFICIENT_EVIDENCE" if vector in insufficient else "NOT_EVALUATED"
                for vector in divergence_vectors
            },
        }

    vector_results = {}
    failures = []

    for vector in divergence_vectors:
        cand_val = candidate_morphology.get(vector)
        hist_val = historical_baseline_morphology.get(vector)

        # If candidate has identical structure despite renamed components, fail
        if cand_val == hist_val and cand_val is not None:
            vector_results[vector] = "MATCHES_HISTORICAL_BASELINE"
            failures.append(vector)
        else:
            vector_results[vector] = "DIVERGENT"

    is_semantic_rename_only = candidate_morphology.get("semantic_rename_only", False)
    if is_semantic_rename_only or len(failures) >= 5:
        return {
            "status": "FAIL",
            "divergence": "MORPHOLOGY_DIVERGENCE_FAIL",
            "failures": failures,
            "semantic_rename_detected": is_semantic_rename_only,
            "vector_results": vector_results,
        }

    return {
        "status": "PASS",
        "divergence": "MORPHOLOGY_DIVERGENCE_PASS",
        "failures": [],
        "semantic_rename_detected": is_semantic_rename_only,
        "vector_results": vector_results,
    }


CleanRoomConceptGenerator = Callable[[CleanRoomManifest], Mapping[str, Any]]
CleanRoomCandidateRenderer = Callable[[Mapping[str, Any]], Mapping[str, Any]]
CleanRoomBaselineLoader = Callable[[str], Mapping[str, Any]]
CleanRoomBlindCritic = Callable[[Mapping[str, Any]], Mapping[str, Any]]
CleanRoomStageReady = Callable[[str, Mapping[str, Any]], None]


@dataclass(frozen=True)
class CleanRoomExecutionAdapters:
    """Provider-neutral callbacks used by the clean-room coordinator.

    The callbacks receive only the stage data they need. In particular, the
    concept generator never receives a repository root or a historical path,
    and the baseline loader is not called until after candidate rendering.
    """

    generate_concepts: CleanRoomConceptGenerator
    render_candidate: CleanRoomCandidateRenderer
    load_negative_baseline: CleanRoomBaselineLoader
    run_blind_critic: CleanRoomBlindCritic
    on_stage_ready: Optional[CleanRoomStageReady] = None


@dataclass(frozen=True)
class CleanRoomExecutionRequest:
    """Inputs for one bounded clean-room creative execution."""

    manifest: CleanRoomManifest | Mapping[str, Any]
    adapters: CleanRoomExecutionAdapters
    negative_baseline_path: str
    business_brief: str
    brand_brief: str
    positive_input_paths: Sequence[str] = ()
    external_reference_screenshots: Sequence[str] = ()
    run_id: str = ""
    source_root: Optional[str] = None
    run_root: str = ".clean-room-runs"
    requested_input_paths: Sequence[str] = ()
    concept_scope: Optional[Mapping[str, Any]] = None
    owner_selection_event: Optional[Mapping[str, Any]] = None


EXECUTION_STAGE_SEQUENCE = (
    "INPUT_PREFLIGHT",
    "REFERENCE_PROVENANCE",
    "STAGED_CREATIVE_WORKSPACE",
    "PRE_GENERATION_SCOPE",
    "NEGATIVE_BASELINE_PRE_RENDER",
    "CONCEPT_GENERATION",
    "CHEAP_CONCEPT_GATE",
    "CANDIDATE_RENDER",
    "NEGATIVE_BASELINE_ACCESS",
    "NEGATIVE_BASELINE_LOAD",
    "RENDER_DERIVED_MORPHOLOGY",
    "BLIND_CRITIC_PACKAGE",
    "BLIND_CRITIC",
    "OWNER_CONCEPT_SELECTION_GATE",
)


def _execution_receipt(
    request: CleanRoomExecutionRequest,
    manifest: CleanRoomManifest,
    run_id: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "receipt_version": "1.0.0",
        "runtime_entrypoint": CLEAN_ROOM_RUNTIME_ENTRYPOINT,
        "run_id": run_id or request.run_id,
        "mode": manifest.mode,
        "status": "BLOCKED",
        "workflow_status": "NOT_STARTED",
        "owner_concept_selection": "PENDING",
        "full_homepage_design": "BLOCKED",
        "programmatic_gauntlet_entrypoint": PROGRAMMATIC_GAUNTLET_ENTRYPOINT,
        "stage_sequence": [],
        "stages": [],
        "controls": {
            "historical_positive_inputs_read": False,
            "negative_baseline_access_before_render": "NOT_EVALUATED",
            "negative_baseline_read_before_render": False,
            "negative_baseline_read_after_render": False,
            "project_files_written": 0,
            "production_side_effects": False,
            "asn_generation_attempted": False,
            "staged_input_file_count": 0,
            "staged_historical_output_files": 0,
            "generator_package_historical_sentinels": 0,
            "blind_critic_sentinel_leaks": 0,
        },
    }


def _record_execution_stage(
    receipt: Dict[str, Any],
    stage_id: str,
    status: str,
    detail: str,
    **evidence: Any,
) -> None:
    receipt["stage_sequence"].append(stage_id)
    receipt["stages"].append(
        {
            "id": stage_id,
            "status": status,
            "detail": detail,
            "evidence": evidence,
        }
    )


def _finish_execution(
    receipt: Dict[str, Any],
    status: str,
    workflow_status: str,
    reason: Optional[str] = None,
) -> Dict[str, Any]:
    receipt["status"] = status
    receipt["workflow_status"] = workflow_status
    if reason:
        receipt["failure" if status in {"BLOCKED", "FAIL"} else "completion_note"] = reason
    return receipt


def _adapter_error(exc: Exception) -> str:
    return f"{type(exc).__name__}: {exc}"


def _manifest_for_execution(value: CleanRoomManifest | Mapping[str, Any]) -> CleanRoomManifest:
    if isinstance(value, CleanRoomManifest):
        return value
    return CleanRoomManifest.from_mapping(value)


def _positive_manifest_paths(manifest: CleanRoomManifest) -> List[str]:
    return [
        manifest.business_understanding_ref,
        manifest.owner_intent_ref,
        manifest.conversion_requirements_ref,
        manifest.content_truth_ref,
    ]


def _check_positive_inputs(
    guard: HistoricalQuarantineGuard,
    manifest: CleanRoomManifest,
    request: CleanRoomExecutionRequest,
) -> Optional[Dict[str, Any]]:
    paths = _positive_manifest_paths(manifest) + list(request.positive_input_paths)
    paths.extend(str(path) for path in request.external_reference_screenshots)
    for reference in manifest.external_references:
        if not isinstance(reference, Mapping):
            return {
                "status": "BLOCKED",
                "violation": "CLEAN_ROOM_MANIFEST_INVALID",
                "reason": "Every external reference must be an object.",
            }
        source_path = reference.get("source_path")
        if source_path:
            paths.append(str(source_path))

    for staged_input in manifest.staged_inputs:
        if not isinstance(staged_input, Mapping):
            return {
                "status": "BLOCKED",
                "violation": "CLEAN_ROOM_MANIFEST_INVALID",
                "reason": "Every staged input must be an object.",
            }
        source_path = staged_input.get("source_path")
        if source_path:
            paths.append(str(source_path))

    for path in paths:
        result = guard.check_input_path(path)
        if result.get("status") != "PASS":
            return result

    for asset in manifest.reusable_assets:
        if not isinstance(asset, Mapping) or not asset.get("source_path"):
            return {
                "status": "BLOCKED",
                "violation": "CLEAN_ROOM_MANIFEST_INVALID",
                "reason": "Every reusable asset must declare a source_path.",
            }
        result = guard.check_asset_reuse(
            asset_id=str(asset.get("asset_id")) if asset.get("asset_id") else None,
            source_path=str(asset["source_path"]),
            is_bulk=bool(asset.get("bulk", False)),
        )
        if result.get("status") != "PASS":
            return result
    return None


def _mapping_value(payload: Any, key: str) -> Optional[Mapping[str, Any]]:
    if not isinstance(payload, Mapping):
        return None
    value = payload.get(key)
    return value if isinstance(value, Mapping) else None


def _normalise_token(value: Any) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", str(value or "").upper()).strip("_")


def _safe_run_id(requested: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", str(requested or "")).strip(".-")
    return value or "clean-room-" + uuid.uuid4().hex[:12]


def _safe_relative_path(value: Any) -> Optional[str]:
    normalized = str(value or "").replace("\\", "/")
    if not normalized or normalized.startswith("/") or re.match(r"^[A-Za-z]:/", normalized):
        return None
    parts = [part for part in normalized.split("/") if part not in ("", ".")]
    if not parts or any(part == ".." for part in parts):
        return None
    return "/".join(parts)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sentinel_count(value: Any) -> int:
    serialized = json.dumps(value, sort_keys=True, default=str)
    return sum(serialized.count(sentinel) for sentinel in HISTORICAL_SENTINELS)


def validate_pre_generation_scope(scope: Mapping[str, Any]) -> Dict[str, Any]:
    """Authorize the cheap scope before any concept-builder callback runs."""

    if not isinstance(scope, Mapping):
        return {"status": "BLOCKED", "reason": "PRE_GENERATION_SCOPE_MISSING"}
    concepts = scope.get("concepts")
    if not isinstance(concepts, list) or len(concepts) != 3:
        return {
            "status": "FAIL",
            "reason": "PRE_GENERATION_SCOPE_REQUIRES_EXACTLY_THREE_CONCEPTS",
            "concept_count": len(concepts) if isinstance(concepts, list) else 0,
        }

    declared_surfaces: list[str] = []
    for key in ("allowed_surfaces", "requested_surfaces", "built_surfaces"):
        values = scope.get(key)
        if isinstance(values, list):
            declared_surfaces.extend(str(value) for value in values)
    for concept in concepts:
        if not isinstance(concept, Mapping):
            continue
        for key in ("allowed_surfaces", "requested_surfaces", "built_surfaces"):
            values = concept.get(key)
            if isinstance(values, list):
                declared_surfaces.extend(str(value) for value in values)
    forbidden = sorted(
        token
        for token in FORBIDDEN_PRE_GENERATION_SURFACES
        if any(token in _normalise_token(surface) for surface in declared_surfaces)
    )
    if forbidden:
        return {
            "status": "FAIL",
            "reason": "PRE_GENERATION_SCOPE_FORBIDDEN_SURFACE",
            "forbidden_surfaces": forbidden,
        }

    expected = {"DESKTOP_HERO", "SIGNATURE_DEVICE"}
    issues: list[str] = []
    declared = {_normalise_token(item) for item in scope.get("allowed_surfaces", [])} \
        if isinstance(scope.get("allowed_surfaces"), list) else set()
    if declared != expected:
        issues.append("top-level allowed_surfaces must be DESKTOP_HERO and SIGNATURE_DEVICE")
    for index, concept in enumerate(concepts):
        if not isinstance(concept, Mapping):
            issues.append(f"concept {index} is not an object")
            continue
        surfaces = {_normalise_token(item) for item in concept.get("allowed_surfaces", [])} \
            if isinstance(concept.get("allowed_surfaces"), list) else set()
        if surfaces != expected:
            issues.append(f"concept {index} has an unauthorized surface set")
    if issues:
        return {"status": "FAIL", "reason": "PRE_GENERATION_SCOPE_INVALID", "issues": issues}
    return {
        "status": "PASS",
        "scope": "DESKTOP_HERO_PLUS_SIGNATURE_DEVICE_ONLY",
        "concept_count": 3,
        "allowed_surfaces": ["DESKTOP_HERO", "SIGNATURE_DEVICE"],
        "builder_task_authorized": True,
    }


def _default_concept_scope() -> Dict[str, Any]:
    return {
        "allowed_surfaces": ["DESKTOP_HERO", "SIGNATURE_DEVICE"],
        "concepts": [
            {"concept_id": "concept-a", "allowed_surfaces": ["DESKTOP_HERO", "SIGNATURE_DEVICE"]},
            {"concept_id": "concept-b", "allowed_surfaces": ["DESKTOP_HERO", "SIGNATURE_DEVICE"]},
            {"concept_id": "concept-c", "allowed_surfaces": ["DESKTOP_HERO", "SIGNATURE_DEVICE"]},
        ],
        "before_owner_selection": "BLOCKED",
    }


def _requested_input_audit(
    guard: HistoricalQuarantineGuard,
    requested_paths: Sequence[str],
) -> List[Dict[str, Any]]:
    audit: List[Dict[str, Any]] = []
    for path in requested_paths:
        result = guard.check_input_path(str(path))
        audit.append({"source_path": str(path), **result})
    return audit


def _stage_creative_workspace(
    request: CleanRoomExecutionRequest,
    manifest: CleanRoomManifest,
    guard: HistoricalQuarantineGuard,
    run_id: str,
) -> Dict[str, Any]:
    """Create an isolated, manifest-driven creative pack and inventory."""

    run_root = Path(request.run_root).expanduser().resolve()
    if any(part.casefold() in {"projects", "review-workspaces"} for part in run_root.parts):
        return {"status": "BLOCKED", "reason": "CLEAN_ROOM_RUNTIME_ROOT_QUARANTINED"}
    run_root.mkdir(parents=True, exist_ok=True)
    actual_run_id = run_id
    stage_root = run_root / actual_run_id
    if stage_root.exists():
        actual_run_id = f"{run_id}-{uuid.uuid4().hex[:8]}"
        stage_root = run_root / actual_run_id
    stage_root.mkdir(parents=True, exist_ok=False)
    for directory in CLEAN_ROOM_STAGE_DIRECTORIES:
        (stage_root / directory).mkdir(parents=True, exist_ok=True)

    _write_json(stage_root / "manifest" / "clean-room-manifest.json", manifest.as_dict())
    inventory: List[Dict[str, Any]] = []
    source_root = Path(request.source_root).expanduser().resolve() if request.source_root else None
    for index, raw_item in enumerate(manifest.staged_inputs):
        if not isinstance(raw_item, Mapping):
            return {"status": "BLOCKED", "stage_root": str(stage_root), "reason": f"STAGED_INPUT_{index}_INVALID"}
        source_path = _safe_relative_path(raw_item.get("source_path"))
        staged_path = _safe_relative_path(raw_item.get("staged_path"))
        classification = str(raw_item.get("classification", "")).strip()
        authorization_basis = str(raw_item.get("authorization_basis", "")).strip()
        if not source_path or not staged_path or not classification or not authorization_basis:
            return {
                "status": "BLOCKED",
                "stage_root": str(stage_root),
                "reason": f"STAGED_INPUT_{index}_DECLARATION_INVALID",
            }
        staged_parts = staged_path.split("/")
        if not staged_parts or staged_parts[0] not in STAGE_INPUT_ROOTS:
            return {
                "status": "BLOCKED",
                "stage_root": str(stage_root),
                "reason": f"STAGED_INPUT_{index}_TARGET_OUT_OF_SCOPE",
            }
        source_check = guard.check_input_path(source_path)
        if source_check.get("status") != "PASS":
            return {
                "status": "BLOCKED",
                "stage_root": str(stage_root),
                "reason": "CLEAN_ROOM_INPUT_VIOLATION",
                "blocked_input": source_check,
            }
        if source_root is None:
            return {"status": "BLOCKED", "stage_root": str(stage_root), "reason": "STAGED_INPUT_SOURCE_ROOT_MISSING"}
        source = (source_root / source_path).resolve()
        if source_root not in source.parents or not source.is_file():
            return {
                "status": "BLOCKED",
                "stage_root": str(stage_root),
                "reason": f"STAGED_INPUT_SOURCE_UNAVAILABLE:{source_path}",
            }
        destination = (stage_root / staged_path).resolve()
        if stage_root not in destination.parents:
            return {"status": "BLOCKED", "stage_root": str(stage_root), "reason": "STAGED_INPUT_TARGET_ESCAPE"}
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        inventory.append({
            "run_id": actual_run_id,
            "source_path": source_path,
            "staged_path": staged_path,
            "classification": classification,
            "sha256": _sha256_file(destination),
            "authorization_basis": authorization_basis,
        })

    staged_historical = 0
    staged_sentinels = 0
    for file_path in stage_root.rglob("*"):
        if not file_path.is_file() or file_path.parent.name == "evidence":
            continue
        relative = file_path.relative_to(stage_root).as_posix()
        if guard.check_input_path(relative).get("status") != "PASS":
            staged_historical += 1
        try:
            staged_sentinels += _sentinel_count(file_path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            pass

    requested_audit = _requested_input_audit(guard, request.requested_input_paths)
    inventory_payload = {
        "run_id": actual_run_id,
        "inputs": inventory,
        "staged_historical_output_files": staged_historical,
        "staged_historical_sentinels": staged_sentinels,
    }
    _write_json(stage_root / "evidence" / "staged-input-inventory.json", inventory_payload)
    _write_json(
        stage_root / "evidence" / "requested-input-audit.json",
        {"run_id": actual_run_id, "requests": requested_audit},
    )
    if staged_historical or staged_sentinels:
        return {
            "status": "BLOCKED",
            "run_id": actual_run_id,
            "stage_root": str(stage_root),
            "inventory": inventory,
            "requested_input_audit": requested_audit,
            "staged_historical_output_files": staged_historical,
            "staged_historical_sentinels": staged_sentinels,
            "reason": "STAGED_HISTORICAL_OUTPUT_PRESENT",
        }
    return {
        "status": "PASS",
        "run_id": actual_run_id,
        "stage_root": str(stage_root),
        "inventory": inventory,
        "requested_input_audit": requested_audit,
        "staged_historical_output_files": 0,
        "staged_historical_sentinels": 0,
    }


def _build_generation_package(
    request: CleanRoomExecutionRequest,
    manifest: CleanRoomManifest,
    stage: Mapping[str, Any],
    scope: Mapping[str, Any],
) -> Dict[str, Any]:
    inventory = [item for item in stage.get("inventory", []) if isinstance(item, Mapping)]
    by_source = {str(item.get("source_path")): item for item in inventory}
    positive_references = []
    for reference in manifest.external_references:
        if not isinstance(reference, Mapping):
            continue
        item = {
            "reference_id": reference.get("reference_id"),
            "classification": reference.get("classification"),
            "url": reference.get("url"),
        }
        source_path = reference.get("source_path")
        if source_path and str(source_path) in by_source:
            item["staged_path"] = by_source[str(source_path)].get("staged_path")
        positive_references.append(item)
    allowed_assets = []
    for asset in manifest.reusable_assets:
        if not isinstance(asset, Mapping):
            continue
        item = {
            "asset_id": asset.get("asset_id"),
            "classification": asset.get("classification", "OWNER_APPROVED_BRAND_ASSET"),
            "authorization_basis": asset.get("authorization_basis", "OWNER_ALLOWLIST_ITEM"),
        }
        source_path = asset.get("source_path")
        if source_path and str(source_path) in by_source:
            item["staged_path"] = by_source[str(source_path)].get("staged_path")
        allowed_assets.append(item)

    package = {
        "run_id": stage.get("run_id"),
        "mode": manifest.mode,
        "staged_workspace": {
            "manifest": "manifest/clean-room-manifest.json",
            "business": "business/",
            "brand": "brand/",
            "approved_assets": "approved-assets/",
            "external_references": "external-references/",
            "candidate_output": "candidate-output/",
            "evidence": "evidence/",
        },
        "business_brief": request.business_brief,
        "brand_brief": request.brand_brief,
        "approved_brand_constants": dict(manifest.brand_constants),
        "allowed_asset_list": allowed_assets,
        "positive_reference_list": positive_references,
        "concept_request": dict(scope),
        "generation_instruction": (
            "CLEAN_ROOM_MODE: use only the staged creative workspace. "
            "Generate exactly three bounded concept candidates, each limited to "
            "DESKTOP_HERO and SIGNATURE_DEVICE. Do not inspect repository, project, "
            "review-workspace, or prior generated output paths. Stop after candidate "
            "rendering and blind critique for owner concept selection."
        ),
    }
    if _sentinel_count(package):
        raise ValueError("GENERATOR_PACKAGE_HISTORICAL_SENTINEL_PRESENT")
    _write_json(Path(str(stage["stage_root"])) / "manifest" / "concept-generation-package.json", package)
    return package


def _persist_rendered_artifacts(stage_root: Optional[str], rendered: Mapping[str, Any]) -> Dict[str, Any]:
    result = dict(rendered)
    if not stage_root:
        return result
    root = Path(stage_root).resolve()
    output_dir = root / "candidate-output"
    output_dir.mkdir(parents=True, exist_ok=True)
    screenshot_bytes = result.pop("screenshot_bytes", None)
    if isinstance(screenshot_bytes, (bytes, bytearray)):
        screenshot_path = output_dir / "candidate.png"
        screenshot_path.write_bytes(bytes(screenshot_bytes))
        result["candidate_screenshot"] = "candidate-output/candidate.png"
        result["candidate_screenshot_sha256"] = hashlib.sha256(bytes(screenshot_bytes)).hexdigest()
    rendered_dom = result.pop("rendered_dom", None)
    if isinstance(rendered_dom, str) and rendered_dom.strip():
        dom_path = output_dir / "candidate-rendered.html"
        dom_path.write_text(rendered_dom, encoding="utf-8")
        result["rendered_dom_ref"] = "candidate-output/candidate-rendered.html"
    rendered_css = result.pop("rendered_css", None)
    if isinstance(rendered_css, str) and rendered_css.strip():
        css_path = output_dir / "candidate-rendered.css"
        css_path.write_text(rendered_css, encoding="utf-8")
        result["rendered_css_ref"] = "candidate-output/candidate-rendered.css"
    return result


def validate_owner_concept_selection(
    event: Optional[Mapping[str, Any]], concept_package: Mapping[str, Any]
) -> Dict[str, Any]:
    """Consume the existing visual-prototype owner-selection authority."""

    before = "BLOCKED"
    if event is None:
        return {
            "status": "PENDING",
            "state_location": "visual_prototypes.owner_selection_confirmed",
            "before_full_homepage_design": before,
            "after_full_homepage_design": before,
            "reason": "OWNER_CONCEPT_SELECTION_REQUIRED",
        }
    if not isinstance(event, Mapping):
        return {"status": "BLOCKED", "reason": "OWNER_SELECTION_EVENT_INVALID"}
    state_location = _normalise_token(event.get("STATE_LOCATION", event.get("state_location")))
    action = _normalise_token(event.get("OWNER_ACTION", event.get("owner_action")))
    approved_by = _normalise_token(event.get("APPROVED_BY", event.get("approved_by")))
    selected = str(event.get("OWNER_SELECTED_DIRECTION", event.get("owner_selected_direction", ""))).strip()
    concepts = concept_package.get("concepts", []) if isinstance(concept_package, Mapping) else []
    concept_ids = {str(item.get("concept_id", item.get("name", ""))) for item in concepts if isinstance(item, Mapping)}
    issues = []
    if state_location != "VISUAL_PROTOTYPES_OWNER_SELECTION_CONFIRMED":
        issues.append("OWNER_SELECTION_MUST_USE_EXISTING_VISUAL_PROTOTYPES_STATE")
    if event.get("OWNER_SELECTION_CONFIRMED", event.get("owner_selection_confirmed")) is not True:
        issues.append("OWNER_SELECTION_CONFIRMATION_REQUIRED")
    if action not in {"SELECT", "HYBRIDIZE"}:
        issues.append("OWNER_SELECTION_ACTION_REQUIRED")
    if approved_by not in {"OWNER", "PROJECT_OWNER", "CLIENT_OWNER"}:
        issues.append("OWNER_SELECTION_MUST_BE_SET_BY_OWNER")
    if selected not in concept_ids:
        issues.append("OWNER_SELECTED_DIRECTION_MUST_MATCH_RENDERED_CONCEPT")
    if issues:
        return {
            "status": "BLOCKED",
            "state_location": "visual_prototypes.owner_selection_confirmed",
            "before_full_homepage_design": before,
            "after_full_homepage_design": before,
            "issues": issues,
        }
    return {
        "status": "PASS",
        "state_location": "visual_prototypes.owner_selection_confirmed",
        "owner_selected_direction": selected,
        "owner_action": action,
        "approved_by": approved_by,
        "before_full_homepage_design": before,
        "after_full_homepage_design": "AUTHORIZED",
        "new_owner_lock_created": False,
    }


def prepare_clean_room_concept_run(request: CleanRoomExecutionRequest) -> Dict[str, Any]:
    """Run the canonical staged clean-room concept boundary.

    This boundary owns the runtime handoffs. It stages the validated manifest,
    emits the generator package, authorizes the bounded scope before the concept
    adapter runs, and never supplies historical positive material to an adapter.
    """
    run_id = _safe_run_id(request.run_id)
    try:
        manifest = _manifest_for_execution(request.manifest)
    except (TypeError, ValueError, AttributeError) as exc:
        receipt = _execution_receipt(request, CleanRoomManifest(mode="INVALID"), run_id)
        return _finish_execution(receipt, "BLOCKED", "INPUT_PREFLIGHT_BLOCKED", _adapter_error(exc))

    receipt = _execution_receipt(request, manifest, run_id)
    if not manifest.is_valid():
        _record_execution_stage(
            receipt, "INPUT_PREFLIGHT", "BLOCKED",
            "clean-room manifest is missing required mode or brief references",
        )
        return _finish_execution(receipt, "BLOCKED", "INPUT_PREFLIGHT_BLOCKED", "CLEAN_ROOM_MANIFEST_INVALID")
    if not request.negative_baseline_path:
        _record_execution_stage(
            receipt, "INPUT_PREFLIGHT", "BLOCKED",
            "negative baseline path is required for post-render comparison",
        )
        return _finish_execution(receipt, "BLOCKED", "INPUT_PREFLIGHT_BLOCKED", "NEGATIVE_BASELINE_PATH_MISSING")

    guard = HistoricalQuarantineGuard(mode=manifest.mode, allowlist=manifest.reusable_assets)
    positive_input_failure = _check_positive_inputs(guard, manifest, request)
    if positive_input_failure:
        _record_execution_stage(
            receipt, "INPUT_PREFLIGHT", "BLOCKED",
            str(positive_input_failure.get("reason") or positive_input_failure.get("violation")),
            violation=positive_input_failure.get("violation"), path=positive_input_failure.get("path"),
        )
        return _finish_execution(
            receipt, "BLOCKED", "INPUT_PREFLIGHT_BLOCKED",
            str(positive_input_failure.get("violation")),
        )
    _record_execution_stage(
        receipt, "INPUT_PREFLIGHT", "PASS",
        "manifest and declared positive inputs passed the historical quarantine boundary",
        positive_input_count=len(_positive_manifest_paths(manifest)) + len(request.positive_input_paths),
        allowlisted_asset_count=len(guard.allowlist),
    )

    provenance = verify_reference_provenance(list(manifest.external_references))
    receipt["reference_provenance"] = provenance
    _record_execution_stage(
        receipt, "REFERENCE_PROVENANCE", str(provenance.get("status")),
        str(provenance.get("reason") or "positive references have accepted provenance"),
        valid_references_count=provenance.get("valid_references_count", 0),
    )
    if provenance.get("status") != "PASS":
        return _finish_execution(
            receipt, "BLOCKED", "REFERENCE_PROVENANCE_BLOCKED", str(provenance.get("violation")),
        )

    stage = _stage_creative_workspace(request, manifest, guard, run_id)
    if stage.get("run_id"):
        receipt["run_id"] = stage["run_id"]
    receipt["stage_root"] = stage.get("stage_root")
    receipt["staged_input_inventory"] = stage.get("inventory", [])
    receipt["requested_input_audit"] = stage.get("requested_input_audit", [])
    receipt["controls"]["staged_input_file_count"] = len(stage.get("inventory", []))
    receipt["controls"]["staged_historical_output_files"] = stage.get("staged_historical_output_files", 0)
    _record_execution_stage(
        receipt, "STAGED_CREATIVE_WORKSPACE", str(stage.get("status")),
        str(stage.get("reason") or "validated inputs staged into the clean-room creative pack"),
        stage_root=stage.get("stage_root"),
        staged_input_file_count=len(stage.get("inventory", [])),
        staged_historical_output_files=stage.get("staged_historical_output_files", 0),
    )
    if stage.get("status") != "PASS":
        return _finish_execution(receipt, "BLOCKED", "STAGED_CREATIVE_WORKSPACE_BLOCKED", str(stage.get("reason")))

    scope = dict(request.concept_scope or _default_concept_scope())
    scope_result = validate_pre_generation_scope(scope)
    receipt["pre_generation_scope"] = scope_result
    _record_execution_stage(
        receipt, "PRE_GENERATION_SCOPE", str(scope_result.get("status")),
        str(scope_result.get("reason") or "three concept builder tasks limited to hero and signature device"),
        allowed_surfaces=scope_result.get("allowed_surfaces", []),
        builder_task_emitted=False,
    )
    if scope_result.get("status") != "PASS":
        return _finish_execution(receipt, "FAIL", "PRE_GENERATION_SCOPE_FAILED", str(scope_result.get("reason")))

    pre_render_baseline = guard.check_input_path(request.negative_baseline_path, is_post_render_negative_baseline=False)
    receipt["controls"]["negative_baseline_access_before_render"] = "BLOCKED" \
        if pre_render_baseline.get("status") == "BLOCKED" else str(pre_render_baseline.get("status"))
    _record_execution_stage(
        receipt, "NEGATIVE_BASELINE_PRE_RENDER", "PASS" if pre_render_baseline.get("status") == "BLOCKED" else "BLOCKED",
        "historical baseline access probe was blocked before candidate render; no baseline read occurred",
        access_result=pre_render_baseline.get("status"), read_performed=False,
    )
    if pre_render_baseline.get("status") != "BLOCKED":
        return _finish_execution(receipt, "BLOCKED", "NEGATIVE_BASELINE_PRE_RENDER_BLOCKED", "NEGATIVE_BASELINE_NOT_QUARANTINED")

    try:
        generator_package = _build_generation_package(request, manifest, stage, scope)
    except (OSError, TypeError, ValueError) as exc:
        _record_execution_stage(receipt, "PRE_GENERATION_SCOPE", "BLOCKED", _adapter_error(exc))
        return _finish_execution(receipt, "BLOCKED", "GENERATOR_PACKAGE_BLOCKED", "GENERATOR_PACKAGE_INVALID")
    receipt["generator_package"] = generator_package
    receipt["controls"]["generator_package_historical_sentinels"] = _sentinel_count(generator_package)
    if receipt["controls"]["generator_package_historical_sentinels"]:
        return _finish_execution(receipt, "BLOCKED", "GENERATOR_PACKAGE_BLOCKED", "GENERATOR_PACKAGE_HISTORICAL_SENTINEL_PRESENT")

    try:
        if request.adapters.on_stage_ready:
            request.adapters.on_stage_ready(str(stage["stage_root"]), generator_package)
        concept_package = request.adapters.generate_concepts(manifest)
    except Exception as exc:  # noqa: BLE001 - provider-neutral boundary must fail closed
        _record_execution_stage(receipt, "CONCEPT_GENERATION", "BLOCKED", "concept adapter raised", error=_adapter_error(exc))
        return _finish_execution(receipt, "BLOCKED", "CONCEPT_GENERATION_BLOCKED", "CLEAN_ROOM_CONCEPT_ADAPTER_ERROR")
    if not isinstance(concept_package, Mapping):
        _record_execution_stage(receipt, "CONCEPT_GENERATION", "BLOCKED", "concept adapter did not return an object")
        return _finish_execution(receipt, "BLOCKED", "CONCEPT_GENERATION_BLOCKED", "CLEAN_ROOM_CONCEPT_OUTPUT_INVALID")
    concept_package = dict(concept_package)
    receipt["pre_generation_scope"]["builder_task_emitted"] = True
    _record_execution_stage(
        receipt, "CONCEPT_GENERATION", "PASS", "concept adapter returned a bounded candidate package",
        concept_count=len(concept_package.get("concepts", [])) if isinstance(concept_package.get("concepts"), list) else None,
    )

    concept_gate = enforce_cheap_concept_gate(concept_package)
    receipt["concept_gate"] = concept_gate
    receipt["post_generation_scope_verification"] = concept_gate
    _record_execution_stage(
        receipt, "CHEAP_CONCEPT_GATE", str(concept_gate.get("status")),
        str(concept_gate.get("reason") or "three hero-plus-signature-device concepts accepted"),
        scope=concept_gate.get("scope"),
    )
    if concept_gate.get("status") != "PASS":
        return _finish_execution(receipt, "FAIL", "CHEAP_CONCEPT_GATE_FAILED", str(concept_gate.get("reason")))

    try:
        rendered = request.adapters.render_candidate(concept_package)
    except Exception as exc:  # noqa: BLE001 - provider-neutral boundary must fail closed
        _record_execution_stage(receipt, "CANDIDATE_RENDER", "BLOCKED", "candidate renderer raised", error=_adapter_error(exc))
        return _finish_execution(receipt, "BLOCKED", "CANDIDATE_RENDER_BLOCKED", "CLEAN_ROOM_RENDER_ADAPTER_ERROR")
    if not isinstance(rendered, Mapping):
        _record_execution_stage(receipt, "CANDIDATE_RENDER", "BLOCKED", "candidate renderer did not return an object")
        return _finish_execution(receipt, "BLOCKED", "CANDIDATE_RENDER_BLOCKED", "CLEAN_ROOM_RENDER_OUTPUT_INVALID")
    rendered = _persist_rendered_artifacts(stage.get("stage_root"), rendered)
    candidate_screenshot = rendered.get("candidate_screenshot")
    candidate_morphology = _mapping_value(rendered, "morphology") or _mapping_value(rendered, "candidate_morphology")
    candidate_evidence = _mapping_value(rendered, "rendered_morphology_evidence")
    if not isinstance(candidate_screenshot, str) or not candidate_screenshot.strip() or (not candidate_morphology and not candidate_evidence):
        _record_execution_stage(
            receipt, "CANDIDATE_RENDER", "BLOCKED",
            "candidate render must return a screenshot identity and declared or rendered morphology evidence",
        )
        return _finish_execution(receipt, "BLOCKED", "CANDIDATE_RENDER_BLOCKED", "CLEAN_ROOM_RENDER_OUTPUT_INVALID")
    candidate_path_check = guard.check_input_path(candidate_screenshot)
    if candidate_path_check.get("status") != "PASS":
        _record_execution_stage(receipt, "CANDIDATE_RENDER", "BLOCKED", "candidate render resolved to a quarantined historical path", path=candidate_path_check.get("path"))
        return _finish_execution(receipt, "BLOCKED", "CANDIDATE_RENDER_BLOCKED", "CLEAN_ROOM_INPUT_VIOLATION")
    _record_execution_stage(receipt, "CANDIDATE_RENDER", "PASS", "candidate hero and signature device rendered", candidate_screenshot=candidate_screenshot)
    receipt["candidate_render"] = {
        "candidate_screenshot": candidate_screenshot,
        "candidate_screenshot_sha256": rendered.get("candidate_screenshot_sha256"),
        "morphology": dict(candidate_morphology or {}),
        "rendered_morphology_evidence": dict(candidate_evidence or {}),
        "rendered_dom_ref": rendered.get("rendered_dom_ref"),
        "rendered_css_ref": rendered.get("rendered_css_ref"),
    }

    baseline_access = guard.check_input_path(request.negative_baseline_path, is_post_render_negative_baseline=True)
    _record_execution_stage(
        receipt, "NEGATIVE_BASELINE_ACCESS", str(baseline_access.get("status")),
        str(baseline_access.get("reason") or "negative baseline access opened after candidate render"),
        path=baseline_access.get("path"), role=baseline_access.get("role", "NEGATIVE_BASELINE_ONLY"),
    )
    if baseline_access.get("status") != "PASS":
        return _finish_execution(receipt, "BLOCKED", "NEGATIVE_BASELINE_BLOCKED", "NEGATIVE_BASELINE_PRE_RENDER_ACCESS")
    receipt["controls"]["negative_baseline_read_after_render"] = True
    try:
        baseline_payload = request.adapters.load_negative_baseline(request.negative_baseline_path)
    except Exception as exc:  # noqa: BLE001 - provider-neutral boundary must fail closed
        _record_execution_stage(receipt, "NEGATIVE_BASELINE_LOAD", "BLOCKED", "negative baseline loader raised", error=_adapter_error(exc))
        return _finish_execution(receipt, "BLOCKED", "NEGATIVE_BASELINE_BLOCKED", "CLEAN_ROOM_BASELINE_ADAPTER_ERROR")
    if not isinstance(baseline_payload, Mapping):
        _record_execution_stage(receipt, "NEGATIVE_BASELINE_LOAD", "BLOCKED", "negative baseline loader did not return an object")
        return _finish_execution(receipt, "BLOCKED", "NEGATIVE_BASELINE_BLOCKED", "CLEAN_ROOM_BASELINE_OUTPUT_INVALID")
    baseline_payload = dict(baseline_payload)
    baseline_evidence = _mapping_value(baseline_payload, "rendered_morphology_evidence")
    baseline_morphology = _mapping_value(baseline_payload, "morphology") or (
        baseline_payload if not baseline_evidence else None
    )
    if not baseline_morphology and not baseline_evidence:
        _record_execution_stage(receipt, "NEGATIVE_BASELINE_LOAD", "BLOCKED", "negative baseline did not return morphology evidence")
        return _finish_execution(receipt, "BLOCKED", "NEGATIVE_BASELINE_BLOCKED", "CLEAN_ROOM_BASELINE_OUTPUT_INVALID")
    _record_execution_stage(receipt, "NEGATIVE_BASELINE_LOAD", "PASS", "historical output was loaded only as a negative baseline", role="NEGATIVE_BASELINE_ONLY")
    receipt["negative_baseline"] = {
        "path": request.negative_baseline_path,
        "role": "NEGATIVE_BASELINE_ONLY",
        "morphology": dict(baseline_morphology or {}),
        "rendered_morphology_evidence": dict(baseline_evidence or {}),
    }

    if candidate_evidence or baseline_evidence:
        if not candidate_evidence or not baseline_evidence:
            _record_execution_stage(receipt, "RENDER_DERIVED_MORPHOLOGY", "BLOCKED", "both candidate and baseline browser layout evidence are required")
            return _finish_execution(receipt, "BLOCKED", "RENDER_DERIVED_MORPHOLOGY_BLOCKED", "RENDERED_BROWSER_LAYOUT_EVIDENCE_INCOMPLETE")
        divergence = compare_rendered_morphology(
            candidate_evidence,
            baseline_evidence,
            evaluation_stage=concept_gate.get("scope"),
        )
        receipt["render_derived_morphology"] = divergence
        _record_execution_stage(
            receipt, "RENDER_DERIVED_MORPHOLOGY", str(divergence.get("status")),
            str(divergence.get("divergence")),
            semantic_labels_used=divergence.get("semantic_labels_used", False),
            failures=divergence.get("failures", []),
        )
        if divergence.get("status") != "PASS_DIVERGENCE":
            blocked = divergence.get("status") == "BLOCKED_INSUFFICIENT_EVIDENCE"
            return _finish_execution(
                receipt,
                "BLOCKED" if blocked else "FAIL",
                "RENDER_DERIVED_MORPHOLOGY_BLOCKED" if blocked else "RENDER_DERIVED_MORPHOLOGY_FAILED",
                str(divergence.get("divergence")),
            )
    else:
        divergence = evaluate_morphology_divergence(dict(candidate_morphology or {}), dict(baseline_morphology or {}))
        receipt["render_derived_morphology"] = {
            "status": "NOT_EVALUATED",
            "reason": "RENDERED_BROWSER_LAYOUT_EVIDENCE_NOT_PROVIDED",
            "declared_morphology_fallback": divergence,
        }
        _record_execution_stage(receipt, "RENDER_DERIVED_MORPHOLOGY", "PASS", "legacy adapter supplied unit morphology; rendered evidence not provided")
        if divergence.get("status") != "PASS":
            blocked = divergence.get("status") == "BLOCKED_INSUFFICIENT_EVIDENCE"
            return _finish_execution(
                receipt,
                "BLOCKED" if blocked else "FAIL",
                "MORPHOLOGY_DIVERGENCE_BLOCKED" if blocked else "MORPHOLOGY_DIVERGENCE_FAILED",
                str(divergence.get("divergence")),
            )

    fixture_comparisons = {}
    for key, label in (("semantic_rename_morphology_evidence", "SEMANTIC_RENAME_RENDER_FIXTURE"), ("genuine_divergence_morphology_evidence", "GENUINE_DIVERGENCE_RENDER_FIXTURE")):
        fixture_evidence = _mapping_value(rendered, key)
        if fixture_evidence and baseline_evidence:
            fixture_comparisons[label] = compare_rendered_morphology(
                fixture_evidence,
                baseline_evidence,
                evaluation_stage=concept_gate.get("scope"),
            )
    if fixture_comparisons:
        receipt["rendered_fixture_comparisons"] = fixture_comparisons

    if not request.business_brief.strip() or not request.brand_brief.strip():
        _record_execution_stage(receipt, "BLIND_CRITIC_PACKAGE", "BLOCKED", "business and brand briefs are required")
        return _finish_execution(receipt, "BLOCKED", "BLIND_CRITIC_BLOCKED", "BLIND_CRITIC_BRIEFS_MISSING")
    positive_refs = [
        str(item.get("staged_path")) for item in generator_package.get("positive_reference_list", [])
        if isinstance(item, Mapping) and item.get("staged_path")
    ] or [str(path) for path in request.external_reference_screenshots]
    critic_package = prepare_blind_critic_package(
        candidate_screenshot=candidate_screenshot,
        external_references=positive_refs,
        business_brief=request.business_brief,
        brand_brief=request.brand_brief,
        rendered_dom_ref=rendered.get("rendered_dom_ref"),
        rendered_css_ref=rendered.get("rendered_css_ref"),
        morphology_evidence=candidate_evidence,
    )
    sentinel_leaks = _sentinel_count(critic_package)
    receipt["controls"]["blind_critic_sentinel_leaks"] = sentinel_leaks
    receipt["blind_critic_package"] = critic_package
    _record_execution_stage(
        receipt, "BLIND_CRITIC_PACKAGE", "PASS" if sentinel_leaks == 0 else "BLOCKED",
        "critic package contains rendered evidence and briefs only",
        implementation_source_excluded=all(critic_package.get(key) is None for key in ("html_source", "css_source", "class_names", "direction_name", "builder_commentary", "self_awarded_scores", "previous_asn_screenshots")),
        sentinel_leaks=sentinel_leaks,
    )
    if sentinel_leaks:
        return _finish_execution(receipt, "BLOCKED", "BLIND_CRITIC_BLOCKED", "BLIND_CRITIC_SENTINEL_LEAK")

    try:
        critic_result = request.adapters.run_blind_critic(critic_package)
    except Exception as exc:  # noqa: BLE001 - provider-neutral boundary must fail closed
        _record_execution_stage(receipt, "BLIND_CRITIC", "BLOCKED", "blind critic adapter raised", error=_adapter_error(exc))
        return _finish_execution(receipt, "BLOCKED", "BLIND_CRITIC_BLOCKED", "CLEAN_ROOM_CRITIC_ADAPTER_ERROR")
    if not isinstance(critic_result, Mapping):
        _record_execution_stage(receipt, "BLIND_CRITIC", "BLOCKED", "blind critic did not return an object")
        return _finish_execution(receipt, "BLOCKED", "BLIND_CRITIC_BLOCKED", "CLEAN_ROOM_CRITIC_OUTPUT_INVALID")
    critic_result = dict(critic_result)
    critic_status = str(critic_result.get("status", "PASS"))
    _record_execution_stage(receipt, "BLIND_CRITIC", critic_status, "existing Website Gauntlet authority package completed")
    receipt["blind_critic_result"] = critic_result
    if critic_status in {"BLOCKED", "FAIL"}:
        return _finish_execution(receipt, critic_status, "BLIND_CRITIC_FAILED", critic_status)

    owner_gate = validate_owner_concept_selection(request.owner_selection_event, concept_package)
    receipt["owner_selection"] = owner_gate
    _record_execution_stage(
        receipt, "OWNER_CONCEPT_SELECTION_GATE", str(owner_gate.get("status")),
        str(owner_gate.get("reason") or "existing visual-prototype owner authority evaluated"),
        before_full_homepage_design=owner_gate.get("before_full_homepage_design"),
        after_full_homepage_design=owner_gate.get("after_full_homepage_design"),
    )
    if owner_gate.get("status") == "PENDING":
        receipt["owner_concept_selection"] = "PENDING"
        return _finish_execution(receipt, "PASS", "OWNER_CONCEPT_SELECTION_PENDING", "owner selection remains required before full-homepage progression")
    if owner_gate.get("status") != "PASS":
        return _finish_execution(receipt, "BLOCKED", "OWNER_CONCEPT_SELECTION_BLOCKED", "OWNER_CONCEPT_SELECTION_INVALID")
    receipt["owner_concept_selection"] = "CONFIRMED"
    receipt["full_homepage_design"] = "AUTHORIZED"
    return _finish_execution(receipt, "PASS", "FULL_HOMEPAGE_AUTHORIZED", "owner selected a rendered concept; full homepage progression is now authorized")


def execute_clean_room_workflow(request: CleanRoomExecutionRequest) -> Dict[str, Any]:
    """Compatibility alias for the canonical clean-room concept boundary."""
    return prepare_clean_room_concept_run(request)


def run_clean_room_creative_mode(request: CleanRoomExecutionRequest) -> Dict[str, Any]:
    """Compatibility-friendly alias for the canonical clean-room boundary."""
    return prepare_clean_room_concept_run(request)


def _synthetic_genuine_candidate_html() -> str:
    return """<!doctype html>
<meta charset="utf-8">
<style>
:root { font-family: "Consolas", monospace; color: #f5f3ed; background: #111; }
* { box-sizing: border-box; }
body { margin: 0; background: #111; }
main { width: 100%; }
main > section { min-height: 720px; padding: 120px 9vw; display: block; }
.hero { min-height: 720px; padding: 120px 9vw; background: #1e2522; display: grid; grid-template-columns: 1fr 320px; gap: 8vw; align-items: center; }
.device { width: 760px; height: 120px; border: 2px solid #e3d17a; background: #384842; }
.signature-surface { min-height: 720px; display: flex; align-items: center; justify-content: center; background: #101513; }
.hero-visual { width: 280px; height: 280px; border-radius: 50%; background: #31463d; }
.cta { display: inline-block; margin-top: 24px; padding: 14px 22px; color: #111; background: #e3d17a; }
h1 { font-size: 64px; line-height: .95; margin: 0 0 30px; }
h2 { font-size: 32px; }
</style>
<main>
  <section class="hero"><div><h1>Calibrate the next move.</h1><p>Evidence-led transformation for demanding systems.</p><a class="cta" data-clean-room-cta href="#contact">Start the review</a></div><div class="hero-visual" role="img" aria-label="abstract visual"></div></section>
  <section class="signature-surface" data-clean-room-surface="signature-device"><div class="device" aria-label="signature device"></div></section>
</main>"""


def _synthetic_semantic_clone_html() -> str:
    return """<!doctype html>
<meta charset="utf-8">
<style>
:root { font-family: "Georgia", serif; color: #1b2430; background: #f5f1e8; }
* { box-sizing: border-box; }
body { margin: 0; background: #f5f1e8; }
main { width: min(1100px, calc(100% - 80px)); margin: 0 auto; }
main > section { min-height: 520px; padding: 64px 58px; display: grid; grid-template-columns: 1fr 1fr; gap: 34px; border: 1px solid #9b8b6e; }
.cinematic-chapter:first-child { min-height: 520px; display: grid; align-items: center; }
.transformation-act { grid-column: 1; }
.immersive-sequence { grid-column: 2; min-height: 150px; background: #d9d0bf; }
main > section:nth-child(even) .transformation-act { grid-column: 2; }
main > section:nth-child(even) .immersive-sequence { grid-column: 1; }
.command-module { display: inline-block; margin-top: 24px; padding: 14px 22px; color: #f5f1e8; background: #1b2430; }
h1 { font-size: 52px; line-height: 1; margin: 0 0 24px; }
h2 { font-size: 30px; }
</style>
<main>
  <section class="cinematic-chapter"><div class="transformation-act"><h1>Calibrate the next move.</h1><p>Evidence-led transformation for demanding systems.</p><a class="command-module" data-clean-room-cta href="#contact">Start the review</a></div><figure class="immersive-sequence"></figure></section>
  <section class="cinematic-chapter" data-clean-room-surface="signature-device"><div class="transformation-act"><h2>Signal</h2><p>Read the conditions before deciding.</p></div><figure class="immersive-sequence"></figure></section>
</main>"""


def _create_synthetic_fixture(source_root: Path) -> None:
    source_root.mkdir(parents=True, exist_ok=True)
    for directory in ("historical-project", "brand", "external-references", "business"):
        (source_root / directory).mkdir(parents=True, exist_ok=True)
    pixel = bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d49444154789c6360f8cf00000004000101a2b4ddbd0000000049454e44ae426082")
    (source_root / "historical-project" / "old-hero.jpg").write_bytes(pixel)
    (source_root / "historical-project" / "rejected-screenshot.png").write_bytes(pixel)
    (source_root / "external-references" / "reference-01.png").write_bytes(pixel)
    (source_root / "external-references" / "reference-02.png").write_bytes(pixel)
    (source_root / "brand" / "allowed-logo.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 10 10\"><rect width=\"10\" height=\"10\"/></svg>\n", encoding="utf-8")
    (source_root / "business" / "brief.json").write_text(json.dumps({"business": "Synthetic systems studio", "truth": "Evidence-led work."}, indent=2) + "\n", encoding="utf-8")
    (source_root / "business" / "owner-intent.json").write_text("{\"owner_intent\": \"Precise and deliberate.\"}\n", encoding="utf-8")
    (source_root / "business" / "measurement.json").write_text("{\"primary_conversion\": \"review\"}\n", encoding="utf-8")
    (source_root / "business" / "content.json").write_text("{\"content_truth\": \"Synthetic content only.\"}\n", encoding="utf-8")
    (source_root / "historical-project" / "old-style.css").write_text("""body { margin: 0; background: #f5f1e8; font-family: Georgia, serif; color: #1b2430; }
main { width: min(1100px, calc(100% - 80px)); margin: 0 auto; }
main > section { min-height: 260px; padding: 64px 58px; display: grid; grid-template-columns: 1fr 1fr; gap: 34px; border: 1px solid #9b8b6e; }
.old-hero { min-height: 520px; align-items: center; }
.old-copy { grid-column: 1; }
.old-media-panel { grid-column: 2; min-height: 150px; background: #d9d0bf; }
main > section:nth-child(even) .old-copy { grid-column: 2; }
main > section:nth-child(even) .old-media-panel { grid-column: 1; }
.old-cta { display: inline-block; margin-top: 24px; padding: 14px 22px; color: #f5f1e8; background: #1b2430; }
""", encoding="utf-8")
    (source_root / "historical-project" / "old-site.html").write_text("""<!doctype html>
<meta charset="utf-8"><link rel="stylesheet" href="old-style.css">
<main>
  <section class="old-hero old-two-column-card"><div class="old-copy"><h1>Old direction</h1><p>NEVER_SHOW_THIS_TO_GENERATOR</p><a class="old-cta" data-clean-room-cta href="#contact">Continue</a></div><figure class="old-media-panel"><img src="old-hero.jpg" alt="old hero"></figure></section>
  <section class="old-two-column-card" data-clean-room-surface="signature-device"><figure class="old-media-panel"></figure><div class="old-copy"><h2>Signal</h2><p>Previous generated material.</p></div></section>
</main>""", encoding="utf-8")
class _SyntheticCleanRoomAdapters:
    """Deterministic adapters used by the local end-to-end proof command."""

    def __init__(self, source_root: Path) -> None:
        self.events: List[str] = []
        self.source_root = source_root
        self.stage_root: Optional[Path] = None

    def on_stage_ready(self, stage_root: str, _package: Mapping[str, Any]) -> None:
        self.stage_root = Path(stage_root)

    @staticmethod
    def _playwright_observation(project_root: Path, serve_dir: str, route: str) -> Mapping[str, Any]:
        browser_root = str(Path(__file__).resolve().parents[1] / "browser-qa")
        if browser_root not in sys.path:
            sys.path.insert(0, browser_root)
        from engine.base import load_engine  # type: ignore[import-not-found]

        engine = load_engine(
            "playwright",
            str(project_root),
            {
                "serve_dir": serve_dir,
                "capture_render_artifacts": True,
                "capture_morphology_evidence": True,
                "morphology_evaluation_stage": "HERO_PLUS_SIGNATURE_DEVICE_ONLY",
            },
        )
        if not engine.available():
            raise RuntimeError("PLAYWRIGHT_ENGINE_UNAVAILABLE")
        engine.start()
        try:
            observation = engine.observe(route, 1440, capture="VIEWPORT")
            return dict(observation.raw)
        finally:
            engine.stop()

    def generate_concepts(self, manifest: CleanRoomManifest) -> Mapping[str, Any]:
        self.events.append("generate_concepts")
        return {
            "concepts": [
                {"concept_id": "concept-a", "built_surfaces": ["desktop_hero", "signature_device"]},
                {"concept_id": "concept-b", "built_surfaces": ["desktop_hero", "signature_device"]},
                {"concept_id": "concept-c", "built_surfaces": ["desktop_hero", "signature_device"]},
            ]
        }

    def render_candidate(self, concept_package: Mapping[str, Any]) -> Mapping[str, Any]:
        self.events.append("render_candidate")
        if self.stage_root is None:
            raise RuntimeError("SYNTHETIC_STAGE_NOT_READY")
        candidate = self.stage_root / "candidate-output" / "candidate.html"
        clone = self.stage_root / "candidate-output" / "semantic-clone.html"
        candidate.write_text(_synthetic_genuine_candidate_html(), encoding="utf-8")
        clone.write_text(_synthetic_semantic_clone_html(), encoding="utf-8")
        candidate_raw = self._playwright_observation(self.stage_root, "candidate-output", "/candidate.html")
        clone_raw = self._playwright_observation(self.stage_root, "candidate-output", "/semantic-clone.html")
        return {
            "screenshot_bytes": candidate_raw["screenshot_bytes"],
            "rendered_dom": candidate_raw.get("rendered_dom", ""),
            "rendered_css": candidate_raw.get("rendered_css", ""),
            "rendered_morphology_evidence": candidate_raw["rendered_morphology_evidence"],
            "semantic_rename_morphology_evidence": clone_raw["rendered_morphology_evidence"],
            "genuine_divergence_morphology_evidence": candidate_raw["rendered_morphology_evidence"],
            "morphology": {"source": "BROWSER_LAYOUT_EVIDENCE"},
            "builder_metadata": {
                "SECRET_BUILDER_SCORE": 99.9,
                "SECRET_CLASS_NAME": "cinematic-masterpiece",
                "SECRET_BUILDER_COMMENT": "definitely premium",
            },
        }

    def load_negative_baseline(self, path: str) -> Mapping[str, Any]:
        self.events.append("load_negative_baseline")
        if self.stage_root is None:
            raise RuntimeError("SYNTHETIC_STAGE_NOT_READY")
        baseline_root = self.source_root / "historical-project"
        baseline_raw = self._playwright_observation(baseline_root, ".", "/old-site.html")
        return {
            "rendered_morphology_evidence": baseline_raw["rendered_morphology_evidence"],
        }

    def run_blind_critic(self, package: Mapping[str, Any]) -> Mapping[str, Any]:
        self.events.append("run_blind_critic")
        serialized = json.dumps(package, sort_keys=True)
        leaks = [sentinel for sentinel in BLIND_CRITIC_SENTINELS if sentinel in serialized]
        return {
            "status": "PASS" if not leaks else "FAIL",
            "review_id": "synthetic-blind-critic-01",
            "sentinel_leaks": leaks,
            "dimensions": {
                "VISUAL_DISTINCTIVENESS": "PASS",
                "HERO_COMPOSITION": "PASS",
                "SIGNATURE_VISUAL_DEVICE": "PASS",
            },
        }


def synthetic_clean_room_request(run_id: str = "synthetic-clean-room-run") -> tuple[CleanRoomExecutionRequest, _SyntheticCleanRoomAdapters]:
    """Create the synthetic repository fixture and a non-ASN execution request."""
    runtime_root = Path(".clean-room-runs").resolve()
    source_root = runtime_root / f"{_safe_run_id(run_id)}-source-{uuid.uuid4().hex[:8]}"
    _create_synthetic_fixture(source_root)
    adapters = _SyntheticCleanRoomAdapters(source_root)
    manifest = CleanRoomManifest(
        business_understanding_ref="business/brief.json",
        owner_intent_ref="business/owner-intent.json",
        conversion_requirements_ref="business/measurement.json",
        content_truth_ref="business/content.json",
        reusable_assets=[
            {
                "asset_id": "ALLOWED_LOGO",
                "source_path": "brand/allowed-logo.svg",
                "authorized": True,
                "authorization_basis": "OWNER_ALLOWLIST_ITEM",
            }
        ],
        external_references=[
            {
                "reference_id": "EXT_SYNTHETIC_01",
                "classification": "EXTERNAL_GOLD_STANDARD",
                "url": "https://example.test/clean-room-reference-01",
                "source_path": "external-references/reference-01.png",
            },
            {
                "reference_id": "EXT_SYNTHETIC_02",
                "classification": "OWNER_SUPPLIED_EXTERNAL_REFERENCE",
                "url": "https://example.test/clean-room-reference-02",
                "source_path": "external-references/reference-02.png",
            }
        ],
        staged_inputs=[
            {"source_path": "business/brief.json", "staged_path": "business/brief.json", "classification": "BUSINESS_BRIEF", "authorization_basis": "CURRENT_BUSINESS_UNDERSTANDING"},
            {"source_path": "business/owner-intent.json", "staged_path": "brand/owner-intent.json", "classification": "OWNER_INTENT", "authorization_basis": "CURRENT_OWNER_INTENT"},
            {"source_path": "business/measurement.json", "staged_path": "business/measurement.json", "classification": "CONVERSION_REQUIREMENTS", "authorization_basis": "CURRENT_MEASUREMENT_PLAN"},
            {"source_path": "business/content.json", "staged_path": "business/content.json", "classification": "CONTENT_TRUTH", "authorization_basis": "CURRENT_CONTENT_TRUTH"},
            {"source_path": "brand/allowed-logo.svg", "staged_path": "approved-assets/allowed-logo.svg", "classification": "OWNER_APPROVED_BRAND_ASSET", "authorization_basis": "OWNER_ALLOWLIST_ITEM"},
            {"source_path": "external-references/reference-01.png", "staged_path": "external-references/reference-01.png", "classification": "EXTERNAL_GOLD_STANDARD", "authorization_basis": "REFERENCE_PROVENANCE_EXT_SYNTHETIC_01"},
            {"source_path": "external-references/reference-02.png", "staged_path": "external-references/reference-02.png", "classification": "OWNER_SUPPLIED_EXTERNAL_REFERENCE", "authorization_basis": "REFERENCE_PROVENANCE_EXT_SYNTHETIC_02"},
        ],
    )
    request = CleanRoomExecutionRequest(
        manifest=manifest,
        adapters=CleanRoomExecutionAdapters(
            generate_concepts=adapters.generate_concepts,
            render_candidate=adapters.render_candidate,
            load_negative_baseline=adapters.load_negative_baseline,
            run_blind_critic=adapters.run_blind_critic,
            on_stage_ready=adapters.on_stage_ready,
        ),
        negative_baseline_path="historical-project/old-site.html",
        business_brief="Synthetic business understanding for clean-room execution.",
        brand_brief="Synthetic owner intent for clean-room execution.",
        positive_input_paths=(
            "business/brief.json",
            "business/owner-intent.json",
            "brand/allowed-logo.svg",
            "external-references/reference-01.png",
            "external-references/reference-02.png",
        ),
        external_reference_screenshots=(
            "external-references/reference-01.png",
            "external-references/reference-02.png",
        ),
        run_id=run_id,
        source_root=str(source_root),
        run_root=str(runtime_root),
        requested_input_paths=(
            "historical-project/old-site.html",
            "historical-project/old-style.css",
            "historical-project/old-hero.jpg",
            "historical-project/rejected-screenshot.png",
            "brand/allowed-logo.svg",
            "external-references/reference-01.png",
            "external-references/reference-02.png",
            "business/brief.json",
        ),
        owner_selection_event={
            "STATE_LOCATION": "visual_prototypes.owner_selection_confirmed",
            "OWNER_SELECTION_CONFIRMED": True,
            "OWNER_SELECTED_DIRECTION": "concept-a",
            "OWNER_ACTION": "SELECT",
            "APPROVED_BY": "OWNER",
        },
    )
    return request, adapters


def run_synthetic_clean_room(run_id: str = "synthetic-clean-room-run") -> Dict[str, Any]:
    """Run the complete local proof and include adapter call order in its receipt."""
    request, adapters = synthetic_clean_room_request(run_id)
    receipt = prepare_clean_room_concept_run(request)
    receipt["synthetic"] = True
    receipt["adapter_events"] = list(adapters.events)
    return receipt


def _write_receipt(path: str, receipt: Mapping[str, Any]) -> None:
    destination = Path(path).resolve()
    forbidden_parts = {part.casefold() for part in destination.parts}
    if forbidden_parts.intersection({"projects", "review-workspaces"}):
        raise ValueError("clean-room receipts cannot be written under quarantined project paths")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the bounded Website Director clean-room execution proof")
    parser.add_argument("--synthetic", action="store_true", help="run the deterministic provider-neutral proof")
    parser.add_argument("--output", help="optional local receipt path outside projects/ and review-workspaces/")
    args = parser.parse_args(argv)
    if not args.synthetic:
        parser.error("provider execution is not implicit; pass --synthetic for the local proof")

    receipt = run_synthetic_clean_room()
    if args.output:
        _write_receipt(args.output, receipt)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
