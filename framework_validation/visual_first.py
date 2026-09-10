"""Deterministic contracts for Website Director's visual-first taste flow.

This module is deliberately small and provider-neutral.  It extends the
existing design-first and visual-prototype authorities with project-local taste
data, concept feasibility, owner selection, hot-path context compilation,
pairwise quality authority, and bounded design-risk reporting.  It does not
generate images, call a model, write project state, start a browser, create a
new lifecycle phase, or create an owner lock.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from typing import Any, Callable


AMBITION_TIERS = ("STANDARD", "PREMIUM", "SHOWCASE", "EXPERIMENTAL")
TECHNICAL_TASK_KINDS = frozenset({"TECHNICAL_TASK", "BUG_FIX", "BACKEND", "TRIVIAL_EDIT"})

TASTE_CONTRACT_FIELDS = (
    "ambition_tier",
    "project_category",
    "design_lane",
    "desired_emotional_character",
    "approved_references",
    "rejected_references",
    "approved_reference_traits",
    "rejected_reference_traits",
    "anti_taste",
    "typography_lane",
    "typography_personality",
    "material_language",
    "visual_world_strategy",
    "motion_appetite",
    "visual_density",
    "design_variance",
    "composition_preferences",
    "signature_requirement",
    "owner_selected_visual_direction",
    "owner_visual_direction_confirmed",
)

MATERIAL_LANGUAGES = ("RAW_FLAT", "SUBTLE_TACTILE", "CHROMATIC_DEPTH", "INTERACTIVE_CANVAS")
CONCEPT_FORMATS = (
    "RASTER_TARGET",
    "HTML_CSS_PROTOTYPE",
    "MOTION_STORYBOARD",
    "INTERACTION_SANDBOX",
)
COMPOSITION_PRIMITIVES = (
    "sticky_split_rail",
    "horizontal_story_track",
    "offset_overlap_plane",
    "full_bleed_media_field",
    "edge_anchored_typography",
    "editorial_multicolumn",
    "viewport_monolith",
    "layered_depth_canvas",
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
DESIGN_RISK_FLAGS = (
    "DEFAULT_RADIUS_UNIFORMITY",
    "UNTRACKED_DEFAULT_DISPLAY_FONT",
    "GENERIC_FEATURE_TRIAD",
    "VISUAL_WORLD_ABSENT",
    "REQUIRED_ASSET_ABSENT",
    "SIGNATURE_ONLY_DECLARED",
    "REFERENCE_TRAITS_NOT_OBSERVABLE",
    "VISUAL_TARGET_DRIFT",
    "REPETITIVE_SECTION_RHYTHM",
    "UNMOTIVATED_UI_CHROME",
)
ON_DEMAND_SPECIALISTS = ("GSAP", "THREEJS", "WEBGL", "CINEMATIC_SCROLL", "SHADER_SYSTEMS")
SOURCE_IMPORT_MODES = ("ADAPTED", "CONCEPT_ONLY", "ON_DEMAND", "REJECTED")
TYPOGRAPHY_RESOLUTION_ORDER = (
    "CLIENT_SUPPLIED_LICENSED",
    "APPROVED_BRAND_FONT",
    "VERIFIED_OPEN_FONT",
    "CURATED_SYSTEM_STACK",
)

_NORMALIZE_RE = re.compile(r"[^A-Z0-9]+")
_DEFAULT_PATTERN_NAMES = frozenset(
    {
        "SYMMETRY",
        "CARDS",
        "FLAT_COLOR",
        "PURE_BLACK",
        "PURE_WHITE",
        "SMALL_TYPE",
        "ROUNDED_CORNERS",
        "DARK_MODE",
    }
)


def _normalize(value: Any) -> str:
    return _NORMALIZE_RE.sub("_", str(value).upper()).strip("_")


def _truthy(value: Any) -> bool:
    return value is True or (isinstance(value, str) and _normalize(value) in {"TRUE", "YES", "PASS", "VERIFIED"})


def _present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, Mapping) or isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return bool(value)
    return True


def _issue(code: str, message: str, **extra: Any) -> dict[str, Any]:
    return {"code": code, "message": message, **extra}


def _result(status: str, issues: Sequence[Mapping[str, Any]] = (), **data: Any) -> dict[str, Any]:
    normalized = [dict(issue) for issue in issues]
    result: dict[str, Any] = {"status": status, "ok": status == "PASS", "issues": normalized}
    result.update(data)
    return result


def _as_records(value: Any) -> list[Mapping[str, Any]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return [item for item in value if isinstance(item, Mapping)]


def validate_taste_contract(contract: Mapping[str, Any], *, active_project_id: str | None = None) -> dict[str, Any]:
    """Validate a project-local taste contract without supplying defaults."""

    if not isinstance(contract, Mapping):
        return _result("BLOCKED", [_issue("TASTE_CONTRACT_REQUIRED", "project taste contract must be an object")])

    issues: list[dict[str, Any]] = []
    missing = [field for field in TASTE_CONTRACT_FIELDS if field not in contract]
    if missing:
        issues.append(_issue("TASTE_CONTRACT_INCOMPLETE", "required taste fields are missing", missing=missing))

    tier = _normalize(contract.get("ambition_tier"))
    if tier not in AMBITION_TIERS:
        issues.append(_issue("AMBITION_TIER_INVALID", f"unsupported ambition tier: {contract.get('ambition_tier')!r}"))

    material = _normalize(contract.get("material_language"))
    if material not in MATERIAL_LANGUAGES:
        issues.append(_issue("MATERIAL_LANGUAGE_INVALID", f"unsupported material language: {contract.get('material_language')!r}"))

    for field in ("approved_references", "rejected_references", "approved_reference_traits", "rejected_reference_traits", "anti_taste", "composition_preferences"):
        if field in contract and not isinstance(contract[field], list):
            issues.append(_issue("TASTE_FIELD_TYPE_INVALID", f"{field} must be a list"))
    if "owner_visual_direction_confirmed" in contract and not isinstance(contract["owner_visual_direction_confirmed"], bool):
        issues.append(_issue("OWNER_CONFIRMATION_TYPE_INVALID", "owner_visual_direction_confirmed must be boolean"))
    if "design_variance" in contract:
        variance = contract["design_variance"]
        if isinstance(variance, bool) or not isinstance(variance, (int, float)) or not 0 <= variance <= 10:
            issues.append(_issue("DESIGN_VARIANCE_INVALID", "design_variance must be a number from 0 to 10"))
    if not _present(contract.get("project_category")):
        issues.append(_issue("PROJECT_CATEGORY_REQUIRED", "project_category must be explicit"))
    if active_project_id is not None and contract.get("project_id") not in {None, active_project_id}:
        issues.append(_issue("CROSS_CLIENT_TASTE_ISOLATION", "taste contract project_id does not match the active project"))

    hard_failure_codes = {"AMBITION_TIER_INVALID", "MATERIAL_LANGUAGE_INVALID", "TASTE_FIELD_TYPE_INVALID", "OWNER_CONFIRMATION_TYPE_INVALID", "DESIGN_VARIANCE_INVALID", "PROJECT_CATEGORY_REQUIRED", "CROSS_CLIENT_TASTE_ISOLATION"}
    status = "FAIL" if any(issue["code"] in hard_failure_codes for issue in issues) else ("BLOCKED" if issues else "PASS")
    return _result(status, issues, ambition_tier=tier, material_language=material, fields=list(TASTE_CONTRACT_FIELDS))


def validate_project_taste_isolation(active_project_id: str, contract: Mapping[str, Any]) -> dict[str, Any]:
    """Reject explicit cross-project inheritance and foreign reference records."""

    if not isinstance(active_project_id, str) or not active_project_id.strip():
        return _result("BLOCKED", [_issue("ACTIVE_PROJECT_REQUIRED", "an active project identity is required")])
    if not isinstance(contract, Mapping):
        return _result("BLOCKED", [_issue("TASTE_CONTRACT_REQUIRED", "project taste contract must be an object")])

    issues: list[dict[str, Any]] = []
    observed_project = contract.get("project_id")
    if observed_project != active_project_id:
        issues.append(_issue("CROSS_CLIENT_TASTE_ISOLATION", "taste state must carry the active project identity", observed_project=observed_project, active_project=active_project_id))
    for field in ("inherited_from_project", "source_project_id", "shared_taste_state"):
        value = contract.get(field)
        if _present(value) and value not in {"NONE", "NOT_APPLICABLE", False}:
            issues.append(_issue("CROSS_CLIENT_TASTE_ISOLATION", f"{field} cannot import another project's taste state"))
    for field in ("approved_references", "rejected_references"):
        for index, record in enumerate(_as_records(contract.get(field))):
            owner = record.get("project_id") or record.get("owner_project_id")
            if owner is not None and owner != active_project_id:
                issues.append(_issue("CROSS_CLIENT_TASTE_ISOLATION", f"{field}[{index}] belongs to another project"))
    return _result("FAIL" if issues else "PASS", issues, active_project_id=active_project_id)


def resolve_project_taste(contract: Mapping[str, Any], external_defaults: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Resolve defaults with project taste taking precedence over external priors."""

    if not isinstance(contract, Mapping):
        return _result("BLOCKED", [_issue("TASTE_CONTRACT_REQUIRED", "project taste contract is required")])
    defaults = dict(external_defaults or {})
    resolved = dict(defaults)
    overridden: list[str] = []
    for key in TASTE_CONTRACT_FIELDS:
        if key in contract and _present(contract[key]):
            resolved[key] = contract[key]
            if key in defaults and defaults[key] != contract[key]:
                overridden.append(key)
    return _result("PASS", (), resolved=resolved, overridden_fields=overridden, authority="PROJECT_TASTE_CONTRACT")


