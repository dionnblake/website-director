"""Derive clean-room morphology from browser layout evidence.

The extractor consumes measured DOM rectangles and computed-style facts emitted
by the existing Playwright browser adapter. It never consumes CSS class names,
builder labels, or a caller-declared ``semantic_rename_only`` flag.
"""

from __future__ import annotations

from statistics import median
from typing import Any, Dict, Mapping


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


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_records(value: Any) -> list[Mapping[str, Any]]:
    return [item for item in value if isinstance(item, Mapping)] if isinstance(value, list) else []


def _font_family_bucket(value: Any) -> str:
    family = str(value or "").lower()
    if any(token in family for token in ("mono", "courier", "consolas", "menlo")):
        return "MONO"
    if any(token in family for token in ("serif", "georgia", "times")):
        return "SERIF"
    return "SANS"


def _section_geometry(sections: list[Mapping[str, Any]]) -> str:
    if not sections:
        return "UNKNOWN"
    two_column = sum(1 for item in sections if _number(item.get("column_count")) >= 2)
    return "ALTERNATING_TWO_COLUMN" if two_column >= max(2, len(sections) // 2) else "SINGLE_COLUMN_NARRATIVE"


def _alternating_two_column(sections: list[Mapping[str, Any]]) -> bool:
    alignments = [str(item.get("column_alignment", "")) for item in sections
                  if _number(item.get("column_count")) >= 2]
    if len(alignments) < 3:
        return False
    changes = sum(left != right for left, right in zip(alignments, alignments[1:]))
    return changes >= len(alignments) - 2


def _page_rhythm(sections: list[Mapping[str, Any]]) -> str:
    heights = [_number(item.get("height")) for item in sections if _number(item.get("height")) > 0]
    gaps = [_number(item.get("gap_before")) for item in sections[1:]]
    if len(heights) < 2:
        return "UNKNOWN"
    height_median = median(heights)
    gap_median = median(gaps) if gaps else 0.0
    height_spread = max(heights) - min(heights)
    gap_spread = (max(gaps) - min(gaps)) if gaps else 0.0
    if height_spread <= max(24.0, height_median * 0.18) and gap_spread <= max(24.0, gap_median * 0.18):
        return "REGULAR_SECTION_CADENCE"
    return "IRREGULAR_CHAPTERS"


def extract_rendered_morphology(evidence: Mapping[str, Any]) -> Dict[str, Any]:
    """Extract the ten divergence vectors from measured browser evidence."""

    if not isinstance(evidence, Mapping) or str(evidence.get("evidence_kind", "")) != "BROWSER_LAYOUT":
        return {
            "status": "BLOCKED",
            "reason": "RENDERED_BROWSER_LAYOUT_EVIDENCE_REQUIRED",
            "vectors": {},
        }

    sections = _safe_records(evidence.get("sections"))
    hero = evidence.get("hero") if isinstance(evidence.get("hero"), Mapping) else {}
    cta = evidence.get("cta") if isinstance(evidence.get("cta"), Mapping) else {}
    viewport_width = _number(evidence.get("viewport_width"), 1.0)
    viewport_height = _number(evidence.get("viewport_height"), 1.0)
    document_height = _number(evidence.get("document_height"), viewport_height)
    media_area_ratio = _number(evidence.get("media_area_ratio"))
    bordered_count = _number(evidence.get("bordered_container_count"))
    section_count = max(1, len(sections))
    round_shape_count = _number(evidence.get("round_shape_count"))
    cta_center = _number(cta.get("x")) + (_number(cta.get("width")) / 2.0)
    centered_cta = abs(cta_center - (viewport_width / 2.0)) <= max(28.0, viewport_width * 0.08)
    hero_full_bleed = (
        _number(hero.get("width")) >= viewport_width * 0.9
        and _number(hero.get("height")) >= viewport_height * 0.55
    )
    hero_has_columns = _number(hero.get("column_count")) >= 2

    vectors = {
        "HERO_SILHOUETTE": "FULL_BLEED_ASYMMETRIC" if hero_full_bleed else (
            "CENTERED_SPLIT_HERO" if hero_has_columns else "COMPACT_HERO"
        ),
        "SECTION_GEOMETRY": _section_geometry(sections),
        "TWO_COLUMN_REPETITION": _alternating_two_column(sections),
        "CARD_CONTAINER_DENSITY": (
            "HIGH_BORDERED_BOXES" if bordered_count / section_count >= 1.5
            else "OPEN_FIELD"
        ),
        "MEDIA_DOMINANCE": (
            "FULL_VIEWPORT_CANVAS" if media_area_ratio >= 0.34
            else "COMPACT_MEDIA_PANEL"
        ),
        "TYPOGRAPHIC_SILHOUETTE": _font_family_bucket(evidence.get("heading_font_family")),
        "WHITESPACE_DENSITY": (
            "EXPANSIVE" if _number(evidence.get("average_section_gap")) >= viewport_height * 0.16
            else "COMPACT"
        ),
        "PAGE_RHYTHM": _page_rhythm(sections),
        "SIGNATURE_DEVICE": "ROUND_FOCAL_DEVICE" if round_shape_count else "NO_ROUND_FOCAL_DEVICE",
        "CTA_MORPHOLOGY": "CENTERED_CONTAINED_BUTTON" if centered_cta else "EDGE_ALIGNED_ACTION",
    }
    return {
        "status": "PASS",
        "evidence_kind": "BROWSER_LAYOUT",
        "vectors": vectors,
        "measurements": {
            "viewport_width": viewport_width,
            "viewport_height": viewport_height,
            "document_height": document_height,
            "section_count": len(sections),
            "bordered_container_count": bordered_count,
            "media_area_ratio": media_area_ratio,
            "round_shape_count": round_shape_count,
            "average_section_gap": _number(evidence.get("average_section_gap")),
        },
    }


def compare_rendered_morphology(
    candidate_evidence: Mapping[str, Any],
    baseline_evidence: Mapping[str, Any],
) -> Dict[str, Any]:
    """Compare vectors extracted from two browser-rendered surfaces."""

    candidate = extract_rendered_morphology(candidate_evidence)
    baseline = extract_rendered_morphology(baseline_evidence)
    if candidate.get("status") != "PASS" or baseline.get("status") != "PASS":
        return {
            "status": "BLOCKED",
            "divergence": "RENDER_DERIVED_MORPHOLOGY_BLOCKED",
            "candidate": candidate,
            "baseline": baseline,
            "failures": [],
        }

    candidate_vectors = candidate["vectors"]
    baseline_vectors = baseline["vectors"]
    failures = [vector for vector in MORPHOLOGY_VECTOR_IDS
                if candidate_vectors.get(vector) == baseline_vectors.get(vector)]
    vector_results = {
        vector: "MATCHES_HISTORICAL_BASELINE" if vector in failures else "DIVERGENT"
        for vector in MORPHOLOGY_VECTOR_IDS
    }
    status = "FAIL_DIVERGENCE" if len(failures) >= 5 else "PASS_DIVERGENCE"
    return {
        "status": status,
        "divergence": "RENDER_DERIVED_MORPHOLOGY_FAIL" if status == "FAIL_DIVERGENCE"
        else "RENDER_DERIVED_MORPHOLOGY_PASS",
        "candidate": candidate,
        "baseline": baseline,
        "failures": failures,
        "vector_results": vector_results,
        "semantic_labels_used": False,
    }


__all__ = ["MORPHOLOGY_VECTOR_IDS", "compare_rendered_morphology", "extract_rendered_morphology"]
