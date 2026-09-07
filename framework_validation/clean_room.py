"""Clean-Room Creative Mode Engine and Verification Rules for Website Director.

This module provides the deterministic clean-room creative input firewall,
historical quarantine checks, asset allowlisting, reference provenance verification,
cheap concept gate enforcement, blind critic packaging, and morphology divergence checks.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

QUARANTINED_PATH_PREFIXES = (
    "projects/",
    "review-workspaces/",
)

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

        normalized = path_str.replace("\\", "/").lstrip("./")

        # Check quarantine prefixes
        is_historical = any(normalized.startswith(prefix) for prefix in QUARANTINED_PATH_PREFIXES)

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

        normalized = source_path.replace("\\", "/").lstrip("./")
        is_historical = any(normalized.startswith(prefix) for prefix in QUARANTINED_PATH_PREFIXES)

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
    brand_brief: str
) -> Dict[str, Any]:
    """Prepare a stripped, blind evaluation package for the Website Gauntlet critic."""
    return {
        "candidate_screenshot": candidate_screenshot,
        "external_reference_screenshots": external_references,
        "business_brief": business_brief,
        "brand_brief": brand_brief,
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
    """Evaluate whether candidate geometry genuinely diverges from historical negative baseline."""
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
