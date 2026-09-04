"""Deterministic contracts for Website Director's design-first flow.

This module is intentionally bounded.  It extends the existing Visual
Prototype and Design System authorities with business-understanding,
full-homepage review, and derivation checks.  It does not create a phase,
readiness gate, owner lock, provider dependency, browser runner, or project
state writer.
"""

from __future__ import annotations

import re
from typing import Any, Iterable, Mapping, Sequence

try:
    from .cinematic_inspiration import validate_owner_selected_reference
    from .validator import CANONICAL_LOCKS
except ImportError:  # pragma: no cover - supports direct legacy module loading
    from cinematic_inspiration import validate_owner_selected_reference
    from validator import CANONICAL_LOCKS


DISCOVERY_MODES = (
    "QUESTIONNAIRE_ONLY",
    "QUESTIONNAIRE_PLUS_TRANSCRIPT",
    "TRANSCRIPT_LED_DISCOVERY",
    "OWNER_SUPPLIED_DISCOVERY_NOTES",
)

CREATIVE_AMBITIONS = ("STANDARD", "PREMIUM", "SHOWCASE", "EXPERIMENTAL")

OPERATING_FLOW = (
    "UNDERSTAND_BUSINESS",
    "DESIGN_BEFORE_IMPLEMENTATION",
    "OWNER_SEES_RENDERED_HOMEPAGE",
    "APPROVE_VISUAL_DIRECTION",
    "DERIVE_DESIGN_SYSTEM",
    "IMPLEMENT_REST",
    "BROWSER_QA",
    "VISUAL_GAUNTLET",
)

OPERATING_INVARIANTS = (
    "UNDERSTANDING_PRECEDES_DESIGN",
    "DESIGN_PRECEDES_IMPLEMENTATION",
    "OWNER_SEES_RENDERED_DESIGN_BEFORE_FULL_BUILD",
    "APPROVED_HOMEPAGE_DEFINES_THE_SITE_SYSTEM",
)

BUSINESS_UNDERSTANDING_FIELDS = (
    "BUSINESS",
    "TARGET_CUSTOMER",
    "PRIMARY_CUSTOMER_PROBLEM",
    "SERVICES",
    "NOT_OFFERED",
    "DIFFERENTIATOR",
    "OWNER_ORIGIN_STORY",
    "CLIENT_VOICE",
    "BRAND_PERSONALITY",
    "PRIMARY_CONVERSION",
    "SECONDARY_CONVERSIONS",
    "PRIMARY_OBJECTIONS",
    "TRUST_REQUIREMENTS",
    "PROOF_AVAILABLE",
    "DESIGN_PREFERENCES",
    "ANTI_PREFERENCES",
    "OWNER_SELECTED_REFERENCE_URLS",
    "OWNER_REFERENCE_DESCRIPTIONS",
    "OWNER_ASSETS",
    "REQUIRED_ASSETS",
    "REFERENCE_ONLY_ASSETS",
    "BRAND_GUIDELINES",
    "OWNER_NON_NEGOTIABLES",
    "UNKNOWN_OR_UNVERIFIED_FACTS",
)

FULL_HOMEPAGE_SECTIONS = (
    "GLOBAL_NAVIGATION",
    "HERO",
    "VALUE_PROPOSITION",
    "SERVICES_OR_OFFERS",
    "PROOF_AND_TRUST",
    "DIFFERENTIATION",
    "PROCESS_OR_HOW_IT_WORKS",
    "IMAGE_AND_MEDIA_LANGUAGE",
    "AUTHENTIC_TESTIMONIAL_TREATMENT",
    "OBJECTIONS",
    "CTA_PROGRESSION",
    "FAQ",
    "FINAL_CTA",
    "FOOTER",
    "RESPONSIVE_MOBILE",
)

DESIGN_SIGNALS = (
    "TYPOGRAPHY",
    "SPACING",
    "GRID",
    "IMAGERY",
    "COLOR",
    "GEOMETRY",
    "MOTION",
    "RHYTHM",
    "CONVERSION_HIERARCHY",
)

DESIGN_SYSTEM_DERIVATION_FIELDS = (
    "TYPOGRAPHY",
    "COLORS",
    "SPACING",
    "GRID_CONTAINER",
    "BUTTONS_FORMS",
    "CARDS_SURFACES",
    "BORDERS_RADIUS_SHADOWS",
    "IMAGE_LANGUAGE_CROPS",
    "ICONS",
    "NAVIGATION",
    "SECTION_TRANSITIONS",
    "MOTION_PHYSICS",
    "CTA_SYSTEM",
    "RESPONSIVE_BEHAVIOR",
    "ACCESSIBILITY",
)

HOMEPAGE_REVIEW_SURFACES = (
    "DESKTOP_FULL_HOMEPAGE",
    "MOBILE_FULL_HOMEPAGE",
)

