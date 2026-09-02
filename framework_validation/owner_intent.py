"""Deterministic owner-intent, authority, brand, and motion contracts.

This module is the framework's small, provider-neutral enforcement layer for
explicit owner direction.  It deliberately does not create a readiness state,
owner lock, browser runner, or project-specific build rule.  It normalizes
inputs before creative work, resolves current authority over historical and
reference material, and derives compliance from implementation and runtime
evidence rather than from prose claims.
"""

from __future__ import annotations

import colorsys
import json
import re
from collections import defaultdict
from typing import Any, Iterable, Mapping, Sequence


AUTHORITY_PRECEDENCE = (
    "CURRENT_OWNER_INSTRUCTION",
    "CURRENT_APPROVED_BRAND_PROJECT_CONTRACT",
    "LOCKED_BUSINESS_AUDIENCE_CONVERSION_PROJECT_TRUTH",
    "LOCKED_DESIGN_AND_MOTION_DECISIONS",
    "WEBSITE_DIRECTOR_SPECIALIST_INTELLIGENCE",
    "REFERENCE_INSPIRATION_INTELLIGENCE",
    "HISTORICAL_PROJECT_MATERIAL",
    "DEFAULTS_HEURISTICS",
)

REQUIREMENT_CLASSES = ("REQUIRED", "PROHIBITED", "PREFERRED", "OPTIONAL")
CURRENTNESS_VALUES = ("CURRENT", "HISTORICAL", "REFERENCE_ONLY", "SUPERSEDED")
REFERENCE_SIGNAL_CLASSES = (
    "TRANSFERABLE_PRINCIPLE",
    "BRAND_SPECIFIC_DO_NOT_TRANSFER",
    "OPTIONAL_INTERPRETATION",
    "REJECTED",
)
MOTION_LEVELS = (
    "MOTION_LEVEL_0",
    "MOTION_LEVEL_1",
    "MOTION_LEVEL_2",
    "MOTION_LEVEL_3",
)

_AUTHORITY_ALIASES = {
    "CURRENT_OWNER": "CURRENT_OWNER_INSTRUCTION",
    "OWNER": "CURRENT_OWNER_INSTRUCTION",
    "EXPLICIT_OWNER": "CURRENT_OWNER_INSTRUCTION",
    "CURRENT_OWNER_INSTRUCTION": "CURRENT_OWNER_INSTRUCTION",
    "APPROVED_BRAND_CONTRACT": "CURRENT_APPROVED_BRAND_PROJECT_CONTRACT",
    "CURRENT_BRAND_CONTRACT": "CURRENT_APPROVED_BRAND_PROJECT_CONTRACT",
    "PROJECT_CONTRACT": "CURRENT_APPROVED_BRAND_PROJECT_CONTRACT",
    "CURRENT_APPROVED_BRAND_PROJECT_CONTRACT": "CURRENT_APPROVED_BRAND_PROJECT_CONTRACT",
    "LOCKED_PROJECT_TRUTH": "LOCKED_BUSINESS_AUDIENCE_CONVERSION_PROJECT_TRUTH",
    "LOCKED_BUSINESS_AUDIENCE_CONVERSION_TRUTH": "LOCKED_BUSINESS_AUDIENCE_CONVERSION_PROJECT_TRUTH",
    "LOCKED_BUSINESS_AUDIENCE_CONVERSION_PROJECT_TRUTH": "LOCKED_BUSINESS_AUDIENCE_CONVERSION_PROJECT_TRUTH",
    "LOCKED_DESIGN_MOTION": "LOCKED_DESIGN_AND_MOTION_DECISIONS",
    "DESIGN_DECISIONS": "LOCKED_DESIGN_AND_MOTION_DECISIONS",
    "LOCKED_DESIGN_AND_MOTION_DECISIONS": "LOCKED_DESIGN_AND_MOTION_DECISIONS",
    "SPECIALIST_INTELLIGENCE": "WEBSITE_DIRECTOR_SPECIALIST_INTELLIGENCE",
    "WEBSITE_DIRECTOR_SPECIALIST_INTELLIGENCE": "WEBSITE_DIRECTOR_SPECIALIST_INTELLIGENCE",
    "REFERENCE": "REFERENCE_INSPIRATION_INTELLIGENCE",
    "REFERENCE_ONLY": "REFERENCE_INSPIRATION_INTELLIGENCE",
    "REFERENCE_INSPIRATION": "REFERENCE_INSPIRATION_INTELLIGENCE",
    "REFERENCE_INSPIRATION_INTELLIGENCE": "REFERENCE_INSPIRATION_INTELLIGENCE",
    "HISTORICAL": "HISTORICAL_PROJECT_MATERIAL",
    "HISTORICAL_PROJECT": "HISTORICAL_PROJECT_MATERIAL",
    "HISTORICAL_PROJECT_MATERIAL": "HISTORICAL_PROJECT_MATERIAL",
    "DEFAULT": "DEFAULTS_HEURISTICS",
    "HEURISTIC": "DEFAULTS_HEURISTICS",
    "DEFAULTS": "DEFAULTS_HEURISTICS",
    "DEFAULTS_HEURISTICS": "DEFAULTS_HEURISTICS",
}

_CLASS_ALIASES = {
    "MUST": "REQUIRED",
    "MANDATORY": "REQUIRED",
    "REQUIRED": "REQUIRED",
    "MUST_NOT": "PROHIBITED",
    "MUST NOT": "PROHIBITED",
    "FORBIDDEN": "PROHIBITED",
    "PROHIBITED": "PROHIBITED",
    "SHOULD": "PREFERRED",
    "PREFERRED": "PREFERRED",
    "MAY": "OPTIONAL",
    "OPTIONAL": "OPTIONAL",
}

_CURRENTNESS_ALIASES = {
    "ACTIVE": "CURRENT",
    "CURRENT": "CURRENT",
    "LOCKED": "CURRENT",
    "HISTORICAL": "HISTORICAL",
    "LEGACY": "HISTORICAL",
    "ARCHIVED": "HISTORICAL",
    "REFERENCE": "REFERENCE_ONLY",
    "REFERENCE_ONLY": "REFERENCE_ONLY",
    "SUPERSEDED": "SUPERSEDED",
}

