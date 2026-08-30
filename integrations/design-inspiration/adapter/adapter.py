"""Bounded, research-only adapter for the audited design inspiration MCP.

This module deliberately does not launch the upstream server, make HTTP
requests, download images, execute dembrandt, or write project files.  It
normalizes already-returned MCP evidence and applies the Website Director
research boundary before a candidate can enter synthesis.
"""

from __future__ import annotations

import ipaddress
import os
import re
import shutil
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


UPSTREAM_REPOSITORY = "https://github.com/YonasValentin/design-inspiration-mcp-server"
UPSTREAM_COMMIT = "2935c0775fb1cfe3d95503615901e1fa743430e8"
UPSTREAM_PACKAGE_VERSION = "1.0.0"
UPSTREAM_CHANGELOG_VERSION = "1.1.0"
UPSTREAM_LICENSE = "MIT"
MCP_PROVIDER = "design-inspiration-mcp-server"
REFERENCE_ONLY = "REFERENCE_ONLY"
TOKEN_EXTRACTION_MODE = "REFERENCE_DECONSTRUCTION_MODE"

PLATFORMS = ("Dribbble", "Behance", "Awwwards", "Mobbin", "Pinterest")
SEARCH_TOOLS = (
    "design_search_images",
    "design_search_references",
    "design_search_styles",
)
TOKEN_TOOL = "design_extract_tokens"

RUBRIC_DIMENSIONS = (
    "VISUAL_CRAFT",
    "SUBJECT_RELEVANCE",
    "DISTINCTIVENESS",
    "INFORMATION_HIERARCHY",
    "TYPOGRAPHIC_QUALITY",
    "LAYOUT_QUALITY",
    "BRAND_FIT",
    "CONVERSION_APPLICABILITY",
    "RESPONSIVE_PLAUSIBILITY",
    "ACCESSIBILITY_PLAUSIBILITY",
    "IMPLEMENTABILITY",
)

_PLATFORM_HOSTS = {
    "dribbble.com": "Dribbble",
    "behance.net": "Behance",
    "awwwards.com": "Awwwards",
    "mobbin.com": "Mobbin",
    "pinterest.com": "Pinterest",
}
_PATTERN_TYPES = {
    "Dribbble": "interface-pattern",
    "Behance": "case-study-pattern",
    "Awwwards": "showcase-benchmark",
    "Mobbin": "product-flow",
    "Pinterest": "moodboard-signal",
}
_GENERIC_QUERIES = {
    "good design",
    "nice website",
    "cool landing page",
    "best ui",
    "website inspiration",
    "design inspiration",
    "modern website",
}
_SENSITIVE_CONTEXT_KEYS = {
    "api_key",
    "apikey",
    "authorization",
    "auth",
    "bearer",
    "credential",
    "credentials",
    "password",
    "secret",
    "token",
    "serper_api_key",
}
_SENSITIVE_QUERY_PATTERNS = (
    re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|authorization|bearer|password|passwd|secret|token)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"(?i)\b(?:sk|pk|ghp|github_pat)_[a-z0-9_-]{8,}\b"),
    re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
)
_CLONE_REQUEST_PATTERN = re.compile(
    r"(?i)\b(?:clone|copy|pixel[- ]perfect|reproduce|duplicate|same exact)\b"
)
_TRACKING_QUERY_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "source",
}


def _text(value: Any) -> str:
    return value if isinstance(value, str) else str(value)


def _contains_sensitive(value: str) -> bool:
    return any(pattern.search(value) for pattern in _SENSITIVE_QUERY_PATTERNS)


def _safe_text(value: Any, limit: int = 500) -> str:
    text = re.sub(r"\s+", " ", _text(value)).strip()
    for pattern in _SENSITIVE_QUERY_PATTERNS:
        text = pattern.sub("[REDACTED_SENSITIVE_VALUE]", text)
    return text[:limit]


def _flatten_context(value: Any, key: str = "", depth: int = 0) -> list[str]:
    if depth > 2 or key.lower() in _SENSITIVE_CONTEXT_KEYS:
        return []
    if isinstance(value, Mapping):
        parts: list[str] = []
        for child_key, child_value in value.items():
            parts.extend(_flatten_context(child_value, str(child_key), depth + 1))
        return parts
    if isinstance(value, (list, tuple, set)):
        parts = []
        for child in value:
            parts.extend(_flatten_context(child, key, depth + 1))
        return parts
    if isinstance(value, str):
        if _contains_sensitive(value):
            return []
        cleaned = _safe_text(value, limit=110)
        return [cleaned] if cleaned else []
    return []