UNKNOWN_VALUES = frozenset({"UNKNOWN", "NOT_PROVIDED", "UNVERIFIED"})
LOWER_HALF_FAILURES = frozenset(
    {
        "GENERIC",
        "GENERIC_FILLER",
        "FILLER",
        "PLACEHOLDER",
        "TEMPLATE",
        "HERO_ONLY",
        "UNASSESSED",
    }
)

_FABRICATION_MARKERS = re.compile(
    r"(?i)(?:lorem\s+ipsum|fake\s+(?:testimonial|stat|award|credential|case|proof)|"
    r"fictional|made[- ]?up|invented\s+(?:metric|claim|testimonial|award)|"
    r"placeholder\s+(?:copy|text|claim)|dummy\s+(?:copy|text)|"
    r"guaranteed\s+results|10x\s+(?:growth|revenue|roi))"
)

_SAFE_BUSINESS_FIELDS = {
    "ANTI_PREFERENCES",
    "NOT_OFFERED",
    "OWNER_NON_NEGOTIABLES",
    "UNKNOWN_OR_UNVERIFIED_FACTS",
}


def _normalise_name(value: Any) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", str(value).upper()).strip("_")


def _get(record: Mapping[str, Any], name: str, default: Any = None) -> Any:
    target = _normalise_name(name)
    for key, value in record.items():
        if _normalise_name(key) == target:
            return value
    return default


def _is_unknown(value: Any) -> bool:
    return isinstance(value, str) and _normalise_name(value) in UNKNOWN_VALUES


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if _is_unknown(value):
        return False
    if isinstance(value, str):
        stripped = value.strip()
        return not stripped or stripped.startswith("[") and stripped.endswith("]")
    if isinstance(value, (list, tuple, set, Mapping)):
        return len(value) == 0
    return False


def _truthy(value: Any) -> bool:
    return value is True or (isinstance(value, str) and value.strip().upper() in {"TRUE", "YES", "PASS", "VERIFIED"})


