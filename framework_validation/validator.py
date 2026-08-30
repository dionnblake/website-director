"""Deterministic self-validation for the Website Director framework.

The validator checks framework governance artifacts, not generated website
quality. It reads source files, runs only explicitly registered local suites,
protects registered frozen projects with the V2.8 ``FrozenIntegrityGuard``,
and writes reports only to the designated validation-report paths.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
from functools import total_ordering
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Mapping, Optional, Sequence
from urllib.parse import unquote, urlsplit


CANONICAL_LOCKS = (
    "design_direction_locked",
    "information_architecture_locked",
    "content_structure_locked",
    "design_system_locked",
    "motion_direction_locked",
)
FORBIDDEN_OWNER_LOCKS = {
    "measurement_locked",
    "security_locked",
    "privacy_locked",
    "accessibility_locked",
    "browser_qa_locked",
    "launch_locked",
    "seo_locked",
    "asset_locked",
    "handoff_locked",
}
VALID_STATUSES = {"ACTIVE", "DEPRECATED", "SUPERSEDED", "HISTORICAL"}
VALID_GATE_TYPES = {"OWNER_LOCK", "READINESS", "VERIFICATION", "REFINEMENT"}
SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)
MARKER_VERSION_RE = re.compile(
    r"FRAMEWORK_VERSION\s*[:=]\s*[`\"']?"
    r"(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)",
    re.IGNORECASE,
)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))[^)]*\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
SOURCE_IGNORED_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache"}
REPORT_RUNTIME_PREFIX = "framework-validation/reports/runtime/"
REPORT_CERTIFICATION_PREFIX = "framework-validation/reports/"
RUNTIME_SOURCE_PREFIXES = (REPORT_RUNTIME_PREFIX, "browser-qa/evidence/")

LAUNCH_STATUSES = (
    "NOT_EVALUATED",
    "PLANNING",
    "BLOCKED",
    "RELEASE_READY",
    "AWAITING_DEPLOYMENT_AUTHORIZATION",
    "DEPLOYMENT_AUTHORIZED",
    "DEPLOYING",
    "DEPLOYED",
    "PRODUCTION_VERIFICATION_RUNNING",
    "PRODUCTION_VERIFICATION_FAILED",
    "PRODUCTION_VERIFIED",
    "POST_LAUNCH_MONITORING",
    "STABILIZED",
    "ROLLBACK_REQUIRED",
    "ROLLED_BACK",
    "EXCEPTION_APPLIED",
)
LAUNCH_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "NOT_EVALUATED": ("PLANNING", "EXCEPTION_APPLIED"),
    "PLANNING": ("PLANNING", "BLOCKED", "RELEASE_READY", "EXCEPTION_APPLIED"),
    "BLOCKED": ("PLANNING", "BLOCKED", "RELEASE_READY", "EXCEPTION_APPLIED"),
    "RELEASE_READY": ("AWAITING_DEPLOYMENT_AUTHORIZATION", "BLOCKED", "PLANNING", "EXCEPTION_APPLIED"),
    "AWAITING_DEPLOYMENT_AUTHORIZATION": ("DEPLOYMENT_AUTHORIZED", "BLOCKED", "RELEASE_READY", "EXCEPTION_APPLIED"),
    "DEPLOYMENT_AUTHORIZED": ("DEPLOYING", "BLOCKED", "EXCEPTION_APPLIED"),
    "DEPLOYING": ("DEPLOYED", "PRODUCTION_VERIFICATION_FAILED", "ROLLBACK_REQUIRED", "BLOCKED"),
    "DEPLOYED": ("PRODUCTION_VERIFICATION_RUNNING", "ROLLBACK_REQUIRED", "BLOCKED"),
    "PRODUCTION_VERIFICATION_RUNNING": ("PRODUCTION_VERIFIED", "PRODUCTION_VERIFICATION_FAILED", "ROLLBACK_REQUIRED"),
    "PRODUCTION_VERIFICATION_FAILED": ("PRODUCTION_VERIFICATION_RUNNING", "ROLLBACK_REQUIRED", "BLOCKED", "DEPLOYMENT_AUTHORIZED"),
    "PRODUCTION_VERIFIED": ("POST_LAUNCH_MONITORING", "ROLLBACK_REQUIRED"),
    "POST_LAUNCH_MONITORING": ("STABILIZED", "ROLLBACK_REQUIRED", "PRODUCTION_VERIFICATION_RUNNING"),
    "STABILIZED": ("STABILIZED", "ROLLBACK_REQUIRED"),
    "ROLLBACK_REQUIRED": ("ROLLED_BACK", "BLOCKED"),
    "ROLLED_BACK": ("PLANNING", "RELEASE_READY", "BLOCKED", "EXCEPTION_APPLIED"),
    "EXCEPTION_APPLIED": ("EXCEPTION_APPLIED", "PLANNING"),
}


@total_ordering
@dataclass(frozen=True)
class SemVer:
    """Small semver value object used for ordering framework releases."""

    major: int
    minor: int
    patch: int
    prerelease: str = field(default="", compare=False)
    build: str = field(default="", compare=False)

    @classmethod
    def parse(cls, value: Any) -> Optional["SemVer"]:
        if not isinstance(value, str):
            return None
        match = SEMVER_RE.fullmatch(value.strip())
        if not match:
            return None
        prerelease = match.group(4) or ""
        for identifier in prerelease.split(".") if prerelease else ():
            if identifier.isdigit() and len(identifier) > 1 and identifier.startswith("0"):
                return None
        return cls(int(match.group(1)), int(match.group(2)), int(match.group(3)), prerelease, match.group(5) or "")

    def _prerelease_key(self) -> tuple[Any, ...]:
        if not self.prerelease:
            return (1,)
        identifiers: list[tuple[int, Any]] = []
        for identifier in self.prerelease.split("."):
            if identifier.isdigit():
                identifiers.append((0, int(identifier)))
            else:
                identifiers.append((1, identifier))
        return (0, tuple(identifiers))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SemVer):
            return NotImplemented
        return (self.major, self.minor, self.patch, self._prerelease_key()) == (other.major, other.minor, other.patch, other._prerelease_key())

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SemVer):
            return NotImplemented
        return (self.major, self.minor, self.patch, self._prerelease_key()) < (other.major, other.minor, other.patch, other._prerelease_key())


def parse_semver(value: Any) -> Optional[SemVer]:
    """Public semver parser used by the validator and negative controls."""

    return SemVer.parse(value)


@dataclass
class Finding:
    rule_id: str
    severity: str
    file: str
    location: str
    message: str
    expected: Any
    observed: Any
    owner: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "RULE_ID": self.rule_id,
            "SEVERITY": self.severity,
            "FILE": self.file,
            "LOCATION": self.location,
            "MESSAGE": self.message,
            "EXPECTED": self.expected,
            "OBSERVED": self.observed,
            "OWNER": self.owner,
        }


@dataclass
class Check:
    rule_id: str
    category: str
    status: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {
            "rule_id": self.rule_id,
            "category": self.category,
            "status": self.status,
            "detail": self.detail,
        }


DEFAULT_MANIFEST: dict[str, Any] = {
    "canonical_version_source": "framework-version.json",
    "current_version_documents": [],
    "canonical_markdown": [],
    "canonical_json_roots": ["schemas", "templates"],
    "python_roots": ["framework_validation"],
    "canonical_protocol_registry": "schemas/protocols.json",
    "canonical_gate_registry": "schemas/gates.json",
    "canonical_phase_registry": "schemas/phases.json",
    "canonical_state_registry": "schemas/state-ownership.json",
    "canonical_frozen_registry": "schemas/frozen-projects.json",
    "canonical_test_registry": "schemas/test-suites.json",
    "site_profile_schema": "schemas/site-profile.schema.json",
    "current_site_profile": "templates/site-profile.json",
    "frozen_guard_path": "browser-qa/guards/frozen_integrity_guard.py",
    "protected_paths": ["projects/"],
    "workflow_path": ".github/workflows/framework-validation.yml",
    "runtime_report_path": "framework-validation/reports/runtime/framework-validation-report.json",
    "certification_report_pattern": "framework-validation/reports/{version}-certification.json",
    "explicit_negative_fixture_metadata": "fixture.json",
    "canonical_templates": ["templates/site-profile.json", "templates/framework-validation-review.md"],
}


def _posix(value: str) -> str:
    return value.replace("\\", "/").lstrip("./")


def _resolve_inside_root(root: Path, relative: str) -> Optional[Path]:
    """Resolve a repository-relative path without allowing root escape."""

    candidate = (root / Path(str(relative).replace("/", os.sep))).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def _phase_key(value: Any) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return Decimal("Infinity")


def _unique_records(records: Iterable[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    output = []
    for record in records:
        if record not in seen:
            seen.add(record)
            output.append(record)
    return output


def _walk_dict(value: Any, prefix: str = "") -> Iterable[tuple[str, Any]]:
    if not isinstance(value, dict):
        return
    for key, child in value.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        yield path, child
        if isinstance(child, dict):
            yield from _walk_dict(child, path)
        elif isinstance(child, list):
            for index, item in enumerate(child):
                if isinstance(item, dict):
                    yield from _walk_dict(item, f"{path}[{index}]")


def _lock_error_records(profile: Any, current: bool = True) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    if not isinstance(profile, dict):
        return [("SITE_PROFILE_TYPE", "site-profile must be a JSON object")]

    locks = profile.get("locks")
    if current:
        if not isinstance(locks, dict):
            records.append(("OWNER_LOCK_INVARIANT", "current profile must contain a locks object"))
        else:
            observed = sorted(locks)
            expected = sorted(CANONICAL_LOCKS)
            if observed != expected:
                records.append(("OWNER_LOCK_INVARIANT", f"current locks must be exactly {expected}; observed {observed}"))
            for name, value in locks.items():
                if name in CANONICAL_LOCKS and not isinstance(value, bool):
                    records.append(("OWNER_LOCK_TYPE", f"{name} must be boolean"))
    elif locks is not None and not isinstance(locks, dict):
        records.append(("OWNER_LOCK_TYPE", "historical locks, when present, must be an object"))

    for path, value in _walk_dict(profile):
        key = path.rsplit(".", 1)[-1]
        if key.endswith("_locked") and key not in CANONICAL_LOCKS:
            records.append(("OWNER_LOCK_INVARIANT", f"non-canonical owner lock {path} is forbidden"))
        if key in FORBIDDEN_OWNER_LOCKS:
            records.append(("OWNER_LOCK_INVARIANT", f"forbidden owner lock {path} is present"))
    return _unique_records(records)


def validate_owner_locks(profile: Mapping[str, Any], current: bool = True) -> list[str]:
    """Return rule IDs raised by a profile's lock shape."""

    return [rule_id for rule_id, _ in _lock_error_records(profile, current=current)]


def _validate_transition_path(path: Sequence[str]) -> Optional[str]:
    if not path:
        return "empty transition path"
    for source, target in zip(path, path[1:]):
        if source not in LAUNCH_STATUSES:
            return f"unknown source status {source!r}"
        if target not in LAUNCH_STATUSES:
            return f"unknown target status {target!r}"
        if target not in LAUNCH_TRANSITIONS.get(source, ()):
            return f"illegal transition {source} -> {target}"
    return None


def validate_transition_path(path: Sequence[str]) -> bool:
    """Return whether a launch status history follows the canonical graph."""

    return _validate_transition_path(path) is None


