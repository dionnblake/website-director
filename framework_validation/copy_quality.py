"""Website Director's bounded source-copy pattern precheck.

This module adapts selected deterministic pattern concepts from SlopMonster
at https://github.com/ItsssssJack/SlopMonster, commit
f261dbf11c2a206ecd8780c070a46dae64edd8be. SlopMonster is MIT licensed,
Copyright (c) 2026 Jack Roberts. The selected concepts are independently
bounded here for advisory Website Director copy review.

The complete upstream permission notice is preserved here because this module
directly adapts selected upstream pattern expressions and concepts:

MIT License

Copyright (c) 2026 Jack Roberts

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

The scanner emits review findings only. It does not score copy, rewrite text,
validate factual claims, call a provider, or create a readiness state or gate.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any


SOURCE = "COPY_PATTERN_SCANNER"
HEURISTIC = "HEURISTIC"
DETERMINISTIC = "DETERMINISTIC"

STATUS_SCANNED = "SCANNED"
STATUS_NOT_APPLICABLE = "NOT_APPLICABLE"
STATUS_BLOCKED = "BLOCKED"

RULE_NEGATED_JUST_BUT = "NEGATED_JUST_CONTRAST_BUT"
RULE_NEGATED_JUST_COPULA = "NEGATED_JUST_COPULA_CONTRAST"
RULE_MORE_THAN_JUST = "MORE_THAN_JUST"
RULE_THATS_WHERE_COMES_IN = "THATS_WHERE_COMES_IN"
RULE_SAY_GOODBYE_TO = "SAY_GOODBYE_TO"
RULE_IMAGINE_OPENER = "IMAGINE_OPENER"
RULE_ESSAY_SUMMARY = "ESSAY_SUMMARY"
RULE_WHEN_IT_COMES_TO = "WHEN_IT_COMES_TO"
RULE_AT_END_OF_DAY = "AT_END_OF_DAY"
RULE_STACKED_HEDGING = "STACKED_HEDGING"
RULE_INTENSIFIER_PADDING = "INTENSIFIER_PADDING"
RULE_THROAT_CLEARING = "THROAT_CLEARING"
RULE_BOILERPLATE_CTA = "BOILERPLATE_CTA"
RULE_SELF_ANSWERING_QUESTION = "SELF_ANSWERING_QUESTION"
RULE_EM_DASH_DENSITY = "EM_DASH_DENSITY"
RULE_HYPHENATED_COMPOUND_STACK = "HYPHENATED_COMPOUND_STACK"

ADOPTED_RULES = (
    RULE_NEGATED_JUST_BUT,
    RULE_NEGATED_JUST_COPULA,
    RULE_MORE_THAN_JUST,
    RULE_THATS_WHERE_COMES_IN,
    RULE_SAY_GOODBYE_TO,
    RULE_IMAGINE_OPENER,
    RULE_ESSAY_SUMMARY,
    RULE_WHEN_IT_COMES_TO,
    RULE_AT_END_OF_DAY,
    RULE_STACKED_HEDGING,
    RULE_INTENSIFIER_PADDING,
    RULE_BOILERPLATE_CTA,
    RULE_SELF_ANSWERING_QUESTION,
)

NARROWED_RULES = (
    RULE_THROAT_CLEARING,
    RULE_EM_DASH_DENSITY,
    RULE_HYPHENATED_COMPOUND_STACK,
)

DELEGATED_RULES = (
    "CUTTING_EDGE",
    "STATE_OF_THE_ART",
    "UNPARALLELED",
    "WORLD_CLASS",
    "BEST_IN_CLASS",
    "WHETHER_YOU_ARE_X_OR_Y",
    "NUMERIC_PEOPLE_PROOF",
)

_NEGATED_JUST = r"(?:\bnot|n['’]t)\s+(?:just|only|merely|simply)\b"
_XY_TAIL = (
    r"[^!?]{0,80}?[,.]\s*"
    r"(?:it|this|that|they|we|you|he|she|i)\b"
)


@dataclass(frozen=True)
class _Pattern:
    rule: str
    expression: re.Pattern[str]
    remediation: str


_PATTERNS = (
    _Pattern(
        RULE_NEGATED_JUST_BUT,
        re.compile(rf"{_NEGATED_JUST}[^.!?]{{0,80}}\bbut\b", re.IGNORECASE),
        "Review whether the contrast adds information; replace generic contrast framing manually if needed.",
    ),
    _Pattern(
        RULE_NEGATED_JUST_COPULA,
        re.compile(rf"{_NEGATED_JUST}{_XY_TAIL}", re.IGNORECASE),
        "Review whether the contrast adds information; replace generic contrast framing manually if needed.",
    ),
    _Pattern(
        RULE_MORE_THAN_JUST,
        re.compile(r"\bmore than just\b", re.IGNORECASE),
        "State the concrete additional value directly instead of relying on a stock contrast.",
    ),
    _Pattern(
        RULE_THATS_WHERE_COMES_IN,
        re.compile(r"\b(?:that|this)(?:'?s| is) where\b[^.!?]{0,30}\bcomes? in\b", re.IGNORECASE),
        "Name the concrete action or role directly rather than using a stock transition.",
    ),
    _Pattern(
        RULE_SAY_GOODBYE_TO,
        re.compile(r"\bsay goodbye to\b", re.IGNORECASE),
        "Describe the specific change or outcome directly; avoid a generic departure promise.",
    ),
    _Pattern(
        RULE_IMAGINE_OPENER,
        re.compile(r"\bimagine (?:a|an|the)\b", re.IGNORECASE),
        "Replace the invitation with a concrete scenario, result, or user action.",
    ),
    _Pattern(
        RULE_ESSAY_SUMMARY,
        re.compile(r"\b(?:in conclusion|to sum up)\b", re.IGNORECASE),
        "End with the decision, action, or implication directly instead of announcing a summary.",
    ),
    _Pattern(
        RULE_WHEN_IT_COMES_TO,
        re.compile(r"\bwhen it comes to\b", re.IGNORECASE),
        "Name the subject directly and remove the throat-clearing transition if it adds no meaning.",
    ),
    _Pattern(
        RULE_AT_END_OF_DAY,
        re.compile(r"\bat the end of the day\b", re.IGNORECASE),
        "State the practical conclusion directly rather than using a stock summary phrase.",
    ),
    _Pattern(
        RULE_STACKED_HEDGING,
        re.compile(r"\b(?:may potentially|could potentially|might possibly)\b", re.IGNORECASE),
        "Choose the accurate level of certainty and remove the redundant hedge.",
    ),
    _Pattern(
        RULE_INTENSIFIER_PADDING,
        re.compile(r"\b(?:very unique|quite literally)\b", re.IGNORECASE),
        "Check whether the intensifier is accurate and necessary; use the precise claim.",
    ),
    _Pattern(
        RULE_THROAT_CLEARING,
        re.compile(r"\b(?:here'?s the thing|let'?s break (?:it|this) down)\b", re.IGNORECASE),
        "Open with the useful point instead of announcing the point or a payoff.",
    ),
    _Pattern(
        RULE_BOILERPLATE_CTA,
        re.compile(r"\b(?:ready to get started|let'?s get started)\b", re.IGNORECASE),
        "Make the CTA describe the next action and its immediate value.",
    ),
    _Pattern(
        RULE_SELF_ANSWERING_QUESTION,
        re.compile(r"\bthe (?:result|answer|catch|kicker|upshot)\?\s", re.IGNORECASE),
        "Replace the rhetorical question with the result or decision itself.",
    ),
)

_COMPOUND = re.compile(r"\b[a-z]{2,}-[a-z]{2,}(?:-[a-z]{2,})*\b", re.IGNORECASE)
_LOCALE = re.compile(r"^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$")


@dataclass(frozen=True)
class CopyFinding:
    """One advisory finding with the evidence fields used by the audit."""

    finding_id: str
    source: str
    method: str
    rule: str
    location_or_context: str
    severity: str
    evidence: str
    remediation: str
    lock_impact: str

    def as_dict(self) -> dict[str, str]:
        return {
            "FINDING_ID": self.finding_id,
            "SOURCE": self.source,
            "METHOD": self.method,
            "RULE": self.rule,
            "LOCATION_OR_CONTEXT": self.location_or_context,
            "SEVERITY": self.severity,
            "EVIDENCE": self.evidence,
            "REMEDIATION": self.remediation,
            "LOCK_IMPACT": self.lock_impact,
        }


@dataclass(frozen=True)
class CopyScanResult:
    """Deterministic scan output without a score or approval claim."""

    status: str
    reason: str | None
    source_locale: str | None
    input_format: str
    findings: tuple[CopyFinding, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "reason": self.reason,
            "source_locale": self.source_locale,
            "input_format": self.input_format,
            "findings": [finding.as_dict() for finding in self.findings],
        }


@dataclass(frozen=True)
class _Candidate:
    start: int
    end: int
    rule: str
    evidence: str
    remediation: str


def _normalise(text: str) -> str:
    """Normalize typography without changing words or sentence punctuation."""

    normalized = (
        text.replace("\u2011", "-")
        .replace("\u00a0", " ")
        .replace("\u2019", "'")
        .replace("\u2018", "'")
    )
    lines = [re.sub(r"[ \t\f\v]+", " ", line).strip() for line in normalized.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def _markdown_prose(text: str) -> str:
    """Extract simple Markdown prose while excluding code and image labels."""

    prose = re.sub(r"```[\s\S]*?```", "\n", text)
    prose = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", prose)
    prose = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", prose)
    prose = re.sub(r"`[^`]*`", " ", prose)
    prose = re.sub(r"~~[^~]*~~", " ", prose)
    prose = re.sub(r"^\s{0,3}(?:#{1,6}|>|[-*+]\s)", "", prose, flags=re.MULTILINE)
    prose = re.sub(r"^\s*\|", "", prose, flags=re.MULTILINE)
    prose = prose.replace("|", " ")
    return _normalise(prose)


def _locale_language(source_locale: str | None) -> str | None:
    if not isinstance(source_locale, str):
        return None
    candidate = source_locale.strip()
    if not candidate or candidate.lower() in {"und", "unknown"} or not _LOCALE.fullmatch(candidate):
        return None
    return candidate.split("-", 1)[0].lower()


def _context(text: str, start: int, end: int) -> str:
    left = max(0, start - 48)
    right = min(len(text), end + 48)
    prefix = "..." if left else ""
    suffix = "..." if right < len(text) else ""
    excerpt = re.sub(r"\s+", " ", text[left:right]).strip()
    return f"{prefix}{excerpt}{suffix}"


def _sentence_windows(text: str) -> list[tuple[int, str]]:
    windows: list[tuple[int, str]] = []
    segment_start = 0
    for punctuation in re.finditer(r"[.!?]", text):
        segment_end = punctuation.end()
        segment = text[segment_start:segment_end]
        if segment.strip():
            for offset in range(0, len(segment), 220):
                windows.append((segment_start + offset, segment[offset : offset + 220]))
        segment_start = segment_end
    if segment_start < len(text):
        segment = text[segment_start:]
        for offset in range(0, len(segment), 220):
            windows.append((segment_start + offset, segment[offset : offset + 220]))
    return windows


def _candidate_findings(text: str) -> list[_Candidate]:
    candidates: list[_Candidate] = []
    for pattern in _PATTERNS:
        for match in pattern.expression.finditer(text):
            candidates.append(
                _Candidate(
                    start=match.start(),
                    end=match.end(),
                    rule=pattern.rule,
                    evidence=match.group(0).strip(),
                    remediation=pattern.remediation,
                )
            )

    for window_start, window in _sentence_windows(text):
        if window.count("—") >= 2:
            candidates.append(
                _Candidate(
                    start=window_start,
                    end=window_start + len(window),
                    rule=RULE_EM_DASH_DENSITY,
                    evidence=_context(text, window_start, window_start + len(window)),
                    remediation="Review whether the sentence needs multiple parenthetical breaks; separate distinct ideas directly.",
                )
            )
        compounds = _COMPOUND.findall(window)
        if len(compounds) >= 4:
            candidates.append(
                _Candidate(
                    start=window_start,
                    end=window_start + len(window),
                    rule=RULE_HYPHENATED_COMPOUND_STACK,
                    evidence=", ".join(compounds[:6]),
                    remediation="Replace stacked modifiers with concrete nouns, verbs, or shorter clauses.",
                )
            )
    return candidates


def _finding(candidate: _Candidate, index: int, content_locked: bool) -> CopyFinding:
    return CopyFinding(
        finding_id=f"COPY_PATTERN_{index:03d}",
        source=SOURCE,
        method=HEURISTIC,
        rule=candidate.rule,
        location_or_context=f"characters {candidate.start}:{candidate.end}; {_context(candidate.evidence, 0, len(candidate.evidence))}",
        severity="MINOR",
        evidence=candidate.evidence,
        remediation=candidate.remediation,
        lock_impact="LOCKED_CHANGE_REQUIRED" if content_locked else "REVIEW_BEFORE_CONTENT_LOCK",
    )


def _blocked(reason: str, source_locale: str | None, input_format: str, *, empty: bool = False) -> CopyScanResult:
    findings: tuple[CopyFinding, ...] = ()
    if empty:
        findings = (
            CopyFinding(
                finding_id="COPY_INPUT_001",
                source=SOURCE,
                method=DETERMINISTIC,
                rule="EMPTY_INPUT",
                location_or_context="input",
                severity="MINOR",
                evidence="No non-whitespace copy was supplied.",
                remediation="Supply the source copy before requesting a pattern review.",
                lock_impact="NONE",
            ),
        )
    return CopyScanResult(STATUS_BLOCKED, reason, source_locale, input_format, findings)


def scan_copy(
    text: str,
    *,
    source_locale: str | None,
    content_locked: bool,
    input_format: str = "plain",
) -> CopyScanResult:
    """Scan supplied source copy for a curated set of advisory heuristics.

    ``source_locale`` is required evidence for applicability. English is the
    only scanned language. Known non-English input is explicitly skipped, and
    unknown locale evidence is blocked rather than treated as clean.
    ``content_locked`` is an explicit boolean supplied by the caller from the
    existing canonical lock condition; this scanner never resolves or writes
    lock state.
    """

    if input_format not in {"plain", "markdown"}:
        raise ValueError("input_format must be 'plain' or 'markdown'")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(content_locked, bool):
        raise TypeError("content_locked must be a boolean")

    prose = _markdown_prose(text) if input_format == "markdown" else _normalise(text)
    if not prose:
        return _blocked("EMPTY_INPUT", source_locale, input_format, empty=True)

    language = _locale_language(source_locale)
    if language is None:
        return _blocked("SOURCE_LOCALE_UNKNOWN", source_locale, input_format)
    if language != "en":
        return CopyScanResult(STATUS_NOT_APPLICABLE, "SOURCE_LOCALE_NON_ENGLISH", source_locale, input_format, ())

    candidates = sorted(_candidate_findings(prose), key=lambda item: (item.start, item.rule, item.end, item.evidence))
    findings = tuple(_finding(candidate, index, content_locked) for index, candidate in enumerate(candidates, start=1))
    return CopyScanResult(STATUS_SCANNED, None, source_locale, input_format, findings)


__all__ = [
    "ADOPTED_RULES",
    "DELEGATED_RULES",
    "NARROWED_RULES",
    "CopyFinding",
    "CopyScanResult",
    "SOURCE",
    "STATUS_BLOCKED",
    "STATUS_NOT_APPLICABLE",
    "STATUS_SCANNED",
    "scan_copy",
]
