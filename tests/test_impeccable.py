"""Synthetic proof for the bounded Impeccable v4.3.1 refresh.

The tests exercise the Website Director-owned scanner only. They do not call
the upstream binary, a provider, a browser, or a network endpoint, and every
filesystem probe is disposable or read-only.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from collections import Counter

from framework_validation import impeccable, validator


ROOT = Path(__file__).resolve().parents[1]
_GUARD_PATH = ROOT / "browser-qa" / "guards" / "frozen_integrity_guard.py"
_GUARD_SPEC = importlib.util.spec_from_file_location("impeccable_test_frozen_guard", _GUARD_PATH)
assert _GUARD_SPEC is not None and _GUARD_SPEC.loader is not None
_GUARD_MODULE = importlib.util.module_from_spec(_GUARD_SPEC)
sys.modules[_GUARD_SPEC.name] = _GUARD_MODULE
_GUARD_SPEC.loader.exec_module(_GUARD_MODULE)
FrozenIntegrityGuard = _GUARD_MODULE.FrozenIntegrityGuard


def rules(result: impeccable.ScanResult) -> set[str]:
    return {finding.rule for finding in result.findings}


class ImpeccableScannerTests(unittest.TestCase):
    def test_all_existing_contract_entries_have_positive_detection(self) -> None:
        cases = {
            "low-contrast": ("fixture.css", ".copy { color: #777; background: #fff; }"),
            "gray-on-color": ("fixture.css", ".copy { color: #808080; background: #ff0000; }"),
            "layout-transition": ("fixture.css", ".box { transition: all 200ms ease; }"),
            "bounce-easing": (
                "fixture.css",
                ".box { animation: enter 1s cubic-bezier(0.68, -0.55, 0.265, 1.55); }",
            ),
            "dark-glow": (
                "fixture.css",
                ".dark { background: #0f172a; box-shadow: 0 0 24px #8b5cf6; }",
            ),
            "touch-target-undersized": (
                "fixture.css",
                ".button { width: 32px; height: 32px; }",
            ),
            "ai-color-palette": (
                "fixture.css",
                ".hero { background: linear-gradient(#6366f1, #06b6d4); }",
            ),
            "hero-eyebrow-chip": (
                "fixture.html",
                '<span class="eyebrow">Announcing</span><h1>Useful work</h1>',
            ),
            "icon-tile-stack": (
                "fixture.html",
                """
                <div class="feature-card"><div class="icon-tile">A</div></div>
                <div class="feature-card"><div class="icon-tile">B</div></div>
                <div class="feature-card"><div class="icon-tile">C</div></div>
                """,
            ),
            "radial-halo": (
                "fixture.css",
                ".hero { background: radial-gradient(circle, #8b5cf6, transparent); filter: blur(8px); }",
            ),
            "side-tab": (
                "fixture.css",
                ".card { border-left: 3px solid #f00; border-radius: 12px; }",
            ),
            "border-accent-on-rounded": (
                "fixture.css",
                ".card { border-left: 3px solid #f00; border-radius: 12px; }",
            ),
            "pulsing-dot": (
                "fixture.css",
                ".dot { animation: pulse 2s infinite; }",
            ),
            "marquee": (
                "fixture.css",
                ".marquee { animation: marquee 10s linear infinite; }",
            ),
            "shape-assembled-illustration": (
                "fixture.css",
                """
                .shape-a { position: absolute; border-radius: 50%; }
                .shape-b { position: absolute; border-radius: 50%; }
                .shape-c { position: absolute; border-radius: 50%; }
                """,
            ),
            "monotonous-spacing": (
                "fixture.css",
                """
                section.one { padding: 64px; }
                section.two { padding: 64px; }
                section.three { padding: 64px; }
                section.four { padding: 64px; }
                """,
            ),
            "gradient-text": (
                "fixture.css",
                """
                .title {
                  background: linear-gradient(#111, #222);
                  -webkit-background-clip: text;
                  color: transparent;
                }
                """,
            ),
            "kicker-above-heading": (
                "fixture.html",
                """
                <span class="kicker">One</span><h2>First</h2>
                <span class="kicker">Two</span><h2>Second</h2>
                """,
            ),
            "italic-serif-display": (
                "fixture.html",
                "<h1>Make <em>better</em> work</h1>",
            ),
        }
        self.assertEqual(len(impeccable.EXISTING_RULE_ENTRIES), 18)
        for rule, (path, source) in cases.items():
            with self.subTest(rule=rule):
                self.assertIn(rule, rules(impeccable.scan_sources({path: source})))

    def test_existing_rules_have_clean_negative_controls(self) -> None:
        cases = {
            "low-contrast": ("fixture.css", ".copy { color: #111; background: #fff; }"),
            "gray-on-color": ("fixture.css", ".copy { color: #e5e7eb; background: #f00; }"),
            "layout-transition": ("fixture.css", ".box { transition: transform 200ms ease; }"),
            "bounce-easing": ("fixture.css", ".box { animation: enter 1s ease-out; }"),
            "dark-glow": ("fixture.css", ".dark { background: #0f172a; box-shadow: 0 8px 24px #000; }"),
            "touch-target-undersized": ("fixture.css", ".button { min-width: 44px; min-height: 44px; }"),
            "ai-color-palette": ("fixture.css", ".hero { background: linear-gradient(#123456, #234567); }"),
            "hero-eyebrow-chip": ("fixture.html", "<h1>Useful work</h1><p>Context</p>"),
            "icon-tile-stack": ("fixture.html", '<div class="feature-icon">A</div><div class="feature-icon">B</div>'),
            "radial-halo": ("fixture.css", ".hero { background: #111; }"),
            "side-tab": ("fixture.css", ".status-card { border-left: 3px solid #0a0; border-radius: 12px; }"),
            "border-accent-on-rounded": ("fixture.css", ".status-card { border-left: 3px solid #0a0; border-radius: 12px; }"),
            "pulsing-dot": ("fixture.css", ".live-dot { animation: pulse 2s infinite; }"),
            "marquee": ("fixture.css", ".marquee { animation: marquee 10s linear; }"),
            "shape-assembled-illustration": ("fixture.css", ".shape { position: relative; }"),
            "monotonous-spacing": (
                "fixture.css",
                "section.one { padding: 64px; } section.two { padding: 48px; } section.three { padding: 64px; } section.four { padding: 64px; }",
            ),
            "gradient-text": ("fixture.css", ".title { color: #111; background: none; }"),
            "kicker-above-heading": ("fixture.html", '<span class="kicker">One</span><h2>First</h2>'),
            "italic-serif-display": ("fixture.html", "<h1>Make <strong>better</strong> work</h1>"),
        }
        for rule, (path, source) in cases.items():
            with self.subTest(rule=rule):
                self.assertNotIn(rule, rules(impeccable.scan_sources({path: source})))

    def test_selected_v431_rules_have_positive_and_negative_controls(self) -> None:
        positives = {
            "flat-type-hierarchy": (
                "fixture.css",
                "h1 { font-size: 24px; } h2 { font-size: 22px; } p { font-size: 20px; }",
            ),
            "organic-clip-path": (
                "fixture.css",
                ".cutout { clip-path: polygon(13% 4%, 26% 8%, 39% 2%, 52% 9%, 65% 3%, 78% 7%, 86% 11%, 93% 6%, 17% 14%, 44% 18%); }",
            ),
            "buried-raster": (
                "fixture.css",
                ".hero { background: linear-gradient(rgba(0,0,0,.98), rgba(0,0,0,.98)), url(hero.jpg); }",
            ),
            "extreme-negative-tracking": (
                "fixture.css",
                "h1 { letter-spacing: -0.1em; }",
            ),
            "broken-image": ("fixture.html", '<img alt="Missing" src="placeholder.png">'),
            "justified-text": ("fixture.css", ".copy { text-align: justify; }"),
            "tiny-text": ("fixture.css", ".copy { font-size: 11px; }"),
            "undersized-ui-text": ("fixture.css", ".button { font-size: 10px; }"),
            "repeating-stripes-gradient": (
                "fixture.css",
                ".texture { background: repeating-linear-gradient(45deg, #111 0 2px, #222 2px 4px); }",
            ),
        }
        negatives = {
            "flat-type-hierarchy": ("fixture.css", "h1 { font-size: 56px; } h2 { font-size: 32px; } p { font-size: 16px; }"),
            "organic-clip-path": ("fixture.css", ".cutout { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }"),
            "buried-raster": ("fixture.css", ".hero { background: url(hero.jpg); }"),
            "extreme-negative-tracking": ("fixture.css", "h1 { letter-spacing: -0.04em; }"),
            "broken-image": ("fixture.html", '<img alt="Real" src="/assets/hero.webp">'),
            "justified-text": ("fixture.css", ".copy { text-align: left; }"),
            "tiny-text": ("fixture.css", ".copy { font-size: 16px; }"),
            "undersized-ui-text": ("fixture.css", ".button { font-size: 14px; }"),
            "repeating-stripes-gradient": ("fixture.css", ".texture { background: linear-gradient(#111, #222); }"),
        }
        self.assertEqual(set(positives), set(impeccable.ADOPTED_NEW_RULE_IDS))
        for rule, (path, source) in positives.items():
            with self.subTest(positive=rule):
                self.assertIn(rule, rules(impeccable.scan_sources({path: source})))
        for rule, (path, source) in negatives.items():
            with self.subTest(negative=rule):
                self.assertNotIn(rule, rules(impeccable.scan_sources({path: source})))

    def test_contextual_false_positive_controls_remain_clean(self) -> None:
        cases = {
            "transparent-raster-tint": (
                "fixture.css",
                ".hero { background: linear-gradient(rgba(0,0,0,.5), transparent), url(hero.jpg); }",
                "buried-raster",
            ),
            "raster-on-top": (
                "fixture.css",
                ".hero { background: url(hero.jpg), linear-gradient(#111, #222); }",
                "buried-raster",
            ),
            "simple-clip": (
                "fixture.css",
                ".cutout { clip-path: polygon(0 0, 20% 4%, 40% 0, 60% 8%, 80% 2%, 100% 0); }",
                "organic-clip-path",
            ),
            "safe-justification": (
                "fixture.css",
                ".copy { text-align: justify; hyphens: auto; }",
                "justified-text",
            ),
            "square-accent": (
                "fixture.css",
                ".card { border-left: 3px solid #f00; border-radius: 0; }",
                "side-tab",
            ),
            "normalized-path-collision": (
                "fixture/page.css",
                ".card { color: #111; }",
                "duplicate source path after normalization",
            ),
        }
        for name, (path, source, rule) in cases.items():
            with self.subTest(control=name):
                if name == "normalized-path-collision":
                    with self.assertRaisesRegex(ValueError, rule):
                        impeccable.scan_sources({path: source, "fixture\\page.css": source})
                else:
                    self.assertNotIn(rule, rules(impeccable.scan_sources({path: source})))

    def test_findings_use_normalized_schema_and_method_taxonomy(self) -> None:
        result = impeccable.scan_sources(
            {
                "src\\page.css": ".card { border-left: 3px solid #f00; border-radius: 12px; }",
                "src/page.html": "<h1>Title</h1><h3>Skipped</h3>",
            }
        )
        self.assertEqual(result.files, ("src/page.css", "src/page.html"))
        self.assertFalse(result.passed)
        expected_fields = {
            "FINDING_ID",
            "SOURCE",
            "METHOD",
            "RULE",
            "LOCATION",
            "SEVERITY",
            "EVIDENCE",
            "REMEDIATION",
            "LOCK_IMPACT",
        }
        for finding in result.findings:
            self.assertEqual(set(finding.as_dict()), expected_fields)
            self.assertEqual(finding.source, impeccable.SOURCE)
            self.assertIn(finding.method, impeccable.VALID_METHODS)
            self.assertIn(finding.severity, impeccable.VALID_SEVERITIES)
            self.assertNotIn("\\", finding.location)

    def test_contextual_override_requires_an_explicit_locked_direction(self) -> None:
        source = {"fixture.html": '<span class="eyebrow">Editorial</span><h1>Title</h1>'}
        unlocked = impeccable.scan_sources(source, {"authorized_heuristics": ["hero-eyebrow-chip"]})
        self.assertFalse(unlocked.passed)
        self.assertEqual(unlocked.findings[0].lock_impact, "NONE")

        locked = impeccable.scan_sources(
            source,
            {
                "design_direction_locked": True,
                "authorized_heuristics": ["hero-eyebrow-chip"],
            },
        )
        self.assertTrue(locked.passed)
        self.assertEqual(locked.authorized_finding_ids, ("HEUR-001",))
        self.assertIn("AUTHORIZED_BY_LOCK", locked.findings[0].remediation)

    def test_locked_change_is_reported_without_mutating_owner_locks(self) -> None:
        source = {"fixture.css": ".box { transition: all 200ms ease; }"}
        lock_context = {"locked_rules": {"layout-transition": "motion_direction_locked"}}
        before = tuple(validator.CANONICAL_LOCKS)
        result = impeccable.scan_sources(source, lock_context)
        after = tuple(validator.CANONICAL_LOCKS)
        self.assertEqual(before, after)
        self.assertEqual(result.findings[0].lock_impact, "LOCKED_CHANGE_REQUIRED")
        self.assertFalse(result.passed)

    def test_browser_and_accessibility_runtime_ownership_is_not_duplicated(self) -> None:
        result = impeccable.scan_sources(
            {
                "fixture.html": "<script>throw new Error('runtime');</script><h1>Title</h1><h3>Skipped</h3>",
                "fixture.css": ".viewport { overflow: hidden; }",
            }
        )
        self.assertNotIn("script-error", rules(result))
        self.assertNotIn("skipped-heading", rules(result))
        self.assertNotIn("text-occlusion", rules(result))
        self.assertNotIn("first-viewport-column-overflow", rules(result))
        self.assertNotIn("body-text-viewport-edge", rules(result))
        self.assertTrue(impeccable.RUNTIME_DELEGATED_RULE_IDS.isdisjoint(impeccable.ADOPTED_RULE_IDS))
        protocol = (ROOT / "IMPECCABLE-ENGINE-PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("Browser QA", protocol)
        self.assertIn("ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md", protocol)

    def test_skipped_heading_is_owned_by_accessibility_and_not_emitted(self) -> None:
        result = impeccable.scan_sources(
            {"fixture.html": "<h1>Title</h1><h3>Skipped</h3>"}
        )
        self.assertNotIn("skipped-heading", rules(result))
        protocol = (ROOT / "IMPECCABLE-ENGINE-PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn(
            "| skipped-heading | STATIC_HTML_DOM | E | accessibility |",
            protocol,
        )
        self.assertIn("Browser QA executes the canonical heading-order assertion", protocol)
        accessibility = (ROOT / "ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("logical heading hierarchy with no skipped levels", accessibility)
        browser_catalog = (ROOT / "browser-qa" / "assertions" / "catalog.py").read_text(encoding="utf-8")
        self.assertIn("heading-order", browser_catalog)

    def test_broken_image_is_source_precheck_only_and_runtime_owned_by_browser_qa(self) -> None:
        result = impeccable.scan_sources(
            {"fixture.html": '<img alt="Missing" src="placeholder.png">'}
        )
        self.assertIn("broken-image", rules(result))
        finding = next(item for item in result.findings if item.rule == "broken-image")
        self.assertEqual(finding.method, impeccable.DETERMINISTIC)
        self.assertIn("placeholder", finding.evidence)
        self.assertNotIn("broken-image", impeccable.RUNTIME_DELEGATED_RULE_IDS)
        protocol = (ROOT / "IMPECCABLE-ENGINE-PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn(
            "source-level precheck for an obvious missing, empty, or placeholder image",
            protocol,
        )
        self.assertIn(
            "Browser QA owns rendered/runtime asset loading and",
            protocol,
        )
        self.assertIn("cannot substitute for Browser QA\nasset-integrity PASS", protocol)
        browser_protocol = (ROOT / "BROWSER-REGRESSION-QA-PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("image response success", browser_protocol)
        self.assertIn("non-zero rendered dimensions", browser_protocol)
        self.assertIn("no accidental placeholder images", browser_protocol)

    def test_official_engine_unavailable_corrupt_and_network_free_paths_fail_closed(self) -> None:
        unavailable = impeccable.assess_official_engine_artifact(
            None,
            "0" * 64,
        )
        self.assertEqual(unavailable["status"], "BLOCKED")
        with tempfile.NamedTemporaryFile("wb", delete=False) as handle:
            handle.write(b"corrupt")
            artifact = Path(handle.name)
        try:
            corrupt = impeccable.assess_official_engine_artifact(
                artifact,
                "0" * 64,
            )
            self.assertEqual(corrupt["status"], "BLOCKED")
            verified_identity = impeccable.assess_official_engine_artifact(
                artifact,
                hashlib.sha256(b"corrupt").hexdigest(),
            )
            self.assertEqual(verified_identity["status"], "IDENTITY_VERIFIED_NOT_EXECUTED")
        finally:
            artifact.unlink(missing_ok=True)
        result = impeccable.scan_sources({"fixture.css": ".ok { color: #111; background: #fff; }"})
        self.assertEqual(result.engine_decision, "CURATED_IMPLEMENTATION_RETAINED")
        self.assertEqual(result.external_engine_status, "NOT_APPLICABLE")

    def test_windows_and_posix_paths_are_normalized_and_scan_path_is_read_only(self) -> None:
        source = {"src\\components\\page.css": ".button { width: 32px; height: 32px; }"}
        result = impeccable.scan_sources(source)
        self.assertEqual(result.files, ("src/components/page.css",))
        self.assertTrue(result.findings[0].location.startswith("src/components/page.css:"))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "page.css").write_text(
                ".button { width: 32px; height: 32px; }",
                encoding="utf-8",
            )
            before = (root / "src" / "page.css").read_bytes()
            scanned = impeccable.scan_path(root)
            after = (root / "src" / "page.css").read_bytes()
            self.assertIn("touch-target-undersized", rules(scanned))
            self.assertEqual(before, after)

    def test_explicit_build_root_is_scanned_and_finds_a_defect(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            build_root = Path(directory) / "build"
            build_root.mkdir()
            (build_root / "index.html").write_text(
                '<main><img alt="Hero" src=""></main>',
                encoding="utf-8",
            )
            result = impeccable.scan_path(build_root)
            self.assertEqual(result.files, ("index.html",))
            self.assertIn("broken-image", rules(result))
            self.assertFalse(result.passed)

    def test_explicit_build_root_records_clean_html_and_css_and_may_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            build_root = Path(directory) / "build"
            build_root.mkdir()
            (build_root / "index.html").write_text(
                "<main><h1>Useful work</h1></main>",
                encoding="utf-8",
            )
            (build_root / "styles.css").write_text(
                ".copy { color: #111; background: #fff; }",
                encoding="utf-8",
            )
            result = impeccable.scan_path(build_root)
            self.assertEqual(result.files, ("index.html", "styles.css"))
            self.assertEqual(result.findings, ())
            self.assertTrue(result.passed)

    def test_nested_dependency_cache_and_generated_directories_remain_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src" / "page.html").write_text(
                "<main><h1>Useful work</h1></main>",
                encoding="utf-8",
            )
            for ignored in (".git", "node_modules", ".pytest_cache", "dist", "build", "coverage"):
                folder = root / ignored
                folder.mkdir()
                (folder / "ignored.html").write_text(
                    '<img alt="Missing" src="">',
                    encoding="utf-8",
                )
            result = impeccable.scan_path(root)
            self.assertEqual(result.files, ("src/page.html",))
            self.assertNotIn("broken-image", rules(result))

    def test_empty_directory_cannot_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "no supported source files to scan"):
                impeccable.scan_path(directory)

    def test_directory_with_only_unsupported_or_binary_files_cannot_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "bundle.bin").write_bytes(bytes((0, 1, 2)))
            with self.assertRaisesRegex(ValueError, "no supported source files to scan"):
                impeccable.scan_path(directory)

    def test_empty_source_map_cannot_pass(self) -> None:
        with self.assertRaisesRegex(ValueError, "no supported source files to scan"):
            impeccable.scan_sources({})

    def test_unsupported_only_source_map_cannot_pass(self) -> None:
        with self.assertRaisesRegex(ValueError, "no supported source files to scan"):
            impeccable.scan_sources({"bundle.bin": "binary placeholder"})

    def test_windows_and_posix_scan_roots_are_equivalent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "dist"
            root.mkdir()
            (root / "index.html").write_text(
                '<main><img alt="Missing" src="placeholder.png"></main>',
                encoding="utf-8",
            )
            windows_result = impeccable.scan_path(str(root))
            posix_result = impeccable.scan_path(str(root).replace("\\", "/"))
            self.assertEqual(windows_result.files, posix_result.files)
            self.assertEqual(
                [(item.rule, item.location, item.evidence) for item in windows_result.findings],
                [(item.rule, item.location, item.evidence) for item in posix_result.findings],
            )

    def test_protected_projects_remain_unchanged_during_scan(self) -> None:
        with tempfile.NamedTemporaryFile(delete=False) as ledger:
            ledger_path = Path(ledger.name)
        ledger_path.unlink(missing_ok=True)
        guard = FrozenIntegrityGuard(
            str(ROOT),
            protected_paths=("projects/",),
            ledger_path=str(ledger_path),
            run_id="impeccable-v431-test",
        ).snapshot()
        try:
            impeccable.scan_sources(
                {
                    "fixture.css": ".hero { background: linear-gradient(#6366f1, #06b6d4); }",
                    "fixture.html": "<h1>Title</h1><h3>Skipped</h3>",
                }
            )
            result = guard.verify(record_violation=False)
            self.assertTrue(result.ok, result.summary())
        finally:
            ledger_path.unlink(missing_ok=True)

    def test_historical_framework_profile_and_five_lock_contract_are_untouched(self) -> None:
        version = json.loads((ROOT / "framework-version.json").read_text(encoding="utf-8"))
        self.assertEqual(version["version"], "2.15.0")
        profile = json.loads((ROOT / "templates" / "site-profile.json").read_text(encoding="utf-8"))
        self.assertEqual(tuple(profile["locks"]), validator.CANONICAL_LOCKS)
        self.assertEqual(len(validator.CANONICAL_LOCKS), 5)
        self.assertEqual(impeccable.UPSTREAM_TARGET_RULE_COUNT, 61)

    def test_protocol_matrix_is_complete_and_uses_the_requested_dispositions(self) -> None:
        protocol = (ROOT / "IMPECCABLE-ENGINE-PROTOCOL.md").read_text(encoding="utf-8")
        start = protocol.index("| Upstream ID | Upstream method class")
        end = protocol.index("### 5.1", start)
        rows = []
        for line in protocol[start:end].splitlines():
            if not line.startswith("| "):
                continue
            columns = [column.strip() for column in line.split("|")[1:-1]]
            if len(columns) == 5 and columns[2] in set("ABCDEFGHIJ"):
                rows.append(columns)
        self.assertEqual(len(rows), 61)
        self.assertEqual(len({row[0] for row in rows}), 61)
        self.assertEqual(
            Counter(row[2] for row in rows),
            Counter({"A": 18, "B": 5, "C": 4, "D": 8, "E": 1, "F": 7, "G": 14, "H": 0, "I": 0, "J": 4}),
        )
        disposition = {row[0]: row[2] for row in rows}
        self.assertEqual(
            {rule for rule, code in disposition.items() if code == "D"},
            set(impeccable.RUNTIME_DELEGATED_RULE_IDS),
        )
        self.assertEqual(
            set(impeccable.ADOPTED_NEW_STATIC_RULE_IDS),
            {rule for rule, code in disposition.items() if code == "B"},
        )
        self.assertEqual(
            set(impeccable.ADOPTED_NEW_HEURISTIC_RULE_IDS),
            {rule for rule, code in disposition.items() if code == "C"},
        )


if __name__ == "__main__":
    unittest.main()