def _profile_error_records(profile: Any, current: bool, current_version: str, legacy_versions: set[str]) -> list[tuple[str, str]]:
    records = _lock_error_records(profile, current=current)
    if not isinstance(profile, dict):
        return _unique_records(records)

    schema_version = profile.get("schema_version")
    if current:
        if schema_version != current_version:
            records.append(("CURRENT_SCHEMA_VERSION_DRIFT", f"current profile schema_version must be {current_version!r}; observed {schema_version!r}"))
        if profile.get("framework_version") != current_version:
            records.append(("CURRENT_FRAMEWORK_VERSION_DRIFT", f"current profile framework_version must be {current_version!r}; observed {profile.get('framework_version')!r}"))
        for key in ("schema_version", "framework_version", "project_name", "locks"):
            if key not in profile:
                records.append(("CURRENT_PROFILE_REQUIRED_FIELD", f"current profile is missing required field {key!r}"))
        for key in ("schema_version", "framework_version", "project_name"):
            if key in profile and not isinstance(profile.get(key), str):
                records.append(("CURRENT_PROFILE_FIELD_TYPE", f"current profile field {key!r} must be a string"))
        if "version" in profile and parse_semver(profile.get("version")) is None:
            records.append(("CURRENT_PROFILE_VERSION_SEMVER", "current profile version must be a strict semantic version"))
        for state_name in (
            "research",
            "seo",
            "design_intelligence",
            "measurement",
            "security_privacy",
            "browser_qa",
            "accessibility",
            "gauntlet",
            "handoff",
            "signature_choreography",
            "visual_prototypes",
        ):
            if state_name in profile and not isinstance(profile.get(state_name), dict):
                records.append(("CURRENT_STATE_OBJECT_TYPE", f"current state object {state_name!r} must be an object"))
        if "launch_ops" in profile and not isinstance(profile.get("launch_ops"), dict):
            records.append(("CURRENT_STATE_OBJECT_TYPE", "current state object 'launch_ops' must be an object"))
        if "framework_validation" in profile:
            records.append(("FRAMEWORK_STATE_SEPARATION", "framework self-validation state must remain outside site-profile.json"))
    else:
        if schema_version is not None and schema_version not in legacy_versions:
            records.append(("HISTORICAL_SCHEMA_UNSUPPORTED", f"historical schema_version {schema_version!r} has no compatibility rule"))

    if "cro" in profile:
        measurement_present = "measurement" in profile
        if current or measurement_present or (parse_semver(schema_version) and parse_semver(schema_version) >= SemVer(2, 6, 0)):
            records.append(("OBSOLETE_CURRENT_STATE", "cro{} is superseded and cannot be current alongside measurement{}"))

    for path, value in _walk_dict(profile):
        key = path.rsplit(".", 1)[-1]
        if key.endswith("_verified") or key in {"complete", "confirmed", "deployed", "deployment_authorized", "stabilization_complete"}:
            if not isinstance(value, bool):
                records.append(("STATE_BOOLEAN_TYPE", f"{path} must be boolean"))
        if key == "exception":
            if not current and value is None:
                continue
            if not isinstance(value, dict) or not isinstance(value.get("applied"), bool) or "reason" not in value:
                records.append(("EXCEPTION_SHAPE", f"{path} must contain boolean applied and reason"))
            elif value.get("applied") is True and not value.get("reason"):
                records.append(("EXCEPTION_REASON_REQUIRED", f"{path}.reason is required when applied is true"))

    launch_ops = profile.get("launch_ops")
    if isinstance(launch_ops, dict):
        status = launch_ops.get("status")
        if status is not None and status not in LAUNCH_STATUSES:
            records.append(("LAUNCH_STATUS_ENUM", f"launch_ops.status {status!r} is not canonical"))
        history = launch_ops.get("status_history") or launch_ops.get("transition_history")
        if history:
            if isinstance(history, list) and all(isinstance(item, str) for item in history):
                transition_error = _validate_transition_path(history)
            else:
                transition_error = "transition history must be an ordered list of statuses"
            if transition_error:
                records.append(("INVALID_STATE_TRANSITION", transition_error))
    return _unique_records(records)


def _state_error_records(registry: Any) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    if not isinstance(registry, dict) or not isinstance(registry.get("states"), list):
        return [("STATE_OWNERSHIP_REGISTRY_SHAPE", "state ownership registry must contain a states array")]
    active_paths: dict[str, str] = {}
    active_concepts: dict[str, str] = {}
    for index, entry in enumerate(registry["states"]):
        location = f"states[{index}]"
        if not isinstance(entry, dict):
            records.append(("STATE_OWNERSHIP_REGISTRY_SHAPE", f"{location} must be an object"))
            continue
        required = {"path", "canonical_concept", "status", "owner_protocol"}
        missing = sorted(required - set(entry))
        if missing:
            records.append(("STATE_OWNERSHIP_REGISTRY_SHAPE", f"{location} missing {missing}"))
            continue
        status = entry["status"]
        if status not in VALID_STATUSES:
            records.append(("STATE_STATUS_ENUM", f"{location}.status {status!r} is invalid"))
        if status == "ACTIVE":
            path = str(entry["path"])
            concept = str(entry["canonical_concept"])
            if path in active_paths:
                records.append(("DUPLICATE_STATE_OWNERSHIP", f"active state path {path!r} is owned by both {active_paths[path]!r} and {entry['owner_protocol']!r}"))
            else:
                active_paths[path] = str(entry["owner_protocol"])
            if concept in active_concepts:
                records.append(("DUPLICATE_CANONICAL_COMPLETION_FLAG", f"active concept {concept!r} has more than one canonical state"))
            else:
                active_concepts[concept] = path
    aliases = registry.get("aliases", [])
    if not isinstance(aliases, list):
        records.append(("STATE_OWNERSHIP_REGISTRY_SHAPE", "aliases must be an array"))
    else:
        for index, alias in enumerate(aliases):
            if not isinstance(alias, dict) or alias.get("status") not in {"DEPRECATED", "SUPERSEDED", "HISTORICAL"}:
                records.append(("STATE_DEPRECATION_POLICY", f"aliases[{index}] must use a non-active deprecation status"))
            if isinstance(alias, dict) and alias.get("path") in active_paths:
                records.append(("OBSOLETE_CURRENT_STATE", f"deprecated alias {alias.get('path')!r} is also active"))
    return _unique_records(records)


def validate_state_ownership_registry(registry: Mapping[str, Any]) -> list[str]:
    """Return rule IDs raised by the state ownership registry."""

    return [rule_id for rule_id, _ in _state_error_records(registry)]


def _registry_path_error_records(registry: Any, root: Optional[Path] = None, kind: str = "protocol") -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    key = "protocols" if kind == "protocol" else "gates"
    if not isinstance(registry, dict) or not isinstance(registry.get(key), list):
        return [(f"{kind.upper()}_REGISTRY_SHAPE", f"{kind} registry must contain a {key} array")]
    ids: set[str] = set()
    active_domains: dict[str, str] = {}
    active_state_owners: dict[str, str] = {}
    for index, entry in enumerate(registry[key]):
        location = f"{key}[{index}]"
        if not isinstance(entry, dict):
            records.append((f"{kind.upper()}_REGISTRY_SHAPE", f"{location} must be an object"))
            continue
        identity = entry.get("id") if kind == "protocol" else entry.get("name")
        if not isinstance(identity, str) or not identity:
            records.append((f"{kind.upper()}_IDENTITY", f"{location} has no identity"))
            continue
        if identity in ids:
            records.append((f"DUPLICATE_{kind.upper()}_IDENTITY", f"{identity!r} appears more than once"))
        ids.add(identity)
        status = entry.get("status")
        if status not in VALID_STATUSES:
            records.append((f"{kind.upper()}_STATUS", f"{identity} has invalid status {status!r}"))
        if kind == "protocol":
            for field_name in ("path", "domain", "phase", "state_owner"):
                if not entry.get(field_name):
                    records.append(("PROTOCOL_REGISTRY_SHAPE", f"{identity} is missing {field_name}"))
            if status == "ACTIVE":
                domain = str(entry.get("domain"))
                if domain in active_domains and not (entry.get("supersedes") or entry.get("superseded_by")):
                    records.append(("DUPLICATE_ACTIVE_PROTOCOL_DOMAIN", f"active domain {domain!r} is claimed by {active_domains[domain]!r} and {identity!r}"))
                active_domains[domain] = identity
                state_owner = str(entry.get("state_owner"))
                if state_owner in active_state_owners and not (entry.get("supersedes") or entry.get("superseded_by")):
                    records.append(("DUPLICATE_PROTOCOL_STATE_OWNER", f"active state owner {state_owner!r} is claimed by {active_state_owners[state_owner]!r} and {identity!r}"))
                active_state_owners[state_owner] = identity
                if entry.get("superseded_by"):
                    records.append(("SUPERSEDED_PROTOCOL_ACTIVE", f"active protocol {identity!r} cannot retain a superseded_by pointer"))
            superseded_by = entry.get("superseded_by")
            if status == "SUPERSEDED" and not superseded_by:
                records.append(("SUPERSEDED_PROTOCOL_POINTER", f"superseded protocol {identity!r} must point to its replacement"))
        else:
            for field_name in ("type", "authoritative_state", "phase", "owner_protocol", "owner_artifact"):
                if field_name not in entry:
                    records.append(("GATE_REGISTRY_SHAPE", f"{identity} is missing {field_name}"))
            if entry.get("type") not in VALID_GATE_TYPES:
                records.append(("GATE_TYPE_ENUM", f"{identity} has invalid gate type {entry.get('type')!r}"))
    if kind == "protocol":
        for entry in registry[key]:
            if not isinstance(entry, dict):
                continue
            replacement = entry.get("superseded_by")
            if replacement and replacement not in ids:
                records.append(("BROKEN_PROTOCOL_COMPATIBILITY_POINTER", f"{entry.get('id')} points to missing protocol {replacement!r}"))
            predecessors = entry.get("supersedes", []) or []
            if not isinstance(predecessors, list):
                records.append(("PROTOCOL_REGISTRY_SHAPE", f"{entry.get('id')} supersedes must be an array"))
                predecessors = []
            for predecessor in predecessors:
                if predecessor not in ids:
                    records.append(("BROKEN_PROTOCOL_COMPATIBILITY_POINTER", f"{entry.get('id')} supersedes missing protocol {predecessor!r}"))
    if kind == "gate":
        owner_lock_names = sorted(
            str(entry.get("name")).lower() for entry in registry[key]
            if isinstance(entry, dict) and entry.get("status") == "ACTIVE" and entry.get("type") == "OWNER_LOCK"
        )
        if owner_lock_names != sorted(CANONICAL_LOCKS):
            records.append(("OWNER_LOCK_INVARIANT", f"active OWNER_LOCK gates must be exactly {sorted(CANONICAL_LOCKS)}; observed {owner_lock_names}"))
        for entry in registry[key]:
            if not isinstance(entry, dict):
                continue
            name = str(entry.get("name"))
            normalized_name = name.lower()
            if entry.get("type") == "OWNER_LOCK" and normalized_name not in CANONICAL_LOCKS:
                records.append(("OWNER_LOCK_INVARIANT", f"gate {name!r} is an unapproved owner lock"))
            if entry.get("type") != "OWNER_LOCK" and normalized_name.endswith("_locked"):
                records.append(("GATE_LOCK_TYPE_CONFLICT", f"gate {name!r} has a lock identity but is not an OWNER_LOCK"))
    return _unique_records(records)


def validate_protocol_registry(registry: Mapping[str, Any]) -> list[str]:
    """Return rule IDs raised by a protocol registry."""

    return [rule_id for rule_id, _ in _registry_path_error_records(registry, kind="protocol")]


def validate_protocol_paths(registry: Mapping[str, Any], root: str | os.PathLike[str]) -> list[str]:
    """Return rule IDs raised by protocol paths relative to ``root``."""

    root_path = Path(root).resolve()
    if not isinstance(registry, dict) or not isinstance(registry.get("protocols"), list):
        return ["PROTOCOL_REGISTRY_SHAPE"]
    records: list[str] = []
    for entry in registry["protocols"]:
        if not isinstance(entry, dict) or not entry.get("path"):
            continue
        path = _resolve_inside_root(root_path, str(entry["path"]))
        if path is None:
            records.append("PROTOCOL_PATH_OUTSIDE_ROOT")
            continue
        if path.is_file():
            continue
        if entry.get("status") == "ACTIVE":
            records.append("CANONICAL_PROTOCOL_EXISTS")
        else:
            records.append("HISTORICAL_PROTOCOL_NOT_IN_CHECKOUT")
    return sorted(set(records))


def validate_template_references(paths: Iterable[str], root: str | os.PathLike[str]) -> list[str]:
    """Return ``BROKEN_TEMPLATE_REFERENCE`` when a registered path is absent."""

    root_path = Path(root).resolve()
    missing = []
    for path in paths:
        resolved = _resolve_inside_root(root_path, str(path))
        if resolved is None or not resolved.is_file():
            missing.append(str(path))
    return ["BROKEN_TEMPLATE_REFERENCE"] if missing else []


def validate_json_content(text: str) -> list[str]:
    """Return rule IDs raised by a JSON document's contents."""

    try:
        json.loads(text)
    except (TypeError, json.JSONDecodeError):
        return ["INVALID_JSON_ARTIFACT"]
    return []


def validate_site_profile(
    profile: Mapping[str, Any],
    *,
    current: bool,
    current_version: str,
    legacy_versions: Iterable[str] = (),
) -> list[str]:
    """Return rule IDs raised by a current or historical site profile."""

    return [
        rule_id
        for rule_id, _ in _profile_error_records(profile, current, current_version, set(legacy_versions))
    ]