def choose_anchor_policy(contract: Mapping[str, Any]) -> dict[str, Any]:
    """Choose category/project anchors without making Awwwards universal."""

    if not isinstance(contract, Mapping):
        return _result("BLOCKED", [_issue("TASTE_CONTRACT_REQUIRED", "anchor selection needs a taste contract")])
    tier = _normalize(contract.get("ambition_tier"))
    category = str(contract.get("project_category") or "").strip()
    has_project_refs = bool(contract.get("approved_references") or contract.get("rejected_references"))
    return _result(
        "PASS",
        (),
        category=category,
        approved_anchor="PROJECT_APPROVED_REFERENCE" if has_project_refs else "CATEGORY_CALIBRATED_QUALITY",
        rejected_anchor="PROJECT_REJECTED_REFERENCE" if has_project_refs else "CATEGORY_CALIBRATED_SLOP",
        awwwards_allowed=tier == "SHOWCASE",
        awwwards_universal=False,
    )


def choose_concept_formats(contract: Mapping[str, Any]) -> tuple[str, ...]:
    """Choose concept representations from project behavior, not one global format."""

    if not isinstance(contract, Mapping):
        return ("HTML_CSS_PROTOTYPE",)
    category = _normalize(contract.get("project_category"))
    lane = _normalize(contract.get("design_lane"))
    motion = _normalize(contract.get("motion_appetite"))
    signature = _normalize(contract.get("signature_requirement"))
    text = " ".join((category, lane, motion, signature))
    formats: list[str] = []
    if any(token in text for token in ("FASHION", "LUXURY", "EDITORIAL", "CAMPAIGN", "BRAND", "ART_DIRECTION")):
        formats.append("RASTER_TARGET")
    if any(token in text for token in ("INTERFACE", "SAAS", "PRODUCT", "APPLICATION", "LAYOUT", "COMPONENT")):
        formats.append("HTML_CSS_PROTOTYPE")
    if any(token in text for token in ("SCROLL", "KINETIC", "CINEMATIC", "MOTION", "HOVER", "TRANSITION")):
        formats.append("MOTION_STORYBOARD")
    if any(token in text for token in ("WEBGL", "THREE", "GAME", "INTERACTIVE", "PROCEDURAL", "SANDBOX")):
        formats.append("INTERACTION_SANDBOX")
    if not formats:
        formats.append("HTML_CSS_PROTOTYPE")
    return tuple(dict.fromkeys(formats))


