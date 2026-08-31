"""Deterministic, provider-neutral Capability #10 validation.

This module validates an application or commerce architecture contract.  It
does not create accounts, call providers, process payments, access production
data, publish, deploy, or generate a production implementation.  Requirement
assessment is driven by explicit behavior and user stories.  Industry,
company name, geography, browser language, IP address, and stereotypes are
never used as a requirement signal.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


APPLICATION_STATUSES = {
    "NOT_REQUIRED",
    "PARTIALLY_REQUIRED",
    "REQUIRED",
    "PLANNING",
    "READY",
    "BLOCKED",
    "IMPLEMENTED",
    "VERIFIED",
    "EXCEPTION_APPLIED",
}

APPLICATION_CLASSIFICATIONS = {
    "STATIC_MARKETING",
    "CONTENT_PUBLISHER",
    "LEAD_GENERATION",
    "ECOMMERCE",
    "SUBSCRIPTION_COMMERCE",
    "AUTHENTICATED_APP",
    "SAAS",
    "CLIENT_PORTAL",
    "MEMBERSHIP",
    "COMMUNITY",
    "MARKETPLACE",
    "BOOKING",
    "USER_GENERATED_CONTENT",
    "INTERNAL_APPLICATION",
    "HYBRID",
}

MODULE_IDS = (
    "AUTHENTICATION",
    "AUTHORIZATION",
    "USER_PROFILE",
    "DATABASE",
    "API",
    "CATALOG",
    "CART",
    "CHECKOUT",
    "PAYMENT",
    "ORDER_MANAGEMENT",
    "SUBSCRIPTION",
    "BOOKING",
    "MEMBERSHIP",
    "USER_GENERATED_CONTENT",
    "FILE_UPLOAD",
    "TRANSACTIONAL_EMAIL",
    "NOTIFICATIONS",
    "WEBHOOKS",
    "SEARCH",
    "BACKGROUND_JOBS",
    "AUDIT_LOG",
    "ADMIN_INTERFACE",
    "THIRD_PARTY_INTEGRATION",
    "STORAGE",
    "ENTITLEMENT",
)

MODULE_SET = set(MODULE_IDS)
MODULE_STATUSES = {"NOT_REQUIRED", "PLANNING", "READY", "BLOCKED", "IMPLEMENTED", "VERIFIED", "EXCEPTION_APPLIED"}
HIGH_RISK_MODULES = {
    "AUTHENTICATION",
    "AUTHORIZATION",
    "DATABASE",
    "PAYMENT",
    "ORDER_MANAGEMENT",
    "SUBSCRIPTION",
    "BOOKING",
    "FILE_UPLOAD",
    "USER_GENERATED_CONTENT",
    "ADMIN_INTERFACE",
}
FORBIDDEN_STATE_KEYS = {
    "auth.complete",
    "authentication.complete",
    "commerce.complete",
    "commerce_locked",
    "payments.complete",
    "payment.complete",
    "application_locked",
    "application.locked",
    "application_architecture.complete",
    "i18n.complete",
    "translation.complete",
}

PASSWORD_HASH_ALGORITHMS = {"ARGON2ID", "ARGON2", "SCRYPT", "BCRYPT", "PBKDF2"}
PAYMENT_STATUSES = {"REQUIRES_PAYMENT", "PROCESSING", "SUCCEEDED", "FAILED", "CANCELED", "REFUNDED"}
ORDER_STATUSES = {"DRAFT", "PENDING_PAYMENT", "PAID", "FULFILLING", "FULFILLED", "CANCELED", "REFUNDED"}
PROVIDER_NEUTRAL = {"PROVIDER_NEUTRAL", "UNSELECTED", "NOT_SELECTED", "NONE"}


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
    path: str = "",
    record_id: str | None = None,
) -> None:
    severity = severity.upper()
    issue = {"code": code, "severity": severity, "message": message}
    if path:
        issue["path"] = path
    if record_id:
        issue["record_id"] = record_id
    result["issues"].append(issue)
    if severity == "WARNING":
        result["warnings"].append(issue)
        result["counts"]["warnings"] += 1
    elif severity == "BLOCKED":
        result["counts"]["blocked"] += 1
        result["unresolved_items"].append(issue)
    else:
        result["counts"]["errors"] += 1


def _finish(result: dict[str, Any]) -> dict[str, Any]:
    if result["counts"]["errors"]:
        result["status"] = "FAIL"
        result["ok"] = False
    elif result["counts"]["blocked"]:
        result["status"] = "BLOCKED"
        result["ok"] = False
    else:
        result["status"] = "PASS"
        result["ok"] = True
    return result


def _merge(target: dict[str, Any], source: dict[str, Any]) -> None:
    target["issues"].extend(source.get("issues", []))
    target["warnings"].extend(source.get("warnings", []))
    target["unresolved_items"].extend(source.get("unresolved_items", []))
    for key in ("errors", "blocked", "warnings"):
        target["counts"][key] += int(source.get("counts", {}).get(key, 0))


def _get(value: Any, *keys: str, default: Any = None) -> Any:
    if not isinstance(value, Mapping):
        return default
    for key in keys:
        if key in value:
            return value[key]
        for candidate in (key.lower(), key.upper()):
            if candidate in value:
                return value[candidate]
    return default


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _upper(value: Any) -> str:
    return _text(value).upper()


def _truth(value: Any) -> bool:
    return value is True or (isinstance(value, str) and value.strip().lower() in {"true", "yes", "1", "pass", "passed"})


def _list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _records(value: Any, id_key: str = "id") -> list[dict[str, Any]]:
    if isinstance(value, Mapping):
        output = []
        for key, item in value.items():
            if isinstance(item, Mapping):
                record = dict(item)
                record.setdefault(id_key, key)
                output.append(record)
        return output
    return [dict(item) for item in value if isinstance(item, Mapping)] if isinstance(value, (list, tuple)) else []


def _walk(value: Any, prefix: str = "") -> list[tuple[str, Any]]:
    if not isinstance(value, Mapping):
        return []
    output: list[tuple[str, Any]] = []
    for key, child in value.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        output.append((path, child))
        if isinstance(child, Mapping):
            output.extend(_walk(child, path))
        elif isinstance(child, list):
            for index, item in enumerate(child):
                if isinstance(item, Mapping):
                    output.extend(_walk(item, f"{path}[{index}]"))
    return output


def _module_ids(value: Any) -> list[str]:
    ids: list[str] = []
    for item in _list(value):
        if isinstance(item, Mapping):
            item_id = _get(item, "module_id", "id", default="")
        else:
            item_id = item
        item_id = _upper(item_id)
        if item_id:
            ids.append(item_id)
    return ids


def _has_any(value: Mapping[str, Any], *keys: str) -> bool:
    return any(_truth(_get(value, key)) for key in keys)


def _sub(value: Mapping[str, Any], *keys: str) -> dict[str, Any]:
    child = _get(value, *keys, default={})
    return dict(child) if isinstance(child, Mapping) else {}


def _unique(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


def calculate_application_requirement(factors: Mapping[str, Any] | None) -> dict[str, Any]:
    """Derive requirement and classifications from explicit behavior evidence.

    The returned assessment is intentionally conservative.  Empty or purely
    presentational evidence produces ``NOT_REQUIRED``.  Stateful behavior,
    account access, data mutation, commerce, booking, or private content
    produces ``REQUIRED`` and a concrete module list.
    """

    data = dict(factors) if isinstance(factors, Mapping) else {}
    stories = _records(_get(data, "user_stories", "stories", default=[]), "story_id")
    explicit_modules = _module_ids(_get(data, "required_modules", "modules_required", default=[]))
    explicit_classes = [_upper(item) for item in _list(_get(data, "classifications", "classification", default=[]))]
    explicit_classes = [item for item in explicit_classes if item]
    signals: set[str] = set(explicit_modules)
    evidence: list[str] = []

    def story_signal(story: Mapping[str, Any], *keys: str) -> bool:
        return _has_any(story, *keys)

    for story in stories:
        if story_signal(story, "auth_required", "authenticated", "account_required", "private_data"):
            signals.update({"AUTHENTICATION", "AUTHORIZATION"})
            evidence.append(f"{_get(story, 'story_id', 'id', default='story')}:account_access")
        if story_signal(story, "authorization_required", "role_required", "admin_action", "object_access"):
            signals.add("AUTHORIZATION")
        if story_signal(story, "state_change", "data_created", "data_updated", "data_deleted", "server_mutation"):
            signals.update({"DATABASE", "API"})
            evidence.append(f"{_get(story, 'story_id', 'id', default='story')}:state_change")
        if story_signal(story, "commerce_required", "purchase", "payment_required", "checkout_required"):
            signals.update({"CATALOG", "CART", "CHECKOUT", "PAYMENT", "ORDER_MANAGEMENT"})
            evidence.append(f"{_get(story, 'story_id', 'id', default='story')}:commerce")
        if story_signal(story, "subscription_required", "recurring_billing"):
            signals.update({"SUBSCRIPTION", "ENTITLEMENT"})
        if story_signal(story, "booking_required", "reservation_required", "appointment_required"):
            signals.add("BOOKING")
        if story_signal(story, "user_generated_content", "content_submission", "commenting", "community_post"):
            signals.update({"USER_GENERATED_CONTENT", "AUTHORIZATION"})
        if story_signal(story, "file_upload", "upload_required"):
            signals.update({"FILE_UPLOAD", "STORAGE"})
        if story_signal(story, "transactional_email", "notification_required", "background_job"):
            signals.add("TRANSACTIONAL_EMAIL")
        if story_signal(story, "admin_interface", "internal_workflow"):
            signals.update({"ADMIN_INTERFACE", "AUDIT_LOG"})

    for key, module in (
        ("authentication_required", "AUTHENTICATION"),
        ("authorization_required", "AUTHORIZATION"),
        ("database_required", "DATABASE"),
        ("api_required", "API"),
        ("commerce_required", "PAYMENT"),
        ("booking_required", "BOOKING"),
        ("user_generated_content_required", "USER_GENERATED_CONTENT"),
        ("file_upload_required", "FILE_UPLOAD"),
    ):
        if _truth(_get(data, key)):
            signals.add(module)

    classifications = [item for item in explicit_classes if item in APPLICATION_CLASSIFICATIONS]
    unknown_classes = [item for item in explicit_classes if item not in APPLICATION_CLASSIFICATIONS]
    if unknown_classes:
        evidence.append("unknown_classification")

    if "PAYMENT" in signals or "CHECKOUT" in signals:
        classifications.append("ECOMMERCE")
    if "SUBSCRIPTION" in signals:
        classifications.append("SUBSCRIPTION_COMMERCE")
    if "BOOKING" in signals:
        classifications.append("BOOKING")
    if "USER_GENERATED_CONTENT" in signals:
        classifications.append("USER_GENERATED_CONTENT")
    if "AUTHENTICATION" in signals:
        classifications.append("AUTHENTICATED_APP")
    if _truth(_get(data, "saas")):
        classifications.append("SAAS")
    if _truth(_get(data, "client_portal")):
        classifications.append("CLIENT_PORTAL")
    if _truth(_get(data, "membership")):
        classifications.append("MEMBERSHIP")
    if _truth(_get(data, "marketplace")):
        classifications.append("MARKETPLACE")
    if _truth(_get(data, "community")):
        classifications.append("COMMUNITY")
    if _truth(_get(data, "internal_application")):
        classifications.append("INTERNAL_APPLICATION")
    if _truth(_get(data, "lead_generation")):
        classifications.append("LEAD_GENERATION")
    if _truth(_get(data, "content_publishing")):
        classifications.append("CONTENT_PUBLISHER")
    if _truth(_get(data, "static_marketing")):
        classifications.append("STATIC_MARKETING")

    classifications = _unique(classifications)
    stateful = bool(signals & (MODULE_SET - {"SEARCH", "THIRD_PARTY_INTEGRATION"}))
    explicit_required = _get(data, "required", default=None)
    if isinstance(explicit_required, bool):
        required = explicit_required or stateful
    else:
        required = stateful
    if not classifications and not required and stories:
        classifications = ["STATIC_MARKETING"] if all(
            not (story_signal(story, "state_change", "data_created", "data_updated", "data_deleted", "auth_required", "payment_required"))
            for story in stories
        ) else []
    if not required:
        required_modules: list[str] = []
        status = "NOT_REQUIRED"
    else:
        required_modules = _unique([item for item in explicit_modules + list(signals) if item in MODULE_SET])
        if "AUTHENTICATION" in required_modules and "AUTHORIZATION" not in required_modules:
            required_modules.append("AUTHORIZATION")
        status = "REQUIRED"
    if len(classifications) > 1 and "HYBRID" not in classifications:
        classifications.append("HYBRID")
    blocked_reason = None
    if unknown_classes or _upper(_get(data, "requirement_status")) in {"AMBIGUOUS", "UNKNOWN", "UNASSESSED"}:
        status = "PARTIALLY_REQUIRED"
        blocked_reason = "OWNER_REVIEW_REQUIRED_FOR_APPLICATION_REQUIREMENT"
    return {
        "required": required,
        "status": status,
        "classifications": classifications,
        "required_modules": required_modules,
        "evidence": evidence,
        "blocked_reason": blocked_reason,
    }


def classify_application(factors: Mapping[str, Any] | None) -> list[str]:
    """Return deterministic behavior-based application classifications."""

    return calculate_application_requirement(factors).get("classifications", [])


def validate_module_registry(registry: Any) -> dict[str, Any]:
    result = _new_result()
    records = _records(_get(registry, "modules", default=registry), "module_id") if isinstance(registry, Mapping) else _records(registry, "module_id")
    if not records:
        _add(result, "MODULE_REGISTRY_EMPTY", "ERROR", "module registry must contain module records", path="/modules")
        return _finish(result)
    if isinstance(registry, Mapping):
        provider_policy = _upper(_get(registry, "provider_policy", default="PROVIDER_NEUTRAL"))
        if provider_policy not in {"PROVIDER_NEUTRAL", "UNSELECTED"}:
            _add(result, "MODULE_PROVIDER_POLICY_INVALID", "ERROR", "the canonical module registry must remain provider-neutral", path="/provider_policy")
    seen: set[str] = set()
    dependency_graph: dict[str, list[str]] = {}
    for index, record in enumerate(records):
        module_id = _upper(_get(record, "module_id", "id", default=""))
        path = f"/modules/{index}"
        if not module_id:
            _add(result, "MODULE_ID_MISSING", "ERROR", "module record requires module_id", path=path)
            continue
        if module_id in seen:
            _add(result, "MODULE_ID_DUPLICATE", "ERROR", f"module_id {module_id!r} appears more than once", path=path, record_id=module_id)
        seen.add(module_id)
        if module_id not in MODULE_SET:
            _add(result, "MODULE_ID_UNKNOWN", "ERROR", f"module_id {module_id!r} is not in the canonical module registry", path=path, record_id=module_id)
        missing = [key for key in ("required", "status", "business_reason", "data_classes", "security_risk", "external_provider", "owner", "dependencies", "verification_required", "exception") if key not in record]
        if missing:
            _add(result, "MODULE_RECORD_SHAPE", "ERROR", f"module {module_id!r} is missing {missing}", path=path, record_id=module_id)
        if not isinstance(_get(record, "required"), bool):
            _add(result, "MODULE_REQUIRED_TYPE", "ERROR", f"module {module_id!r}.required must be boolean", path=path, record_id=module_id)
        status = _upper(_get(record, "status"))
        if status not in MODULE_STATUSES:
            _add(result, "MODULE_STATUS_ENUM", "ERROR", f"module {module_id!r} has invalid status {status!r}", path=path, record_id=module_id)
        elif _truth(_get(record, "required")) and status == "NOT_REQUIRED":
            _add(result, "REQUIRED_MODULE_NOT_READY", "ERROR", f"required module {module_id!r} cannot have NOT_REQUIRED status", path=path, record_id=module_id)
        dependencies = _module_ids(_get(record, "dependencies", default=[]))
        for dependency in dependencies:
            if dependency not in MODULE_SET:
                _add(result, "MODULE_DEPENDENCY_UNKNOWN", "ERROR", f"module {module_id!r} depends on unknown module {dependency!r}", path=path, record_id=module_id)
            if dependency == module_id:
                _add(result, "MODULE_DEPENDENCY_CYCLE", "ERROR", f"module {module_id!r} cannot depend on itself", path=path, record_id=module_id)
        if not isinstance(_get(record, "dependencies"), list):
            _add(result, "MODULE_DEPENDENCIES_TYPE", "ERROR", f"module {module_id!r}.dependencies must be an array", path=path, record_id=module_id)
        elif module_id:
            dependency_graph.setdefault(module_id, dependencies)
        if not isinstance(_get(record, "data_classes"), list):
            _add(result, "MODULE_DATA_CLASSES_TYPE", "ERROR", f"module {module_id!r}.data_classes must be an array", path=path, record_id=module_id)
        if not isinstance(_get(record, "verification_required"), bool):
            _add(result, "MODULE_VERIFICATION_TYPE", "ERROR", f"module {module_id!r}.verification_required must be boolean", path=path, record_id=module_id)
        exception = _get(record, "exception")
        if not isinstance(exception, Mapping) or not isinstance(_get(exception, "applied"), bool) or "reason" not in exception:
            _add(result, "MODULE_EXCEPTION_SHAPE", "ERROR", f"module {module_id!r}.exception requires applied and reason", path=path, record_id=module_id)
        elif _truth(_get(exception, "applied")) and not _text(_get(exception, "reason")):
            _add(result, "MODULE_EXCEPTION_REASON_REQUIRED", "ERROR", f"module {module_id!r} exception requires a reason", path=path, record_id=module_id)
    visiting: set[str] = set()
    visited: set[str] = set()
    cycle_reported = False

    def visit(module_id: str) -> None:
        nonlocal cycle_reported
        if module_id in visited or cycle_reported:
            return
        if module_id in visiting:
            if not cycle_reported:
                _add(result, "MODULE_DEPENDENCY_CYCLE", "ERROR", f"module dependency cycle includes {module_id!r}", path="/modules", record_id=module_id)
                cycle_reported = True
            return
        visiting.add(module_id)
        for dependency in dependency_graph.get(module_id, []):
            if dependency in dependency_graph:
                visit(dependency)
        visiting.remove(module_id)
        visited.add(module_id)

    for module_id in sorted(dependency_graph):
        visit(module_id)
    return _finish(result)


def validate_application_state(state: Any, *, registry: Any = None) -> dict[str, Any]:
    result = _new_result()
    if not isinstance(state, Mapping):
        _add(result, "APPLICATION_STATE_TYPE", "ERROR", "application state must be an object", path="/application")
        return _finish(result)
    for path, _ in _walk(state):
        terminal = path.rsplit(".", 1)[-1]
        normalized = path.lower().replace("[", ".").replace("]", "")
        if terminal.lower().endswith("_locked") or terminal.lower() == "locked" or normalized in FORBIDDEN_STATE_KEYS:
            _add(result, "APPLICATION_LOCK_FORBIDDEN", "ERROR", f"non-canonical application lock or completion state {path!r} is forbidden", path=f"/{path}")
    required_fields = ("required", "complete", "status", "classifications", "modules_required", "modules_ready", "authentication_required", "commerce_required", "database_required", "external_integrations", "high_risk_operations", "implementation_verified", "production_verified", "blocked_reason", "exception")
    missing = [key for key in required_fields if key not in state]
    if missing:
        _add(result, "APPLICATION_STATE_SHAPE", "ERROR", f"application state is missing {missing}", path="/application")
    for key in ("required", "complete", "authentication_required", "commerce_required", "database_required", "implementation_verified", "production_verified"):
        if key in state and not isinstance(state[key], bool):
            _add(result, "APPLICATION_STATE_BOOLEAN_TYPE", "ERROR", f"application.{key} must be boolean", path=f"/application/{key}")
    for key in ("classifications", "modules_required", "modules_ready", "external_integrations", "high_risk_operations"):
        if key in state and not isinstance(state[key], list):
            _add(result, "APPLICATION_STATE_ARRAY_TYPE", "ERROR", f"application.{key} must be an array", path=f"/application/{key}")
    classifications = _list(_get(state, "classifications", default=[]))
    normalized_classifications = [_upper(item) for item in classifications]
    if any(not item or item not in APPLICATION_CLASSIFICATIONS for item in normalized_classifications):
        _add(result, "APPLICATION_CLASSIFICATION_ENUM", "ERROR", "application.classifications must contain only canonical classification IDs", path="/application/classifications")
    if len(normalized_classifications) != len(set(normalized_classifications)):
        _add(result, "APPLICATION_CLASSIFICATION_DUPLICATE", "ERROR", "application.classifications must contain unique IDs", path="/application/classifications")
    status = _upper(_get(state, "status"))
    if status not in APPLICATION_STATUSES:
        _add(result, "APPLICATION_STATE_STATUS_ENUM", "ERROR", f"application.status {status!r} is invalid", path="/application/status")
    required_ids = _module_ids(_get(state, "modules_required", default=[]))
    ready_ids = _module_ids(_get(state, "modules_ready", default=[]))
    if len(required_ids) != len(set(required_ids)):
        _add(result, "APPLICATION_MODULE_DUPLICATE", "ERROR", "application.modules_required must contain unique module IDs", path="/application/modules_required")
    if len(ready_ids) != len(set(ready_ids)):
        _add(result, "APPLICATION_READY_MODULE_DUPLICATE", "ERROR", "application.modules_ready must contain unique module IDs", path="/application/modules_ready")
    for module_id in required_ids + ready_ids:
        if module_id not in MODULE_SET:
            _add(result, "APPLICATION_MODULE_UNKNOWN", "ERROR", f"application references unknown module {module_id!r}", path="/application/modules_required")
    if not set(ready_ids).issubset(required_ids):
        _add(result, "APPLICATION_READY_MODULE_NOT_REQUIRED", "ERROR", "modules_ready must be a subset of modules_required", path="/application/modules_ready")
    if _truth(_get(state, "complete")) and not _truth(_get(state, "required")):
        _add(result, "APPLICATION_COMPLETE_NOT_REQUIRED", "ERROR", "application.complete cannot be true when application.required is false", path="/application/complete")
    if _upper(_get(state, "status")) == "NOT_REQUIRED" and (_truth(_get(state, "required")) or required_ids):
        _add(result, "APPLICATION_STATUS_CONTRADICTION", "ERROR", "NOT_REQUIRED status cannot carry required application modules", path="/application/status")
    if _upper(_get(state, "status")) == "BLOCKED" and not _text(_get(state, "blocked_reason")):
        _add(result, "APPLICATION_BLOCKED_REASON_REQUIRED", "ERROR", "BLOCKED application state requires blocked_reason", path="/application/blocked_reason")
    if _truth(_get(state, "production_verified")) and not _truth(_get(state, "implementation_verified")):
        _add(result, "APPLICATION_PRODUCTION_BEFORE_IMPLEMENTATION", "ERROR", "production_verified cannot be true before implementation_verified", path="/application/production_verified")
    exception = _get(state, "exception")
    if not isinstance(exception, Mapping) or not isinstance(_get(exception, "applied"), bool) or "reason" not in exception:
        _add(result, "APPLICATION_EXCEPTION_SHAPE", "ERROR", "application.exception requires applied and reason", path="/application/exception")
    elif _truth(_get(exception, "applied")) and not _text(_get(exception, "reason")):
        _add(result, "APPLICATION_EXCEPTION_REASON_REQUIRED", "ERROR", "application exception requires a reason", path="/application/exception")
    if registry is not None:
        registry_ids = {_upper(_get(record, "module_id", "id", default="")) for record in _records(_get(registry, "modules", default=registry), "module_id")}
        missing_registry = sorted(set(required_ids) - registry_ids)
        if missing_registry:
            _add(result, "APPLICATION_MODULE_REGISTRY_REFERENCE", "ERROR", f"required modules are absent from the module registry: {missing_registry}", path="/application/modules_required")
    return _finish(result)


def validate_authentication(config: Any, *, required: bool = True) -> dict[str, Any]:
    result = _new_result()
    cfg = dict(config) if isinstance(config, Mapping) else {}
    if not required and not cfg:
        return _finish(result)
    password = _sub(cfg, "password", "password_policy")
    passwordless = _truth(_get(cfg, "passwordless", "passwordless_required"))
    if _truth(_get(password, "plaintext", "stored_plaintext")) or _upper(_get(password, "storage")) in {"PLAINTEXT", "PLAIN_TEXT"}:
        _add(result, "PLAINTEXT_PASSWORD_STORAGE", "ERROR", "passwords must never be stored in plaintext", path="/authentication/password")
    algorithm = _upper(_get(password, "hash_algorithm", "algorithm"))
    if not passwordless and not algorithm:
        _add(result, "PASSWORD_HASH_ALGORITHM_MISSING", "ERROR", "password authentication requires an explicit modern password-hash algorithm", path="/authentication/password/hash_algorithm")
    if algorithm and algorithm not in PASSWORD_HASH_ALGORITHMS:
        _add(result, "PASSWORD_HASH_ALGORITHM_UNSAFE", "ERROR", f"password hash algorithm {algorithm!r} is not an approved password-hash family", path="/authentication/password/hash_algorithm")
    if _truth(_get(cfg, "password_hash_exposed", "hash_exposed", "client_hash_exposed")):
        _add(result, "PASSWORD_HASH_EXPOSED", "ERROR", "password hashes must not be exposed to clients or logs", path="/authentication/password_hash_exposed")
    provider = _sub(cfg, "provider")
    if _truth(_get(cfg, "provider_required")) and _get(cfg, "provider_available", default=_get(provider, "available", default=True)) is False:
        _add(result, "AUTH_PROVIDER_UNAVAILABLE", "BLOCKED", "authentication provider is unavailable; implementation and production verification remain blocked", path="/authentication/provider")
    recovery = _sub(cfg, "recovery", "account_recovery")
    if not _truth(_get(recovery, "defined", "enabled")):
        _add(result, "ACCOUNT_RECOVERY_UNDEFINED", "ERROR", "account recovery must be defined for an authenticated product", path="/authentication/recovery")
    else:
        if not _truth(_get(recovery, "single_use", "tokens_single_use")):
            _add(result, "ACCOUNT_RECOVERY_TOKEN_REUSE", "ERROR", "account recovery tokens must be single use", path="/authentication/recovery/single_use")
        if not _truth(_get(recovery, "expires", "expiring")):
            _add(result, "ACCOUNT_RECOVERY_TOKEN_EXPIRY", "ERROR", "account recovery tokens must expire", path="/authentication/recovery/expires")
        if _truth(_get(recovery, "user_enumeration")):
            _add(result, "ACCOUNT_ENUMERATION", "ERROR", "account recovery must not disclose whether an account exists", path="/authentication/recovery/user_enumeration")
    session = _sub(cfg, "session", "sessions")
    for key, code in (("secure_cookie", "SESSION_COOKIE_SECURE"), ("http_only", "SESSION_COOKIE_HTTP_ONLY"), ("same_site", "SESSION_COOKIE_SAMESITE"), ("rotation", "SESSION_ROTATION")):
        configured = _truth(session.get(key)) or (key == "same_site" and bool(_text(session.get(key))))
        if key not in session or not configured:
            _add(result, code, "ERROR", f"session policy must enable {key}", path=f"/authentication/session/{key}")
    if _truth(_get(cfg, "mfa_required")) and not _truth(_get(cfg, "mfa_defined", "mfa_policy_defined")):
        _add(result, "MFA_POLICY_UNDEFINED", "ERROR", "required MFA must have an explicit policy", path="/authentication/mfa")
    if _truth(_get(cfg, "email_verification_required")) and not _truth(_get(cfg, "email_verification_defined")):
        _add(result, "EMAIL_VERIFICATION_UNDEFINED", "ERROR", "required email verification must have an explicit flow", path="/authentication/email_verification")
    return _finish(result)


def validate_authorization(config: Any, *, required: bool = True) -> dict[str, Any]:
    result = _new_result()
    cfg = dict(config) if isinstance(config, Mapping) else {}
    if not required and not cfg:
        return _finish(result)
    if not _truth(_get(cfg, "server_enforced", "server_side_enforced")):
        _add(result, "AUTHORIZATION_SERVER_ENFORCEMENT_MISSING", "ERROR", "authorization must be enforced at the server boundary", path="/authorization/server_enforced")
    if _truth(_get(cfg, "client_role_trusted", "trust_client_role")):
        _add(result, "CLIENT_ROLE_TRUST", "ERROR", "client-supplied roles must never be authoritative", path="/authorization/client_role_trusted")
    if _truth(_get(cfg, "object_access_required", "object_level_required")) and not _truth(_get(cfg, "object_level_enforced", "object_access_enforced")):
        _add(result, "OBJECT_LEVEL_AUTHORIZATION_MISSING", "ERROR", "object-level authorization must be checked for every protected object", path="/authorization/object_level_enforced")
    roles = _list(_get(cfg, "roles", default=[]))
    if _truth(_get(cfg, "roles_required", "role_required")) and not roles:
        _add(result, "AUTHORIZATION_ROLES_MISSING", "ERROR", "role requirements must name the allowed roles", path="/authorization/roles")
    if _truth(_get(cfg, "default_allow")):
        _add(result, "AUTHORIZATION_DEFAULT_ALLOW", "ERROR", "authorization must fail closed with default deny", path="/authorization/default_allow")
    if _truth(_get(cfg, "admin_route_required", "admin_required")) and not _truth(_get(cfg, "admin_route_server_protected", "admin_server_protected")):
        _add(result, "ADMIN_ROUTE_CLIENT_ONLY", "ERROR", "admin routes must be protected on the server, not hidden in the client", path="/authorization/admin_route_server_protected")
    return _finish(result)


def validate_data_and_database(config: Any, *, database_required: bool = True) -> dict[str, Any]:
    result = _new_result()
    cfg = dict(config) if isinstance(config, Mapping) else {}
    data = _sub(cfg, "data_model", "data")
    database = _sub(cfg, "database", "db")
    if database_required:
        for key, code in (("migrations_defined", "DATABASE_MIGRATIONS_MISSING"), ("backup_recovery_defined", "DATABASE_RECOVERY_MISSING")):
            if not _truth(_get(database, key)):
                _add(result, code, "ERROR", f"database contract must define {key}", path=f"/database/{key}")
        if _truth(_get(database, "production_connection_string_in_repo", "secret_in_repo")):
            _add(result, "DATABASE_SECRET_EXPOSED", "ERROR", "database credentials must not be stored in the repository", path="/database")
        if _truth(_get(database, "transactions_required")) and not _truth(_get(database, "transactions_defined")):
            _add(result, "DATABASE_TRANSACTION_BOUNDARY_MISSING", "ERROR", "multi-record mutations require transaction boundaries", path="/database/transactions_defined")
    if _truth(_get(data, "sensitive_data")) and not _truth(_get(data, "minimization_reviewed")):
        _add(result, "DATA_MINIMIZATION_MISSING", "ERROR", "sensitive data requires a minimization review", path="/data_model/minimization_reviewed")
    return _finish(result)


def validate_api(config: Any, *, required: bool = True) -> dict[str, Any]:
    result = _new_result()
    cfg = dict(config) if isinstance(config, Mapping) else {}
    if not required and not cfg:
        return _finish(result)
    for key, code in (("input_validation", "API_INPUT_VALIDATION_MISSING"), ("output_allowlist", "API_OUTPUT_ALLOWLIST_MISSING"), ("error_contract", "API_ERROR_CONTRACT_MISSING"), ("rate_limiting", "API_RATE_LIMITING_MISSING")):
        if not _truth(_get(cfg, key, key + "_defined")):
            _add(result, code, "ERROR", f"API contract must define {key}", path=f"/api/{key}")
    if _truth(_get(cfg, "auth_bypass", "unauthenticated_mutation")):
        _add(result, "API_AUTH_BOUNDARY_BYPASS", "ERROR", "mutating API routes cannot bypass the declared auth boundary", path="/api/auth_bypass")
    return _finish(result)


def _state_machine(values: Any, allowed: set[str]) -> bool:
    statuses = [_upper(item) for item in _list(values)]
    return bool(statuses) and all(item in allowed for item in statuses) and len(statuses) == len(set(statuses))


def validate_ecommerce(config: Any, *, required: bool = True) -> dict[str, Any]:
    result = _new_result()
    cfg = dict(config) if isinstance(config, Mapping) else {}
    if not required and not cfg:
        return _finish(result)
    price = _sub(cfg, "price", "pricing")
    if _truth(_get(cfg, "client_price_trusted", "trust_client_price")) or _upper(_get(price, "authority")) in {"CLIENT", "BROWSER", "UNTRUSTED_CLIENT"}:
        _add(result, "CLIENT_PRICE_TRUST", "ERROR", "the server must resolve the canonical price; client price is never authoritative", path="/commerce/price")
    if _truth(_get(cfg, "checkout_required", default=True)) and not _truth(_get(price, "canonical_price_verified", "server_authoritative", default=False)):
        _add(result, "CANONICAL_PRICE_VERIFICATION_MISSING", "ERROR", "checkout must verify the canonical server-side price", path="/commerce/price/canonical_price_verified")
    if _truth(_get(cfg, "checkout_click_marks_paid", "button_marks_paid")):
        _add(result, "CHECKOUT_BUTTON_MARKS_PAID", "ERROR", "a client click cannot mark an order paid", path="/commerce/checkout_click_marks_paid")
    payment = _sub(cfg, "payment")
    provider_available = _get(payment, "provider_available", default=_get(cfg, "provider_available", default=True))
    if provider_available is False:
        _add(result, "PAYMENT_PROVIDER_UNAVAILABLE", "BLOCKED", "payment provider is unavailable; no implementation or production verification can be claimed", path="/commerce/payment/provider_available")
    if _truth(_get(payment, "live_payment_attempted", "real_payment_attempted")):
        _add(result, "LIVE_PAYMENT_SIDE_EFFECT", "ERROR", "synthetic architecture validation must not attempt a live payment", path="/commerce/payment/live_payment_attempted")
    if _truth(_get(payment, "raw_card_stored", "stores_raw_card")):
        _add(result, "RAW_CARD_STORAGE", "ERROR", "raw card data must not be stored by the application", path="/commerce/payment/raw_card_stored")
    if _truth(_get(payment, "hosted_or_tokenized", "tokenized")) is False:
        _add(result, "PAYMENT_TOKENIZATION_MISSING", "ERROR", "payment collection must use a hosted or tokenized boundary", path="/commerce/payment/hosted_or_tokenized")
    if not _state_machine(_get(payment, "statuses", "state_machine", default=[]), PAYMENT_STATUSES):
        _add(result, "PAYMENT_STATE_MACHINE_INVALID", "ERROR", "payment status transitions must be explicit and distinct from order status", path="/commerce/payment/statuses")
    order = _sub(cfg, "order", "orders")
    if not _state_machine(_get(order, "statuses", "state_machine", default=[]), ORDER_STATUSES):
        _add(result, "ORDER_STATE_MACHINE_INVALID", "ERROR", "order status transitions must be explicit and distinct from payment status", path="/commerce/order/statuses")
    if _truth(_get(order, "paid_boolean_only", "collapsed_paid_state")):
        _add(result, "ORDER_PAYMENT_STATE_COLLAPSED", "ERROR", "order and payment state cannot be represented by a single paid boolean", path="/commerce/order")
    confirmation_source = _upper(_get(cfg, "payment_confirmation_source", "confirmation_source", default=""))
    if _truth(_get(cfg, "success_route_without_payment_confirmation", "success_without_confirmation")) or (confirmation_source and confirmation_source not in {"WEBHOOK", "SERVER_PROVIDER_CONFIRMATION", "SERVER_VERIFIED"}):
        _add(result, "PAYMENT_CONFIRMATION_BYPASS", "ERROR", "success UI and order fulfillment require server/provider payment confirmation", path="/commerce/payment_confirmation_source")
    webhook = _sub(cfg, "webhook", "webhooks")
    if _truth(_get(cfg, "webhook_required", default=True)) or webhook:
        if not _truth(_get(webhook, "signature_verified", "signature_validation")):
            _add(result, "WEBHOOK_SIGNATURE_MISSING", "ERROR", "webhooks must verify the provider signature before mutation", path="/commerce/webhook/signature_verified")
        if not _truth(_get(webhook, "idempotent", "idempotency")):
            _add(result, "WEBHOOK_IDEMPOTENCY_MISSING", "ERROR", "webhook side effects must be idempotent", path="/commerce/webhook/idempotent")
        if _truth(_get(webhook, "duplicate_side_effect_created", "duplicate_effect")):
            _add(result, "WEBHOOK_DUPLICATE_SIDE_EFFECT", "ERROR", "duplicate webhook delivery must not create a duplicate side effect", path="/commerce/webhook/duplicate_side_effect_created")
    shipping = _sub(cfg, "shipping")
    product_kind = _upper(_get(cfg, "product_type", "fulfillment", default=""))
    if product_kind in {"DIGITAL", "DIGITAL_GOODS", "SERVICE"}:
        if _truth(_get(shipping, "required")) or _truth(_get(cfg, "shipping_fields_required")):
            _add(result, "DIGITAL_SHIPPING_BLOAT", "ERROR", "digital goods must not collect unnecessary shipping data", path="/commerce/shipping")
    if product_kind in {"PHYSICAL", "PHYSICAL_GOODS"}:
        if not _truth(_get(shipping, "defined", "required_fields_defined")):
            _add(result, "PHYSICAL_SHIPPING_MISSING", "ERROR", "physical goods require an explicit shipping architecture", path="/commerce/shipping/defined")
    return _finish(result)


def validate_subscription(config: Any, *, required: bool = False) -> dict[str, Any]:
    result = _new_result()
    cfg = dict(config) if isinstance(config, Mapping) else {}
    if not required and not cfg:
        return _finish(result)
    if not _truth(_get(cfg, "entitlements_separate", "entitlement_state_separate")):
        _add(result, "SUBSCRIPTION_ENTITLEMENT_STATE_MISSING", "ERROR", "subscription billing state must be separate from product entitlements", path="/subscription/entitlements_separate")
    if _truth(_get(cfg, "payment_failed_entitlement_active", "failed_payment_keeps_entitlement")):
        _add(result, "FAILED_PAYMENT_ENTITLEMENT_ACTIVE", "ERROR", "failed payment must not leave a paid entitlement active", path="/subscription/payment_failed_entitlement_active")
    if not _truth(_get(cfg, "cancellation_defined", "dunning_defined")):
        _add(result, "SUBSCRIPTION_LIFECYCLE_MISSING", "ERROR", "subscription cancellation and failure lifecycle must be defined", path="/subscription/cancellation_defined")
    return _finish(result)


def validate_booking(config: Any, *, required: bool = False) -> dict[str, Any]:
    result = _new_result()
    cfg = dict(config) if isinstance(config, Mapping) else {}
    if not required and not cfg:
        return _finish(result)
    if _truth(_get(cfg, "overlap_allowed", "double_booking_possible")) or not _truth(_get(cfg, "overlap_prevented", "conflict_check")):
        _add(result, "BOOKING_OVERLAP_UNSAFE", "ERROR", "booking creation must prevent overlapping reservations", path="/booking/overlap_prevented")
    timezone_value = _get(cfg, "timezone", "timezone_policy", default="")
    if not _text(timezone_value) or _upper(timezone_value) in {"LOCAL", "UNKNOWN", "AMBIGUOUS", "INFERRED"}:
        _add(result, "BOOKING_TIMEZONE_AMBIGUOUS", "ERROR", "booking times require an explicit timezone policy", path="/booking/timezone")
    return _finish(result)


def validate_uploads(config: Any, *, required: bool = False) -> dict[str, Any]:
    result = _new_result()
    cfg = dict(config) if isinstance(config, Mapping) else {}
    if not required and not cfg:
        return _finish(result)
    if not _truth(_get(cfg, "allowlist_enforced", "mime_allowlist", "extension_allowlist")):
        _add(result, "UPLOAD_ALLOWLIST_MISSING", "ERROR", "uploads require an explicit type and extension allowlist", path="/uploads/allowlist_enforced")
    if _truth(_get(cfg, "executable_upload_accepted", "accepts_executable")):
        _add(result, "EXECUTABLE_UPLOAD_ACCEPTED", "ERROR", "unrestricted executable uploads are forbidden", path="/uploads/executable_upload_accepted")
    if _truth(_get(cfg, "private_required", "private_storage_required")):
        if not _truth(_get(cfg, "private_storage_authorized", "authorization_before_download")):
            _add(result, "PRIVATE_UPLOAD_AUTH_MISSING", "ERROR", "private files require authorization before download", path="/uploads/private_storage_authorized")
        if _truth(_get(cfg, "private_file_public", "public_url_exposed")):
            _add(result, "PRIVATE_FILE_PUBLIC", "ERROR", "private uploads must not be exposed through an unrestricted public URL", path="/uploads/private_file_public")
    return _finish(result)


def validate_user_generated_content(config: Any, *, required: bool = False) -> dict[str, Any]:
    result = _new_result()
    cfg = dict(config) if isinstance(config, Mapping) else {}
    if not required and not cfg:
        return _finish(result)
    if not _truth(_get(cfg, "sanitized", "sanitization", "output_sanitized")):
        _add(result, "UGC_SANITIZATION_MISSING", "ERROR", "user-generated content must be sanitized before rendering", path="/user_generated_content/sanitized")
    if _truth(_get(cfg, "script_executed", "raw_html_executed", "script_allowed")):
        _add(result, "UGC_SCRIPT_EXECUTION", "ERROR", "user-generated content must not execute arbitrary script", path="/user_generated_content/script_executed")
    return _finish(result)


def validate_messaging(config: Any, *, required: bool = False) -> dict[str, Any]:
    result = _new_result()
    cfg = dict(config) if isinstance(config, Mapping) else {}
    if not required and not cfg:
        return _finish(result)
    if _truth(_get(cfg, "required", default=required)) and _truth(_get(cfg, "failure_reported_as_success", "email_failure_ui_success")):
        _add(result, "TRANSACTIONAL_EMAIL_FALSE_SUCCESS", "ERROR", "a failed required email must not be reported as successful", path="/messaging/failure_reported_as_success")
    if _truth(_get(cfg, "required", default=required)) and not _truth(_get(cfg, "delivery_status_observable", "delivery_failure_visible")):
        _add(result, "TRANSACTIONAL_EMAIL_STATUS_MISSING", "ERROR", "required transactional email needs an observable delivery status", path="/messaging/delivery_status_observable")
    return _finish(result)


def validate_integrations(config: Any, *, required: bool = False) -> dict[str, Any]:
    result = _new_result()
    cfg = dict(config) if isinstance(config, Mapping) else {}
    if not required and not cfg:
        return _finish(result)
    if not _truth(_get(cfg, "inventory_complete", "third_party_inventory_complete")):
        _add(result, "INTEGRATION_INVENTORY_MISSING", "ERROR", "every external integration must have an owner, purpose, scope, and failure policy", path="/integrations/inventory_complete")
    unknown = _list(_get(cfg, "unknown_integrations", "undeclared", default=[]))
    if unknown:
        _add(result, "INTEGRATION_UNDECLARED", "ERROR", f"unknown integrations are not permitted: {unknown}", path="/integrations/unknown_integrations")
    if _truth(_get(cfg, "secret_exposed_client", "application_secret_exposed", "client_secret_exposed")):
        _add(result, "APPLICATION_SECRET_CLIENT_EXPOSURE", "ERROR", "application secrets must remain server-side", path="/integrations/secret_exposed_client")
    return _finish(result)


def validate_measurement_and_seo(config: Any) -> dict[str, Any]:
    result = _new_result()
    cfg = dict(config) if isinstance(config, Mapping) else {}
    measurement = _sub(cfg, "measurement", "analytics")
    if _truth(_get(measurement, "purchase_event_from_click", "purchase_event_button_triggered")):
        _add(result, "PURCHASE_EVENT_CLICK_TRUST", "ERROR", "purchase analytics must follow an authoritative confirmed purchase, not a click", path="/measurement/purchase_event_from_click")
    if _truth(_get(measurement, "purchase_event_required", "purchase_event_authoritative")) and not _truth(_get(measurement, "purchase_event_authoritative", "server_confirmed")):
        _add(result, "PURCHASE_EVENT_AUTHORITY_MISSING", "ERROR", "purchase measurement must be tied to an authoritative confirmation", path="/measurement/purchase_event_authoritative")
    if _truth(_get(measurement, "duplicate_locale_events", "locale_event_duplicate")):
        _add(result, "LOCALE_EVENT_DUPLICATE", "ERROR", "localization must parameterize canonical events rather than duplicate semantic events", path="/measurement/duplicate_locale_events")
    if _truth(_get(measurement, "canonical_event_with_locale", "locale_parameter_present")) is False and _truth(_get(measurement, "localized_measurement_required")):
        _add(result, "LOCALE_EVENT_PARAMETER_MISSING", "ERROR", "localized measurement requires the canonical event plus a locale parameter", path="/measurement/canonical_event_with_locale")
    seo = _sub(cfg, "seo")
    if _truth(_get(seo, "private_route_indexable", "private_route_indexed")):
        _add(result, "PRIVATE_ROUTE_INDEXABLE", "ERROR", "private application routes must not be indexable", path="/seo/private_route_indexable")
    return _finish(result)


def validate_high_risk_operations(config: Any, modules: Sequence[str]) -> dict[str, Any]:
    result = _new_result()
    cfg = dict(config) if isinstance(config, Mapping) else {}
    operations = _list(_get(cfg, "high_risk_operations", "high_risk", default=[]))
    for index, operation in enumerate(operations):
        record = operation if isinstance(operation, Mapping) else {"operation": operation}
        operation_name = _text(_get(record, "operation", "id", default="operation"))
        if not _truth(_get(record, "verification_complete", "verified", "verification")):
            _add(result, "HIGH_RISK_VERIFICATION_MISSING", "BLOCKED", f"high-risk operation {operation_name!r} lacks completed verification", path=f"/high_risk_operations/{index}")
    required_high_risk = set(modules) & HIGH_RISK_MODULES
    declared = {_upper(_get(item, "operation", "id", default="")) for item in operations if isinstance(item, Mapping)}
    if "PAYMENT" in required_high_risk and operations and not declared:
        _add(result, "HIGH_RISK_OPERATION_ID_MISSING", "ERROR", "high-risk operations require stable identifiers", path="/high_risk_operations")
    return _finish(result)


def _forbidden_state_issues(manifest: Mapping[str, Any]) -> list[str]:
    hits: list[str] = []
    app = _get(manifest, "application", default=manifest)
    paths: list[tuple[str, Any]] = _walk(app)
    # A full site profile legitimately contains the framework's five owner
    # locks. They are outside Capability 10 and must not be treated as an
    # application lock, while an extra lock inside that block remains invalid.
    if app is not manifest and isinstance(manifest, Mapping):
        for key, value in manifest.items():
            if str(key).lower() == "application":
                continue
            if str(key).lower() == "locks" and isinstance(value, Mapping):
                allowed = {
                    "design_direction_locked",
                    "information_architecture_locked",
                    "content_structure_locked",
                    "design_system_locked",
                    "motion_direction_locked",
                }
                for lock in value:
                    if str(lock).lower() not in allowed:
                        hits.append(f"locks.{lock}")
                continue
            paths.extend(_walk({str(key): value}))
    for path, _ in paths:
        terminal = path.rsplit(".", 1)[-1].lower()
        normalized = path.lower().replace("[", ".").replace("]", "")
        if terminal.endswith("_locked") or terminal == "locked" or normalized in FORBIDDEN_STATE_KEYS:
            hits.append(path)
    return hits


def validate_application_architecture(manifest: Any, *, module_registry: Any = None) -> dict[str, Any]:
    """Validate a complete application architecture manifest."""

    result = _new_result()
    if not isinstance(manifest, Mapping):
        _add(result, "APPLICATION_MANIFEST_TYPE", "ERROR", "application architecture manifest must be an object", path="/")
        return _finish(result)
    app = _get(manifest, "application", default=manifest)
    if not isinstance(app, Mapping):
        _add(result, "APPLICATION_MANIFEST_APPLICATION_TYPE", "ERROR", "manifest.application must be an object", path="/application")
        return _finish(result)
    for path in _forbidden_state_issues(manifest):
        _add(result, "APPLICATION_LOCK_FORBIDDEN", "ERROR", f"forbidden parallel application state {path!r}", path=f"/{path}")

    registry = module_registry
    if registry is None and isinstance(_get(manifest, "module_registry"), Mapping):
        registry = _get(manifest, "module_registry")
    if registry is not None:
        registry_result = validate_module_registry(registry)
        _merge(result, registry_result)

    assessment = calculate_application_requirement(app)
    result["requirement_assessment"] = assessment
    state_result = validate_application_state(app, registry=registry)
    _merge(result, state_result)
    required = _truth(_get(app, "required")) or assessment["required"]
    required_ids = _module_ids(_get(app, "modules_required", default=assessment["required_modules"]))
    if not required:
        if (
            required_ids
            or any(_truth(_get(app, key)) for key in (
                "authentication_required",
                "commerce_required",
                "database_required",
                "api_required",
            ))
            or _list(_get(app, "external_integrations", default=[]))
            or _list(_get(app, "high_risk_operations", default=[]))
        ):
            _add(result, "APPLICATION_BLOAT", "ERROR", "a non-application surface must not activate authentication, commerce, database, or other application infrastructure", path="/application")
        if assessment["status"] == "PARTIALLY_REQUIRED":
            _add(result, "APPLICATION_REQUIREMENT_AMBIGUOUS", "BLOCKED", assessment["blocked_reason"] or "application requirement needs owner review", path="/application")
        result["required"] = False
        return _finish(result)

    if not _records(_get(app, "user_stories", "stories", default=[]), "story_id"):
        _add(result, "APPLICATION_USER_STORIES_MISSING", "ERROR", "required application architecture must name the user stories that create the requirement", path="/application/user_stories")
    if not _records(_get(app, "actors", default=[]), "actor_id"):
        _add(result, "APPLICATION_ACTORS_MISSING", "ERROR", "required application architecture must name actors and trust boundaries", path="/application/actors")
    if not required_ids:
        _add(result, "APPLICATION_MODULES_MISSING", "ERROR", "required application architecture must activate only the modules justified by behavior", path="/application/modules_required")
    if registry is not None:
        registry_ids = {_upper(_get(record, "module_id", "id", default="")) for record in _records(_get(registry, "modules", default=registry), "module_id")}
        missing = sorted(set(required_ids) - registry_ids)
        if missing:
            _add(result, "APPLICATION_MODULE_REGISTRY_REFERENCE", "ERROR", f"required modules are absent from registry: {missing}", path="/application/modules_required")
        records_by_id = {_upper(_get(record, "module_id", "id", default="")): record for record in _records(_get(registry, "modules", default=registry), "module_id")}
        for module_id in required_ids:
            record = records_by_id.get(module_id, {})
            dependencies = _module_ids(_get(record, "dependencies", default=[]))
            missing_dependencies = sorted(set(dependencies) - set(required_ids))
            if missing_dependencies:
                _add(result, "APPLICATION_REQUIRED_DEPENDENCY_MISSING", "ERROR", f"required module {module_id!r} omits dependencies {missing_dependencies}", path="/application/modules_required", record_id=module_id)

    auth_required = "AUTHENTICATION" in required_ids or _truth(_get(app, "authentication_required"))
    authz_required = "AUTHORIZATION" in required_ids or auth_required or _truth(_get(app, "authorization_required"))
    _merge(result, validate_authentication(_get(app, "authentication", "auth", default={}), required=auth_required))
    _merge(result, validate_authorization(_get(app, "authorization", "authz", default={}), required=authz_required))
    _merge(result, validate_data_and_database(app, database_required="DATABASE" in required_ids or _truth(_get(app, "database_required"))))
    _merge(result, validate_api(_get(app, "api", default={}), required="API" in required_ids or bool(_get(app, "api"))))
    commerce_required = bool(set(required_ids) & {"CATALOG", "CART", "CHECKOUT", "PAYMENT", "ORDER_MANAGEMENT"}) or _truth(_get(app, "commerce_required"))
    _merge(result, validate_ecommerce(_get(app, "commerce", "ecommerce", default={}), required=commerce_required))
    _merge(result, validate_subscription(_get(app, "subscription", default={}), required="SUBSCRIPTION" in required_ids))
    _merge(result, validate_booking(_get(app, "booking", default={}), required="BOOKING" in required_ids))
    _merge(result, validate_uploads(_get(app, "uploads", "file_upload", default={}), required="FILE_UPLOAD" in required_ids))
    _merge(result, validate_user_generated_content(_get(app, "user_generated_content", "ugc", default={}), required="USER_GENERATED_CONTENT" in required_ids))
    _merge(result, validate_messaging(_get(app, "messaging", "transactional_email", default={}), required="TRANSACTIONAL_EMAIL" in required_ids))
    _merge(result, validate_integrations(_get(app, "integrations", default={}), required="THIRD_PARTY_INTEGRATION" in required_ids))
    _merge(result, validate_measurement_and_seo(app))
    _merge(result, validate_high_risk_operations(app, required_ids))
    if _get(app, "provider_available", default=True) is False:
        _add(result, "APPLICATION_PROVIDER_UNAVAILABLE", "BLOCKED", "a required external provider is unavailable; architecture may be specified but implementation verification is blocked", path="/application/provider_available")
    if _truth(_get(app, "live_user_created", "real_user_attempted")):
        _add(result, "LIVE_USER_SIDE_EFFECT", "ERROR", "synthetic validation must not create or modify real user accounts", path="/application/live_user_created")
    if _truth(_get(app, "live_payment_attempted", "real_payment_attempted")):
        _add(result, "LIVE_PAYMENT_SIDE_EFFECT", "ERROR", "synthetic validation must not attempt a live payment", path="/application/live_payment_attempted")
    result["required"] = True
    result["required_modules"] = required_ids
    return _finish(result)


def validate_application(manifest: Any, *, module_registry: Any = None) -> dict[str, Any]:
    """Compatibility alias for the sole Capability #10 validator."""

    return validate_application_architecture(manifest, module_registry=module_registry)
