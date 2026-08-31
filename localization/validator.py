"""Deterministic, provider-neutral Localization and Internationalization validation.

The validator distinguishes internationalization (the engineering/content
architecture that permits localization), localization (adaptation for a
language, locale, culture, or market), and translation (one part of
localization).  It validates project contracts and evidence boundaries; it
does not judge translation quality, call translation providers, make legal
determinations, or publish content.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
import re
from typing import Any, Optional
from urllib.parse import urlsplit


LOCALIZATION_STATUSES = {
    "NOT_REQUIRED",
    "PLANNING",
    "READY",
    "BLOCKED",
    "IMPLEMENTED",
    "VERIFIED",
    "EXCEPTION_APPLIED",
}
ROUTE_STRATEGIES = {
    "PATH_PREFIX",
    "SUBDOMAIN",
    "SEPARATE_DOMAIN",
    "NO_PUBLIC_LOCALE_ROUTING",
}
DEFAULT_URL_POLICIES = {"ROOT", "PREFIX"}
FALLBACK_POLICIES = {
    "NO_FALLBACK",
    "SOURCE_LOCALE_FALLBACK",
    "PARENT_LANGUAGE_FALLBACK",
    "CONTENT_TYPE_SPECIFIC",
}
CONTENT_COVERAGE = {"FULL", "PARTIAL", "NOT_AVAILABLE"}
DIRECTIONS = {"ltr", "rtl"}
TRANSLATION_STATUSES = {
    "SOURCE",
    "NOT_TRANSLATED",
    "MACHINE_DRAFT",
    "MACHINE_TRANSLATED",
    "HUMAN_REVIEW_REQUIRED",
    "HUMAN_REVIEWED",
    "REVIEWED",
    "APPROVED",
    "STALE",
    "PUBLISHED",
}
REVIEW_STATUSES = {"NOT_REVIEWED", "HUMAN_REVIEW_REQUIRED", "HUMAN_REVIEWED", "REVIEWED", "APPROVED", "LEGAL_REVIEW_REQUIRED"}
PUBLISHED_REVIEW_STATUSES = {"HUMAN_REVIEWED", "REVIEWED", "APPROVED"}
RTL_LANGUAGES = {"ar", "dv", "fa", "he", "ku", "ps", "ur", "yi"}
LANGUAGE_SCRIPT_DEFAULTS = {
    "ar": "Arab",
    "dv": "Thaa",
    "fa": "Arab",
    "he": "Hebr",
    "ja": "Jpan",
    "ko": "Kore",
    "ps": "Arab",
    "ru": "Cyrl",
    "uk": "Cyrl",
    "ur": "Arab",
    "yi": "Hebr",
    "zh": "Hans",
}
REGION_SCRIPT_DEFAULTS = {
    ("zh", "HK"): "Hant",
    ("zh", "MO"): "Hant",
    ("zh", "TW"): "Hant",
}
RESERVED_ROUTE_SEGMENTS = {
    "admin",
    "api",
    "assets",
    "auth",
    "login",
    "logout",
    "static",
    "_next",
    "404",
    "500",
}
SEMANTIC_MESSAGE_ID = re.compile(r"^[a-z][a-z0-9_-]*(?:\.[a-z0-9_-]+)+$")
HARD_CODED_DATE = re.compile(r"(?i)(?:mm[/.-]dd[/.-]yyyy|dd[/.-]mm[/.-]yyyy|\b\d{1,2}/\d{1,2}/\d{2,4}\b)")
CONCATENATION = re.compile(r"(?i)(?:\+\s*[a-z_{]|[a-z_}]\s*\+)")
STRENGTHENING_TERMS = ("guarantee", "guarantees", "guaranteed", "ensure", "ensures", "ensured", "always", "must")
HEDGING_TERMS = ("may", "might", "can", "could", "possibly", "potentially", "helps", "help")
REFERENCE_ONLY_TERMS = ("dribbble", "behance", "landbook", "mobbin", "awwwards", "siteinspire", "pinterest", "reference_only", "screenshot_reference")
STRENGTH_RANK = {
    "UNKNOWN": 0,
    "MAY": 1,
    "MIGHT": 1,
    "CAN": 2,
    "COULD": 2,
    "SUPPORTS": 2,
    "HELPS": 2,
    "IMPROVES": 3,
    "WILL": 4,
    "ENSURES": 5,
    "GUARANTEES": 5,
}
PSEUDO_MAP = str.maketrans(
    {
        "A": "Ȧ",
        "B": "Ḃ",
        "C": "Ƈ",
        "D": "Ḋ",
        "E": "Ë",
        "F": "Ḟ",
        "G": "Ġ",
        "H": "Ḧ",
        "I": "Ï",
        "J": "Ĵ",
        "K": "Ḱ",
        "L": "Ŀ",
        "M": "Ṁ",
        "N": "Ñ",
        "O": "Ö",
        "P": "Ṗ",
        "Q": "Ɋ",
        "R": "Ŕ",
        "S": "Š",
        "T": "Ṫ",
        "U": "Ü",
        "V": "Ṿ",
        "W": "Ŵ",
        "X": "Ẍ",
        "Y": "Ÿ",
        "Z": "Ž",
        "a": "ȧ",
        "b": "ḃ",
        "c": "ƈ",
        "d": "ḋ",
        "e": "ë",
        "f": "ḟ",
        "g": "ġ",
        "h": "ḧ",
        "i": "ï",
        "j": "ĵ",
        "k": "ḱ",
        "l": "ŀ",
        "m": "ṁ",
        "n": "ñ",
        "o": "ö",
        "p": "ṗ",
        "q": "ɋ",
        "r": "ŕ",
        "s": "š",
        "t": "ṫ",
        "u": "ü",
        "v": "ṿ",
        "w": "ŵ",
        "x": "ẍ",
        "y": "ÿ",
        "z": "ž",
    }
)


def _get(record: Mapping[str, Any], *keys: str, default: Any = None) -> Any:
    if not isinstance(record, Mapping):
        return default
    for key in keys:
        if key in record:
            return record[key]
        for candidate in (key.upper(), key.lower()):
            if candidate in record:
                return record[candidate]
    return default


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _upper(value: Any) -> str:
    return _text(value).upper()


def _list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _missing(value: Any) -> bool:
    """Return whether a field is absent or contains an empty scalar/collection."""

    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    return isinstance(value, (list, tuple, set, dict)) and len(value) == 0


def _records(value: Any, *id_keys: str) -> list[dict[str, Any]]:
    if isinstance(value, Mapping):
        output: list[dict[str, Any]] = []
        for key, child in value.items():
            if isinstance(child, Mapping):
                record = dict(child)
                if id_keys and not any(candidate in record for candidate in id_keys):
                    record[id_keys[0]] = key
                output.append(record)
            else:
                output.append({id_keys[0] if id_keys else "id": key, "value": child})
        return output
    return [dict(item) for item in value if isinstance(item, Mapping)] if isinstance(value, (list, tuple)) else []


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
    issue: dict[str, Any] = {"code": code, "severity": severity, "message": message}
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
        "errors": sum(item["severity"] == "ERROR" for item in result["issues"]),
        "blocked": sum(item["severity"] == "BLOCKED" for item in result["issues"]),
        "warnings": sum(item["severity"] == "WARNING" for item in result["issues"]),
    }
    result["status"] = "FAIL" if result["counts"]["errors"] else "BLOCKED" if result["counts"]["blocked"] else "PASS"
    result["ok"] = result["status"] == "PASS"
    result["unresolved_items"] = sorted(set(result["unresolved_items"]))
    return result


def _merge(result: dict[str, Any], name: str, child: Mapping[str, Any]) -> None:
    result.setdefault("component_results", {})[name] = dict(child)
    result["issues"].extend(child.get("issues", []))
    result["warnings"].extend(child.get("warnings", []))
    result["unresolved_items"].extend(child.get("unresolved_items", []))


def parse_locale(value: Any) -> Optional[dict[str, Any]]:
    """Parse a standards-compatible BCP 47-style locale identifier.

    The framework intentionally implements only the syntax needed for public
    locale registries.  It accepts language, optional script, optional region,
    variants, extensions, and private-use subtags, while rejecting underscore
    aliases such as ``english_USA``.
    """

    if not isinstance(value, str):
        return None
    raw = value.strip()
    if not raw or "_" in raw or raw.startswith("-") or raw.endswith("-"):
        return None
    parts = raw.split("-")
    if not 1 <= len(parts) <= 20 or not re.fullmatch(r"[A-Za-z]{2,8}", parts[0]):
        return None
    language = parts[0].lower()
    index = 1
    script: Optional[str] = None
    region: Optional[str] = None
    variants: list[str] = []
    extensions: list[str] = []
    private_use = False
    if index < len(parts) and re.fullmatch(r"[A-Za-z]{4}", parts[index]):
        script = parts[index].title()
        index += 1
    if index < len(parts) and (re.fullmatch(r"[A-Za-z]{2}", parts[index]) or re.fullmatch(r"\d{3}", parts[index])):
        region = parts[index].upper() if parts[index].isalpha() else parts[index]
        index += 1
    while index < len(parts):
        part = parts[index]
        if not re.fullmatch(r"[A-Za-z0-9]{1,8}", part):
            return None
        lower_part = part.lower()
        if lower_part == "x":
            private_use = True
            index += 1
            if index >= len(parts):
                return None
            private_subtags: list[str] = []
            while index < len(parts):
                if not re.fullmatch(r"[A-Za-z0-9]{1,8}", parts[index]):
                    return None
                private_subtags.append(parts[index].lower())
                index += 1
            extensions.append("x-" + "-".join(private_subtags))
            break
        if len(part) == 1:
            if not re.fullmatch(r"[0-9A-WY-Za-wy-z]", part):
                return None
            singleton = lower_part
            index += 1
            extension_subtags: list[str] = []
            while index < len(parts) and len(parts[index]) != 1:
                extension_part = parts[index]
                if not re.fullmatch(r"[A-Za-z0-9]{2,8}", extension_part):
                    return None
                extension_subtags.append(extension_part.lower())
                index += 1
            if not extension_subtags:
                return None
            if any(extension.startswith(singleton + "-") for extension in extensions):
                return None
            extensions.append(singleton + "-" + "-".join(extension_subtags))
            continue
        if (len(part) == 4 and part[0].isdigit()) or len(part) in {5, 6, 7, 8}:
            variants.append(lower_part)
            index += 1
            continue
        return None
    canonical_parts = [language]
    if script:
        canonical_parts.append(script)
    if region:
        canonical_parts.append(region)
    canonical_parts.extend(variants)
    canonical_parts.extend(extensions)
    return {
        "locale": raw,
        "canonical": "-".join(canonical_parts),
        "language": language,
        "script": script,
        "region": region,
        "variants": variants,
        "extensions": extensions,
        "private_use": private_use,
    }


def is_valid_locale_code(value: Any) -> bool:
    return parse_locale(value) is not None


def _locale_key(value: Any) -> str:
    parsed = parse_locale(value)
    return parsed["canonical"].lower() if parsed else ""


def _locale_key_set(value: Any) -> set[str]:
    """Return normalized locale identities from a supported-locale collection."""

    values = value if isinstance(value, (list, tuple, set)) else []
    keys: set[str] = set()
    for item in values:
        candidate = item.get("locale") if isinstance(item, Mapping) else item
        key = _locale_key(candidate)
        if key:
            keys.add(key)
    return keys


def _script_for(parsed: Mapping[str, Any]) -> Optional[str]:
    if parsed.get("script"):
        return str(parsed["script"])
    language = str(parsed.get("language"))
    region = str(parsed.get("region")) if parsed.get("region") else None
    return REGION_SCRIPT_DEFAULTS.get((language, region)) or LANGUAGE_SCRIPT_DEFAULTS.get(language)


def _normal_prefix(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return None
    value = value.strip()
    if value in {"", "/"}:
        return "/"
    if "://" in value or "?" in value or "#" in value:
        return None
    if not value.startswith("/"):
        value = "/" + value
    value = re.sub(r"/{2,}", "/", value.rstrip("/"))
    return value or "/"


def _url_key(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    try:
        parsed = urlsplit(value.strip())
    except ValueError:
        return ""
    path = parsed.path or value.strip().split("?", 1)[0].split("#", 1)[0]
    if not path.startswith("/"):
        path = "/" + path
    return re.sub(r"/{2,}", "/", path.rstrip("/")) or "/"


def _route_host(record: Mapping[str, Any]) -> str:
    explicit = _text(_get(record, "route_host", "domain", "host", default=""))
    if explicit:
        try:
            parsed = urlsplit(explicit if "://" in explicit else "//" + explicit)
            return (parsed.netloc or explicit.split("/", 1)[0]).lower()
        except ValueError:
            return explicit.split("/", 1)[0].lower()
    for key in ("url", "route", "path"):
        value = _text(_get(record, key, default=""))
        if value:
            try:
                parsed = urlsplit(value)
            except ValueError:
                continue
            if parsed.netloc:
                return parsed.netloc.lower()
    return ""


def _url_identity(value: Any, *, host: Any = None) -> str:
    """Normalize a route while preserving an absolute or declared host."""

    if not isinstance(value, str):
        return ""
    try:
        parsed = urlsplit(value.strip())
    except ValueError:
        return ""
    route_host = (parsed.netloc or _text(host)).lower()
    return (route_host + _url_key(value)) if route_host else _url_key(value)


def _bool_field(result: dict[str, Any], record: Mapping[str, Any], key: str, *, path: str) -> Optional[bool]:
    if key not in record:
        return None
    value = record.get(key)
    if not isinstance(value, bool):
        _add(result, "BOOLEAN_FIELD_INVALID", "ERROR", f"{path}.{key} must be boolean", path=f"{path}.{key}")
        return None
    return value


def calculate_localization_requirement(factors: Optional[Mapping[str, Any]] = None) -> dict[str, Any]:
    """Assess localization need from recorded strategy facts only.

    IP address, browser language, owner ethnicity, company name, and
    geographic stereotypes are deliberately reported as ignored inputs and
    never contribute to the decision.
    """

    source = dict(factors or {})
    result: dict[str, Any] = {
        "localization_required": False,
        "status": "NOT_REQUIRED",
        "signals": [],
        "ignored_inference_inputs": [],
        "factors": {},
        "rationale": "No recorded market, language, regional, or owner-strategy requirement establishes localization need.",
    }
    explicit = _get(source, "localization_required", "required", default=None)
    if explicit is not None and not isinstance(explicit, bool):
        result["status"] = "BLOCKED"
        result["blocked_reason"] = "explicit localization requirement must be boolean"
        return result
    if explicit is True:
        result["localization_required"] = True
        result["status"] = "PLANNING"
        result["signals"].append("OWNER_EXPLICIT_REQUIREMENT")
    elif explicit is False:
        result["rationale"] = "Owner explicitly recorded that multiple languages or regions are not required."

    positive_keys = (
        ("target_markets", "TARGET_MARKETS"),
        ("audience_languages", "AUDIENCE_LANGUAGES"),
        ("geographic_expansion", "GEOGRAPHIC_EXPANSION"),
        ("regulatory_requirements", "REGULATORY_OR_CONTRACTUAL_REQUIREMENT"),
        ("contractual_requirements", "REGULATORY_OR_CONTRACTUAL_REQUIREMENT"),
        ("contractual_requirement", "REGULATORY_OR_CONTRACTUAL_REQUIREMENT"),
        ("existing_translated_content", "EXISTING_TRANSLATED_CONTENT"),
        ("seo_opportunity", "SEO_OPPORTUNITY"),
        ("product_availability_by_region", "REGIONAL_PRODUCT_AVAILABILITY"),
        ("currencies", "MULTIPLE_CURRENCIES"),
        ("local_offices", "LOCAL_OFFICES"),
        ("customer_support_capability", "CUSTOMER_SUPPORT_CAPABILITY"),
        ("content_maintenance_capability", "CONTENT_MAINTENANCE_CAPABILITY"),
        ("owner_strategy", "OWNER_STRATEGY"),
    )
    for key, signal in positive_keys:
        value = _get(source, key, key.upper(), default=None)
        result["factors"][key] = value
        meaningful = False
        if isinstance(value, bool):
            meaningful = value
        elif isinstance(value, (list, tuple, set, dict)):
            meaningful = len(value) > 0
        elif isinstance(value, str):
            meaningful = bool(value.strip()) and _upper(value) not in {"NONE", "NO", "NOT_REQUIRED", "NOT_APPLICABLE"}
        if meaningful:
            result["signals"].append(signal)
    ignored_keys = ("ip_address", "browser_language", "owner_ethnicity", "company_name", "geographic_stereotypes")
    for key in ignored_keys:
        if _get(source, key, key.upper(), default=None) is not None:
            result["ignored_inference_inputs"].append(key)

    owner_strategy = _upper(_get(source, "owner_strategy", default=""))
    meaningful_signals = set(result["signals"])
    strategy_requires = owner_strategy in {"MULTILINGUAL", "MULTI_REGION", "REGIONAL_EXPANSION", "INTERNATIONAL_EXPANSION"}
    multiple_languages = isinstance(_get(source, "audience_languages", default=None), (list, tuple, set)) and len(_get(source, "audience_languages", default=[])) > 1
    multiple_markets = isinstance(_get(source, "target_markets", default=None), (list, tuple, set)) and len(_get(source, "target_markets", default=[])) > 1
    multiple_currencies = isinstance(_get(source, "currencies", default=None), (list, tuple, set)) and len(_get(source, "currencies", default=[])) > 1
    if explicit is not False and (explicit is True or strategy_requires or multiple_languages or multiple_markets or multiple_currencies or meaningful_signals.intersection({"GEOGRAPHIC_EXPANSION", "REGULATORY_OR_CONTRACTUAL_REQUIREMENT", "EXISTING_TRANSLATED_CONTENT", "SEO_OPPORTUNITY", "REGIONAL_PRODUCT_AVAILABILITY", "LOCAL_OFFICES"})):
        result["localization_required"] = True
        result["status"] = "PLANNING"
        result["rationale"] = "Recorded market, language, regional, SEO, regulatory, content, or owner-strategy facts justify localization assessment."
    return result


def _registry_locales(registry: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = _get(registry, "locales", "supported_locales", default=[])
    if isinstance(raw, Mapping):
        records = []
        for key, value in raw.items():
            record = dict(value) if isinstance(value, Mapping) else {}
            record.setdefault("locale", key)
            records.append(record)
        return records
    return _records(raw, "locale")


def _locale_records(value: Any) -> list[dict[str, Any]]:
    """Normalize either locale records or a simple list of locale codes."""

    if isinstance(value, Mapping):
        if any(key in value for key in ("locale", "language", "direction")):
            return [dict(value)]
        return _records(value, "locale")
    if isinstance(value, (list, tuple)):
        return [dict(item) if isinstance(item, Mapping) else {"locale": item} for item in value]
    return []


def _flagged(records: Sequence[Mapping[str, Any]], key: str) -> list[str]:
    return [_text(record.get("locale")) for record in records if record.get(key) is True]


def _validate_fallback_cycles(fallbacks: Mapping[str, str], result: dict[str, Any]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, path: list[str]) -> None:
        if node in visiting:
            cycle = " -> ".join(path + [node])
            _add(result, "FALLBACK_CYCLE", "ERROR", f"locale fallback cycle detected: {cycle}", path="fallback_locale")
            return
        if node in visited:
            return
        visiting.add(node)
        target = fallbacks.get(node)
        if target:
            visit(target, path + [node])
        visiting.remove(node)
        visited.add(node)

    for locale in fallbacks:
        visit(locale, [])


def validate_locale_registry(registry: Mapping[str, Any], *, required: Optional[bool] = None) -> dict[str, Any]:
    """Validate locale identity, routing, direction, coverage, and fallback policy."""

    result = _new_result()
    if not isinstance(registry, Mapping):
        _add(result, "LOCALE_REGISTRY_MISSING", "BLOCKED", "locale registry must be an object")
        return _finish(result)
    records = _registry_locales(registry)
    explicit_required = registry.get("required", required)
    if explicit_required is not None and not isinstance(explicit_required, bool):
        _add(result, "LOCALIZATION_REQUIRED_TYPE", "ERROR", "locale registry required must be boolean", path="required")
    is_required = bool(explicit_required) if isinstance(explicit_required, bool) else bool(records or registry.get("source_locale") or registry.get("default_locale"))
    registry_status = _upper(registry.get("status", ""))
    if registry_status and registry_status not in LOCALIZATION_STATUSES:
        _add(result, "LOCALIZATION_STATUS_INVALID", "ERROR", f"locale registry status {registry_status!r} is unsupported", path="status")
    seen: set[str] = set()
    parsed_by_key: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        path = f"locales[{index}]"
        if not isinstance(record, Mapping):
            _add(result, "LOCALE_RECORD_SHAPE", "ERROR", f"{path} must be an object", path=path)
            continue
        locale = _get(record, "locale", default=None)
        parsed = parse_locale(locale)
        if parsed is None:
            _add(result, "INVALID_LOCALE_CODE", "ERROR", f"{path}.locale is not a valid locale identifier", path=f"{path}.locale")
            continue
        key = parsed["canonical"].lower()
        if key in seen:
            _add(result, "DUPLICATE_LOCALE", "ERROR", f"locale {parsed['canonical']} is declared more than once", path=f"{path}.locale")
        seen.add(key)
        parsed_by_key[key] = dict(parsed)
        for field in ("enabled", "default", "source"):
            _bool_field(result, record, field, path=path)
        direction = _text(_get(record, "direction", default="")).lower()
        if direction and direction not in DIRECTIONS:
            _add(result, "DIRECTION_INVALID", "ERROR", f"{path}.direction must be ltr or rtl", path=f"{path}.direction")
        if parsed["language"] in RTL_LANGUAGES and direction == "ltr":
            _add(result, "RTL_DIRECTION_MISMATCH", "ERROR", f"{parsed['canonical']} uses an RTL language but is declared ltr", path=f"{path}.direction")
        coverage = _upper(_get(record, "content_coverage", default=""))
        if coverage and coverage not in CONTENT_COVERAGE:
            _add(result, "CONTENT_COVERAGE_INVALID", "ERROR", f"{path}.content_coverage is unsupported", path=f"{path}.content_coverage")
        record_status = _upper(_get(record, "status", default=""))
        if record_status and record_status not in LOCALIZATION_STATUSES | TRANSLATION_STATUSES:
            _add(result, "LOCALE_STATUS_INVALID", "ERROR", f"{path}.status is unsupported", path=f"{path}.status")
        review_status = _upper(_get(record, "review_status", default=""))
        if review_status and review_status not in REVIEW_STATUSES:
            _add(result, "LOCALE_REVIEW_STATUS_INVALID", "ERROR", f"{path}.review_status is unsupported", path=f"{path}.review_status")
        seo_enabled = _get(record, "seo_enabled", default=None)
        if seo_enabled is not None and not isinstance(seo_enabled, bool):
            _add(result, "BOOLEAN_FIELD_INVALID", "ERROR", f"{path}.seo_enabled must be boolean", path=f"{path}.seo_enabled")
        for field, expected in (("language", parsed["language"]), ("script", parsed["script"]), ("region", parsed["region"])):
            if field in record and record[field] is not None and _text(record[field]) != _text(expected):
                _add(result, "LOCALE_COMPONENT_MISMATCH", "ERROR", f"{path}.{field} does not match the locale identifier", path=f"{path}.{field}")

    if not is_required:
        optional_status = registry_status or "NOT_REQUIRED"
        if records and optional_status not in {"NOT_REQUIRED", "EXCEPTION_APPLIED"}:
            _add(result, "LOCALIZATION_STATUS_INCONSISTENT", "WARNING", "optional localization records exist while registry status is not NOT_REQUIRED")
        return _finish(result)

    if not records:
        _add(result, "LOCALE_REGISTRY_EMPTY", "BLOCKED", "a required localization architecture needs at least one locale")

    top_source = _locale_key(registry.get("source_locale")) if registry.get("source_locale") is not None else ""
    top_default = _locale_key(registry.get("default_locale")) if registry.get("default_locale") is not None else ""
    if registry.get("source_locale") is not None and not top_source:
        _add(result, "INVALID_LOCALE_CODE", "ERROR", "source_locale is not a valid locale identifier", path="source_locale")
    if registry.get("default_locale") is not None and not top_default:
        _add(result, "INVALID_LOCALE_CODE", "ERROR", "default_locale is not a valid locale identifier", path="default_locale")
    source_flags = [_locale_key(value) for value in _flagged(records, "source") if _locale_key(value)]
    default_flags = [_locale_key(value) for value in _flagged(records, "default") if _locale_key(value)]
    if registry.get("source_locale") is None and len(source_flags) != 1:
        _add(result, "SOURCE_LOCALE_REQUIRED", "BLOCKED", "exactly one authoritative source locale is required", path="source_locale")
    if registry.get("default_locale") is None and len(default_flags) != 1:
        _add(result, "DEFAULT_LOCALE_REQUIRED", "BLOCKED", "exactly one default locale is required", path="default_locale")
    if top_source and top_source not in parsed_by_key:
        _add(result, "SOURCE_LOCALE_UNKNOWN", "ERROR", "source_locale is not present in the locale registry", path="source_locale")
    if top_default and top_default not in parsed_by_key:
        _add(result, "DEFAULT_LOCALE_UNKNOWN", "ERROR", "default_locale is not present in the locale registry", path="default_locale")
    if top_source and not source_flags:
        _add(result, "SOURCE_LOCALE_FLAG_MISSING", "BLOCKED", "the source locale record must declare source=true", path="locales")
    if top_default and not default_flags:
        _add(result, "DEFAULT_LOCALE_FLAG_MISSING", "BLOCKED", "the default locale record must declare default=true", path="locales")
    if source_flags and len(source_flags) != 1:
        _add(result, "MULTIPLE_SOURCE_LOCALES", "ERROR", "locale registry must have exactly one source=true locale", path="locales")
    if default_flags and len(default_flags) != 1:
        _add(result, "MULTIPLE_DEFAULT_LOCALES", "ERROR", "locale registry must have exactly one default=true locale", path="locales")
    if top_source and source_flags and source_flags[0] != top_source:
        _add(result, "SOURCE_LOCALE_MISMATCH", "ERROR", "source_locale and source=true record disagree", path="source_locale")
    if top_default and default_flags and default_flags[0] != top_default:
        _add(result, "DEFAULT_LOCALE_MISMATCH", "ERROR", "default_locale and default=true record disagree", path="default_locale")
    supported_value = registry.get("supported_locales")
    supported_keys: list[str] = []
    if supported_value is not None:
        if not isinstance(supported_value, list):
            _add(result, "SUPPORTED_LOCALES_INVALID", "ERROR", "supported_locales must be an array", path="supported_locales")
        else:
            for index, value in enumerate(supported_value):
                key = _locale_key(value)
                if not key:
                    _add(result, "INVALID_LOCALE_CODE", "ERROR", "supported_locales contains an invalid locale identifier", path=f"supported_locales[{index}]")
                elif key in supported_keys:
                    _add(result, "DUPLICATE_LOCALE", "ERROR", f"supported_locales contains {value!r} more than once", path=f"supported_locales[{index}]")
                else:
                    supported_keys.append(key)
                    if key not in parsed_by_key:
                        _add(result, "SUPPORTED_LOCALE_UNKNOWN", "ERROR", f"supported locale {value!r} has no registry record", path=f"supported_locales[{index}]")
                    elif next((item for item in records if _locale_key(item.get("locale")) == key), {}).get("enabled", True) is False:
                        _add(result, "SUPPORTED_LOCALE_DISABLED", "ERROR", f"supported locale {value!r} is disabled", path=f"supported_locales[{index}]")
    source_key = top_source or (source_flags[0] if len(source_flags) == 1 else "")
    default_key = top_default or (default_flags[0] if len(default_flags) == 1 else "")

    route_strategy = _upper(_get(registry, "route_strategy", default=""))
    if route_strategy not in ROUTE_STRATEGIES:
        _add(result, "ROUTE_STRATEGY_INVALID", "ERROR", "required localization must declare a supported route_strategy", path="route_strategy")
    default_url_policy = _upper(_get(registry, "default_locale_url_policy", default=""))
    if route_strategy == "PATH_PREFIX" and default_url_policy not in DEFAULT_URL_POLICIES:
        _add(result, "DEFAULT_LOCALE_URL_POLICY_MISSING", "BLOCKED", "PATH_PREFIX routing requires an explicit ROOT or PREFIX default locale URL policy", path="default_locale_url_policy")
    prefixes: dict[str, str] = {}
    hosts: dict[str, str] = {}
    for index, record in enumerate(records):
        locale_key = _locale_key(record.get("locale"))
        if locale_key not in parsed_by_key:
            continue
        enabled = record.get("enabled", True)
        if not isinstance(enabled, bool):
            continue
        if route_strategy == "PATH_PREFIX" and enabled:
            prefix = _normal_prefix(_get(record, "route_prefix", default=None))
            if prefix is None:
                _add(result, "LOCALE_ROUTE_MISSING", "BLOCKED", f"{record.get('locale')} needs a valid route_prefix", path=f"locales[{index}].route_prefix")
            else:
                overlapping = next((owner for existing, owner in prefixes.items() if prefix == existing or (existing != "/" and prefix.startswith(existing + "/")) or (prefix != "/" and existing.startswith(prefix + "/"))), None)
                if overlapping:
                    _add(result, "LOCALE_ROUTE_COLLISION", "ERROR", f"{record.get('locale')} collides with {overlapping} at {prefix}", path=f"locales[{index}].route_prefix")
                elif prefix in prefixes:
                    _add(result, "LOCALE_ROUTE_COLLISION", "ERROR", f"{record.get('locale')} collides with {prefixes[prefix]} at {prefix}", path=f"locales[{index}].route_prefix")
                prefixes[prefix] = str(record.get("locale"))
                first_segment = prefix.strip("/").split("/", 1)[0].lower()
                if first_segment in RESERVED_ROUTE_SEGMENTS:
                    _add(result, "LOCALE_ROUTE_RESERVED", "ERROR", f"{record.get('locale')} uses reserved route segment {first_segment!r}", path=f"locales[{index}].route_prefix")
                if locale_key == default_key:
                    if default_url_policy == "ROOT" and prefix != "/":
                        _add(result, "DEFAULT_LOCALE_URL_POLICY_VIOLATION", "ERROR", "default locale must use the root URL under ROOT policy", path=f"locales[{index}].route_prefix")
                    if default_url_policy == "PREFIX" and prefix == "/":
                        _add(result, "DEFAULT_LOCALE_URL_POLICY_VIOLATION", "ERROR", "default locale must use a prefix under PREFIX policy", path=f"locales[{index}].route_prefix")
        elif route_strategy in {"SUBDOMAIN", "SEPARATE_DOMAIN"} and enabled:
            host = _text(_get(record, "route_host", "domain", "host", default="")).lower()
            if not host:
                _add(result, "LOCALE_ROUTE_MISSING", "BLOCKED", f"{record.get('locale')} needs a route host/domain", path=f"locales[{index}].route_host")
            elif host in hosts:
                _add(result, "LOCALE_ROUTE_COLLISION", "ERROR", f"{record.get('locale')} collides with {hosts[host]} at {host}", path=f"locales[{index}].route_host")
            else:
                hosts[host] = str(record.get("locale"))

    fallback_policy = _upper(_get(registry, "fallback_policy", "fallback", default=""))
    if fallback_policy not in FALLBACK_POLICIES:
        _add(result, "FALLBACK_POLICY_MISSING", "BLOCKED", "required localization must declare a fallback policy", path="fallback_policy")
    fallback_map: dict[str, str] = {}
    for index, record in enumerate(records):
        locale_key = _locale_key(record.get("locale"))
        fallback_value = _get(record, "fallback_locale", default=None)
        if _missing(fallback_value):
            continue
        fallback_key = _locale_key(fallback_value)
        if not fallback_key or fallback_key not in parsed_by_key:
            _add(result, "FALLBACK_TARGET_UNKNOWN", "ERROR", f"{record.get('locale')} fallback target does not exist", path=f"locales[{index}].fallback_locale")
        elif fallback_key == locale_key:
            _add(result, "FALLBACK_CYCLE", "ERROR", f"{record.get('locale')} cannot fall back to itself", path=f"locales[{index}].fallback_locale")
        fallback_map[locale_key] = fallback_key
        if fallback_policy == "NO_FALLBACK":
            _add(result, "FALLBACK_POLICY_CONFLICT", "ERROR", "NO_FALLBACK cannot declare fallback_locale values", path=f"locales[{index}].fallback_locale")
    _validate_fallback_cycles(fallback_map, result)
    for field, record_key in (("source", "source"), ("default", "default")):
        for index, record in enumerate(records):
            if record_key in record and not isinstance(record[record_key], bool):
                _add(result, "BOOLEAN_FIELD_INVALID", "ERROR", f"locales[{index}].{field} must be boolean", path=f"locales[{index}].{field}")
    for key, parsed in parsed_by_key.items():
        record = next((item for item in records if _locale_key(item.get("locale")) == key), {})
        enabled = record.get("enabled", True)
        if enabled is False and (key == source_key or key == default_key):
            _add(result, "PRIMARY_LOCALE_DISABLED", "ERROR", f"{record.get('locale')} cannot be disabled as source/default locale", path=f"locales/{record.get('locale')}/enabled")
        if enabled is True:
            for field in ("enabled", "default", "source"):
                if field not in record:
                    _add(result, "LOCALE_REGISTRY_FIELD_MISSING", "BLOCKED", f"{record.get('locale')} must declare {field}", path=f"locales[{record.get('locale')}].{field}")
            if not _text(_get(record, "direction", default="")):
                _add(result, "DIRECTION_MISSING", "BLOCKED", f"{record.get('locale')} must declare direction", path=f"locales[{record.get('locale')}].direction")
            if not _text(_get(record, "content_coverage", default="")):
                _add(result, "CONTENT_COVERAGE_MISSING", "BLOCKED", f"{record.get('locale')} must declare content coverage", path=f"locales[{record.get('locale')}].content_coverage")
            if not _text(_get(record, "translation_owner", default="")):
                _add(result, "LOCALE_TRANSLATION_OWNER_MISSING", "BLOCKED", f"{record.get('locale')} must declare translation ownership", path=f"locales[{record.get('locale')}].translation_owner")
            if "fallback_locale" not in record:
                _add(result, "LOCALE_FALLBACK_UNDECLARED", "BLOCKED", f"{record.get('locale')} must declare fallback behavior", path=f"locales[{record.get('locale')}].fallback_locale")
            if "seo_enabled" not in record:
                _add(result, "LOCALE_SEO_STATUS_MISSING", "BLOCKED", f"{record.get('locale')} must declare SEO participation", path=f"locales[{record.get('locale')}].seo_enabled")
            if not _text(_get(record, "status", default="")):
                _add(result, "LOCALE_STATUS_MISSING", "BLOCKED", f"{record.get('locale')} must declare status", path=f"locales[{record.get('locale')}].status")
            if not _text(_get(record, "review_status", default="")):
                _add(result, "LOCALE_REVIEW_STATUS_MISSING", "BLOCKED", f"{record.get('locale')} must declare review status", path=f"locales[{record.get('locale')}].review_status")
    return _finish(result)


def validate_localization_state(state: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the single ``localization{}`` readiness state."""

    result = _new_result()
    if not isinstance(state, Mapping):
        _add(result, "LOCALIZATION_STATE_MISSING", "BLOCKED", "localization state must be an object")
        return _finish(result)
    forbidden = sorted(key for key in state if str(key).lower().endswith("_locked") or str(key).lower() in {"i18n_locked", "language_locked", "translation_locked"})
    if forbidden:
        _add(result, "LOCALIZATION_LOCK_FORBIDDEN", "ERROR", f"localization state cannot create owner locks: {forbidden}", path="localization")
    for key in ("required", "complete", "fallback_policy_defined", "seo_localization_ready", "content_localization_ready", "rtl_required", "translation_review_required", "implementation_verified", "production_verified"):
        if key in state and not isinstance(state[key], bool):
            _add(result, "LOCALIZATION_STATE_BOOLEAN", "ERROR", f"localization.{key} must be boolean", path=key)
    status_present = "status" in state
    status = _upper(state.get("status")) if status_present else ""
    if status_present and status not in LOCALIZATION_STATUSES:
        _add(result, "LOCALIZATION_STATUS_INVALID", "ERROR", f"localization.status {status!r} is unsupported", path="status")
    required = state.get("required", False)
    if required is False:
        if state.get("complete") is True:
            _add(result, "LOCALIZATION_NOT_REQUIRED_COMPLETE", "ERROR", "localization cannot be complete when required is false", path="complete")
        if status_present and status not in {"NOT_REQUIRED", "EXCEPTION_APPLIED"}:
            _add(result, "LOCALIZATION_STATUS_INCONSISTENT", "ERROR", "non-required localization must be NOT_REQUIRED or EXCEPTION_APPLIED", path="status")
    else:
        source_key = _locale_key(state.get("source_locale"))
        default_key = _locale_key(state.get("default_locale"))
        if not source_key:
            _add(result, "SOURCE_LOCALE_REQUIRED", "BLOCKED", "required localization state needs source_locale", path="source_locale")
        if not default_key:
            _add(result, "DEFAULT_LOCALE_REQUIRED", "BLOCKED", "required localization state needs default_locale", path="default_locale")
        supported = state.get("supported_locales")
        supported_keys: list[str] = []
        if not isinstance(supported, list) or not supported:
            _add(result, "SUPPORTED_LOCALES_REQUIRED", "BLOCKED", "required localization state needs supported_locales", path="supported_locales")
        else:
            for index, locale in enumerate(supported):
                key = _locale_key(locale)
                if not key:
                    _add(result, "INVALID_LOCALE_CODE", "ERROR", "supported_locales entries must be valid locale identifiers", path=f"supported_locales[{index}]")
                elif key in supported_keys:
                    _add(result, "DUPLICATE_LOCALE", "ERROR", f"supported_locales contains {locale!r} more than once", path=f"supported_locales[{index}]")
                else:
                    supported_keys.append(key)
            if source_key and source_key not in supported_keys:
                _add(result, "SOURCE_LOCALE_UNKNOWN", "ERROR", "source_locale must be included in supported_locales", path="source_locale")
            if default_key and default_key not in supported_keys:
                _add(result, "DEFAULT_LOCALE_UNKNOWN", "ERROR", "default_locale must be included in supported_locales", path="default_locale")
        route_strategy = _upper(state.get("route_strategy"))
        if route_strategy and route_strategy not in ROUTE_STRATEGIES:
            _add(result, "ROUTE_STRATEGY_INVALID", "ERROR", "localization.route_strategy is unsupported", path="route_strategy")
        if state.get("complete") is True:
            required_flags = ("fallback_policy_defined", "seo_localization_ready", "content_localization_ready")
            missing = [key for key in required_flags if state.get(key) is not True]
            if missing:
                _add(result, "LOCALIZATION_INCOMPLETE", "BLOCKED", f"complete localization state is missing required readiness facts: {missing}", path="complete")
            if not route_strategy:
                _add(result, "ROUTE_STRATEGY_MISSING", "BLOCKED", "complete localization state needs route_strategy", path="route_strategy")
            if status_present and status not in {"READY", "IMPLEMENTED", "VERIFIED"}:
                _add(result, "LOCALIZATION_STATUS_INCONSISTENT", "ERROR", "complete localization must use READY, IMPLEMENTED, or VERIFIED status", path="status")
    blocked_reason = state.get("blocked_reason")
    if status_present and status == "BLOCKED" and not _text(blocked_reason):
        _add(result, "LOCALIZATION_BLOCK_REASON_MISSING", "BLOCKED", "BLOCKED localization state requires blocked_reason", path="blocked_reason")
    if state.get("complete") is True and _text(blocked_reason):
        _add(result, "LOCALIZATION_BLOCKED_COMPLETE_CONFLICT", "ERROR", "complete localization state cannot retain blocked_reason", path="blocked_reason")
    exception = state.get("exception")
    if exception is not None:
        if not isinstance(exception, Mapping) or not isinstance(exception.get("applied"), bool) or "reason" not in exception:
            _add(result, "LOCALIZATION_EXCEPTION_INVALID", "ERROR", "localization.exception needs boolean applied and reason", path="exception")
        elif exception.get("applied") and not _text(exception.get("reason")):
            _add(result, "LOCALIZATION_EXCEPTION_INVALID", "ERROR", "an applied localization exception needs a reason", path="exception.reason")
        elif not exception.get("applied") and not _missing(exception.get("reason")):
            _add(result, "LOCALIZATION_EXCEPTION_INVALID", "ERROR", "a non-applied localization exception cannot retain a reason", path="exception.reason")
    return _finish(result)


