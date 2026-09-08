"""Derive clean-room morphology from complete browser layout evidence.

The evaluator compares normalized measurements before assigning reporting
labels. Missing measurements never imply similarity or divergence, and the
evaluation stage controls which vector families enter the denominator.
"""

from __future__ import annotations

from math import ceil, isfinite
from statistics import mean, median
from typing import Any, Dict, Mapping, Sequence


MORPHOLOGY_VECTOR_IDS = (
    "HERO_SILHOUETTE",
    "SECTION_GEOMETRY",
    "TWO_COLUMN_REPETITION",
    "CARD_CONTAINER_DENSITY",
    "MEDIA_DOMINANCE",
    "TYPOGRAPHIC_SILHOUETTE",
    "WHITESPACE_DENSITY",
    "PAGE_RHYTHM",
    "SIGNATURE_DEVICE",
    "CTA_MORPHOLOGY",
)

HERO_PLUS_SIGNATURE_DEVICE_ONLY = "HERO_PLUS_SIGNATURE_DEVICE_ONLY"
CHEAP_CONCEPT_VECTOR_IDS = (
    "HERO_SILHOUETTE",
    "CARD_CONTAINER_DENSITY",
    "MEDIA_DOMINANCE",
    "TYPOGRAPHIC_SILHOUETTE",
    "WHITESPACE_DENSITY",
    "SIGNATURE_DEVICE",
    "CTA_MORPHOLOGY",
)
CHEAP_CONCEPT_NOT_APPLICABLE_VECTOR_IDS = tuple(
    vector for vector in MORPHOLOGY_VECTOR_IDS if vector not in CHEAP_CONCEPT_VECTOR_IDS
)
SUBSTANTIAL_DIVERGENCE_RATIO = 0.60

_VECTOR_DISTANCE_THRESHOLDS = {
    "HERO_SILHOUETTE": 0.20,
    "SECTION_GEOMETRY": 0.20,
    "TWO_COLUMN_REPETITION": 0.25,
    "CARD_CONTAINER_DENSITY": 0.15,
    "MEDIA_DOMINANCE": 0.20,
    "TYPOGRAPHIC_SILHOUETTE": 0.20,
    "WHITESPACE_DENSITY": 0.18,
    "PAGE_RHYTHM": 0.20,
    "SIGNATURE_DEVICE": 0.20,
    "CTA_MORPHOLOGY": 0.18,
}


def _number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if isfinite(result) else None


def _records(value: Any) -> list[Mapping[str, Any]]:
    return [item for item in value if isinstance(item, Mapping)] if isinstance(value, list) else []


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _positive(mapping: Mapping[str, Any], key: str) -> float | None:
    value = _number(mapping.get(key))
    return value if value is not None and value > 0 else None


def _ratio(value: float | None, denominator: float | None) -> float | None:
    if value is None or denominator is None or denominator <= 0:
        return None
    return value / denominator


def _valid_rect(value: Any) -> bool:
    rect = _mapping(value)
    return (
        _number(rect.get("x")) is not None
        and _number(rect.get("y")) is not None
        and _positive(rect, "width") is not None
        and _positive(rect, "height") is not None
    )


def _rect_union_area(rectangles: Sequence[Mapping[str, Any]], width: float, height: float) -> float:
    """Return clipped union area so nested or overlapping boxes count once."""

    clipped: list[tuple[float, float, float, float]] = []
    for rectangle in rectangles:
        x = _number(rectangle.get("doc_x"))
        y = _number(rectangle.get("doc_y"))
        if x is None:
            x = _number(rectangle.get("x"))
        if y is None:
            y = _number(rectangle.get("y"))
        rect_width = _positive(rectangle, "width")
        rect_height = _positive(rectangle, "height")
        if x is None or y is None or rect_width is None or rect_height is None:
            continue
        left, top = max(0.0, x), max(0.0, y)
        right, bottom = min(width, x + rect_width), min(height, y + rect_height)
        if right > left and bottom > top:
            clipped.append((left, top, right, bottom))
    if not clipped:
        return 0.0

    xs = sorted({coordinate for rectangle in clipped for coordinate in (rectangle[0], rectangle[2])})
    area = 0.0
    for left, right in zip(xs, xs[1:]):
        if right <= left:
            continue
        intervals = sorted(
            (top, bottom)
            for rect_left, top, rect_right, bottom in clipped
            if rect_left < right and rect_right > left
        )
        covered_height = 0.0
        if intervals:
            current_top, current_bottom = intervals[0]
            for top, bottom in intervals[1:]:
                if top <= current_bottom:
                    current_bottom = max(current_bottom, bottom)
                else:
                    covered_height += current_bottom - current_top
                    current_top, current_bottom = top, bottom
            covered_height += current_bottom - current_top
        area += (right - left) * covered_height
    return area