def validate_gate_registry(
    registry: Mapping[str, Any],
    *,
    protocol_ids: Iterable[str] = (),
    phase_ids: Iterable[str] = (),
) -> list[str]:
    """Return rule IDs raised by a gate registry and its known references."""

    records = _registry_path_error_records(registry, kind="gate")
    known_protocols = set(protocol_ids)
    known_phases = set(phase_ids)
    if isinstance(registry, dict) and isinstance(registry.get("gates"), list):
        for entry in registry["gates"]:
            if not isinstance(entry, dict):
                continue
            name = str(entry.get("name"))
            if known_phases and entry.get("phase") not in known_phases:
                records.append(("BROKEN_GATE_PHASE_REFERENCE", f"gate {name} points to missing phase {entry.get('phase')!r}"))
            if known_protocols and entry.get("owner_protocol") not in known_protocols:
                records.append(("UNKNOWN_GATE_OWNER", f"gate {name} has unknown owner protocol {entry.get('owner_protocol')!r}"))
    return sorted({rule_id for rule_id, _ in records})


def _read_json_file(path: Path) -> tuple[Optional[Any], Optional[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, UnicodeDecodeError) as exc:
        return None, str(exc)
    except json.JSONDecodeError as exc:
        return None, f"line {exc.lineno}, column {exc.colno}: {exc.msg}"


class ValidationContext:
    def __init__(self, root: Path, report_paths: Iterable[str] = ()) -> None:
        self.root = root.resolve()
        self.report_paths = {_posix(path) for path in report_paths}
        self.checks: list[Check] = []
        self.findings: list[Finding] = []
        self.json_cache: dict[str, Optional[Any]] = {}
        self.metadata: dict[str, Any] = {}
        self.manifest: dict[str, Any] = dict(DEFAULT_MANIFEST)

    def rel(self, path: Path | str) -> str:
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        try:
            return candidate.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return str(path).replace("\\", "/")

    def path(self, relative: str) -> Path:
        return self.root / Path(relative.replace("/", os.sep))

    def read_json(self, relative: str) -> Optional[Any]:
        relative = _posix(relative)
        if relative in self.json_cache:
            return self.json_cache[relative]
        path = self.path(relative)
        if not path.is_file():
            self.json_cache[relative] = None
            return None
        value, _ = _read_json_file(path)
        self.json_cache[relative] = value
        return value

    def check(
        self,
        rule_id: str,
        category: str,
        passed: bool,
        detail: str,
        *,
        file: str = "repository",
        location: str = "root",
        expected: Any = "no violation",
        observed: Any = None,
        severity: str = "ERROR",
        blocked: bool = False,
        owner: str = "framework-validation",
    ) -> bool:
        if passed:
            status = "PASS"
        elif blocked:
            status = "BLOCKED"
        elif severity == "WARNING":
            status = "WARNING"
        elif severity == "INFO":
            status = "INFO"
        else:
            status = "FAIL"
        self.checks.append(Check(rule_id, category, status, detail))
        if not passed:
            self.findings.append(Finding(rule_id, severity, file, location, detail, expected, observed, owner))
        return passed


def _load_manifest(ctx: ValidationContext) -> None:
    path = "framework_validation_manifest.json"
    value = ctx.read_json(path)
    if value is None:
        value = ctx.read_json("schemas/validation-manifest.json")
    if isinstance(value, dict):
        merged = dict(DEFAULT_MANIFEST)
        merged.update(value)
        ctx.manifest = merged
    else:
        ctx.check(
            "VALIDATION_MANIFEST_PRESENT",
            "structural",
            False,
            "canonical validation manifest schemas/validation-manifest.json is missing or invalid",
            file="schemas/validation-manifest.json",
            location="root",
            expected="valid JSON object",
            observed="missing or invalid",
        )


def _git_output(root: Path, args: Sequence[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip()


def _git_status(root: Path) -> str:
    return _git_output(root, ["status", "--porcelain=v1"])


def _git_identity(root: Path) -> dict[str, str]:
    return {
        "branch": _git_output(root, ["branch", "--show-current"]) or "DETACHED_OR_UNKNOWN",
        "commit_sha": _git_output(root, ["rev-parse", "HEAD"]) or "UNKNOWN",
    }


def _git_divergence(root: Path, head_sha: str) -> dict[str, Any]:
    main_ref = "origin/main"
    main_sha = _git_output(root, ["rev-parse", "--verify", main_ref])
    result: dict[str, Any] = {
        "canonical_development_head": head_sha,
        "remote_main_ref": main_ref,
        "remote_main_head": main_sha or "UNAVAILABLE",
        "status": "REMOTE_MAIN_UNAVAILABLE",
    }
    if not main_sha or not head_sha or head_sha == "UNKNOWN":
        return result
    if main_sha == head_sha:
        result["status"] = "ALIGNED"
        return result
    main_in_head = subprocess.run(["git", "merge-base", "--is-ancestor", main_sha, head_sha], cwd=root, check=False).returncode == 0
    head_in_main = subprocess.run(["git", "merge-base", "--is-ancestor", head_sha, main_sha], cwd=root, check=False).returncode == 0
    if main_in_head:
        result["status"] = "REMOTE_MAIN_BEHIND_DEVELOPMENT"
    elif head_in_main:
        result["status"] = "DEVELOPMENT_BEHIND_REMOTE_MAIN"
    else:
        result["status"] = "DIVERGED"
    return result


def _version_at_pointer(value: Any, pointer: str) -> Any:
    current = value
    for part in pointer.strip("/").split("/"):
        if not part:
            continue
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def _extract_versions(text: str) -> list[str]:
    return MARKER_VERSION_RE.findall(text)


def validate_version_markers(text: str, expected: str) -> list[str]:
    """Return rule IDs when a versioned document drifts from ``expected``."""

    versions = _extract_versions(text)
    return [] if versions and all(version == expected for version in versions) else ["VERSION_DOCUMENT_CONSISTENCY"]


def _check_versions(ctx: ValidationContext) -> str:
    source_rel = str(ctx.manifest.get("canonical_version_source", "framework-version.json"))
    source = ctx.read_json(source_rel)
    canonical = source.get("version") if isinstance(source, dict) else None
    current_version = canonical if isinstance(canonical, str) else "0.0.0"
    previous = source.get("previous_version") if isinstance(source, dict) else None
    ctx.metadata["framework_version"] = current_version
    ctx.metadata["previous_version"] = previous
    lineage = source.get("lineage") if isinstance(source, dict) else {}
    if not isinstance(lineage, dict):
        lineage = {}
    ctx.metadata["base_branch"] = lineage.get("base_branch", "UNKNOWN")
    ctx.metadata["base_commit"] = lineage.get("base_commit", "UNKNOWN")
    ctx.metadata["base_version"] = lineage.get("base_version", previous or "UNKNOWN")

    parsed = parse_semver(canonical)
    ctx.check(
        "CANONICAL_VERSION_SEMVER",
        "version",
        parsed is not None,
        f"canonical framework version is {canonical!r}",
        file=source_rel,
        location="/version",
        expected="strict semantic version MAJOR.MINOR.PATCH",
        observed=canonical,
    )
    ctx.check(
        "CANONICAL_VERSION_AUTHORITY",
        "version",
        isinstance(source, dict) and source.get("source_of_truth") is True and source.get("status") == "CURRENT",
        "framework-version.json must be marked as the current source of truth",
        file=source_rel,
        location="/source_of_truth",
        expected={"source_of_truth": True, "status": "CURRENT"},
        observed=source if isinstance(source, dict) else "missing or invalid",
    )
    previous_semver = parse_semver(previous)
    if parsed is not None and previous is not None:
        monotonic = previous_semver is not None and parsed > previous_semver
        ctx.check(
            "VERSION_MONOTONICITY",
            "version",
            monotonic,
            f"framework version {canonical!r} must increase from previous version {previous!r}",
            file=source_rel,
            location="/previous_version",
            expected="current semver greater than previous semver",
            observed={"current": canonical, "previous": previous},
        )
        if previous_semver and parsed.major > previous_semver.major:
            intentional = source.get("release_type") == "major" and source.get("breaking_change") is True
            ctx.check(
                "INTENTIONAL_MAJOR_RELEASE",
                "version",
                intentional,
                "major framework releases require explicit major release and breaking-change declarations",
                file=source_rel,
                location="/release_type",
                expected={"release_type": "major", "breaking_change": True},
                observed={"release_type": source.get("release_type") if isinstance(source, dict) else None, "breaking_change": source.get("breaking_change") if isinstance(source, dict) else None},
            )
    elif previous is not None:
        ctx.check(
            "PREVIOUS_VERSION_SEMVER",
            "version",
            previous_semver is not None,
            f"previous framework version {previous!r} must use semantic versioning",
            file=source_rel,
            location="/previous_version",
            expected="strict semantic version",
            observed=previous,
        )

    if lineage.get("base_version"):
        lineage_base = lineage["base_version"]
        ctx.check(
            "LINEAGE_BASE_VERSION_CONSISTENCY",
            "version",
            lineage_base == previous,
            "lineage base_version must match previous_version",
            file=source_rel,
            location="/lineage/base_version",
            expected=previous,
            observed=lineage_base,
        )

    legacy = ctx.read_json("schemas/compatibility.json") or {}
    legacy_versions = set(legacy.get("legacy_schema_versions", [])) if isinstance(legacy, dict) else set()
    ctx.metadata["legacy_schema_versions"] = sorted(legacy_versions)
    for document in ctx.manifest.get("current_version_documents", []):
        if not isinstance(document, dict):
            ctx.check("VERSION_DOCUMENT_REGISTRY_SHAPE", "version", False, "version document entry must be an object", file="schemas/validation-manifest.json", location="/current_version_documents")
            continue
        relative = str(document.get("path", ""))
        path = ctx.path(relative)
        if not path.is_file():
            ctx.check(
                "VERSION_DOCUMENT_MISSING",
                "version",
                False,
                f"current version document {relative!r} is missing",
                file=relative or "schemas/validation-manifest.json",
                location="root",
                expected="file exists",
                observed="missing",
            )
            continue
        expected = canonical
        if "json_pointer" in document:
            value = ctx.read_json(relative)
            observed = _version_at_pointer(value, str(document["json_pointer"]))
            ctx.check(
                "VERSION_DOCUMENT_CONSISTENCY",
                "version",
                observed == expected,
                f"{relative} version marker derives from canonical framework version",
                file=relative,
                location=str(document["json_pointer"]),
                expected=expected,
                observed=observed,
            )
        else:
            document_text = path.read_text(encoding="utf-8")
            versions = _extract_versions(document_text)
            ctx.check(
                "VERSION_DOCUMENT_CONSISTENCY",
                "version",
                not validate_version_markers(document_text, str(expected)),
                f"{relative} contains one consistent FRAMEWORK_VERSION marker",
                file=relative,
                location="FRAMEWORK_VERSION",
                expected=expected,
                observed=versions,
            )
    return current_version


def _check_structure(ctx: ValidationContext) -> None:
    required = {
        str(ctx.manifest.get("canonical_version_source")),
        str(ctx.manifest.get("canonical_protocol_registry")),
        str(ctx.manifest.get("canonical_gate_registry")),
        str(ctx.manifest.get("canonical_phase_registry")),
        str(ctx.manifest.get("canonical_state_registry")),
        str(ctx.manifest.get("canonical_frozen_registry")),
        str(ctx.manifest.get("canonical_test_registry")),
        str(ctx.manifest.get("site_profile_schema")),
        str(ctx.manifest.get("current_site_profile")),
        str(ctx.manifest.get("workflow_path")),
        str(ctx.manifest.get("frozen_guard_path")),
        "FRAMEWORK-VALIDATION-PROTOCOL.md",
        "templates/framework-validation-review.md",
        "framework_validation/__main__.py",
    }
    missing = sorted(relative for relative in required if not ctx.path(relative).exists())
    ctx.check(
        "FRAMEWORK_STRUCTURE",
        "structural",
        not missing,
        "canonical framework validation structure exists",
        file="schemas/validation-manifest.json",
        location="root",
        expected="all required framework artifacts exist",
        observed={"missing": missing},
    )
    competing_sources = [candidate for candidate in ("VERSION", "VERSION.txt", "framework-version.yaml") if ctx.path(candidate).exists()]
    ctx.check(
        "SINGLE_CANONICAL_VERSION_SOURCE",
        "structural",
        not competing_sources,
        "framework-version.json is the only canonical framework version source",
        file="framework-version.json",
        location="root",
        expected="no competing root version source",
        observed=competing_sources,
    )


def _is_explicit_negative_fixture(path: Path, root: Path) -> bool:
    try:
        relative_parts = path.resolve().relative_to(root.resolve()).parts
    except ValueError:
        return False
    if "fixtures" not in {part.lower() for part in relative_parts}:
        return False
    metadata_path = path.parent / "fixture.json"
    if not metadata_path.is_file():
        return False
    metadata, error = _read_json_file(metadata_path)
    return error is None and isinstance(metadata, dict) and metadata.get("validation") == "negative" and metadata.get("allow_invalid_json") is True


def _iter_json_files(ctx: ValidationContext) -> Iterable[Path]:
    roots = ctx.manifest.get("canonical_json_roots", [])
    seen: set[Path] = set()
    for configured in roots:
        path = ctx.path(str(configured))
        if path.is_file() and path.suffix.lower() == ".json":
            candidates = [path]
        elif path.is_dir():
            candidates = sorted(path.rglob("*.json"))
        else:
            candidates = []
        for candidate in candidates:
            relative = ctx.rel(candidate)
            if relative in seen or relative.startswith(REPORT_RUNTIME_PREFIX) or _is_explicit_negative_fixture(candidate, ctx.root):
                continue
            seen.add(relative)
            yield candidate


def _check_json_artifacts(ctx: ValidationContext) -> None:
    invalid: list[tuple[str, str]] = []
    count = 0
    for path in _iter_json_files(ctx):
        count += 1
        value, error = _read_json_file(path)
        if error:
            invalid.append((ctx.rel(path), error))
        else:
            ctx.json_cache[ctx.rel(path)] = value
    ctx.check(
        "JSON_ARTIFACT_VALIDITY",
        "schema",
        not invalid,
        f"validated {count} canonical JSON artifact(s)",
        file="schemas/validation-manifest.json",
        location="/canonical_json_roots",
        expected="every canonical JSON artifact parses",
        observed=invalid or {"files_checked": count},
    )
    for relative, error in invalid:
        ctx.check(
            "INVALID_JSON_ARTIFACT",
            "schema",
            False,
            f"canonical JSON artifact is invalid: {error}",
            file=relative,
            location="json",
            expected="valid JSON",
            observed=error,
        )


def _check_site_profile_schema(ctx: ValidationContext, current_version: str) -> None:
    schema_rel = str(ctx.manifest.get("site_profile_schema"))
    schema = ctx.read_json(schema_rel)
    schema_ok = isinstance(schema, dict) and schema.get("$schema", "").startswith("https://json-schema.org/")
    if schema_ok:
        locks = schema.get("$defs", {}).get("locks", {})
        schema_ok = (
            isinstance(locks, dict)
            and sorted(locks.get("required", [])) == sorted(CANONICAL_LOCKS)
            and locks.get("additionalProperties") is False
            and schema.get("x-framework-version") == current_version
        )
    ctx.check(
        "SITE_PROFILE_SCHEMA_AUTHORITY",
        "schema",
        schema_ok,
        "current site-profile schema declares the five-lock contract and framework version",
        file=schema_rel,
        location="/$defs/locks",
        expected={"five_locks": True, "x-framework-version": current_version},
        observed=schema if not schema_ok else {"five_locks": True, "x-framework-version": current_version},
    )
    profile_rel = str(ctx.manifest.get("current_site_profile"))
    profile = ctx.read_json(profile_rel)
    errors = _profile_error_records(profile, True, current_version, set(ctx.metadata.get("legacy_schema_versions", [])))
    if not errors:
        ctx.check("CURRENT_SITE_PROFILE_VALID", "schema", True, "current templates/site-profile.json passes the current profile contract", file=profile_rel, location="root")
    else:
        for rule_id, detail in errors:
            ctx.check(rule_id, "schema", False, detail, file=profile_rel, location="profile", expected="current profile contract", observed=profile)

    compatibility = ctx.read_json("schemas/compatibility.json")
    compatibility_ok = isinstance(compatibility, dict) and compatibility.get("rules", {}).get("historical_is_read_only") is True and compatibility.get("rules", {}).get("framework_validation_state_is_external_to_site_profile") is True
    ctx.check(
        "SCHEMA_COMPATIBILITY_POLICY",
        "compatibility",
        compatibility_ok,
        "historical schemas have explicit compatibility rules and self-validation remains external to site profiles",
        file="schemas/compatibility.json",
        location="/rules",
        expected="explicit compatibility policy",
        observed=compatibility.get("rules") if isinstance(compatibility, dict) else "missing or invalid",
    )

    frozen_registry = ctx.read_json(str(ctx.manifest.get("canonical_frozen_registry")))
    projects_root = ctx.path("projects")
    historical_profiles: list[Path] = []
    if projects_root.is_dir():
        historical_profiles = sorted(projects_root.rglob("site-profile.json"))
    for path in historical_profiles:
        profile_value, error = _read_json_file(path)
        if error:
            continue
        errors = _profile_error_records(profile_value, False, current_version, set(ctx.metadata.get("legacy_schema_versions", [])))
        for rule_id, detail in errors:
            ctx.check(rule_id, "compatibility", False, detail, file=ctx.rel(path), location="profile", expected="valid legacy compatibility interpretation", observed=profile_value)
    ctx.metadata["historical_profiles_checked"] = len(historical_profiles)
    ctx.metadata["frozen_registry_entries"] = len(frozen_registry.get("projects", [])) if isinstance(frozen_registry, dict) else 0


def _check_protocols_gates_phases(ctx: ValidationContext) -> None:
    protocol_rel = str(ctx.manifest.get("canonical_protocol_registry"))
    gate_rel = str(ctx.manifest.get("canonical_gate_registry"))
    phase_rel = str(ctx.manifest.get("canonical_phase_registry"))
    protocols = ctx.read_json(protocol_rel)
    gates = ctx.read_json(gate_rel)
    phases = ctx.read_json(phase_rel)
    protocol_errors = _registry_path_error_records(protocols, kind="protocol")
    if not protocol_errors:
        ctx.check("PROTOCOL_REGISTRY_VALID", "invariants", True, "protocol registry shape, statuses, domains, and compatibility pointers are valid", file=protocol_rel, location="/protocols")
    else:
        for rule_id, detail in protocol_errors:
            ctx.check(rule_id, "invariants", False, detail, file=protocol_rel, location="/protocols", expected="coherent protocol registry", observed=protocols)
    protocol_by_id = {entry.get("id"): entry for entry in protocols.get("protocols", []) if isinstance(entry, dict)} if isinstance(protocols, dict) else {}
    if isinstance(protocols, dict):
        for entry in protocols.get("protocols", []):
            if not isinstance(entry, dict):
                continue
            path = str(entry.get("path", ""))
            if not path:
                continue
            resolved_path = _resolve_inside_root(ctx.root, path)
            exists = resolved_path is not None and resolved_path.is_file()
            if resolved_path is None:
                ctx.check(
                    "PROTOCOL_PATH_OUTSIDE_ROOT",
                    "references",
                    False,
                    f"protocol {entry.get('id')} points outside the repository root",
                    file=path,
                    location="path",
                    expected="repository-relative protocol path",
                    observed=path,
                )
                continue
            if entry.get("status") == "ACTIVE":
                ctx.check("CANONICAL_PROTOCOL_EXISTS", "references", exists, f"active protocol {entry.get('id')} resolves to a local file", file=path or protocol_rel, location="path", expected="file exists", observed="present" if exists else "missing")
            elif not exists:
                ctx.check("HISTORICAL_PROTOCOL_NOT_IN_CHECKOUT", "compatibility", False, f"historical protocol {entry.get('id')} is recorded but absent from this checkout", file=path, location="path", expected="historical absence is explicit and non-authoritative", observed="missing", severity="WARNING")

    gate_errors = _registry_path_error_records(gates, kind="gate")
    if not gate_errors:
        ctx.check("GATE_REGISTRY_VALID", "invariants", True, "gate registry shape and five-lock classification are valid", file=gate_rel, location="/gates")
    else:
        for rule_id, detail in gate_errors:
            ctx.check(rule_id, "invariants", False, detail, file=gate_rel, location="/gates", expected="coherent gate registry", observed=gates)
    phase_entries = phases.get("phases", []) if isinstance(phases, dict) else None
    phase_ids: set[str] = set()
    phase_errors: list[tuple[str, str]] = []
    if not isinstance(phase_entries, list):
        phase_errors.append(("PHASE_REGISTRY_SHAPE", "phase registry must contain a phases array"))
    else:
        previous_key: Optional[Decimal] = None
        for index, entry in enumerate(phase_entries):
            if not isinstance(entry, dict) or not entry.get("phase"):
                phase_errors.append(("PHASE_REGISTRY_SHAPE", f"phases[{index}] must contain a phase identity"))
                continue
            identity = str(entry["phase"])
            if identity in phase_ids:
                phase_errors.append(("DUPLICATE_ACTIVE_PHASE_IDENTITY", f"phase {identity!r} appears more than once"))
            phase_ids.add(identity)
            key = _phase_key(identity)
            if previous_key is not None and key <= previous_key:
                phase_errors.append(("PHASE_ORDER_INVALID", f"phase {identity!r} is not strictly after the prior phase"))
            previous_key = key
            if entry.get("protocol") not in protocol_by_id:
                phase_errors.append(("BROKEN_PHASE_PROTOCOL_REFERENCE", f"phase {identity} points to missing protocol {entry.get('protocol')!r}"))
            if entry.get("gate") and isinstance(gates, dict) and entry.get("gate") not in {g.get("name") for g in gates.get("gates", []) if isinstance(g, dict)}:
                phase_errors.append(("BROKEN_PHASE_GATE_REFERENCE", f"phase {identity} points to missing gate {entry.get('gate')!r}"))
            for precondition in entry.get("preconditions", []) or []:
                known_gate_names = {g.get("name") for g in gates.get("gates", []) if isinstance(g, dict)} if isinstance(gates, dict) else set()
                if precondition not in known_gate_names and precondition not in protocol_by_id:
                    phase_errors.append(("BROKEN_PHASE_PRECONDITION", f"phase {identity} points to missing precondition {precondition!r}"))
        protocol_phase_use: dict[str, list[str]] = {}
        for entry in phase_entries:
            if isinstance(entry, dict) and entry.get("protocol"):
                protocol_phase_use.setdefault(str(entry["protocol"]), []).append(str(entry["phase"]))
        for protocol, phase_list in protocol_phase_use.items():
            if len(phase_list) > 1 and protocol not in {"WEBSITE_DIRECTOR_CORE", "IMPLEMENTATION_CONTRACT"}:
                phase_errors.append(("PROTOCOL_PHASE_CONFLICT", f"protocol {protocol!r} is assigned to conflicting phases {phase_list}"))
    if not phase_errors:
        ctx.check("PHASE_REGISTRY_VALID", "invariants", True, "phase registry identities, ordering, and references are valid", file=phase_rel, location="/phases")
    else:
        for rule_id, detail in _unique_records(phase_errors):
            ctx.check(rule_id, "invariants", False, detail, file=phase_rel, location="/phases", expected="ordered resolvable phase registry", observed=phases)

    if isinstance(protocols, dict):
        for entry in protocols.get("protocols", []):
            if not isinstance(entry, dict) or not entry.get("phase"):
                continue
            protocol_id = entry.get("id")
            if str(entry.get("phase")) not in phase_ids:
                ctx.check(
                    "BROKEN_PROTOCOL_PHASE_REFERENCE",
                    "references",
                    False,
                    f"protocol {protocol_id} points to missing phase {entry.get('phase')!r}",
                    file=protocol_rel,
                    location=f"/protocols/{protocol_id}/phase",
                    expected="phase exists",
                    observed=entry.get("phase"),
                )

    if isinstance(gates, dict) and isinstance(phases, dict):
        phase_ids = {str(entry.get("phase")) for entry in phases.get("phases", []) if isinstance(entry, dict)}
        protocol_ids = set(protocol_by_id)
        state_registry = ctx.read_json(str(ctx.manifest.get("canonical_state_registry")))
        active_state_paths = {
            str(entry.get("path"))
            for entry in state_registry.get("states", [])
            if isinstance(entry, dict) and entry.get("status") == "ACTIVE" and entry.get("path")
        } if isinstance(state_registry, dict) else set()

        def state_reference_known(reference: str) -> bool:
            if reference in active_state_paths:
                return True
            for path in active_state_paths:
                if path.endswith(".*") and reference.startswith(path[:-1]):
                    return True
                if "." in path and reference.startswith(path.rsplit(".", 1)[0] + "."):
                    return True
            return False

        for entry in gates.get("gates", []):
            if not isinstance(entry, dict):
                continue
            name = str(entry.get("name"))
            if entry.get("phase") not in phase_ids:
                ctx.check("BROKEN_GATE_PHASE_REFERENCE", "references", False, f"gate {name} points to missing phase {entry.get('phase')!r}", file=gate_rel, location=f"/gates/{name}/phase", expected="phase exists", observed=entry.get("phase"))
            if entry.get("owner_protocol") not in protocol_ids:
                ctx.check("UNKNOWN_GATE_OWNER", "invariants", False, f"gate {name} has unknown owner protocol {entry.get('owner_protocol')!r}", file=gate_rel, location=f"/gates/{name}/owner_protocol", expected="registered protocol id", observed=entry.get("owner_protocol"))
            authoritative_state = str(entry.get("authoritative_state", ""))
            if entry.get("status") == "ACTIVE" and active_state_paths:
                ctx.check(
                    "GATE_STATE_REFERENCE",
                    "invariants",
                    state_reference_known(authoritative_state),
                    f"active gate {name} points to a registered active state concept",
                    file=gate_rel,
                    location=f"/gates/{name}/authoritative_state",
                    expected="active state path or registered wildcard",
                    observed=authoritative_state,
                )
            artifact = str(entry.get("owner_artifact", ""))
            artifact_exists = ctx.path(artifact).exists() if artifact else False
            generated_runtime_artifact = artifact.startswith(REPORT_RUNTIME_PREFIX)
            if entry.get("status") == "ACTIVE":
                ctx.check("ACTIVE_GATE_ARTIFACT_EXISTS", "references", artifact_exists or generated_runtime_artifact, f"active gate {name} has a resolvable owner artifact", file=artifact or gate_rel, location=f"/gates/{name}/owner_artifact", expected="artifact exists or is a designated generated report", observed=artifact)
            elif not artifact_exists:
                ctx.check("HISTORICAL_GATE_ARTIFACT_NOT_IN_CHECKOUT", "compatibility", False, f"historical gate {name} references a lineage artifact absent from this checkout", file=artifact or gate_rel, location=f"/gates/{name}/owner_artifact", expected="historical absence is explicit", observed="missing", severity="WARNING")


def _check_state_ownership(ctx: ValidationContext) -> None:
    relative = str(ctx.manifest.get("canonical_state_registry"))
    registry = ctx.read_json(relative)
    errors = _state_error_records(registry)
    if not errors:
        ctx.check("STATE_OWNERSHIP_REGISTRY_VALID", "invariants", True, "state concepts have one active owner and historical aliases are non-authoritative", file=relative, location="/states")
    else:
        for rule_id, detail in errors:
            ctx.check(rule_id, "invariants", False, detail, file=relative, location="/states", expected="one active owner per concept", observed=registry)
    protocols = ctx.read_json(str(ctx.manifest.get("canonical_protocol_registry"))) or {}
    protocol_ids = {entry.get("id") for entry in protocols.get("protocols", []) if isinstance(entry, dict)} if isinstance(protocols, dict) else set()
    for index, entry in enumerate(registry.get("states", []) if isinstance(registry, dict) else []):
        if not isinstance(entry, dict):
            continue
        owner = entry.get("owner_protocol")
        if owner not in protocol_ids:
            ctx.check("STATE_OWNER_PROTOCOL_UNKNOWN", "invariants", False, f"state {entry.get('path')} has unknown owner protocol {owner!r}", file=relative, location=f"/states/{index}/owner_protocol", expected="registered protocol id", observed=owner)


def _check_template_references(ctx: ValidationContext) -> None:
    templates = [str(path) for path in ctx.manifest.get("canonical_templates", [])]
    gates = ctx.read_json(str(ctx.manifest.get("canonical_gate_registry"))) or {}
    protocols = ctx.read_json(str(ctx.manifest.get("canonical_protocol_registry"))) or {}
    if isinstance(gates, dict):
        templates.extend(
            str(entry.get("owner_artifact"))
            for entry in gates.get("gates", [])
            if isinstance(entry, dict)
            and entry.get("status") == "ACTIVE"
            and str(entry.get("owner_artifact", "")).startswith("templates/")
        )
    if isinstance(protocols, dict):
        templates.extend(
            str(entry.get("path"))
            for entry in protocols.get("protocols", [])
            if isinstance(entry, dict)
            and entry.get("status") == "ACTIVE"
            and str(entry.get("path", "")).startswith("templates/")
        )
    templates = sorted({path for path in templates if path})
    missing = []
    for path in templates:
        resolved = _resolve_inside_root(ctx.root, path)
        if resolved is None or not resolved.is_file():
            missing.append(path)
    ctx.check(
        "TEMPLATE_REFERENCE_INTEGRITY",
        "references",
        not missing,
        "canonical template references resolve",
        file="schemas/validation-manifest.json",
        location="/canonical_templates",
        expected="every active template reference exists",
        observed={"missing": missing, "checked": templates},
    )
    for path in missing:
        ctx.check(
            "BROKEN_TEMPLATE_REFERENCE",
            "references",
            False,
            f"registered template reference {path!r} is missing",
            file="schemas/validation-manifest.json",
            location="/canonical_templates",
            expected="template file exists",
            observed="missing",
        )
    template_dir = ctx.path("templates")
    registered = set(templates)
    if template_dir.is_dir():
        orphans = sorted(
            ctx.rel(path)
            for path in template_dir.iterdir()
            if path.is_file()
            and path.name != "AGENTS.md"
            and ctx.rel(path) not in registered
        )
        if orphans:
            ctx.check("ORPHAN_TEMPLATE", "references", False, "unregistered templates are reported but not deleted", file="templates", location="directory", expected="orphan is explicitly reviewed", observed=orphans, severity="WARNING", owner="framework-owner")
        else:
            ctx.check("ORPHAN_TEMPLATE", "references", True, "no unregistered templates detected", file="templates", location="directory")


def _case_sensitive_target(root: Path, target: str) -> tuple[str, Optional[Path]]:
    normalized = target.replace("\\", "/").lstrip("/")
    current = root
    for component in PurePosixPath(normalized).parts:
        if component in ("", "."):
            continue
        if component == "..":
            current = current.parent
            continue
        if not current.is_dir():
            return "missing", None
        names = {entry.name: entry for entry in current.iterdir()}
        if component in names:
            current = names[component]
            continue
        lower_matches = [entry for entry in current.iterdir() if entry.name.lower() == component.lower()]
        if lower_matches:
            return "case_mismatch", lower_matches[0]
        return "missing", None
    try:
        current.resolve().relative_to(root.resolve())
    except ValueError:
        return "outside_root", None
    return "ok" if current.exists() else "missing", current if current.exists() else None


def _check_markdown_references(ctx: ValidationContext) -> None:
    broken: list[tuple[str, str, str]] = []
    case_mismatches: list[tuple[str, str]] = []
    checked = 0
    for relative in sorted({str(path) for path in ctx.manifest.get("canonical_markdown", [])}):
        path = ctx.path(relative)
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        headings = {re.sub(r"[^a-z0-9 -]", "", heading.lower()).strip().replace(" ", "-") for heading in HEADING_RE.findall(text)}
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = unquote(match.group(1) or match.group(2) or "").strip()
            checked += 1
            if not target or target.startswith("#"):
                if target.startswith("#") and target[1:] not in headings:
                    broken.append((relative, target, "missing anchor"))
                continue
            parsed = urlsplit(target)
            if parsed.scheme in {"http", "https", "mailto", "tel"}:
                continue
            if parsed.scheme == "file":
                # Historical Windows file:/// links are intentionally not
                # resolved against a Linux checkout or this prototype root.
                continue
            target_path = parsed.path
            if not target_path:
                if parsed.fragment and parsed.fragment not in headings:
                    broken.append((relative, target, "missing anchor"))
                continue
            if target_path.startswith("/") and re.match(r"^/[A-Za-z]:/", target_path):
                continue
            resolved_target = (path.parent / target_path).resolve()
            try:
                resolved_target.relative_to(ctx.root.resolve())
            except ValueError:
                broken.append((relative, target, "outside repository"))
                continue
            status, _ = _case_sensitive_target(ctx.root, resolved_target.relative_to(ctx.root).as_posix())
            if status == "missing":
                broken.append((relative, target, "missing file"))
            elif status == "outside_root":
                broken.append((relative, target, "outside repository"))
            elif status == "case_mismatch":
                case_mismatches.append((relative, target))
            if parsed.fragment and parsed.fragment not in headings and status == "ok" and resolved_target.suffix.lower() in {".md", ".markdown"}:
                target_text = resolved_target.read_text(encoding="utf-8")
                target_headings = {re.sub(r"[^a-z0-9 -]", "", heading.lower()).strip().replace(" ", "-") for heading in HEADING_RE.findall(target_text)}
                if parsed.fragment not in target_headings:
                    broken.append((relative, target, "missing anchor"))
    ctx.check(
        "MARKDOWN_REFERENCE_INTEGRITY",
        "references",
        not broken,
        f"validated {checked} internal Markdown reference(s)",
        file="schemas/validation-manifest.json",
        location="/canonical_markdown",
        expected="all repository-relative references resolve",
        observed=broken or {"references_checked": checked},
    )
    ctx.check(
        "MARKDOWN_REFERENCE_CASE",
        "references",
        not case_mismatches,
        "repository-relative Markdown references preserve path casing",
        file="schemas/validation-manifest.json",
        location="/canonical_markdown",
        expected="exact path casing",
        observed=case_mismatches,
    )


def _check_python(ctx: ValidationContext) -> None:
    files: list[Path] = []
    for configured in ctx.manifest.get("python_roots", []):
        path = ctx.path(str(configured))
        if path.is_file() and path.suffix == ".py":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.py")))
    errors: list[tuple[str, str]] = []
    for path in files:
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec", dont_inherit=True)
        except (OSError, UnicodeDecodeError, SyntaxError) as exc:
            errors.append((ctx.rel(path), str(exc)))
    ctx.check(
        "PYTHON_SYNTAX_VALIDATION",
        "structural",
        not errors,
        f"compiled {len(files)} framework Python source file(s) without writing bytecode",
        file="framework_validation/validator.py",
        location="python roots",
        expected="Python sources parse and compile",
        observed=errors or {"files_checked": len(files)},
    )
    package = ctx.path("framework_validation/__init__.py")
    ctx.check(
        "PYTHON_IMPORT_SURFACE",
        "structural",
        package.is_file(),
        "framework_validation exposes a package import surface",
        file="framework_validation/__init__.py",
        location="root",
        expected="package initializer exists",
        observed="present" if package.is_file() else "missing",
    )


def _workflow_rule_ids(text: str) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    lines = text.splitlines()
    if "name:" not in text or "jobs:" not in text or "runs-on:" not in text:
        records.append(("CI_WORKFLOW_SHAPE", "workflow must declare name, jobs, and runs-on"))
    permissions_match = re.search(r"(?ms)^permissions:\s*\n((?:^[ ]+.*\n?)*)", text)
    permissions_block = permissions_match.group(1) if permissions_match else ""
    if not permissions_match or not re.search(r"(?m)^\s+contents:\s*read\s*$", permissions_block):
        records.append(("CI_READ_ONLY_PERMISSIONS", "workflow must explicitly grant contents: read"))
    if re.search(r"(?mi)^\s*(?:contents|permissions):\s*(?:write|write-all)|\bcontents:\s*write\b", text):
        records.append(("CI_READ_ONLY_PERMISSIONS", "workflow grants unnecessary write permission"))
    required_fragments = ("actions/checkout@", "actions/setup-python@", "python -m framework_validation", "actions/upload-artifact@")
    for fragment in required_fragments:
        if fragment not in text:
            records.append(("CI_WORKFLOW_REQUIRED_STEP", f"workflow is missing {fragment}"))
    forbidden = re.compile(r"(?i)(?:git\s+push|gh\s+(?:pr|release)|\bdeploy\b|vercel|netlify|curl\s|invoke-webrequest|secrets\.)")
    for index, line in enumerate(lines, 1):
        if forbidden.search(line):
            records.append(("CI_NO_EXTERNAL_SIDE_EFFECTS", f"forbidden deployment, secret, or network-mutation token at line {index}"))
    if "ubuntu-latest" not in text or "windows-latest" not in text:
        records.append(("CI_PLATFORM_MATRIX", "core workflow must include ubuntu-latest and windows-latest"))
    if "workflow_dispatch:" not in text:
        records.append(("CI_MANUAL_DISPATCH", "workflow must support manual dispatch"))
    if "pull_request:" not in text or "push:" not in text:
        records.append(("CI_TRIGGER_POLICY", "workflow must run for pull requests and pushes"))
    if "framework-development" not in text or "release/**" not in text:
        records.append(("CI_BRANCH_TRIGGER_POLICY", "workflow must include framework-development and release branches"))
    if "extended_browser" in text.lower() and "schedule:" in text:
        records.append(("CI_NO_UNJUSTIFIED_SCHEDULE", "extended browser scheduling is not defined for this capability"))
    return _unique_records(records)


def validate_workflow_text(text: str) -> list[str]:
    """Return workflow rule IDs raised by a synthetic workflow string."""

    return [rule_id for rule_id, _ in _workflow_rule_ids(text)]


def _check_ci(ctx: ValidationContext) -> None:
    relative = str(ctx.manifest.get("workflow_path"))
    path = ctx.path(relative)
    if not path.is_file():
        ctx.check("CI_WORKFLOW_PRESENT", "structural", False, "framework validation GitHub Actions workflow is missing", file=relative, location="root", expected="workflow exists", observed="missing")
        return
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
    except ImportError:
        yaml_ok = "\t" not in text and text.count("[") == text.count("]") and text.count("{") == text.count("}")
    else:
        try:
            parsed_workflow = yaml.safe_load(text)
            yaml_ok = isinstance(parsed_workflow, dict)
        except Exception:
            yaml_ok = False
    ctx.check("CI_WORKFLOW_YAML", "structural", yaml_ok, "framework validation workflow passes the available YAML syntax check", file=relative, location="yaml", expected="parseable YAML", observed="parseable" if yaml_ok else "invalid")
    records = _workflow_rule_ids(text)
    if not records:
        ctx.check("CI_WORKFLOW_SELF_CHECK", "invariants", True, "workflow jobs, permissions, commands, and triggers are safe and complete", file=relative, location="workflow")
    else:
        for rule_id, detail in records:
            ctx.check(rule_id, "invariants", False, detail, file=relative, location="workflow", expected="read-only core validation workflow", observed=detail)


def _load_guard(root: Path, relative: str) -> Optional[type]:
    path = root / relative
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return None
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("website_director_frozen_integrity_guard", path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        # dataclasses resolves postponed annotations through sys.modules while
        # the dynamically loaded guard module is being executed.
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return getattr(module, "FrozenIntegrityGuard", None)
    except (ImportError, OSError, SyntaxError, AttributeError):
        return None
    finally:
        sys.modules.pop(spec.name, None)


def _check_frozen_registry(ctx: ValidationContext) -> None:
    relative = str(ctx.manifest.get("canonical_frozen_registry"))
    registry = ctx.read_json(relative)
    protected = registry.get("protected_paths", []) if isinstance(registry, dict) else []
    entries = registry.get("projects", []) if isinstance(registry, dict) else []
    ctx.metadata["frozen_project_count"] = len(entries) if isinstance(entries, list) else 0
    ctx.check(
        "FROZEN_PROJECT_COUNT_NONZERO",
        "compatibility",
        isinstance(entries, list) and len(entries) > 0,
        "frozen-project registry contains a non-empty historical inventory",
        file=relative,
        location="/projects",
        expected="at least one registered frozen project",
        observed=ctx.metadata["frozen_project_count"],
    )
    protected_ok = isinstance(protected, list) and "projects/" in protected and isinstance(entries, list)
    ctx.check("FROZEN_PROJECT_REGISTRY", "compatibility", protected_ok, "frozen-project inventory declares the protected projects root", file=relative, location="/protected_paths", expected="projects/ registered", observed=registry)
    missing = [entry.get("path") for entry in entries if isinstance(entry, dict) and entry.get("path") and not ctx.path(str(entry["path"])).exists()]
    if missing:
        missing_is_warning = bool((registry.get("policy") or {}).get("missing_registered_project_is_warning")) if isinstance(registry, dict) else False
        ctx.check("FROZEN_PROJECT_CORPUS_NOT_IN_CHECKOUT", "compatibility", False, "registered frozen projects are absent from this checkout; no migration is attempted", file=relative, location="/projects", expected="all registered projects are present", observed={"missing_count": len(missing), "sample": missing[:5]}, severity="WARNING" if missing_is_warning else "ERROR", owner="framework-owner")
    else:
        ctx.check("FROZEN_PROJECT_CORPUS_PRESENT", "compatibility", True, "all registered frozen project paths are present", file=relative, location="/projects")
    guard_relative = str(ctx.manifest.get("frozen_guard_path"))
    guard_class = _load_guard(ctx.root, guard_relative)
    projects_present = ctx.path("projects").is_dir()
    if guard_class is None:
        ctx.check("FROZEN_INTEGRITY_GUARD_AVAILABLE", "frozen_fixture_integrity", False, "registered V2.8 FrozenIntegrityGuard cannot be loaded", file=guard_relative, location="root", expected="guard importable", observed="missing", blocked=projects_present)
        ctx.metadata["frozen_guard"] = None
        return
    ledger = REPORT_RUNTIME_PREFIX + "frozen-integrity-violations.log"
    try:
        guard = guard_class(str(ctx.root), protected_paths=ctx.manifest.get("protected_paths", ["projects/"]), ledger_path=ledger, run_id="framework-validation")
        guard.snapshot()
        ctx.metadata["frozen_guard"] = guard
        ctx.metadata["protected_file_count"] = len(getattr(guard, "_baseline", {}))
        ctx.check(
            "PROTECTED_FILE_COUNT_NONZERO",
            "frozen_fixture_integrity",
            ctx.metadata["protected_file_count"] > 0,
            "frozen-integrity guard captured a non-empty protected project corpus",
            file=guard_relative,
            location="snapshot",
            expected="at least one protected project file",
            observed=ctx.metadata["protected_file_count"],
        )
        ctx.check("FROZEN_INTEGRITY_GUARD_AVAILABLE", "frozen_fixture_integrity", True, "V2.8 FrozenIntegrityGuard was loaded and snapshotted before suite execution", file=guard_relative, location="root")
    except Exception as exc:  # noqa: BLE001
        ctx.metadata["frozen_guard"] = None
        ctx.check("FROZEN_INTEGRITY_GUARD_AVAILABLE", "frozen_fixture_integrity", False, f"FrozenIntegrityGuard could not snapshot protected paths: {exc}", file=guard_relative, location="snapshot", expected="snapshot succeeds", observed=str(exc), blocked=projects_present)


def _check_test_registry(ctx: ValidationContext, run_suites: bool) -> None:
    relative = str(ctx.manifest.get("canonical_test_registry"))
    registry = ctx.read_json(relative)
    suites = registry.get("suites", []) if isinstance(registry, dict) else None
    if not isinstance(suites, list):
        ctx.check("TEST_SUITE_REGISTRY_SHAPE", "versioned_test_suites", False, "test suite registry must contain a suites array", file=relative, location="/suites", expected="array", observed=registry)
        return
    tiers = registry.get("tiers") if isinstance(registry, dict) else None
    core_tier = tiers.get("CORE_FRAMEWORK_CI") if isinstance(tiers, dict) else None
    extended_tier = tiers.get("EXTENDED_BROWSER_CI") if isinstance(tiers, dict) else None
    tier_policy_ok = (
        isinstance(core_tier, dict)
        and core_tier.get("status") == "REQUIRED"
        and isinstance(extended_tier, dict)
        and extended_tier.get("status") == "OPTIONAL"
        and extended_tier.get("enabled") is False
        and extended_tier.get("schedule") is False
    )
    ctx.check(
        "TEST_TIER_POLICY",
        "versioned_test_suites",
        tier_policy_ok,
        "core framework CI is required while extended browser CI remains explicit, optional, and unscheduled",
        file=relative,
        location="/tiers",
        expected={"core": "REQUIRED", "extended_browser": {"status": "OPTIONAL", "enabled": False, "schedule": False}},
        observed=tiers,
    )
    active = [suite for suite in suites if isinstance(suite, dict) and suite.get("status") == "ACTIVE"]
    runs: list[dict[str, Any]] = []
    for index, suite in enumerate(suites):
        if not isinstance(suite, dict):
            ctx.check("TEST_SUITE_REGISTRY_SHAPE", "versioned_test_suites", False, f"suites[{index}] must be an object", file=relative, location=f"/suites/{index}", expected="suite object", observed=suite)
            continue
        suite_id = str(suite.get("id", index))
        command = suite.get("command")
        paths = suite.get("paths", [])
        required = ("command", "paths", "status", "tier")
        missing = [field_name for field_name in required if field_name not in suite]
        if missing:
            ctx.check("TEST_SUITE_REGISTRY_SHAPE", "versioned_test_suites", False, f"suite {suite_id} is missing {missing}", file=relative, location=f"/suites/{index}", expected="registered command and isolation metadata", observed=suite)
            continue
        if suite.get("status") == "ACTIVE":
            missing_paths = [path for path in paths if not ctx.path(str(path)).is_file()]
            ctx.check("ACTIVE_TEST_SUITE_DISCOVERABLE", "versioned_test_suites", not missing_paths, f"active suite {suite_id} is discoverable", file=relative, location=f"/suites/{index}/paths", expected="all registered suite paths exist", observed=missing_paths)
            isolation_fields = {
                "uses_temp_fixtures": True,
                "temporary_browser_profiles": True,
                "isolated_ports": True,
                "persistent_daemon": False,
                "external_writes": False,
                "production_credentials": False,
                "order_independent": True,
            }
            for field_name, expected in isolation_fields.items():
                ctx.check("TEST_ISOLATION_POLICY", "versioned_test_suites", suite.get(field_name) is expected, f"active suite {suite_id} declares isolated test behavior", file=relative, location=f"/suites/{index}/{field_name}", expected=expected, observed=suite.get(field_name))
            command_text = " ".join(str(part) for part in command) if isinstance(command, list) else str(command)
            unsafe = re.search(r"(?i)(?:deploy|publish|curl|invoke-webrequest|production credentials|git push)", command_text)
            ctx.check("TEST_SUITE_NO_EXTERNAL_SIDE_EFFECTS", "versioned_test_suites", not unsafe, f"active suite {suite_id} has no external side-effect command", file=relative, location=f"/suites/{index}/command", expected="local read-only command", observed=command_text)
        elif suite.get("status") == "HISTORICAL" and any(not ctx.path(str(path)).is_file() for path in paths):
            ctx.check("HISTORICAL_SUITE_NOT_IN_CHECKOUT", "compatibility", False, f"historical suite {suite_id} is not present in this checkout", file=relative, location=f"/suites/{index}/paths", expected="historical absence remains explicit", observed=paths, severity="WARNING", owner="framework-owner")

    if not run_suites:
        ctx.check("VERSIONED_TEST_SUITES_EXECUTED", "versioned_test_suites", False, "registered active suites were not executed; use --run-suites for release certification", file=relative, location="/suites", expected="suite execution evidence", observed="not run", blocked=True)
    else:
        for suite in active:
            command = suite.get("command")
            if not isinstance(command, list) or not command or not all(isinstance(part, str) for part in command):
                continue
            try:
                result = subprocess.run(command, cwd=ctx.root, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180, check=False)
                output = ((result.stdout or "") + (result.stderr or "")).strip()
                record = {"id": suite.get("id"), "command": command, "return_code": result.returncode, "output_tail": output[-2000:]}
                runs.append(record)
                ctx.check("VERSIONED_TEST_SUITE_PASS", "versioned_test_suites", result.returncode == 0, f"registered suite {suite.get('id')} completed", file=relative, location=f"/suites/{suite.get('id')}/command", expected="exit code 0", observed=record)
            except (OSError, subprocess.SubprocessError) as exc:
                record = {"id": suite.get("id"), "command": command, "error": str(exc)}
                runs.append(record)
                ctx.check("VERSIONED_TEST_SUITE_BLOCKED", "versioned_test_suites", False, f"registered suite {suite.get('id')} could not execute: {exc}", file=relative, location=f"/suites/{suite.get('id')}/command", expected="suite executable", observed=str(exc), blocked=True)
    ctx.metadata["suite_runs"] = runs


def _check_governance_docs(ctx: ValidationContext, current_version: str) -> None:
    paths = ("AGENTS.md", "SKILL.md", "README.md")
    phase_registry = ctx.read_json(str(ctx.manifest.get("canonical_phase_registry")))
    active_phase = next(
        (
            entry
            for entry in phase_registry.get("phases", [])
            if isinstance(entry, dict) and entry.get("status") == "ACTIVE"
        ),
        {},
    ) if isinstance(phase_registry, dict) else {}
    phase_marker = "framework_phase={}:{}:{}".format(
        active_phase.get("phase", "UNKNOWN"),
        active_phase.get("name", "UNKNOWN"),
        active_phase.get("status", "UNKNOWN"),
    )
    gate_marker = f"framework_gate={active_phase.get('gate', 'UNKNOWN')}"
    required_terms = {
        "framework_version_source=framework-version.json": "version authority",
        "deployment_authority=OWNER_APPROVAL_REQUIRED": "deployment authorization",
        "external_side_effects=NONE": "external side-effect boundary",
        "state_ownership=schemas/state-ownership.json": "state ownership authority",
        "browser_qa=browser-qa/guards/frozen_integrity_guard.py": "browser-QA guard authority",
        "accessibility=owner-controlled historical protocol state": "accessibility boundary",
        "security_privacy=owner-controlled historical protocol state": "security/privacy boundary",
        "framework_validation_state=EXTERNAL_TO_SITE_PROFILE": "framework-state separation",
        phase_marker: "current framework phase",
        gate_marker: "current framework gate",
    }
    expected_lock_text = "owner_locks=" + ",".join(CANONICAL_LOCKS)
    for relative in paths:
        path = ctx.path(relative)
        if not path.is_file():
            ctx.check("GOVERNANCE_DOCUMENT_PRESENT", "structural", False, f"governance document {relative} is missing", file=relative, location="root", expected="document exists", observed="missing")
            continue
        text = path.read_text(encoding="utf-8")
        versions = _extract_versions(text)
        marker_ok = current_version in versions
        ctx.check("GOVERNANCE_VERSION_MARKER", "version", marker_ok, f"{relative} carries the canonical framework version marker", file=relative, location="FRAMEWORK_VERSION", expected=current_version, observed=versions)
        for term, label in required_terms.items():
            ctx.check("AGENTS_GOVERNANCE_CONSISTENCY", "invariants", term in text, f"{relative} records the {label} marker", file=relative, location="FRAMEWORK_GOVERNANCE", expected=term, observed="present" if term in text else "missing")
        lock_values = re.findall(r"owner_locks\s*=\s*([^\n<]+)", text)
        ctx.check("GOVERNANCE_FIVE_LOCKS", "invariants", bool(lock_values) and all(value.strip() == ",".join(CANONICAL_LOCKS) for value in lock_values), f"{relative} preserves exactly five canonical owner locks", file=relative, location="owner_locks", expected=expected_lock_text, observed=lock_values)
        if re.search(r"owner_locks\s*=.*(?:measurement_locked|security_locked|accessibility_locked|launch_locked|seo_locked)", text, re.IGNORECASE):
            ctx.check("GOVERNANCE_NO_SIXTH_LOCK", "invariants", False, f"{relative} introduces a non-canonical owner lock", file=relative, location="owner_locks", expected=expected_lock_text, observed="non-canonical lock")


def _check_impact(ctx: ValidationContext) -> None:
    status_lines = _git_status(ctx.root).splitlines()
    paths: list[str] = []
    for line in status_lines:
        if len(line) >= 4:
            paths.append(line[3:].strip().strip('"'))
    impacts = set()
    for path in paths:
        lower = path.lower().replace("\\", "/")
        if lower.startswith("schemas/") or "framework-validation" in lower or lower in {"framework-version.json", "framework_validation/validator.py"}:
            impacts.add("CORE_GOVERNANCE")
        elif lower.startswith("browser-qa/"):
            impacts.add("BROWSER_QA")
        elif "security" in lower:
            impacts.add("SECURITY")
        elif "accessib" in lower:
            impacts.add("ACCESSIBILITY")
        elif "launch" in lower:
            impacts.add("LAUNCH")
        elif lower.endswith(".md"):
            impacts.add("PROTOCOL_ONLY")
    ctx.metadata["change_impact"] = sorted(impacts) or ["NO_UNCOMMITTED_CHANGE_DETECTED"]
    ctx.check("CHANGE_IMPACT_CLASSIFICATION", "structural", True, "changed paths are classified without changing validation policy", file="framework_validation/validator.py", location="change impact", expected="deterministic impact class", observed=ctx.metadata["change_impact"])


def _iter_source_files(root: Path, report_paths: set[str]) -> Iterable[tuple[str, Path]]:
    for directory, dirnames, filenames in os.walk(root):
        directory_path = Path(directory)
        dirnames[:] = [name for name in dirnames if name not in SOURCE_IGNORED_DIRS]
        for filename in filenames:
            path = directory_path / filename
            relative = path.relative_to(root).as_posix()
            if any(relative.startswith(prefix) for prefix in RUNTIME_SOURCE_PREFIXES) or (relative.startswith(REPORT_CERTIFICATION_PREFIX) and relative.endswith("-certification.json")) or relative in report_paths:
                continue
            yield relative, path


def _snapshot_sources(root: Path, report_paths: set[str]) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for relative, path in _iter_source_files(root, report_paths):
        digest = hashlib.sha256()
        try:
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(65536), b""):
                    digest.update(chunk)
        except OSError:
            continue
        snapshot[relative] = digest.hexdigest()
    return snapshot


def _source_mutations(before: Mapping[str, str], after: Mapping[str, str], expected: set[str]) -> list[str]:
    changed = sorted(set(before) | set(after))
    return [path for path in changed if before.get(path) != after.get(path) and path not in expected]


def _filtered_git_status(status: str, expected: set[str]) -> str:
    kept = []
    for line in status.splitlines():
        path = line[3:].strip().strip('"') if len(line) >= 4 else line
        if _posix(path) not in expected:
            kept.append(line)
    return "\n".join(kept)


def _check_mutation_evidence(ctx: ValidationContext, before_status: str, before_sources: Mapping[str, str], expected_paths: set[str]) -> None:
    after_status = _git_status(ctx.root)
    after_sources = _snapshot_sources(ctx.root, expected_paths)
    source_mutations = _source_mutations(before_sources, after_sources, expected_paths)
    status_changed = _filtered_git_status(before_status, expected_paths) != _filtered_git_status(after_status, expected_paths)
    unexpected = sorted(set(source_mutations) | ({"git status"} if status_changed else set()))
    ctx.metadata["mutation_evidence"] = {
        "git_status_before": before_status,
        "git_status_after": after_status,
        "expected_changed_files": sorted(expected_paths),
        "unexpected_changed_files": unexpected,
        "frozen_path_mutations": [],
    }
    ctx.check(
        "MUTATION_EVIDENCE_READ_ONLY",
        "invariants",
        not unexpected,
        "framework validation did not mutate source outside designated report paths",
        file="framework_validation/validator.py",
        location="mutation evidence",
        expected="no unexpected source mutation",
        observed=unexpected,
    )


def _run_negative_controls(ctx: ValidationContext) -> None:
    scenarios: list[tuple[str, str, Callable[[], bool]]] = []
    current_version = str(ctx.metadata.get("framework_version"))
    legacy_versions = set(ctx.metadata.get("legacy_schema_versions", []))
    base_profile = {"schema_version": current_version, "framework_version": current_version, "project_name": "fixture", "locks": {name: False for name in CANONICAL_LOCKS}, "measurement": {"complete": False}}

    def sixth_lock() -> bool:
        bad = json.loads(json.dumps(base_profile))
        bad["locks"]["measurement_locked"] = False
        return "OWNER_LOCK_INVARIANT" in validate_owner_locks(bad)

    def duplicate_state() -> bool:
        bad = {"states": [
            {"path": "measurement.complete", "canonical_concept": "measurement", "status": "ACTIVE", "owner_protocol": "A"},
            {"path": "cro.complete", "canonical_concept": "measurement", "status": "ACTIVE", "owner_protocol": "B"},
        ]}
        return "DUPLICATE_CANONICAL_COMPLETION_FLAG" in validate_state_ownership_registry(bad)

    def broken_template() -> bool:
        return "BROKEN_TEMPLATE_REFERENCE" in validate_template_references(
            ["templates/__synthetic_missing_template__.md"], ctx.root
        )

    def invalid_json() -> bool:
        return "INVALID_JSON_ARTIFACT" in validate_json_content("{ this is not JSON")

    def invalid_schema() -> bool:
        bad = json.loads(json.dumps(base_profile))
        bad["project_name"] = None
        return "CURRENT_PROFILE_FIELD_TYPE" in validate_site_profile(
            bad,
            current=True,
            current_version=str(ctx.metadata.get("framework_version")),
            legacy_versions=ctx.metadata.get("legacy_schema_versions", []),
        )

    def malformed_semver() -> bool:
        return parse_semver("2.11") is None

    def version_drift() -> bool:
        return "VERSION_DOCUMENT_CONSISTENCY" in validate_version_markers(
            "<!-- FRAMEWORK_VERSION: 2.10.0 -->", str(ctx.metadata.get("framework_version"))
        )

    def invalid_transition() -> bool:
        return not validate_transition_path(["NOT_EVALUATED", "STABILIZED"])

    def obsolete_state() -> bool:
        bad = json.loads(json.dumps(base_profile))
        bad["cro"] = {"complete": False}
        return "OBSOLETE_CURRENT_STATE" in [rule for rule, _ in _profile_error_records(bad, True, current_version, legacy_versions)]

    def missing_protocol() -> bool:
        bad = {"protocols": [{"id": "MISSING", "path": "__missing__.md", "status": "ACTIVE", "domain": "fixture", "phase": "0", "state_owner": "fixture"}]}
        return "CANONICAL_PROTOCOL_EXISTS" in validate_protocol_paths(bad, ctx.root)

    def broken_protocol_pointer() -> bool:
        bad = {
            "protocols": [
                {
                    "id": "SUPERSEDED",
                    "path": "__missing__.md",
                    "status": "SUPERSEDED",
                    "domain": "fixture",
                    "phase": "0",
                    "state_owner": "fixture",
                    "superseded_by": "DOES_NOT_EXIST",
                }
            ]
        }
        return "BROKEN_PROTOCOL_COMPATIBILITY_POINTER" in validate_protocol_registry(bad)

    def malformed_registry() -> bool:
        return "PROTOCOL_REGISTRY_SHAPE" in validate_protocol_registry({})

    def unsafe_ci() -> bool:
        safe = "permissions:\n  contents: read\n"
        bad = safe.replace("contents: read", "contents: write")
        return "CI_READ_ONLY_PERMISSIONS" in validate_workflow_text(bad)

    with tempfile.TemporaryDirectory(prefix="website-director-negative-") as temporary:
        temp_root = Path(temporary)
        frozen_file = temp_root / "projects" / "fixture" / "state.json"
        frozen_file.parent.mkdir(parents=True)
        frozen_file.write_text("{}", encoding="utf-8")
        guard_class = _load_guard(ctx.root, str(ctx.manifest.get("frozen_guard_path")))
        if guard_class is None:
            frozen_mutation = lambda: False
        else:
            def frozen_mutation() -> bool:
                # The probe owns its temporary corpus because scenarios are
                # evaluated after the fixture-construction block exits.
                with tempfile.TemporaryDirectory(prefix="website-director-frozen-negative-") as probe_directory:
                    probe_root = Path(probe_directory)
                    probe_file = probe_root / "projects" / "fixture" / "state.json"
                    probe_file.parent.mkdir(parents=True)
                    probe_file.write_text("{}", encoding="utf-8")
                    guard = guard_class(str(probe_root), protected_paths=["projects/"], ledger_path="runtime/violations.log", run_id="negative-control")
                    guard.snapshot()
                    probe_file.write_text('{"mutated": true}', encoding="utf-8")
                    result = guard.verify()
                    return not result.ok and bool(result.mutations)
        scenarios.extend([
            ("sixth_owner_lock", "OWNER_LOCK_INVARIANT", sixth_lock),
            ("duplicate_state_completion_flag", "DUPLICATE_CANONICAL_COMPLETION_FLAG", duplicate_state),
            ("broken_template_reference", "BROKEN_TEMPLATE_REFERENCE", broken_template),
            ("invalid_json", "INVALID_JSON_ARTIFACT", invalid_json),
            ("invalid_schema", "CURRENT_PROFILE_FIELD_TYPE", invalid_schema),
            ("malformed_semver", "CANONICAL_VERSION_SEMVER", malformed_semver),
            ("current_version_drift", "VERSION_DOCUMENT_CONSISTENCY", version_drift),
            ("frozen_fixture_mutation", "FROZEN_FIXTURE_MUTATION", frozen_mutation),
            ("invalid_state_transition", "INVALID_STATE_TRANSITION", invalid_transition),
            ("obsolete_current_state", "OBSOLETE_CURRENT_STATE", obsolete_state),
            ("missing_canonical_protocol", "CANONICAL_PROTOCOL_EXISTS", missing_protocol),
            ("broken_protocol_pointer", "BROKEN_PROTOCOL_COMPATIBILITY_POINTER", broken_protocol_pointer),
            ("malformed_registry", "PROTOCOL_REGISTRY_SHAPE", malformed_registry),
            ("unsafe_ci_permissions", "CI_READ_ONLY_PERMISSIONS", unsafe_ci),
        ])
    results = []
    for name, expected_rule, probe in scenarios:
        try:
            caught = bool(probe())
            error = None
        except Exception as exc:  # noqa: BLE001
            caught = False
            error = str(exc)
        result = {"scenario": name, "expected_rule": expected_rule, "caught": caught}
        if error:
            result["error"] = error
        results.append(result)
        ctx.check(
            "NEGATIVE_CONTROL_PROVEN",
            "negative_controls",
            caught,
            f"negative control {name} deterministically produces a failure signal",
            file="framework_validation/validator.py",
            location=f"negative_controls/{name}",
            expected=expected_rule,
            observed=result,
        )
    ctx.metadata["negative_controls"] = results


def _category_status(checks: Sequence[Check], category: str) -> str:
    relevant = [check.status for check in checks if check.category == category]
    if not relevant:
        return "BLOCKED"
    if "FAIL" in relevant:
        return "FAIL"
    if "BLOCKED" in relevant:
        return "BLOCKED"
    return "PASS"


def _report_status(checks: Sequence[Check]) -> str:
    if any(check.status == "FAIL" for check in checks):
        return "FAIL"
    if any(check.status == "BLOCKED" for check in checks):
        return "BLOCKED"
    return "PASS"


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _build_report(ctx: ValidationContext, identity: Mapping[str, str], divergence: Mapping[str, Any]) -> dict[str, Any]:
    status = _report_status(ctx.checks)
    framework_status = {
        "PASS": "FRAMEWORK_VALIDATION_PASS",
        "FAIL": "FRAMEWORK_VALIDATION_FAIL",
        "BLOCKED": "FRAMEWORK_VALIDATION_BLOCKED",
    }[status]
    category_names = sorted({check.category for check in ctx.checks})
    category_status = {category: _category_status(ctx.checks, category) for category in category_names}
    required_categories = {
        "structural": category_status.get("structural", "BLOCKED"),
        "schema": category_status.get("schema", "BLOCKED"),
        "references": category_status.get("references", "BLOCKED"),
        "invariants": category_status.get("invariants", "BLOCKED"),
        "compatibility": category_status.get("compatibility", "BLOCKED"),
        "versioned_test_suites": category_status.get("versioned_test_suites", "BLOCKED"),
        "frozen_fixture_integrity": category_status.get("frozen_fixture_integrity", "BLOCKED"),
        "negative_controls": category_status.get("negative_controls", "BLOCKED"),
    }
    certification_status = (
        "PASS"
        if all(value == "PASS" for value in required_categories.values())
        else "FAIL"
        if "FAIL" in required_categories.values()
        else "BLOCKED"
        if "BLOCKED" in required_categories.values()
        else "FAIL"
    )
    ctx.check(
        "RELEASE_CERTIFICATION_REQUIREMENTS",
        "release_certification",
        certification_status == "PASS",
        "release certification requires every mandatory framework validation category to pass",
        file="FRAMEWORK-VALIDATION-PROTOCOL.md",
        location="release certification",
        expected={key: "PASS" for key in required_categories},
        observed=required_categories,
        blocked=certification_status == "BLOCKED",
        owner="release-governance",
    )
    status = _report_status(ctx.checks)
    framework_status = {"PASS": "FRAMEWORK_VALIDATION_PASS", "FAIL": "FRAMEWORK_VALIDATION_FAIL", "BLOCKED": "FRAMEWORK_VALIDATION_BLOCKED"}[status]
    return {
        "framework_version": ctx.metadata.get("framework_version", "UNKNOWN"),
        "commit_sha": identity.get("commit_sha", "UNKNOWN"),
        "branch": identity.get("branch", "UNKNOWN"),
        "base_branch": ctx.metadata.get("base_branch", "UNKNOWN"),
        "base_commit": ctx.metadata.get("base_commit", "UNKNOWN"),
        "base_version": ctx.metadata.get("base_version", ctx.metadata.get("previous_version", "UNKNOWN")),
        "development_head": identity.get("commit_sha", "UNKNOWN"),
        "remote_main_head": divergence.get("remote_main_head", "UNAVAILABLE"),
        "divergence_status": divergence.get("status", "UNKNOWN"),
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": status,
        "framework_status": framework_status,
        "checks_total": len(ctx.checks),
        "checks_passed": sum(check.status == "PASS" for check in ctx.checks),
        "checks_failed": sum(check.status == "FAIL" for check in ctx.checks),
        "checks_blocked": sum(check.status == "BLOCKED" for check in ctx.checks),
        "checks_warning": sum(check.status == "WARNING" for check in ctx.checks),
        "checks_info": sum(check.status == "INFO" for check in ctx.checks),
        "checks": [check.as_dict() for check in ctx.checks],
        "findings": [finding.as_dict() for finding in ctx.findings],
        "category_status": category_status,
        "release_certification": {
            "status": certification_status,
            "required_categories": required_categories,
            "artifact_generated_by": "framework_validation.validator",
        },
        "identity": dict(identity),
        "main_divergence": dict(divergence),
        "change_impact": ctx.metadata.get("change_impact", []),
        "suite_runs": ctx.metadata.get("suite_runs", []),
        "negative_controls": ctx.metadata.get("negative_controls", []),
        "historical_profiles_checked": ctx.metadata.get("historical_profiles_checked", 0),
        "frozen_project_count": ctx.metadata.get("frozen_project_count", 0),
        "protected_file_count": ctx.metadata.get("protected_file_count", 0),
        "frozen_registry_entries": ctx.metadata.get("frozen_registry_entries", 0),
        "mutation_evidence": ctx.metadata.get("mutation_evidence", {}),
        "pre_existing_failures": [],
    }


def validate_repository(
    root: str | os.PathLike[str],
    *,
    report_path: Optional[str | os.PathLike[str]] = None,
    certification_path: Optional[str | os.PathLike[str]] = None,
    run_suites: bool = False,
    run_negative_controls: bool = True,
    mutation_probe: Optional[Callable[[Path], None]] = None,
) -> dict[str, Any]:
    """Validate a repository and return the complete machine-readable report.

    ``run_suites`` is opt-in for library callers and enabled by the module CLI.
    The CLI is the release-certification path. ``mutation_probe`` is a
    test-only injection point used to prove mutation evidence catches a source
    change; normal validation never supplies it.
    """

    root_path = Path(root).resolve()
    output_paths: set[str] = set()
    for output in (report_path, certification_path):
        if output is None:
            continue
        output_path = Path(output)
        if not output_path.is_absolute():
            output_path = root_path / output_path
        try:
            output_paths.add(output_path.resolve().relative_to(root_path).as_posix())
        except ValueError:
            output_paths.add(output_path.as_posix())
    ctx = ValidationContext(root_path, report_paths=output_paths)
    before_status = _git_status(root_path)
    before_sources = _snapshot_sources(root_path, output_paths)
    _load_manifest(ctx)
    _check_structure(ctx)
    current_version = _check_versions(ctx)
    _check_governance_docs(ctx, current_version)
    _check_json_artifacts(ctx)
    _check_site_profile_schema(ctx, current_version)
    _check_protocols_gates_phases(ctx)
    _check_state_ownership(ctx)
    _check_template_references(ctx)
    _check_markdown_references(ctx)
    _check_python(ctx)
    _check_ci(ctx)
    _check_frozen_registry(ctx)
    _check_test_registry(ctx, run_suites)
    _check_impact(ctx)
    if run_negative_controls:
        _run_negative_controls(ctx)
    else:
        ctx.check("NEGATIVE_CONTROLS_EXECUTED", "negative_controls", False, "negative controls were not executed", file="framework_validation/validator.py", location="negative controls", expected="synthetic controls run", observed="not run", blocked=True)

    guard = ctx.metadata.get("frozen_guard")
    if guard is not None:
        try:
            integrity = guard.verify()
            detail = integrity.summary()
            ctx.metadata["frozen_integrity"] = {
                "ok": integrity.ok,
                "summary": detail,
                "checked_files": integrity.checked_files,
                "mutations": integrity.mutations,
                "additions": integrity.additions,
                "deletions": integrity.deletions,
                "ledger_path": integrity.ledger_path,
            }
            ctx.check("FROZEN_FIXTURE_INTEGRITY", "frozen_fixture_integrity", integrity.ok, detail, file=str(ctx.manifest.get("frozen_guard_path")), location="verify", expected="protected projects unchanged", observed=ctx.metadata["frozen_integrity"])
            if not integrity.ok:
                ctx.metadata["mutation_evidence"]["frozen_path_mutations"] = integrity.mutations + integrity.additions + integrity.deletions
        except Exception as exc:  # noqa: BLE001
            ctx.check("FROZEN_FIXTURE_INTEGRITY", "frozen_fixture_integrity", False, f"FrozenIntegrityGuard verification failed: {exc}", file=str(ctx.manifest.get("frozen_guard_path")), location="verify", expected="guard verification succeeds", observed=str(exc))
    else:
        ctx.check("FROZEN_FIXTURE_INTEGRITY", "frozen_fixture_integrity", False, "FrozenIntegrityGuard was unavailable for this validation run", file=str(ctx.manifest.get("frozen_guard_path")), location="verify", expected="guard available", observed="unavailable", blocked=ctx.path("projects").is_dir())

    if mutation_probe is not None:
        mutation_probe(root_path)
    _check_mutation_evidence(ctx, before_status, before_sources, output_paths)
    identity = _git_identity(root_path)
    divergence = _git_divergence(root_path, identity["commit_sha"])
    ctx.metadata["main_divergence"] = divergence
    if divergence.get("status") not in {"ALIGNED", "REMOTE_MAIN_UNAVAILABLE"}:
        ctx.check("MAIN_DIVERGENCE_STATUS", "compatibility", False, f"development head and remote main are not aligned: {divergence.get('status')}", file="git refs", location="origin/main", expected="divergence is reported without merge", observed=divergence, severity="WARNING", owner="release-governance")
    else:
        ctx.check("MAIN_DIVERGENCE_STATUS", "compatibility", True, f"main divergence status recorded as {divergence.get('status')}", file="git refs", location="origin/main", observed=divergence)
    report = _build_report(ctx, identity, divergence)

    if report_path is not None:
        report_target = Path(report_path)
        if not report_target.is_absolute():
            report_target = root_path / report_target
        _write_json(report_target, report)
    if certification_path is not None:
        certification_target = Path(certification_path)
        if not certification_target.is_absolute():
            certification_target = root_path / certification_target
        _write_json(certification_target, report)
    return report


def _print_summary(report: Mapping[str, Any], report_path: str, certification_path: str) -> None:
    print("WEBSITE DIRECTOR FRAMEWORK VALIDATION")
    print(f"version: {report.get('framework_version')}")
    print(f"status: {report.get('framework_status')} ({report.get('status')})")
    print(
        "checks: "
        f"{report.get('checks_passed')} passed, "
        f"{report.get('checks_failed')} failed, "
        f"{report.get('checks_blocked')} blocked, "
        f"{report.get('checks_warning')} warnings"
    )
    for finding in report.get("findings", []):
        if finding.get("SEVERITY") == "ERROR":
            print(f"{finding.get('RULE_ID')} [{finding.get('FILE')}:{finding.get('LOCATION')}] {finding.get('MESSAGE')}")
    print(f"report: {report_path}")
    print(f"certification: {certification_path}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Website Director itself")
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--report", default=None, help="runtime report path")
    parser.add_argument("--certification", default=None, help="release certification report path")
    parser.add_argument("--run-suites", action="store_true", help="run active registered framework suites")
    parser.add_argument("--skip-suites", action="store_true", help="skip suite execution and produce a blocked certification")
    parser.add_argument("--skip-negative-controls", action="store_true", help="skip synthetic negative controls")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    version_value, _ = _read_json_file(root / "framework-version.json")
    version = version_value.get("version", "unknown") if isinstance(version_value, dict) else "unknown"
    report_path = args.report or "framework-validation/reports/runtime/framework-validation-report.json"
    certification_path = args.certification or f"framework-validation/reports/{version}-certification.json"
    report = validate_repository(
        root,
        report_path=report_path,
        certification_path=certification_path,
        run_suites=args.run_suites or not args.skip_suites,
        run_negative_controls=not args.skip_negative_controls,
    )
    _print_summary(report, str(report_path), str(certification_path))
    return 0 if report.get("status") == "PASS" else 2 if report.get("status") == "BLOCKED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