def _parse_timestamp(value: Any) -> Optional[datetime]:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def detect_stale_translation(record: Mapping[str, Any], current_source_version: Optional[str] = None) -> bool:
    """Return whether source identity/timestamps prove a translation is stale."""

    if record.get("stale") is True:
        return True
    source_version = _text(_get(record, "source_text_version", "source_version", default=""))
    current = _text(current_source_version or _get(record, "current_source_text_version", "current_source_version", default=""))
    if source_version and current and source_version != current:
        return True
    source_changed = _parse_timestamp(_get(record, "source_changed_at", default=None))
    translated_at = _parse_timestamp(_get(record, "translated_at", default=None))
    return bool(source_changed and translated_at and source_changed > translated_at)


def _is_legal_record(record: Mapping[str, Any]) -> bool:
    if record.get("legal_content") is True or record.get("legal") is True:
        return True
    text = " ".join(_text(_get(record, key, default="")) for key in ("content_type", "field_id", "content_id", "source_text"))
    return bool(re.search(r"(?i)(?:^|[^a-z0-9])(?:legal|privacy|terms|policy|consent|disclaimer)(?:$|[^a-z0-9])", text))


def _claim_rank(value: Any) -> int:
    upper = _upper(value)
    if upper in STRENGTH_RANK:
        return STRENGTH_RANK[upper]
    lower = _text(value).lower()
    if any(term in lower for term in STRENGTHENING_TERMS):
        return 5
    if any(term in lower for term in HEDGING_TERMS):
        return 1
    return 0