def _issue(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def _result(status: str, issues: Iterable[Mapping[str, str]] = (), **data: Any) -> dict[str, Any]:
    issue_list = [dict(item) for item in issues]
    result: dict[str, Any] = {
        "status": status,
        "ok": status == "PASS",
        "issues": issue_list,
    }
    result.update(data)
    return result


def _walk_strings(value: Any, path: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            yield from _walk_strings(child, child_path)
    elif isinstance(value, (list, tuple, set)):
        for index, child in enumerate(value):
            yield from _walk_strings(child, f"{path}[{index}]")


def _surface_ids(value: Any) -> set[str]:
    if isinstance(value, Mapping):
        value = value.get("surfaces") or value.get("items") or value.get("screenshot_receipts")
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return set()
    result: set[str] = set()
    for item in value:
        if isinstance(item, str):
            result.add(_normalise_name(item))
        elif isinstance(item, Mapping):
            surface_id = _get(item, "SURFACE_ID")
            if surface_id:
                result.add(_normalise_name(surface_id))
    return result


def _section_ids(value: Any) -> set[str]:
    if isinstance(value, Mapping):
        return {_normalise_name(key) for key in value}
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return set()
    result: set[str] = set()
    for item in value:
        if isinstance(item, str):
            result.add(_normalise_name(item))
        elif isinstance(item, Mapping):
            identifier = _get(item, "ID", _get(item, "SECTION"))
            if identifier:
                result.add(_normalise_name(identifier))
    return result


def validate_operating_flow(sequence: Sequence[str]) -> dict[str, Any]:
    """Require the bounded sequence without introducing a new lifecycle phase."""

    observed = tuple(_normalise_name(item) for item in sequence) if isinstance(sequence, Sequence) else ()
    if observed == OPERATING_FLOW:
        return _result("PASS", flow=list(OPERATING_FLOW), invariants=list(OPERATING_INVARIANTS))
    return _result(
        "FAIL",
        [_issue("DESIGN_FIRST_SEQUENCE_INVALID", "the design-first flow must preserve the canonical bounded order")],
        expected=list(OPERATING_FLOW),
        observed=list(observed),
    )


def validate_discovery_mode(mode: str, transcript: Any = None) -> dict[str, Any]:
    """Validate optional discovery modes and keep transcript use explicit."""

    normalised = _normalise_name(mode)
    issues: list[dict[str, str]] = []
    if normalised not in DISCOVERY_MODES:
        issues.append(_issue("DISCOVERY_MODE_INVALID", f"unsupported discovery mode {mode!r}"))
        return _result("FAIL", issues, mode=normalised)
    transcript_present = not _is_missing(transcript)
    transcript_required = normalised in {"QUESTIONNAIRE_PLUS_TRANSCRIPT", "TRANSCRIPT_LED_DISCOVERY"}
    if transcript_required and not transcript_present:
        issues.append(_issue("TRANSCRIPT_REQUIRED_FOR_SELECTED_MODE", f"{normalised} explicitly requires a transcript"))
    status = "BLOCKED" if issues else "PASS"
    return _result(
        status,
        issues,
        mode=normalised,
        transcript_present=transcript_present,
        transcript_required=transcript_required,
    )


def validate_business_understanding(artifact: Mapping[str, Any]) -> dict[str, Any]:
    """Check semantic business fields and fail closed on invented claims."""

    if not isinstance(artifact, Mapping):
        return _result("BLOCKED", [_issue("BUSINESS_UNDERSTANDING_INCOMPLETE", "the Business Understanding Pack must be an object")])

    issues: list[dict[str, str]] = []
    missing: list[str] = []
    for field in BUSINESS_UNDERSTANDING_FIELDS:
        value = _get(artifact, field)
        if value is None or _is_missing(value):
            missing.append(field)
    if missing:
        issues.append(_issue("BUSINESS_UNDERSTANDING_INCOMPLETE", f"missing or empty semantic fields: {', '.join(missing)}"))

    for path, text in _walk_strings(artifact):
        field = _normalise_name(path.split(".", 1)[0].split("[", 1)[0])
        if field in _SAFE_BUSINESS_FIELDS:
            continue
        if _FABRICATION_MARKERS.search(text):
            issues.append(_issue("FABRICATED_BUSINESS_FACT", f"unverified or fabricated claim marker found at {path}"))
            break

    status = "FAIL" if any(item["code"] == "FABRICATED_BUSINESS_FACT" for item in issues) else ("BLOCKED" if issues else "PASS")
    return _result(
        status,
        issues,
        required_fields=list(BUSINESS_UNDERSTANDING_FIELDS),
        missing_fields=missing,
        unknown_fields=[field for field in BUSINESS_UNDERSTANDING_FIELDS if _is_unknown(_get(artifact, field))],
    )


def extract_client_voice(discovery: Mapping[str, Any]) -> dict[str, Any]:
    """Extract only language present in optional transcript or notes.

    This is intentionally a conservative, deterministic extraction.  It never
    creates a brand voice from defaults when no owner language was supplied.
    """

    if not isinstance(discovery, Mapping):
        return _result("NOT_PROVIDED", client_voice={
            "verbatim_or_near_verbatim": [],
            "common_terms": [],
            "brand_register": [],
            "important_stories": [],
            "service_explanations": [],
            "owner_priorities": [],
        })

    structured = _get(discovery, "CLIENT_VOICE")
    if isinstance(structured, Mapping) and any(not _is_missing(value) for value in structured.values()):
        return _result("PASS", client_voice=dict(structured), source="OWNER_SUPPLIED_CLIENT_VOICE")

    raw = _get(discovery, "TRANSCRIPT", _get(discovery, "DISCOVERY_NOTES", _get(discovery, "NOTES")))
    if _is_missing(raw):
        return _result(
            "NOT_PROVIDED",
            client_voice={
                "verbatim_or_near_verbatim": [],
                "common_terms": [],
                "brand_register": [],
                "important_stories": [],
                "service_explanations": [],
                "owner_priorities": [],
            },
            source="NONE",
        )

    text = str(raw).strip()
    segments = [part.strip() for part in re.split(r"(?:\r?\n+|(?<=[.!?])\s+)", text) if part.strip()]
    words = re.findall(r"[A-Za-z][A-Za-z'-]{3,}", text.lower())
    stopwords = {
        "that", "this", "with", "from", "have", "will", "want", "what", "when", "where", "they", "their", "about", "should", "would", "there", "really", "just", "into", "more", "than", "then", "been", "very",
    }
    common_terms: list[str] = []
    for word in words:
        if word in stopwords or word in common_terms:
            continue
        common_terms.append(word)
        if len(common_terms) == 12:
            break

    register_cues = ("precise", "warm", "direct", "technical", "human", "quiet", "bold", "playful", "serious", "plain", "confident", "calm")
    brand_register = [cue for cue in register_cues if re.search(rf"\b{re.escape(cue)}\b", text.lower())]
    stories = [segment for segment in segments if re.search(r"(?i)\b(founded|started|origin|story|because|grew up|learned)\b", segment)]
    services = [segment for segment in segments if re.search(r"(?i)\b(we help|we offer|we provide|our service|we build|we make|we do)\b", segment)]
    priorities = [segment for segment in segments if re.search(r"(?i)\b(must|priority|important|non-negotiable|need to|do not want|don't want)\b", segment)]
    return _result(
        "PASS",
        client_voice={
            "verbatim_or_near_verbatim": segments,
            "common_terms": common_terms,
            "brand_register": brand_register,
            "important_stories": stories,
            "service_explanations": services,
            "owner_priorities": priorities,
        },
        source="TRANSCRIPT_OR_DISCOVERY_NOTES",
    )


def validate_client_voice_fidelity(record: Mapping[str, Any]) -> dict[str, Any]:
    """Require an explicit answer to the client-voice fidelity question."""

    if not isinstance(record, Mapping):
        return _result("BLOCKED", [_issue("CLIENT_VOICE_FIDELITY_UNASSESSED", "client-voice fidelity has not been assessed")])
    answer = _normalise_name(_get(record, "CLIENT_VOICE_FIDELITY", ""))
    evidence = _get(record, "CLIENT_VOICE_FIDELITY_EVIDENCE")
    if answer in {"FAIL", "NO"}:
        return _result("FAIL", [_issue("CLIENT_VOICE_FIDELITY_FAIL", "copy does not sound like the client or uses unsupported language")])
    if answer not in {"PASS", "VERIFIED", "YES"} or _is_missing(evidence):
        return _result(
            "BLOCKED",
            [_issue("CLIENT_VOICE_FIDELITY_UNASSESSED", "record whether the copy sounds like this client and cite the owner language used")],
        )
    return _result("PASS", client_voice_fidelity=answer, evidence=evidence)


def validate_ambition_policy(ambition: str, artifact: Mapping[str, Any]) -> dict[str, Any]:
    """Apply the bounded full-homepage policy by creative ambition."""

    normalised = _normalise_name(ambition)
    if normalised not in CREATIVE_AMBITIONS:
        return _result("FAIL", [_issue("CREATIVE_AMBITION_INVALID", f"unsupported creative ambition {ambition!r}")], ambition=normalised)
    artifact = artifact if isinstance(artifact, Mapping) else {}
    full_homepage = _truthy(_get(artifact, "FULL_HOMEPAGE_VISUAL_DESIGN"))
    artifact_kind = _normalise_name(_get(artifact, "ARTIFACT_KIND", ""))
    bounded_exception = _truthy(_get(artifact, "BOUNDED_ARTIFACT_EXCEPTION"))
    exception_reason = _get(artifact, "EXCEPTION_REASON")
    accepted_standard_kind = artifact_kind in {"FULL_HOMEPAGE", "SELECTED_DIRECTION_PLUS_COMPLETE_HOMEPAGE"}
    issues: list[dict[str, str]] = []

    if normalised in {"PREMIUM", "SHOWCASE"} and not (full_homepage and accepted_standard_kind):
        issues.append(_issue("FULL_HOMEPAGE_VISUAL_DESIGN_REQUIRED", f"{normalised} requires a complete rendered homepage design before production"))
    elif normalised == "EXPERIMENTAL" and not (full_homepage and accepted_standard_kind):
        if not (bounded_exception and not _is_missing(exception_reason)):
            issues.append(_issue("FULL_HOMEPAGE_VISUAL_DESIGN_REQUIRED", "EXPERIMENTAL requires a full homepage unless a bounded artifact exception is documented"))
    elif normalised == "STANDARD" and not (full_homepage or accepted_standard_kind):
        issues.append(_issue("STANDARD_HOMEPAGE_PATH_REQUIRED", "STANDARD requires a full homepage or a selected direction followed by a complete homepage"))

    status = "BLOCKED" if issues else "PASS"
    return _result(
        status,
        issues,
        ambition=normalised,
        full_homepage_visual_design=full_homepage,
        artifact_kind=artifact_kind,
        bounded_artifact_exception=bounded_exception,
    )


def validate_homepage_design(ambition: str, homepage: Mapping[str, Any]) -> dict[str, Any]:
    """Require a rendered, content-complete homepage with a specific lower half."""

    if not isinstance(homepage, Mapping):
        return _result("BLOCKED", [_issue("FULL_HOMEPAGE_REVIEW_INCOMPLETE", "homepage design evidence must be an object")])
    issues: list[dict[str, str]] = []
    policy = validate_ambition_policy(ambition, homepage)
    issues.extend(policy["issues"])

    sections = _section_ids(_get(homepage, "SECTIONS", {}))
    missing_sections = [section for section in FULL_HOMEPAGE_SECTIONS if _normalise_name(section) not in sections]
    if _truthy(_get(homepage, "TESTIMONIALS_NOT_APPLICABLE")):
        missing_sections = [section for section in missing_sections if section != "AUTHENTIC_TESTIMONIAL_TREATMENT"]
    if missing_sections:
        issues.append(_issue("FULL_HOMEPAGE_SECTIONS_INCOMPLETE", f"homepage is missing: {', '.join(missing_sections)}"))

    missing_signals = [field for field in DESIGN_SIGNALS if _is_missing(_get(homepage, field))]
    if missing_signals:
        issues.append(_issue("FULL_HOMEPAGE_VISUAL_SIGNALS_INCOMPLETE", f"homepage is missing visual signals: {', '.join(missing_signals)}"))

    surfaces = _surface_ids(_get(homepage, "RENDERED_SURFACES", _get(homepage, "SCREENSHOT_RECEIPTS")))
    missing_surfaces = [surface for surface in HOMEPAGE_REVIEW_SURFACES if _normalise_name(surface) not in surfaces]
    if missing_surfaces:
        issues.append(_issue("FULL_HOMEPAGE_RENDER_REQUIRED", f"real rendered evidence is missing: {', '.join(missing_surfaces)}"))
    if _truthy(_get(homepage, "PROSE_ONLY")):
        issues.append(_issue("PROSE_ONLY_DIRECTION_REJECTED", "a prose-only homepage cannot establish visual direction"))

    lower_half = _normalise_name(_get(homepage, "LOWER_HALF_QUALITY", ""))
    if lower_half in LOWER_HALF_FAILURES:
        issues.append(_issue("HOMEPAGE_LOWER_HALF_QUALITY", "the homepage lower half is generic, filler, placeholder, or hero-only"))
    elif not lower_half:
        issues.append(_issue("HOMEPAGE_LOWER_HALF_QUALITY", "record a specific lower-half quality verdict before review"))
    if _truthy(_get(homepage, "GENERIC_LOWER_SECTIONS")):
        issues.append(_issue("HOMEPAGE_LOWER_HALF_QUALITY", "generic lower sections are not allowed below an elite hero"))

    voice = validate_client_voice_fidelity(homepage)
    issues.extend(voice["issues"])

    for path, text in _walk_strings(homepage):
        if _FABRICATION_MARKERS.search(text) and "WHAT_NOT_TO_COPY" not in _normalise_name(path):
            issues.append(_issue("FABRICATED_OR_PLACEHOLDER_HOMEPAGE_COPY", f"unsupported copy marker found at {path}"))
            break

    codes = {item["code"] for item in issues}
    status = "FAIL" if any(code.startswith("FABRICATED") or code in {"PROSE_ONLY_DIRECTION_REJECTED", "HOMEPAGE_LOWER_HALF_QUALITY", "CLIENT_VOICE_FIDELITY_FAIL"} for code in codes) else ("BLOCKED" if issues else "PASS")
    return _result(
        status,
        issues,
        ambition=_normalise_name(ambition),
        missing_sections=missing_sections,
        missing_signals=missing_signals,
        missing_surfaces=missing_surfaces,
    )


def validate_homepage_approval(approval: Mapping[str, Any]) -> dict[str, Any]:
    """Require explicit owner approval of rendered desktop and mobile pages."""

    if not isinstance(approval, Mapping):
        return _result("BLOCKED", [_issue("HOMEPAGE_VISUAL_APPROVAL_REQUIRED", "owner approval evidence must be an object")])
    issues: list[dict[str, str]] = []
    if _normalise_name(_get(approval, "STATE_LOCATION", "")) != "VISUAL_PROTOTYPES_HOMEPAGE_VISUAL_APPROVED":
        issues.append(_issue("HOMEPAGE_APPROVAL_MUST_USE_EXISTING_STATE", "approval belongs under visual_prototypes.homepage_visual_approved"))
    if not _truthy(_get(approval, "HOMEPAGE_VISUAL_APPROVED")):
        issues.append(_issue("HOMEPAGE_VISUAL_APPROVAL_REQUIRED", "visual_prototypes.homepage_visual_approved must be true only after owner approval"))
    if not _truthy(_get(approval, "OWNER_APPROVED")) or _normalise_name(_get(approval, "OWNER_ACTION", "")) != "APPROVE":
        issues.append(_issue("OWNER_APPROVAL_REQUIRED", "the owner must explicitly approve the rendered full homepage"))
    approved_by = _normalise_name(_get(approval, "APPROVED_BY", ""))
    if approved_by in {"BUILDER", "BUILDER_AGENT", "CRITIC", "CRITIC_AGENT", "INTERNAL_CRITIC", "AGENT"} or "CRITIC" in approved_by or "BUILDER" in approved_by:
        issues.append(_issue("OWNER_APPROVAL_CANNOT_BE_SET_BY_CRITIC", "builder or critic output cannot set owner approval"))
    elif approved_by not in {"OWNER", "PROJECT_OWNER", "CLIENT_OWNER"}:
        issues.append(_issue("OWNER_APPROVAL_REQUIRED", "approval actor must be the project owner"))
    surfaces = _surface_ids(_get(approval, "RENDERED_SURFACES", _get(approval, "SCREENSHOT_RECEIPTS")))
    missing_surfaces = [surface for surface in HOMEPAGE_REVIEW_SURFACES if _normalise_name(surface) not in surfaces]
    if missing_surfaces:
        issues.append(_issue("FULL_HOMEPAGE_RENDER_REQUIRED", f"owner review is missing: {', '.join(missing_surfaces)}"))
    if not _truthy(_get(approval, "REVIEWED")):
        issues.append(_issue("OWNER_REVIEW_REQUIRED", "the owner review event must be recorded"))
    if _truthy(_get(approval, "PROSE_ONLY")) or not surfaces:
        issues.append(_issue("PROSE_ONLY_DIRECTION_REJECTED", "prose cannot replace rendered homepage evidence"))
    if _truthy(_get(approval, "INTERNAL_CRITIC_APPROVAL")) or _truthy(_get(approval, "NEW_OWNER_LOCK_CREATED")):
        issues.append(_issue("HOMEPAGE_APPROVAL_NOT_A_LOCK", "critic approval and homepage approval cannot create a new owner lock"))

    codes = {item["code"] for item in issues}
    status = "FAIL" if any(code in {"OWNER_APPROVAL_CANNOT_BE_SET_BY_CRITIC", "HOMEPAGE_APPROVAL_NOT_A_LOCK", "PROSE_ONLY_DIRECTION_REJECTED"} for code in codes) else ("BLOCKED" if issues else "PASS")
    return _result("FAIL" if status == "FAIL" else status, issues, missing_surfaces=missing_surfaces, approved_by=approved_by)


def validate_production_gate(evidence: Mapping[str, Any]) -> dict[str, Any]:
    """Block full production implementation until all design-first evidence exists."""

    required = (
        "BUSINESS_UNDERSTANDING_COMPLETE",
        "OWNER_INTENT_CAPTURED",
        "REQUIRED_ASSETS_IDENTIFIED",
        "REFERENCES_INTERPRETED",
        "HOMEPAGE_RENDERED_AND_REVIEWED",
        "OWNER_APPROVAL_RECORDED",
        "DESIGN_SYSTEM_DERIVED_AND_READY",
    )
    if not isinstance(evidence, Mapping):
        return _result("BLOCKED", [_issue("PRODUCTION_GATE_BLOCKED", "production gate evidence must be an object")], missing_fields=list(required))
    issues: list[dict[str, str]] = []
    missing = [field for field in required if not _truthy(_get(evidence, field))]
    if missing:
        issues.append(_issue("PRODUCTION_GATE_BLOCKED", f"production cannot start; missing evidence: {', '.join(missing)}"))

    approval = _get(evidence, "HOMEPAGE_APPROVAL")
    if not isinstance(approval, Mapping):
        issues.append(_issue("HOMEPAGE_APPROVAL_EVIDENCE_REQUIRED", "owner approval must include the existing-state approval record and rendered surfaces"))
    else:
        approval_result = validate_homepage_approval(approval)
        issues.extend(approval_result["issues"])

    if _truthy(_get(evidence, "PRODUCTION_STARTED")) and missing:
        issues.append(_issue("PRODUCTION_STARTED_BEFORE_HOMEPAGE_APPROVAL", "production implementation started before the design-first gate passed"))
    status = "FAIL" if any(item["code"].startswith("OWNER_APPROVAL_CANNOT") or item["code"].startswith("PROSE_ONLY") for item in issues) else ("BLOCKED" if issues else "PASS")
    return _result(status, issues, missing_fields=missing, can_start_production=not issues)


def validate_design_system_derivation(design_system: Mapping[str, Any]) -> dict[str, Any]:
    """Ensure the token system formalizes the approved homepage rather than redesigning it."""

    if not isinstance(design_system, Mapping):
        return _result("BLOCKED", [_issue("DESIGN_SYSTEM_SOURCE_NOT_APPROVED_HOMEPAGE", "design system evidence must be an object")])
    issues: list[dict[str, str]] = []
    source = _normalise_name(_get(design_system, "HOMEPAGE_SOURCE", _get(design_system, "DERIVED_FROM", "")))
    allowed_sources = {"APPROVED_HOMEPAGE", "VISUAL_PROTOTYPES_HOMEPAGE_VISUAL_APPROVED", "VISUAL_PROTOTYPES_OWNER_SELECTION_PLUS_FULL_HOMEPAGE"}
    if source not in allowed_sources:
        issues.append(_issue("DESIGN_SYSTEM_SOURCE_NOT_APPROVED_HOMEPAGE", "design system must cite the approved full homepage as its source"))
    if _is_missing(_get(design_system, "SOURCE_APPROVAL_REF")):
        issues.append(_issue("DESIGN_SYSTEM_SOURCE_NOT_APPROVED_HOMEPAGE", "design system derivation must cite the homepage approval record"))
    missing_fields = [field for field in DESIGN_SYSTEM_DERIVATION_FIELDS if _is_missing(_get(design_system, field))]
    if missing_fields:
        issues.append(_issue("DESIGN_SYSTEM_DERIVATION_INCOMPLETE", f"design system is missing: {', '.join(missing_fields)}"))
    if _truthy(_get(design_system, "REINTERPRETS_AESTHETIC")) or _truthy(_get(design_system, "CONTRADICTS_HOMEPAGE")):
        issues.append(_issue("DESIGN_SYSTEM_CONTRADICTS_APPROVED_HOMEPAGE", "the design system may formalize the homepage but may not reinterpret or contradict it"))
    status = "FAIL" if any(item["code"] == "DESIGN_SYSTEM_CONTRADICTS_APPROVED_HOMEPAGE" for item in issues) else ("BLOCKED" if issues else "PASS")
    return _result("FAIL" if status == "FAIL" else status, issues, source=source, missing_fields=missing_fields)


def validate_component_routing(router: Mapping[str, Any]) -> dict[str, Any]:
    """Keep components downstream of the approved homepage and design system."""

    if not isinstance(router, Mapping):
        return _result("BLOCKED", [_issue("COMPONENT_AUTHORITY_MISSING", "component routing must identify its upstream design authority")])
    issues: list[dict[str, str]] = []
    authority = _normalise_name(_get(router, "DESIGN_AUTHORITY", _get(router, "DIRECTION_AUTHORITY", "")))
    if authority in {"COMPONENT_LIBRARY", "LIBRARY", "CODESTITCH", "FIGMA"} or _truthy(_get(router, "LIBRARY_DETERMINES_DIRECTION")):
        issues.append(_issue("COMPONENT_LIBRARY_NOT_AUTHORITY", "a component library may supply primitives but cannot determine visual direction"))
    elif authority not in {"APPROVED_HOMEPAGE", "DESIGN_SYSTEM", "OWNER_APPROVED_DESIGN"}:
        issues.append(_issue("COMPONENT_AUTHORITY_MISSING", "components must consume the approved homepage or derived design system"))
    for field in ("FIGMA_REQUIRED", "CODESTITCH_REQUIRED", "MODEL_REQUIRED", "FRAMEWORK_REQUIRED"):
        if _truthy(_get(router, field)):
            issues.append(_issue("COMPONENT_ROUTING_NOT_MANDATORY", f"{field} cannot be a mandatory Website Director dependency"))
    return _result("FAIL" if any(item["code"] == "COMPONENT_LIBRARY_NOT_AUTHORITY" for item in issues) else ("BLOCKED" if issues else "PASS"), issues, authority=authority)


def validate_inspiration_records(records: Sequence[Mapping[str, Any]], registry: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Consume the existing inspiration architecture without cloning or promotion."""

    if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
        return _result("BLOCKED", [_issue("INSPIRATION_INPUTS_INVALID", "inspiration inputs must be an array")])
    issues: list[dict[str, str]] = []
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            issues.append(_issue("INSPIRATION_INPUTS_INVALID", f"inspiration record {index} must be an object"))
            continue
        if not _truthy(_get(record, "REFERENCE_ONLY_STATUS", _get(record, "REFERENCE_ONLY"))):
            mode = _normalise_name(_get(record, "IMPLEMENTATION_MODE", "STUDY_ONLY"))
            if mode != "SOURCE_REUSE":
                issues.append(_issue("REFERENCE_ONLY_BOUNDARY_ENFORCED", f"inspiration record {index} must remain reference-only"))
        if _truthy(_get(record, "LITERAL_CLONE")) or _truthy(_get(record, "CLONE_SOURCE")):
            issues.append(_issue("REFERENCE_CLONE_REJECTED", f"inspiration record {index} proposes literal source cloning"))
        if registry is not None:
            issues.extend(
                _issue(item["code"], f"record {index}: {item['detail']}")
                for item in validate_owner_selected_reference(record, registry)
            )
    status = "FAIL" if any(item["code"] in {"REFERENCE_CLONE_REJECTED", "REFERENCE_ONLY_BOUNDARY_ENFORCED"} for item in issues) else ("BLOCKED" if issues else "PASS")
    return _result(status, issues, record_count=len(records))


def validate_asset_intent(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Keep production assets, support material, and reference inspiration distinct."""

    if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
        return _result("BLOCKED", [_issue("ASSET_INTENT_INVALID", "asset intent must be an array")])
    issues: list[dict[str, str]] = []
    allowed = {"REQUIRED_ASSET", "REFERENCE_INSPIRATION_ONLY", "SUPPORTING_MATERIAL"}
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            issues.append(_issue("ASSET_INTENT_INVALID", f"asset record {index} must be an object"))
            continue
        classification = _normalise_name(_get(record, "CLASSIFICATION", ""))
        if classification not in allowed:
            issues.append(_issue("ASSET_INTENT_INVALID", f"asset record {index} has no valid classification"))
        if classification == "REFERENCE_INSPIRATION_ONLY" and (_truthy(_get(record, "PROMOTED_TO_PRODUCTION")) or _truthy(_get(record, "SHIPS"))):
            issues.append(_issue("REFERENCE_ONLY_ASSET_NOT_PROMOTED", f"reference-only asset {index} cannot ship as a production asset"))
        if classification == "REQUIRED_ASSET" and _is_missing(_get(record, "PROVENANCE_REF")):
            issues.append(_issue("REQUIRED_ASSET_PROVENANCE_REQUIRED", f"required asset {index} needs a provenance reference"))
    status = "FAIL" if any(item["code"] == "REFERENCE_ONLY_ASSET_NOT_PROMOTED" for item in issues) else ("BLOCKED" if issues else "PASS")
    return _result(status, issues, record_count=len(records))


def validate_downstream_authorities(flow: Mapping[str, Any]) -> dict[str, Any]:
    """Preserve Browser QA as behavior authority and Gauntlet as qualitative authority."""

    if not isinstance(flow, Mapping):
        return _result("BLOCKED", [_issue("DOWNSTREAM_AUTHORITY_CONTRACT_INVALID", "downstream authority evidence must be an object")])
    issues: list[dict[str, str]] = []
    sequence = tuple(_normalise_name(item) for item in (_get(flow, "SEQUENCE", []) or []))
    if not sequence or "BROWSER_QA" not in sequence or "VISUAL_GAUNTLET" not in sequence or sequence.index("BROWSER_QA") > sequence.index("VISUAL_GAUNTLET"):
        issues.append(_issue("BROWSER_QA_BEFORE_GAUNTLET_REQUIRED", "Browser QA must precede the qualitative Visual Gauntlet"))
    authorities = _get(flow, "AUTHORITIES", {})
    if isinstance(authorities, Mapping):
        if _normalise_name(_get(authorities, "BROWSER_QA", "")) not in {"BEHAVIOR_AUTHORITY", "MACHINE_BEHAVIOR_AUTHORITY"}:
            issues.append(_issue("BROWSER_QA_AUTHORITY_PRESERVED", "Browser QA remains the behavior authority"))
        if _normalise_name(_get(authorities, "VISUAL_GAUNTLET", "")) not in {"QUALITATIVE_AUTHORITY", "ADVERSARIAL_QUALITATIVE_AUTHORITY"}:
            issues.append(_issue("GAUNTLET_AUTHORITY_PRESERVED", "the Visual Gauntlet remains the post-QA qualitative authority"))
    else:
        issues.append(_issue("DOWNSTREAM_AUTHORITY_CONTRACT_INVALID", "authority roles must be explicit"))
    if _truthy(_get(flow, "DUPLICATE_BROWSER_RUNNER")) or _truthy(_get(flow, "DUPLICATE_GAUNTLET")):
        issues.append(_issue("EXISTING_AUTHORITIES_NOT_DUPLICATED", "the flow must consume existing Browser QA and Gauntlet authorities"))
    return _result("FAIL" if issues else "PASS", issues)


def validate_owner_lock_contract(profile: Mapping[str, Any]) -> dict[str, Any]:
    """Prove the new flow leaves the exact five owner locks untouched."""

    if not isinstance(profile, Mapping):
        return _result("BLOCKED", [_issue("OWNER_LOCK_INVARIANT", "profile must contain the existing locks object")])
    locks = _get(profile, "LOCKS", profile)
    if not isinstance(locks, Mapping):
        return _result("BLOCKED", [_issue("OWNER_LOCK_INVARIANT", "locks must be an object")])
    observed = tuple(sorted(str(key) for key in locks))
    expected = tuple(sorted(CANONICAL_LOCKS))
    issues: list[dict[str, str]] = []
    if observed != expected:
        issues.append(_issue("OWNER_LOCK_INVARIANT", f"expected exactly {', '.join(expected)}"))
    if any(not isinstance(value, bool) for value in locks.values()):
        issues.append(_issue("OWNER_LOCK_INVARIANT", "all canonical lock values must remain booleans"))
    if any("HOMEPAGE" in str(key).upper() or str(key).lower().endswith("_locked") and str(key) not in CANONICAL_LOCKS for key in locks):
        issues.append(_issue("NO_SIXTH_OWNER_LOCK", "homepage approval cannot be represented as a new owner lock"))
    return _result("FAIL" if issues else "PASS", issues, observed_locks=list(observed), expected_locks=list(expected))


__all__ = [
    "BUSINESS_UNDERSTANDING_FIELDS",
    "CANONICAL_LOCKS",
    "CREATIVE_AMBITIONS",
    "DESIGN_SIGNALS",
    "DESIGN_SYSTEM_DERIVATION_FIELDS",
    "DISCOVERY_MODES",
    "FULL_HOMEPAGE_SECTIONS",
    "HOMEPAGE_REVIEW_SURFACES",
    "OPERATING_FLOW",
    "OPERATING_INVARIANTS",
    "extract_client_voice",
    "validate_ambition_policy",
    "validate_asset_intent",
    "validate_business_understanding",
    "validate_client_voice_fidelity",
    "validate_component_routing",
    "validate_design_system_derivation",
    "validate_discovery_mode",
    "validate_downstream_authorities",
    "validate_homepage_approval",
    "validate_homepage_design",
    "validate_inspiration_records",
    "validate_operating_flow",
    "validate_owner_lock_contract",
    "validate_production_gate",
]
