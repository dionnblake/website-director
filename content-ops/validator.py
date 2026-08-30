"""Deterministic Content Operations and CMS Architecture validation.

This module validates content models, editorial boundaries, CMS decisions,
publishing safety, slug continuity, rich-text safety, portability, and the
bounded integrations owned by adjacent Website Director capabilities.  It is
deliberately provider-neutral and performs no network, browser, deployment,
credential, or production write operation.

The validator returns structured ``PASS``, ``FAIL``, or ``BLOCKED`` results.
Warnings are explicit and never silently promoted to a pass for a blocked or
invalid decision.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
import re
from typing import Any, Mapping, Optional, Sequence


CMS_REQUIREMENT_CLASSES = (
    "NO_CMS_REQUIRED",
    "STATIC_STRUCTURED_CONTENT",
    "FILE_BASED_CMS",
    "HEADLESS_CMS",
    "TRADITIONAL_CMS",
    "DATABASE_BACKED_CONTENT",
    "ECOMMERCE_CATALOG",
    "APPLICATION_DATA",
    "HYBRID",
)

ARCHITECTURE_REQUIRED_CLASSES = {
    "FILE_BASED_CMS",
    "HEADLESS_CMS",
    "TRADITIONAL_CMS",
    "DATABASE_BACKED_CONTENT",
    "ECOMMERCE_CATALOG",
    "APPLICATION_DATA",
    "HYBRID",
}

CONTENT_LIFECYCLE_STATES = (
    "DRAFT",
    "IN_REVIEW",
    "APPROVED",
    "SCHEDULED",
    "PUBLISHED",
    "ARCHIVED",
)

EDITABLE_SURFACE_CLASSES = (
    "OWNER_EDITABLE",
    "EDITOR_EDITABLE",
    "ADMIN_ONLY",
    "DEVELOPER_CONTROLLED",
    "SYSTEM_GENERATED",
    "LOCKED_BRAND_ELEMENT",
)

ROLE_CAPABILITIES = (
    "CAN_EDIT",
    "CAN_REVIEW",
    "CAN_PUBLISH",
    "CAN_ARCHIVE",
    "CAN_DELETE",
)

COST_STATUSES = ("KNOWN", "UNKNOWN", "OWNER_CONFIRMATION_REQUIRED")

FIELD_TYPES = {
    "TEXT",
    "LONG_TEXT",
    "RICH_TEXT",
    "RICH_TEXT_ARRAY",
    "NUMBER",
    "BOOLEAN",
    "DATE",
    "DATETIME",
    "URL",
    "EMAIL",
    "IMAGE_REF",
    "MEDIA_REF",
    "REFERENCE",
    "REFERENCE_ARRAY",
    "ARRAY",
    "OBJECT",
    "ENUM",
    "JSON",
    "SLUG",
    "CTA",
    "MONEY",
    "IDENTIFIER",
}

PUBLIC_STATES = {"PUBLISHED"}
NON_PUBLIC_STATES = {"DRAFT", "IN_REVIEW", "APPROVED", "SCHEDULED", "ARCHIVED"}
RESERVED_ROUTES = {
    "admin",
    "api",
    "assets",
    "auth",
    "login",
    "logout",
    "_next",
    "static",
    "404",
    "500",
    "robots.txt",
    "sitemap.xml",
}

HIGH_RISK_CLAIM_TYPES = {
    "HEALTH",
    "FINANCIAL",
    "QUANTITATIVE",
    "COMPARATIVE",
    "PERFORMANCE",
    "CERTIFICATION",
    "AWARD",
    "TESTIMONIAL",
    "CUSTOMER_COUNT",
    "YEARS_IN_BUSINESS",
    "GUARANTEE",
    "AFFILIATE_PRODUCT",
}

PROTECTED_SURFACE_TERMS = (
    "analytics",
    "event_name",
    "event identifier",
    "design token",
    "design_token",
    "design_tokens",
    "structured data",
    "schema.org",
    "security header",
    "content security policy",
    "canonical lock",
    "owner lock",
    "lock state",
)

REFERENCE_ONLY_TERMS = (
    "dribbble",
    "behance",
    "landbook",
    "mobbin",
    "awwwards",
    "siteinspire",
    "pinterest",
    "screenshot_reference",
    "research_reference",
    "reference_only",
    "inspiration",
)

PRESENTATION_FIELD_PATTERNS = (
    re.compile(r"(?:^|_)(?:left|right)_(?:column|rail|panel)(?:_|$)"),
    re.compile(r"(?:^|_)(?:first|second|third|fourth|fifth)_card(?:_|$)"),
    re.compile(r"(?:^|_)hero_text_line(?:_|$)"),
    re.compile(r"(?:^|_)text_line_[0-9]+(?:_|$)"),
    re.compile(r"(?:^|_)(?:desktop|mobile)_(?:margin|padding|position|layout|offset)(?:_|$)"),
    re.compile(r"(?:^|_)(?:grid|flex)_column_[0-9]+(?:_|$)"),
    re.compile(r"(?:^|_)(?:blue|red|green|gold|black|white)_?(?:text|heading|background|border)?(?:_|$)"),
)

RICH_TEXT_BLOCK_PATTERNS = (
    re.compile(r"<\s*script\b", re.IGNORECASE),
    re.compile(r"<\s*style\b", re.IGNORECASE),
    re.compile(r"\sstyle\s*=", re.IGNORECASE),
    re.compile(r"\son[a-z]+\s*=", re.IGNORECASE),
    re.compile(r"javascript\s*:", re.IGNORECASE),
    re.compile(r"<\s*(?:iframe|object|embed|frame|form)\b", re.IGNORECASE),
    re.compile(r"<(?:font|svg)\b", re.IGNORECASE),
    re.compile(r"(?:font-size|background-color|color\s*:|--[a-z-]+\s*:)", re.IGNORECASE),
)

RICH_TEXT_UNSAFE_URL_PATTERN = re.compile(
    r"(?:href|src)\s*=\s*['\"]?\s*(?:javascript:|data:|vbscript:|file:|chrome:|about:)",
    re.IGNORECASE,
)

ALLOWED_RICH_TEXT_TAGS = {
    "p",
    "br",
    "strong",
    "em",
    "b",
    "i",
    "u",
    "s",
    "h2",
    "h3",
    "h4",
    "ul",
    "ol",
    "li",
    "blockquote",
    "a",
    "figure",
    "figcaption",
    "img",
    "mark",
}


def _get(record: Mapping[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in record:
            return record[key]
        upper = key.upper()
        if upper in record:
            return record[upper]
        lower = key.lower()
        if lower in record:
            return record[lower]
    return default


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _upper(value: Any) -> str:
    return _text(value).upper()


def _missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, dict, set)):
        return not value
    return False


def _list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _new_result() -> dict[str, Any]:
    return {
        "status": "PASS",
        "ok": True,
        "issues": [],
        "warnings": [],
        "counts": {"errors": 0, "blocked": 0, "warnings": 0},
        "unresolved_items": [],
    }


def _add(
    result: dict[str, Any],
    code: str,
    severity: str,
    message: str,
    *,
    path: Optional[str] = None,
    record_id: Optional[str] = None,
) -> None:
    issue: dict[str, Any] = {
        "code": code,
        "severity": severity,
        "message": message,
    }
    if path:
        issue["path"] = path
    if record_id:
        issue["record_id"] = record_id
    result["issues"].append(issue)
    if severity == "WARNING":
        result["warnings"].append(issue)
    if severity in {"ERROR", "BLOCKED"} and record_id and record_id not in result["unresolved_items"]:
        result["unresolved_items"].append(record_id)


def _finish(result: dict[str, Any]) -> dict[str, Any]:
    result["counts"] = {
        "errors": sum(issue["severity"] == "ERROR" for issue in result["issues"]),
        "blocked": sum(issue["severity"] == "BLOCKED" for issue in result["issues"]),
        "warnings": sum(issue["severity"] == "WARNING" for issue in result["issues"]),
    }
    if result["counts"]["errors"]:
        result["status"] = "FAIL"
    elif result["counts"]["blocked"]:
        result["status"] = "BLOCKED"
    else:
        result["status"] = "PASS"
    result["ok"] = result["status"] == "PASS"
    result["unresolved_items"] = sorted(set(result["unresolved_items"]))
    return result


def _merge(target: dict[str, Any], name: str, source: Mapping[str, Any]) -> None:
    target.setdefault("component_results", {})[name] = source
    target["issues"].extend(source.get("issues", []))
    target["warnings"].extend(source.get("warnings", []))
    target["unresolved_items"].extend(source.get("unresolved_items", []))


def _id(record: Mapping[str, Any], *keys: str, fallback: str = "") -> str:
    return _text(_get(record, *keys, default="")) or fallback


def _field_records(raw: Any) -> list[Mapping[str, Any]]:
    if isinstance(raw, list):
        return [record for record in raw if isinstance(record, Mapping)]
    if isinstance(raw, Mapping):
        records: list[Mapping[str, Any]] = []
        for key, value in raw.items():
            if isinstance(value, Mapping):
                merged = dict(value)
                merged.setdefault("field_id", key)
                records.append(merged)
            else:
                records.append({"field_id": key, "type": value})
        return records
    return []


def _record_index(records: Any, *id_keys: str) -> dict[str, Mapping[str, Any]]:
    index: dict[str, Mapping[str, Any]] = {}
    if isinstance(records, Mapping) and all(isinstance(value, Mapping) for value in records.values()):
        records = [dict(value, **{"id": key}) for key, value in records.items()]
    for position, record in enumerate(_list(records)):
        if isinstance(record, Mapping):
            key = _id(record, *id_keys, fallback=f"record[{position}]")
            if key:
                index[key] = record
    return index


def _presentation_coupled(field_id: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", "_", field_id.lower()).strip("_")
    return any(pattern.search(normalized) for pattern in PRESENTATION_FIELD_PATTERNS)


def _date_value(value: Any) -> Optional[date]:
    raw = _text(value)
    if not raw:
        return None
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        return None


def _as_of(value: Optional[str]) -> date:
    if value:
        parsed = _date_value(value)
        if parsed:
            return parsed
    return datetime.now(timezone.utc).date()


def _values_from_items(content_items: Any) -> list[tuple[Optional[str], Mapping[str, Any]]]:
    """Normalize list and type-keyed content item inputs without mutating them."""

    if content_items is None:
        return []
    if isinstance(content_items, Mapping):
        if isinstance(content_items.get("items"), list):
            return [
                (_text(_get(item, "content_type_id", "type_id", "content_type")), item)
                for item in content_items["items"]
                if isinstance(item, Mapping)
            ]
        normalized: list[tuple[Optional[str], Mapping[str, Any]]] = []
        for type_id, items in content_items.items():
            if not isinstance(items, list):
                continue
            normalized.extend(
                (str(type_id), item) for item in items if isinstance(item, Mapping)
            )
        return normalized
    return [
        (_text(_get(item, "content_type_id", "type_id", "content_type")), item)
        for item in _list(content_items)
        if isinstance(item, Mapping)
    ]


def _item_values(item: Mapping[str, Any]) -> dict[str, Any]:
    values = dict(item)
    nested = item.get("fields")
    if isinstance(nested, Mapping):
        values.update(nested)
    return values


def calculate_cms_necessity(factors: Optional[Mapping[str, Any]] = None) -> dict[str, Any]:
    """Return a bounded, explainable CMS-necessity assessment.

    The score is a prioritization aid, not a claim of mathematical objectivity.
    Explicit facts and rationale remain part of the returned record.
    """

    factors = factors if isinstance(factors, Mapping) else {}
    score = 0
    reasons: list[str] = []

    volume = _get(factors, "content_volume", "CONTENT_VOLUME", default=0)
    if isinstance(volume, (int, float)):
        if volume >= 250:
            score += 3
            reasons.append("high content volume")
        elif volume >= 50:
            score += 2
            reasons.append("moderate content volume")
    elif _upper(volume) in {"HIGH", "LARGE", "MANY"}:
        score += 3
        reasons.append("high content volume")

    frequency = _upper(_get(factors, "update_frequency", "UPDATE_FREQUENCY", default=""))
    if frequency in {"DAILY", "WEEKLY", "CONTINUOUS", "HIGH"}:
        score += 2
        reasons.append("frequent updates")
    elif frequency in {"MONTHLY", "QUARTERLY", "OCCASIONAL"}:
        score += 1
        reasons.append("recurring updates")

    editors = _get(factors, "number_of_editors", "NUMBER_OF_EDITORS", default=1)
    if isinstance(editors, (int, float)) and editors >= 3:
        score += 2
        reasons.append("multiple editors")
    elif _upper(editors) in {"MANY", "MULTIPLE", "TEAM"}:
        score += 2
        reasons.append("multiple editors")

    technical_level = _upper(_get(factors, "editor_technical_level", "EDITOR_TECHNICAL_LEVEL", default=""))
    if technical_level in {"NONTECHNICAL", "LOW", "BEGINNER", "CLIENT"}:
        score += 2
        reasons.append("nontechnical editors need a safe editing surface")

    boolean_factors = (
        ("content_relationships", "CONTENT_RELATIONSHIPS", "content relationships"),
        ("preview_requirements", "PREVIEW_REQUIREMENTS", "preview requirements"),
        ("scheduling_requirements", "SCHEDULING_REQUIREMENTS", "scheduled publishing"),
        ("multi_channel_requirements", "MULTI_CHANNEL_REQUIREMENTS", "multi-channel delivery"),
        ("localization_requirements", "LOCALIZATION_REQUIREMENTS", "localization requirements"),
        ("approval_workflow", "APPROVAL_WORKFLOW", "approval workflow"),
        ("portability_requirements", "PORTABILITY_REQUIREMENTS", "portability requirements"),
    )
    for key, uppercase, reason in boolean_factors:
        value = _get(factors, key, uppercase, default=False)
        if value is True or _upper(value) in {"REQUIRED", "HIGH", "YES", "MANY"}:
            score += 2
            reasons.append(reason)

    for key, uppercase, reason in (
        ("seo_editability", "SEO_EDITABILITY", "editorial SEO control"),
        ("media_volume", "MEDIA_VOLUME", "media management"),
    ):
        value = _get(factors, key, uppercase, default=False)
        if value is True or _upper(value) in {"REQUIRED", "HIGH", "LARGE", "YES"}:
            score += 1
            reasons.append(reason)

    if score >= 6:
        cms_required = True
        explicit_class = _upper(_get(factors, "cms_class", "cms_requirement", default=""))
        if explicit_class in CMS_REQUIREMENT_CLASSES and explicit_class not in {"NO_CMS_REQUIRED", "STATIC_STRUCTURED_CONTENT"}:
            requirement = explicit_class
        elif _get(factors, "multi_channel_requirements", "MULTI_CHANNEL_REQUIREMENTS", default=False) is True:
            requirement = "HEADLESS_CMS"
        elif _get(factors, "content_relationships", "CONTENT_RELATIONSHIPS", default=False) is True:
            requirement = "DATABASE_BACKED_CONTENT"
        else:
            requirement = "TRADITIONAL_CMS"
    elif score >= 2:
        cms_required = False
        requirement = "STATIC_STRUCTURED_CONTENT"
    else:
        cms_required = False
        requirement = "NO_CMS_REQUIRED"

    if not reasons:
        reasons.append("small, infrequently changed content surface")
    return {
        "cms_required": cms_required,
        "cms_requirement": requirement,
        "class": requirement,
        "score": score,
        "thresholds": {
            "no_cms_required": "0-1 bounded pressure points",
            "static_structured_content": "2-5 bounded pressure points",
            "cms_required": "6 or more bounded pressure points",
        },
        "confidence": "bounded_assessment_requires_owner_review",
        "rationale": reasons,
        "factors": dict(factors),
    }


assess_cms_necessity = calculate_cms_necessity
evaluate_cms_necessity = calculate_cms_necessity
classify_cms_requirement = calculate_cms_necessity


def validate_cms_decision(
    decision: Optional[Mapping[str, Any]],
    factors: Optional[Mapping[str, Any]] = None,
) -> dict[str, Any]:
    result = _new_result()
    if not isinstance(decision, Mapping):
        _add(result, "CMS_DECISION_MISSING", "BLOCKED", "CMS decision record is required before content operations can be ready")
        return _finish(result)

    requirement = _upper(_get(decision, "cms_requirement", "CMS_REQUIREMENT", "cms_class", "CMS_CLASS"))
    if requirement not in CMS_REQUIREMENT_CLASSES:
        _add(result, "CMS_REQUIREMENT_INVALID", "ERROR", "CMS requirement must use the bounded classification taxonomy", path="cms_requirement")

    provider_status = _upper(_get(decision, "provider_status", "availability", "status", default=""))
    if provider_status in {"UNAVAILABLE", "UNREACHABLE", "NOT_CONFIGURED"}:
        _add(result, "CMS_PROVIDER_UNAVAILABLE", "BLOCKED", "selected CMS/provider is unavailable or not configured", path="provider_status")

    cms_required = _get(decision, "cms_required", default=None)
    if cms_required is not None and not isinstance(cms_required, bool):
        _add(result, "CMS_REQUIRED_TYPE", "ERROR", "cms_required must be boolean", path="cms_required")
    if cms_required is True and requirement in {"NO_CMS_REQUIRED", "STATIC_STRUCTURED_CONTENT"}:
        _add(result, "CMS_REQUIREMENT_CONFLICT", "ERROR", "decision marks a CMS as required but selects a no-provider/static class", path="cms_requirement")
    if cms_required is False and requirement in ARCHITECTURE_REQUIRED_CLASSES:
        _add(result, "CMS_REQUIREMENT_CONFLICT", "ERROR", "decision selects a provider-backed class while marking CMS as not required", path="cms_required")

    selected = _get(decision, "selected_provider", "selected_architecture", "SELECTED_PROVIDER")
    if (cms_required is True or requirement in ARCHITECTURE_REQUIRED_CLASSES) and _missing(selected):
        _add(result, "CMS_ARCHITECTURE_UNSELECTED", "BLOCKED", "a required CMS architecture/provider decision is unresolved", path="selected_provider")

    candidates = _get(decision, "candidates", "CANDIDATES", default=[])
    if candidates is not None and not isinstance(candidates, list):
        _add(result, "CMS_CANDIDATES_SHAPE", "ERROR", "CMS candidates must be an array", path="candidates")

    if requirement == "STATIC_STRUCTURED_CONTENT":
        storage = _get(decision, "storage", "content_source", default={})
        storage_format = _upper(storage.get("format") if isinstance(storage, Mapping) else storage)
        if storage_format and storage_format not in {"MARKDOWN", "MD", "MDX", "JSON", "YAML", "TYPED_FILES", "TYPED"}:
            _add(result, "STATIC_CONTENT_FORMAT_INVALID", "ERROR", "static structured content must use a portable Markdown, MDX, JSON, YAML, or typed-file source", path="storage.format")

    cost_model = _get(decision, "cost_model", "COST_MODEL", default={})
    if requirement in ARCHITECTURE_REQUIRED_CLASSES and _missing(cost_model):
        _add(result, "CMS_COST_STATUS_UNRESOLVED", "BLOCKED", "provider-backed content operations require an explicit cost status", path="cost_model")
    if isinstance(cost_model, Mapping):
        for key, value in cost_model.items():
            status = _upper(value.get("status") if isinstance(value, Mapping) else value)
            if status and status not in COST_STATUSES:
                _add(result, "CMS_COST_STATUS_INVALID", "ERROR", "CMS cost status must be KNOWN, UNKNOWN, or OWNER_CONFIRMATION_REQUIRED", path=f"cost_model.{key}")
    elif not _missing(cost_model) and _upper(cost_model) not in COST_STATUSES:
        _add(result, "CMS_COST_STATUS_INVALID", "ERROR", "CMS cost status must be KNOWN, UNKNOWN, or OWNER_CONFIRMATION_REQUIRED", path="cost_model")

    export_capability = _get(decision, "export_capability", "EXPORT_CAPABILITY", default=None)
    lock_in_risk = _upper(_get(decision, "lock_in_risk", "LOCK_IN_RISK", default=""))
    acceptance = _get(decision, "lock_in_acceptance", "owner_acceptance", default=None)
    if export_capability is False or lock_in_risk in {"HIGH", "PROPRIETARY", "VENDOR_LOCK_IN"}:
        if not isinstance(acceptance, Mapping) or not _text(_get(acceptance, "reason", "note")):
            _add(result, "CMS_EXPORT_UNAVAILABLE", "WARNING", "provider portability is limited; record explicit owner acceptance and an exit plan", path="export_capability")

    if factors is not None:
        assessment = calculate_cms_necessity(factors)
        result["necessity_assessment"] = assessment
        if requirement == "NO_CMS_REQUIRED" and assessment["cms_required"]:
            _add(result, "CMS_DECISION_UNDERBUILT", "BLOCKED", "bounded necessity factors indicate a CMS is required but the decision says no CMS")
        if requirement not in CMS_REQUIREMENT_CLASSES:
            result["necessity_assessment"] = assessment
    return _finish(result)


def validate_editable_surfaces(surfaces: Any) -> dict[str, Any]:
    result = _new_result()
    if isinstance(surfaces, Mapping):
        surfaces = _get(surfaces, "editable_surfaces", "surfaces", default=[])
    if surfaces is None:
        return _finish(result)
    if not isinstance(surfaces, list):
        _add(result, "EDITABLE_SURFACES_SHAPE", "ERROR", "editable surfaces must be an array", path="editable_surfaces")
        return _finish(result)

    seen: set[str] = set()
    for position, surface in enumerate(surfaces):
        fallback = f"surface[{position}]"
        if not isinstance(surface, Mapping):
            _add(result, "EDITABLE_SURFACE_SHAPE", "ERROR", "editable surface must be an object", path=fallback)
            continue
        surface_id = _id(surface, "surface_id", "id", fallback=fallback)
        if surface_id in seen:
            _add(result, "DUPLICATE_EDITABLE_SURFACE", "ERROR", "editable surface identifier is duplicated", record_id=surface_id)
        seen.add(surface_id)
        classification = _upper(_get(surface, "classification", "surface_class"))
        if classification not in EDITABLE_SURFACE_CLASSES:
            _add(result, "EDITABLE_SURFACE_CLASS_INVALID", "ERROR", "editable surface classification is outside the controlled taxonomy", record_id=surface_id)
        editable_by = _list(_get(surface, "editable_by", "roles", default=[]))
        operations = _list(_get(surface, "operations", default=[]))
        searchable = " ".join(str(value) for value in (
            surface_id,
            _get(surface, "label", default=""),
            _get(surface, "field_id", default=""),
            _get(surface, "protected_concept", default=""),
        )).lower()
        protected = any(term in searchable for term in PROTECTED_SURFACE_TERMS)
        editable = bool(_get(surface, "editable", default=bool(editable_by)))
        if protected and editable:
            _add(result, "PROTECTED_SURFACE_EDITABLE", "ERROR", "analytics, structured data, security, design-token, and lock controls cannot be editor-editable", record_id=surface_id)
        if classification in {"DEVELOPER_CONTROLLED", "SYSTEM_GENERATED", "LOCKED_BRAND_ELEMENT", "ADMIN_ONLY"} and editable_by:
            if classification != "ADMIN_ONLY" or any(_upper(role) in {"EDITOR", "AUTHOR", "CLIENT", "CONTENT_EDITOR"} for role in editable_by):
                _add(result, "EDITABLE_SURFACE_BOUNDARY_BREACH", "ERROR", "surface role permissions exceed its declared protection class", record_id=surface_id)
        if "CAN_PUBLISH" in {_upper(operation) for operation in operations} and classification not in {"OWNER_EDITABLE", "EDITOR_EDITABLE"}:
            _add(result, "SURFACE_PUBLISH_OPERATION_INVALID", "ERROR", "publishing is a role capability, not a control-surface edit operation", record_id=surface_id)
    return _finish(result)


def validate_roles_permissions(roles: Any, *, publishing_required: bool = False) -> dict[str, Any]:
    result = _new_result()
    if isinstance(roles, Mapping):
        roles = _get(roles, "roles", "permissions", default=[])
    if roles is None:
        roles = []
    if not isinstance(roles, list):
        _add(result, "ROLES_SHAPE", "ERROR", "roles must be an array", path="roles")
        return _finish(result)
    has_publisher = False
    for position, role in enumerate(roles):
        if not isinstance(role, Mapping):
            _add(result, "ROLE_SHAPE", "ERROR", "role must be an object", path=f"roles[{position}]")
            continue
        role_id = _id(role, "role_id", "id", "name", fallback=f"role[{position}]")
        capabilities = {_upper(capability) for capability in _list(_get(role, "capabilities", "permissions", default=[]))}
        invalid = sorted(capabilities - set(ROLE_CAPABILITIES))
        if invalid:
            _add(result, "ROLE_CAPABILITY_INVALID", "ERROR", f"role contains unsupported capability values: {invalid}", record_id=role_id)
        if "CAN_PUBLISH" in capabilities:
            has_publisher = True
            if any(term in role_id.lower() for term in ("agent", "bot", "model", "automation")) or _upper(_get(role, "actor_type", "principal_type", default="")) == "AGENT":
                _add(result, "AGENT_PUBLISHING_FORBIDDEN", "ERROR", "agents may draft content but may not hold autonomous publishing authority", record_id=role_id)
    if publishing_required and not has_publisher:
        _add(result, "PUBLISH_AUTHORITY_MISSING", "BLOCKED", "a publishing workflow requires an explicit human or owner CAN_PUBLISH role", path="roles")
    return _finish(result)


def validate_content_lifecycle(lifecycle: Any, roles: Any = None) -> dict[str, Any]:
    result = _new_result()
    if isinstance(lifecycle, Mapping):
        states = _get(lifecycle, "states", "EDITORIAL_STATUS", "editorial_status", default=[])
        transitions = _get(lifecycle, "transitions", default=[])
    else:
        states = lifecycle
        transitions = []
    states_list = [_upper(state) for state in _list(states)]
    if not states_list:
        states_list = ["DRAFT", "PUBLISHED"]
    invalid = sorted(set(states_list) - set(CONTENT_LIFECYCLE_STATES))
    if invalid:
        _add(result, "LIFECYCLE_STATE_INVALID", "ERROR", f"lifecycle contains unsupported states: {invalid}", path="lifecycle.states")
    if len(states_list) != len(set(states_list)):
        _add(result, "DUPLICATE_LIFECYCLE_STATE", "ERROR", "lifecycle states must be unique", path="lifecycle.states")
    for position, transition in enumerate(_list(transitions)):
        if not isinstance(transition, Mapping):
            _add(result, "LIFECYCLE_TRANSITION_SHAPE", "ERROR", "lifecycle transition must be an object", path=f"lifecycle.transitions[{position}]")
            continue
        source = _upper(_get(transition, "from", "source"))
        target = _upper(_get(transition, "to", "target"))
        if source not in states_list or target not in states_list:
            _add(result, "LIFECYCLE_TRANSITION_REFERENCE", "ERROR", "lifecycle transition references an undeclared state", path=f"lifecycle.transitions[{position}]")
        if target == "PUBLISHED" and _upper(_get(transition, "authority", "required_capability", default="CAN_PUBLISH")) != "CAN_PUBLISH":
            _add(result, "PUBLISH_AUTHORITY_MISMATCH", "ERROR", "transition to PUBLISHED must require CAN_PUBLISH", path=f"lifecycle.transitions[{position}]")
    if roles is not None:
        _merge(result, "roles", validate_roles_permissions(roles, publishing_required="PUBLISHED" in states_list))
    return _finish(result)


def validate_preview(preview: Any) -> dict[str, Any]:
    result = _new_result()
    if preview is None:
        return _finish(result)
    if not isinstance(preview, Mapping):
        _add(result, "PREVIEW_SHAPE", "ERROR", "preview contract must be an object", path="preview")
        return _finish(result)
    required = _get(preview, "required", "REQUIRED", default=False)
    if not isinstance(required, bool):
        _add(result, "PREVIEW_REQUIRED_TYPE", "ERROR", "preview.required must be boolean", path="preview.required")
    raw_json = _get(preview, "raw_json_is_preview", "RAW_JSON_IS_PREVIEW", default=False)
    if not isinstance(raw_json, bool):
        _add(result, "PREVIEW_RAW_JSON_TYPE", "ERROR", "preview.raw_json_is_preview must be boolean", path="preview.raw_json_is_preview")
    if raw_json is True:
        _add(result, "RAW_JSON_PREVIEW_FORBIDDEN", "ERROR", "a raw CMS field dump is not a visual preview", path="preview.raw_json_is_preview")
    renderer = _text(_get(preview, "renderer", "preview_renderer", "RENDERER", default=""))
    renderer_lower = renderer.lower()
    if renderer_lower in {"json", "raw", "raw_fields", "cms_fields"} or any(term in renderer_lower for term in ("raw json", "json dump", "json response", "cms field", "field dump")):
        _add(result, "RAW_JSON_PREVIEW_FORBIDDEN", "ERROR", "preview must use the real route composition and design system", path="preview.renderer")
    if required is True and not renderer:
        _add(result, "PREVIEW_RENDERER_MISSING", "BLOCKED", "required preview architecture must name a route-composed renderer", path="preview.renderer")
    return _finish(result)


def validate_scheduling(scheduling: Any) -> dict[str, Any]:
    result = _new_result()
    if scheduling is None:
        return _finish(result)
    if not isinstance(scheduling, Mapping):
        _add(result, "SCHEDULING_SHAPE", "ERROR", "scheduling contract must be an object", path="scheduling")
        return _finish(result)
    required = _get(scheduling, "required", "REQUIRED", default=False)
    if not isinstance(required, bool):
        _add(result, "SCHEDULING_REQUIRED_TYPE", "ERROR", "scheduling.required must be boolean", path="scheduling.required")
    if required is True:
        for key in ("SCHEDULED_AT", "TIMEZONE", "PUBLISHING_SYSTEM", "FAILURE_BEHAVIOR"):
            if _missing(_get(scheduling, key, key.lower())):
                _add(result, "SCHEDULING_FIELD_MISSING", "BLOCKED", f"required scheduling architecture must record {key}", path=f"scheduling.{key}")
    return _finish(result)


def validate_rich_text(value: Any) -> dict[str, Any]:
    result = _new_result()
    values = value if isinstance(value, list) else [value]
    for position, entry in enumerate(values):
        if isinstance(entry, Mapping):
            entry = _get(entry, "html", "value", "text", default="")
        if not isinstance(entry, str):
            _add(result, "RICH_TEXT_VALUE_TYPE", "ERROR", "rich text must be a string or string array", path=f"rich_text[{position}]")
            continue
        for pattern in RICH_TEXT_BLOCK_PATTERNS:
            if pattern.search(entry):
                _add(result, "UNSAFE_RICH_TEXT", "ERROR", "rich text contains script, inline styling, arbitrary embeds, or unsafe URL content", path=f"rich_text[{position}]")
                break
        if RICH_TEXT_UNSAFE_URL_PATTERN.search(entry):
            _add(result, "UNSAFE_RICH_TEXT_URL", "ERROR", "rich text links and media may not use executable, local-file, or data URLs", path=f"rich_text[{position}]")
        for tag in re.findall(r"<\s*/?\s*([a-zA-Z0-9-]+)", entry):
            if tag.lower() not in ALLOWED_RICH_TEXT_TAGS:
                _add(result, "RICH_TEXT_TAG_NOT_ALLOWED", "ERROR", f"rich text tag {tag!r} is outside the semantic allowlist", path=f"rich_text[{position}]")
    return _finish(result)


def _resolve_reference(reference: Any, records: Any, id_keys: Sequence[str]) -> bool:
    ref = _text(reference)
    if not ref:
        return False
    if ref in _record_index(records, *id_keys):
        return True
    for record in _list(records):
        if isinstance(record, Mapping):
            for key in ("url", "source_url", "canonical_url", "href"):
                if _text(_get(record, key)) == ref:
                    return True
    return False


def validate_media_reference(
    media: Any,
    *,
    asset_manifest: Optional[Mapping[str, Any]] = None,
    provenance_ledger: Optional[Mapping[str, Any]] = None,
    production: bool = True,
) -> dict[str, Any]:
    result = _new_result()
    records = media if isinstance(media, list) else [media]
    assets = _get(asset_manifest or {}, "assets", "records", default=[])
    provenance_records: list[Any] = []
    if isinstance(provenance_ledger, Mapping):
        for key in ("assets", "sources", "claims", "research_references"):
            provenance_records.extend(_list(provenance_ledger.get(key, [])))
    for position, record in enumerate(records):
        if isinstance(record, str):
            record = {"asset_id": record}
        if not isinstance(record, Mapping):
            _add(result, "MEDIA_REFERENCE_SHAPE", "ERROR", "media reference must be an object", path=f"media[{position}]")
            continue
        record_id = _id(record, "media_id", "asset_id", "id", fallback=f"media[{position}]")
        raw = str(record).lower()
        if production and any(term in raw for term in REFERENCE_ONLY_TERMS):
            _add(result, "REFERENCE_ASSET_NOT_PRODUCTION", "ERROR", "research or inspiration references cannot be used as production media", record_id=record_id)
        if production and _missing(_get(record, "asset_id", "ASSET_ID")):
            _add(result, "MEDIA_ASSET_ID_MISSING", "ERROR", "production media must reference an Asset Director asset identity", record_id=record_id)
        if production and _missing(_get(record, "provenance_ref", "PROVENANCE_REF", "evidence_ref")):
            _add(result, "MEDIA_PROVENANCE_MISSING", "ERROR", "production media must reference the V2.12 evidence/provenance ledger", record_id=record_id)
        asset_id = _get(record, "asset_id", "ASSET_ID")
        if production and asset_id:
            if not isinstance(asset_manifest, Mapping) or not assets or not _resolve_reference(asset_id, assets, ("asset_id", "id")):
                _add(result, "MEDIA_ASSET_UNRESOLVED", "BLOCKED", "media asset identity does not resolve to the supplied Asset Director manifest", record_id=record_id)
        provenance_ref = _get(record, "provenance_ref", "PROVENANCE_REF", "evidence_ref")
        if production and provenance_ref:
            if not isinstance(provenance_ledger, Mapping) or not provenance_records or not _resolve_reference(provenance_ref, provenance_records, ("provenance_id", "source_id", "asset_id", "id", "reference_id")):
                _add(result, "MEDIA_PROVENANCE_UNRESOLVED", "BLOCKED", "media provenance reference does not resolve to the supplied evidence ledger", record_id=record_id)
    return _finish(result)


def validate_seo_fields(fields: Any, content_items: Any = None) -> dict[str, Any]:
    result = _new_result()
    records = fields if isinstance(fields, Mapping) else {}
    canonical = _get(records, "canonical_override", "CANONICAL_OVERRIDE", default=None)
    if canonical:
        canonical_text = _text(canonical)
        if not re.match(r"^https://[^\s]+$", canonical_text):
            _add(result, "SEO_CANONICAL_INVALID", "ERROR", "canonical override must be an absolute HTTPS URL", path="canonical_override")
        if any(term in canonical_text.lower() for term in ("localhost", "127.0.0.1", "staging", "preview", "dev.")):
            _add(result, "SEO_CANONICAL_NONPRODUCTION", "ERROR", "staging, preview, and local canonicals cannot be published", path="canonical_override")
    indexability = _upper(_get(records, "indexability", "INDEXABILITY", default=""))
    if indexability and indexability not in {"INDEX", "NOINDEX", "FOLLOW", "NOFOLLOW", "INDEX_FOLLOW", "NOINDEX_FOLLOW", "NOINDEX_NOFOLLOW"}:
        _add(result, "SEO_INDEXABILITY_INVALID", "ERROR", "indexability value is outside the controlled SEO policy", path="indexability")
    if _get(records, "structured_data_editable", "STRUCTURED_DATA_EDITABLE", default=False) is True:
        _add(result, "SEO_STRUCTURED_DATA_EDITABLE", "ERROR", "structured data schema is system-controlled, not an editor free-form field", path="structured_data_editable")
    titles: dict[str, str] = {}
    for type_id, item in _values_from_items(content_items):
        title = _text(_get(item, "seo_title", "SEO_TITLE", default=""))
        if title:
            if title in titles:
                _add(result, "DUPLICATE_SEO_TITLE", "WARNING", "duplicate SEO titles require editorial review", record_id=type_id or "content_item")
            titles[title] = type_id or "content_item"
    return _finish(result)


def _slug_value(value: Any) -> str:
    raw = _text(value).strip("/").lower()
    raw = re.sub(r"\s+", "-", raw)
    return raw


def validate_slug(slug: Any, *, allow_nested: bool = True) -> dict[str, Any]:
    result = _new_result()
    raw = _slug_value(slug)
    if not raw:
        _add(result, "SLUG_MISSING", "ERROR", "published content requires a non-empty slug", path="slug")
        return _finish(result)
    if raw.startswith(("http://", "https://")) or "?" in raw or "#" in raw:
        _add(result, "SLUG_INVALID", "ERROR", "slug must be a route path, not a URL, query, or fragment", path="slug")
    segments = raw.split("/")
    if not allow_nested and len(segments) != 1:
        _add(result, "NESTED_SLUG_NOT_ALLOWED", "ERROR", "nested slug is not allowed by this route policy", path="slug")
    for segment in segments:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", segment):
            _add(result, "SLUG_FORMAT_INVALID", "ERROR", "slug segments must be lowercase kebab-case", path="slug")
        if segment in RESERVED_ROUTES:
            _add(result, "SLUG_RESERVED_ROUTE", "ERROR", "slug collides with a reserved system route", path="slug")
    return _finish(result)


def validate_slug_change(
    old_slug: Any,
    new_slug: Any,
    *,
    status: str = "PUBLISHED",
    redirects: Any = None,
) -> dict[str, Any]:
    result = _new_result()
    old_value = _slug_value(old_slug)
    new_value = _slug_value(new_slug)
    _merge(result, "new_slug", validate_slug(new_value))
    if old_value == new_value:
        return _finish(result)
    state = _upper(status)
    redirect_records = _list(redirects)
    found = False
    for redirect in redirect_records:
        if not isinstance(redirect, Mapping):
            continue
        source = _slug_value(_get(redirect, "source", "from", "old_slug"))
        destination = _slug_value(_get(redirect, "destination", "to", "new_slug"))
        code = _get(redirect, "status", "code", "http_status", default=301)
        if source == old_value and destination == new_value and str(code) == "301":
            found = True
            break
    if state not in CONTENT_LIFECYCLE_STATES:
        _add(result, "CONTENT_STATUS_INVALID", "ERROR", "slug change status is outside the editorial lifecycle", path="status")
    elif state in {"PUBLISHED", "ARCHIVED"} and not found:
        _add(result, "PUBLISHED_SLUG_REDIRECT_MISSING", "ERROR", "published or archived slug changes require a durable 301 redirect", path="redirects")
    return _finish(result)


def validate_public_visibility(status: str, *, publicly_visible: bool, listed: Optional[bool] = None) -> dict[str, Any]:
    result = _new_result()
    state = _upper(status)
    if state not in CONTENT_LIFECYCLE_STATES:
        _add(result, "CONTENT_STATUS_INVALID", "ERROR", "content status is outside the editorial lifecycle", path="status")
        return _finish(result)
    if not isinstance(publicly_visible, bool):
        _add(result, "CONTENT_VISIBILITY_TYPE", "ERROR", "publicly_visible must be boolean", path="publicly_visible")
        publicly_visible = False
    if listed is not None and not isinstance(listed, bool):
        _add(result, "CONTENT_LISTING_TYPE", "ERROR", "listed must be boolean or null", path="listed")
        listed = False
    if state in NON_PUBLIC_STATES and publicly_visible:
        _add(result, "DRAFT_PUBLIC_LEAK", "ERROR", "draft, review, scheduled, and archived content must not be publicly visible", path="publicly_visible")
    if state == "PUBLISHED" and not publicly_visible:
        _add(result, "PUBLISHED_NOT_VISIBLE", "ERROR", "published content must resolve publicly when the release surface is active", path="publicly_visible")
    if state == "ARCHIVED" and listed is True:
        _add(result, "ARCHIVED_LISTING_LEAK", "ERROR", "archived content may retain a redirect but must not remain in public listings", path="listed")
    return _finish(result)


def validate_publishing_authority(roles: Any, lifecycle: Any = None) -> dict[str, Any]:
    required = True
    if lifecycle is not None:
        lifecycle_states = lifecycle.get("states", []) if isinstance(lifecycle, Mapping) else lifecycle
        required = "PUBLISHED" in {_upper(value) for value in _list(lifecycle_states)}
    result = validate_roles_permissions(roles, publishing_required=required)
    agent_published = _get(roles if isinstance(roles, Mapping) else {}, "agent_status", default=None)
    if _upper(agent_published) == "PUBLISHED":
        _add(result, "AGENT_PUBLISHING_FORBIDDEN", "ERROR", "agent-generated content must stop at DRAFT until human review")
        _finish(result)
    return result


def validate_agent_publishing(item: Mapping[str, Any]) -> dict[str, Any]:
    result = _new_result()
    generated = _get(item, "generated_by_agent", "agent_generated", default=False) is True or _upper(_get(item, "origin", default="")) in {"AGENT", "MODEL", "AI"}
    status = _upper(_get(item, "editorial_status", "status", default=""))
    if generated and status == "PUBLISHED":
        _add(result, "AGENT_PUBLISHING_FORBIDDEN", "ERROR", "agent-generated content must enter DRAFT and human review before publication", path="status")
    if generated and status not in {"DRAFT", "IN_REVIEW", "APPROVED", "SCHEDULED", "PUBLISHED", "ARCHIVED"}:
        _add(result, "AGENT_CONTENT_STATUS_INVALID", "ERROR", "agent-generated content requires an explicit editorial lifecycle status", path="status")
    return _finish(result)


def _validate_claims(result: dict[str, Any], item: Mapping[str, Any], provenance_ledger: Optional[Mapping[str, Any]]) -> None:
    claims = _get(item, "claims", "factual_claims", default=[])
    ledger_records: list[Any] = []
    if isinstance(provenance_ledger, Mapping):
        for key in ("claims", "sources", "research_references"):
            ledger_records.extend(_list(provenance_ledger.get(key, [])))
    for position, claim in enumerate(_list(claims)):
        if not isinstance(claim, Mapping):
            _add(result, "CLAIM_SHAPE", "ERROR", "claim must be an object", path=f"claims[{position}]")
            continue
        claim_id = _id(claim, "claim_id", "id", fallback=f"claim[{position}]")
        claim_type = _upper(_get(claim, "claim_type", "type", default=""))
        high_risk = claim_type in HIGH_RISK_CLAIM_TYPES or _get(claim, "high_risk", default=False) is True
        reference = _get(claim, "provenance_ref", "evidence_ref", "source_ref", "claim_evidence")
        if high_risk and _missing(reference):
            _add(result, "CLAIM_PROVENANCE_REQUIRED", "ERROR", "high-risk factual content cannot publish without a V2.12 evidence/provenance reference", record_id=claim_id)
        if reference and (high_risk or ledger_records):
            if not isinstance(provenance_ledger, Mapping) or not ledger_records or not _resolve_reference(reference, ledger_records, ("claim_id", "source_id", "provenance_id", "reference_id", "id")):
                _add(result, "CLAIM_PROVENANCE_UNRESOLVED", "BLOCKED", "claim provenance reference does not resolve to the supplied evidence ledger", record_id=claim_id)


def _validate_affiliate_and_freshness(result: dict[str, Any], item: Mapping[str, Any], as_of: date) -> None:
    affiliate = _get(item, "affiliate", "is_affiliate", default=False) is True
    if affiliate:
        for key in ("merchant", "product", "affiliate_url", "disclosure_requirement", "claim_evidence", "last_verified"):
            if _missing(_get(item, key)):
                _add(result, "AFFILIATE_FIELD_MISSING", "ERROR", f"affiliate content requires {key}", path=key)
        if _get(item, "click_is_sale", default=False) is True:
            _add(result, "AFFILIATE_ATTRIBUTION_OVERCLAIM", "ERROR", "a click must not be represented as a sale without downstream evidence", path="click_is_sale")
    time_sensitive = _get(item, "time_sensitive", "requires_freshness", default=False) is True
    if time_sensitive:
        for key in ("last_verified_at", "review_due_at"):
            if _date_value(_get(item, key)) is None:
                _add(result, "FRESHNESS_DATE_MISSING", "ERROR", f"time-sensitive content requires a valid {key}", path=key)
        expires = _date_value(_get(item, "expires_at"))
        if expires and expires < as_of:
            _add(result, "CONTENT_EXPIRED", "ERROR", "time-sensitive content is past its recorded expiration date", path="expires_at")


def _validate_migrations(result: dict[str, Any], migration: Any) -> None:
    if migration is None:
        return
    records = _list(migration.get("inventory") if isinstance(migration, Mapping) else migration)
    for position, record in enumerate(records):
        if not isinstance(record, Mapping):
            _add(result, "MIGRATION_RECORD_SHAPE", "ERROR", "migration inventory record must be an object", path=f"migration[{position}]")
            continue
        for key in ("source_url", "source_type", "target_type", "target_slug", "migration_status", "redirect_required", "asset_refs", "provenance_refs", "seo_notes"):
            if _missing(_get(record, key, key.upper())):
                _add(result, "MIGRATION_FIELD_MISSING", "ERROR", f"migration inventory requires {key}", path=f"migration[{position}].{key}")
        redirect_required = _get(record, "redirect_required", "REDIRECT_REQUIRED", default=False)
        if not isinstance(redirect_required, bool):
            _add(result, "MIGRATION_REDIRECT_REQUIRED_TYPE", "ERROR", "migration redirect_required must be boolean", path=f"migration[{position}].redirect_required")
        if _get(record, "redirect_required", default=False) is True and _missing(_get(record, "source_url", "source")):
            _add(result, "MIGRATION_REDIRECT_SOURCE_MISSING", "ERROR", "redirect-required migration records need a source URL", path=f"migration[{position}]")


def _validate_revision_history(result: dict[str, Any], revision_history: Any) -> None:
    if revision_history is None:
        return
    if not isinstance(revision_history, Mapping):
        _add(result, "REVISION_HISTORY_SHAPE", "ERROR", "revision history contract must be an object", path="revision_history")
        return
    status = _upper(_get(revision_history, "status", "STATUS", default=""))
    if status and status not in {"VERSIONED", "NOT_REQUIRED", "PROVIDER_MANAGED", "CUSTOM_REQUIRED"}:
        _add(result, "REVISION_STATUS_INVALID", "ERROR", "revision history status is outside the controlled taxonomy", path="revision_history.status")


def _validate_archive_delete(result: dict[str, Any], policy: Any) -> None:
    if policy is None:
        return
    if not isinstance(policy, Mapping):
        _add(result, "ARCHIVE_DELETE_SHAPE", "ERROR", "archive/delete policy must be an object", path="archive_delete")
        return
    for key, code, message in (
        ("archive_distinct_from_delete", "ARCHIVE_DELETE_CONFLATED", "archive and delete must remain distinct operations"),
        ("delete_requires_inbound_link_review", "DELETE_LINK_REVIEW_MISSING", "delete policy must include inbound-link impact review"),
    ):
        value = _get(policy, key, key.upper(), default=None)
        if value is not True:
            _add(result, code, "ERROR", message, path=f"archive_delete.{key}")
    if _missing(_get(policy, "restore_policy", "RESTORE_POLICY", default=None)):
        _add(result, "RESTORE_POLICY_MISSING", "BLOCKED", "archive/delete policy must identify its restore authority", path="archive_delete.restore_policy")


def validate_content_model(
    model: Optional[Mapping[str, Any]],
    content_items: Any = None,
    redirects: Any = None,
    provenance_ledger: Optional[Mapping[str, Any]] = None,
    asset_manifest: Optional[Mapping[str, Any]] = None,
    as_of: Optional[str] = None,
) -> dict[str, Any]:
    result = _new_result()
    if not isinstance(model, Mapping):
        _add(result, "CONTENT_MODEL_MISSING", "BLOCKED", "content model is required before content operations can be ready")
        return _finish(result)

    raw_types = _get(model, "content_types", "types", "CONTENT_TYPES", default=None)
    is_template = _get(model, "template", default=False) is True
    if raw_types is None:
        _add(result, "CONTENT_TYPES_MISSING", "ERROR", "content model must declare content_types")
        raw_types = []
    if not isinstance(raw_types, list):
        _add(result, "CONTENT_TYPES_SHAPE", "ERROR", "content_types must be an array", path="content_types")
        raw_types = []
    if not raw_types and not is_template:
        _add(result, "CONTENT_TYPES_EMPTY", "WARNING", "content model has no activated content types; activate only models required by the site")

    type_index: dict[str, Mapping[str, Any]] = {}
    field_index: dict[str, dict[str, Mapping[str, Any]]] = {}
    ownership_index = _record_index(_get(model, "content_ownership", "CONTENT_OWNERSHIP", default=[]), "type_id", "TYPE_ID", "id")
    for position, content_type in enumerate(raw_types):
        fallback = f"content_types[{position}]"
        if not isinstance(content_type, Mapping):
            _add(result, "CONTENT_TYPE_SHAPE", "ERROR", "content type must be an object", path=fallback)
            continue
        type_id = _id(content_type, "type_id", "TYPE_ID", "id", fallback="")
        if not type_id:
            _add(result, "CONTENT_TYPE_ID_MISSING", "ERROR", "content type requires a durable TYPE_ID", path=fallback)
            continue
        if type_id in type_index:
            _add(result, "DUPLICATE_CONTENT_TYPE_ID", "ERROR", "content type identifier is duplicated", record_id=type_id)
        type_index[type_id] = content_type
        ownership_record = ownership_index.get(type_id, {})
        owner = _get(content_type, "content_owner", "owner", "CONTENT_OWNER", default=None)
        if _missing(owner):
            owner = _get(ownership_record, "content_owner", "owner", "CONTENT_OWNER", default=None)
        if _missing(owner):
            _add(result, "CONTENT_OWNER_MISSING", "BLOCKED", "every activated content type requires an explicit CONTENT_OWNER", record_id=type_id)
        contract_missing = object()
        for key in (
            "name",
            "purpose",
            "routes_used",
            "fields",
            "required_fields",
            "optional_fields",
            "relationships",
            "seo_fields",
            "media_fields",
            "provenance_fields",
            "editorial_status",
            "slug_policy",
            "archive_policy",
        ):
            if _get(content_type, key, key.upper(), default=contract_missing) is contract_missing:
                _add(result, "CONTENT_TYPE_CONTRACT_FIELD_MISSING", "ERROR", f"content type requires {key}", record_id=type_id)
        fields = _field_records(_get(content_type, "fields", "FIELDS", default=[]))
        field_index[type_id] = {}
        for field_position, field in enumerate(fields):
            field_id = _id(field, "field_id", "FIELD_ID", "id", fallback="")
            field_path = f"content_types[{position}].fields[{field_position}]"
            if not field_id:
                _add(result, "FIELD_ID_MISSING", "ERROR", "field requires a durable FIELD_ID", path=field_path)
                continue
            field_missing = object()
            for key in ("label", "type", "required", "validation"):
                field_keys = (key, key.upper(), "field_type") if key == "type" else (key, key.upper())
                if _get(field, *field_keys, default=field_missing) is field_missing:
                    _add(result, "FIELD_CONTRACT_FIELD_MISSING", "ERROR", f"field requires {key}", record_id=f"{type_id}.{field_id}")
            if field_id in field_index[type_id]:
                _add(result, "DUPLICATE_FIELD_ID", "ERROR", "field identifier is duplicated within its content type", record_id=f"{type_id}.{field_id}")
            field_index[type_id][field_id] = field
            if _presentation_coupled(field_id):
                _add(result, "PRESENTATION_COUPLED_FIELD", "ERROR", "content fields must describe subject meaning, not column, card, line, color, or breakpoint placement", record_id=f"{type_id}.{field_id}")
            field_type = _upper(_get(field, "type", "field_type", "TYPE", default=""))
            if field_type not in FIELD_TYPES:
                _add(result, "FIELD_TYPE_INVALID", "ERROR", "field type is outside the content contract taxonomy", record_id=f"{type_id}.{field_id}")
            required = _get(field, "required", "REQUIRED", default=False)
            if not isinstance(required, bool):
                _add(result, "FIELD_REQUIRED_TYPE", "ERROR", "field REQUIRED value must be boolean", record_id=f"{type_id}.{field_id}")
            character_limit = _get(field, "character_limit", "CHARACTER_LIMIT", default=None)
            if character_limit is not None and (not isinstance(character_limit, int) or character_limit <= 0):
                _add(result, "FIELD_CHARACTER_LIMIT_INVALID", "ERROR", "character limit must be a positive integer", record_id=f"{type_id}.{field_id}")

        required_fields = {_text(value) for value in _list(_get(content_type, "required_fields", "REQUIRED_FIELDS", default=[]))}
        optional_fields = {_text(value) for value in _list(_get(content_type, "optional_fields", "OPTIONAL_FIELDS", default=[]))}
        declared_fields = set(field_index[type_id])
        for field_id in required_fields | optional_fields:
            if field_id not in declared_fields:
                _add(result, "FIELD_REFERENCE_INVALID", "ERROR", "required/optional field reference is not declared", record_id=f"{type_id}.{field_id}")
        if required_fields & optional_fields:
            _add(result, "REQUIRED_OPTIONAL_FIELD_CONFLICT", "ERROR", "field cannot be both required and optional", record_id=type_id)
        for field_id, field in field_index[type_id].items():
            if _get(field, "required", "REQUIRED", default=False) is True and optional_fields and field_id in optional_fields:
                _add(result, "REQUIRED_OPTIONAL_FIELD_CONFLICT", "ERROR", "field marked required cannot be listed as optional", record_id=f"{type_id}.{field_id}")
            if required_fields and _get(field, "required", "REQUIRED", default=False) is True and field_id not in required_fields:
                _add(result, "REQUIRED_FIELD_UNDECLARED", "ERROR", "field marked required must appear in REQUIRED_FIELDS", record_id=f"{type_id}.{field_id}")

        for list_key in ("seo_fields", "media_fields", "provenance_fields"):
            for field_id in _list(_get(content_type, list_key, list_key.upper(), default=[])):
                if _text(field_id) not in declared_fields:
                    _add(result, "FIELD_REFERENCE_INVALID", "ERROR", f"{list_key} reference is not declared", record_id=f"{type_id}.{field_id}")

    for type_id, content_type in type_index.items():
        relationships = _list(_get(content_type, "relationships", "RELATIONSHIPS", default=[]))
        for position, relationship in enumerate(relationships):
            if isinstance(relationship, str):
                target_type = relationship
                source_field = ""
            elif isinstance(relationship, Mapping):
                target_type = _text(_get(relationship, "target_type", "TARGET_TYPE", "to_type", "type"))
                source_field = _text(_get(relationship, "field", "source_field", "FIELD_ID", default=""))
                target_field = _text(_get(relationship, "target_field", "TARGET_FIELD", default=""))
                if target_field and target_type in type_index and target_field not in field_index.get(target_type, {}):
                    _add(result, "RELATIONSHIP_FIELD_INVALID", "ERROR", "relationship target field is not declared", path=f"content_types.{type_id}.relationships[{position}]")
            else:
                _add(result, "RELATIONSHIP_SHAPE", "ERROR", "relationship must be a string or object", path=f"content_types.{type_id}.relationships[{position}]")
                continue
            if target_type not in type_index:
                _add(result, "RELATIONSHIP_TARGET_INVALID", "ERROR", "relationship points to an unknown content type", path=f"content_types.{type_id}.relationships[{position}]")
            if source_field and source_field not in field_index.get(type_id, {}):
                _add(result, "RELATIONSHIP_SOURCE_INVALID", "ERROR", "relationship source field is not declared", path=f"content_types.{type_id}.relationships[{position}]")

    taxonomies = _list(_get(model, "taxonomies", "TAXONOMIES", default=[]))
    taxonomy_ids: set[str] = set()
    for position, taxonomy in enumerate(taxonomies):
        if not isinstance(taxonomy, Mapping):
            _add(result, "TAXONOMY_SHAPE", "ERROR", "taxonomy must be an object", path=f"taxonomies[{position}]")
            continue
        taxonomy_id = _id(taxonomy, "taxonomy_id", "TAXONOMY_ID", "id", fallback=f"taxonomy[{position}]")
        if taxonomy_id in taxonomy_ids:
            _add(result, "DUPLICATE_TAXONOMY_ID", "ERROR", "taxonomy identifier is duplicated", record_id=taxonomy_id)
        taxonomy_ids.add(taxonomy_id)

    repeated = _list(_get(model, "repeated_content", "repeated_content_entries", default=[]))
    if _upper(_get(model, "content_strategy", default="")) == "HARD_CODED_INDIVIDUAL" and len(raw_types) > 1:
        _add(result, "REPEATED_CONTENT_HARD_CODED", "ERROR", "repeated content must be modeled as entities rather than individually hard-coded pages")
    for position, entry in enumerate(repeated):
        if not isinstance(entry, Mapping):
            continue
        mode = _upper(_get(entry, "mode", "strategy", default=""))
        count = _get(entry, "count", "instances", default=0)
        if mode in {"HARD_CODED_INDIVIDUAL", "DUPLICATED_MARKUP"} and isinstance(count, (int, float)) and count > 1:
            _add(result, "REPEATED_CONTENT_HARD_CODED", "ERROR", "repeated content must be modeled as entities rather than individually hard-coded pages", path=f"repeated_content[{position}]")

    _merge(result, "editable_surfaces", validate_editable_surfaces(_get(model, "editable_surfaces", default=[])))
    lifecycle = _get(model, "lifecycle", "editorial_lifecycle", default={})
    _merge(result, "lifecycle", validate_content_lifecycle(lifecycle, _get(model, "roles", default=[])))
    preview = _get(model, "preview", default=None)
    _merge(result, "preview", validate_preview(preview))
    scheduling = _get(model, "scheduling", default=None)
    scheduling_result = validate_scheduling(scheduling)
    lifecycle_states = lifecycle.get("states", []) if isinstance(lifecycle, Mapping) else lifecycle
    if "SCHEDULED" in {_upper(value) for value in _list(lifecycle_states)} and not (
        isinstance(scheduling, Mapping) and _get(scheduling, "required", "REQUIRED", default=False) is True
    ):
        _add(scheduling_result, "SCHEDULING_CONTRACT_REQUIRED", "BLOCKED", "a lifecycle containing SCHEDULED requires an explicit scheduling contract", path="scheduling")
    _merge(result, "scheduling", scheduling_result)
    _merge(result, "seo", validate_seo_fields(_get(model, "seo", default={}), content_items))
    _validate_migrations(result, _get(model, "migration", "migration_inventory", default=None))
    _validate_revision_history(result, _get(model, "revision_history", "REVISION_HISTORY", default=None))
    _validate_archive_delete(result, _get(model, "archive_delete", "ARCHIVE_DELETE", default=None))

    portability = _get(model, "portability", default={})
    if isinstance(portability, Mapping):
        for key in ("export_format", "media_export", "relationship_export", "slug_export", "provenance_export"):
            if _missing(_get(portability, key, key.upper())):
                _add(result, "PORTABILITY_FIELD_MISSING", "ERROR", f"portability contract requires {key}", path=f"portability.{key}")

    if content_items is not None:
        seen_slugs: dict[str, str] = {}
        for position, (hint_type_id, item) in enumerate(_values_from_items(content_items)):
            type_id = hint_type_id or _text(_get(item, "content_type_id", "type_id", "content_type"))
            if type_id not in type_index:
                _add(result, "CONTENT_ITEM_TYPE_INVALID", "ERROR", "content item references an unknown content type", path=f"content_items[{position}]")
                continue
            values = _item_values(item)
            known_meta = {"id", "content_type_id", "type_id", "content_type", "fields", "status", "editorial_status", "publicly_visible", "listed", "generated_by_agent", "agent_generated", "origin", "affiliate", "is_affiliate", "time_sensitive", "requires_freshness", "claims", "factual_claims", "seo_title", "SEO_TITLE"}
            for field_id, field in field_index[type_id].items():
                if _get(field, "required", "REQUIRED", default=False) is True and _missing(values.get(field_id)):
                    _add(result, "REQUIRED_CONTENT_FIELD_MISSING", "ERROR", "content item is missing a required field", path=f"content_items[{position}].{field_id}")
                if field_id in values:
                    field_type = _upper(_get(field, "type", "field_type", default=""))
                    if field_type in {"RICH_TEXT", "RICH_TEXT_ARRAY"}:
                        _merge(result, f"rich_text_{position}_{field_id}", validate_rich_text(values[field_id]))
                    if field_type in {"IMAGE_REF", "MEDIA_REF"}:
                        _merge(result, f"media_{position}_{field_id}", validate_media_reference(values[field_id], asset_manifest=asset_manifest, provenance_ledger=provenance_ledger))
                    if field_type == "SLUG":
                        slug_result = validate_slug(values[field_id])
                        _merge(result, f"slug_{position}_{field_id}", slug_result)
                        slug = _slug_value(values[field_id])
                        if slug in seen_slugs:
                            _add(result, "DUPLICATE_PUBLISHED_SLUG", "ERROR", "published content slugs must be unique", path=f"content_items[{position}].{field_id}")
                        seen_slugs[slug] = f"content_items[{position}]"
            state = _upper(_get(item, "editorial_status", "status", default="DRAFT"))
            visible = _get(item, "publicly_visible", default=state == "PUBLISHED")
            listed = _get(item, "listed", default=state == "PUBLISHED")
            _merge(result, f"visibility_{position}", validate_public_visibility(state, publicly_visible=visible, listed=listed))
            _merge(result, f"agent_{position}", validate_agent_publishing(item))
            _validate_claims(result, item, provenance_ledger)
            _validate_affiliate_and_freshness(result, item, _as_of(as_of))

    if redirects is not None:
        result["redirects_reviewed"] = len(_list(redirects))
    return _finish(result)


validate_content_model_contract = validate_content_model


def validate_content_item(
    item: Mapping[str, Any],
    content_type: Mapping[str, Any],
    *,
    redirects: Any = None,
    provenance_ledger: Optional[Mapping[str, Any]] = None,
    asset_manifest: Optional[Mapping[str, Any]] = None,
) -> dict[str, Any]:
    type_id = _id(content_type, "type_id", "TYPE_ID", "id", fallback="content")
    item_copy = dict(item)
    item_copy.setdefault("content_type_id", type_id)
    return validate_content_model(
        {"content_types": [content_type], "template": False, "portability": {
            "export_format": "JSON",
            "media_export": "ASSET_ID",
            "relationship_export": "TYPE_ID",
            "slug_export": "SOURCE_AND_TARGET",
            "provenance_export": "PROVENANCE_REF",
        }},
        [item_copy],
        redirects=redirects,
        provenance_ledger=provenance_ledger,
        asset_manifest=asset_manifest,
    )


def validate_content_ops_state(state: Optional[Mapping[str, Any]]) -> dict[str, Any]:
    result = _new_result()
    if not isinstance(state, Mapping):
        _add(result, "CONTENT_OPS_STATE_MISSING", "BLOCKED", "content_ops state is required for the readiness gate")
        return _finish(result)
    for key in state:
        if str(key).lower().endswith("_locked"):
            _add(result, "CONTENT_OPS_LOCK_FORBIDDEN", "ERROR", "content operations readiness must not create a sixth owner lock", path=str(key))
    for key in ("complete", "content_model_ready", "editable_surfaces_defined", "editorial_workflow_defined", "publishing_authority_defined", "slug_policy_defined", "portability_reviewed", "migration_required"):
        if key in state and not isinstance(state[key], bool):
            _add(result, "CONTENT_OPS_STATE_BOOLEAN", "ERROR", f"content_ops.{key} must be boolean", path=key)
    requirement = _upper(state.get("cms_requirement", ""))
    if requirement and requirement != "UNASSESSED" and requirement not in CMS_REQUIREMENT_CLASSES:
        _add(result, "CONTENT_OPS_REQUIREMENT_INVALID", "ERROR", "content_ops.cms_requirement is outside the bounded classification taxonomy", path="cms_requirement")
    complete = state.get("complete") is True
    if complete:
        required_true = ("content_model_ready", "editable_surfaces_defined", "editorial_workflow_defined", "publishing_authority_defined", "slug_policy_defined", "portability_reviewed")
        missing = [key for key in required_true if state.get(key) is not True]
        if missing:
            _add(result, "CONTENT_OPS_INCOMPLETE", "BLOCKED", f"content operations cannot be complete while required checks are false: {missing}")
        if requirement in {"", "UNASSESSED"}:
            _add(result, "CONTENT_OPS_REQUIREMENT_UNASSESSED", "BLOCKED", "content operations cannot be complete with an unassessed CMS requirement")
        if _missing(state.get("selected_architecture")) and requirement not in {"NO_CMS_REQUIRED", "STATIC_STRUCTURED_CONTENT"}:
            _add(result, "CONTENT_OPS_ARCHITECTURE_MISSING", "BLOCKED", "provider-backed content operations require a selected architecture")
    exception = state.get("exception")
    if exception is not None:
        if not isinstance(exception, Mapping) or not isinstance(exception.get("applied"), bool):
            _add(result, "CONTENT_OPS_EXCEPTION_INVALID", "ERROR", "content operations exception requires a boolean applied value", path="exception")
        elif exception.get("applied") is True and not _text(exception.get("reason")):
            _add(result, "CONTENT_OPS_EXCEPTION_INVALID", "ERROR", "an applied content operations exception requires a durable reason", path="exception")
        elif exception.get("applied") is False and _text(exception.get("reason")):
            _add(result, "CONTENT_OPS_EXCEPTION_INVALID", "ERROR", "a non-applied content operations exception must not retain a reason", path="exception")
    if requirement == "UNASSESSED" and _text(state.get("blocked_reason")):
        _add(result, "CONTENT_OPS_BLOCK_REASON_WITHOUT_CLASS", "ERROR", "blocked_reason requires a concrete CMS requirement or blocked provider decision")
    if _text(state.get("blocked_reason")) and complete:
        _add(result, "CONTENT_OPS_BLOCKED_COMPLETE_CONFLICT", "ERROR", "complete content operations state cannot retain a blocked_reason")
    return _finish(result)


validate_content_state = validate_content_ops_state


def validate_relationships(model: Mapping[str, Any]) -> dict[str, Any]:
    result = validate_content_model(model)
    return result


def validate_content_operations(
    content_model: Optional[Mapping[str, Any]] = None,
    cms_decision: Optional[Mapping[str, Any]] = None,
    state: Optional[Mapping[str, Any]] = None,
    content_items: Any = None,
    redirects: Any = None,
    provenance_ledger: Optional[Mapping[str, Any]] = None,
    asset_manifest: Optional[Mapping[str, Any]] = None,
    factors: Optional[Mapping[str, Any]] = None,
    as_of: Optional[str] = None,
) -> dict[str, Any]:
    """Validate the bounded Capability #8 contract as one report."""

    result = _new_result()
    result["component_results"] = {}
    if cms_decision is not None:
        _merge(result, "cms_decision", validate_cms_decision(cms_decision, factors=factors))
    elif factors is not None:
        result["necessity_assessment"] = calculate_cms_necessity(factors)
    if content_model is not None:
        _merge(result, "content_model", validate_content_model(
            content_model,
            content_items=content_items,
            redirects=redirects,
            provenance_ledger=provenance_ledger,
            asset_manifest=asset_manifest,
            as_of=as_of,
        ))
    elif content_items is not None:
        _add(result, "CONTENT_MODEL_MISSING", "BLOCKED", "content items cannot be validated without their content model")
    if state is not None:
        _merge(result, "content_ops_state", validate_content_ops_state(state))
        if state.get("complete") is True:
            if content_model is None:
                _add(result, "CONTENT_MODEL_MISSING", "BLOCKED", "content operations cannot be complete without a content model")
            elif _get(content_model, "template", default=False) is True:
                _add(result, "CONTENT_MODEL_TEMPLATE_UNACTIVATED", "BLOCKED", "a reusable template cannot certify an activated content model")
            if cms_decision is None:
                _add(result, "CMS_DECISION_MISSING", "BLOCKED", "content operations cannot be complete without a CMS decision record")
            elif isinstance(content_model, Mapping):
                model_requirement = _upper(_get(content_model, "cms_requirement", "CMS_REQUIREMENT", default=""))
                decision_requirement = _upper(_get(cms_decision, "cms_requirement", "CMS_REQUIREMENT", "cms_class", "CMS_CLASS", default=""))
                if model_requirement and decision_requirement and model_requirement != decision_requirement:
                    _add(result, "CMS_REQUIREMENT_MISMATCH", "ERROR", "content model and CMS decision records must use the same requirement class")
            if state.get("migration_required") is True and isinstance(content_model, Mapping) and _missing(_get(content_model, "migration", "migration_inventory")):
                _add(result, "MIGRATION_CONTRACT_MISSING", "BLOCKED", "content operations marked migration_required must carry a migration inventory")
    if redirects is not None and content_model is None:
        result["redirects_reviewed"] = len(_list(redirects))
    return _finish(result)


validate_content_ops = validate_content_operations


__all__ = [
    "ALLOWED_RICH_TEXT_TAGS",
    "ARCHITECTURE_REQUIRED_CLASSES",
    "CMS_REQUIREMENT_CLASSES",
    "CONTENT_LIFECYCLE_STATES",
    "COST_STATUSES",
    "EDITABLE_SURFACE_CLASSES",
    "FIELD_TYPES",
    "ROLE_CAPABILITIES",
    "assess_cms_necessity",
    "calculate_cms_necessity",
    "classify_cms_requirement",
    "evaluate_cms_necessity",
    "validate_agent_publishing",
    "validate_content_item",
    "validate_content_lifecycle",
    "validate_content_model",
    "validate_content_model_contract",
    "validate_content_operations",
    "validate_content_ops",
    "validate_content_ops_state",
    "validate_content_state",
    "validate_cms_decision",
    "validate_editable_surfaces",
    "validate_media_reference",
    "validate_public_visibility",
    "validate_publishing_authority",
    "validate_relationships",
    "validate_rich_text",
    "validate_roles_permissions",
    "validate_seo_fields",
    "validate_preview",
    "validate_scheduling",
    "validate_slug",
    "validate_slug_change",
]