def validate_translation_record(record: Mapping[str, Any], *, current_source_version: Optional[str] = None) -> dict[str, Any]:
    result = _new_result()
    if not isinstance(record, Mapping):
        _add(result, "TRANSLATION_RECORD_SHAPE", "ERROR", "translation record must be an object")
        return _finish(result)
    record_id = _text(_get(record, "translation_id", "id", "content_id", default="")) or None
    target_locale = _get(record, "target_locale", "locale", default=None)
    status = _upper(_get(record, "translation_status", "status", default=""))
    if status == "MACHINE_TRANSLATED":
        status = "MACHINE_DRAFT"
    if status not in TRANSLATION_STATUSES:
        _add(result, "TRANSLATION_STATUS_INVALID", "ERROR", f"translation status {status!r} is unsupported", path="translation_status", record_id=record_id)
    if target_locale is not None and not is_valid_locale_code(target_locale):
        _add(result, "INVALID_LOCALE_CODE", "ERROR", "translation target locale is invalid", path="target_locale", record_id=record_id)
    source_locale = _get(record, "source_locale", default=None)
    if source_locale is not None and not is_valid_locale_code(source_locale):
        _add(result, "INVALID_LOCALE_CODE", "ERROR", "translation source locale is invalid", path="source_locale", record_id=record_id)
    if status not in {"SOURCE", "NOT_TRANSLATED", ""}:
        provenance_fields = ("source_locale", "target_locale", "source_text_version", "translation_method", "review_status", "reviewer")
        missing = [field for field in provenance_fields if _missing(_get(record, field, default=None))]
        if missing:
            _add(result, "TRANSLATION_PROVENANCE_INCOMPLETE", "BLOCKED", f"translation provenance is missing {missing}", path="provenance", record_id=record_id)
    review_status = _upper(_get(record, "review_status", "review", default=""))
    if review_status and review_status not in REVIEW_STATUSES:
        _add(result, "TRANSLATION_REVIEW_STATUS_INVALID", "ERROR", f"review status {review_status!r} is unsupported", path="review_status", record_id=record_id)
    published = record.get("published") is True or record.get("publicly_visible") is True or status == "PUBLISHED"
    reviewed = (review_status in PUBLISHED_REVIEW_STATUSES) if review_status else (
        status in PUBLISHED_REVIEW_STATUSES or record.get("human_reviewed") is True or record.get("approved") is True
    )
    draft_only = status in {"MACHINE_DRAFT", "HUMAN_REVIEW_REQUIRED", "NOT_TRANSLATED"}
    if published and draft_only:
        _add(result, "MACHINE_DRAFT_PUBLISHED", "ERROR", "draft or not-translated content cannot be public even when a review field is present", path="published", record_id=record_id)
    elif published and not reviewed:
        code = "UNREVIEWED_TRANSLATION_PUBLISHED"
        _add(result, code, "ERROR", "a translation cannot be public without human/authorized review and approval", path="published", record_id=record_id)
    stale = detect_stale_translation(record, current_source_version)
    if stale:
        if status == "STALE" or record.get("stale") is True:
            _add(result, "TRANSLATION_STALE_DETECTED", "WARNING", "source identity indicates this translation is stale", path="stale", record_id=record_id)
        else:
            _add(result, "TRANSLATION_STALE", "ERROR", "source content changed after translation; mark the translation STALE", path="stale", record_id=record_id)
        if published:
            _add(result, "STALE_TRANSLATION_PUBLISHED", "ERROR", "stale translations cannot be published", path="published", record_id=record_id)
    if _is_legal_record(record):
        method = _upper(_get(record, "translation_method", "method", default=""))
        legal_reviewed = record.get("legal_reviewed") is True or _upper(_get(record, "legal_review_status", default="")) in {"APPROVED", "REVIEWED"}
        if method in {"MACHINE", "MACHINE_TRANSLATION", "MACHINE_DRAFT", "AI"} and (published or record.get("legally_approved") is True or review_status in {"APPROVED", "HUMAN_REVIEWED"}) and not legal_reviewed:
            _add(result, "LEGAL_TRANSLATION_NOT_APPROVED", "ERROR", "machine-translated legal content cannot be marked legally approved without legal review", path="legal_reviewed", record_id=record_id)
    source_claim = _get(record, "source_claim_strength", default=None)
    translated_claim = _get(record, "translated_claim_strength", "target_claim_strength", default=None)
    source_text = _text(_get(record, "source_text", default=""))
    translated_text = _text(_get(record, "translated_text", "target_text", default=""))
    if source_claim is not None and translated_claim is not None and _claim_rank(translated_claim) > _claim_rank(source_claim):
        _add(result, "CLAIM_STRENGTHENED", "ERROR", "translated claim is stronger than the source claim", path="translated_claim_strength", record_id=record_id)
    elif source_text and translated_text and any(term in source_text.lower() for term in HEDGING_TERMS) and any(term in translated_text.lower() for term in STRENGTHENING_TERMS):
        _add(result, "CLAIM_STRENGTHENED", "ERROR", "translated wording appears to strengthen a hedged source claim", path="translated_text", record_id=record_id)
    if record.get("claim") is True or source_claim is not None or _get(record, "evidence_ref", "source_evidence_ref", default=None) is not None:
        evidence_ref = _text(_get(record, "evidence_ref", default=""))
        source_evidence_ref = _text(_get(record, "source_evidence_ref", default=""))
        if not evidence_ref and not source_evidence_ref:
            _add(result, "TRANSLATED_CLAIM_PROVENANCE_MISSING", "BLOCKED", "translated claims must retain a resolvable evidence reference", path="evidence_ref", record_id=record_id)
        if evidence_ref and source_evidence_ref and evidence_ref != source_evidence_ref:
            _add(result, "TRANSLATED_CLAIM_PROVENANCE_DRIFT", "ERROR", "translated claim evidence reference differs from source without a recorded material-change decision", path="evidence_ref", record_id=record_id)
    return _finish(result)