def _font_family_bucket(value: Any) -> str | None:
    family = str(value or "").strip().lower()
    if not family:
        return None
    if any(token in family for token in ("mono", "courier", "consolas", "menlo", "monaco")):
        return "MONO"
    # ``sans-serif`` contains ``serif``; classify explicit sans families first.
    if any(token in family for token in ("sans-serif", "arial", "helvetica", "verdana", "tahoma", "system-ui")):
        return "SANS"
    if any(token in family for token in ("serif", "georgia", "times", "garamond", "baskerville")):
        return "SERIF"
    return "DISPLAY_OR_UNCLASSIFIED"


def _stage(value: Any) -> str:
    token = str(value or "FULL_HOMEPAGE").strip().upper().replace("-", "_")
    return HERO_PLUS_SIGNATURE_DEVICE_ONLY if token in {
        HERO_PLUS_SIGNATURE_DEVICE_ONLY,
        "CHEAP_CONCEPT",
        "CHEAP_CONCEPT_GATE",
        "DESKTOP_HERO_PLUS_SIGNATURE_DEVICE",
    } else "FULL_HOMEPAGE"


def applicable_vectors(evaluation_stage: Any) -> tuple[str, ...]:
    """Return the vector denominator allowed for the rendered surface stage."""

    return CHEAP_CONCEPT_VECTOR_IDS if _stage(evaluation_stage) == HERO_PLUS_SIGNATURE_DEVICE_ONLY else MORPHOLOGY_VECTOR_IDS


def _relative_distance(candidate: float, baseline: float) -> float:
    # Most geometry ratios already live on a 0..1 scale. Keep that unit scale
    # at the zero boundary so browser rounding noise cannot become maximum
    # divergence; values above one retain proportional comparison.
    scale = max(abs(candidate), abs(baseline), 1.0)
    return min(1.0, abs(candidate - baseline) / scale)


def _measurement_distance(
    candidate: Mapping[str, Any],
    baseline: Mapping[str, Any],
    *,
    categorical: Sequence[str] = (),
) -> float | None:
    distances: list[float] = []
    categorical_keys = set(categorical)
    keys = set(candidate) | set(baseline)
    for key in sorted(keys):
        left, right = candidate.get(key), baseline.get(key)
        if left is None or right is None:
            return None
        if key in categorical_keys:
            distances.append(0.0 if left == right else 1.0)
            continue
        left_number, right_number = _number(left), _number(right)
        if left_number is None or right_number is None:
            return None
        distances.append(_relative_distance(left_number, right_number))
    return round(mean(distances), 6) if distances else None


def _layout_axis(children: list[Mapping[str, Any]]) -> str | None:
    if not children:
        return None
    if len(children) == 1:
        return "SINGLE"
    xs = [_number(item.get("x")) for item in children]
    ys = [_number(item.get("y")) for item in children]
    if any(value is None for value in (*xs, *ys)):
        return None
    x_spread = max(xs) - min(xs)  # type: ignore[arg-type]
    y_spread = max(ys) - min(ys)  # type: ignore[arg-type]
    return "HORIZONTAL" if x_spread > y_spread else "VERTICAL"


def _hero_vector(evidence: Mapping[str, Any]) -> tuple[Dict[str, Any] | None, str | None]:
    viewport, hero = _mapping(evidence.get("viewport")), _mapping(evidence.get("hero"))
    width, height = _positive(viewport, "width"), _positive(viewport, "height")
    hero_width, hero_height = _positive(hero, "width"), _positive(hero, "height")
    children = _records(hero.get("major_children"))
    if not all((width, height, hero_width, hero_height)) or not children or not all(_valid_rect(item) for item in children):
        return None, None
    child_areas = [_positive(item, "width") * _positive(item, "height") for item in children]  # type: ignore[operator]
    raw = {
        "x_ratio": _ratio(_number(hero.get("x")), width),
        "y_ratio": _ratio(_number(hero.get("y")), height),
        "width_ratio": _ratio(hero_width, width),
        "height_ratio": _ratio(hero_height, height),
        "aspect_ratio": _ratio(hero_width, hero_height),
        "major_child_count": float(len(children)),
        "dominant_child_area_ratio": max(child_areas) / max(1.0, hero_width * hero_height),
        "layout_axis": _layout_axis(children),
    }
    if any(value is None for value in raw.values()):
        return None, None
    label = "FULL_BLEED_ASYMMETRIC" if raw["width_ratio"] >= 0.9 and raw["height_ratio"] >= 0.55 else (
        "SPLIT_HERO" if raw["layout_axis"] == "HORIZONTAL" and len(children) >= 2 else "COMPACT_HERO"
    )
    return raw, label