def generate_design_query(context: Mapping[str, Any]) -> str:
    """Build a specific, bounded query from project context only.

    Credentials, tokens, email addresses, and arbitrary context keys are
    excluded.  The resulting string is kept within the upstream tool's
    200-character input bound.
    """

    allowed_keys = (
        "project_brief",
        "positioning",
        "research_brief",
        "business_type",
        "audience",
        "emotional_posture",
        "design_ambition",
        "reference_mode",
        "design_goal",
        "conversion_goal",
    )
    terms: list[str] = []
    for key in allowed_keys:
        if key in context:
            terms.extend(_flatten_context(context[key], key))
    if not terms:
        raise ValueError("SPECIFIC_QUERY_CONTEXT_REQUIRED")
    unique_terms: list[str] = []
    seen: set[str] = set()
    for term in terms:
        normalized = term.lower()
        if normalized not in seen:
            seen.add(normalized)
            unique_terms.append(term)
    query = " ".join(unique_terms[:6]) + " website design interface reference patterns"
    return re.sub(r"\s+", " ", query).strip()[:200]


def validate_query(query: Any, context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Reject sensitive/generic queries or rewrite generic input from context."""

    raw = _text(query).strip()
    if _contains_sensitive(raw):
        return {
            "status": "QUERY_REJECTED_SENSITIVE",
            "query": None,
            "redacted_query": "[REDACTED_SENSITIVE_QUERY]",
            "reason": "Sensitive data is never sent to the search provider.",
        }
    normalized = re.sub(r"\s+", " ", raw)
    if len(normalized) < 2 or len(normalized) > 200:
        return {
            "status": "QUERY_REJECTED_INVALID",
            "query": None,
            "reason": "Query must be between 2 and 200 characters.",
        }
    if normalized.lower() in _GENERIC_QUERIES:
        if context is not None:
            try:
                rewritten = generate_design_query(context)
            except ValueError:
                rewritten = ""
            if rewritten:
                return {
                    "status": "QUERY_REWRITTEN_GENERIC",
                    "query": rewritten,
                    "reason": "Generic input was replaced with a project-grounded query.",
                }
        return {
            "status": "QUERY_REJECTED_GENERIC",
            "query": None,
            "reason": "A project-specific research question is required.",
        }
    return {"status": "QUERY_ACCEPTED", "query": normalized}


def credential_state(env: Mapping[str, str] | None = None, enabled: bool = True) -> dict[str, Any]:
    """Return a credential state without exposing or logging the key value."""

    if not enabled:
        return {"status": "DISABLED", "env_var": "SERPER_API_KEY", "key_present": False}
    source = os.environ if env is None else env
    present = bool(str(source.get("SERPER_API_KEY", "")).strip())
    return {
        "status": "AVAILABLE" if present else "BLOCKED_CREDENTIAL_MISSING",
        "env_var": "SERPER_API_KEY",
        "key_present": present,
    }


def bound_search_count(requested: Any = None, stage: str = "initial") -> int:
    """Apply the bounded initial/shortlist/deep research budget."""

    bounds = {"initial": (8, 6, 12), "shortlist": (3, 3, 6), "deep": (1, 1, 3)}
    if stage not in bounds:
        raise ValueError("UNKNOWN_SEARCH_STAGE")
    default, minimum, maximum = bounds[stage]
    try:
        count = default if requested is None else int(requested)
    except (TypeError, ValueError):
        count = default
    return max(minimum, min(count, maximum))


def canonicalize_url(url: Any) -> str | None:
    """Canonicalize a source URL for provenance and duplicate detection."""

    if not isinstance(url, str):
        return None
    try:
        parts = urlsplit(url.strip())
    except ValueError:
        return None
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        return None
    if parts.username or parts.password:
        return None
    host = parts.hostname.lower()
    if host.startswith("www."):
        host = host[4:]
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    if path != "/":
        path = path.rstrip("/")
    query_parts = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        if key.lower().startswith("utm_") or key.lower() in _TRACKING_QUERY_KEYS:
            continue
        query_parts.append((key, value))
    query = urlencode(sorted(query_parts))
    return urlunsplit((parts.scheme.lower(), host, path, query, ""))


def infer_platform(source: Any) -> str | None:
    """Map a supported platform URL or label to the canonical platform name."""

    value = _text(source).strip()
    lowered = value.lower()
    for label in PLATFORMS:
        if lowered == label.lower():
            return label
    try:
        host = (urlsplit(value).hostname or "").lower().removeprefix("www.")
    except ValueError:
        host = ""
    for domain, label in _PLATFORM_HOSTS.items():
        if host == domain or host.endswith("." + domain):
            return label
    return None


def prepare_search_request(
    tool: str,
    query: Any,
    sites: Sequence[str] | None = None,
    requested: Any = None,
    stage: str = "initial",
    context: Mapping[str, Any] | None = None,
    env: Mapping[str, str] | None = None,
    enabled: bool = True,
) -> dict[str, Any]:
    """Prepare a bounded MCP request; this function never performs I/O."""

    if tool not in SEARCH_TOOLS:
        return {"status": "TOOL_NOT_EXPOSED", "tool": tool, "query": None}
    credential = credential_state(env=env, enabled=enabled)
    query_result = validate_query(query, context=context)
    if query_result["status"] not in {"QUERY_ACCEPTED", "QUERY_REWRITTEN_GENERIC"}:
        return {**query_result, "tool": tool, "credential": credential}
    selected = list(sites or PLATFORMS)
    canonical_sites = []
    for site in selected:
        platform = infer_platform(site)
        if platform and platform not in canonical_sites:
            canonical_sites.append(platform)
    if not canonical_sites:
        return {
            "status": "PLATFORM_REJECTED",
            "tool": tool,
            "query": query_result["query"],
            "credential": credential,
        }
    if credential["status"] != "AVAILABLE":
        return {
            "status": credential["status"],
            "tool": tool,
            "query": query_result["query"],
            "credential": credential,
            "sites": canonical_sites,
            "num": bound_search_count(requested, stage),
        }
    return {
        "status": "READY",
        "tool": tool,
        "query": query_result["query"],
        "query_status": query_result["status"],
        "credential": credential,
        "sites": canonical_sites,
        "num": bound_search_count(requested, stage),
    }


def _record_url(record: Mapping[str, Any]) -> str | None:
    for key in ("link", "url", "source_url", "sourceUrl"):
        value = canonicalize_url(record.get(key))
        if value:
            return value
    return None


def _image_url(record: Mapping[str, Any]) -> str | None:
    for key in ("imageUrl", "image_url", "thumbnail", "thumbnailUrl"):
        value = record.get(key)
        if not isinstance(value, str):
            continue
        candidate = canonicalize_url(value)
        if candidate:
            return candidate
    return None


def _records_from_payload(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    records: list[Mapping[str, Any]] = []
    for key in ("images", "references", "results", "organic"):
        values = payload.get(key, [])
        if isinstance(values, list):
            records.extend(item for item in values if isinstance(item, Mapping))
    return records


def normalize_mcp_results(
    tool: str,
    payload: Mapping[str, Any],
    query: Any,
    retrieved_at: str,
    upstream_commit: str = UPSTREAM_COMMIT,
    max_results: Any = None,
    stage: str = "initial",
) -> dict[str, Any]:
    """Normalize structured upstream output into reference-only evidence."""

    if tool not in SEARCH_TOOLS:
        return {"status": "TOOL_NOT_EXPOSED", "query": None, "results": []}
    if upstream_commit != UPSTREAM_COMMIT:
        return {
            "status": "UPSTREAM_PIN_INVALID",
            "query": None,
            "results": [],
            "reason": "Only the audited immutable commit is accepted.",
        }
    query_result = validate_query(query)
    if query_result["status"] not in {"QUERY_ACCEPTED", "QUERY_REWRITTEN_GENERIC"}:
        return {**query_result, "results": [], "provenance": {"upstream_commit": UPSTREAM_COMMIT}}
    limit = bound_search_count(max_results, stage)
    normalized: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    dropped = 0
    for record in _records_from_payload(payload):
        source_url = _record_url(record)
        if not source_url:
            dropped += 1
            continue
        if source_url in seen_urls:
            dropped += 1
            continue
        source_platform = infer_platform(record.get("source_platform") or record.get("source") or source_url)
        if not source_platform:
            dropped += 1
            continue
        seen_urls.add(source_url)
        title = _safe_text(record.get("title") or record.get("name") or "Untitled reference", 180)
        snippet = _safe_text(record.get("snippet") or record.get("description") or "", 300)
        notes = [
            f"Discovery evidence from {source_platform}; interpret before synthesis.",
            "Research patterns, do not clone compositions.",
        ]
        if snippet:
            notes.append(snippet)
        normalized.append(
            {
                "source_platform": source_platform,
                "source_url": source_url,
                "title": title,
                "image_url": _image_url(record),
                "query": query_result["query"],
                "pattern_type": _PATTERN_TYPES[source_platform],
                "visual_notes": notes,
                "production_plausibility": "UNASSESSED",
                "reference_grade": "UNASSESSED",
                "why_selected": "PENDING_CLIENT_RELEVANCE_REVIEW",
                "pattern_to_learn": f"Study the {_PATTERN_TYPES[source_platform]} signal; record a client-specific principle before synthesis.",
                "what_not_to_copy": "SOURCE_COMPOSITION_BRANDED_ASSETS_AND_LITERAL_COPY",
                "accessibility_risk": "UNASSESSED",
                "implementation_risk": "UNASSESSED",
                "copyright_boundary": REFERENCE_ONLY,
                "retrieved_at": retrieved_at,
                "provider": MCP_PROVIDER,
                "upstream_commit": UPSTREAM_COMMIT,
                "interpretation_authority": (
                    "AWWWARDS-SHOWCASE-INTELLIGENCE"
                    if source_platform == "Awwwards"
                    else "VISUAL-RESEARCH-PROTOCOL"
                ),
            }
        )
        if len(normalized) >= limit:
            break
    return {
        "status": "NORMALIZED" if normalized else "NORMALIZED_EMPTY",
        "query": query_result["query"],
        "results": normalized,
        "dropped_count": dropped,
        "provenance": {
            "provider": MCP_PROVIDER,
            "upstream_commit": UPSTREAM_COMMIT,
            "retrieved_at": retrieved_at,
            "transport": "stdio-configured-upstream; local adapter normalization",
            "copyright_boundary": REFERENCE_ONLY,
        },
    }


def evaluate_reference(reference: Mapping[str, Any], scores: Mapping[str, Any]) -> dict[str, Any]:
    """Apply a bounded 0–5 heuristic rubric without inventing missing scores."""

    assessed: dict[str, int] = {}
    unassessed: list[str] = []
    for dimension in RUBRIC_DIMENSIONS:
        value = scores.get(dimension, scores.get(dimension.lower()))
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 5:
            unassessed.append(dimension)
        else:
            assessed[dimension] = value
    if unassessed:
        return {
            "status": "UNASSESSED",
            "reference_grade": "UNASSESSED",
            "grade": "UNASSESSED",
            "production_plausibility": "UNASSESSED",
            "scores": assessed,
            "unassessed_dimensions": unassessed,
            "rubric_method": "BOUNDED_HEURISTIC_0_TO_5_NOT_OBJECTIVE",
        }
    average = sum(assessed.values()) / len(RUBRIC_DIMENSIONS)
    production_dimensions = (
        assessed["RESPONSIVE_PLAUSIBILITY"],
        assessed["ACCESSIBILITY_PLAUSIBILITY"],
        assessed["IMPLEMENTABILITY"],
    )
    if min(production_dimensions) >= 4:
        production = "HIGH"
    elif min(production_dimensions) >= 2:
        production = "MEDIUM"
    else:
        production = "LOW"
    subject_fit = min(
        assessed["SUBJECT_RELEVANCE"],
        assessed["BRAND_FIT"],
        assessed["CONVERSION_APPLICABILITY"],
    )
    fantasy = assessed["VISUAL_CRAFT"] >= 4 and min(production_dimensions) <= 1
    if fantasy:
        grade = "D"
        reason = "High visual craft with low production utility (Dribbble fantasy risk)."
    elif average >= 4 and subject_fit >= 3 and min(production_dimensions) >= 3:
        grade = "A"
        reason = "Strong craft, subject fit, and production plausibility."
    elif average >= 3 and subject_fit >= 2 and min(production_dimensions) >= 2:
        grade = "B"
        reason = "Useful reference with bounded transferability."
    else:
        grade = "C"
        reason = "Some transferable signal, but material fit or utility is limited."
    return {
        "status": "ASSESSED",
        "reference_grade": grade,
        "grade": grade,
        "grade_reason": reason,
        "production_plausibility": production,
        "score_average": round(average, 2),
        "scores": assessed,
        "unassessed_dimensions": [],
        "rubric_method": "BOUNDED_HEURISTIC_0_TO_5_NOT_OBJECTIVE",
        "source_url": canonicalize_url(reference.get("source_url")),
    }


def enforce_production_asset_boundary(reference: Mapping[str, Any]) -> dict[str, Any]:
    """Refuse treating an MCP image or URL as a production asset."""

    return {
        "status": "PRODUCTION_ASSET_REFUSED",
        "allowed": False,
        "copyright_boundary": REFERENCE_ONLY,
        "source_url": canonicalize_url(reference.get("source_url")),
        "reason": "MCP images are discovery evidence only; Asset Director owns production assets.",
    }


def enforce_originality_request(request: Any) -> dict[str, Any]:
    """Refuse exact-copy instructions without echoing the request content."""

    if _CLONE_REQUEST_PATTERN.search(_text(request)):
        return {
            "status": "CLONE_REQUEST_REFUSED",
            "allowed": False,
            "reason": "Research patterns, do not clone compositions.",
        }
    return {
        "status": "PATTERN_ANALYSIS_ALLOWED",
        "allowed": True,
        "reason": "Only transferable principles may advance to synthesis.",
    }


def _public_authorized_url(url: Any) -> str | None:
    canonical = canonicalize_url(url)
    if not canonical:
        return None
    parts = urlsplit(canonical)
    if parts.scheme != "https" or not parts.hostname:
        return None
    host = parts.hostname.lower().rstrip(".")
    if host in {"localhost", "localhost.localdomain"} or host.endswith((".local", ".internal", ".test")):
        return None
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address is not None and (address.is_private or address.is_loopback or address.is_link_local or address.is_reserved or address.is_multicast or address.is_unspecified):
        return None
    return canonical


def token_extraction_status(
    url: Any,
    *,
    mode: str | None = None,
    deliberate: bool = False,
    authorized: bool = False,
    dembrandt_available: bool | None = None,
) -> dict[str, Any]:
    """Report token policy without invoking the unsafe upstream subprocess."""

    base = {"tool": TOKEN_TOOL, "tokens": None, "copyright_boundary": REFERENCE_ONLY}
    if mode is None and not deliberate:
        return {**base, "status": "DISABLED", "reason": "Token extraction is off by default."}
    if mode != TOKEN_EXTRACTION_MODE or not deliberate:
        return {**base, "status": "TOKEN_EXTRACTION_BLOCKED", "reason": "Deliberate reference deconstruction mode is required."}
    if not authorized:
        return {**base, "status": "TOKEN_EXTRACTION_BLOCKED", "reason": "A public or explicitly authorized URL is required."}
    public_url = _public_authorized_url(url)
    if not public_url:
        return {**base, "status": "TOKEN_EXTRACTION_BLOCKED", "reason": "Private, local, non-HTTPS, or malformed URLs are not allowed."}
    available = shutil.which("dembrandt") is not None if dembrandt_available is None else bool(dembrandt_available)
    if not available:
        return {**base, "status": "TOKEN_EXTRACTION_BLOCKED", "reason": "dembrandt is unavailable; no fallback execution is permitted."}
    return {
        **base,
        "status": "TOKEN_EXTRACTION_ALLOWED_REFERENCE_ONLY",
        "url": public_url,
        "reason": "A separate owner-authorized review may invoke the audited tool; this adapter does not execute it.",
    }


def validate_upstream_pin(metadata: Mapping[str, Any]) -> dict[str, Any]:
    """Fail closed unless the recorded immutable upstream audit is complete."""

    errors: list[str] = []
    if metadata.get("source_repository") != UPSTREAM_REPOSITORY:
        errors.append("UPSTREAM_REPOSITORY_MISMATCH")
    if metadata.get("upstream_commit_sha") != UPSTREAM_COMMIT:
        errors.append("UPSTREAM_COMMIT_UNPINNED_OR_MISMATCHED")
    if metadata.get("pin_type") != "immutable_commit":
        errors.append("UPSTREAM_PIN_TYPE_INVALID")
    if metadata.get("auto_update") is not False:
        errors.append("UPSTREAM_AUTO_UPDATE_MUST_BE_FALSE")
    if metadata.get("license") != UPSTREAM_LICENSE:
        errors.append("UPSTREAM_LICENSE_MISMATCH")
    if metadata.get("package_version") != UPSTREAM_PACKAGE_VERSION:
        errors.append("UPSTREAM_PACKAGE_VERSION_MISMATCH")
    if metadata.get("changelog_version") != UPSTREAM_CHANGELOG_VERSION:
        errors.append("UPSTREAM_CHANGELOG_VERSION_MISMATCH")
    if not re.fullmatch(r"[0-9a-f]{40}", str(metadata.get("upstream_commit_sha", ""))):
        errors.append("UPSTREAM_COMMIT_SHA_INVALID")
    return {
        "status": "PIN_VALID" if not errors else "UPSTREAM_PIN_INVALID",
        "ok": not errors,
        "errors": errors,
    }


def utc_now() -> str:
    """Return an explicit UTC timestamp for live provenance records."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