def validate_translations(records: Any, *, current_source_versions: Optional[Mapping[str, str]] = None) -> dict[str, Any]:
    result = _new_result()
    for index, record in enumerate(_records(records, "translation_id")):
        record_id = _text(_get(record, "translation_id", "id", "content_id", default=str(index)))
        version = None
        if current_source_versions:
            key = _text(_get(record, "content_id", "source_content_id", "field_id", default=""))
            version = current_source_versions.get(key)
        child = validate_translation_record(record, current_source_version=version)
        _merge(result, f"translation:{record_id}", child)
    return _finish(result)


def _alternate_records(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, Mapping):
        return [{"hreflang": key, "href": child} for key, child in value.items()]
    return _records(value, "hreflang")


def validate_hreflang(pages: Any, *, source_locale: Optional[str] = None, require_self_reference: bool = True) -> dict[str, Any]:
    """Validate localized page language, canonical, route, and reciprocal alternates."""

    result = _new_result()
    page_records = _records(pages, "page_id")
    by_url: dict[str, Mapping[str, Any]] = {}
    by_id: dict[str, Mapping[str, Any]] = {}
    source_key = _locale_key(source_locale) if source_locale else ""
    for index, page in enumerate(page_records):
        page_id = _text(_get(page, "page_id", "id", default=str(index)))
        url = _get(page, "url", "route", "path", default=None)
        url_key = _url_identity(url, host=_route_host(page))
        locale = _get(page, "locale", default=None)
        locale_key = _locale_key(locale)
        if not url_key:
            _add(result, "LOCALE_ROUTE_MISSING", "BLOCKED", f"page {page_id} has no route", path=f"pages[{index}].url", record_id=page_id)
        elif url_key in by_url:
            _add(result, "LOCALE_ROUTE_COLLISION", "ERROR", f"page routes collide at {url_key}", path=f"pages[{index}].url", record_id=page_id)
        else:
            by_url[url_key] = page
        by_id[page_id] = page
        if not locale_key:
            _add(result, "INVALID_LOCALE_CODE", "ERROR", f"page {page_id} has no valid locale", path=f"pages[{index}].locale", record_id=page_id)
        elif not source_key:
            source_key = locale_key
        html_lang = _text(_get(page, "html_lang", "lang", default=""))
        if not html_lang or _locale_key(html_lang) != locale_key:
            _add(result, "HTML_LANG_MISMATCH", "ERROR", f"page {page_id} document language does not match its locale", path=f"pages[{index}].html_lang", record_id=page_id)
        canonical = _url_identity(_get(page, "canonical", "canonical_url", default=None), host=_route_host(page))
        if page.get("indexable", True) is not False and not canonical:
            _add(result, "CANONICAL_MISSING", "BLOCKED", f"indexable page {page_id} needs a canonical URL", path=f"pages[{index}].canonical", record_id=page_id)
        if canonical and url_key and canonical != url_key and page.get("canonical_exception") is not True:
            _add(result, "CANONICAL_NOT_SELF_REFERENCING", "ERROR", f"localized page {page_id} canonicalizes away from its own route", path=f"pages[{index}].canonical", record_id=page_id)
        if page.get("route_exists") is False:
            _add(result, "LOCALE_ROUTE_MISSING", "ERROR", f"page {page_id} route is recorded as unresolved", path=f"pages[{index}].route_exists", record_id=page_id)

    for index, page in enumerate(page_records):
        page_id = _text(_get(page, "page_id", "id", default=str(index)))
        locale_key = _locale_key(page.get("locale"))
        url_key = _url_identity(_get(page, "url", "route", "path", default=None), host=_route_host(page))
        alternates = _alternate_records(_get(page, "hreflang", "alternates", default=[]))
        if page.get("hreflang_required") is True and not alternates:
            _add(result, "HREFLANG_MISSING", "BLOCKED", f"page {page_id} requires hreflang alternates", path=f"pages[{index}].hreflang", record_id=page_id)
        alternate_keys: set[str] = set()
        for alt_index, alternate in enumerate(alternates):
            code = _text(_get(alternate, "hreflang", "locale", default=""))
            href = _get(alternate, "href", "url", default=None)
            if code.lower() != "x-default" and not is_valid_locale_code(code):
                _add(result, "INVALID_HREFLANG_CODE", "ERROR", f"page {page_id} has an invalid hreflang code", path=f"pages[{index}].hreflang[{alt_index}]", record_id=page_id)
                continue
            href_key = _url_identity(href)
            if not href_key or href_key not in by_url:
                _add(result, "HREFLANG_TARGET_MISSING", "ERROR", f"page {page_id} hreflang target does not resolve", path=f"pages[{index}].hreflang[{alt_index}].href", record_id=page_id)
                continue
            target = by_url[href_key]
            if code.lower() != "x-default" and _locale_key(target.get("locale")) != _locale_key(code):
                _add(result, "HREFLANG_TARGET_LOCALE_MISMATCH", "ERROR", f"page {page_id} alternate target locale does not match hreflang", path=f"pages[{index}].hreflang[{alt_index}]", record_id=page_id)
            if code.lower() != "x-default":
                alternate_keys.add(_locale_key(code))
                target_alternates = _alternate_records(_get(target, "hreflang", "alternates", default=[]))
                reciprocal = any(_locale_key(_get(item, "hreflang", "locale", default="")) == locale_key and _url_identity(_get(item, "href", "url", default=None)) == url_key for item in target_alternates)
                if not reciprocal:
                    _add(result, "HREFLANG_RECIPROCITY_MISSING", "ERROR", f"page {page_id} alternate {code} does not reciprocate", path=f"pages[{index}].hreflang[{alt_index}]", record_id=page_id)
        if require_self_reference and alternates and locale_key not in alternate_keys:
            _add(result, "HREFLANG_SELF_REFERENCE_MISSING", "ERROR", f"page {page_id} is missing a self-referencing hreflang alternate", path=f"pages[{index}].hreflang", record_id=page_id)

    title_by_content: dict[str, str] = {}
    for page in page_records:
        content_id = _text(_get(page, "content_id", "page_group", default=""))
        if content_id and _locale_key(page.get("locale")) == source_key:
            title_by_content[content_id] = _text(_get(page, "title", "seo_title", default=""))
    for index, page in enumerate(page_records):
        content_id = _text(_get(page, "content_id", "page_group", default=""))
        title = _text(_get(page, "title", "seo_title", default=""))
        if content_id and _locale_key(page.get("locale")) != source_key and title and title == title_by_content.get(content_id):
            _add(result, "UNTRANSLATED_SEO_TITLE", "ERROR", "localized page title is identical to the source title without an explicit intentional exception", path=f"pages[{index}].title")
    return _finish(result)