def _section_vector(evidence: Mapping[str, Any]) -> tuple[Dict[str, Any] | None, str | None]:
    viewport, document = _mapping(evidence.get("viewport")), _mapping(evidence.get("document"))
    sections = _records(evidence.get("sections"))
    vw, dh = _positive(viewport, "width"), _positive(document, "height")
    if len(sections) < 3 or not vw or not dh:
        return None, None
    widths = [_positive(item, "width") for item in sections]
    heights = [_positive(item, "height") for item in sections]
    child_counts = [_number(item.get("major_child_count")) for item in sections]
    if any(value is None for value in (*widths, *heights, *child_counts)):
        return None, None
    raw = {
        "surface_count": float(len(sections)),
        "mean_width_ratio": mean(widths) / vw,  # type: ignore[arg-type]
        "mean_height_ratio": mean(heights) / dh,  # type: ignore[arg-type]
        "mean_major_child_count": mean(child_counts),  # type: ignore[arg-type]
        "grid_surface_ratio": sum(str(item.get("display", "")).lower() == "grid" for item in sections) / len(sections),
    }
    label = "REPEATED_GRID_SURFACES" if raw["grid_surface_ratio"] >= 0.6 else "OPEN_NARRATIVE_SURFACES"
    return raw, label


def _two_column_vector(evidence: Mapping[str, Any]) -> tuple[Dict[str, Any] | None, str | None]:
    sections = _records(evidence.get("sections"))
    if len(sections) < 3:
        return None, None
    counts = [_number(item.get("column_count")) for item in sections]
    if any(value is None for value in counts):
        return None, None
    two_column = [item for item, count in zip(sections, counts) if count is not None and count >= 2]
    alignments = [str(item.get("column_alignment", "")) for item in two_column]
    if any(not value for value in alignments):
        return None, None
    changes = sum(left != right for left, right in zip(alignments, alignments[1:]))
    raw = {
        "two_column_surface_ratio": len(two_column) / len(sections),
        "alternation_ratio": changes / max(1, len(alignments) - 1),
    }
    return raw, "REPEATED_ALTERNATING_COLUMNS" if all(value >= 0.6 for value in raw.values()) else "NON_REPEATING_COLUMNS"


def _card_vector(evidence: Mapping[str, Any]) -> tuple[Dict[str, Any] | None, str | None]:
    sections = _records(evidence.get("sections"))
    containers = _records(evidence.get("bordered_containers"))
    document, viewport = _mapping(evidence.get("document")), _mapping(evidence.get("viewport"))
    scan = _mapping(evidence.get("scan_complete"))
    doc_width, doc_height = _positive(document, "width"), _positive(document, "height")
    doc_area, viewport_area = _positive(document, "area"), _positive(viewport, "area")
    if not sections or not doc_width or not doc_height or not doc_area or not viewport_area or scan.get("bordered_containers") is not True:
        return None, None
    if not all(_valid_rect(item) for item in containers):
        return None, None
    union_area = _rect_union_area(containers, doc_width, doc_height)
    raw = {
        "bordered_containers_per_surface": len(containers) / len(sections),
        "bordered_container_area_ratio": min(1.0, union_area / doc_area),
        "bordered_containers_per_viewport_area": len(containers) / max(1.0, doc_area / viewport_area),
    }
    density = raw["bordered_containers_per_surface"]
    label = "OPEN_FIELD" if density < 0.5 else ("MODERATE_CONTAINMENT" if density < 1.5 else "HIGH_CONTAINMENT")
    return raw, label


def _media_vector(evidence: Mapping[str, Any]) -> tuple[Dict[str, Any] | None, str | None]:
    media = _records(evidence.get("media_elements"))
    scan = _mapping(evidence.get("scan_complete"))
    document, hero, signature = _mapping(evidence.get("document")), _mapping(evidence.get("hero")), _mapping(evidence.get("signature_device"))
    doc_width, doc_height = _positive(document, "width"), _positive(document, "height")
    doc_area = _positive(document, "area")
    hero_area = (_positive(hero, "width") or 0) * (_positive(hero, "height") or 0)
    if not doc_width or not doc_height or not doc_area or hero_area <= 0 or scan.get("media") is not True:
        return None, None
    if not all(_valid_rect(item) for item in media):
        return None, None
    total = _rect_union_area(media, doc_width, doc_height)
    hero_media = _number(hero.get("media_area"))
    signature_media = _number(signature.get("media_area")) if signature.get("target_found") is True else 0.0
    if hero_media is None or signature_media is None:
        return None, None
    signature_area = (_positive(signature, "width") or 0) * (_positive(signature, "height") or 0)
    raw = {
        "document_media_area_ratio": min(1.0, total / doc_area),
        "hero_media_area_ratio": min(1.0, hero_media / hero_area),
        "signature_media_area_ratio": min(1.0, signature_media / max(1.0, signature_area)) if signature.get("target_found") is True else 0.0,
    }
    ratio = raw["document_media_area_ratio"]
    label = "NO_MEDIA" if ratio == 0 else ("SPARSE_MEDIA" if ratio < 0.04 else ("LIGHT_MEDIA" if ratio < 0.12 else ("SUBSTANTIAL_MEDIA" if ratio < 0.30 else "DOMINANT_MEDIA")))
    return raw, label


