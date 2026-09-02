"""Pure contracts for cinematic production intelligence and visual evidence.

This module is deliberately small and provider-neutral.  It does not call a
model, browse a reference, launch a browser, or change Website Director state.
It gives the deterministic test suite one place to prove that owner-selected
references stay reference-only until rights and adaptation work are explicit,
and that a visual-quality claim is backed by real rendered receipts.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


REQUIRED_REGISTRY_SOURCES = {
    "21ST_DEV": ("https://21st.dev/", "COMPONENT_PATTERN_LIBRARY"),
    "GODLY": ("https://godly.design/", "CURATED_SITE_AND_SECTION_DISCOVERY"),
    "AWWWARDS": ("https://www.awwwards.com/", "WORLD_CLASS_DIMENSIONAL_REFERENCE_BAR"),
    "MOTIONSITES": ("https://motionsites.ai/", "MOTION_PATTERN_AND_BACKGROUND_LIBRARY"),
}

PRESERVED_REGISTRY_SOURCES = {
    "LANDBOOK",
    "DESIGN_INSPIRATION_MCP",
    "INDUSTRY_LANDSCAPE",
    "CROSS_INDUSTRY",
    "REFERENCE_RECON",
}

OWNER_INPUT_FIELDS = (
    "SOURCE",
    "REFERENCE_URL",
    "REFERENCE_TYPE",
    "ELEMENT_OR_SECTION",
    "WHAT_I_LIKE",
    "WHAT_I_DO_NOT_WANT",
    "WHY_IS_THIS_RELEVANT",
)

OWNER_INTERPRETATION_FIELDS = (
    "OWNER_SELECTED_REFERENCE",
    "SOURCE",
    "URL",
    "ASSIGNED_DIMENSION",
    "PATTERN_TO_LEARN",
    "OWNER_REQUESTED_ELEMENT",
    "WHY_IS_THIS_RELEVANT",
    "WHAT_NOT_TO_COPY",
    "REFERENCE_GRADE",
    "LICENSE_STATUS",
    "IMPLEMENTATION_RISK",
    "ACCESSIBILITY_RISK",
    "PRODUCTION_PLAUSIBILITY",
    "REFERENCE_ONLY_STATUS",
)

MODEL_ROLES = (
    "BUILDER_AGENT",
    "CRITIC_AGENT",
    "RESEARCH_AGENT",
    "ASSET_GENERATION_PROVIDER",
    "DEPLOYMENT_PROVIDER",
)

REQUIRED_RENDER_SURFACES = (
    "DESKTOP_FULL_PAGE",
    "DESKTOP_HERO",
    "DESKTOP_MID_PAGE",
    "DESKTOP_PRIMARY_CONVERSION",
    "MOBILE_FULL_PAGE",
    "MOBILE_HERO",
    "MOBILE_NAV_OPEN",
    "PRIMARY_INTERACTIVE_STATE",
    "REDUCED_MOTION_STATE",
)

_DEPENDENCY_MARKERS = re.compile(
    r"(?i)(?:claude_only|codex_only|lovable_only|higgsfield|hostinger|"
    r"lovable)"
)


def _get(record: Mapping[str, Any], name: str, default: Any = None) -> Any:
    """Read a canonical field while accepting the uppercase intake spelling."""

    candidates = (name, name.lower(), name.upper())
    for candidate in candidates:
        if candidate in record:
            return record[candidate]
    return default


def _nonempty(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _issue(code: str, detail: str) -> dict[str, str]:
    return {"code": code, "detail": detail}


def _append_issue(issues: list[dict[str, str]], code: str, detail: str) -> None:
    if code not in {item["code"] for item in issues}:
        issues.append(_issue(code, detail))


def required_surface_ids(config: Mapping[str, Any] | None = None) -> list[str]:
    """Return the configured render set, or the canonical production set."""

    config = config or {}
    raw = config.get("required_surfaces") or config.get("required_render_set")
    if isinstance(raw, Mapping):
        raw = raw.get("surfaces") or raw.get("items")
    if isinstance(raw, Sequence) and not isinstance(raw, (str, bytes)):
        result: list[str] = []
        for item in raw:
            value = item if isinstance(item, str) else _get(item, "surface_id")
            if value and str(value) not in result:
                result.append(str(value))
        if result:
            return result
    return list(REQUIRED_RENDER_SURFACES)


def validate_inspiration_registry(registry: Mapping[str, Any]) -> list[dict[str, str]]:
    """Validate the bounded source registry without making a live request."""

    issues: list[dict[str, str]] = []
    if _get(registry, "status") != "REFERENCE_ONLY":
        _append_issue(issues, "REFERENCE_ONLY_BOUNDARY_ENFORCED",
                      "the registry default status must be REFERENCE_ONLY")

    sources = registry.get("sources")
    if not isinstance(sources, list):
        return [_issue("INSPIRATION_REGISTRY_SHAPE", "sources must be an array")]
    by_id = {
        str(_get(item, "source_id")): item
        for item in sources
        if isinstance(item, Mapping) and _nonempty(_get(item, "source_id"))
    }

    for source_id, (url, role) in REQUIRED_REGISTRY_SOURCES.items():
        item = by_id.get(source_id)
        if not isinstance(item, Mapping):
            _append_issue(issues, f"{source_id}_REGISTRY_PRESENT",
                          f"missing required source {source_id}")
            continue
        if _get(item, "url") != url or _get(item, "role") != role:
            _append_issue(issues, f"{source_id}_REGISTRY_PRESENT",
                          f"{source_id} must preserve its canonical URL and role")
        if _get(item, "reference_only_default") is not True:
            _append_issue(issues, "REFERENCE_ONLY_BOUNDARY_ENFORCED",
                          f"{source_id} must default to reference-only")

    for source_id in PRESERVED_REGISTRY_SOURCES:
        if source_id not in by_id:
            _append_issue(issues, "EXISTING_RESEARCH_SOURCE_PRESERVED",
                          f"existing research source {source_id} was not preserved")

    awwards = by_id.get("AWWWARDS", {})
    if (_get(awwards, "authority_ref") != "AWWWARDS-SHOWCASE-INTELLIGENCE.md"
            or _get(awwards, "duplicate_authority") is not False):
        _append_issue(issues, "AWWWARDS_EXISTING_AUTHORITY_NOT_DUPLICATED",
                      "Awwwards must point to its existing authority and declare no duplicate")

    twenty_first = by_id.get("21ST_DEV", {})
    reuse = _get(twenty_first, "source_reuse_requires", [])
    required_reuse = {
        "VERIFY_LICENSE",
        "RECORD_PROVENANCE",
        "ADAPT_TO_PROJECT_STACK",
        "ADAPT_TO_DESIGN_SYSTEM",
    }
    if not required_reuse.issubset(set(reuse if isinstance(reuse, list) else [])):
        _append_issue(issues, "LICENSE_CHECK_REQUIRED_FOR_SOURCE_REUSE",
                      "21ST_DEV reuse must require license, provenance, stack, and design-system checks")

    motionsites = by_id.get("MOTIONSITES", {})
    if (_get(motionsites, "premium_material_default") != "REFERENCE_ONLY"
            or _get(motionsites, "proprietary_prompt_policy") != "DO_NOT_COPY"):
        _append_issue(issues, "REFERENCE_ONLY_BOUNDARY_ENFORCED",
                      "premium MotionSites material must remain reference-only and must not be copied")

    contract = registry.get("owner_selection_contract")
    if not isinstance(contract, Mapping):
        _append_issue(issues, "OWNER_REFERENCE_SELECTION_SUPPORTED",
                      "registry must publish an owner-selection contract")
    else:
        required_input = set(_get(contract, "required_input_fields", []))
        if not set(OWNER_INPUT_FIELDS).issubset(required_input):
            _append_issue(issues, "OWNER_REFERENCE_SELECTION_SUPPORTED",
                          "owner intake fields are incomplete")
        required_output = set(_get(contract, "required_interpretation_fields", []))
        if not set(OWNER_INTERPRETATION_FIELDS).issubset(required_output):
            _append_issue(issues, "OWNER_REFERENCE_SELECTION_SUPPORTED",
                          "owner interpretation fields are incomplete")
    return issues


def validate_owner_selected_reference(
    reference: Mapping[str, Any], registry: Mapping[str, Any]
) -> list[dict[str, str]]:
    """Validate one owner request and its Website Director interpretation."""

    issues: list[dict[str, str]] = []
    for field in OWNER_INTERPRETATION_FIELDS:
        if _get(reference, field) is None:
            _append_issue(issues, "OWNER_REFERENCE_SELECTION_SUPPORTED",
                          f"owner reference is missing {field}")
    if _get(reference, "OWNER_SELECTED_REFERENCE") is not True:
        _append_issue(issues, "OWNER_REFERENCE_SELECTION_SUPPORTED",
                      "the interpreted record must be marked owner-selected")

    source_id = _get(reference, "SOURCE")
    source_ids = {
        str(_get(item, "source_id"))
        for item in registry.get("sources", [])
        if isinstance(item, Mapping)
    }
    if source_id not in source_ids:
        _append_issue(issues, "OWNER_REFERENCE_SELECTION_SUPPORTED",
                      "owner reference SOURCE must resolve in the registry")

    reference_url = _get(reference, "URL", _get(reference, "REFERENCE_URL"))
    if not _nonempty(reference_url):
        _append_issue(issues, "OWNER_REFERENCE_SELECTION_SUPPORTED",
                      "owner reference URL is required")
    relevance = _get(reference, "WHY_IS_THIS_RELEVANT")
    if not _nonempty(relevance):
        _append_issue(issues, "OWNER_REFERENCE_SELECTION_SUPPORTED",
                      "WHY_IS_THIS_RELEVANT is required")
    elif str(relevance).strip().lower() in {"it looks cool", "looks cool", "cool"}:
        _append_issue(issues, "OWNER_REFERENCE_SELECTION_SUPPORTED",
                      "visual appeal alone is not a relevance rationale")

    if _get(reference, "REFERENCE_ONLY_STATUS") is not True:
        mode = str(_get(reference, "IMPLEMENTATION_MODE", "STUDY_ONLY")).upper()
        if mode != "SOURCE_REUSE":
            _append_issue(issues, "REFERENCE_ONLY_BOUNDARY_ENFORCED",
                          "a study-only reference must remain REFERENCE_ONLY")

    if str(_get(reference, "IMPLEMENTATION_MODE", "STUDY_ONLY")).upper() == "SOURCE_REUSE":
        if _get(reference, "LICENSE_CHECK_REQUIRED") is not True:
            _append_issue(issues, "LICENSE_CHECK_REQUIRED_FOR_SOURCE_REUSE",
                          "source reuse requires an explicit license check")
        if str(_get(reference, "LICENSE_STATUS", "")).upper() != "VERIFIED":
            _append_issue(issues, "LICENSE_CHECK_REQUIRED_FOR_SOURCE_REUSE",
                          "source reuse requires VERIFIED license status")
        for field in ("PROVENANCE_REF", "STACK_ADAPTATION", "DESIGN_SYSTEM_ADAPTATION"):
            if not _nonempty(_get(reference, field)):
                _append_issue(issues, "LICENSE_CHECK_REQUIRED_FOR_SOURCE_REUSE",
                              f"source reuse requires {field}")
    return issues


def validate_model_agnostic_routing(text: str) -> list[dict[str, str]]:
    """Check that role routing is explicit without binding a model or vendor."""

    issues: list[dict[str, str]] = []
    for role in MODEL_ROLES:
        if role not in text:
            _append_issue(issues, "MODEL_AGNOSTIC_ROUTING",
                          f"missing model-agnostic role {role}")
    if _DEPENDENCY_MARKERS.search(text):
        _append_issue(issues, "MODEL_AGNOSTIC_ROUTING",
                      "production intelligence contains a fixed model or vendor dependency")
    return issues


def validate_provider_neutral_documents(paths: Iterable[str | Path]) -> list[dict[str, str]]:
    """Scan the newly reconciled documents for fixed-provider requirements."""

    issues: list[dict[str, str]] = []
    for raw_path in paths:
        path = Path(raw_path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            _append_issue(issues, "MODEL_AGNOSTIC_ROUTING", f"cannot read {path}: {exc}")
            continue
        if _DEPENDENCY_MARKERS.search(text):
            _append_issue(issues, "MODEL_AGNOSTIC_ROUTING",
                          f"fixed provider dependency found in {path.name}")
    return issues


def _screenshot_items(evidence: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    raw = evidence.get("screenshot_set", evidence.get("screenshots", []))
    if isinstance(raw, Mapping):
        raw = raw.get("screenshots", raw.get("items", []))
    return [item for item in raw if isinstance(item, Mapping)] if isinstance(raw, list) else []


def _actual_screenshot(item: Mapping[str, Any]) -> bool:
    digest = str(item.get("screenshot_sha256", ""))
    return (
        item.get("actual_rendered") is True
        and str(item.get("engine_identity", "")).upper() == "REAL_BROWSER"
        and _nonempty(item.get("screenshot_path"))
        and bool(re.fullmatch(r"[0-9a-fA-F]{64}", digest))
    )


def validate_rendered_visual_evidence(
    evidence: Mapping[str, Any],
    required_surfaces: Sequence[str] | None = None,
    *,
    require_critic: bool = False,
) -> dict[str, Any]:
    """Validate screenshot receipts and, optionally, the Gauntlet critic loop.

    The function never trusts a claimed PASS.  It derives PASS from the
    receipts, which is what lets negative controls reject source-only or stale
    visual reviews.
    """

    required = list(required_surfaces or required_surface_ids(evidence))
    screenshots = _screenshot_items(evidence)
    issues: list[dict[str, str]] = []
    actual = [item for item in screenshots if _actual_screenshot(item)]
    if not actual:
        _append_issue(issues, "SOURCE_ONLY_VISUAL_PASS_REJECTED",
                      "a visual pass requires real-browser screenshot receipts")

    latest: dict[str, Mapping[str, Any]] = {}
    for item in screenshots:
        surface_id = item.get("surface_id")
        if not surface_id:
            continue
        previous = latest.get(str(surface_id))
        if previous is None or _int_or_zero(item.get("attempt", 0)) >= _int_or_zero(previous.get("attempt", 0)):
            latest[str(surface_id)] = item
    missing = [surface_id for surface_id in required if surface_id not in latest]
    invalid = [surface_id for surface_id in required
               if surface_id in latest and not _actual_screenshot(latest[surface_id])]
    if missing or invalid:
        detail = []
        if missing:
            detail.append("missing=" + ",".join(missing))
        if invalid:
            detail.append("not-real-browser=" + ",".join(invalid))
        _append_issue(issues, "MISSING_SCREENSHOT_SET_REJECTED", "; ".join(detail))

    if require_critic:
        critic = evidence.get("critic", evidence.get("critic_input", {}))
        if not isinstance(critic, Mapping):
            critic = {}
        inspected = set(critic.get("inspected_inputs", []))
        required_inputs = (
            "actual_screenshots",
            "actual_rendered_dom",
            "actual_css",
            "approved_design_direction",
            "approved_design_system",
            "owner_intent",
            "assigned_reference_bars",
        )
        missing_inputs = [key for key in required_inputs
                          if critic.get(key) is not True and key not in inspected]
        critic_context = critic.get("fresh_context_id", critic.get("context_id"))
        builder_context = critic.get("builder_context_id", evidence.get("builder_context_id"))
        if (missing_inputs or not _nonempty(critic_context)
                or (builder_context and critic_context == builder_context)
                or critic.get("fresh_context") is False):
            detail = "fresh critic required"
            if missing_inputs:
                detail += "; missing inputs=" + ",".join(missing_inputs)
            _append_issue(issues, "FRESH_CRITIC_REQUIRED", detail)
        if not _nonempty(critic.get("actual_dom_ref")) or not _nonempty(critic.get("actual_css_ref")):
            _append_issue(issues, "FRESH_CRITIC_REQUIRED",
                          "fresh critic receipt must point to actual rendered DOM and CSS")

        repairs = evidence.get("repairs", [])
        if isinstance(repairs, list) and repairs:
            repair_revisions = []
            for item in repairs:
                if not isinstance(item, Mapping):
                    _append_issue(issues, "REPAIR_RECEIPT_INVALID",
                                  "every repair receipt must be an object with a revision")
                    continue
                repair_revisions.append(_int_or_zero(item.get("revision", 0)))
            latest_repair = max(repair_revisions, default=0)
            screenshot_revision = _int_or_zero(
                evidence.get("screenshot_set_revision",
                             evidence.get("screenshots_revision", 0)))
            if evidence.get("recapture_after_repair") is not True or screenshot_revision <= latest_repair:
                _append_issue(issues, "RECAPTURE_AFTER_REPAIR_REQUIRED",
                              "a repair requires a newer screenshot set and fresh re-evaluation")
            pre_sha = evidence.get("pre_repair_build_sha")
            current_sha = evidence.get("current_build_sha")
            if pre_sha and current_sha and pre_sha == current_sha:
                _append_issue(issues, "STALE_SCREENSHOT_AFTER_REPAIR_REJECTED",
                              "the post-repair review still identifies the pre-repair build")

    return {
        "status": "PASS" if not issues else "BLOCKED",
        "required_surfaces": required,
        "captured_surfaces": sorted({str(item.get("surface_id")) for item in actual
                                      if item.get("surface_id")}),
        "issues": issues,
    }


def build_rendered_visual_evidence(
    config: Mapping[str, Any], observations: Iterable[Mapping[str, Any]],
    *, run_id: str, git_sha: str
) -> dict[str, Any]:
    """Build a manifest receipt from runner observations and derive its status."""

    required = required_surface_ids(config)
    ordered: dict[str, Mapping[str, Any]] = {}
    for observation in observations:
        surface_id = observation.get("surface_id")
        if not surface_id:
            continue
        previous = ordered.get(str(surface_id))
        if previous is None or _int_or_zero(observation.get("attempt", 0)) >= _int_or_zero(previous.get("attempt", 0)):
            ordered[str(surface_id)] = observation
    screenshots = [dict(ordered[surface_id]) for surface_id in required if surface_id in ordered]
    receipt = {
        "required": True,
        "required_surfaces": required,
        "browser_run_id": run_id,
        "build_sha": git_sha,
        "screenshot_set_revision": 0,
        "screenshot_set": screenshots,
    }
    result = validate_rendered_visual_evidence(receipt, required)
    receipt.update({"status": result["status"], "captured_surfaces": result["captured_surfaces"],
                    "issues": result["issues"]})
    return receipt