def route_visual_first(task: Mapping[str, Any] | str, contract: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Route standard, premium, showcase, experimental, and technical work."""

    active_project_id = None
    if isinstance(task, Mapping):
        task_kind = _normalize(task.get("kind") or task.get("type") or task.get("lane"))
        active_project_id = task.get("project_id")
    else:
        task_kind = _normalize(task)
    if task_kind in TECHNICAL_TASK_KINDS:
        return _result(
            "PASS",
            (),
            route="TECHNICAL_TASK",
            taste_required=False,
            visual_direction_studio_required=False,
            owner_visual_gate_required=False,
            image_generation_required=False,
            production_build_allowed=True,
            on_demand_specialists=[],
        )

    validation = validate_taste_contract(contract or {}, active_project_id=active_project_id)
    if validation["status"] != "PASS":
        return _result("BLOCKED" if validation["status"] == "BLOCKED" else "FAIL", validation["issues"], route="TASTE_CONTRACT_REQUIRED", production_build_allowed=False)
    if active_project_id is not None:
        isolation = validate_project_taste_isolation(str(active_project_id), contract or {})
        if isolation["status"] != "PASS":
            return _result(isolation["status"], isolation["issues"], route="TASTE_CONTRACT_ISOLATION", production_build_allowed=False)
    tier = validation["ambition_tier"]
    formats = choose_concept_formats(contract or {})
    if tier == "STANDARD":
        return _result(
            "PASS",
            (),
            route="STANDARD",
            ambition_tier=tier,
            taste_required=True,
            visual_direction_studio_required=False,
            owner_visual_gate_required=False,
            image_generation_required=False,
            image_generation_optional=True,
            direction_count_range=[0, 1],
            concept_formats=list(formats),
            on_demand_specialists=[],
            production_build_allowed=True,
        )
    count = 3 if tier == "SHOWCASE" else 2
    return _result(
        "PASS",
        (),
        route=tier,
        ambition_tier=tier,
        taste_required=True,
        visual_direction_studio_required=True,
        owner_visual_gate_required=True,
        image_generation_required=False,
        image_generation_mode="DYNAMIC_BY_CONCEPT_FORMAT",
        direction_count=count,
        concept_formats=list(formats),
        motion_storyboard_required=tier in {"SHOWCASE", "EXPERIMENTAL"} and _normalize(contract.get("motion_appetite")) not in {"NONE", "MINIMAL"},
        on_demand_specialists=[],
        production_build_allowed=False,
    )


def validate_concept_feasibility(concept: Mapping[str, Any]) -> dict[str, Any]:
    """Require a visual concept to decompose into implementable web topology."""

    if not isinstance(concept, Mapping):
        return _result("BLOCKED", [_issue("CONCEPT_REQUIRED", "visual concept must be an object")])
    required = ("semantic_regions", "layout_tracks", "media_layers", "typography_planes", "interaction_layers", "responsive_interpretation")
    missing = [field for field in required if not _present(concept.get(field))]
    issues: list[dict[str, Any]] = []
    if missing:
        issues.append(_issue("CONCEPT_DECOMPOSITION_INCOMPLETE", "concept lacks implementable topology fields", missing=missing))
    for field in ("impossible_layout", "gibberish_micro_ui", "floating_interface_without_anchor", "not_decomposable"):
        if _truthy(concept.get(field)):
            issues.append(_issue("CONCEPT_FEASIBILITY_FAIL", f"concept declares an impossible or non-decomposable layout: {field}"))
    concept_format = _normalize(concept.get("format"))
    if concept_format not in CONCEPT_FORMATS:
        issues.append(_issue("CONCEPT_FORMAT_INVALID", f"unsupported concept format: {concept.get('format')!r}"))
    prompt = str(concept.get("image_generation_prompt") or concept.get("prompt") or "").casefold()
    forbidden_prompt_terms = ("gibberish micro-ui", "impossible floating interface")
    if any(term in prompt for term in forbidden_prompt_terms):
        issues.append(_issue("CONCEPT_PROMPT_UNSAFE", "image prompt must explicitly avoid impossible UI topology"))
    if concept_format == "RASTER_TARGET" and prompt:
        required_prompt_terms = ("responsive web viewport", "readable hierarchy", "implementable layout", "realistic spacing")
        absent = [term for term in required_prompt_terms if term not in prompt]
        if absent:
            issues.append(_issue("CONCEPT_PROMPT_TOPOLOGY_INCOMPLETE", "raster concept prompt lacks web-topology constraints", missing=absent))
    status = "FAIL" if any(issue["code"].startswith("CONCEPT_FEASIBILITY_FAIL") or issue["code"] in {"CONCEPT_FORMAT_INVALID", "CONCEPT_PROMPT_UNSAFE"} for issue in issues) else ("BLOCKED" if issues else "PASS")
    return _result(status, issues, concept_id=concept.get("concept_id"), concept_format=concept_format, decomposable=not issues)


def evaluate_visual_direction_attempt(
    contract: Mapping[str, Any], concepts: Sequence[Mapping[str, Any]], *, attempt: int = 1
) -> dict[str, Any]:
    """Evaluate a bounded concept attempt and stop after one regeneration."""

    route = route_visual_first("WEBSITE", contract)
    if route["status"] != "PASS":
        return _result(route["status"], route["issues"], owner_gate="NOT_REACHED")
    if route.get("visual_direction_studio_required") is not True:
        return _result("NOT_REQUIRED", (), owner_gate="NOT_REQUIRED", concepts=[])
    if not isinstance(concepts, Sequence) or isinstance(concepts, (str, bytes)):
        return _result("BLOCKED", [_issue("CONCEPTS_REQUIRED", "visual direction studio needs candidate concepts")], owner_gate="NOT_REACHED")
    expected = int(route.get("direction_count", 0))
    if len(concepts) < expected:
        return _result("BLOCKED", [_issue("CONCEPT_COUNT_INCOMPLETE", f"{route['ambition_tier']} requires {expected} divergent concepts")], owner_gate="NOT_REACHED")
    reviewed: list[dict[str, Any]] = []
    for concept in concepts:
        feasibility = validate_concept_feasibility(concept)
        pairwise = _concept_pairwise_precheck(concept)
        reviewed.append({"concept_id": concept.get("concept_id"), "feasibility": feasibility, "pairwise_precheck": pairwise})
    feasible = [item for item in reviewed if item["feasibility"]["status"] == "PASS"]
    rejected = [item for item in feasible if item["pairwise_precheck"] == "CLOSER_TO_REJECTED"]
    if not feasible:
        return _result("FAIL", [_issue("NO_FEASIBLE_CONCEPT", "no concept may reach the owner gate")], owner_gate="NOT_REACHED", concepts=reviewed, attempt=attempt)
    if rejected and len(rejected) == len(feasible):
        if attempt < 2:
            return _result("REGENERATE_ONCE", [_issue("MEDIOCRE_CONCEPT_CIRCUIT_BREAKER", "all feasible concepts are closer to the rejected anchor")], owner_gate="NOT_REACHED", concepts=reviewed, attempt=attempt, next_attempt=2)
        return _result("FAIL", [_issue("VISUAL_DIRECTION_STUDIO_FAIL", "bounded regeneration also remained closer to the rejected anchor")], owner_gate="NOT_REACHED", concepts=reviewed, attempt=attempt)
    return _result("PASS", (), owner_gate="READY_FOR_OWNER_SELECTION", concepts=reviewed, attempt=attempt, next_attempt=None)


def _concept_pairwise_precheck(concept: Mapping[str, Any]) -> str:
    raw = concept.get("pairwise_precheck")
    if isinstance(raw, Mapping):
        raw = raw.get("verdict") or raw.get("choice") or raw.get("result")
    value = _normalize(raw)
    return {
        "A": "CLOSER_TO_APPROVED",
        "APPROVED": "CLOSER_TO_APPROVED",
        "CLOSER_TO_APPROVED": "CLOSER_TO_APPROVED",
        "B": "CLOSER_TO_REJECTED",
        "REJECTED": "CLOSER_TO_REJECTED",
        "CLOSER_TO_REJECTED": "CLOSER_TO_REJECTED",
        "AMBIGUOUS": "AMBIGUOUS",
    }.get(value, "UNASSESSED")


def evaluate_owner_visual_gate(
    contract: Mapping[str, Any],
    concepts: Sequence[Mapping[str, Any]],
    *,
    selected_direction: str | None = None,
    owner_confirmed: bool = False,
    selection_actor: str | None = None,
    approved_visual_target: Mapping[str, Any] | None = None,
    builder_selected_direction: str | None = None,
) -> dict[str, Any]:
    """Apply the existing visual-prototype hard stop without adding a lock."""

    route = route_visual_first("WEBSITE", contract)
    if route["status"] != "PASS":
        return _result(route["status"], route["issues"], visual_direction_lock="NOT_REACHED", production_build_allowed=False)
    if not route.get("owner_visual_gate_required"):
        return _result("PASS", (), gate_required=False, visual_direction_lock="NOT_REQUIRED", production_build_allowed=True)
    issues: list[dict[str, Any]] = []
    attempt = evaluate_visual_direction_attempt(contract, concepts, attempt=1)
    if attempt["status"] != "PASS":
        issues.extend(attempt["issues"])
    by_id = {str(item.get("concept_id")): item for item in concepts if isinstance(item, Mapping)}
    if not _present(approved_visual_target):
        issues.append(_issue("VISUAL_TARGET_REQUIRED_BEFORE_BUILD", "premium/showcase implementation needs an approved visual target"))
    if not selected_direction:
        issues.append(_issue("OWNER_MUST_SELECT_VISUAL_DIRECTION", "the owner must select a direction before production"))
    elif selected_direction not in by_id:
        issues.append(_issue("OWNER_SELECTION_UNKNOWN_DIRECTION", "owner selection does not identify a presented concept"))
    if builder_selected_direction and not selected_direction:
        issues.append(_issue("BUILDER_CANNOT_SELECT_DIRECTION", "builder preference cannot substitute for owner selection"))
    if selection_actor is not None and _normalize(selection_actor) not in {"OWNER", "CLIENT", "PROJECT_OWNER"}:
        issues.append(_issue("OWNER_SELECTION_ACTOR_INVALID", "selection actor must be the owner/client"))
    if owner_confirmed is not True:
        issues.append(_issue("OWNER_VISUAL_CONFIRMATION_REQUIRED", "owner_visual_direction_confirmed must be true"))
    if selected_direction in by_id:
        feasibility = validate_concept_feasibility(by_id[selected_direction])
        if feasibility["status"] != "PASS":
            issues.append(_issue("CONCEPT_FEASIBILITY_FAIL", "selected concept is not feasible"))
        if _concept_pairwise_precheck(by_id[selected_direction]) == "CLOSER_TO_REJECTED":
            issues.append(_issue("PAIRWISE_PRECHECK_REJECTED", "selected concept is closer to the rejected anchor"))
    status = "FAIL" if any(issue["code"] in {"BUILDER_CANNOT_SELECT_DIRECTION", "OWNER_SELECTION_ACTOR_INVALID", "PAIRWISE_PRECHECK_REJECTED", "CONCEPT_FEASIBILITY_FAIL"} for issue in issues) else ("BLOCKED" if issues else "PASS")
    return _result(status, issues, gate_required=True, visual_direction_lock="PASS" if not issues else "NOT_REACHED", production_build_allowed=not issues, selected_direction=selected_direction, owner_visual_direction_confirmed=owner_confirmed)


def compile_hot_path_context(
    cold_path: Mapping[str, Any],
    *,
    current_phase: str,
    project_state: Mapping[str, Any] | None = None,
    taste_contract: Mapping[str, Any] | None = None,
    approved_visual_target: Mapping[str, Any] | None = None,
    asset_manifest: Mapping[str, Any] | None = None,
    active_design_tokens: Mapping[str, Any] | None = None,
    responsive_motion_contract: Mapping[str, Any] | None = None,
    hard_constraints: Sequence[str] | Mapping[str, Any] | None = None,
    escalation_required: bool = False,
    token_measure: Callable[[str], int] | None = None,
) -> dict[str, Any]:
    """Compile only implementation-relevant context while preserving cold data."""

    source = dict(cold_path) if isinstance(cold_path, Mapping) else {}
    context: dict[str, Any] = {"current_phase": current_phase}
    values = {
        "current_project_state": project_state if project_state is not None else source.get("current_project_state"),
        "project_taste_contract": taste_contract if taste_contract is not None else source.get("project_taste_contract"),
        "approved_visual_target": approved_visual_target if approved_visual_target is not None else source.get("approved_visual_target"),
        "asset_manifest": asset_manifest if asset_manifest is not None else source.get("asset_manifest"),
        "active_design_tokens": active_design_tokens if active_design_tokens is not None else source.get("active_design_tokens"),
        "responsive_motion_contract": responsive_motion_contract if responsive_motion_contract is not None else source.get("responsive_motion_contract"),
        "hard_constraints": hard_constraints if hard_constraints is not None else source.get("hard_constraints"),
    }
    context.update({key: value for key, value in values.items() if value is not None})
    if escalation_required:
        context["escalation_context"] = {key: value for key, value in source.items() if key not in context}
    serialized = json.dumps(context, sort_keys=True, default=str)
    metrics: dict[str, Any] = {
        "character_count": len(serialized),
        "field_count": len(context),
        "token_count": token_measure(serialized) if token_measure is not None else None,
        "token_measurement": "SUPPLIED" if token_measure is not None else "NOT_AVAILABLE",
    }
    return {
        "status": "PASS",
        "context": context,
        "excluded_cold_path_fields": sorted(set(source) - set(context)),
        "escalation_required": escalation_required,
        "metrics": metrics,
    }


def evaluate_structural_design_risks(implementation: Mapping[str, Any], contract: Mapping[str, Any]) -> dict[str, Any]:
    """Emit bounded risks; do not convert ordinary aesthetic choices into bans."""

    if not isinstance(implementation, Mapping):
        return _result("BLOCKED", [_issue("IMPLEMENTATION_EVIDENCE_REQUIRED", "implementation evidence must be an object")])
    risks: list[dict[str, Any]] = []

    def risk(flag: str, location: str, evidence: Any, conflict: str, severity: str = "RISK") -> None:
        risks.append({"flag": flag, "location": location, "evidence": evidence, "project_contract_conflict": conflict, "severity": severity})

    radii = implementation.get("radius_values")
    if isinstance(radii, Sequence) and not isinstance(radii, (str, bytes)) and len(radii) >= 3 and len(set(radii)) == 1:
        risk("DEFAULT_RADIUS_UNIFORMITY", "surface_geometry", radii, "uniform radius is not explained by the contract")
    if _present(contract.get("typography_lane")) and _truthy(implementation.get("default_display_font_untracked")):
        risk("UNTRACKED_DEFAULT_DISPLAY_FONT", "typography", implementation.get("display_font"), "display typography is not tied to the project contract")
    if _truthy(implementation.get("generic_feature_triad")):
        risk("GENERIC_FEATURE_TRIAD", "features", implementation.get("feature_structure"), "repeated icon-title-description pattern is not motivated")
    if _truthy(contract.get("signature_requirement")) and not _truthy(implementation.get("signature_rendered_proof")):
        risk("SIGNATURE_ONLY_DECLARED", "signature", implementation.get("signature_rendered_proof"), "declared signature has no rendered proof", "BLOCKING_RISK")
    if _truthy(implementation.get("required_assets_absent")):
        risk("REQUIRED_ASSET_ABSENT", "assets", implementation.get("missing_assets"), "required asset is absent", "BLOCKING_RISK")
    if _truthy(implementation.get("visual_world_absent")):
        risk("VISUAL_WORLD_ABSENT", "visual_world", implementation.get("visual_world_evidence"), "visual-world strategy is not observable")
    if _truthy(implementation.get("visual_target_drift")):
        risk("VISUAL_TARGET_DRIFT", "approved_target", implementation.get("drift_evidence"), "render materially diverges from the approved visual target", "BLOCKING_RISK")
    blocking = any(item["severity"] == "BLOCKING_RISK" for item in risks)
    return _result("RISK" if risks and not blocking else ("FAIL" if blocking else "PASS"), (), risks=risks, risk_count=len(risks))


def evaluate_common_design_pattern(pattern: str, *, motivated: bool = False) -> dict[str, Any]:
    """A common pattern is a risk only when it is unmotivated, never automatic slop."""

    normalized = _normalize(pattern)
    if normalized not in _DEFAULT_PATTERN_NAMES:
        return _result("PASS", (), pattern=normalized, classification="PROJECT_SPECIFIC")
    if motivated:
        return _result("PASS", (), pattern=normalized, classification="MOTIVATED")
    return _result("RISK", [_issue("COMMON_PATTERN_UNMOTIVATED", "common design pattern needs project rationale")], pattern=normalized, classification="REVIEW_REQUIRED")


def validate_specialist_activation(name: str, request: Mapping[str, Any]) -> dict[str, Any]:
    """Keep GSAP/WebGL/Three.js and cinematic systems explicitly on-demand."""

    normalized = _normalize(name)
    if normalized not in {_normalize(item) for item in ON_DEMAND_SPECIALISTS}:
        return _result("FAIL", [_issue("SPECIALIST_UNKNOWN", f"unknown specialist capability: {name!r}")])
    if not isinstance(request, Mapping) or not _truthy(request.get("on_demand")) or not _present(request.get("justification")):
        return _result("BLOCKED", [_issue("SPECIALIST_ON_DEMAND_ONLY", f"{name} requires an explicit project justification")], specialist=normalized)
    return _result("PASS", (), specialist=normalized, activation="ON_DEMAND")


def validate_typography_dependency_boundary(record: Mapping[str, Any]) -> dict[str, Any]:
    """Use typography methodology without importing an external runtime graph."""

    if not isinstance(record, Mapping):
        return _result("BLOCKED", [_issue("TYPOGRAPHY_BOUNDARY_REQUIRED", "typography boundary record is required")])
    dependencies = record.get("runtime_dependencies", [])
    if not isinstance(dependencies, list):
        return _result("FAIL", [_issue("TYPOGRAPHY_DEPENDENCY_SHAPE", "runtime_dependencies must be a list")])
    dangling = [item for item in dependencies if isinstance(item, str) and "event4u" in item.casefold()]
    if dangling:
        return _result("FAIL", [_issue("TYPOGRAPHY_DANGLING_EXTERNAL_DEPENDENCY", "event4u methodology must not add a runtime dependency", dependencies=dangling)])
    return _result("PASS", (), methodology_source=record.get("methodology_source", "SOURCE_NEUTRAL"), resolution_order=list(TYPOGRAPHY_RESOLUTION_ORDER))


def evaluate_quality_authority(
    pairwise: Mapping[str, Any] | None,
    *,
    numeric_score: int | float | None = None,
    owner_decision: str | None = None,
) -> dict[str, Any]:
    """Make pairwise visual judgment authoritative over telemetry and owner acceptance."""

    telemetry = numeric_score
    if _normalize(owner_decision) in {"REJECT", "REJECTED", "FAIL"}:
        return _result("FAIL", [_issue("OWNER_REJECTED", "owner rejection cannot be overridden by a machine score")], authority="OWNER", numeric_telemetry=telemetry)
    if not isinstance(pairwise, Mapping):
        return _result("BLOCKED", [_issue("PAIRWISE_GATE_REQUIRED", "pairwise visual evidence is required")], authority="PAIRWISE", numeric_telemetry=telemetry)
    pairwise_status = _normalize(pairwise.get("status"))
    if pairwise_status == "FAIL":
        return _result("FAIL", [_issue("PAIRWISE_FAIL", "pairwise visual evidence failed")], authority="PAIRWISE", numeric_telemetry=telemetry)
    if pairwise_status in {"BLOCKED", "INVALID"}:
        return _result("BLOCKED", [_issue("PAIRWISE_BLOCKED", "pairwise visual evidence is incomplete or invalid")], authority="PAIRWISE", numeric_telemetry=telemetry)
    verdict = _normalize(pairwise.get("verdict") or pairwise.get("result"))
    if verdict in {"B", "CLOSER_TO_REJECTED", "FAIL"}:
        return _result("FAIL", [_issue("PAIRWISE_FAIL", "candidate is closer to the rejected anchor")], authority="PAIRWISE", numeric_telemetry=telemetry)
    if verdict in {"AMBIGUOUS", "BLOCKED", "UNASSESSED"}:
        return _result("BLOCKED", [_issue("PAIRWISE_AMBIGUOUS", "pairwise evidence does not establish a clear approved-anchor preference")], authority="PAIRWISE", numeric_telemetry=telemetry)
    if verdict in {"A", "CLOSER_TO_APPROVED", "PASS"}:
        return _result("PASS", (), authority="PAIRWISE", numeric_telemetry=telemetry)
    return _result("BLOCKED", [_issue("PAIRWISE_RESULT_INVALID", "pairwise result must be A, B, or AMBIGUOUS")], authority="PAIRWISE", numeric_telemetry=telemetry)


def validate_source_provenance(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Validate compact provenance records for adapted/concept-only methods."""

    if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
        return _result("BLOCKED", [_issue("SOURCE_PROVENANCE_REQUIRED", "source provenance must be a list")])
    issues: list[dict[str, Any]] = []
    required = ("source_repository", "source_commit", "source_path", "license", "import_mode", "local_capability")
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            issues.append(_issue("SOURCE_PROVENANCE_INVALID", f"source record {index} must be an object"))
            continue
        missing = [field for field in required if not _present(record.get(field))]
        if missing:
            issues.append(_issue("SOURCE_PROVENANCE_INCOMPLETE", f"source record {index} is incomplete", missing=missing))
        if _normalize(record.get("import_mode")) not in SOURCE_IMPORT_MODES:
            issues.append(_issue("SOURCE_IMPORT_MODE_INVALID", f"source record {index} has an invalid import mode"))
    return _result("FAIL" if issues else "PASS", issues, record_count=len(records))


__all__ = [
    "AMBITION_TIERS",
    "COMPOSITION_PRIMITIVES",
    "CONCEPT_FORMATS",
    "DESIGN_RISK_FLAGS",
    "MATERIAL_LANGUAGES",
    "ON_DEMAND_SPECIALISTS",
    "PAIRWISE_DIMENSIONS",
    "TASTE_CONTRACT_FIELDS",
    "choose_concept_formats",
    "choose_anchor_policy",
    "compile_hot_path_context",
    "evaluate_common_design_pattern",
    "evaluate_owner_visual_gate",
    "evaluate_quality_authority",
    "evaluate_structural_design_risks",
    "evaluate_visual_direction_attempt",
    "resolve_project_taste",
    "route_visual_first",
    "validate_concept_feasibility",
    "validate_project_taste_isolation",
    "validate_source_provenance",
    "validate_specialist_activation",
    "validate_taste_contract",
    "validate_typography_dependency_boundary",
]