def _typography_vector(evidence: Mapping[str, Any]) -> tuple[Dict[str, Any] | None, str | None]:
    heading, viewport = _mapping(evidence.get("heading")), _mapping(evidence.get("viewport"))
    vw, vh = _positive(viewport, "width"), _positive(viewport, "height")
    rect = _mapping(heading.get("rect"))
    family_class = _font_family_bucket(heading.get("font_family"))
    font_size, line_height = _positive(heading, "font_size"), _positive(heading, "line_height")
    heading_width, heading_height = _positive(rect, "width"), _positive(rect, "height")
    line_count, letter_spacing = _positive(heading, "line_count"), _number(heading.get("letter_spacing"))
    if not _valid_rect(rect) or not all((vw, vh, family_class, font_size, line_height, heading_width, heading_height, line_count)) or letter_spacing is None:
        return None, None
    raw = {
        "family_class": family_class,
        "font_size_viewport_height_ratio": font_size / vh,
        "line_height_font_size_ratio": line_height / font_size,
        "heading_width_viewport_ratio": heading_width / vw,
        "heading_height_viewport_ratio": heading_height / vh,
        "line_count": line_count,
        "letter_spacing_em": letter_spacing / font_size,
    }
    scale = "DISPLAY" if raw["font_size_viewport_height_ratio"] >= 0.07 else "TEXTUAL"
    return raw, f"{family_class}_{scale}"


def _whitespace_vector(evidence: Mapping[str, Any]) -> tuple[Dict[str, Any] | None, str | None]:
    whitespace = _mapping(evidence.get("whitespace"))
    keys = ("occupied_area_ratio", "negative_space_ratio", "hero_occupied_area_ratio", "major_region_gap_ratio")
    raw = {key: _number(whitespace.get(key)) for key in keys}
    if any(value is None for value in raw.values()):
        return None, None
    negative = raw["negative_space_ratio"]
    label = "EXPANSIVE" if negative >= 0.62 else ("BALANCED" if negative >= 0.38 else "DENSE")
    return raw, label


def _rhythm_vector(evidence: Mapping[str, Any]) -> tuple[Dict[str, Any] | None, str | None]:
    sections = _records(evidence.get("sections"))
    viewport = _mapping(evidence.get("viewport"))
    vh = _positive(viewport, "height")
    if len(sections) < 3 or not vh:
        return None, None
    heights = [_positive(item, "height") for item in sections]
    gaps = [_number(item.get("gap_before")) for item in sections[1:]]
    if any(value is None for value in (*heights, *gaps)):
        return None, None
    height_mean = mean(heights)  # type: ignore[arg-type]
    gap_mean = mean(gaps) if gaps else 0.0  # type: ignore[arg-type]
    raw = {
        "median_surface_height_viewport_ratio": median(heights) / vh,  # type: ignore[arg-type]
        "height_variation_ratio": (max(heights) - min(heights)) / max(1.0, height_mean),  # type: ignore[arg-type]
        "median_gap_viewport_ratio": median(gaps) / vh if gaps else 0.0,  # type: ignore[arg-type]
        "gap_variation_ratio": (max(gaps) - min(gaps)) / max(1.0, gap_mean) if gaps and gap_mean else 0.0,  # type: ignore[arg-type]
    }
    label = "REGULAR_CADENCE" if raw["height_variation_ratio"] < 0.2 and raw["gap_variation_ratio"] < 0.2 else "IRREGULAR_CADENCE"
    return raw, label


def _signature_vector(evidence: Mapping[str, Any]) -> tuple[Dict[str, Any] | None, str | None]:
    signature, viewport = _mapping(evidence.get("signature_device")), _mapping(evidence.get("viewport"))
    if signature.get("target_found") is not True:
        return None, None
    dominant_child = _mapping(signature.get("dominant_child"))
    vw, vh = _positive(viewport, "width"), _positive(viewport, "height")
    width, height = _positive(signature, "width"), _positive(signature, "height")
    occupancy, dominant_aspect = _number(signature.get("occupied_area_ratio")), _positive(signature, "dominant_child_aspect_ratio")
    orientation = str(signature.get("structural_orientation") or "")
    if not _valid_rect(signature) or not _valid_rect(dominant_child) or not all((vw, vh, width, height, dominant_aspect, orientation)) or occupancy is None:
        return None, None
    raw = {
        "width_viewport_ratio": width / vw,
        "height_viewport_ratio": height / vh,
        "aspect_ratio": width / height,
        "occupied_area_ratio": occupancy,
        "dominant_child_aspect_ratio": dominant_aspect,
        "structural_orientation": orientation,
    }
    aspect = raw["aspect_ratio"]
    shape = "ROUND_OR_SQUARE" if 0.85 <= aspect <= 1.15 else ("LINEAR_HORIZONTAL" if aspect > 1.15 else "LINEAR_VERTICAL")
    return raw, f"{shape}_{orientation}"


