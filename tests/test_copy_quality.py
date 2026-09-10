"""Tests for the bounded, advisory source-copy pattern precheck."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "browser-qa"))

from guards.frozen_integrity_guard import FrozenIntegrityGuard  # noqa: E402
from framework_validation.copy_quality import (
    ADOPTED_RULES,
    CopyFinding,
    DELEGATED_RULES,
    NARROWED_RULES,
    STATUS_BLOCKED,
    STATUS_NOT_APPLICABLE,
    STATUS_SCANNED,
    scan_copy,
)


class CopyQualityPatternTests(unittest.TestCase):
    def test_each_adopted_rule_has_a_positive_and_a_control(self) -> None:
        cases = {
            "NEGATED_JUST_CONTRAST_BUT": (
                "This is not just a report, but a working record.",
                "This report covers the record and the review.",
            ),
            "NEGATED_JUST_COPULA_CONTRAST": (
                "This isn't just a report, it's a working record.",
                "This report is about the record, not the claim.",
            ),
            "MORE_THAN_JUST": (
                "More than just a checklist.",
                "This checklist is just the starting point.",
            ),
            "THATS_WHERE_COMES_IN": (
                "This is where the record comes in.",
                "This is the place where the record lives.",
            ),
            "SAY_GOODBYE_TO": (
                "Say goodbye to brittle handoffs.",
                "Goodbye, brittle handoffs.",
            ),
            "IMAGINE_OPENER": (
                "Imagine a clear handoff.",
                "We imagine better records.",
            ),
            "ESSAY_SUMMARY": (
                "In conclusion, the plan is ready.",
                "The conclusion is in the record.",
            ),
            "WHEN_IT_COMES_TO": (
                "When it comes to handoffs, use the record.",
                "When records change, update the source.",
            ),
            "AT_END_OF_DAY": (
                "At the end of the day, the record must be current.",
                "At the end of this sentence, the record is clear.",
            ),
            "STACKED_HEDGING": (
                "It could potentially fail.",
                "It could fail, but we need evidence.",
            ),
            "INTENSIFIER_PADDING": (
                "The result is very unique.",
                "It is unique and literal.",
            ),
            "BOILERPLATE_CTA": (
                "Ready to get started?",
                "Get started when the review is complete.",
            ),
            "SELF_ANSWERING_QUESTION": (
                "The result? Evidence matters.",
                "The result is recorded.",
            ),
        }
        self.assertEqual(tuple(ADOPTED_RULES), tuple(cases))
        for rule, (positive, control) in cases.items():
            with self.subTest(rule=rule, kind="positive"):
                result = scan_copy(positive, source_locale="en-US")
                self.assertEqual(result.status, STATUS_SCANNED)
                self.assertIn(rule, {finding.rule for finding in result.findings})
            with self.subTest(rule=rule, kind="control"):
                result = scan_copy(control, source_locale="en-US")
                self.assertEqual(result.status, STATUS_SCANNED)
                self.assertNotIn(rule, {finding.rule for finding in result.findings})

    def test_narrowed_punctuation_rules_are_bounded_to_sentence_windows(self) -> None:
        em_dash = scan_copy("One record — one owner — one review.", source_locale="en-US")
        compounds = scan_copy(
            "Our industry-leading, context-aware, best-in-class, AI-powered record ships.",
            source_locale="en-US",
        )
        self.assertIn("EM_DASH_DENSITY", {finding.rule for finding in em_dash.findings})
        self.assertIn("HYPHENATED_COMPOUND_STACK", {finding.rule for finding in compounds.findings})
        self.assertEqual(
            tuple(NARROWED_RULES),
            ("THROAT_CLEARING", "EM_DASH_DENSITY", "HYPHENATED_COMPOUND_STACK"),
        )
        throat = scan_copy("Here's the thing: evidence matters.", source_locale="en-US")
        self.assertIn("THROAT_CLEARING", {finding.rule for finding in throat.findings})
        self.assertEqual(
            scan_copy("The best part of the record is the hash.", source_locale="en-US").findings,
            (),
        )
        self.assertEqual(
            scan_copy("One record — one owner.", source_locale="en-US").findings,
            (),
        )
        self.assertEqual(
            scan_copy(
                "An industry-leading tool supports a well-known standard.",
                source_locale="en-US",
            ).findings,
            (),
        )

    def test_findings_have_the_declared_evidence_contract(self) -> None:
        result = scan_copy("Say goodbye to brittle handoffs.", source_locale="en-US")
        self.assertEqual(len(result.findings), 1)
        finding = result.findings[0]
        self.assertIsInstance(finding, CopyFinding)
        self.assertEqual(
            set(finding.as_dict()),
            {
                "FINDING_ID",
                "SOURCE",
                "METHOD",
                "RULE",
                "LOCATION_OR_CONTEXT",
                "SEVERITY",
                "EVIDENCE",
                "REMEDIATION",
                "LOCK_IMPACT",
            },
        )
        self.assertEqual(finding.source, "COPY_PATTERN_SCANNER")
        self.assertEqual(finding.method, "HEURISTIC")
        self.assertEqual(finding.severity, "MINOR")
        self.assertEqual(finding.lock_impact, "REVIEW_BEFORE_CONTENT_LOCK")
        self.assertNotIn("rewrite", finding.remediation.lower())

    def test_output_order_and_serialization_are_deterministic(self) -> None:
        text = (
            "Imagine a clear handoff. Say goodbye to brittle handoffs. "
            "One record — one owner — one review."
        )
        first = scan_copy(text, source_locale="en-US")
        second = scan_copy(text, source_locale="en-US")
        self.assertEqual(first.as_dict(), second.as_dict())
        self.assertEqual(
            [finding.finding_id for finding in first.findings],
            ["COPY_PATTERN_001", "COPY_PATTERN_002", "COPY_PATTERN_003"],
        )

    def test_locked_copy_requires_existing_owner_change_path(self) -> None:
        result = scan_copy(
            "Say goodbye to brittle handoffs.",
            source_locale="en-US",
            content_locked=True,
        )
        self.assertEqual(result.findings[0].lock_impact, "LOCKED_CHANGE_REQUIRED")


class CopyQualityBoundaryTests(unittest.TestCase):
    def test_locale_boundary_never_treats_unknown_or_non_english_as_clean(self) -> None:
        unknown = scan_copy("Say goodbye to brittle handoffs.", source_locale=None)
        undetermined = scan_copy("Say goodbye to brittle handoffs.", source_locale="und")
        non_english = scan_copy("Say goodbye to brittle handoffs.", source_locale="es-MX")
        self.assertEqual(unknown.status, STATUS_BLOCKED)
        self.assertEqual(unknown.reason, "SOURCE_LOCALE_UNKNOWN")
        self.assertEqual(undetermined.status, STATUS_BLOCKED)
        self.assertEqual(non_english.status, STATUS_NOT_APPLICABLE)
        self.assertEqual(non_english.findings, ())
        self.assertNotIn("COPY_PATTERN_PASS", str(unknown.as_dict()))
        self.assertNotIn("COPY_PATTERN_PASS", str(non_english.as_dict()))

    def test_empty_input_is_fail_closed(self) -> None:
        result = scan_copy(" \n\t", source_locale="en-US")
        self.assertEqual(result.status, STATUS_BLOCKED)
        self.assertEqual(result.reason, "EMPTY_INPUT")
        self.assertEqual(result.findings[0].rule, "EMPTY_INPUT")
        self.assertEqual(result.findings[0].method, "DETERMINISTIC")

    def test_unicode_typography_is_normalised_deterministically(self) -> None:
        result = scan_copy(
            "It’s not just a tool, it’s a platform.\nSay\u00a0goodbye\u00a0to brittle handoffs.",
            source_locale="en-US",
        )
        rules = {finding.rule for finding in result.findings}
        self.assertIn("NEGATED_JUST_COPULA_CONTRAST", rules)
        self.assertIn("SAY_GOODBYE_TO", rules)

        compounds = scan_copy(
            "industry\u2011leading, context\u2011aware, best\u2011in\u2011class, AI\u2011powered record.",
            source_locale="en-US",
        )
        self.assertIn("HYPHENATED_COMPOUND_STACK", {finding.rule for finding in compounds.findings})

    def test_markdown_extraction_skips_non_prose_regions(self) -> None:
        markdown = """# Visible heading

