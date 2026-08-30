"""Deterministic evidence and asset provenance validation.

This module validates recorded identity, evidence references, usage boundaries,
attribution requirements, and release-state claims. It does not decide legal
ownership or grant copyright, exclusivity, or compliance status. Production is
the default mode and is intentionally fail-closed when required evidence is
missing, stale, ambiguous, or inconsistent.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Mapping, Optional


RISK_LEVELS = (
    "LOW",
    "MODERATE",
    "HIGH",
    "SPECIALIST_REVIEW_REQUIRED",
)

ASSET_ORIGINS = (
    "OWNER_PROVIDED",
    "CLIENT_PROVIDED",
    "ORIGINAL_CREATED",
    "AI_GENERATED",
    "LICENSED_STOCK",
    "OPEN_LICENSE",
    "PUBLIC_DOMAIN",
    "COMMISSIONED",
    "THIRD_PARTY_BRAND",
    "SCREENSHOT_REFERENCE",
    "RESEARCH_REFERENCE",
    "UNKNOWN",
)

CLAIM_TYPES = (
    "FACTUAL",
    "QUANTITATIVE",
    "COMPARATIVE",
    "PERFORMANCE",
    "HEALTH",
    "FINANCIAL",
    "CERTIFICATION",
    "AWARD",
    "TESTIMONIAL",
    "CUSTOMER_COUNT",
    "YEARS_IN_BUSINESS",
    "LOCATION",
    "PRODUCT_FEATURE",
    "AFFILIATE_PRODUCT",
    "GUARANTEE",
)

EVIDENCE_STRENGTH = (
    "PRIMARY_SOURCE",
    "AUTHORITATIVE_SECONDARY",
    "REPUTABLE_SECONDARY",
    "OWNER_ATTESTED",
    "CUSTOMER_ATTESTED",
    "INTERNAL_RECORD",
    "RESEARCH_REFERENCE",
    "UNVERIFIED",
)

CLAIM_STATUSES = (
    "SUPPORTED",
    "PARTIALLY_SUPPORTED",
    "UNVERIFIED",
    "CONTRADICTED",
    "EXPIRED",
    "OWNER_ATTESTED",
    "REVIEW_REQUIRED",
    "PROHIBITED",
)

CERTIFICATION_RELEASE_STATUSES = {
    "ACTIVE",
    "CURRENT",
    "VALID",
    "VERIFIED",
    "ISSUED",
    "RENEWED",
}

CERTIFICATION_BLOCKED_STATUSES = {
    "REVOKED",
    "EXPIRED",
    "SUSPENDED",
    "UNVERIFIED",
    "REVIEW_REQUIRED",
    "UNKNOWN",
    "INACTIVE",
    "LAPSED",
    "WITHDRAWN",
    "CANCELLED",
    "PROHIBITED",
}

LEDGER_SCHEMA_VERSION = "2.12.0"

FRESHNESS_REQUIRED_CLAIM_TYPES = {
    "QUANTITATIVE",
    "COMPARATIVE",
    "PERFORMANCE",
    "HEALTH",
    "FINANCIAL",
    "CERTIFICATION",
    "AWARD",
    "CUSTOMER_COUNT",
    "YEARS_IN_BUSINESS",
    "PRODUCT_FEATURE",
    "AFFILIATE_PRODUCT",
}

PROTOTYPE_STATUSES = {
    "PROTOTYPE_ONLY",
    "REFERENCE_ONLY",
    "DRAFT",
    "NOT_FOR_PRODUCTION",
}

PRODUCTION_STATUSES = {
    "PRODUCTION",
    "PRODUCTION_APPROVED",
    "PRODUCTION_READY",
    "APPROVED",
    "PUBLISHED",
}

LEGAL_ASSERTION_PATTERNS = (
    re.compile(r"\bcopyright\s+cleared\b", re.IGNORECASE),
    re.compile(r"\ball\s+rights\s+secured\b", re.IGNORECASE),
    re.compile(r"\blegally\s+verified\b", re.IGNORECASE),
    re.compile(r"\brights\s+verified\b", re.IGNORECASE),
    re.compile(r"\bexclusive\s+copyright\b", re.IGNORECASE),
    re.compile(r"\bno\s+rights\s+issues\b", re.IGNORECASE),
)

LEGAL_ASSERTION_PATTERNS += (
    re.compile(r"\btrademark\s+cleared\b", re.IGNORECASE),
    re.compile(r"\blegal(?:ly)?\s+use\s+verified\b", re.IGNORECASE),
)

ID_KEYS = (
    "provenance_id",
    "source_id",
    "claim_id",
    "asset_id",
    "testimonial_id",
    "certification_id",
    "reference_id",
    "id",
)


def _get(record: Mapping[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in record:
            return record[key]
    return default


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, dict, set)):
        return not value
    return False


def _has_any(record: Mapping[str, Any], *keys: str) -> bool:
    return any(not _missing(record.get(key)) for key in keys)


def _upper(value: Any) -> str:
    return _text(value).upper()


def _record_id(record: Mapping[str, Any], fallback: str) -> str:
    value = _get(record, *ID_KEYS)
    return _text(value) or fallback


def _new_result() -> dict[str, Any]:
    return {
        "status": "PASS",
        "ok": True,
        "issues": [],
        "counts": {
            "sources": 0,
            "claims": 0,
            "testimonials": 0,
            "certifications": 0,
            "research_references": 0,
            "assets": 0,
            "errors": 0,
            "blocked": 0,
            "warnings": 0,
        },
        "high_risk_items": [],
        "unresolved_items": [],
    }


def _add(
    result: dict[str, Any],
    code: str,
    severity: str,
    message: str,
    *,
    record_id: Optional[str] = None,
    field: Optional[str] = None,
) -> None:
    issue = {
        "code": code,
        "severity": severity,
        "message": message,
    }
    if record_id:
        issue["record_id"] = record_id
        if severity in {"ERROR", "BLOCKED"} and record_id not in result["unresolved_items"]:
            result["unresolved_items"].append(record_id)
    if field:
        issue["field"] = field
    result["issues"].append(issue)


def _finish(result: dict[str, Any]) -> dict[str, Any]:
    errors = sum(1 for issue in result["issues"] if issue["severity"] == "ERROR")
    blocked = sum(1 for issue in result["issues"] if issue["severity"] == "BLOCKED")
    warnings = sum(1 for issue in result["issues"] if issue["severity"] == "WARNING")
    result["counts"].update(errors=errors, blocked=blocked, warnings=warnings)
    if errors:
        result["status"] = "FAIL"
    elif blocked:
        result["status"] = "BLOCKED"
    else:
        result["status"] = "PASS"
    result["ok"] = result["status"] == "PASS"
    result["unresolved_items"] = sorted(set(result["unresolved_items"]))
    result["high_risk_items"] = sorted(set(result["high_risk_items"]))
    return result


def _mode(mode: str = "production", production: Optional[bool] = None) -> str:
    if production is not None:
        return "production" if production else "prototype"
    normalized = _text(mode).lower()
    if normalized in {"production", "release", "handoff"}:
        return "production"
    if normalized in {"prototype", "demo", "local-demo", "internal", "internal-demo"}:
        return "prototype"
    return "invalid"


def _is_production_record(record: Mapping[str, Any], mode: str) -> bool:
    status = _upper(_get(record, "production_status", "status", default=""))
    approved = _get(record, "production_approved", default=None)
    if status in PRODUCTION_STATUSES:
        return True
    if approved is True:
        return True
    if status in PROTOTYPE_STATUSES or approved is False:
        return False
    return mode == "production"


def _validate_status_boundary(
    result: dict[str, Any],
    record: Mapping[str, Any],
    record_id: str,
) -> None:
    status = _upper(_get(record, "production_status", "status", default=""))
    approved = _get(record, "production_approved", default=None)
    if status in PROTOTYPE_STATUSES and approved is True:
        _add(result, "PRODUCTION_STATUS_CONFLICT", "ERROR", "prototype-only status cannot be production-approved", record_id=record_id, field="production_approved")
    if status in PRODUCTION_STATUSES and approved is False:
        _add(result, "PRODUCTION_STATUS_CONFLICT", "ERROR", "production status cannot be explicitly unapproved", record_id=record_id, field="production_approved")
    exception = record.get("exception")
    if exception is not None:
        if not isinstance(exception, Mapping) or exception.get("applied") is not True or not _text(exception.get("reason")):
            _add(result, "PROTOTYPE_EXCEPTION_INVALID", "ERROR", "recorded prototype exception requires applied=true and a reason", record_id=record_id, field="exception")
        elif status not in PROTOTYPE_STATUSES:
            _add(result, "PROTOTYPE_EXCEPTION_CONFLICT", "ERROR", "an exception record must remain explicitly prototype-only", record_id=record_id, field="production_status")


def _today(as_of: Optional[str]) -> date:
    if as_of:
        return date.fromisoformat(as_of[:10])
    return datetime.now(timezone.utc).date()


def _date_value(value: Any) -> Optional[date]:
    raw = _text(value)
    if not raw:
        return None
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        return None


def _normal_hash(value: Any) -> Optional[str]:
    raw = _text(value).lower()
    if raw.startswith("sha256:"):
        raw = raw[7:]
    return raw if re.fullmatch(r"[0-9a-f]{64}", raw) else None


def _resolve_relative(root: Optional[Path], value: Any) -> tuple[Optional[Path], Optional[str]]:
    relative = _text(value)
    if not relative:
        return None, "missing path"
    if root is None:
        return None, None
    candidate = Path(relative)
    if candidate.is_absolute():
        return None, "absolute paths are not allowed"
    resolved_root = root.resolve()
    resolved = (resolved_root / Path(relative.replace("/", "/"))).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError:
        return None, "path escapes validation root"
    return resolved, None


def _hash_matches(result: dict[str, Any], asset: Mapping[str, Any], root: Optional[Path], record_id: str, production: bool) -> None:
    expected = _normal_hash(_get(asset, "sha256", "hash", "output_hash", "file_hash"))
    if production and not expected:
        _add(result, "MISSING_ASSET_HASH", "BLOCKED", "production asset must carry a valid SHA-256 identity hash", record_id=record_id, field="sha256")
        return
    if production and root is None:
        _add(result, "ASSET_HASH_VALIDATION_UNAVAILABLE", "BLOCKED", "production asset hash cannot be verified without a validation root", record_id=record_id, field="file")
        return
    if not expected or root is None:
        return
    path_value = _get(asset, "file", "path", "file_path", "output_path")
    resolved, error = _resolve_relative(root, path_value)
    if error:
        _add(result, "ASSET_PATH_INVALID", "ERROR", error, record_id=record_id, field="file")
        return
    if resolved is None:
        return
    if not resolved.is_file():
        _add(result, "ASSET_FILE_MISSING", "BLOCKED", "recorded asset file is not present at validation time", record_id=record_id, field="file")
        return
    actual = hashlib.sha256(resolved.read_bytes()).hexdigest()
    if actual != expected:
        _add(result, "ASSET_HASH_MISMATCH", "ERROR", "asset bytes do not match the recorded SHA-256 identity", record_id=record_id, field="sha256")


def _legal_assertion(result: dict[str, Any], record: Mapping[str, Any], record_id: str) -> None:
    raw = json.dumps(record, ensure_ascii=False, sort_keys=True)
    if _get(record, "copyright_cleared", default=False) is True or _get(record, "exclusive", default=False) is True:
        _add(result, "UNSUPPORTED_LEGAL_ASSERTION", "ERROR", "record makes an unsupported ownership or exclusivity assertion", record_id=record_id)
        return
    if any(pattern.search(raw) for pattern in LEGAL_ASSERTION_PATTERNS):
        _add(result, "UNSUPPORTED_LEGAL_ASSERTION", "ERROR", "record uses an unsupported legal-certification assertion", record_id=record_id)


def classify_claim_risk(claim: Mapping[str, Any]) -> str:
    claim_type = _upper(_get(claim, "claim_type", "type"))
    if claim_type in {"HEALTH", "FINANCIAL"}:
        return "SPECIALIST_REVIEW_REQUIRED"
    if claim_type in {
        "QUANTITATIVE",
        "COMPARATIVE",
        "PERFORMANCE",
        "CERTIFICATION",
        "AWARD",
        "TESTIMONIAL",
        "CUSTOMER_COUNT",
        "YEARS_IN_BUSINESS",
        "GUARANTEE",
    }:
        return "HIGH"
    if claim_type in {"FACTUAL", "LOCATION", "PRODUCT_FEATURE", "AFFILIATE_PRODUCT"}:
        return "MODERATE"
    return "HIGH"


def classify_asset_risk(asset: Mapping[str, Any]) -> str:
    origin = _upper(_get(asset, "origin", "asset_origin"))
    if origin in {"UNKNOWN", "THIRD_PARTY_BRAND"}:
        return "SPECIALIST_REVIEW_REQUIRED"
    if origin in {"SCREENSHOT_REFERENCE", "RESEARCH_REFERENCE", "COMMISSIONED"}:
        return "HIGH"
    if origin == "LICENSED_STOCK" and not _get(asset, "license", "license_name"):
        return "HIGH"
    if origin in {"OWNER_PROVIDED", "CLIENT_PROVIDED", "AI_GENERATED", "LICENSED_STOCK"}:
        return "MODERATE"
    return "LOW"


def _source_index(ledger: Mapping[str, Any], result: dict[str, Any]) -> dict[str, Mapping[str, Any]]:
    sources = ledger.get("sources", [])
    if not isinstance(sources, list):
        _add(result, "SOURCES_SHAPE", "ERROR", "sources must be an array")
        return {}
    index: dict[str, Mapping[str, Any]] = {}
    for index_number, source in enumerate(sources):
        fallback = f"sources[{index_number}]"
        if not isinstance(source, Mapping):
            _add(result, "SOURCE_SHAPE", "ERROR", "source record must be an object", record_id=fallback)
            continue
        source_id = _record_id(source, fallback)
        if not _has_any(source, "source_id", "provenance_id", "id"):
            _add(result, "SOURCE_ID_MISSING", "BLOCKED", "source record requires a durable source identifier", record_id=source_id, field="source_id")
        if source_id in index:
            _add(result, "DUPLICATE_PROVENANCE_ID", "ERROR", "source identifier is duplicated", record_id=source_id)
        else:
            index[source_id] = source
        source_type = _upper(_get(source, "source_type", "type"))
        if source_type not in EVIDENCE_STRENGTH and source_type not in {"OWNER_ATTESTED", "CUSTOMER_ATTESTED", "INTERNAL_RECORD"}:
            _add(result, "SOURCE_TYPE_INVALID", "BLOCKED", "source type is not a bounded evidence type", record_id=source_id, field="source_type")
        if not _get(source, "url_or_ref", "source_url_or_ref", "url", "ref"):
            _add(result, "SOURCE_REFERENCE_MISSING", "BLOCKED", "source record has no URL or durable reference", record_id=source_id, field="url_or_ref")
        if "ai said so" in json.dumps(source, ensure_ascii=False).lower():
            _add(result, "AI_NOT_EVIDENCE", "ERROR", "model output is not accepted as evidence", record_id=source_id)
        _legal_assertion(result, source, source_id)
    result["counts"]["sources"] = len(sources)
    return index


def _resolve_evidence(
    result: dict[str, Any],
    record: Mapping[str, Any],
    sources: Mapping[str, Mapping[str, Any]],
    record_id: str,
    *,
    required: bool,
) -> tuple[Optional[Mapping[str, Any]], str]:
    ref = _get(record, "source_ref", "evidence_ref", "source_id", "license_evidence_ref")
    direct = _get(record, "source_url_or_ref", "source_url", "url_or_ref", "source")
    source: Optional[Mapping[str, Any]] = None
    if ref:
        ref_text = _text(ref)
        source = sources.get(ref_text)
        if source is None and required:
            _add(result, "EVIDENCE_REFERENCE_MISSING", "BLOCKED", "production evidence reference must resolve to a source register record", record_id=record_id, field="source_ref")
        elif source is None and not str(ref_text).lower().startswith(("http://", "https://")):
            _add(result, "EVIDENCE_REFERENCE_MISSING", "BLOCKED", "evidence reference does not resolve to a source record", record_id=record_id, field="source_ref")
    if source is None and direct:
        direct_text = _text(direct)
        if "ai said so" in direct_text.lower():
            _add(result, "AI_NOT_EVIDENCE", "ERROR", "model output is not accepted as evidence", record_id=record_id, field="source")
        if not required:
            source = {"source_type": _get(record, "source_type", default="UNVERIFIED"), "url_or_ref": direct_text}
        else:
            _add(result, "EVIDENCE_REFERENCE_MISSING", "BLOCKED", "production evidence URL must be registered as a source record", record_id=record_id, field="source_ref")
    if required and source is None:
        _add(result, "EVIDENCE_REQUIRED", "BLOCKED", "production record has no traceable evidence source", record_id=record_id, field="source_ref")
    declared_type = _upper(_get(record, "source_type", default=""))
    resolved_type = _upper(_get(source or {}, "source_type", "type"))
    if ref and source is not None and declared_type and resolved_type and declared_type != resolved_type:
        if resolved_type == "UNVERIFIED" and declared_type != "UNVERIFIED":
            _add(result, "SOURCE_TYPE_CONFLICT", "BLOCKED", "record-declared evidence strength exceeds the resolved source type", record_id=record_id, field="source_type")
    return source, resolved_type or declared_type


def _validate_source_record(
    result: dict[str, Any],
    source: Optional[Mapping[str, Any]],
    sources: Mapping[str, Mapping[str, Any]],
    record: Mapping[str, Any],
    record_id: str,
    *,
    production: bool,
) -> None:
    if not production or source is None:
        return
    source_type = _upper(_get(source, "source_type", "type"))
    if source_type not in EVIDENCE_STRENGTH:
        _add(result, "SOURCE_TYPE_INVALID", "BLOCKED", "production evidence source type is missing or outside the bounded taxonomy", record_id=record_id, field="source_type")
    elif source_type == "UNVERIFIED":
        _add(result, "UNVERIFIED_SOURCE", "BLOCKED", "unverified source cannot support a production record", record_id=record_id, field="source_type")
    ref = _text(_get(record, "source_ref", "evidence_ref", "source_id", "license_evidence_ref", "license_ref"))
    if not ref or ref not in sources:
        return
    for field in ("source_date", "retrieved_date"):
        if _missing(source.get(field)):
            _add(result, "SOURCE_FIELD_MISSING", "BLOCKED", f"production evidence source requires {field}", record_id=record_id, field=field)
        elif _date_value(source.get(field)) is None:
            _add(result, "SOURCE_DATE_INVALID", "ERROR", f"production evidence source {field} is not an ISO date", record_id=record_id, field=field)
    if not _has_any(source, "evidence_excerpt", "evidence_summary", "excerpt"):
        _add(result, "SOURCE_EVIDENCE_SUMMARY_MISSING", "BLOCKED", "production evidence source requires a bounded excerpt or summary", record_id=record_id, field="evidence_excerpt")


def _validate_claims(
    result: dict[str, Any],
    ledger: Mapping[str, Any],
    sources: Mapping[str, Mapping[str, Any]],
    mode: str,
    as_of: date,
) -> None:
    claims = ledger.get("claims", [])
    if not isinstance(claims, list):
        _add(result, "CLAIMS_SHAPE", "ERROR", "claims must be an array")
        return
    result["counts"]["claims"] = len(claims)
    for index, claim in enumerate(claims):
        fallback = f"claims[{index}]"
        if not isinstance(claim, Mapping):
            _add(result, "CLAIM_SHAPE", "ERROR", "claim record must be an object", record_id=fallback)
            continue
        claim_id = _record_id(claim, fallback)
        claim_type = _upper(_get(claim, "claim_type", "type"))
        risk = classify_claim_risk(claim)
        _validate_status_boundary(result, claim, claim_id)
        production = _is_production_record(claim, mode)
        if risk in {"HIGH", "SPECIALIST_REVIEW_REQUIRED"} and claim_id not in result["high_risk_items"]:
            result["high_risk_items"].append(claim_id)
        if not claim_type or claim_type not in CLAIM_TYPES:
            _add(result, "CLAIM_TYPE_INVALID", "ERROR", "claim type is missing or outside the controlled taxonomy", record_id=claim_id, field="claim_type")
        if not _get(claim, "claim_text", "text"):
            _add(result, "CLAIM_TEXT_MISSING", "ERROR", "claim text is required", record_id=claim_id, field="claim_text")
        if "ai said so" in json.dumps(claim, ensure_ascii=False).lower():
            _add(result, "AI_NOT_EVIDENCE", "ERROR", "model output is not accepted as evidence", record_id=claim_id)
        if production:
            required_fields = (
                ("claim_id", ("claim_id", "provenance_id", "id")),
                ("route", ("route",)),
                ("component", ("component",)),
                ("source", ("source", "source_ref", "evidence_ref", "source_url_or_ref", "source_url", "source_id")),
                ("source_type", ("source_type",)),
                ("source_date", ("source_date",)),
                ("verified_date", ("verified_date",)),
                ("evidence_strength", ("evidence_strength", "strength")),
                ("owner", ("owner",)),
                ("disclosure_required", ("disclosure_required",)),
                ("production_status", ("production_status", "status")),
                ("claim_status", ("claim_status", "claim_state")),
            )
            for field, keys in required_fields:
                if not _has_any(claim, *keys):
                    _add(result, "CLAIM_FIELD_MISSING", "BLOCKED", f"production claim requires {field}", record_id=claim_id, field=field)
            if (
                _get(claim, "freshness_required", default=False) is True
                or claim_type in FRESHNESS_REQUIRED_CLAIM_TYPES
            ) and not _has_any(
                claim, "expiration_or_review_date", "expiration_date", "review_date"
            ):
                _add(result, "CLAIM_FRESHNESS_MISSING", "BLOCKED", "freshness-required claim has no review or expiration date", record_id=claim_id, field="expiration_or_review_date")
        _legal_assertion(result, claim, claim_id)
        status = _upper(_get(claim, "claim_status", "status", default=""))
        if not status and production:
            _add(result, "CLAIM_STATUS_MISSING", "BLOCKED", "production claim requires an explicit claim status", record_id=claim_id, field="claim_status")
        elif status in {"CONTRADICTED", "PROHIBITED"}:
            _add(result, "CLAIM_NOT_USABLE", "ERROR" if production else "WARNING", f"claim status {status} cannot be released", record_id=claim_id, field="status")
        elif status in {"UNVERIFIED", "EXPIRED", "REVIEW_REQUIRED", "PARTIALLY_SUPPORTED"}:
            _add(result, "CLAIM_REVIEW_REQUIRED", "BLOCKED" if production else "WARNING", f"claim status {status} is not release-ready", record_id=claim_id, field="status")
        elif status and status not in CLAIM_STATUSES:
            _add(result, "CLAIM_STATUS_INVALID", "ERROR", "claim status is outside the controlled taxonomy", record_id=claim_id, field="status")

        source, source_type = _resolve_evidence(result, claim, sources, claim_id, required=production)
        _validate_source_record(result, source, sources, claim, claim_id, production=production)
        if production:
            declared_strength = _upper(_get(claim, "evidence_strength", "strength", default=""))
            resolved_strength = _upper(_get(source or {}, "evidence_strength", "source_type", "type"))
            strength = resolved_strength or declared_strength
            if declared_strength == "UNVERIFIED":
                strength = "UNVERIFIED"
            if strength not in EVIDENCE_STRENGTH or strength == "UNVERIFIED":
                _add(result, "EVIDENCE_STRENGTH_INSUFFICIENT", "BLOCKED", "production claim evidence strength is missing or unverified", record_id=claim_id, field="evidence_strength")
            claim_source_type = _upper(_get(claim, "source_type", default=""))
            if claim_source_type and claim_source_type not in EVIDENCE_STRENGTH:
                _add(result, "SOURCE_TYPE_INVALID", "BLOCKED", "claim source type is not a bounded evidence type", record_id=claim_id, field="source_type")
            claim_match = _get(claim, "evidence_match", "supports_claim", default=None)
            source_match = _get(source or {}, "evidence_match", "supports_claim", default=None)
            if claim_match is False or source_match is False:
                _add(result, "CLAIM_EVIDENCE_CONTRADICTION", "ERROR", "recorded evidence explicitly does not support the claim", record_id=claim_id, field="evidence_match")
                evidence_match = False
            else:
                evidence_match = (
                    claim_match is True
                    or source_match is True
                    or bool(_get(source or {}, "evidence_excerpt", "excerpt", "evidence_summary"))
                )
            if not evidence_match:
                _add(result, "CLAIM_SUPPORT_NOT_RECORDED", "BLOCKED", "source identity exists but support for the exact claim is not recorded", record_id=claim_id, field="evidence_match")
            if risk == "SPECIALIST_REVIEW_REQUIRED" and _upper(_get(claim, "specialist_review_status")) != "REVIEWED":
                _add(result, "SPECIALIST_REVIEW_REQUIRED", "BLOCKED", "claim requires specialist review before production use", record_id=claim_id)

        expiry = _date_value(_get(claim, "expiration_or_review_date", "expiration_date", "review_date"))
        for date_field in ("source_date", "verified_date", "expiration_or_review_date"):
            date_value = _get(claim, date_field)
            if date_value and _date_value(date_value) is None:
                _add(result, "CLAIM_DATE_INVALID", "ERROR", f"claim {date_field} is not an ISO date", record_id=claim_id, field=date_field)
        if expiry and expiry < as_of:
            _add(result, "CLAIM_EXPIRED", "BLOCKED" if production else "WARNING", "claim evidence is past its recorded review or expiration date", record_id=claim_id, field="expiration_or_review_date")

        if claim_type == "AFFILIATE_PRODUCT" or _get(claim, "affiliate", default=False) is True:
            origin = _upper(_get(claim, "claim_origin", "origin"))
            if origin not in {"MERCHANT", "EDITORIAL", "OWNER", "THIRD_PARTY"}:
                _add(result, "AFFILIATE_ORIGIN_UNCLASSIFIED", "BLOCKED", "affiliate claim origin must be classified and cannot be UNVERIFIED", record_id=claim_id, field="claim_origin")
            if origin == "MERCHANT" and not _get(claim, "disclosure_required", "disclosure_text"):
                _add(result, "AFFILIATE_DISCLOSURE_MISSING", "BLOCKED", "merchant-origin affiliate claims require a recorded disclosure dependency", record_id=claim_id, field="disclosure_required")


def _validate_testimonials(result: dict[str, Any], ledger: Mapping[str, Any], sources: Mapping[str, Mapping[str, Any]], mode: str) -> None:
    testimonials = ledger.get("testimonials", [])
    if not isinstance(testimonials, list):
        _add(result, "TESTIMONIALS_SHAPE", "ERROR", "testimonials must be an array")
        return
    result["counts"]["testimonials"] = len(testimonials)
    for index, testimonial in enumerate(testimonials):
        fallback = f"testimonials[{index}]"
        if not isinstance(testimonial, Mapping):
            _add(result, "TESTIMONIAL_SHAPE", "ERROR", "testimonial record must be an object", record_id=fallback)
            continue
        record_id = _record_id(testimonial, fallback)
        _validate_status_boundary(result, testimonial, record_id)
        production = _is_production_record(testimonial, mode)
        _legal_assertion(result, testimonial, record_id)
        if _get(testimonial, "is_composite", "composite", default=False) is True or _upper(_get(testimonial, "source_type")) == "COMPOSITE":
            _add(result, "COMPOSITE_TESTIMONIAL", "ERROR", "composite or fabricated testimonials are not accepted", record_id=record_id)
        if _upper(_get(testimonial, "status")) == "DEMO" and production:
            _add(result, "DEMO_TESTIMONIAL_PRODUCTION", "ERROR", "demo testimonial must remain prototype-only", record_id=record_id)
        source, _ = _resolve_evidence(result, testimonial, sources, record_id, required=production)
        _validate_source_record(result, source, sources, testimonial, record_id, production=production)
        if production:
            required_fields = (
                ("testimonial_id", ("testimonial_id", "provenance_id", "id")),
                ("text", ("text", "quote_text", "claim_text")),
                ("person_or_entity", ("person_or_entity", "person", "entity", "authority", "author", "customer_name", "attribution")),
                ("consent_or_usage_authority", ("consent_status", "consent", "usage_authority")),
                ("quote_status", ("quote_status", "quote_state")),
                ("date", ("date", "testimonial_date", "source_date")),
                ("production_status", ("production_status",)),
                ("production_approved", ("production_approved",)),
            )
            for field, keys in required_fields:
                if not _has_any(testimonial, *keys):
                    _add(result, "TESTIMONIAL_FIELD_MISSING", "BLOCKED", f"production testimonial requires {field}", record_id=record_id, field=field)
            if not _get(testimonial, "authority", "author", "customer_name", "attribution"):
                _add(result, "TESTIMONIAL_AUTHORITY_MISSING", "BLOCKED", "testimonial authority or attribution is missing", record_id=record_id, field="authority")
            consent = _get(testimonial, "consent_status", "consent", "usage_authority", default="")
            if consent is not True and _upper(consent) not in {"GRANTED", "OWNER_ATTESTED"}:
                _add(result, "TESTIMONIAL_CONSENT_MISSING", "BLOCKED", "testimonial consent is not recorded", record_id=record_id, field="consent_status")
            if _get(testimonial, "production_approved", default=False) is not True:
                _add(result, "TESTIMONIAL_NOT_APPROVED", "BLOCKED", "testimonial is not approved for production", record_id=record_id, field="production_approved")
            testimonial_date = _get(testimonial, "date", "testimonial_date", "source_date")
            if testimonial_date and _date_value(testimonial_date) is None:
                _add(result, "TESTIMONIAL_DATE_INVALID", "ERROR", "testimonial date is not an ISO date", record_id=record_id, field="date")
        if _get(testimonial, "edited", default=False) is True and not _get(testimonial, "edit_notes", "editing_notes"):
            _add(result, "TESTIMONIAL_EDIT_NOTES_MISSING", "BLOCKED" if production else "WARNING", "edited testimonial requires a record of edits", record_id=record_id, field="edit_notes")


def _validate_certifications(result: dict[str, Any], ledger: Mapping[str, Any], sources: Mapping[str, Mapping[str, Any]], mode: str, as_of: date) -> None:
    certifications = ledger.get("certifications", [])
    if not isinstance(certifications, list):
        _add(result, "CERTIFICATIONS_SHAPE", "ERROR", "certifications must be an array")
        return
    result["counts"]["certifications"] = len(certifications)
    for index, certification in enumerate(certifications):
        fallback = f"certifications[{index}]"
        if not isinstance(certification, Mapping):
            _add(result, "CERTIFICATION_SHAPE", "ERROR", "certification record must be an object", record_id=fallback)
            continue
        record_id = _record_id(certification, fallback)
        _validate_status_boundary(result, certification, record_id)
        result["high_risk_items"].append(record_id)
        production = _is_production_record(certification, mode)
        _legal_assertion(result, certification, record_id)
        required = (
            ("issuer", "issuer"),
            ("status", "status"),
            ("evidence_ref", "evidence_ref"),
            ("validity", "validity"),
            ("authorized_display", "authorized_display"),
        )
        for key, field in required:
            value = _get(certification, key, field)
            if value in (None, "", [], {}):
                _add(result, "CERTIFICATION_FIELD_MISSING", "BLOCKED" if production else "WARNING", f"certification requires {field}", record_id=record_id, field=field)
        status = _upper(_get(certification, "status"))
        if status in CERTIFICATION_BLOCKED_STATUSES:
            _add(result, "CERTIFICATION_STATUS_NOT_RELEASE_READY", "BLOCKED" if production else "WARNING", f"certification status {status} cannot be released", record_id=record_id, field="status")
        elif status and status not in CERTIFICATION_RELEASE_STATUSES:
            _add(result, "CERTIFICATION_STATUS_INVALID", "ERROR" if production else "WARNING", "certification status is outside the release taxonomy", record_id=record_id, field="status")
        source, _ = _resolve_evidence(result, certification, sources, record_id, required=production)
        _validate_source_record(result, source, sources, certification, record_id, production=production)
        validity_end = _date_value(_get(certification, "valid_until", "validity_end", "expiration_date"))
        if validity_end and validity_end < as_of:
            _add(result, "CERTIFICATION_EXPIRED", "BLOCKED" if production else "WARNING", "certification validity has expired", record_id=record_id, field="valid_until")
        if production and _get(certification, "authorized_display", default=False) is not True:
            _add(result, "CERTIFICATION_DISPLAY_NOT_AUTHORIZED", "BLOCKED", "certification display authorization is not recorded", record_id=record_id, field="authorized_display")


def _validate_research_references(result: dict[str, Any], ledger: Mapping[str, Any], mode: str) -> None:
    references = ledger.get("research_references", [])
    if not isinstance(references, list):
        _add(result, "RESEARCH_REFERENCES_SHAPE", "ERROR", "research_references must be an array")
        return
    result["counts"]["research_references"] = len(references)
    for index, reference in enumerate(references):
        fallback = f"research_references[{index}]"
        if not isinstance(reference, Mapping):
            _add(result, "RESEARCH_REFERENCE_SHAPE", "ERROR", "research reference must be an object", record_id=fallback)
            continue
        record_id = _record_id(reference, fallback)
        required_fields = (
            ("platform", "platform"),
            ("source_url", "source_url"),
            ("query", "query"),
            ("retrieved_at", "retrieved_at"),
            ("reference_purpose", "reference_purpose"),
            ("grade", "grade"),
            ("pattern_to_learn", "pattern_to_learn"),
            ("what_not_to_copy", "what_not_to_copy"),
            ("upstream_sha256", "upstream_sha256"),
        )
        for key, field in required_fields:
            if not _get(reference, key, default=None):
                _add(result, "RESEARCH_REFERENCE_FIELD_MISSING", "BLOCKED", f"research reference requires {field}", record_id=record_id, field=field)
        if _get(reference, "reference_only", default=None) is not True:
            _add(result, "RESEARCH_REFERENCE_BOUNDARY", "ERROR", "research references must remain REFERENCE_ONLY", record_id=record_id, field="reference_only")
        upstream_hash = _normal_hash(_get(reference, "upstream_sha256", "upstream_hash"))
        if not upstream_hash:
            _add(result, "RESEARCH_UPSTREAM_HASH_INVALID", "BLOCKED", "research reference requires a valid upstream SHA-256 identity", record_id=record_id, field="upstream_sha256")
        promoted = _upper(_get(reference, "production_status", "usage", "status"))
        if promoted in PRODUCTION_STATUSES or _get(reference, "promoted_to_asset", "production_asset", default=False) is True:
            _add(result, "RESEARCH_REFERENCE_PROMOTION", "ERROR", "research reference cannot be promoted to a production asset", record_id=record_id)


def _license_reference(
    result: dict[str, Any],
    asset: Mapping[str, Any],
    sources: Mapping[str, Mapping[str, Any]],
    record_id: str,
    *,
    production: bool,
) -> None:
    ref = _text(_get(asset, "license_evidence_ref", "license_ref", "evidence_ref"))
    source = sources.get(ref) if ref else None
    if production and not ref:
        _add(result, "LICENSE_EVIDENCE_MISSING", "BLOCKED", "production asset has no recorded license or rights evidence", record_id=record_id, field="license_evidence_ref")
    if production and ref and source is None:
        _add(result, "LICENSE_REFERENCE_MISSING", "BLOCKED", "production license evidence must resolve to a source register record", record_id=record_id, field="license_evidence_ref")
    elif ref and source is None and not ref.lower().startswith(("http://", "https://")):
        _add(result, "LICENSE_REFERENCE_MISSING", "BLOCKED", "license evidence reference does not resolve", record_id=record_id, field="license_evidence_ref")
    if source is not None:
        source_type = _upper(_get(source, "source_type", "type"))
        if source_type == "UNVERIFIED":
            _add(result, "LICENSE_EVIDENCE_UNVERIFIED", "BLOCKED", "license evidence source is explicitly unverified", record_id=record_id, field="license_evidence_ref")
        _validate_source_record(result, source, sources, asset, record_id, production=production)


def _validate_assets(
    result: dict[str, Any],
    ledger: Mapping[str, Any],
    sources: Mapping[str, Mapping[str, Any]],
    root: Optional[Path],
    mode: str,
) -> None:
    assets = ledger.get("assets", [])
    if not isinstance(assets, list):
        _add(result, "ASSETS_SHAPE", "ERROR", "assets must be an array")
        return
    result["counts"]["assets"] = len(assets)
    for index, asset in enumerate(assets):
        fallback = f"assets[{index}]"
        if not isinstance(asset, Mapping):
            _add(result, "ASSET_SHAPE", "ERROR", "asset record must be an object", record_id=fallback)
            continue
        record_id = _record_id(asset, fallback)
        _validate_status_boundary(result, asset, record_id)
        origin = _upper(_get(asset, "origin", "asset_origin"))
        risk = classify_asset_risk(asset)
        if risk in {"HIGH", "SPECIALIST_REVIEW_REQUIRED"}:
            result["high_risk_items"].append(record_id)
        _legal_assertion(result, asset, record_id)
        if origin not in ASSET_ORIGINS:
            _add(result, "ASSET_ORIGIN_INVALID", "ERROR", "asset origin is missing or outside the controlled taxonomy", record_id=record_id, field="origin")
            continue
        production = _is_production_record(asset, mode)
        if production:
            required_fields = (
                ("asset_id", ("asset_id", "provenance_id", "id")),
                ("file", ("file", "path", "file_path", "output_path")),
                ("asset_type", ("asset_type", "type", "file_type")),
                ("production_status", ("production_status", "status")),
                ("production_approved", ("production_approved",)),
                ("authorized_uses", ("authorized_uses", "permitted_uses")),
            )
            for field, keys in required_fields:
                if not _has_any(asset, *keys):
                    _add(result, "ASSET_FIELD_MISSING", "BLOCKED", f"production asset requires {field}", record_id=record_id, field=field)
            if _get(asset, "production_approved", default=False) is not True:
                _add(result, "ASSET_PRODUCTION_APPROVAL_MISSING", "BLOCKED", "production asset approval is not recorded", record_id=record_id, field="production_approved")
        if origin in {"SCREENSHOT_REFERENCE", "RESEARCH_REFERENCE"} and production:
            _add(result, "REFERENCE_ASSET_PROMOTION", "ERROR", "reference material cannot be promoted to a production asset", record_id=record_id, field="origin")
        if origin == "UNKNOWN" and production:
            _add(result, "UNKNOWN_ASSET_PROVENANCE", "BLOCKED", "unknown asset origin cannot be released", record_id=record_id, field="origin")

        if production and not _get(asset, "file", "path", "file_path", "output_path"):
            _add(result, "ASSET_FILE_REFERENCE_MISSING", "BLOCKED", "production asset must identify its output file", record_id=record_id, field="file")
        _hash_matches(result, asset, root, record_id, production)

        asset_type = _text(_get(asset, "asset_type", "type", "file_type")).lower()
        if "font" in asset_type:
            _license_reference(result, asset, sources, record_id, production=production)
            if production and _upper(_get(asset, "license", "license_name")) in {"", "UNKNOWN", "UNVERIFIED"}:
                _add(result, "FONT_LICENSE_MISSING", "BLOCKED", "font license identity is missing or unverified", record_id=record_id, field="license")

        if origin in {"LICENSED_STOCK", "OPEN_LICENSE", "PUBLIC_DOMAIN"}:
            if production and _upper(_get(asset, "license", "license_name")) in {"", "UNKNOWN", "UNVERIFIED"}:
                _add(result, "LICENSE_IDENTITY_MISSING", "BLOCKED", "licensed asset has no usable license identity", record_id=record_id, field="license")
            _license_reference(result, asset, sources, record_id, production=production)
            if production and not _get(asset, "authorized_uses", "permitted_uses"):
                _add(result, "AUTHORIZED_USE_MISSING", "BLOCKED", "asset authorized uses are not recorded", record_id=record_id, field="authorized_uses")
        if origin == "LICENSED_STOCK" and production:
            if not _get(asset, "provider", "provider_name", "stock_provider"):
                _add(result, "STOCK_PROVIDER_MISSING", "BLOCKED", "licensed stock asset lacks provider identity", record_id=record_id, field="provider")
            if not _get(asset, "source_url", "source_url_or_ref"):
                _add(result, "STOCK_SOURCE_MISSING", "BLOCKED", "licensed stock asset lacks source URL or durable reference", record_id=record_id, field="source_url")

        if origin in {"OWNER_PROVIDED", "CLIENT_PROVIDED"} and production:
            authority = _upper(_get(asset, "usage_authority", "authority", "rights_basis"))
            if authority not in {"OWNER_ATTESTED", "CLIENT_ATTESTED", "LICENSED", "COMMISSIONED"}:
                _add(result, "OWNER_USAGE_AUTHORITY_MISSING", "BLOCKED", "owner or client provided asset lacks a recorded usage authority", record_id=record_id, field="usage_authority")

        if origin == "AI_GENERATED" and production:
            provider = _get(asset, "provider", "tool", "model_provider")
            generated_date = _get(asset, "generation_date", "generated_at", "date")
            source_inputs = _get(asset, "source_inputs", "inputs", default=None)
            if not provider:
                _add(result, "AI_METADATA_MISSING", "BLOCKED", "AI-generated asset lacks provider or tool metadata", record_id=record_id, field="provider")
            if not generated_date:
                _add(result, "AI_METADATA_MISSING", "BLOCKED", "AI-generated asset lacks generation date metadata", record_id=record_id, field="generation_date")
            if source_inputs is None:
                _add(result, "AI_METADATA_MISSING", "BLOCKED", "AI-generated asset lacks source-input metadata", record_id=record_id, field="source_inputs")

        if origin == "COMMISSIONED" and production:
            if not _get(asset, "commission_record_ref", "commission_agreement_ref", "license_evidence_ref"):
                _add(result, "COMMISSION_RECORD_MISSING", "BLOCKED", "commissioned asset lacks a recorded commission or usage reference", record_id=record_id)

        if origin == "THIRD_PARTY_BRAND" and production:
            if not _get(asset, "mark_owner", "trademark_owner"):
                _add(result, "BRAND_OWNER_MISSING", "BLOCKED", "third-party brand asset lacks mark-owner identity", record_id=record_id)
            authorization = _upper(_get(asset, "authorization_status", "authorized_status"))
            if authorization not in {"AUTHORIZED", "OWNER_ATTESTED"}:
                _add(result, "BRAND_AUTHORIZATION_REVIEW_REQUIRED", "BLOCKED", "third-party brand authorization is unresolved", record_id=record_id, field="authorization_status")

        if _get(asset, "attribution_required", default=False) is True or _upper(_get(asset, "attribution_status")) == "REQUIRED":
            if production and not _get(asset, "attribution", "attribution_text", "credit"):
                _add(result, "ATTRIBUTION_MISSING", "ERROR", "required asset attribution is omitted", record_id=record_id, field="attribution")
        if _get(asset, "modified", default=False) is True and not _get(asset, "modification_notes", "edit_history"):
            _add(result, "ASSET_EDIT_HISTORY_MISSING", "BLOCKED" if production else "WARNING", "modified asset lacks edit history", record_id=record_id, field="modification_notes")


def _validate_duplicate_ids(result: dict[str, Any], ledger: Mapping[str, Any]) -> None:
    seen: dict[str, str] = {}
    collection_names = ("sources", "claims", "testimonials", "certifications", "research_references", "assets")
    for collection in collection_names:
        records = ledger.get(collection, [])
        if not isinstance(records, list):
            continue
        for index, record in enumerate(records):
            if not isinstance(record, Mapping):
                continue
            record_id = _record_id(record, f"{collection}[{index}]")
            previous = seen.get(record_id)
            if previous:
                _add(result, "DUPLICATE_PROVENANCE_ID", "ERROR", f"identifier is already used by {previous}", record_id=record_id)
            else:
                seen[record_id] = f"{collection}[{index}]"


def validate_ledger(
    ledger: Mapping[str, Any],
    *,
    root: Optional[Path | str] = None,
    ledger_ref: Optional[Path | str] = None,
    mode: str = "production",
    as_of: Optional[str] = None,
    production: Optional[bool] = None,
) -> dict[str, Any]:
    """Validate a ledger and return a machine-readable PASS/BLOCKED/FAIL result."""

    result = _new_result()
    if not isinstance(ledger, Mapping):
        _add(result, "LEDGER_SHAPE", "ERROR", "evidence ledger must be an object")
        return _finish(result)
    requested_mode = _mode(mode, production)
    normalized_mode = requested_mode if requested_mode != "invalid" else "production"
    if requested_mode == "invalid":
        _add(result, "VALIDATION_MODE_INVALID", "ERROR", "validation mode is outside the production/prototype policy")
    schema_version = _text(ledger.get("schema_version"))
    if not schema_version:
        _add(result, "LEDGER_SCHEMA_VERSION_MISSING", "ERROR", "evidence ledger requires schema_version", field="schema_version")
    elif schema_version != LEDGER_SCHEMA_VERSION:
        _add(result, "LEDGER_SCHEMA_VERSION_UNSUPPORTED", "BLOCKED", f"evidence ledger schema {schema_version} is not the current {LEDGER_SCHEMA_VERSION} contract", field="schema_version")
    if not _text(ledger.get("project_name")):
        _add(result, "LEDGER_PROJECT_NAME_MISSING", "ERROR", "evidence ledger requires project_name", field="project_name")
    root_path = Path(root) if root is not None else None
    if root_path is not None and not root_path.exists():
        _add(result, "VALIDATION_ROOT_MISSING", "BLOCKED", "validation root does not exist")
    sources = _source_index(ledger, result)
    _validate_duplicate_ids(result, ledger)
    today = _today(as_of)
    _validate_claims(result, ledger, sources, normalized_mode, today)
    _validate_testimonials(result, ledger, sources, normalized_mode)
    _validate_certifications(result, ledger, sources, normalized_mode, today)
    _validate_research_references(result, ledger, normalized_mode)
    _validate_assets(result, ledger, sources, root_path, normalized_mode)
    result["ledger_schema_version"] = schema_version or None
    result["mode"] = normalized_mode
    result["requested_mode"] = requested_mode
    if ledger_ref is not None:
        result["ledger_ref"] = _text(str(ledger_ref))
    return _finish(result)


def validate_asset_manifest(
    manifest: Mapping[str, Any],
    ledger: Mapping[str, Any],
    *,
    root: Optional[Path | str] = None,
    mode: str = "production",
    production: Optional[bool] = None,
) -> dict[str, Any]:
    """Verify that production asset manifest entries point into the ledger."""

    result = _new_result()
    if not isinstance(manifest, Mapping) or not isinstance(manifest.get("assets"), list):
        _add(result, "ASSET_MANIFEST_SHAPE", "ERROR", "asset manifest must contain an assets array")
        return _finish(result)
    if not isinstance(ledger, Mapping):
        _add(result, "LEDGER_SHAPE", "ERROR", "asset manifest cannot resolve provenance without a ledger")
        return _finish(result)
    requested_mode = _mode(mode, production)
    normalized_mode = requested_mode if requested_mode != "invalid" else "production"
    if requested_mode == "invalid":
        _add(result, "VALIDATION_MODE_INVALID", "ERROR", "validation mode is outside the production/prototype policy")
    ledger_assets = ledger.get("assets", [])
    ledger_index = {
        _record_id(asset, f"assets[{index}]"): asset
        for index, asset in enumerate(ledger_assets)
        if isinstance(asset, Mapping)
    }
    for index, entry in enumerate(manifest["assets"]):
        fallback = f"manifest.assets[{index}]"
        if not isinstance(entry, Mapping):
            _add(result, "ASSET_MANIFEST_ENTRY_SHAPE", "ERROR", "asset manifest entry must be an object", record_id=fallback)
            continue
        _validate_status_boundary(result, entry, fallback)
        production_entry = _is_production_record(entry, normalized_mode)
        reference = _text(_get(entry, "provenance_ref", "evidence_ref", "asset_provenance_ref"))
        if production_entry and not reference:
            _add(result, "MISSING_PRODUCTION_PROVENANCE_REF", "ERROR", "production asset manifest entry has no provenance_ref", record_id=fallback, field="provenance_ref")
            continue
        if not reference:
            continue
        reference_id = reference.split("#", 1)[-1].replace("asset:", "")
        if reference_id not in ledger_index:
            _add(result, "ASSET_PROVENANCE_REF_UNRESOLVED", "ERROR", "asset manifest provenance_ref does not resolve to a ledger asset", record_id=fallback, field="provenance_ref")
            continue
        target = ledger_index[reference_id]
        target_id = _record_id(target, reference_id)
        entry_id = _text(_get(entry, "asset_id", "id"))
        if entry_id and entry_id != target_id:
            _add(result, "ASSET_PROVENANCE_ID_MISMATCH", "ERROR", "asset manifest asset_id does not match its provenance target", record_id=fallback, field="asset_id")
        if production_entry:
            target_status = _upper(_get(target, "production_status", "status"))
            target_origin = _upper(_get(target, "origin", "asset_origin"))
            if target_status in PROTOTYPE_STATUSES or _get(target, "production_approved", default=None) is not True:
                _add(result, "ASSET_PROVENANCE_NOT_PRODUCTION_APPROVED", "ERROR", "production asset manifest entry resolves to an unapproved or prototype-only ledger asset", record_id=fallback, field="provenance_ref")
            if target_origin in {"SCREENSHOT_REFERENCE", "RESEARCH_REFERENCE"}:
                _add(result, "REFERENCE_ASSET_PROMOTION", "ERROR", "production asset manifest entry resolves to reference-only material", record_id=fallback, field="provenance_ref")
    result["counts"]["assets"] = len(manifest["assets"])
    result["mode"] = normalized_mode
    result["requested_mode"] = requested_mode
    return _finish(result)


def validate_provenance_state(
    state: Mapping[str, Any],
    *,
    ledger_result: Optional[Mapping[str, Any]] = None,
    root: Optional[Path | str] = None,
) -> dict[str, Any]:
    """Validate the cross-cutting site-profile provenance state shape."""

    result = _new_result()
    if not isinstance(state, Mapping):
        _add(result, "PROVENANCE_STATE_SHAPE", "ERROR", "provenance state must be an object")
        return _finish(result)
    if "locks" in state or any("lock" in str(key).lower() for key in state):
        _add(result, "PROVENANCE_LOCK_FORBIDDEN", "ERROR", "evidence readiness cannot create an owner lock")
    complete = state.get("complete", False)
    if not isinstance(complete, bool):
        _add(result, "PROVENANCE_COMPLETE_TYPE", "ERROR", "provenance.complete must be boolean", field="complete")
    if complete is True:
        ledger_ref = _text(state.get("ledger_ref"))
        if not ledger_ref:
            _add(result, "PROVENANCE_LEDGER_REF_MISSING", "BLOCKED", "provenance.complete requires a canonical ledger_ref", field="ledger_ref")
        if ledger_result is None:
            _add(result, "PROVENANCE_LEDGER_RESULT_MISSING", "BLOCKED", "provenance.complete requires a validated ledger result")
        elif ledger_result.get("status") != "PASS":
            _add(result, "PROVENANCE_LEDGER_NOT_PASSING", "BLOCKED", "provenance.complete cannot be true while the ledger is not passing")
        elif root is None and _text(ledger_result.get("ledger_ref")) != ledger_ref:
            _add(result, "PROVENANCE_LEDGER_IDENTITY_MISSING", "BLOCKED", "validated ledger result must carry the same ledger_ref when no validation root is supplied", field="ledger_ref")
        if root is not None and ledger_ref:
            resolved, error = _resolve_relative(Path(root), ledger_ref)
            if error:
                _add(result, "PROVENANCE_LEDGER_REF_INVALID", "ERROR", error, field="ledger_ref")
            elif resolved is None or not resolved.is_file():
                _add(result, "PROVENANCE_LEDGER_REF_UNRESOLVED", "BLOCKED", "provenance ledger_ref does not resolve to a ledger file", field="ledger_ref")
        inventory_flags = (
            "claim_inventory_complete",
            "asset_inventory_complete",
            "research_reference_inventory_complete",
            "license_review_complete",
            "attribution_review_complete",
        )
        for flag in inventory_flags:
            if state.get(flag) is not True:
                _add(result, "PROVENANCE_COMPLETION_INCOMPLETE", "BLOCKED", f"{flag} must be true before provenance is complete", field=flag)
        unresolved = state.get("unresolved_items", state.get("unresolved", []))
        high_risk = state.get("high_risk_items", state.get("high_risk", []))
        if unresolved:
            _add(result, "PROVENANCE_UNRESOLVED_ITEMS", "BLOCKED", "provenance state reports unresolved items")
        if high_risk:
            _add(result, "PROVENANCE_HIGH_RISK_ITEMS", "BLOCKED", "provenance state reports unresolved high-risk items")
    exception = state.get("exception")
    if exception is not None:
        if not isinstance(exception, Mapping) or exception.get("applied") is not True or not _text(exception.get("reason")):
            _add(result, "PROVENANCE_EXCEPTION_SHAPE", "ERROR", "provenance exception requires applied=true and a reason")
        elif complete is True:
            _add(result, "PROVENANCE_EXCEPTION_COMPLETE_CONFLICT", "ERROR", "an exception cannot certify a complete provenance state")
    if state.get("implementation_verified") is True and not state.get("implementation_evidence_ref"):
        _add(result, "PROVENANCE_IMPLEMENTATION_EVIDENCE_MISSING", "BLOCKED", "implementation verification requires an evidence reference")
    if state.get("production_verified") is True and not state.get("production_evidence_ref"):
        _add(result, "PROVENANCE_PRODUCTION_EVIDENCE_MISSING", "BLOCKED", "production verification requires an evidence reference")
    return _finish(result)


def load_ledger(path: Path | str) -> Mapping[str, Any]:
    """Load a JSON ledger without silently accepting malformed content."""

    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, Mapping):
        raise ValueError("evidence ledger must be a JSON object")
    return value