def _cta_vector(evidence: Mapping[str, Any]) -> tuple[Dict[str, Any] | None, str | None]:
    cta, viewport, hero = _mapping(evidence.get("cta")), _mapping(evidence.get("viewport")), _mapping(evidence.get("hero"))
    if cta.get("target_found") is not True:
        return None, None
    vw, vh = _positive(viewport, "width"), _positive(viewport, "height")
    width, height = _positive(cta, "width"), _positive(cta, "height")
    hero_width, hero_height = _positive(hero, "width"), _positive(hero, "height")
    alignment, treatment = str(cta.get("alignment") or ""), str(cta.get("treatment") or "")
    raw = {
        "x_viewport_ratio": _ratio(_number(cta.get("x")), vw),
        "y_viewport_ratio": _ratio(_number(cta.get("y")), vh),
        "width_viewport_ratio": _ratio(width, vw),
        "height_viewport_ratio": _ratio(height, vh),
        "x_hero_ratio": _number(cta.get("x_hero_ratio")),
        "y_hero_ratio": _number(cta.get("y_hero_ratio")),
        "width_hero_ratio": _ratio(width, hero_width),
        "height_hero_ratio": _ratio(height, hero_height),
        "alignment": alignment,
        "treatment": treatment,
    }
    if not _valid_rect(cta) or any(value is None or value == "" for value in raw.values()):
        return None, None
    return raw, f"{alignment}_{treatment}"


_EXTRACTORS = {
    "HERO_SILHOUETTE": _hero_vector,
    "SECTION_GEOMETRY": _section_vector,
    "TWO_COLUMN_REPETITION": _two_column_vector,
    "CARD_CONTAINER_DENSITY": _card_vector,
    "MEDIA_DOMINANCE": _media_vector,
    "TYPOGRAPHIC_SILHOUETTE": _typography_vector,
    "WHITESPACE_DENSITY": _whitespace_vector,
    "PAGE_RHYTHM": _rhythm_vector,
    "SIGNATURE_DEVICE": _signature_vector,
    "CTA_MORPHOLOGY": _cta_vector,
}

_CATEGORICAL_MEASUREMENTS = {
    "HERO_SILHOUETTE": ("layout_axis",),
    "TYPOGRAPHIC_SILHOUETTE": ("family_class",),
    "SIGNATURE_DEVICE": ("structural_orientation",),
    "CTA_MORPHOLOGY": ("alignment", "treatment"),
}

_VECTOR_SCAN_REQUIREMENTS = {
    "HERO_SILHOUETTE": ("viewport", "hero"),
    "SECTION_GEOMETRY": ("viewport", "document", "sections"),
    "TWO_COLUMN_REPETITION": ("sections",),
    "CARD_CONTAINER_DENSITY": ("viewport", "document", "sections", "bordered_containers"),
    "MEDIA_DOMINANCE": ("document", "hero", "media", "signature_device"),
    "TYPOGRAPHIC_SILHOUETTE": ("viewport", "heading"),
    "WHITESPACE_DENSITY": ("viewport", "hero", "sections"),
    "PAGE_RHYTHM": ("viewport", "sections"),
    "SIGNATURE_DEVICE": ("viewport", "signature_device"),
    "CTA_MORPHOLOGY": ("viewport", "hero", "cta"),
}

_COMPUTED_LAYOUT_KEYS = (
    "display",
    "position",
    "grid_template_columns",
    "grid_template_rows",
    "flex_direction",
    "gap",
    "justify_content",
    "align_items",
)

_MEASUREMENT_SCHEMA_ENTRIES = {
    "viewport",
    "document",
    "hero",
    "hero.major_children",
    "sections",
    "sections.child_regions",
    "sections.computed_layout",
    "media_elements",
    "bordered_containers",
    "heading.computed_style",
    "whitespace.internal_occupancy",
    "signature_device.target_region",
    "cta.geometry_and_alignment",
}


def _missing_rect(value: Any, prefix: str) -> list[str]:
    rect = _mapping(value)
    missing = []
    for key in ("x", "y"):
        if _number(rect.get(key)) is None:
            missing.append(f"{prefix}.{key}")
    for key in ("width", "height"):
        if _positive(rect, key) is None:
            missing.append(f"{prefix}.{key}")
    return missing


def _missing_computed(value: Any, prefix: str) -> list[str]:
    computed = _mapping(value)
    return [f"{prefix}.{key}" for key in _COMPUTED_LAYOUT_KEYS if not isinstance(computed.get(key), str)]


