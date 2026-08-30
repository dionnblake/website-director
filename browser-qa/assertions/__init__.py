"""Requirement-traced browser QA assertions (Website Director V2.15).

Every assertion traces to exactly one requirement source (protocol sec 29):

    LOCKED_SPEC | PRODUCTION_CHECKLIST | MEASUREMENT_PLAN | SECURITY_PRIVACY_REVIEW |
    ACCESSIBILITY_REVIEW | LOCALIZATION_PLAN | APPLICATION_ARCHITECTURE_PLAN |
    MOTION_SPEC | PAGE_EXPERIENCE_SPEC | BROWSER_QA_PLAN

Assertions read a ``PageObservation`` and the parsed browser-qa plan. They never
launch a browser and never mutate anything. Where Impeccable already owns a
*static* rule (a raw hex colour in a stylesheet, ``transition: all``), browser QA
does not re-implement it -- it only checks the *runtime-observable* half
(protocol sec 32).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

import os as _os
import sys as _sys

_BROWSER_QA_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _BROWSER_QA_ROOT not in _sys.path:
    _sys.path.insert(0, _BROWSER_QA_ROOT)

from engine.base import BLOCKED, FAIL, NOT_APPLICABLE, PASS, VERDICTS  # noqa: E402

REQUIREMENT_SOURCES = (
    "LOCKED_SPEC",
    "PRODUCTION_CHECKLIST",
    "MEASUREMENT_PLAN",
    "SECURITY_PRIVACY_REVIEW",
    "ACCESSIBILITY_REVIEW",
    "LOCALIZATION_PLAN",
    "APPLICATION_ARCHITECTURE_PLAN",
    "MOTION_SPEC",
    "PAGE_EXPERIENCE_SPEC",
    "BROWSER_QA_PLAN",
)


@dataclass
class Finding:
    check_id: str
    title: str
    verdict: str
    requirement_source: str
    route: str = ""
    viewport: int = 0
    browser: str = ""
    detail: str = ""
    method: str = "BROWSER_EXECUTED"
    owning_spec: str = ""
    evidence: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        assert self.verdict in VERDICTS, "bad verdict %r" % self.verdict
        assert self.requirement_source in REQUIREMENT_SOURCES, \
            "untraceable assertion %r" % self.requirement_source

    @property
    def ok(self) -> bool:
        return self.verdict in (PASS, NOT_APPLICABLE)


def finding(check_id, title, ok, source, obs, *, detail="", owning_spec="", na=False,
            evidence=None) -> Finding:
    verdict = NOT_APPLICABLE if na else (PASS if ok else FAIL)
    return Finding(
        check_id=check_id, title=title, verdict=verdict, requirement_source=source,
        route=getattr(obs, "route", ""), viewport=getattr(obs, "viewport", 0),
        browser=getattr(obs, "browser", ""), detail=detail, owning_spec=owning_spec,
        evidence=evidence or {},
    )


def blocked(check_id, title, source, reason) -> Finding:
    return Finding(check_id=check_id, title=title, verdict=BLOCKED,
                   requirement_source=source, detail=reason)


from . import catalog  # noqa: E402,F401  (registers the checks)

ALL_CHECKS = catalog.ALL_CHECKS


def evaluate(obs, plan: Dict[str, Any]) -> List[Finding]:
    out: List[Finding] = []
    for fn in ALL_CHECKS:
        result = fn(obs, plan)
        if result is None:
            continue
        out.extend(result if isinstance(result, list) else [result])
    return out
