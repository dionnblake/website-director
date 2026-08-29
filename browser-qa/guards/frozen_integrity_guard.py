"""Frozen Project Integrity Guard (Website Director V2.8).

Reusable, engine-independent guard that proves a test run did not mutate any
file under a set of protected paths (by default ``projects/``, where Website
Director declares certification pilots frozen).

Design invariants (BROWSER-REGRESSION-QA-PROTOCOL.md sec 23):

* The guard hashes every protected file at ``snapshot()`` time and re-checks at
  ``verify()`` time.
* It also records ``git status --porcelain`` for the protected paths, so a *new*
  or *deleted* file is caught even though it has no baseline hash.
* ``verify()`` writes any detected drift to an append-only violation ledger the
  moment it is observed. A later ``git checkout`` / ``shutil`` restore cannot
  erase that record, so "restore afterwards" never converts a mutating run into
  a PASS.
* ``assert_unchanged()`` raises ``FrozenFixtureMutation`` -- callers must let it
  fail the suite, not swallow it.

The guard performs no network access and launches no browser. It is safe to
import from framework assertion suites and from the browser-qa runner alike.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import time
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

DEFAULT_PROTECTED_PATHS = ("projects/",)
DEFAULT_LEDGER = os.path.join("browser-qa", "evidence", "frozen-integrity-violations.log")
_IGNORED_DIR_NAMES = {".git", "node_modules", "__pycache__", ".chrome_test_profile",
                      ".pytest_cache", ".playwright", "evidence-runs"}


class FrozenFixtureMutation(AssertionError):
    """Raised when a protected (frozen) file changed during a test run."""


@dataclass
class IntegrityResult:
    ok: bool
    checked_files: int
    mutations: List[str] = field(default_factory=list)          # modified content
    additions: List[str] = field(default_factory=list)          # new files
    deletions: List[str] = field(default_factory=list)          # removed files
    git_status_changed: bool = False
    git_status_before: str = ""
    git_status_after: str = ""
    ledger_path: Optional[str] = None

    def summary(self) -> str:
        if self.ok:
            return "FROZEN_FIXTURE_INTEGRITY = PASS (%d files unchanged)" % self.checked_files
        parts = []
        if self.mutations:
            parts.append("modified=%s" % self.mutations)
        if self.additions:
            parts.append("added=%s" % self.additions)
        if self.deletions:
            parts.append("removed=%s" % self.deletions)
        if self.git_status_changed:
            parts.append("git_status_changed=True")
        return "FROZEN_FIXTURE_MUTATION = FAIL (%s)" % "; ".join(parts)


class FrozenIntegrityGuard:
    def __init__(
        self,
        repo_root: str,
        protected_paths: Iterable[str] = DEFAULT_PROTECTED_PATHS,
        ledger_path: str = DEFAULT_LEDGER,
        run_id: Optional[str] = None,
    ) -> None:
        self.repo_root = os.path.abspath(repo_root)
        self.protected_paths = [p.replace("\\", "/").rstrip("/") + "/" for p in protected_paths]
        self.ledger_path = os.path.join(self.repo_root, ledger_path)
        self.run_id = run_id or ("run-%d" % int(time.time() * 1000))
        self._baseline: Dict[str, str] = {}
        self._baseline_git: str = ""
        self._snapshotted = False

    # -- internal helpers ---------------------------------------------------
    def _iter_protected_files(self):
        for rel_root in self.protected_paths:
            abs_root = os.path.join(self.repo_root, rel_root)
            if not os.path.isdir(abs_root):
                continue
            for dirpath, dirnames, filenames in os.walk(abs_root):
                dirnames[:] = [d for d in dirnames if d not in _IGNORED_DIR_NAMES]
                for fn in filenames:
                    full = os.path.join(dirpath, fn)
                    rel = os.path.relpath(full, self.repo_root).replace("\\", "/")
                    yield rel, full

    @staticmethod
    def _hash_file(path: str) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    def _git_status(self) -> str:
        try:
            out = subprocess.check_output(
                ["git", "status", "--porcelain", "--"] + [p.rstrip("/") for p in self.protected_paths],
                cwd=self.repo_root,
                encoding="utf-8",
                stderr=subprocess.DEVNULL,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            return "<git-unavailable>"
        return "\n".join(sorted(line for line in out.splitlines() if line.strip()))

    def _append_ledger(self, result: IntegrityResult) -> None:
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        record = {
            "run_id": self.run_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "verdict": "FROZEN_FIXTURE_MUTATION",
            "protected_paths": self.protected_paths,
            "modified": result.mutations,
            "added": result.additions,
            "removed": result.deletions,
            "git_status_changed": result.git_status_changed,
        }
        with io.open(self.ledger_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
        result.ledger_path = self.ledger_path

    # -- public API -------------------------------------------------------
    def snapshot(self) -> "FrozenIntegrityGuard":
        self._baseline = {rel: self._hash_file(full) for rel, full in self._iter_protected_files()}
        self._baseline_git = self._git_status()
        self._snapshotted = True
        return self

    def verify(self, record_violation: bool = True) -> IntegrityResult:
        if not self._snapshotted:
            raise RuntimeError("FrozenIntegrityGuard.verify() called before snapshot()")

        current = {rel: self._hash_file(full) for rel, full in self._iter_protected_files()}
        baseline_keys = set(self._baseline)
        current_keys = set(current)

        mutations = sorted(k for k in (baseline_keys & current_keys) if self._baseline[k] != current[k])
        additions = sorted(current_keys - baseline_keys)
        deletions = sorted(baseline_keys - current_keys)
        git_after = self._git_status()
        git_changed = git_after != self._baseline_git

        ok = not (mutations or additions or deletions or git_changed)
        result = IntegrityResult(
            ok=ok,
            checked_files=len(current),
            mutations=mutations,
            additions=additions,
            deletions=deletions,
            git_status_changed=git_changed,
            git_status_before=self._baseline_git,
            git_status_after=git_after,
        )
        if not ok and record_violation:
            self._append_ledger(result)
        return result

    def assert_unchanged(self) -> IntegrityResult:
        result = self.verify()
        if not result.ok:
            raise FrozenFixtureMutation(result.summary())
        return result


def snapshot(repo_root: str, protected_paths: Iterable[str] = DEFAULT_PROTECTED_PATHS) -> FrozenIntegrityGuard:
    """Convenience: build a guard and take its baseline in one call."""
    return FrozenIntegrityGuard(repo_root, protected_paths).snapshot()