def validate_rendered_morphology_evidence(
    evidence: Mapping[str, Any],
    evaluation_stage: Any = None,
) -> Dict[str, Any]:
    """Validate the complete, versioned browser evidence contract."""

    if not isinstance(evidence, Mapping):
        return {"status": "BLOCKED_INSUFFICIENT_EVIDENCE", "missing_fields": ["evidence"]}
    missing: list[str] = []
    if evidence.get("evidence_kind") != "BROWSER_LAYOUT":
        missing.append("evidence_kind")
    if str(evidence.get("measurement_schema_version") or "") != "2.0":
        missing.append("measurement_schema_version")
    embedded_stage = evidence.get("evaluation_stage")
    if not isinstance(embedded_stage, str) or not embedded_stage.strip():
        missing.append("evaluation_stage")
    elif evaluation_stage is not None and _stage(embedded_stage) != _stage(evaluation_stage):
        missing.append("evaluation_stage:mismatch")
    declared_schema = evidence.get("measurement_schema")
    if not isinstance(declared_schema, list):
        missing.append("measurement_schema")
    else:
        declared_entries = {entry for entry in declared_schema if isinstance(entry, str)}
        if len(declared_entries) != len(declared_schema):
            missing.append("measurement_schema:invalid_entry")
        missing.extend(
            f"measurement_schema:{entry}"
            for entry in sorted(_MEASUREMENT_SCHEMA_ENTRIES - declared_entries)
        )

    for name in ("viewport", "document"):
        record = _mapping(evidence.get(name))
        for key in ("width", "height", "area"):
            if _positive(record, key) is None:
                missing.append(f"{name}.{key}")

    hero = _mapping(evidence.get("hero"))
    missing.extend(_missing_rect(hero, "hero"))
    missing.extend(_missing_computed(hero, "hero"))
    hero_children = _records(hero.get("major_children"))
    if not hero_children:
        missing.append("hero.major_children")
    for index, child in enumerate(hero_children):
        missing.extend(_missing_rect(child, f"hero.major_children[{index}]"))
        missing.extend(_missing_computed(child.get("computed"), f"hero.major_children[{index}].computed"))

    sections = _records(evidence.get("sections"))
    if not sections:
        missing.append("sections")
    for index, section in enumerate(sections):
        prefix = f"sections[{index}]"
        missing.extend(_missing_rect(section, prefix))
        missing.extend(_missing_computed(section, prefix))
        children = _records(section.get("child_regions"))
        if not children:
            missing.append(f"{prefix}.child_regions")
        for child_index, child in enumerate(children):
            child_prefix = f"{prefix}.child_regions[{child_index}]"
            missing.extend(_missing_rect(child, child_prefix))
            missing.extend(_missing_computed(child.get("computed"), f"{child_prefix}.computed"))

    media = evidence.get("media_elements")
    if not isinstance(media, list):
        missing.append("media_elements")
    else:
        for index, item in enumerate(media):
            missing.extend(_missing_rect(item, f"media_elements[{index}]"))
            if not isinstance(_mapping(item).get("media_kind"), str):
                missing.append(f"media_elements[{index}].media_kind")

    containers = evidence.get("bordered_containers")
    if not isinstance(containers, list):
        missing.append("bordered_containers")
    else:
        for index, item in enumerate(containers):
            missing.extend(_missing_rect(item, f"bordered_containers[{index}]"))
            if not isinstance(_mapping(item).get("border_widths"), Mapping):
                missing.append(f"bordered_containers[{index}].border_widths")

    heading = _mapping(evidence.get("heading"))
    if heading.get("target_found") is not True:
        missing.append("heading.target_found")
    missing.extend(_missing_rect(heading.get("rect"), "heading.rect"))
    for key in ("font_family",):
        if not isinstance(heading.get(key), str) or not str(heading.get(key)).strip():
            missing.append(f"heading.{key}")
    for key in ("font_size", "line_height", "line_count"):
        if _positive(heading, key) is None:
            missing.append(f"heading.{key}")
    if _number(heading.get("letter_spacing")) is None:
        missing.append("heading.letter_spacing")

    whitespace = _mapping(evidence.get("whitespace"))
    for key in ("occupied_area_ratio", "negative_space_ratio", "hero_occupied_area_ratio", "major_region_gap_ratio"):
        if _number(whitespace.get(key)) is None:
            missing.append(f"whitespace.{key}")

    signature = _mapping(evidence.get("signature_device"))
    missing.extend(_missing_rect(signature, "signature_device"))
    missing.extend(_missing_rect(signature.get("dominant_child"), "signature_device.dominant_child"))
    for key in ("occupied_area_ratio", "dominant_child_aspect_ratio", "media_area"):
        if _number(signature.get(key)) is None:
            missing.append(f"signature_device.{key}")
    if not isinstance(signature.get("structural_orientation"), str) or not signature.get("structural_orientation"):
        missing.append("signature_device.structural_orientation")

    cta = _mapping(evidence.get("cta"))
    missing.extend(_missing_rect(cta, "cta"))
    for key in ("x_hero_ratio", "y_hero_ratio"):
        if _number(cta.get(key)) is None:
            missing.append(f"cta.{key}")
    for key in ("alignment", "treatment"):
        if not isinstance(cta.get(key), str) or not cta.get(key):
            missing.append(f"cta.{key}")
    if not isinstance(cta.get("source"), str) or not cta.get("source"):
        missing.append("cta.source")
    effective_stage = _stage(evaluation_stage if evaluation_stage is not None else embedded_stage)
    if effective_stage == HERO_PLUS_SIGNATURE_DEVICE_ONLY and cta.get("within_hero") is not True:
        missing.append("cta.within_hero")

    scan = _mapping(evidence.get("scan_complete"))
    for flag in sorted({flag for values in _VECTOR_SCAN_REQUIREMENTS.values() for flag in values}):
        if scan.get(flag) is not True:
            missing.append(f"scan_complete.{flag}")
    return {
        "status": "PASS" if not missing else "BLOCKED_INSUFFICIENT_EVIDENCE",
        "missing_fields": sorted(set(missing)),
    }