def validate_formatting(formatting: Mapping[str, Any], *, locales: Any = None) -> dict[str, Any]:
    result = _new_result()
    if not isinstance(formatting, Mapping):
        _add(result, "FORMATTING_POLICY_MISSING", "BLOCKED", "localization formatting policy must be an object")
        return _finish(result)
    for key in ("date_strategy", "time_strategy", "number_strategy", "currency_strategy", "unit_strategy", "pluralization_strategy", "interpolation_strategy"):
        if key not in formatting or not _text(formatting[key]):
            _add(result, "FORMATTING_POLICY_MISSING", "BLOCKED", f"{key} must be a non-empty strategy", path=key)
    values = " ".join(_text(value) for value in formatting.values() if isinstance(value, str))
    if HARD_CODED_DATE.search(values) or formatting.get("hard_coded_dates") is True:
        _add(result, "HARDCODED_DATE_FORMAT", "ERROR", "date display must use locale-aware formatting, not a fixed US date mask", path="date_strategy")
    if formatting.get("currency_inferred_from_language") is True or formatting.get("currency_from_language_only") is True:
        _add(result, "CURRENCY_INFERRED_FROM_LANGUAGE", "ERROR", "currency must be recorded explicitly and cannot be inferred from language", path="currency_by_locale")
    if formatting.get("hard_coded_number_format") is True or formatting.get("number_punctuation_hard_coded") is True:
        _add(result, "HARDCODED_NUMBER_FORMAT", "ERROR", "number display must use locale-aware grouping and decimal formatting", path="number_strategy")
    if formatting.get("timezone_required") is True and not _text(_get(formatting, "timezone_strategy", "display_timezone", "time_zone", default="")):
        _add(result, "TIMEZONE_POLICY_MISSING", "BLOCKED", "displayed times need an explicit timezone policy", path="timezone_strategy")
    currency_map = _get(formatting, "currency_by_locale", "currencies", default=None)
    if currency_map is not None and not isinstance(currency_map, Mapping):
        _add(result, "CURRENCY_MAP_INVALID", "ERROR", "currency_by_locale must map locale identifiers to explicit currency codes", path="currency_by_locale")
        currency_map = {}
    if currency_map is None:
        currency_map = {}
    if isinstance(currency_map, Mapping):
        for locale, currency in currency_map.items():
            if not _text(currency):
                _add(result, "CURRENCY_MISSING", "BLOCKED", f"currency is missing for {locale}", path=f"currency_by_locale.{locale}")
    if formatting.get("automatic_unit_conversion") is True and not _text(formatting.get("unit_conversion_rule")):
        _add(result, "UNIT_CONVERSION_RULE_MISSING", "BLOCKED", "automatic unit conversion needs an explicit business/precision rule", path="unit_conversion_rule")
    if locales:
        locale_keys = [_locale_key(item.get("locale") if isinstance(item, Mapping) else item) for item in _list(locales)]
        if isinstance(currency_map, Mapping):
            for key in locale_keys:
                if key and not any(_locale_key(locale) == key for locale in currency_map):
                    _add(result, "CURRENCY_MISSING", "BLOCKED", f"currency is not explicit for {key}", path="currency_by_locale")
    return _finish(result)


