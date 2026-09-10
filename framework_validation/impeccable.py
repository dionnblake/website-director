"""Bounded Website Director design-quality scanning.

This module is the Website Director-owned implementation behind the existing
design_qa_impeccable capability. It is deliberately smaller than the upstream
Impeccable runtime:

* standard library only;
* source-in, findings-out, with no network, subprocess, browser, or writes;
* static findings use the shared Website Director finding fields;
* heuristic findings may be authorized by an explicitly locked design
  direction, but the scanner never changes a lock or applies a repair.

The upstream v4.3.1 engine was audited but not adopted as a provider. The
curated implementation below ports the existing Website Director contract and
the selected v4.3.1 rules listed in IMPECCABLE-ENGINE-PROTOCOL.md.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re
from typing import Any, Iterable, Mapping, Sequence


SOURCE = "IMPECCABLE_DETECTOR"
DETERMINISTIC = "DETERMINISTIC"
HEURISTIC = "HEURISTIC"
ENGINE_DECISION = "CURATED_IMPLEMENTATION_RETAINED"
ENGINE_ADOPTION = "REJECTED"
EXTERNAL_ENGINE_STATUS = "NOT_APPLICABLE"

UPSTREAM_PREVIOUS_VERSION = "skill-v4.1.2"
UPSTREAM_PREVIOUS_SHA = "63b04e2530f5c7b41ea83c133daab24f34912456"
UPSTREAM_TARGET_VERSION = "skill-v4.3.1"
UPSTREAM_TARGET_SHA = "cd12f8660e2dde57b9615c8a6b8ea674101f9cfc"
UPSTREAM_TARGET_RULE_COUNT = 61

# The protocol calls the side-tab and rounded-border variants one contractual
# rule entry while the upstream registry exposes two IDs.
EXISTING_RULE_ENTRIES = (
    "low-contrast",
    "gray-on-color",
    "layout-transition",
    "bounce-easing",
    "dark-glow",
    "touch-target-undersized",
    "ai-color-palette",
    "hero-eyebrow-chip",
    "icon-tile-stack",
    "radial-halo",
    "side-tab / border-accent-on-rounded",
    "pulsing-dot",
    "marquee",
    "shape-assembled-illustration",
    "monotonous-spacing",
    "gradient-text",
    "kicker-above-heading",
    "italic-serif-display",
)

EXISTING_RULE_IDS = (
    "low-contrast",
    "gray-on-color",
    "layout-transition",
    "bounce-easing",
    "dark-glow",
    "touch-target-undersized",
    "ai-color-palette",
    "hero-eyebrow-chip",
    "icon-tile-stack",
    "radial-halo",
    "side-tab",
    "border-accent-on-rounded",
    "pulsing-dot",
    "marquee",
    "shape-assembled-illustration",
    "monotonous-spacing",
    "gradient-text",
    "kicker-above-heading",
    "italic-serif-display",
)

# This is intentionally a curated adoption, not a second upstream registry.
# The full v4.3.1 catalog and the reasons for every non-adopted rule live in
# IMPECCABLE-ENGINE-PROTOCOL.md.
ADOPTED_NEW_RULE_IDS = (
    "flat-type-hierarchy",
    "organic-clip-path",
    "buried-raster",
    "extreme-negative-tracking",
    "broken-image",
    "skipped-heading",
    "justified-text",
    "tiny-text",
    "undersized-ui-text",
    "repeating-stripes-gradient",
)
ADOPTED_NEW_STATIC_RULE_IDS = (
    "extreme-negative-tracking",
    "broken-image",
    "skipped-heading",
    "justified-text",
    "tiny-text",
    "undersized-ui-text",
)
ADOPTED_NEW_HEURISTIC_RULE_IDS = (
    "flat-type-hierarchy",
    "organic-clip-path",
    "buried-raster",
    "repeating-stripes-gradient",
)

ADOPTED_RULE_IDS = EXISTING_RULE_IDS + ADOPTED_NEW_RULE_IDS

RUNTIME_DELEGATED_RULE_IDS = frozenset(
    {
        "script-error",
        "content-hidden-at-rest",
        "edge-flush-cards",
        "text-occlusion",
        "first-viewport-column-overflow",
        "body-text-viewport-edge",
        "text-overflow",
        "clipped-overflow-container",
    }
)

HEURISTIC_RULE_IDS = frozenset(
    {
        "ai-color-palette",
        "hero-eyebrow-chip",
        "icon-tile-stack",
        "radial-halo",
        "side-tab",
        "border-accent-on-rounded",
        "pulsing-dot",
        "marquee",
        "shape-assembled-illustration",
        "monotonous-spacing",
        "gradient-text",
        "kicker-above-heading",
        "italic-serif-display",
        "flat-type-hierarchy",
        "organic-clip-path",
        "buried-raster",
        "repeating-stripes-gradient",
    }
)

VALID_METHODS = frozenset({DETERMINISTIC, HEURISTIC})
VALID_SEVERITIES = frozenset({"CRITICAL", "MAJOR", "MINOR"})
LOCK_NAMES = frozenset(
    {
        "design_direction_locked",
        "information_architecture_locked",
        "content_structure_locked",
        "design_system_locked",
        "motion_direction_locked",
    }
)

_HTML_SUFFIXES = frozenset(
    {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro"}
)
_CSS_SUFFIXES = frozenset(
    {
        ".css",
        ".scss",
        ".sass",
        ".less",
        ".html",
        ".htm",
        ".jsx",
        ".tsx",
        ".vue",
        ".svelte",
        ".astro",
    }
)
_TEXT_SUFFIXES = _HTML_SUFFIXES | _CSS_SUFFIXES | frozenset(
    {".js", ".mjs", ".cjs", ".ts", ".md", ".mdx"}
)
_SKIP_DIRS = frozenset(
    {
        ".git",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        "dist",
        "build",
        "coverage",
    }
)


@dataclass(frozen=True)
class Finding:
    """One normalized static or heuristic finding."""

    finding_id: str
    source: str
    method: str
    rule: str
    location: str
    severity: str
    evidence: str
    remediation: str
    lock_impact: str
    authorized_by_lock: bool = False

    def as_dict(self) -> dict[str, str]:
        """Return the exact nine-field Website Director finding contract."""

        return {
            "FINDING_ID": self.finding_id,
            "SOURCE": self.source,
            "METHOD": self.method,
            "RULE": self.rule,
            "LOCATION": self.location,
            "SEVERITY": self.severity,
            "EVIDENCE": self.evidence,
            "REMEDIATION": self.remediation,
            "LOCK_IMPACT": self.lock_impact,
        }


@dataclass(frozen=True)
class ScanResult:
    """Read-only result of a bounded scan."""

    findings: tuple[Finding, ...]
    files: tuple[str, ...]
    authorized_finding_ids: tuple[str, ...]
    engine_decision: str = ENGINE_DECISION
    external_engine_status: str = EXTERNAL_ENGINE_STATUS

    @property
    def blocking_findings(self) -> tuple[Finding, ...]:
        return tuple(
            finding
            for finding in self.findings
            if not finding.authorized_by_lock
        )

    @property
    def passed(self) -> bool:
        return not self.blocking_findings

    def as_dict(self) -> dict[str, Any]:
        return {
            "engine_decision": self.engine_decision,
            "external_engine_status": self.external_engine_status,
            "files": list(self.files),
            "authorized_finding_ids": list(self.authorized_finding_ids),
            "findings": [finding.as_dict() for finding in self.findings],
            "passed": self.passed,
        }


@dataclass(frozen=True)
class _Context:
    authorized_heuristics: frozenset[str]
    design_direction_locked: bool
    locked_rules: frozenset[str]


@dataclass(frozen=True)
class _RawFinding:
    rule: str
    method: str
    path: str
    line: int
    detail: str
    severity: str
    remediation: str


def _normalize_path(value: str | os.PathLike[str]) -> str:
    text = os.fspath(value).replace("\\", "/")
    while text.startswith("./"):
        text = text[2:]
    return text or "."


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, max(0, offset)) + 1


def _context(value: Mapping[str, Any] | None) -> _Context:
    value = value or {}
    authorized = value.get("authorized_heuristics", ())
    if isinstance(authorized, str):
        authorized = (authorized,)
    authorized_set = frozenset(str(item) for item in authorized)
    locked_rules_value = value.get("locked_rules", ())
    if isinstance(locked_rules_value, Mapping):
        locked_rules_value = locked_rules_value.keys()
    if isinstance(locked_rules_value, str):
        locked_rules_value = (locked_rules_value,)
    return _Context(
        authorized_heuristics=authorized_set,
        design_direction_locked=bool(value.get("design_direction_locked", False)),
        locked_rules=frozenset(str(item) for item in locked_rules_value),
    )


def _css_blocks(text: str) -> Iterable[tuple[str, str, int]]:
    """Yield simple selector/declaration blocks without evaluating CSS."""

    for match in re.finditer(r"(?s)([^{}]+)\{([^{}]*)\}", text):
        selector = " ".join(match.group(1).split())
        if selector.lstrip().startswith("@"):
            continue
        yield selector, match.group(2), match.start()


def _declarations(body: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for match in re.finditer(r"(?is)([-a-z]+)\s*:\s*([^;]+)", body):
        values[match.group(1).lower()] = match.group(2).strip()
    return values


def _parse_color(value: str) -> tuple[int, int, int] | None:
    value = value.strip().lower()
    hex_match = re.search(r"#([0-9a-f]{3,8})\b", value)
    if hex_match:
        raw = hex_match.group(1)
        if len(raw) in {3, 4}:
            raw = "".join(char * 2 for char in raw)
        if len(raw) >= 6:
            return tuple(int(raw[index : index + 2], 16) for index in (0, 2, 4))
    rgb_match = re.search(
        r"rgba?\(\s*([0-9.]+)\s*[, ]\s*([0-9.]+)\s*[, ]\s*([0-9.]+)",
        value,
    )
    if rgb_match:
        return tuple(min(255, int(float(rgb_match.group(index)))) for index in (1, 2, 3))
    return None


def _is_neutral(color: tuple[int, int, int] | None) -> bool:
    return color is not None and max(color) - min(color) <= 3


def _luminance(color: tuple[int, int, int]) -> float:
    channels = []
    for channel in color:
        value = channel / 255
        channels.append(value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def _contrast(first: tuple[int, int, int], second: tuple[int, int, int]) -> float:
    light = max(_luminance(first), _luminance(second))
    dark = min(_luminance(first), _luminance(second))
    return (light + 0.05) / (dark + 0.05)


def _first_value(values: Mapping[str, str], *names: str) -> str | None:
    for name in names:
        if name in values:
            return values[name]
    return None


def _px_or_em(value: str) -> float | None:
    match = re.search(r"(-?\d+(?:\.\d+)?)\s*(px|em|rem)\b", value.lower())
    if not match:
        return None
    number = float(match.group(1))
    unit = match.group(2)
    if unit == "px":
        return number
    return number * 16


def _plain_number(value: str) -> float | None:
    match = re.search(r"^\s*(-?\d+(?:\.\d+)?)\s*(?:;|$)", value)
    return float(match.group(1)) if match else None


def _has_nonzero_radius(value: str) -> bool:
    numbers = re.findall(r"-?\d+(?:\.\d+)?\s*(?:px|em|rem|%)?", value.lower())
    return bool(numbers) and any(
        float(re.search(r"-?\d+(?:\.\d+)?", number).group()) > 0
        for number in numbers
    )


def _gradient_functions(value: str) -> Iterable[str]:
    """Yield balanced gradient function bodies from a CSS value."""

    for match in re.finditer(r"(?i)(?:linear|radial|conic)-gradient\s*\(", value):
        depth = 1
        index = match.end()
        while index < len(value) and depth:
            if value[index] == "(":
                depth += 1
            elif value[index] == ")":
                depth -= 1
            index += 1
        if depth == 0:
            yield value[match.end() : index - 1]


def _alpha(value: str) -> float | None:
    value = value.strip().lower()
    if value.endswith("%"):
        try:
            return float(value[:-1]) / 100
        except ValueError:
            return None
    try:
        return float(value)
    except ValueError:
        return None


def _gradient_has_opaque_wash(value: str) -> bool:
    """Return true only when a pre-raster gradient is provably near-opaque."""

    first_url = re.search(r"(?i)\burl\s*\(", value)
    if not first_url:
        return False
    prefix = value[: first_url.start()]
    for body in _gradient_functions(prefix):
        alphas: list[float] = []
        remainder = body
        for color_function in re.finditer(r"(?is)\b(?:rgb|rgba|hsl|hsla)\s*\(([^)]*)\)", body):
            parts = re.split(r"[,/]", color_function.group(1))
            alphas.append(_alpha(parts[3]) if len(parts) >= 4 else 1.0)
            remainder = remainder.replace(color_function.group(0), " ")
        for hex_match in re.finditer(r"#([0-9a-f]{3,8})\b", remainder, re.IGNORECASE):
            raw = hex_match.group(1)
            if len(raw) == 4:
                alphas.append(int(raw[3] * 2, 16) / 255)
            elif len(raw) == 8:
                alphas.append(int(raw[6:8], 16) / 255)
            else:
                alphas.append(1.0)
        if re.search(r"(?i)\btransparent\b", remainder):
            alphas.append(0.0)
        if re.search(r"(?i)\b(?:white|black|ivory|beige|linen|snow|cream)\b", remainder):
            alphas.append(1.0)
        if alphas and all(alpha is not None and alpha >= 0.9 for alpha in alphas):
            return True
    return False


def _organic_clip(value: str) -> bool:
    path_match = re.search(r"(?is)\bpath\s*\(([^)]*)\)", value)
    if path_match:
        return len(re.findall(r"[CSQTAcsqta]", path_match.group(1))) >= 3
    polygon_match = re.search(r"(?is)\bpolygon\s*\(([^)]*)\)", value)
    if not polygon_match:
        return False
    points = [point.strip() for point in polygon_match.group(1).split(",") if point.strip()]
    if len(points) < 10:
        return False
    off_grid = 0
    for point in points:
        numbers = re.findall(r"-?\d+(?:\.\d+)?", point)
        if any(abs(float(number) - round(float(number) / 25) * 25) > 0.5 for number in numbers):
            off_grid += 1
    return off_grid >= len(points)


def _looks_interactive(selector: str) -> bool:
    return bool(
        re.search(
            r"(?i)(?:^|[,\s>])(?:button|a|input|select|textarea)\b|"
            r"\[role\s*=\s*[\"']?button|\.button\b|\.btn\b",
            selector,
        )
    )


def _looks_status_or_live(selector: str, source_text: str) -> bool:
    return bool(
        re.search(r"(?i)(?:status|alert|success|warning|error|live|progress)", selector)
        or re.search(r"(?i)(?:aria-live|data-live|data-status)", source_text)
    )


def _emit(
    raw: list[_RawFinding],
    rule: str,
    method: str,
    path: str,
    text: str,
    offset: int,
    detail: str,
    severity: str,
    remediation: str,
) -> None:
    raw.append(
        _RawFinding(
            rule=rule,
            method=method,
            path=_normalize_path(path),
            line=_line_number(text, offset),
            detail=detail,
            severity=severity,
            remediation=remediation,
        )
    )


def _build_findings(raw: Sequence[_RawFinding], context: _Context) -> ScanResult:
    findings: list[Finding] = []
    authorized_ids: list[str] = []
    for index, item in enumerate(raw, start=1):
        if item.method not in VALID_METHODS:
            raise ValueError(f"unsupported Impeccable method: {item.method}")
        if item.severity not in VALID_SEVERITIES:
            raise ValueError(f"unsupported Impeccable severity: {item.severity}")
        authorized = (
            item.method == HEURISTIC
            and context.design_direction_locked
            and item.rule in context.authorized_heuristics
        )
        if authorized:
            remediation = (
                "AUTHORIZED_BY_LOCK: retain the approved treatment; no repair "
                "is authorized by this finding."
            )
            lock_impact = "NONE"
        elif item.rule in context.locked_rules:
            remediation = item.remediation
            lock_impact = "LOCKED_CHANGE_REQUIRED"
        else:
            remediation = item.remediation
            lock_impact = "NONE"
        prefix = "HEUR" if item.method == HEURISTIC else "DET"
        finding_id = f"{prefix}-{index:03d}"
        finding = Finding(
            finding_id=finding_id,
            source=SOURCE,
            method=item.method,
            rule=item.rule,
            location=f"{item.path}:{item.line}",
            severity=item.severity,
            evidence=item.detail,
            remediation=remediation,
            lock_impact=lock_impact,
            authorized_by_lock=authorized,
        )
        findings.append(finding)
        if authorized:
            authorized_ids.append(finding_id)
    return ScanResult(
        findings=tuple(findings),
        files=(),
        authorized_finding_ids=tuple(authorized_ids),
    )


def _scan_source(path: str, text: str, context: _Context) -> list[_RawFinding]:
    raw: list[_RawFinding] = []
    lower_path = _normalize_path(path).lower()
    is_html = Path(lower_path).suffix in _HTML_SUFFIXES
    is_css = Path(lower_path).suffix in _CSS_SUFFIXES
    css_blocks = list(_css_blocks(text)) if is_css else []

    if is_css:
        for selector, body, offset in css_blocks:
            values = _declarations(body)
            color_value = _first_value(values, "color")
            background_value = _first_value(values, "background-color", "background")
            color = _parse_color(color_value or "")
            background = _parse_color(background_value or "")
            if color and background:
                threshold = 3.0 if re.search(r"(?i)\b(?:h1|h2|h3|display|hero)\b", selector) else 4.5
                ratio = _contrast(color, background)
                if ratio < threshold:
                    _emit(
                        raw,
                        "low-contrast",
                        DETERMINISTIC,
                        path,
                        text,
                        offset,
                        f"computed contrast {ratio:.2f}:1 is below the {threshold:.1f}:1 threshold for {selector}",
                        "MAJOR",
                        "Increase the foreground/background contrast or use the approved design-system token.",
                    )
            if color and background and _is_neutral(color) and not _is_neutral(background):
                _emit(
                    raw,
                    "gray-on-color",
                    DETERMINISTIC,
                    path,
                    text,
                    offset,
                    f"neutral foreground {color_value} is used on colored surface {background_value}",
                    "MAJOR",
                    "Tint secondary text from the surface hue or use a foreground token with sufficient contrast.",
                )

            transition = _first_value(values, "transition", "transition-property")
            if transition and re.search(
                r"(?i)(?:^|[, ])(?:all|width|height|padding|margin|top|right|bottom|left)\b",
                transition,
            ):
                _emit(
                    raw,
                    "layout-transition",
                    DETERMINISTIC,
                    path,
                    text,
                    offset,
                    f"{selector} declares layout-triggering transition {transition}",
                    "MAJOR",
                    "Animate transform or opacity, or use a layout-specific compositor-safe technique.",
                )

            for easing in re.finditer(r"(?i)cubic-bezier\(([^)]+)\)", body):
                numbers = [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", easing.group(1))]
                if len(numbers) == 4 and (numbers[1] < 0 or numbers[3] > 1):
                    _emit(
                        raw,
                        "bounce-easing",
                        DETERMINISTIC,
                        path,
                        text,
                        offset + easing.start(),
                        f"overshooting cubic-bezier({easing.group(1)}) is not a calm production easing curve",
                        "MAJOR",
                        "Replace the overshooting curve with the locked smooth or mechanical easing token.",
                    )
                    break

            shadow = _first_value(values, "box-shadow", "text-shadow")
            if shadow:
                shadow_color = _parse_color(shadow)
                surface = _parse_color(background_value or "")
                if shadow_color and surface and not _is_neutral(shadow_color) and _luminance(surface) < 0.22:
                    _emit(
                        raw,
                        "dark-glow",
                        DETERMINISTIC,
                        path,
                        text,
                        offset,
                        f"colored shadow {shadow} is attached to a dark surface in {selector}",
                        "MAJOR",
                        "Use a neutral elevation shadow or a material-backed lighting treatment.",
                    )

            if _looks_interactive(selector):
                undersized = []
                for name in ("width", "height", "min-width", "min-height"):
                    parsed = _px_or_em(values.get(name, ""))
                    if parsed is not None and 0 < parsed < 44:
                        undersized.append(f"{name}={values[name]}")
                if undersized:
                    _emit(
                        raw,
                        "touch-target-undersized",
                        DETERMINISTIC,
                        path,
                        text,
                        offset,
                        f"interactive selector {selector} declares {', '.join(undersized)}",
                        "MAJOR",
                        "Provide at least a 44px by 44px declared interactive target on mobile.",
                    )

            if re.search(r"(?i)(?:linear|radial)-gradient", body):
                palette_hits = re.findall(
                    r"(?i)#(?:6366f1|8b5cf6|06b6d4|4f46e5|a855f7|22d3ee)\b",
                    body,
                )
                if len(set(value.lower() for value in palette_hits)) >= 2:
                    _emit(
                        raw,
                        "ai-color-palette",
                        HEURISTIC,
                        path,
                        text,
                        offset,
                        f"uncurated indigo/violet/cyan gradient pairing {', '.join(sorted(set(palette_hits)))}",
                        "MINOR",
                        "Replace the default gradient pairing with an intentional, subject-grounded palette.",
                    )

            if (
                re.search(
                    r"(?i)(?:border-(?:left|right)|border-inline-(?:start|end))\s*:\s*[2-4]px\s+[^;]+"
                    r"|border-(?:left|right)-width\s*:\s*[2-4]px",
                    body,
                )
                and values.get("border-radius")
                and _has_nonzero_radius(values["border-radius"])
                and not _looks_status_or_live(selector, text)
            ):
                _emit(
                    raw,
                    "side-tab",
                    HEURISTIC,
                    path,
                    text,
                    offset,
                    f"colored side accent is attached to rounded selector {selector} without status semantics",
                    "MINOR",
                    "Remove the decorative side stripe or give it a real status/semantic role.",
                )
                _emit(
                    raw,
                    "border-accent-on-rounded",
                    HEURISTIC,
                    path,
                    text,
                    offset,
                    f"accent border and border-radius coexist on {selector} without status semantics",
                    "MINOR",
                    "Remove either the accent border or the radius, unless the component has a documented semantic purpose.",
                )

            animation = _first_value(values, "animation", "animation-name")
            if (
                animation
                and re.search(r"(?i)(?:pulse|ping|blink)", animation)
                and re.search(r"(?i)(?:dot|ping|indicator)", selector)
                and not _looks_status_or_live(selector, text)
            ):
                _emit(
                    raw,
                    "pulsing-dot",
                    HEURISTIC,
                    path,
                    text,
                    offset,
                    f"decorative dot selector {selector} uses animation {animation} without live/status context",
                    "MINOR",
                    "Use a static indicator unless the animation communicates genuinely changing data.",
                )

            if (
                animation
                and re.search(r"(?i)\bmarquee\b", animation)
                and re.search(r"(?i)\binfinite\b", animation)
                and not re.search(
                    r"(?i)(?:marquee[-_](?:pause|control)|data-marquee-purpose\s*=\s*[\"']editorial)",
                    text,
                )
            ):
                _emit(
                    raw,
                    "marquee",
                    HEURISTIC,
                    path,
                    text,
                    offset,
                    f"infinite marquee animation {animation} has no declared pause or editorial purpose",
                    "MINOR",
                    "Add an accessible pause control and editorial purpose, or let visitors move through the content.",
                )

            if (
                re.search(r"(?i)background(?:-image)?\s*:\s*[^;]*(?:linear|radial)-gradient", body)
                and ("background-clip" in values or "-webkit-background-clip" in values)
                and re.search(
                    r"(?i)\btext\b",
                    values.get("background-clip", "") + values.get("-webkit-background-clip", ""),
                )
                and re.search(
                    r"(?i)(?:color\s*:\s*transparent|text-fill-color\s*:\s*transparent)",
                    body,
                )
            ):
                _emit(
                    raw,
                    "gradient-text",
                    HEURISTIC,
                    path,
                    text,
                    offset,
                    f"gradient text treatment on {selector} relies on clipped transparent glyphs",
                    "MINOR",
                    "Use a solid, legible text token unless the gradient has a documented material purpose.",
                )

            clip = values.get("clip-path", "")
            if clip and _organic_clip(clip):
                _emit(
                    raw,
                    "organic-clip-path",
                    HEURISTIC,
                    path,
                    text,
                    offset,
                    f"complex clip-path on {selector} approximates an organic produced edge",
                    "MINOR",
                    "Use a provenance-backed cut-out asset for produced silhouettes; keep clip-path for deliberate geometry.",
                )

            background_image = values.get("background-image", "") or values.get("background", "")
            opacity = values.get("opacity", "")
            opacity_number = _plain_number(opacity) if opacity else None
            blend_mode = values.get("background-blend-mode", "") + values.get("mix-blend-mode", "")
            if (
                "url(" in background_image.lower()
                and _gradient_has_opaque_wash(background_image)
                and not blend_mode.strip().lower().startswith(("multiply", "screen", "overlay", "darken", "lighten"))
            ):
                _emit(
                    raw,
                    "buried-raster",
                    HEURISTIC,
                    path,
                    text,
                    offset,
                    f"raster background on {selector} is covered by a gradient wash",
                    "MINOR",
                    "Let the produced material remain visible, or remove the unused raster asset.",
                )
            elif opacity_number is not None and 0 <= opacity_number <= 0.1 and "url(" in body.lower():
                _emit(
                    raw,
                    "buried-raster",
                    HEURISTIC,
                    path,
                    text,
                    offset,
                    f"raster-bearing selector {selector} is near-zero opacity",
                    "MINOR",
                    "Make the raster materially visible or remove it from the build.",
                )

            letter_spacing = values.get("letter-spacing", "")
            if re.search(r"(?i)\b(?:h1|h2|h3|heading|display|hero)\b", selector) and letter_spacing:
                match = re.search(r"(-?\d+(?:\.\d+)?)\s*(em|px|rem)\b", letter_spacing.lower())
                if match:
                    number = float(match.group(1))
                    em_value = number if match.group(2) == "em" else number / 16
                    if em_value <= -0.08:
                        _emit(
                            raw,
                            "extreme-negative-tracking",
                            DETERMINISTIC,
                            path,
                            text,
                            offset,
                            f"heading selector {selector} declares letter-spacing {letter_spacing}",
                            "MAJOR",
                            "Relax display tracking to preserve character shapes and reading rhythm.",
                        )

            if re.search(r"(?i)text-align\s*:\s*justify\b", body) and not re.search(
                r"(?i)\bauto\b",
                values.get("hyphens", "") + values.get("-webkit-hyphens", ""),
            ):
                _emit(
                    raw,
                    "justified-text",
                    DETERMINISTIC,
                    path,
                    text,
                    offset,
                    f"text-align: justify is declared on {selector} without a hyphenation contract",
                    "MINOR",
                    "Use left-aligned body text or explicitly pair justification with safe hyphenation.",
                )

            font_size = _px_or_em(values.get("font-size", ""))
            if font_size is not None and font_size < 12 and not re.search(
                r"(?i)(?:legal|fine[-_ ]?print|copyright|disclaimer)",
                selector,
            ):
                if _looks_interactive(selector):
                    if font_size < 11:
                        _emit(
                            raw,
                            "undersized-ui-text",
                            DETERMINISTIC,
                            path,
                            text,
                            offset,
                            f"interactive selector {selector} declares {values.get('font-size')}",
                            "MINOR",
                            "Use at least 11px for functional UI text; reserve smaller text for non-functional legal copy.",
                        )
                elif re.search(r"(?i)\b(?:body|p|article|content|copy)\b", selector):
                    _emit(
                        raw,
                        "tiny-text",
                        DETERMINISTIC,
                        path,
                        text,
                        offset,
                        f"body/content selector {selector} declares {values.get('font-size')}",
                        "MINOR",
                        "Use at least 12px for body text, with 14-16px preferred for readable content.",
                    )

            if "repeating-linear-gradient" in body.lower() or "repeating-radial-gradient" in body.lower():
                _emit(
                    raw,
                    "repeating-stripes-gradient",
                    HEURISTIC,
                    path,
                    text,
                    offset,
                    f"repeating gradient on {selector} creates a stripe texture without an explicit material rationale",
                    "MINOR",
                    "Use a provenance-backed texture or document the material purpose of the repeating pattern.",
                )

        section_values: list[tuple[str, int]] = []
        role_sizes: dict[str, list[tuple[float, int]]] = {}
        shape_count = 0
        for selector, body, offset in css_blocks:
            values = _declarations(body)
            if re.search(r"(?i)(?:^|[,\s>])(?:section|\.section)\b", selector):
                spacing = values.get("padding") or values.get("padding-block") or values.get("margin")
                if spacing:
                    section_values.append((spacing.strip(), offset))
            if re.search(r"(?i)\b(?:h1|h2|h3|p|body)\b", selector):
                size = _px_or_em(values.get("font-size", ""))
                if size is not None:
                    for role in re.findall(r"(?i)\b(?:h1|h2|h3|p|body)\b", selector):
                        role_sizes.setdefault(role.lower(), []).append((size, offset))
            if re.search(r"(?i)\.(?:shape|decor|blob)[-\w]*\b", selector):
                if re.search(r"(?i)(?:position\s*:\s*absolute|border-radius\s*:\s*50%)", body):
                    shape_count += 1
        if len(section_values) >= 4:
            values = {value for value, _ in section_values}
            if len(values) == 1:
                _emit(
                    raw,
                    "monotonous-spacing",
                    HEURISTIC,
                    path,
                    text,
                    section_values[0][1],
                    f"{len(section_values)} section rules reuse the same macro spacing value {section_values[0][0]}",
                    "MINOR",
                    "Create meaningful macro/micro spacing contrast between related groups and section boundaries.",
                )
        unique_role_sizes = [entries[0] for entries in role_sizes.values() if entries]
        if len(unique_role_sizes) >= 3:
            sizes = [size for size, _ in unique_role_sizes]
            if min(sizes) > 0 and max(sizes) / min(sizes) < 1.25:
                _emit(
                    raw,
                    "flat-type-hierarchy",
                    HEURISTIC,
                    path,
                    text,
                    unique_role_sizes[0][1],
                    f"heading/body sizes {sorted(round(size, 2) for size in sizes)}px have less than a 1.25x hierarchy step",
                    "MINOR",
                    "Increase at least one meaningful type-scale step while preserving the approved design direction.",
                )
        if shape_count >= 3:
            _emit(
                raw,
                "shape-assembled-illustration",
                HEURISTIC,
                path,
                text,
                0,
                f"{shape_count} absolute decorative shape blocks assemble a scene from primitives",
                "MINOR",
                "Replace decorative filler with a subject-grounded graphic, photograph, or deliberate empty space.",
            )
        if re.search(r"(?i)radial-gradient\([^)]*transparent", text) and re.search(
            r"(?i)(?:blur\s*\(|filter\s*:\s*blur|background(?:-image)?\s*:)",
            text,
        ) and not re.search(r"(?i)data-(?:material|lighting-purpose)\s*=", text):
            _emit(
                raw,
                "radial-halo",
                HEURISTIC,
                path,
                text,
                max(0, text.lower().find("radial-gradient")),
                "decorative radial gradient fades into transparency without a material or spatial purpose",
                "MINOR",
                "Remove the floating haze or ground the lighting in a documented material treatment.",
            )

    if is_html:
        for image in re.finditer(r"(?is)<img\b[^>]*>", text):
            tag = image.group(0)
            src = re.search(r"(?is)\bsrc\s*=\s*[\"']([^\"']*)[\"']", tag)
            value = src.group(1).strip() if src else ""
            if not value or value in {"#", "/", "about:blank"} or re.search(
                r"(?i)placeholder|coming[-_ ]?soon|image[-_ ]?placeholder",
                value,
            ):
                _emit(
                    raw,
                    "broken-image",
                    DETERMINISTIC,
                    path,
                    text,
                    image.start(),
                    f"img tag has missing, empty, or placeholder src {value or '<missing>'}",
                    "MAJOR",
                    "Provide a real asset with provenance, generate the asset, or remove the image element.",
                )

        heading_levels = []
        for heading in re.finditer(r"(?is)<h([1-6])\b[^>]*>", text):
            heading_levels.append((int(heading.group(1)), heading.start()))
        for (previous, _), (current, offset) in zip(heading_levels, heading_levels[1:]):
            if current > previous + 1:
                _emit(
                    raw,
                    "skipped-heading",
                    DETERMINISTIC,
                    path,
                    text,
                    offset,
                    f"heading hierarchy jumps from h{previous} to h{current}",
                    "MAJOR",
                    "Restore sequential heading levels so assistive technology can navigate the outline.",
                )
                break

        eyebrow_pattern = re.compile(
            r"(?is)<(?:span|p|div|label)\b[^>]*(?:class|data-role)\s*=\s*[\"'][^\"']*"
            r"(?:eyebrow|chip|badge|kicker)[^\"']*[\"'][^>]*>.*?</(?:span|p|div|label)>"
            r"\s*(?:<!--.*?-->\s*)*<h1\b"
        )
        eyebrow = eyebrow_pattern.search(text)
        if eyebrow:
            _emit(
                raw,
                "hero-eyebrow-chip",
                HEURISTIC,
                path,
                text,
                eyebrow.start(),
                "small eyebrow/chip content is stacked immediately before the hero h1",
                "MINOR",
                "Integrate the label into the hierarchy or document its subject-specific navigation purpose.",
            )

        icon_tiles = re.findall(
            r"(?is)<[^>]+\bclass\s*=\s*[\"'][^\"']*(?:icon-tile|icon-badge|feature-icon)[^\"']*[\"']",
            text,
        )
        if len(icon_tiles) >= 3:
            _emit(
                raw,
                "icon-tile-stack",
                HEURISTIC,
                path,
                text,
                max(0, text.lower().find("icon")),
                f"{len(icon_tiles)} repeated icon tile/badge containers form a feature-card loop",
                "MINOR",
                "Let icons sit in flow or vary the composition instead of repeating the universal feature-card template.",
            )

        kicker_count = len(
            re.findall(
                r"(?is)<(?:span|p|div|label)\b[^>]*(?:class|data-role)\s*=\s*[\"'][^\"']*"
                r"(?:kicker|eyebrow|section-label)[^\"']*[\"'][^>]*>",
                text,
            )
        )
        heading_count = len(re.findall(r"(?is)<h[2-6]\b", text))
        if kicker_count >= 2 and heading_count >= 2:
            _emit(
                raw,
                "kicker-above-heading",
                HEURISTIC,
                path,
                text,
                max(0, text.lower().find("kicker")),
                f"{kicker_count} mechanical kicker/eyebrow labels accompany {heading_count} section headings",
                "MINOR",
                "Remove repeated scaffolding or earn the label through a specific content/navigation role.",
            )

        single_word_italic = re.search(
            r"(?is)<h[1-3]\b[^>]*>[^<]*<em\b[^>]*>\s*[A-Za-z][A-Za-z-]*\s*</em>",
            text,
        )
        if single_word_italic:
            _emit(
                raw,
                "italic-serif-display",
                HEURISTIC,
                path,
                text,
                single_word_italic.start(),
                "a single italicized word is used as a display accent inside a heading",
                "MINOR",
                "Use the approved typographic register or justify the editorial/heritage treatment in the locked direction.",
            )

    return raw


def scan_sources(
    sources: Mapping[str, str],
    context: Mapping[str, Any] | None = None,
) -> ScanResult:
    """Scan an explicit source mapping without filesystem or network effects."""

    normalized_sources: dict[str, str] = {}
    for path, text in sources.items():
        if not isinstance(text, str):
            raise TypeError(f"source {path!r} must be text")
        normalized = _normalize_path(path)
        if normalized in normalized_sources:
            raise ValueError(f"duplicate source path after normalization: {normalized}")
        normalized_sources[normalized] = text

    scan_context = _context(context)
    raw: list[_RawFinding] = []
    for path in sorted(normalized_sources):
        raw.extend(_scan_source(path, normalized_sources[path], scan_context))
    result = _build_findings(raw, scan_context)
    return ScanResult(
        findings=result.findings,
        files=tuple(sorted(normalized_sources)),
        authorized_finding_ids=result.authorized_finding_ids,
        engine_decision=result.engine_decision,
        external_engine_status=result.external_engine_status,
    )


def _iter_source_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root
        return
    for candidate in sorted(root.rglob("*")):
        if not candidate.is_file():
            continue
        if any(part in _SKIP_DIRS for part in candidate.parts):
            continue
        if candidate.suffix.lower() in _TEXT_SUFFIXES:
            yield candidate


def scan_path(
    root: str | os.PathLike[str],
    context: Mapping[str, Any] | None = None,
) -> ScanResult:
    """Read source files below root and run the same pure source scanner."""

    root_path = Path(root)
    if not root_path.exists():
        raise FileNotFoundError(os.fspath(root))
    files: dict[str, str] = {}
    base = root_path if root_path.is_dir() else root_path.parent
    for candidate in _iter_source_files(root_path):
        relative = _normalize_path(candidate.relative_to(base))
        files[relative] = candidate.read_text(encoding="utf-8", errors="replace")
    return scan_sources(files, context=context)


def assess_official_engine_artifact(
    artifact: str | os.PathLike[str] | None,
    expected_sha256: str,
    expected_version: str = UPSTREAM_TARGET_VERSION,
) -> dict[str, str]:
    """Fail closed for an attempted official-engine handoff.

    Website Director does not call this function during normal scans. It is a
    narrow audit helper for future owner-approved adapter work: missing,
    corrupt, or unverified artifacts never become a passing provider.
    """

    if expected_version != UPSTREAM_TARGET_VERSION:
        return {
            "status": "BLOCKED",
            "reason": "official engine version is not the audited v4.3.1 target",
        }
    if not artifact:
        return {
            "status": "BLOCKED",
            "reason": "official engine artifact is unavailable",
        }
    path = Path(artifact)
    if not path.is_file():
        return {
            "status": "BLOCKED",
            "reason": "official engine artifact path is not a file",
        }
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest.lower() != expected_sha256.lower():
        return {
            "status": "BLOCKED",
            "reason": f"official engine artifact checksum mismatch: {digest}",
        }
    return {
        "status": "IDENTITY_VERIFIED_NOT_EXECUTED",
        "reason": "artifact identity is verified; no external engine execution is authorized by this module",
    }


__all__ = [
    "ADOPTED_NEW_RULE_IDS",
    "ADOPTED_NEW_HEURISTIC_RULE_IDS",
    "ADOPTED_NEW_STATIC_RULE_IDS",
    "ADOPTED_RULE_IDS",
    "ENGINE_DECISION",
    "ENGINE_ADOPTION",
    "EXISTING_RULE_ENTRIES",
    "EXISTING_RULE_IDS",
    "Finding",
    "RUNTIME_DELEGATED_RULE_IDS",
    "ScanResult",
    "UPSTREAM_PREVIOUS_SHA",
    "UPSTREAM_PREVIOUS_VERSION",
    "UPSTREAM_TARGET_RULE_COUNT",
    "UPSTREAM_TARGET_SHA",
    "UPSTREAM_TARGET_VERSION",
    "assess_official_engine_artifact",
    "scan_path",
    "scan_sources",
]