_MOTION_KEYWORDS_LEVEL_3 = re.compile(
    r"(?i)\b(cinematic|cinema|immersive|animation[- _]?heavy|scroll[- _]?driven|"
    r"scroll[- _]?storytelling|scrollytelling|film[- _]?like|choreograph(?:y|ed)|"
    r"kinetic|environment transition|sequence[- _]?driven)\b"
)
_MOTION_LEVEL_RE = re.compile(r"(?i)MOTION[ _-]*LEVEL[ _-]*([0-3])|\bLEVEL[ _-]*([0-3])\b")
_HEX_RE = re.compile(r"^#?([0-9a-f]{3}|[0-9a-f]{6}|[0-9a-f]{8})$", re.I)
_RGB_RE = re.compile(r"rgba?\s*\(([^)]+)\)", re.I)
_HSL_RE = re.compile(r"hsla?\s*\(([^)]+)\)", re.I)
_GENERIC_MOTION_RE = re.compile(
    r"(?i)(?:^|[_ -])(fade(?:[-_ ]?(?:in|up|down|out))?|generic(?:[-_ ]?reveal)?|"
    r"reveal|opacity(?:[-_ ]?translate)?|translate[-_ ]?y)(?:$|[_ -])"
)
_NEUTRAL_RE = re.compile(
    r"(?i)\b(white|black|gray|grey|silver|neutral|charcoal|slate|ivory|"
    r"transparent|currentcolor|inherit)\b"
)
_COLOR_FAMILY_WORDS = {
    "red": "RED", "crimson": "RED", "scarlet": "RED", "coral": "RED",
    "orange": "ORANGE", "burnt orange": "ORANGE", "peach": "PEACH",
    "amber": "AMBER", "yellow": "YELLOW", "lemon": "YELLOW",
    "gold": "YELLOW", "blue": "BLUE", "navy": "BLUE", "navy blue": "BLUE",
    "cobalt": "BLUE", "azure": "BLUE", "royal blue": "BLUE", "indigo": "BLUE",
    "purple": "PURPLE", "violet": "PURPLE", "lavender": "PURPLE",
    "pink": "PINK", "green": "GREEN", "teal": "TEAL", "cyan": "CYAN",
    "beige": "BEIGE", "cream": "CREAM", "brown": "BROWN",
}


def _read(record: Mapping[str, Any], *names: str, default: Any = None) -> Any:
    for name in names:
        candidates = (name, name.lower(), name.upper())
        for candidate in candidates:
            if candidate in record:
                return record[candidate]
    return default


def _nonempty(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, Mapping):
        for key in ("items", "requirements", "sequences", "screenshots", "records"):
            nested = value.get(key)
            if isinstance(nested, list):
                return nested
        return [value]
    return [value]


def _issue(code: str, detail: str, *, blocking: bool = False) -> dict[str, Any]:
    return {"code": code, "detail": detail, "blocking": blocking}


def _append_issue(issues: list[dict[str, Any]], code: str, detail: str, *, blocking: bool = False) -> None:
    if not any(item.get("code") == code and item.get("detail") == detail for item in issues):
        issues.append(_issue(code, detail, blocking=blocking))


def _canonical_class(value: Any) -> str | None:
    if value is None:
        return None
    return _CLASS_ALIASES.get(str(value).strip().upper())


def _canonical_authority(value: Any) -> str | None:
    if value is None:
        return None
    key = re.sub(r"[^A-Z0-9_]+", "_", str(value).strip().upper()).strip("_")
    return _AUTHORITY_ALIASES.get(key)


def _canonical_currentness(value: Any) -> str | None:
    if value is None:
        return None
    return _CURRENTNESS_ALIASES.get(str(value).strip().upper())