def validate_ui_strings(strings: Any, *, required_locales: Any = None) -> dict[str, Any]:
    result = _new_result()
    for index, record in enumerate(_records(strings, "message_id")):
        message_id = _text(_get(record, "message_id", "id", "key", default=""))
        if not message_id or not SEMANTIC_MESSAGE_ID.fullmatch(message_id) or re.search(r"(?i)(?:click_here|_english|submit_now|translated)", message_id):
            _add(result, "UI_MESSAGE_ID_INVALID", "ERROR", "localized UI strings need stable semantic message identifiers", path=f"ui_strings[{index}].message_id", record_id=message_id or None)
        source_message = _text(_get(record, "source_message", "message", default=""))
        if not source_message:
            _add(result, "UI_SOURCE_MESSAGE_MISSING", "BLOCKED", "localized UI strings need a source message", path=f"ui_strings[{index}].source_message", record_id=message_id or None)
        construction = _upper(_get(record, "construction", "assembly", default=""))
        if record.get("uses_concatenation") is True or record.get("concatenation") is True or construction == "CONCATENATION" or CONCATENATION.search(_text(_get(record, "source_expression", "code", default=""))):
            _add(result, "UI_STRING_CONCATENATION", "ERROR", "localized UI messages cannot be assembled through unsafe string concatenation", path=f"ui_strings[{index}]", record_id=message_id or None)
        interpolation_safe = _get(record, "interpolation_safe", "safe_interpolation", default=None)
        if interpolation_safe is False or record.get("unsafe_interpolation") is True or _upper(_get(record, "interpolation_strategy", default="")) in {"UNSAFE", "STRING_CONCATENATION"}:
            _add(result, "UNSAFE_INTERPOLATION", "ERROR", "localized UI messages must use escaped named interpolation", path=f"ui_strings[{index}]", record_id=message_id or None)
        variables = set(re.findall(r"\{([A-Za-z][A-Za-z0-9_.-]*)\}", source_message))
        has_count = record.get("count_variable") is not None or record.get("count") is not None or "{count}" in _text(_get(record, "source_message", "message", default=""))
        if has_count and not (record.get("uses_plural_categories") is True or record.get("pluralized") is True or _upper(record.get("format", "")) in {"ICU", "MESSAGE_FORMAT", "CLDR"}):
            _add(result, "PLURALIZATION_UNSAFE", "ERROR", "count-bearing messages must use standards-aware plural categories", path=f"ui_strings[{index}]", record_id=message_id or None)
        if required_locales:
            translations = record.get("translations")
            if not isinstance(translations, Mapping):
                _add(result, "UI_TRANSLATION_MISSING", "ERROR", "required localized UI messages must declare translations for every supported locale", path=f"ui_strings[{index}].translations", record_id=message_id or None)
            else:
                translation_keys = {_locale_key(key) for key in translations}
                missing = [locale for locale in required_locales if _locale_key(locale) not in translation_keys]
                if missing:
                    _add(result, "UI_TRANSLATION_MISSING", "ERROR", f"UI message has no translation for {missing}", path=f"ui_strings[{index}].translations", record_id=message_id or None)
                for locale, translated in translations.items():
                    translated_text = _text(translated)
                    translated_variables = set(re.findall(r"\{([A-Za-z][A-Za-z0-9_.-]*)\}", translated_text))
                    if variables - translated_variables:
                        _add(result, "INTERPOLATION_VARIABLE_MISSING", "ERROR", f"translation for {locale} omits interpolation variables {sorted(variables - translated_variables)}", path=f"ui_strings[{index}].translations.{locale}", record_id=message_id or None)
                    if translated_variables - variables:
                        _add(result, "INTERPOLATION_VARIABLE_UNEXPECTED", "ERROR", f"translation for {locale} adds interpolation variables {sorted(translated_variables - variables)}", path=f"ui_strings[{index}].translations.{locale}", record_id=message_id or None)
        elif isinstance(record.get("translations"), Mapping):
            translations = record["translations"]
            for locale, translated in translations.items():
                translated_text = _text(translated)
                translated_variables = set(re.findall(r"\{([A-Za-z][A-Za-z0-9_.-]*)\}", translated_text))
                if variables - translated_variables:
                    _add(result, "INTERPOLATION_VARIABLE_MISSING", "ERROR", f"translation for {locale} omits interpolation variables {sorted(variables - translated_variables)}", path=f"ui_strings[{index}].translations.{locale}", record_id=message_id or None)
                if translated_variables - variables:
                    _add(result, "INTERPOLATION_VARIABLE_UNEXPECTED", "ERROR", f"translation for {locale} adds interpolation variables {sorted(translated_variables - variables)}", path=f"ui_strings[{index}].translations.{locale}", record_id=message_id or None)
    return _finish(result)


def validate_rtl(locales: Any, pages: Any = None, *, logical_css: Optional[Mapping[str, Any]] = None) -> dict[str, Any]:
    result = _new_result()
    locale_records = _locale_records(locales)
    rtl_keys: set[str] = set()
    for index, record in enumerate(locale_records):
        parsed = parse_locale(record.get("locale"))
        if parsed is None:
            continue
        direction = _text(record.get("direction", "")).lower()
        if parsed["language"] in RTL_LANGUAGES:
            rtl_keys.add(parsed["canonical"].lower())
            if direction != "rtl":
                _add(result, "RTL_DIRECTION_MISMATCH", "ERROR", f"{record.get('locale')} must use direction=rtl", path=f"locales[{index}].direction")
            mirror_policy = _get(record, "mirror_policy", "icon_mirroring_policy", default=None)
            if not isinstance(mirror_policy, Mapping) or not mirror_policy:
                _add(result, "RTL_ICON_POLICY_MISSING", "BLOCKED", "RTL locales need an explicit directional-icon and brand-mark mirroring policy", path=f"locales[{index}].mirror_policy")
            elif mirror_policy.get("brand_logo") is True:
                _add(result, "RTL_BRAND_MARK_MIRRORED", "ERROR", "brand marks must not be mirrored mechanically in RTL", path=f"locales[{index}].mirror_policy.brand_logo")
    for index, page in enumerate(_records(pages, "page_id")):
        if _locale_key(page.get("locale")) in rtl_keys:
            direction = _text(_get(page, "direction", "dir", "html_dir", default="")).lower()
            if direction != "rtl":
                _add(result, "RTL_PAGE_DIRECTION_MISMATCH", "ERROR", "RTL page must expose dir=rtl", path=f"pages[{index}].direction")
            if page.get("rtl_layout_verified") is not True or page.get("rtl_focus_verified") is not True:
                _add(result, "RTL_LAYOUT_UNVERIFIED", "BLOCKED", "RTL layout and focus behavior need verification", path=f"pages[{index}]")
    if rtl_keys and logical_css is not None:
        if logical_css.get("required") is True and logical_css.get("uses_logical_properties") is not True:
            _add(result, "LOGICAL_CSS_REQUIRED", "ERROR", "localized RTL builds must use logical CSS properties where practical", path="logical_css")
    return _finish(result)


def validate_typography(locales: Any, fonts: Any) -> dict[str, Any]:
    result = _new_result()
    locale_records = _locale_records(locales)
    font_records = _records(fonts, "font_id")
    for index, locale in enumerate(locale_records):
        parsed = parse_locale(locale.get("locale"))
        if parsed is None:
            continue
        target_script = _script_for(parsed)
        if not target_script or parsed["language"] in {"en", "es", "fr", "de", "it", "pt", "nl"}:
            continue
        applicable = []
        for font in font_records:
            scopes = {_text(value).lower() for value in _list(_get(font, "locales", "supported_locales", "scripts", "supported_scripts", default=[]))}
            if not scopes or target_script.lower() in scopes or parsed["language"] in scopes or _locale_key(parsed["canonical"]) in scopes:
                applicable.append(font)
        if not applicable:
            _add(result, "LOCALE_FONT_COVERAGE_UNVERIFIED", "BLOCKED", f"no font records cover the {target_script} script for {locale.get('locale')}", path=f"locales[{index}].typography")
            continue
        for font in applicable:
            coverage = _get(font, "glyph_coverage", "script_coverage", default=None)
            supported = _get(font, "supported_scripts", "scripts", default=[])
            if coverage is False or (supported and target_script.lower() not in {_text(value).lower() for value in _list(supported)} and parsed["language"] not in {_text(value).lower() for value in _list(supported)}):
                _add(result, "LOCALE_FONT_COVERAGE_UNVERIFIED", "ERROR", f"font {_get(font, 'font_id', 'id', default='unknown')} lacks required {target_script} coverage", path="fonts", record_id=_text(_get(font, "font_id", "id", default="")) or None)
            license_status = _upper(_get(font, "license_status", "license", default=""))
            redistribution = _upper(_get(font, "redistribution_status", "redistribution", default=""))
            if license_status not in {"VERIFIED", "APPROVED", "PERMITTED"} or redistribution in {"UNRESOLVED", "UNKNOWN", "FORBIDDEN", "NOT_REVIEWED"}:
                _add(result, "LOCALE_FONT_LICENSE_UNRESOLVED", "ERROR", f"font {_get(font, 'font_id', 'id', default='unknown')} lacks resolved web/redistribution provenance", path="fonts", record_id=_text(_get(font, "font_id", "id", default="")) or None)
            if not _text(_get(font, "provenance_ref", "evidence_ref", "source_ref", default="")):
                _add(result, "LOCALE_FONT_PROVENANCE_MISSING", "BLOCKED", f"font {_get(font, 'font_id', 'id', default='unknown')} lacks a V2.12 provenance reference", path="fonts", record_id=_text(_get(font, "font_id", "id", default="")) or None)
            if font.get("web_use") is False or font.get("webfont_permitted") is False:
                _add(result, "LOCALE_FONT_WEB_USE_FORBIDDEN", "ERROR", f"font {_get(font, 'font_id', 'id', default='unknown')} is not cleared for web use", path="fonts", record_id=_text(_get(font, "font_id", "id", default="")) or None)
            for coverage_field in ("punctuation_coverage", "numeral_coverage", "weight_coverage"):
                if coverage_field in font and font[coverage_field] is False:
                    _add(result, "LOCALE_FONT_GLYPH_COVERAGE_UNVERIFIED", "ERROR", f"font {_get(font, 'font_id', 'id', default='unknown')} lacks {coverage_field.replace('_', ' ')}", path=f"fonts.{coverage_field}", record_id=_text(_get(font, "font_id", "id", default="")) or None)
    return _finish(result)