def extract_rendered_morphology(evidence: Mapping[str, Any], evaluation_stage: Any = None) -> Dict[str, Any]:
    """Extract applicable vectors while retaining raw normalized evidence."""

    stage = _stage(evaluation_stage or (evidence.get("evaluation_stage") if isinstance(evidence, Mapping) else None))
    applicable = applicable_vectors(stage)
    not_applicable = tuple(vector for vector in MORPHOLOGY_VECTOR_IDS if vector not in applicable)
    schema_validation = validate_rendered_morphology_evidence(evidence, stage)
    if schema_validation["status"] != "PASS":
        return {
            "status": "BLOCKED_INSUFFICIENT_EVIDENCE",
            "reason": "RENDERED_BROWSER_LAYOUT_EVIDENCE_INCOMPLETE",
            "evaluation_stage": stage,
            "applicable_vectors": list(applicable),
            "not_applicable_vectors": list(not_applicable),
            "insufficient_evidence_vectors": list(applicable),
            "missing_evidence_fields": schema_validation["missing_fields"],
            "vectors": {},
            "raw_measurements": {},
            "evidence_schema_complete": False,
        }

    labels: Dict[str, Any] = {}
    raw_measurements: Dict[str, Any] = {}
    insufficient: list[str] = []
    scan = _mapping(evidence.get("scan_complete"))
    schema_current = True
    for vector in MORPHOLOGY_VECTOR_IDS:
        if vector not in applicable:
            labels[vector] = "NOT_APPLICABLE"
            continue
        scan_complete = schema_current and all(
            scan.get(flag) is True for flag in _VECTOR_SCAN_REQUIREMENTS[vector]
        )
        if not scan_complete:
            labels[vector] = "INSUFFICIENT_EVIDENCE"
            insufficient.append(vector)
            continue
        raw, label = _EXTRACTORS[vector](evidence)
        if raw is None or label is None:
            labels[vector] = "INSUFFICIENT_EVIDENCE"
            insufficient.append(vector)
            continue
        labels[vector] = label
        raw_measurements[vector] = raw
    return {
        "status": "BLOCKED_INSUFFICIENT_EVIDENCE" if insufficient else "PASS",
        "reason": "APPLICABLE_VECTOR_EVIDENCE_INCOMPLETE" if insufficient else None,
        "evidence_kind": "BROWSER_LAYOUT",
        "measurement_schema_version": evidence.get("measurement_schema_version"),
        "evaluation_stage": stage,
        "applicable_vectors": list(applicable),
        "not_applicable_vectors": list(not_applicable),
        "insufficient_evidence_vectors": insufficient,
        "missing_evidence_fields": [],
        "vectors": labels,
        "raw_measurements": raw_measurements,
        "evidence_schema_complete": not insufficient,
    }