def _canonical_level(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    match = re.search(r"(?i)(?:MOTION[ _-]*)?LEVEL[ _-]*([0-3])", str(value))
    if not match and str(value).strip() in {"0", "1", "2", "3"}:
        match = re.match(r"([0-3])", str(value).strip())
    return "MOTION_LEVEL_" + match.group(1) if match else None


def motion_level_number(value: Any) -> int | None:
    canonical = _canonical_level(value)
    return int(canonical[-1]) if canonical else None


def _authority_rank(value: Any) -> int:
    canonical = _canonical_authority(value) or "DEFAULTS_HEURISTICS"
    return AUTHORITY_PRECEDENCE.index(canonical)


def _currentness_rank(value: Any) -> int:
    return {"CURRENT": 3, "REFERENCE_ONLY": 2, "SUPERSEDED": 1, "HISTORICAL": 0}.get(
        _canonical_currentness(value) or "HISTORICAL", 0)


def _semantic_value(record: Mapping[str, Any]) -> Any:
    value = _read(record, "values", "value", "constraint", "requirement", "description")
    if isinstance(value, Mapping):
        return {str(k): value[k] for k in sorted(value)}
    if isinstance(value, (list, tuple, set)):
        return sorted(str(item) for item in value)
    return str(value).strip().lower() if value is not None else None


def _target_for(record: Mapping[str, Any]) -> str:
    target = _read(record, "target", "constraint_id", "subject")
    if _nonempty(target):
        return str(target).strip().lower()
    identifier = _read(record, "id", "requirement_id")
    if _nonempty(identifier):
        return str(identifier).strip().lower()
    domain = _read(record, "domain", default="general")
    return str(domain).strip().lower()


def _raw_requirement_items(source: Any) -> list[Any]:
    if isinstance(source, Mapping):
        raw = _read(source, "requirements", "owner_requirements", "constraints")
        if raw is not None:
            return _as_list(raw)
        if any(_read(source, key) is not None for key in ("id", "requirement_id", "class", "requirement_class", "target")):
            return [source]
        nested: list[Any] = []
        for key in ("brand_requirements", "motion_requirements", "reference_requirements"):
            nested.extend(_as_list(_read(source, key)))
        return nested
    return _as_list(source)


def normalize_owner_requirements(source: Any) -> dict[str, Any]:
    """Normalize explicit constraints while retaining authority metadata.

    The returned ``requirements`` list is deliberately verbose.  It keeps the
    source, currentness, scope, authority, class, and target beside the value
    so downstream validators cannot accidentally treat prose or stale history
    as current authority.
    """

    parent = source if isinstance(source, Mapping) else {}
    issues: list[dict[str, Any]] = []
    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    parent_source = _read(parent, "source", "source_id", default=None)
    parent_authority = _canonical_authority(_read(parent, "authority", "authority_level"))
    parent_currentness = _canonical_currentness(_read(parent, "currentness", "recency", "status"))
    parent_scope = _read(parent, "scope", "applies_to", default="PROJECT_CURRENT")

    for index, raw in enumerate(_raw_requirement_items(source)):
        if isinstance(raw, str):
            raw = {"id": "requirement-%d" % (index + 1), "requirement": raw}
        if not isinstance(raw, Mapping):
            _append_issue(issues, "REQUIREMENT_SHAPE", "requirements[%d] must be an object" % index)
            continue
        identifier = _read(raw, "id", "requirement_id")
        if not _nonempty(identifier):
            _append_issue(issues, "REQUIREMENT_ID_MISSING", "requirements[%d] has no stable id" % index)
            identifier = "requirement-%d" % (index + 1)
        identifier = str(identifier)
        if identifier in seen_ids:
            _append_issue(issues, "DUPLICATE_REQUIREMENT_ID", "duplicate requirement id %r" % identifier)
        seen_ids.add(identifier)

        requirement_class = _canonical_class(_read(raw, "class", "requirement_class", "type"))
        authority = _canonical_authority(_read(raw, "authority", "authority_level")) or parent_authority
        currentness = _canonical_currentness(_read(raw, "currentness", "recency", "status")) or parent_currentness
        source_name = _read(raw, "source", "source_id") or parent_source
        scope = _read(raw, "scope", "applies_to") or parent_scope
        if requirement_class is None:
            _append_issue(issues, "REQUIREMENT_CLASS_MISSING", "%s has no valid class" % identifier)
            requirement_class = "OPTIONAL"
        raw_authority = _read(raw, "authority", "authority_level")
        raw_currentness = _read(raw, "currentness", "recency", "status")
        if raw_authority is not None and _canonical_authority(raw_authority) is None:
            _append_issue(issues, "AUTHORITY_METADATA_INVALID", "%s has an unknown authority %r" % (identifier, raw_authority))
        if raw_currentness is not None and _canonical_currentness(raw_currentness) is None:
            _append_issue(issues, "CURRENTNESS_METADATA_INVALID", "%s has an unknown currentness %r" % (identifier, raw_currentness))
        if authority is None:
            _append_issue(issues, "AUTHORITY_METADATA_MISSING", "%s has no authority" % identifier)
            authority = "DEFAULTS_HEURISTICS"
        if currentness is None:
            _append_issue(issues, "CURRENTNESS_METADATA_MISSING", "%s has no currentness/recency" % identifier)
            currentness = "HISTORICAL"
        if not _nonempty(source_name):
            _append_issue(issues, "SOURCE_METADATA_MISSING", "%s has no source" % identifier)
            source_name = "UNSPECIFIED"
        if not _nonempty(scope):
            _append_issue(issues, "SCOPE_METADATA_MISSING", "%s has no scope" % identifier)
            scope = "PROJECT_CURRENT"

        requirement_text = _read(raw, "requirement", "constraint", "description", default="")
        value = _read(raw, "values", "value", default=requirement_text)
        level = _canonical_level(_read(raw, "minimum_motion_level", "motion_level", "level"))
        if level is None and str(_read(raw, "domain", default="")).lower() == "motion":
            level = _extract_level_from_text(value)
        normalized.append({
            "id": identifier,
            "target": _target_for({**raw, "id": identifier}),
            "domain": str(_read(raw, "domain", default="general")).lower(),
            "class": requirement_class,
            "requirement": requirement_text,
            "values": value,
            "source": str(source_name),
            "currentness": currentness,
            "recency": currentness,
            "scope": str(scope),
            "authority": authority,
            "minimum_motion_level": level,
            "rationale": _read(raw, "rationale", "why", default=""),
            "raw": dict(raw),
        })

    return {
        "status": "PASS" if not issues else "FAIL",
        "contract_id": _read(parent, "contract_id", "id", default=""),
        "project_name": _read(parent, "project_name", "project", default=""),
        "authority_precedence": list(AUTHORITY_PRECEDENCE),
        "requirements": normalized,
        "issues": issues,
    }


def _extract_level_from_text(value: Any) -> str | None:
    if isinstance(value, Mapping):
        for child in value.values():
            level = _extract_level_from_text(child)
            if level:
                return level
        return None
    if isinstance(value, (list, tuple)):
        for child in value:
            level = _extract_level_from_text(child)
            if level:
                return level
        return None
    if value is None:
        return None
    match = _MOTION_LEVEL_RE.search(str(value))
    if match:
        return "MOTION_LEVEL_" + (match.group(1) or match.group(2))
    if _MOTION_KEYWORDS_LEVEL_3.search(str(value)):
        return "MOTION_LEVEL_3"
    return None


def _contract_records(records: Any) -> list[Any]:
    if isinstance(records, Mapping) and any(
            _read(records, key) is not None for key in ("requirements", "owner_requirements", "constraints")):
        return [records]
    if isinstance(records, Mapping):
        return [records]
    return _as_list(records)


def classify_historical_brand_direction(direction: Any, current_brand: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Classify an old palette without allowing it to become current authority."""

    current_brand = current_brand or {}
    text = json.dumps(direction, sort_keys=True) if isinstance(direction, Mapping) else str(direction)
    current_text = json.dumps(current_brand, sort_keys=True)
    changed = text.strip().lower() not in current_text.strip().lower()
    return {
        "classification": "SUPERSEDED" if changed else "HISTORICAL",
        "authority": "HISTORICAL_PROJECT_MATERIAL",
        "currentness": "SUPERSEDED" if changed else "HISTORICAL",
        "reference_only": True,
        "direction": direction,
    }


def resolve_authority_conflicts(records: Any) -> dict[str, Any]:
    """Resolve same-target records using the canonical authority ordering."""

    requirements: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    for record in _contract_records(records):
        normalized = normalize_owner_requirements(record)
        requirements.extend(normalized["requirements"])
        for issue in normalized["issues"]:
            _append_issue(issues, issue["code"], issue["detail"], blocking=issue.get("blocking", False))

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for requirement in requirements:
        grouped[requirement["target"]].append(requirement)

    resolutions: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    historical_conflicts: list[dict[str, Any]] = []
    for target, candidates in sorted(grouped.items()):
        values = {_json_key(_semantic_value(candidate)) for candidate in candidates}
        ordered = sorted(candidates, key=lambda item: (
            _authority_rank(item["authority"]),
            -_currentness_rank(item["currentness"]),
            item["id"],
        ))
        top = ordered[0]
        top_tier = [candidate for candidate in ordered if (
            _authority_rank(candidate["authority"]), -_currentness_rank(candidate["currentness"])
        ) == (_authority_rank(top["authority"]), -_currentness_rank(top["currentness"]))]
        top_values = {_json_key(_semantic_value(candidate)) for candidate in top_tier}
        unresolved = len(top_values) > 1
        if unresolved:
            conflict = {
                "target": target,
                "candidates": top_tier,
                "reason": "same authority and currentness contain incompatible values",
            }
            conflicts.append(conflict)
            _append_issue(issues, "UNRESOLVED_AUTHORITY_CONFLICT", target, blocking=True)
        losers = []
        for candidate in ordered[1:]:
            if _json_key(_semantic_value(candidate)) == _json_key(_semantic_value(top)):
                continue
            if candidate["currentness"] in ("HISTORICAL", "SUPERSEDED"):
                classification = "LEGACY" if candidate["currentness"] == "HISTORICAL" else "SUPERSEDED"
                historical_conflicts.append({"target": target, "record": candidate, "classification": classification})
            elif _canonical_authority(candidate["authority"]) == "REFERENCE_INSPIRATION_INTELLIGENCE":
                classification = "NON_AUTHORITATIVE"
            else:
                classification = "SUPERSEDED"
            losers.append({"record": candidate, "classification": classification})
        resolutions.append({
            "target": target,
            "winner": None if unresolved else top,
            "losers": losers,
            "conflict": unresolved,
            "candidate_count": len(candidates),
        })

    return {
        "status": "FAIL" if conflicts else "PASS",
        "requirements": requirements,
        "resolutions": resolutions,
        "conflicts": conflicts,
        "historical_conflicts": historical_conflicts,
        "issues": issues,
    }


def detect_contradictions(records: Any) -> dict[str, Any]:
    """Run the authority resolver as the pre-implementation contradiction gate."""

    result = resolve_authority_conflicts(records)
    return {
        "status": result["status"],
        "contradictions": result["conflicts"],
        "resolutions": result["resolutions"],
        "historical_conflicts": result["historical_conflicts"],
        "issues": result["issues"],
    }


def _brand_entries(value: Any, *, role: str = "", source: str = "implementation", material: bool = False) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if isinstance(value, Mapping):
        if any(key in value for key in ("value", "color", "token", "name", "hex", "css")):
            raw_value = _read(value, "value", "color", "token", "name", "hex", "css")
            entry = dict(value)
            entry.update({"value": raw_value, "role": _read(value, "role", default=role),
                          "source": source, "material": material or bool(_read(value, "dominant", "primary", default=False))})
            entries.append(entry)
            return entries
        for key, child in value.items():
            key_lower = str(key).lower()
            child_role = key_lower if key_lower in {"primary", "accent", "brand", "dominant", "background", "surface", "text", "border", "neutral", "supporting_neutral", "from", "to", "start", "end", "stop"} else role
            child_material = material or key_lower in {"primary", "accent", "brand", "dominant", "dominant_colors", "brand_tokens", "gradient", "gradients", "stops"}
            entries.extend(_brand_entries(child, role=child_role, source=source, material=child_material))
        return entries
    if isinstance(value, (list, tuple, set)):
        for child in value:
            entries.extend(_brand_entries(child, role=role, source=source, material=True if role in ("primary", "accent", "brand", "dominant") else material))
        return entries
    if _nonempty(value):
        entries.append({"value": value, "role": role, "source": source, "material": material})
    return entries


def _color_family(value: Any) -> str | None:
    text = str(value).strip().lower().replace("_", " ").replace("-", " ")
    for name in sorted(_COLOR_FAMILY_WORDS, key=len, reverse=True):
        if name in text:
            return _COLOR_FAMILY_WORDS[name]
    rgb = _parse_color(value)
    if rgb is None:
        return None
    red, green, blue = rgb
    hue, lightness, saturation = colorsys.rgb_to_hls(red, green, blue)
    if saturation < 0.08:
        return "NEUTRAL"
    degrees = hue * 360
    if degrees < 15 or degrees >= 345:
        return "RED"
    if degrees < 45:
        return "ORANGE"
    if degrees < 75:
        return "YELLOW"
    if degrees < 165:
        return "GREEN"
    if degrees < 195:
        return "CYAN"
    if degrees < 255:
        return "BLUE"
    if degrees < 300:
        return "PURPLE"
    return "PINK"


def _parse_color(value: Any) -> tuple[float, float, float] | None:
    text = str(value).strip()
    match = _HEX_RE.fullmatch(text)
    if match:
        raw = match.group(1)
        if len(raw) in (3, 4):
            raw = "".join(char * 2 for char in raw[:3])
        return tuple(int(raw[index:index + 2], 16) / 255 for index in (0, 2, 4))  # type: ignore[return-value]
    match = _RGB_RE.search(text)
    if match:
        values = [part.strip() for part in match.group(1).split(",")[:3]]
        try:
            return tuple(float(part.rstrip("%")) / (100 if part.endswith("%") else 255) for part in values)  # type: ignore[return-value]
        except ValueError:
            return None
    match = _HSL_RE.search(text)
    if match:
        parts = [part.strip().rstrip("%") for part in match.group(1).split(",")[:3]]
        try:
            hue = (float(parts[0]) % 360) / 360
            saturation = float(parts[1]) / 100
            lightness = float(parts[2]) / 100
            red, green, blue = colorsys.hls_to_rgb(hue, lightness, saturation)
            return red, green, blue
        except ValueError:
            return None
    return None


def _color_name(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value).strip().lower().replace("_", " ").replace("-", " "))


def _is_neutral(value: Any) -> bool:
    return _color_family(value) == "NEUTRAL" or bool(_NEUTRAL_RE.search(_color_name(value)))


def _brand_contract_entries(brand_contract: Mapping[str, Any]) -> tuple[list[dict[str, Any]], set[str]]:
    current = _read(brand_contract, "current_brand", "brand")
    if not isinstance(current, Mapping):
        return [], set()
    entries: list[dict[str, Any]] = []
    allowed_names: set[str] = set()
    for role, child in current.items():
        if role in {"forbidden_dominant_hues", "supporting_neutrals", "allowed_derivatives", "notes", "exact_values_approved"}:
            continue
        for entry in _brand_entries(child, role=str(role), source="current_brand", material=True):
            entries.append(entry)
            allowed_names.add(_color_name(entry.get("value")))
            token = _read(entry, "token", "semantic_token")
            if token:
                allowed_names.add(_color_name(token))
    for color in _as_list(_read(current, "supporting_neutrals", default=[])):
        allowed_names.add(_color_name(color))
    return entries, allowed_names


def _is_approved_color(entry: Mapping[str, Any], approved: list[dict[str, Any]], allowed_names: set[str]) -> bool:
    value = entry.get("value")
    name = _color_name(value)
    token = _color_name(_read(entry, "token", "semantic_token", default=""))
    derived = _color_name(_read(entry, "derived_from", "derivative_of", default=""))
    if name in allowed_names or token in allowed_names or derived in allowed_names:
        return True
    if _read(entry, "approved", "approved_derivative", default=False) is True:
        return True
    family = _color_family(value)
    approved_families = {_color_family(item.get("value")) for item in approved}
    approved_families.discard(None)
    return family in approved_families


def validate_brand_tokens(
    brand_contract: Mapping[str, Any],
    implementation: Mapping[str, Any] | None = None,
    rendered: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate role/dominance-aware brand tokens and rendered color evidence."""

    implementation = implementation or {}
    issues: list[dict[str, Any]] = []
    approved, allowed_names = _brand_contract_entries(brand_contract)
    current = _read(brand_contract, "current_brand", "brand")
    if not isinstance(current, Mapping) or not any(_read(current, key) is not None for key in ("primary", "accent")):
        _append_issue(issues, "BRAND_CONTRACT_MISSING", "current brand contract must define primary and accent", blocking=True)
        return {"status": "FAIL", "issues": issues, "findings": [], "allowed_tokens": sorted(allowed_names)}

    forbidden = {_color_name(item) for item in _as_list(_read(current, "forbidden_dominant_hues", default=[]))}
    approved_brand_names = {
        _color_name(item.get("value"))
        for item in approved
        if _color_name(item.get("role", "")) in {"primary", "accent", "brand", "dominant"}
    }
    approved_brand_names.update(
        _color_name(_read(item, "token", "semantic_token", default=""))
        for item in approved
        if _color_name(item.get("role", "")) in {"primary", "accent", "brand", "dominant"}
    )
    raw_entries: list[dict[str, Any]] = []
    for key in ("colors", "color_roles", "brand_tokens", "tokens", "dominant_colors", "palette", "gradients", "computed_colors"):
        if key in implementation:
            raw_entries.extend(_brand_entries(implementation[key], source=key, material=key in {"dominant_colors", "palette", "brand_tokens", "gradients", "computed_colors"}))
    if not raw_entries:
        raw_entries.extend(_brand_entries(implementation, source="implementation", material=False))
    if rendered:
        for key in ("colors", "dominant_colors", "palette", "computed_colors", "rendered_colors"):
            if key in rendered:
                raw_entries.extend(_brand_entries(rendered[key], source="rendered." + key, material=True))

    findings: list[dict[str, Any]] = []
    for entry in raw_entries:
        value = entry.get("value")
        if not _nonempty(value):
            continue
        name = _color_name(value)
        family = _color_family(value)
        role = _color_name(entry.get("role", ""))
        area_ratio = entry.get("area_ratio", entry.get("coverage", 0))
        try:
            area_ratio = float(area_ratio or 0)
        except (TypeError, ValueError):
            area_ratio = 0.0
        material = bool(entry.get("material")) or role in {"primary", "accent", "brand", "dominant"} or area_ratio >= 0.15
        if name in forbidden and material:
            reason = "forbidden historical/unapproved dominant hue %s" % value
            findings.append({"value": value, "family": family, "role": role, "source": entry.get("source"), "reason": reason})
            _append_issue(issues, "UNAPPROVED_DOMINANT_BRAND_HUE", reason)
            continue
        if _is_neutral(value):
            # Neutrals are permitted for contrast and accessibility, but a
            # neutral still cannot silently become the primary/accent brand
            # role when the contract names a different brand color.
            if role not in {"primary", "accent", "brand", "dominant"}:
                continue
            if _is_approved_color(entry, approved, approved_brand_names):
                continue
        if material and not _is_approved_color(entry, approved, allowed_names):
            reason = "unapproved dominant brand hue %s (role=%s, source=%s)" % (value, role or "unspecified", entry.get("source"))
            findings.append({"value": value, "family": family, "role": role, "source": entry.get("source"), "reason": reason})
            _append_issue(issues, "UNAPPROVED_DOMINANT_BRAND_HUE", reason)

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "findings": findings,
        "allowed_tokens": sorted(allowed_names),
        "approved_families": sorted({_color_family(item.get("value")) for item in approved if _color_family(item.get("value"))}),
    }


def classify_reference_signal(reference: Mapping[str, Any]) -> str:
    explicit = _read(reference, "signal_class", "reference_signal_class", "classification")
    if explicit:
        normalized = str(explicit).strip().upper().replace("-", "_").replace(" ", "_")
        if normalized in REFERENCE_SIGNAL_CLASSES:
            return normalized
    if _read(reference, "rejected", default=False) is True:
        return "REJECTED"
    if _read(reference, "brand_specific", "do_not_transfer", default=False) is True:
        return "BRAND_SPECIFIC_DO_NOT_TRANSFER"
    if _nonempty(_read(reference, "transferable_principle", "TRANSFERABLE_PRINCIPLE")):
        return "TRANSFERABLE_PRINCIPLE"
    return "OPTIONAL_INTERPRETATION"


def validate_reference_translation_trace(reference: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the four-class reference boundary and implementation trace."""

    signal_class = classify_reference_signal(reference)
    source_signal = _read(reference, "source_signal", "signal", "WHAT_I_LIKE", "what_i_like")
    principle = _read(reference, "transferable_principle", "PATTERN_TO_LEARN", "WHAT_SPECIFICALLY_WORKS")
    translation = _read(reference, "client_specific_interpretation", "client_translation", "BRAND_ADAPTATION", "WHY_IS_THIS_RELEVANT")
    implementation = _read(reference, "implementation_ref", "implementation", "IMPLEMENTATION_REF", default="")
    implemented = _read(reference, "implemented", "in_implementation", default=None)
    if implemented is None:
        implemented = bool(implementation) or str(_read(reference, "implementation_mode", "IMPLEMENTATION_MODE", default="STUDY_ONLY")).upper() not in {"STUDY_ONLY", "REFERENCE_ONLY", "NONE"}
    non_copy = _read(reference, "non_copy_boundary", "WHAT_NOT_TO_COPY", "what_not_to_copy")
    issues: list[dict[str, Any]] = []
    if signal_class in {"TRANSFERABLE_PRINCIPLE", "OPTIONAL_INTERPRETATION"} and implemented:
        for code, label, value in (
            ("REFERENCE_SOURCE_SIGNAL_MISSING", "source signal", source_signal),
            ("REFERENCE_TRANSFERABLE_PRINCIPLE_MISSING", "transferable principle", principle),
            ("REFERENCE_CLIENT_TRANSLATION_MISSING", "client-specific interpretation", translation),
            ("REFERENCE_IMPLEMENTATION_TRACE_MISSING", "implementation trace", implementation),
        ):
            if not _nonempty(value):
                _append_issue(issues, code, "implemented reference is missing %s" % label, blocking=True)
        if not _nonempty(non_copy):
            _append_issue(issues, "REFERENCE_NON_COPY_BOUNDARY_MISSING", "implemented reference is missing what-not-to-copy boundary", blocking=True)
    if signal_class in {"BRAND_SPECIFIC_DO_NOT_TRANSFER", "REJECTED"} and implemented:
        _append_issue(issues, "REFERENCE_BOUNDARY_VIOLATION", "%s reference signal cannot be implemented" % signal_class)
    return {
        "status": "PASS" if not issues else "FAIL",
        "signal_class": signal_class,
        "source_signal": source_signal,
        "transferable_principle": principle,
        "client_specific_interpretation": translation,
        "implementation_ref": implementation,
        "non_copy_boundary": non_copy,
        "implemented": bool(implemented),
        "issues": issues,
    }


def resolve_motion_requirement(
    owner_requirements: Any,
    heuristic_level: Any = "MOTION_LEVEL_1",
    approved_downgrade: bool = False,
) -> dict[str, Any]:
    """Resolve explicit owner motion intent before heuristic defaults."""

    normalized = owner_requirements if isinstance(owner_requirements, Mapping) and "requirements" in owner_requirements else normalize_owner_requirements(owner_requirements)
    requirements = normalized.get("requirements", [])
    owner_levels: list[int] = []
    sources: list[str] = []
    for requirement in requirements:
        if str(requirement.get("domain", "")).lower() not in {"motion", "animation", "experience"}:
            continue
        if requirement.get("class") != "REQUIRED":
            continue
        level = motion_level_number(requirement.get("minimum_motion_level"))
        level = level if level is not None else motion_level_number(_extract_level_from_text(requirement.get("requirement")))
        if level is None:
            level = 3 if _MOTION_KEYWORDS_LEVEL_3.search(str(requirement.get("requirement", ""))) else None
        if level is not None:
            owner_levels.append(level)
            sources.append(requirement.get("id", ""))
    owner_required = max(owner_levels, default=None)
    heuristic = motion_level_number(heuristic_level)
    if heuristic is None:
        heuristic = 1
    selected = owner_required if owner_required is not None else heuristic
    if owner_required is not None and approved_downgrade:
        selected = heuristic
    downgrade_blocked = owner_required is not None and selected < owner_required and not approved_downgrade
    issues: list[dict[str, Any]] = []
    if downgrade_blocked:
        _append_issue(issues, "OWNER_MOTION_DOWNGRADE_BLOCKED", "selected %s is below owner-required %s" % (
            MOTION_LEVELS[selected], MOTION_LEVELS[owner_required]), blocking=True)
    return {
        "status": "FAIL" if issues else "PASS",
        "owner_required_level": MOTION_LEVELS[owner_required] if owner_required is not None else None,
        "heuristic_level": MOTION_LEVELS[heuristic],
        "recommended_level": MOTION_LEVELS[max(owner_required or 0, heuristic)],
        "execution_level": MOTION_LEVELS[selected],
        "owner_requirement_ids": sources,
        "downgrade_blocked": downgrade_blocked,
        "approved_downgrade": bool(approved_downgrade),
        "issues": issues,
    }


def _sequence_items(value: Any) -> list[dict[str, Any]]:
    items = _as_list(value)
    output: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        if isinstance(item, str):
            output.append({"sequence_id": item, "name": item, "index": index})
        elif isinstance(item, Mapping):
            row = dict(item)
            row.setdefault("sequence_id", row.get("id") or row.get("name") or "sequence-%d" % (index + 1))
            row.setdefault("index", index)
            output.append(row)
    return output


def _sequence_value(record: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        value = _read(record, key)
        if value is not None:
            return value
    return None


def _runtime_rows(runtime_evidence: Any) -> tuple[str | None, list[dict[str, Any]], bool]:
    if isinstance(runtime_evidence, Mapping):
        identity = _read(runtime_evidence, "engine_identity", "engine", "measurement_engine")
        rows = _sequence_items(_read(runtime_evidence, "motion_observations", "sequence_receipts", "sequences", "observations", default=[]))
        observed = _read(runtime_evidence, "runtime_observed", "motion_observed", default=None)
        if observed is None:
            observed = bool(rows)
        return str(identity).upper() if identity else None, rows, bool(observed)
    return None, _sequence_items(runtime_evidence), bool(runtime_evidence)


def _meaningful_runtime_change(row: Mapping[str, Any]) -> bool:
    for key in ("meaningful_state_change", "state_changed", "observed_state_change", "motion_observed"):
        if row.get(key) is True:
            return True
    for key in ("changed_properties", "changed_nodes", "state_changes", "measured_changes"):
        value = row.get(key)
        if isinstance(value, (list, tuple, dict)) and len(value) > 0:
            return True
        if isinstance(value, (int, float)) and abs(value) > 0.01:
            return True
    for key in ("max_geometry_delta", "max_opacity_delta", "max_transform_delta", "scroll_delta", "delta"):
        try:
            if abs(float(row.get(key, 0) or 0)) > 0.01:
                return True
        except (TypeError, ValueError):
            pass
    before = _sequence_value(row, "initial_state", "before", "start_state")
    after = _sequence_value(row, "settled_state", "after", "end_state")
    return before is not None and after is not None and before != after


def _motion_family(row: Mapping[str, Any]) -> str:
    family = _sequence_value(row, "family", "animation_family", "pattern", "type", "name")
    return str(family or "UNKNOWN").upper().replace(" ", "_").replace("-", "_")


def _runtime_row_map(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row.get("sequence_id") or row.get("id") or "sequence-%d" % (index + 1)): row
            for index, row in enumerate(rows)}


def validate_motion_implementation_trace(
    motion_requirement: Mapping[str, Any] | None,
    motion_brief: Mapping[str, Any] | None,
    implementation: Mapping[str, Any] | None,
    runtime_evidence: Any,
) -> dict[str, Any]:
    """Require brief-to-code-to-real-browser evidence for Level 2/3 motion."""

    motion_requirement = motion_requirement or {}
    motion_brief = motion_brief or {}
    implementation = implementation or {}
    required_level = motion_level_number(_read(motion_requirement, "owner_required_level", "minimum_motion_level", "execution_level", "level")) or 0
    promised = _sequence_items(_read(motion_brief, "required_sequences", "promised_sequences", "sequences", "segment_inventory", default=[]))
    if not promised:
        promised = _sequence_items(_read(motion_requirement, "required_sequences", "sequences", default=[]))
    implemented = _sequence_items(_read(implementation, "sequence_implementations", "implemented_sequences", "motion_sequences", "sequences", default=[]))
    identity, runtime_rows, runtime_observed = _runtime_rows(runtime_evidence)
    runtime_map = _runtime_row_map(runtime_rows)
    implementation_map = _runtime_row_map(implemented)
    issues: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []

    if required_level >= 2 and not promised:
        _append_issue(issues, "MOTION_BRIEF_SEQUENCES_MISSING", "Level 2/3 motion has no named promised sequences", blocking=True)
    for index, sequence in enumerate(promised):
        sequence_id = str(sequence.get("sequence_id") or "sequence-%d" % (index + 1))
        impl = implementation_map.get(sequence_id)
        runtime = runtime_map.get(sequence_id)
        if impl is None and index < len(implemented) and not sequence.get("sequence_id"):
            impl = implemented[index]
        if runtime is None and index < len(runtime_rows) and not sequence.get("sequence_id"):
            runtime = runtime_rows[index]
        implementation_ref = _sequence_value(impl or {}, "implementation_ref", "location", "file", "selector", "module")
        runtime_ref = _sequence_value(runtime or {}, "runtime_evidence_ref", "evidence_ref", "receipt", "sequence_id")
        trace = {"sequence_id": sequence_id, "implementation_ref": implementation_ref,
                 "runtime_evidence_ref": runtime_ref, "runtime": runtime or {},
                 "family": _motion_family(impl or sequence),
                 "meaningful_state_change": _meaningful_runtime_change(runtime or {})}
        traces.append(trace)
        if required_level >= 2 and not _nonempty(implementation_ref):
            _append_issue(issues, "MOTION_IMPLEMENTATION_TRACE_MISSING", "%s has no implementation location" % sequence_id, blocking=True)
        if required_level >= 2 and not _nonempty(runtime_ref):
            _append_issue(issues, "MOTION_RUNTIME_TRACE_MISSING", "%s has no runtime evidence reference" % sequence_id, blocking=True)

    if required_level >= 2:
        if identity != "REAL_BROWSER" or not runtime_observed:
            _append_issue(issues, "MOTION_RUNTIME_EVIDENCE_REQUIRED", "Level 2/3 motion requires runtime evidence from REAL_BROWSER", blocking=True)
        if not runtime_rows:
            _append_issue(issues, "MOTION_RUNTIME_STATE_CHANGE_MISSING", "no runtime motion sequence observations were emitted", blocking=True)
        elif not any(_meaningful_runtime_change(row) for row in runtime_rows):
            _append_issue(issues, "MOTION_RUNTIME_STATE_CHANGE_MISSING", "runtime observations show no meaningful state change")

        families = [_motion_family(row) for row in (implemented or runtime_rows)]
        if families and all(_GENERIC_MOTION_RE.search(family) for family in families):
            _append_issue(issues, "MOTION_GENERIC_FADE_DIVERSITY_REQUIRED", "all implemented motion uses generic fade/translate reveal families")
        if _read(motion_brief, "cinematic_specialist_required", "required_specialist", default=False) is True:
            invoked = _read(implementation, "cinematic_specialist_invoked", "specialist_invoked", "specialist_used", default=False)
            if invoked is not True:
                _append_issue(issues, "CINEMATIC_SPECIALIST_RUNTIME_REQUIRED", "brief requires cinematic specialist evidence but implementation does not record invocation", blocking=True)

    promised_ids = {str(item.get("sequence_id")) for item in promised}
    observed_ids = {str(item.get("sequence_id") or item.get("id")) for item in runtime_rows}
    missing_ids = sorted(promised_ids - observed_ids) if promised_ids else []
    if missing_ids and required_level >= 2:
        _append_issue(issues, "MOTION_PROMISED_SEQUENCE_MISSING", "runtime evidence is missing promised sequences: %s" % ",".join(missing_ids), blocking=True)
    return {
        "status": "FAIL" if issues else "PASS",
        "required_level": MOTION_LEVELS[required_level] if required_level in range(4) else None,
        "engine_identity": identity,
        "runtime_observed": runtime_observed,
        "promised_sequence_count": len(promised),
        "implemented_sequence_count": len(implemented),
        "runtime_sequence_count": len(runtime_rows),
        "missing_sequence_ids": missing_ids,
        "traces": traces,
        "issues": issues,
    }


def _requirement_evidence_match(requirement: Mapping[str, Any], implemented_output: Mapping[str, Any]) -> bool:
    satisfied = _read(implemented_output, "satisfied_requirements", "requirements_satisfied", default=[])
    if isinstance(satisfied, Mapping):
        return satisfied.get(requirement.get("id")) is True
    if isinstance(satisfied, (list, tuple, set)) and requirement.get("id") in satisfied:
        return True
    return False


def audit_owner_requirement_compliance(
    owner_contract: Mapping[str, Any],
    locked_decisions: Mapping[str, Any] | None,
    implemented_output: Mapping[str, Any] | None,
    runtime_evidence: Any = None,
) -> dict[str, Any]:
    """Audit every explicit required/prohibited constraint before completion."""

    locked_decisions = locked_decisions or {}
    implemented_output = implemented_output or {}
    normalized = normalize_owner_requirements(owner_contract)
    contradictions = detect_contradictions([owner_contract])
    issues: list[dict[str, Any]] = list(normalized.get("issues", []))
    statuses: list[dict[str, Any]] = []
    brand_result = None
    motion_result = None
    motion_trace = None
    current_brand = _read(owner_contract, "current_brand", "brand")
    if isinstance(current_brand, Mapping):
        brand_impl = _read(implemented_output, "brand", "colors", "tokens", default=implemented_output)
        brand_rendered = _read(runtime_evidence, "rendered", "rendered_colors", default=None) if isinstance(runtime_evidence, Mapping) else None
        brand_result = validate_brand_tokens(owner_contract, brand_impl if isinstance(brand_impl, Mapping) else {}, brand_rendered if isinstance(brand_rendered, Mapping) else None)
        issues.extend(brand_result.get("issues", []))

    motion_requirements = [item for item in normalized["requirements"] if item.get("domain") in {"motion", "animation", "experience"}]
    if motion_requirements:
        motion_result = resolve_motion_requirement(normalized, heuristic_level=_read(locked_decisions, "heuristic_motion_level", "motion_level", default="MOTION_LEVEL_1"), approved_downgrade=bool(_read(locked_decisions, "approved_motion_downgrade", default=False)))
        issues.extend(motion_result.get("issues", []))
        execution = _read(locked_decisions, "execution_motion_level", "selected_motion_level", "motion_level", default=motion_result.get("execution_level"))
        motion_requirement = {**motion_result, "execution_level": execution}
        motion_trace = validate_motion_implementation_trace(
            motion_requirement,
            _read(implemented_output, "motion_brief", "cinematic_brief", default={}) or {},
            _read(implemented_output, "motion", "motion_implementation", default=implemented_output) or {},
            runtime_evidence,
        )
        owner_level_number = motion_level_number(motion_result.get("owner_required_level"))
        execution_level_number = motion_level_number(execution)
        if (owner_level_number is not None and execution_level_number is not None
                and execution_level_number < owner_level_number):
            _append_issue(issues, "OWNER_MOTION_DOWNGRADE_BLOCKED", "implementation selected below explicit owner motion requirement", blocking=True)
        issues.extend(motion_trace.get("issues", []))

    references = _as_list(_read(implemented_output, "references", "reference_translations", default=[]))
    reference_results = [validate_reference_translation_trace(item) for item in references if isinstance(item, Mapping)]
    for result in reference_results:
        issues.extend(result.get("issues", []))

    for requirement in normalized["requirements"]:
        if requirement["class"] == "REQUIRED":
            domain = requirement["domain"]
            if domain == "brand":
                result_status = "SATISFIED" if brand_result and brand_result.get("status") == "PASS" else "BLOCKED_WITH_EXPLANATION"
                detail = "brand token audit" if result_status == "SATISFIED" else "brand evidence is missing or failed"
            elif domain in {"motion", "animation", "experience"}:
                result_status = "SATISFIED" if motion_trace and motion_trace.get("status") == "PASS" and not (motion_result or {}).get("downgrade_blocked") else "BLOCKED_WITH_EXPLANATION"
                detail = "motion brief, implementation, and runtime trace" if result_status == "SATISFIED" else "motion compliance evidence is incomplete or failed"
            elif domain in {"reference", "inspiration"}:
                result_status = "SATISFIED" if reference_results and all(item.get("status") == "PASS" for item in reference_results) else "BLOCKED_WITH_EXPLANATION"
                detail = "reference translation trace" if result_status == "SATISFIED" else "reference translation evidence is missing or failed"
            else:
                result_status = "SATISFIED" if _requirement_evidence_match(requirement, implemented_output) else "BLOCKED_WITH_EXPLANATION"
                detail = "explicit implementation receipt" if result_status == "SATISFIED" else "no explicit evidence receipt for required constraint"
            statuses.append({"id": requirement["id"], "class": requirement["class"], "status": result_status, "detail": detail})
            if result_status != "SATISFIED":
                _append_issue(issues, "REQUIRED_OWNER_CONSTRAINT_UNSATISFIED", "%s: %s" % (requirement["id"], detail), blocking=True)
        elif requirement["class"] == "PROHIBITED":
            prohibited = _read(implemented_output, "violations", "prohibited_present", default=[])
            prohibited_text = json.dumps(prohibited, sort_keys=True).lower()
            target_text = json.dumps(requirement.get("values"), sort_keys=True).lower()
            violated = requirement["id"] in prohibited if isinstance(prohibited, (list, tuple, set)) else requirement["id"].lower() in prohibited_text
            violated = violated or (target_text and target_text not in {"null", "\"\""} and target_text.strip('"') in prohibited_text)
            statuses.append({"id": requirement["id"], "class": requirement["class"], "status": "FAIL" if violated else "SATISFIED", "detail": "prohibited value present" if violated else "prohibited value not observed"})
            if violated:
                _append_issue(issues, "PROHIBITED_OWNER_CONSTRAINT_VIOLATION", requirement["id"])

    if contradictions.get("status") != "PASS":
        issues.extend(contradictions.get("issues", []))
    return {
        "OWNER_REQUIREMENT_COMPLIANCE": "PASS" if not issues else "FAIL",
        "status": "PASS" if not issues else "FAIL",
        "requirements": statuses,
        "normalized_requirements": normalized["requirements"],
        "brand": brand_result,
        "motion": motion_result,
        "motion_trace": motion_trace,
        "references": reference_results,
        "contradictions": contradictions,
        "issues": issues,
    }


def validate_owner_intent_contract(contract: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the durable owner-intent artifact shape and current authority."""

    issues: list[dict[str, Any]] = []
    if not isinstance(contract, Mapping):
        return {"status": "FAIL", "issues": [_issue("OWNER_INTENT_SHAPE", "contract must be an object", blocking=True)]}
    if str(_read(contract, "status", default="")).upper() != "CURRENT":
        _append_issue(issues, "OWNER_INTENT_CURRENT_AUTHORITY_REQUIRED", "owner-intent artifact must be marked CURRENT", blocking=True)
    if list(_read(contract, "authority_precedence", default=[])) != list(AUTHORITY_PRECEDENCE):
        _append_issue(issues, "AUTHORITY_PRECEDENCE_CONTRACT_DRIFT", "authority precedence must match the canonical eight-level ordering", blocking=True)
    normalized = normalize_owner_requirements(contract)
    issues.extend(normalized["issues"])
    current = _read(contract, "current_brand", "brand")
    if not isinstance(current, Mapping):
        _append_issue(issues, "BRAND_CONTRACT_MISSING", "current_brand is required", blocking=True)
    else:
        primary = json.dumps(_read(current, "primary", default=""), sort_keys=True).lower()
        accent = json.dumps(_read(current, "accent", default=""), sort_keys=True).lower()
        if "navy" not in primary or "blue" not in primary:
            _append_issue(issues, "ASN_PRIMARY_BRAND_AUTHORITY_INVALID", "current primary must be navy blue", blocking=True)
        if "yellow" not in accent:
            _append_issue(issues, "ASN_ACCENT_BRAND_AUTHORITY_INVALID", "current accent must be yellow", blocking=True)
    required = {item["id"] for item in normalized["requirements"] if item.get("class") == "REQUIRED"}
    if not any("brand" in item for item in required):
        _append_issue(issues, "OWNER_BRAND_REQUIREMENT_MISSING", "current owner contract must contain a required brand constraint", blocking=True)
    if not any("motion" in item for item in required):
        _append_issue(issues, "OWNER_MOTION_REQUIREMENT_MISSING", "current owner contract must contain a required motion constraint", blocking=True)
    return {"status": "PASS" if not issues else "FAIL", "issues": issues, "normalized": normalized}


def _json_key(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str)


__all__ = [
    "AUTHORITY_PRECEDENCE", "CURRENTNESS_VALUES", "MOTION_LEVELS", "REFERENCE_SIGNAL_CLASSES",
    "REQUIREMENT_CLASSES", "audit_owner_requirement_compliance", "classify_historical_brand_direction",
    "classify_reference_signal", "detect_contradictions", "motion_level_number", "normalize_owner_requirements",
    "resolve_authority_conflicts", "resolve_motion_requirement", "validate_brand_tokens",
    "validate_motion_implementation_trace", "validate_owner_intent_contract", "validate_reference_translation_trace",
]