def validate_assets(assets: Any) -> dict[str, Any]:
    result = _new_result()
    for index, asset in enumerate(_records(assets, "asset_id")):
        asset_id = _text(_get(asset, "asset_id", "id", default=str(index)))
        text = " ".join(_text(value).lower() for value in asset.values() if isinstance(value, str))
        production = _upper(_get(asset, "production_status", "status", default="")) in {"PRODUCTION", "PRODUCTION_READY", "PUBLISHED"} or asset.get("production") is True
        if production and (asset.get("reference_only") is True or any(term in text for term in REFERENCE_ONLY_TERMS)):
            _add(result, "REFERENCE_ASSET_NOT_PRODUCTION", "ERROR", "research/reference media cannot be localized production media", path=f"assets[{index}]", record_id=asset_id)
        scope = _upper(_get(asset, "locale_scope", "scope", default="LOCALE_NEUTRAL"))
        if scope not in {"LOCALE_NEUTRAL", "LOCALE_SPECIFIC"}:
            _add(result, "ASSET_LOCALE_SCOPE_INVALID", "ERROR", "asset locale scope must be LOCALE_NEUTRAL or LOCALE_SPECIFIC", path=f"assets[{index}].locale_scope", record_id=asset_id)
        if scope == "LOCALE_SPECIFIC" and not is_valid_locale_code(_get(asset, "locale", default=None)):
            _add(result, "ASSET_LOCALE_MISSING", "BLOCKED", "locale-specific assets need a valid locale", path=f"assets[{index}].locale", record_id=asset_id)
        if (production or scope == "LOCALE_SPECIFIC") and not _text(_get(asset, "provenance_ref", "evidence_ref", default="")):
            _add(result, "ASSET_PROVENANCE_MISSING", "BLOCKED", "localized production assets need a V2.12 provenance reference", path=f"assets[{index}].provenance_ref", record_id=asset_id)
    return _finish(result)


def validate_localized_slugs(slugs: Any) -> dict[str, Any]:
    """Validate locale-scoped slug uniqueness and durable change redirects."""

    result = _new_result()
    seen: dict[tuple[str, str], str] = {}
    for index, record in enumerate(_records(slugs, "slug_id")):
        record_id = _text(_get(record, "slug_id", "id", "content_id", default=str(index)))
        locale_key = _locale_key(_get(record, "locale", "target_locale", default=None))
        if not locale_key:
            _add(result, "INVALID_LOCALE_CODE", "ERROR", "localized slug records need a valid locale", path=f"slugs[{index}].locale", record_id=record_id)
        slug_value = _get(record, "slug", "localized_slug", "path", "route", default=None)
        slug = _url_key(slug_value)
        if not slug or slug == "/":
            _add(result, "LOCALIZED_SLUG_MISSING", "BLOCKED", "localized content needs a non-empty slug or route", path=f"slugs[{index}].slug", record_id=record_id)
            continue
        key = (locale_key, slug)
        if key in seen:
            _add(result, "LOCALIZED_SLUG_COLLISION", "ERROR", f"localized slug collides with {seen[key]} at {slug}", path=f"slugs[{index}].slug", record_id=record_id)
        else:
            seen[key] = record_id
        previous = _url_key(_get(record, "previous_slug", "old_slug", "previous_route", default=None))
        if previous and previous != slug and (record.get("published") is True or record.get("redirect_required") is True or record.get("status") == "PUBLISHED"):
            redirect_status = _get(record, "redirect_status", "redirect_code", default=None)
            has_301 = str(redirect_status) == "301" or redirect_status == 301
            if not has_301:
                _add(result, "LOCALIZED_SLUG_REDIRECT_MISSING", "BLOCKED", "published localized slug changes need durable 301 redirect evidence", path=f"slugs[{index}].redirect_ref", record_id=record_id)
    return _finish(result)


def validate_content_ops_integration(content_ops: Mapping[str, Any], *, content_model: Optional[Mapping[str, Any]] = None) -> dict[str, Any]:
    result = _new_result()
    if not isinstance(content_ops, Mapping):
        _add(result, "CONTENT_OPS_INTEGRATION_MISSING", "BLOCKED", "localization must consume the V2.13 content model")
        return _finish(result)
    strategy = _upper(_get(content_ops, "strategy", "cms_strategy", default=""))
    if strategy not in {"FIELD_LEVEL_LOCALIZATION", "DOCUMENT_PER_LOCALE", "HYBRID"}:
        _add(result, "CMS_LOCALIZATION_STRATEGY_INVALID", "ERROR", "CMS localization strategy must be FIELD_LEVEL_LOCALIZATION, DOCUMENT_PER_LOCALE, or HYBRID", path="strategy")
    model_ref = _text(_get(content_ops, "content_model_ref", "model_ref", default=""))
    if not model_ref:
        _add(result, "CONTENT_MODEL_REFERENCE_MISSING", "BLOCKED", "localization must reference the V2.13 content model", path="content_model_ref")
    if content_ops.get("duplicates_content_model") is True:
        _add(result, "CONTENT_MODEL_DUPLICATED", "ERROR", "localization must not create a second CMS/content model")
    if content_ops.get("portability_reviewed") is False:
        _add(result, "LOCALIZED_CONTENT_NOT_PORTABLE", "BLOCKED", "localized content must be covered by the content export/portability strategy")
    if content_model is not None:
        localizable = set(_text(value) for value in _list(content_ops.get("localizable_fields", [])))
        non_localizable = set(_text(value) for value in _list(content_ops.get("non_localizable_fields", [])))
        for content_type in _records(_get(content_model, "content_types", "types", default=[]), "type_id"):
            for field in _records(content_type.get("fields", []), "field_id"):
                field_id = _text(_get(field, "field_id", "id", default=""))
                flag = field.get("localizable")
                if flag is True and field_id not in localizable:
                    _add(result, "LOCALIZABLE_FIELD_NOT_REGISTERED", "ERROR", f"localizable field {field_id} is absent from localization policy", path="localizable_fields")
                if flag is True and field_id in non_localizable:
                    _add(result, "LOCALIZABLE_FIELD_CONFLICT", "ERROR", f"field {field_id} is classified as both localizable and non-localizable", path="localizable_fields")
                if flag is False and field_id in localizable:
                    _add(result, "NON_LOCALIZABLE_FIELD_TRANSLATED", "ERROR", f"non-localizable field {field_id} was included in localization policy", path="localizable_fields")
                if flag is False and field_id not in non_localizable:
                    _add(result, "NON_LOCALIZABLE_FIELD_NOT_REGISTERED", "ERROR", f"non-localizable field {field_id} is absent from localization policy", path="non_localizable_fields")
    return _finish(result)


def validate_accessibility_integration(accessibility: Mapping[str, Any]) -> dict[str, Any]:
    result = _new_result()
    if not isinstance(accessibility, Mapping):
        _add(result, "ACCESSIBILITY_INTEGRATION_MISSING", "BLOCKED", "localization must consume the V2.9 accessibility authority")
        return _finish(result)
    switcher_required = accessibility.get("locale_switcher_required", True)
    if not isinstance(switcher_required, bool):
        _add(result, "BOOLEAN_FIELD_INVALID", "ERROR", "locale_switcher_required must be boolean", path="locale_switcher_required")
        switcher_required = True
    if switcher_required is True and accessibility.get("locale_switcher_accessible") is not True:
        _add(result, "LOCALE_SWITCHER_INACCESSIBLE", "ERROR", "locale switcher must be keyboard and screen-reader accessible")
    if accessibility.get("flag_only_selector") is True:
        _add(result, "FLAG_ONLY_LOCALE_SELECTOR", "ERROR", "flags cannot be the sole language selector label")
    for key in ("keyboard_accessible", "screen_reader_accessible", "current_locale_exposed"):
        if switcher_required is True and accessibility.get(key) is not True:
            _add(result, "LOCALE_SWITCHER_INACCESSIBLE", "ERROR", f"locale switcher is missing {key}", path=key)
    if switcher_required is True and (accessibility.get("translated_form_errors") is not True or accessibility.get("translated_labels") is not True):
        _add(result, "LOCALIZED_FORM_ACCESSIBILITY_MISSING", "ERROR", "localized forms need translated labels and errors")
    return _finish(result)


def validate_analytics_locale(analytics: Mapping[str, Any]) -> dict[str, Any]:
    result = _new_result()
    if not isinstance(analytics, Mapping):
        _add(result, "ANALYTICS_INTEGRATION_MISSING", "BLOCKED", "localization analytics integration must be an object with explicit locale-parameter policy")
        return _finish(result)
    events = _records(_get(analytics, "events", "event_manifest", default=[]), "event_name")
    for index, event in enumerate(events):
        name = _text(_get(event, "event_name", "name", default=""))
        if not name:
            continue
        locale_specific = _text(_get(event, "locale", "language", default=""))
        if locale_specific and analytics.get("locale_parameter") is not True:
            _add(result, "ANALYTICS_EVENT_LOCALE_ARCHITECTURE", "ERROR", "locale must be an event parameter, not a separate event identity", path=f"events[{index}].event_name")
        if re.search(r"(?i)(?:^|[_-])(en|es|fr|de|ar|mx|us)(?:[_-]|$)", name) and analytics.get("locale_parameter") is not True:
            _add(result, "DUPLICATE_LOCALE_ANALYTICS_EVENT", "ERROR", "do not create one analytics event name per language", path=f"events[{index}].event_name")
        parameters = _get(event, "parameters", "params", default=[])
        parameter_names = {_text(_get(parameter, "name", "key", default=parameter)) for parameter in _list(parameters)}
        if analytics.get("locale_parameter_required") is True and "locale" not in parameter_names and not locale_specific:
            _add(result, "ANALYTICS_LOCALE_PARAMETER_MISSING", "BLOCKED", "each measured event must expose locale as a parameter", path=f"events[{index}].parameters")
    if analytics.get("locale_parameter_required") is True and analytics.get("locale_parameter") is not True:
        _add(result, "ANALYTICS_LOCALE_PARAMETER_MISSING", "BLOCKED", "measurement must record locale as a parameter where required", path="locale_parameter")
    return _finish(result)


def validate_handoff_integration(handoff: Mapping[str, Any]) -> dict[str, Any]:
    result = _new_result()
    if not isinstance(handoff, Mapping):
        _add(result, "LOCALIZATION_HANDOFF_MISSING", "BLOCKED", "localization inputs must transfer through the existing V2.5 handoff authority")
        return _finish(result)
    required_fields = ("locale_list", "source_locale", "translation_workflow", "cms_localization_model", "review_responsibilities", "stale_translation_process", "localized_asset_responsibilities", "seo_localization_process")
    for key in required_fields:
        if key not in handoff or _missing(handoff.get(key)):
            _add(result, "LOCALIZATION_HANDOFF_FIELD_MISSING", "BLOCKED", f"handoff field {key} is empty", path=key)
    if "provider_dependencies" not in handoff:
        _add(result, "LOCALIZATION_HANDOFF_FIELD_MISSING", "BLOCKED", "handoff field provider_dependencies is missing", path="provider_dependencies")
    if handoff.get("duplicates_v25_handoff") is True:
        _add(result, "HANDOFF_AUTHORITY_DUPLICATED", "ERROR", "localization must feed V2.5 handoff, not create a second handoff authority")
    return _finish(result)


def pseudolocalize(text: Any) -> str:
    """Apply a deterministic pseudo-locale transformation; never a translation."""

    value = _text(text)
    if not value:
        return "[!! !!]"
    return "[!! " + value.translate(PSEUDO_MAP) + " - extended !!]"