def compare_rendered_morphology(
    candidate_evidence: Mapping[str, Any],
    baseline_evidence: Mapping[str, Any],
    evaluation_stage: Any = None,
) -> Dict[str, Any]:
    """Compare browser evidence using continuous values and a scoped denominator."""

    stage = _stage(
        evaluation_stage
        or (candidate_evidence.get("evaluation_stage") if isinstance(candidate_evidence, Mapping) else None)
        or (baseline_evidence.get("evaluation_stage") if isinstance(baseline_evidence, Mapping) else None)
    )
    candidate = extract_rendered_morphology(candidate_evidence, stage)
    baseline = extract_rendered_morphology(baseline_evidence, stage)
    applicable = list(applicable_vectors(stage))
    not_applicable = [vector for vector in MORPHOLOGY_VECTOR_IDS if vector not in applicable]
    insufficient = sorted(
        set(candidate.get("insufficient_evidence_vectors", [])) | set(baseline.get("insufficient_evidence_vectors", [])),
        key=MORPHOLOGY_VECTOR_IDS.index,
    )

    vector_results: Dict[str, Any] = {}
    divergent: list[str] = []
    matching: list[str] = []
    for vector in MORPHOLOGY_VECTOR_IDS:
        if vector in not_applicable:
            vector_results[vector] = {
                "RAW_CANDIDATE_MEASUREMENTS": None,
                "RAW_BASELINE_MEASUREMENTS": None,
                "NORMALIZED_DISTANCE_OR_SIMILARITY": None,
                "CANONICAL_LABEL": "NOT_APPLICABLE",
                "VECTOR_VERDICT": "NOT_APPLICABLE",
            }
            continue
        candidate_raw = _mapping(candidate.get("raw_measurements", {})).get(vector)
        baseline_raw = _mapping(baseline.get("raw_measurements", {})).get(vector)
        if vector in insufficient or not isinstance(candidate_raw, Mapping) or not isinstance(baseline_raw, Mapping):
            vector_results[vector] = {
                "RAW_CANDIDATE_MEASUREMENTS": candidate_raw,
                "RAW_BASELINE_MEASUREMENTS": baseline_raw,
                "NORMALIZED_DISTANCE_OR_SIMILARITY": None,
                "CANONICAL_LABEL": {
                    "candidate": _mapping(candidate.get("vectors", {})).get(vector),
                    "baseline": _mapping(baseline.get("vectors", {})).get(vector),
                },
                "VECTOR_VERDICT": "INSUFFICIENT_EVIDENCE",
            }
            continue
        distance = _measurement_distance(candidate_raw, baseline_raw, categorical=_CATEGORICAL_MEASUREMENTS.get(vector, ()))
        verdict = "INSUFFICIENT_EVIDENCE" if distance is None else (
            "DIVERGENT" if distance >= _VECTOR_DISTANCE_THRESHOLDS[vector] else "MATCHES_HISTORICAL_BASELINE"
        )
        if verdict == "INSUFFICIENT_EVIDENCE":
            insufficient.append(vector)
        elif verdict == "DIVERGENT":
            divergent.append(vector)
        else:
            matching.append(vector)
        vector_results[vector] = {
            "RAW_CANDIDATE_MEASUREMENTS": dict(candidate_raw),
            "RAW_BASELINE_MEASUREMENTS": dict(baseline_raw),
            "NORMALIZED_DISTANCE_OR_SIMILARITY": {
                "distance": distance,
                "similarity": round(1.0 - distance, 6) if distance is not None else None,
                "divergence_threshold": _VECTOR_DISTANCE_THRESHOLDS[vector],
            },
            "CANONICAL_LABEL": {
                "candidate": _mapping(candidate.get("vectors", {})).get(vector),
                "baseline": _mapping(baseline.get("vectors", {})).get(vector),
            },
            "VECTOR_VERDICT": verdict,
        }

    insufficient = sorted(set(insufficient), key=MORPHOLOGY_VECTOR_IDS.index)
    evidenced_count = len(applicable) - len(insufficient)
    divergence_ratio = round(len(divergent) / evidenced_count, 6) if evidenced_count else None
    required_count = ceil(len(applicable) * SUBSTANTIAL_DIVERGENCE_RATIO)
    if insufficient:
        status = "BLOCKED_INSUFFICIENT_EVIDENCE"
    else:
        status = "PASS_DIVERGENCE" if len(divergent) >= required_count else "FAIL_DIVERGENCE"
    evidence_schema_complete = (
        candidate.get("evidence_schema_complete") is True
        and baseline.get("evidence_schema_complete") is True
        and not insufficient
    )
    return {
        "status": status,
        "divergence": {
            "PASS_DIVERGENCE": "RENDER_DERIVED_MORPHOLOGY_PASS",
            "FAIL_DIVERGENCE": "RENDER_DERIVED_MORPHOLOGY_FAIL",
            "BLOCKED_INSUFFICIENT_EVIDENCE": "RENDER_DERIVED_MORPHOLOGY_BLOCKED_INSUFFICIENT_EVIDENCE",
        }[status],
        "evaluation_stage": stage,
        "candidate": candidate,
        "baseline": baseline,
        "applicable_vectors": applicable,
        "not_applicable_vectors": not_applicable,
        "insufficient_evidence_vectors": insufficient,
        "divergent_vectors": divergent,
        "matching_vectors": matching,
        "applicable_vector_count": len(applicable),
        "not_applicable_vector_count": len(not_applicable),
        "sufficiently_evidenced_vector_count": evidenced_count,
        "divergent_vector_count": len(divergent),
        "substantial_divergence_required": SUBSTANTIAL_DIVERGENCE_RATIO,
        "required_divergent_vector_count": required_count,
        "divergence_ratio": divergence_ratio,
        "failures": matching,
        "vector_results": vector_results,
        "vector_verdicts": {vector: result["VECTOR_VERDICT"] for vector, result in vector_results.items()},
        "evidence_schema_complete": evidence_schema_complete,
        "semantic_labels_used": False,
        "continuous_evidence_used": True,
    }


__all__ = [
    "CHEAP_CONCEPT_NOT_APPLICABLE_VECTOR_IDS",
    "CHEAP_CONCEPT_VECTOR_IDS",
    "HERO_PLUS_SIGNATURE_DEVICE_ONLY",
    "MORPHOLOGY_VECTOR_IDS",
    "SUBSTANTIAL_DIVERGENCE_RATIO",
    "applicable_vectors",
    "compare_rendered_morphology",
    "extract_rendered_morphology",
    "validate_rendered_morphology_evidence",
]