```text
Say goodbye to hidden implementation details.
```

![Say goodbye to image labels](image.png)

`Say goodbye to inline code.`

~~Say goodbye to struck text.~~

[Say goodbye to linked prose](https://example.test)
"""
        result = scan_copy(markdown, source_locale="en-US", input_format="markdown")
        self.assertEqual(
            [finding.evidence for finding in result.findings],
            ["Say goodbye to"],
        )

    def test_proof_pattern_is_not_a_copy_finding(self) -> None:
        result = scan_copy("Trusted by 10,000+ customers.", source_locale="en-US")
        self.assertEqual(result.findings, ())
        self.assertEqual(len(DELEGATED_RULES), 7)
        self.assertIn("NUMERIC_PEOPLE_PROOF", DELEGATED_RULES)

    def test_rejected_broad_rules_and_legitimate_lists_stay_clean(self) -> None:
        text = (
            "Career execution, high-leverage digital and AI tools. "
            "This technical method elevates core body temperature. "
            "Curated Tools & Gear. "
            "Whether you are rebuilding your health after a setback or refusing to settle. "
            "Trusted, reliable and built to last. "
            "Inspection; repair; replacement; maintenance; review."
        )
        result = scan_copy(text, source_locale="en-US")
        self.assertEqual(result.findings, ())


class CopyQualityRepositoryContractTests(unittest.TestCase):
    def test_scanner_is_standard_library_only_and_has_no_execution_hooks(self) -> None:
        source_path = ROOT / "framework_validation" / "copy_quality.py"
        source = source_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported_modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module.split(".", 1)[0])
        self.assertEqual(imported_modules, {"dataclasses", "re", "typing", "__future__"})
        function_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        self.assertNotIn("rewrite", function_names)
        self.assertNotIn("cleanse", function_names)
        self.assertNotIn("score", function_names)

    def test_protected_projects_remain_unchanged_during_read_only_corpus_scan(self) -> None:
        sample = ROOT / "projects" / "alpha-starts-now" / "build" / "index.html"
        self.assertTrue(sample.is_file())
        with tempfile.TemporaryDirectory() as temp_dir:
            ledger = str(Path(temp_dir) / "integrity.log")
            guard = FrozenIntegrityGuard(str(ROOT), ["projects/"], ledger).snapshot()
            source_copy = sample.read_text(encoding="utf-8")
            result = scan_copy(source_copy, source_locale="en-US")
            integrity = guard.verify(record_violation=False)
        self.assertEqual(result.status, STATUS_SCANNED)
        self.assertTrue(integrity.ok, integrity.summary())
        self.assertGreater(integrity.checked_files, 0)

    def test_existing_framework_registry_gains_no_new_suite_or_gate(self) -> None:
        suites = json.loads((ROOT / "schemas" / "test-suites.json").read_text(encoding="utf-8"))
        active_suites = [suite for suite in suites["suites"] if suite["status"] == "ACTIVE"]
        self.assertEqual(len(active_suites), 13)
        framework_suite = next(suite for suite in active_suites if suite["id"] == "framework_validation")
        self.assertIn("tests.test_copy_quality", framework_suite["command"])
        self.assertIn("tests/test_copy_quality.py", framework_suite["paths"])

        gates = json.loads((ROOT / "schemas" / "gates.json").read_text(encoding="utf-8"))["gates"]
        owner_locks = [gate for gate in gates if gate["type"] == "OWNER_LOCK" and gate["status"] == "ACTIVE"]
        self.assertEqual(len(owner_locks), 5)
        self.assertFalse(any("COPY" in gate["name"] for gate in gates))
        self.assertFalse(any("SLOP" in gate["name"] for gate in gates))


if __name__ == "__main__":
    unittest.main()