def validate_pseudolocalized_items(items: Any) -> dict[str, Any]:
    result = _new_result()
    for index, item in enumerate(_records(items, "id")):
        source = _text(_get(item, "source", "text", default=""))
        pseudo = _text(_get(item, "pseudo", "pseudolocalized", default="")) or pseudolocalize(source)
        limit = _get(item, "max_chars", "available_chars", "max_length", default=None)
        if item.get("overflow") is True:
            _add(result, "PSEUDOLOCALIZATION_OVERFLOW", "ERROR", "pseudo-localized content overflows its available layout space", path=f"items[{index}]", record_id=_text(item.get("id")) or None)
        if isinstance(limit, (int, float)) and not isinstance(limit, bool) and len(pseudo) > limit:
            _add(result, "PSEUDOLOCALIZATION_OVERFLOW", "ERROR", f"pseudo-localized text length {len(pseudo)} exceeds capacity {limit}", path=f"items[{index}]", record_id=_text(item.get("id")) or None)
        expansion = _get(item, "minimum_expansion", "expansion_ratio", "expansion_target", "target_expansion", default=None)
        expansion_fraction: Optional[float] = None
        if isinstance(expansion, (int, float)) and not isinstance(expansion, bool):
            expansion_fraction = expansion / 100 if expansion > 2 else expansion - 1 if expansion >= 1 else expansion
        elif isinstance(expansion, str):
            match = re.fullmatch(r"\s*\+?\s*([0-9]+(?:\.[0-9]+)?)\s*(%|x)?\s*", expansion)
            if match:
                numeric = float(match.group(1))
                expansion_fraction = numeric / 100 if match.group(2) == "%" or numeric > 2 else numeric - 1 if numeric >= 1 else numeric
        if expansion_fraction is not None and source and expansion_fraction >= 0:
            minimum_length = int(len(source) * (1 + expansion_fraction) + 0.999999)
            if len(pseudo) < minimum_length:
                _add(result, "PSEUDOLOCALIZATION_EXPANSION_UNTESTED", "ERROR", f"pseudo-localized text length {len(pseudo)} does not exercise the requested +{int(expansion_fraction * 100)}% expansion", path=f"items[{index}]", record_id=_text(item.get("id")) or None)
    return _finish(result)


def validate_localization_manifest(manifest: Mapping[str, Any], *, current_source_versions: Optional[Mapping[str, str]] = None) -> dict[str, Any]:
    """Validate the complete provider-neutral localization manifest."""

    result = _new_result()
    if not isinstance(manifest, Mapping):
        _add(result, "LOCALIZATION_MANIFEST_MISSING", "BLOCKED", "localization manifest must be an object")
        return _finish(result)
    duplicate_state_keys = [key for key in ("i18n", "l10n", "translation_state", "internationalization") if key in manifest]
    if "state" in manifest and "localization" in manifest:
        duplicate_state_keys.extend(("state", "localization"))
    if duplicate_state_keys:
        _add(result, "DUPLICATE_LOCALIZATION_STATE", "ERROR", f"localization has duplicate state authorities: {duplicate_state_keys}")
    state = _get(manifest, "state", "localization", default=None)
    if state is not None:
        _merge(result, "state", validate_localization_state(state))
    if "required" in manifest and not isinstance(manifest.get("required"), bool):
        _add(result, "LOCALIZATION_REQUIRED_TYPE", "ERROR", "manifest required must be boolean", path="required")
    for field in ("source_locale", "default_locale"):
        if field in manifest and manifest.get(field) is not None and not is_valid_locale_code(manifest.get(field)):
            _add(result, "INVALID_LOCALE_CODE", "ERROR", f"manifest {field} is not a valid locale identifier", path=field)
    if "supported_locales" in manifest:
        if not isinstance(manifest.get("supported_locales"), list):
            _add(result, "SUPPORTED_LOCALES_INVALID", "ERROR", "manifest supported_locales must be an array", path="supported_locales")
        else:
            for index, locale in enumerate(manifest["supported_locales"]):
                if not is_valid_locale_code(locale):
                    _add(result, "INVALID_LOCALE_CODE", "ERROR", "manifest supported_locales contains an invalid locale identifier", path=f"supported_locales[{index}]")
    manifest_status = _upper(manifest.get("status", ""))
    if manifest_status and manifest_status not in LOCALIZATION_STATUSES:
        _add(result, "LOCALIZATION_STATUS_INVALID", "ERROR", f"manifest status {manifest_status!r} is unsupported", path="status")
    registry = _get(manifest, "locale_registry", default=None)
    if registry is None and ("locales" in manifest or "supported_locales" in manifest):
        registry = {
            "required": manifest.get("required", True),
            "source_locale": manifest.get("source_locale"),
            "default_locale": manifest.get("default_locale"),
            "route_strategy": manifest.get("route_strategy"),
            "default_locale_url_policy": manifest.get("default_locale_url_policy"),
            "fallback_policy": manifest.get("fallback_policy"),
            "locales": manifest.get("locales", manifest.get("supported_locales", [])),
        }
    required = manifest.get("required") is True or (isinstance(state, Mapping) and state.get("required") is True) or (isinstance(registry, Mapping) and registry.get("required") is True)
    if required and registry is None:
        _add(result, "LOCALE_REGISTRY_MISSING", "BLOCKED", "required localization must provide the canonical locale registry", path="locale_registry")
    if required and state is None:
        _add(result, "LOCALIZATION_STATE_MISSING", "BLOCKED", "required localization must provide the canonical localization state authority", path="state")
    if registry is not None:
        _merge(result, "locale_registry", validate_locale_registry(registry, required=manifest.get("required")))
    if isinstance(state, Mapping) and isinstance(registry, Mapping):
        state_required = state.get("required")
        registry_required = registry.get("required")
        if isinstance(state_required, bool) and isinstance(registry_required, bool) and state_required != registry_required:
            _add(result, "LOCALIZATION_REQUIRED_CONFLICT", "ERROR", "localization state and locale registry disagree about whether localization is required", path="required")
    if isinstance(registry, Mapping) and isinstance(manifest.get("required"), bool) and isinstance(registry.get("required"), bool) and manifest["required"] != registry["required"]:
        _add(result, "LOCALIZATION_REQUIRED_CONFLICT", "ERROR", "manifest and locale registry disagree about whether localization is required", path="required")
    locale_authorities: list[tuple[str, Mapping[str, Any]]] = [("manifest", manifest)]
    if isinstance(state, Mapping):
        locale_authorities.append(("state", state))
    if isinstance(registry, Mapping):
        locale_authorities.append(("locale_registry", registry))
    for field, issue_code in (("source_locale", "LOCALIZATION_SOURCE_LOCALE_CONFLICT"), ("default_locale", "LOCALIZATION_DEFAULT_LOCALE_CONFLICT")):
        declared = [
            (name, _locale_key(authority.get(field)))
            for name, authority in locale_authorities
            if field in authority and authority.get(field) is not None and _locale_key(authority.get(field))
        ]
        if len({key for _, key in declared}) > 1:
            details = ", ".join(f"{name}={key}" for name, key in declared)
            _add(result, issue_code, "ERROR", f"localization authorities disagree about {field}: {details}", path=field)
    supported_authorities: list[tuple[str, set[str]]] = []
    if "supported_locales" in manifest:
        supported_authorities.append(("manifest", _locale_key_set(manifest.get("supported_locales"))))
    if isinstance(state, Mapping) and "supported_locales" in state:
        supported_authorities.append(("state", _locale_key_set(state.get("supported_locales"))))
    if isinstance(registry, Mapping):
        if "supported_locales" in registry:
            supported_authorities.append(("locale_registry", _locale_key_set(registry.get("supported_locales"))))
        elif "locales" in registry:
            supported_authorities.append(("locale_registry", _locale_key_set(registry.get("locales"))))
    if len({tuple(sorted(keys)) for _, keys in supported_authorities}) > 1:
        details = ", ".join(f"{name}={sorted(keys)}" for name, keys in supported_authorities)
        _add(result, "LOCALIZATION_SUPPORTED_LOCALES_CONFLICT", "ERROR", f"localization authorities disagree about supported_locales: {details}", path="supported_locales")
    effective_source_locale = manifest.get("source_locale")
    if _missing(effective_source_locale) and isinstance(state, Mapping):
        effective_source_locale = state.get("source_locale")
    if _missing(effective_source_locale) and isinstance(registry, Mapping):
        effective_source_locale = registry.get("source_locale")
    effective_supported_locales = manifest.get("supported_locales")
    if _missing(effective_supported_locales) and isinstance(state, Mapping):
        effective_supported_locales = state.get("supported_locales")
    if _missing(effective_supported_locales) and isinstance(registry, Mapping):
        effective_supported_locales = registry.get("supported_locales")
        if _missing(effective_supported_locales):
            effective_supported_locales = [record.get("locale") for record in _registry_locales(registry)]
    if manifest.get("external_translation_provider_required") is True:
        _add(result, "EXTERNAL_TRANSLATION_PROVIDER_REQUIRED", "BLOCKED", "framework certification cannot require a network translation provider")
    if required:
        if "formatting" in manifest:
            _merge(result, "formatting", validate_formatting(manifest["formatting"], locales=_registry_locales(registry) if isinstance(registry, Mapping) else manifest.get("supported_locales")))
        if "ui_strings" in manifest:
            _merge(result, "ui_strings", validate_ui_strings(manifest["ui_strings"], required_locales=effective_supported_locales))
        if "translations" in manifest or "localized_content" in manifest:
            _merge(result, "translations", validate_translations(manifest.get("translations", manifest.get("localized_content", [])), current_source_versions=current_source_versions))
        if "pages" in manifest:
            _merge(result, "seo", validate_hreflang(manifest["pages"], source_locale=effective_source_locale))
        if "rtl" in manifest or "logical_css" in manifest:
            locales = _registry_locales(registry) if isinstance(registry, Mapping) else manifest.get("supported_locales", [])
            _merge(result, "rtl", validate_rtl(locales, manifest.get("pages"), logical_css=manifest.get("logical_css")))
        if "fonts" in manifest:
            locales = _registry_locales(registry) if isinstance(registry, Mapping) else manifest.get("supported_locales", [])
            _merge(result, "typography", validate_typography(locales, manifest["fonts"]))
        if "assets" in manifest:
            _merge(result, "assets", validate_assets(manifest["assets"]))
        if "content_ops" in manifest:
            _merge(result, "content_ops", validate_content_ops_integration(manifest["content_ops"], content_model=manifest.get("content_model")))
        if "slugs" in manifest or "localized_slugs" in manifest:
            _merge(result, "slugs", validate_localized_slugs(manifest.get("slugs", manifest.get("localized_slugs", []))))
        if "accessibility" in manifest:
            _merge(result, "accessibility", validate_accessibility_integration(manifest["accessibility"]))
        if "analytics" in manifest or "measurement" in manifest:
            _merge(result, "analytics", validate_analytics_locale(manifest.get("analytics", manifest.get("measurement", {}))))
        if "handoff" in manifest:
            _merge(result, "handoff", validate_handoff_integration(manifest["handoff"]))
        if "pseudolocalization" in manifest:
            _merge(result, "pseudolocalization", validate_pseudolocalized_items(manifest["pseudolocalization"]))
    else:
        if manifest.get("complete") is True:
            _add(result, "LOCALIZATION_NOT_REQUIRED_COMPLETE", "ERROR", "manifest cannot be complete when localization is not required", path="complete")
    return _finish(result)


def validate_localization(project: Mapping[str, Any], **kwargs: Any) -> dict[str, Any]:
    """Compatibility alias for callers that use the shorter validator name."""

    return validate_localization_manifest(project, **kwargs)


__all__ = [
    "FALLBACK_POLICIES",
    "LOCALIZATION_STATUSES",
    "ROUTE_STRATEGIES",
    "TRANSLATION_STATUSES",
    "calculate_localization_requirement",
    "detect_stale_translation",
    "is_valid_locale_code",
    "parse_locale",
    "pseudolocalize",
    "validate_accessibility_integration",
    "validate_analytics_locale",
    "validate_assets",
    "validate_content_ops_integration",
    "validate_formatting",
    "validate_handoff_integration",
    "validate_hreflang",
    "validate_localization",
    "validate_localization_manifest",
    "validate_localization_state",
    "validate_locale_registry",
    "validate_localized_slugs",
    "validate_pseudolocalized_items",
    "validate_rtl",
    "validate_translation_record",
    "validate_translations",
    "validate_typography",
    "validate_ui_strings",
]
