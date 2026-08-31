"""Manifest-driven Browser & Regression QA runner (Website Director V2.15).

    python browser-qa/runner.py --plan <project>/browser-qa-manifest.json \
        --engine simulation --evidence <project>/evidence/browser-qa

Reads a browser-qa manifest, drives the selected BROWSER_QA_ENGINE across the
route x viewport x browser matrix, runs the requirement-traced assertion
catalogue, applies the bounded flake policy, snapshots frozen-project integrity
around the whole run, and writes a machine-readable evidence manifest plus a
human-readable summary. It never mutates ``site-profile.json`` -- it prints the
``browser_qa{}`` block the operator should apply.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter
from typing import Any, Dict, List

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from assertions import evaluate  # noqa: E402
from engine.base import BLOCKED, FAIL, FLAKY, NOT_APPLICABLE, PASS, load_engine  # noqa: E402
from guards.frozen_integrity_guard import FrozenIntegrityGuard  # noqa: E402

DEFAULT_VIEWPORTS = {
    "smoke": [390, 768, 1440],
    "regression": [360, 375, 390, 428, 768, 1024, 1280, 1440],
}


def _load(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _matrix(plan: Dict[str, Any], mode: str) -> List[Dict[str, Any]]:
    vp_cfg = plan.get("viewports", {})
    viewports = vp_cfg.get(mode) or DEFAULT_VIEWPORTS[mode]
    browsers = plan.get("browsers", {}).get(mode, ["chromium"])
    if mode == "smoke":
        browsers = plan.get("browsers", {}).get("smoke", ["chromium"])
    jobs = []
    for route in plan.get("routes", []):
        path = route.get("path") or route.get("route")
        route_vps = route.get("viewports") or viewports
        for vp in route_vps:
            for br in browsers:
                jobs.append({"route": path, "viewport": vp, "browser": br,
                             "reduced_motion": False, "interactions": route.get("interactions")})
            if route.get("reduced_motion") or plan.get("reduced_motion_all_routes"):
                jobs.append({"route": path, "viewport": vp, "browser": browsers[0],
                             "reduced_motion": True, "interactions": route.get("interactions")})
    return jobs


def run(plan_path: str, engine_name: str, evidence_dir: str, mode: str,
        retries: int, project_root: str) -> int:
    plan = _load(plan_path)
    project_root = os.path.abspath(project_root or os.path.dirname(plan_path))
    repo_root = plan.get("repo_root") or _find_repo_root(project_root)

    guard = FrozenIntegrityGuard(repo_root, plan.get("protected_paths", ["projects/"]),
                                 run_id="browser-qa-%d" % int(time.time()))
    guard.snapshot()

    engine_config = dict(plan.get("engine_config", {}))
    # Runtime specialist checks consume their canonical plan blocks through the
    # same engine. They do not create a second runner or a second state owner.
    if plan.get("localization") and "localization" not in engine_config:
        engine_config["localization"] = plan["localization"]
    if plan.get("application") and "application" not in engine_config:
        engine_config["application"] = plan["application"]
    engine = load_engine(engine_name, project_root, engine_config)
    run_id = "bqa-%s" % time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    started = time.time()
    findings_json: List[Dict[str, Any]] = []
    verdict_counts: Counter = Counter()
    flaky_tests: List[str] = []
    blocked_reason = None

    try:
        available = engine.available()
    except Exception as exc:  # noqa: BLE001
        blocked_reason = _blocked_reason("engine.available()", exc)
    else:
        if not available:
            blocked_reason = "BLOCKED_ENVIRONMENT: BROWSER_QA_ENGINE '%s' unavailable in this environment" % engine_name

    if blocked_reason is None:
        try:
            engine.start()
        except Exception as exc:  # noqa: BLE001
            blocked_reason = _blocked_reason("engine.start()", exc)

    jobs = _matrix(plan, mode)
    try:
        if blocked_reason is None:
            for job in jobs:
                if blocked_reason is not None:
                    _append_blocked_job(findings_json, verdict_counts, job, blocked_reason)
                    continue
                try:
                    job_blocked_reason = _run_job(
                        engine, plan, job, retries, findings_json, verdict_counts, flaky_tests)
                except Exception as exc:  # noqa: BLE001
                    job_blocked_reason = _blocked_reason("browser QA job", exc)
                    _append_blocked_job(findings_json, verdict_counts, job, job_blocked_reason,
                                        check_id="engine.runtime")
                if job_blocked_reason is not None:
                    blocked_reason = job_blocked_reason
        else:
            for job in jobs:
                _append_blocked_job(findings_json, verdict_counts, job, blocked_reason)
    finally:
        try:
            engine.stop()
        except Exception as exc:  # noqa: BLE001
            stop_reason = _blocked_reason("engine.stop()", exc)
            blocked_reason = "%s; %s" % (blocked_reason, stop_reason) if blocked_reason else stop_reason

    integrity = guard.verify()
    is_production = plan.get("environment") == "production" or \
        any(str(r.get("path", "")).startswith("https://") for r in plan.get("routes", []))

    passed = (verdict_counts[FAIL] == 0 and verdict_counts[BLOCKED] == 0
              and verdict_counts[FLAKY] == 0 and integrity.ok and blocked_reason is None)
    manifest = {
        "run_id": run_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_sha": _git_sha(repo_root),
        "environment": "production" if is_production else "local",
        "engine": engine.name,
        "engine_real_browser": engine.supports_real_browser,
        "mode": mode,
        "matrix_jobs": len(jobs),
        "duration_s": round(time.time() - started, 2),
        "verdict_counts": dict(verdict_counts),
        "flaky_tests": flaky_tests,
        "frozen_fixture_integrity": "PASS" if integrity.ok else "FAIL",
        "frozen_integrity_detail": integrity.summary(),
        "blocked_reason": blocked_reason,
        "findings": findings_json,
        "overall": ("PASS" if passed else "BLOCKED" if blocked_reason
                    else "FLAKY" if verdict_counts[FLAKY] else "FAIL"),
    }

    os.makedirs(evidence_dir, exist_ok=True)
    man_path = os.path.join(evidence_dir, "%s.evidence.json" % run_id)
    with open(man_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    _write_summary(os.path.join(evidence_dir, "%s.summary.md" % run_id), manifest)

    state = _propose_state(manifest, engine, is_production, plan)
    print(json.dumps(manifest["verdict_counts"], indent=2))
    print("\nfrozen_fixture_integrity:", manifest["frozen_fixture_integrity"], "-", integrity.summary())
    print("evidence:", man_path)
    print("\n--- proposed site-profile.json browser_qa{} (apply manually) ---")
    print(json.dumps({"browser_qa": state}, indent=2))
    if plan.get("accessibility"):
        a11y_state = _propose_a11y_state(manifest, engine, is_production)
        print("\n--- proposed site-profile.json accessibility{} verification fields (apply manually) ---")
        print(json.dumps({"accessibility": a11y_state}, indent=2))
    return 0 if passed else 1


def _propose_a11y_state(manifest, engine, is_production):
    rel = [f for f in manifest["findings"] if f["check_id"].startswith("a11y.")]
    engine_f = [f for f in rel if f["check_id"] in ("a11y.engine", "a11y.engine-violations")]
    sr_f = [f for f in rel if f["check_id"] == "a11y.screen-reader"]
    mk_f = [f for f in rel if f["check_id"] == "a11y.manual-keyboard"]
    auto_only = [f for f in rel if f["check_id"] not in ("a11y.screen-reader", "a11y.manual-keyboard")]
    real = engine.supports_real_browser
    automated_ok = bool(auto_only) and all(f["verdict"] in (PASS, NOT_APPLICABLE, FLAKY) for f in auto_only)
    engine_blocked = any(f["verdict"] == BLOCKED and "ENGINE_UNAVAILABLE" in f.get("detail", "")
                         for f in engine_f)
    manual_keyboard_pass = bool(mk_f) and all(f["verdict"] == PASS for f in mk_f)
    manual_keyboard_fail = any(f["verdict"] == FAIL for f in mk_f)
    sr_blocked = any(f["verdict"] == BLOCKED for f in sr_f)
    sr_done = any(f["verdict"] == PASS for f in sr_f)
    gaps = [f["check_id"] for f in rel if f["verdict"] in (FAIL, BLOCKED)]
    return {
        "automated_engine": next((f["title"].split("(")[-1].split(")")[0]
                                  for f in engine_f if "(" in f["title"]), None),
        "automated_verified": bool(automated_ok and real and not engine_blocked),
        "manual_verified": bool(manual_keyboard_pass and not manual_keyboard_fail),
        "screen_reader_verified": bool(sr_done and not sr_blocked),
        "production_verified": bool(automated_ok and real and is_production and manual_keyboard_pass),
        "known_gaps": gaps,
        "blocked_reason": ("BLOCKED_ACCESSIBILITY_ENGINE_UNAVAILABLE" if engine_blocked
                           else "BLOCKED_SCREEN_READER_ENVIRONMENT" if sr_blocked else None),
        "_note": ("Full PASS requires automated checks PASS AND the manual keyboard/zoom scope "
                  "MANUAL_VERIFIED AND screen-reader smoke COMPLETED or an explicit recorded gap."),
    }


def _run_job(engine, plan, job, retries, findings_json, verdict_counts, flaky_tests):
    """Bounded flake policy (protocol sec 21): FAIL then PASS on retry == FLAKY,
    never an unconditional PASS. A check that fails every attempt is FAIL."""
    attempts: List[Dict[str, Any]] = []
    for attempt in range(retries + 1):
        try:
            obs = engine.observe(job["route"], job["viewport"],
                                 reduced_motion=job["reduced_motion"], browser=job["browser"],
                                 interactions=job.get("interactions"))
        except Exception as exc:  # noqa: BLE001
            detail = _blocked_reason("engine.observe()", exc)
            rec = _mk("engine.observe", "Browser observation is available", BLOCKED,
                       "BROWSER_QA_PLAN", job, detail=detail)
            rec["attempts"] = attempt + 1
            verdict_counts[BLOCKED] += 1
            findings_json.append(rec)
            return detail
        fx_flaky = (obs.raw or {}).get("flaky")
        if fx_flaky:
            phase = "first_run" if attempt == 0 else "retry"
            verdict = fx_flaky.get(phase, PASS)
            results = {"fixture.flaky-probe": _mk("fixture.flaky-probe", "Flaky-probe fixture",
                                                  verdict, "BROWSER_QA_PLAN", job,
                                                  detail="phase=%s" % phase)}
        else:
            results = {f.check_id: _to_dict(f, job) for f in evaluate(obs, plan)}
        attempts.append(results)
        if all(r["verdict"] in (PASS, NOT_APPLICABLE) for r in results.values()):
            break

    first, final = attempts[0], attempts[-1]
    for cid, rec in final.items():
        v = rec["verdict"]
        first_ok = first.get(cid, {}).get("verdict") in (PASS, NOT_APPLICABLE)
        final_ok = v in (PASS, NOT_APPLICABLE)
        if len(attempts) > 1 and not first_ok and final_ok:
            v = FLAKY
            flaky_tests.append("%s @ %s:%d%s (recovered on retry %d)"
                               % (cid, job["route"], job["viewport"],
                                  " rm" if job["reduced_motion"] else "", len(attempts) - 1))
        rec["verdict"] = v
        rec["attempts"] = len(attempts)
        verdict_counts[v] += 1
        findings_json.append(rec)
    return None


def _blocked_reason(operation: str, exc: Exception) -> str:
    detail = str(exc).strip().splitlines()[0] if str(exc).strip() else exc.__class__.__name__
    return "BLOCKED_ENVIRONMENT: %s failed: %s" % (operation, detail)


def _append_blocked_job(findings_json, verdict_counts, job, detail, check_id="engine.availability"):
    verdict_counts[BLOCKED] += 1
    findings_json.append({"check_id": check_id, "verdict": BLOCKED,
                          "route": job["route"], "viewport": job["viewport"],
                          "browser": job["browser"],
                          "reduced_motion": job.get("reduced_motion", False),
                          "requirement_source": "BROWSER_QA_PLAN", "detail": detail})


def _to_dict(f, job):
    return {"check_id": f.check_id, "title": f.title, "verdict": f.verdict,
            "requirement_source": f.requirement_source, "owning_spec": f.owning_spec,
            "route": f.route, "viewport": f.viewport, "browser": f.browser,
            "reduced_motion": job["reduced_motion"], "method": f.method,
            "detail": f.detail, "evidence": f.evidence}


def _mk(cid, title, verdict, source, job, detail=""):
    return {"check_id": cid, "title": title, "verdict": verdict, "requirement_source": source,
            "owning_spec": "", "route": job["route"], "viewport": job["viewport"],
            "browser": job["browser"], "reduced_motion": job["reduced_motion"],
            "method": "BROWSER_EXECUTED", "detail": detail, "evidence": {}}


def _propose_state(manifest, engine, is_production, plan):
    counts = manifest["verdict_counts"]
    ok = manifest["overall"] == "PASS"

    def cat(src):
        rel = [f for f in manifest["findings"] if f["requirement_source"] == src]
        if not rel:
            return None
        return all(f["verdict"] in (PASS, NOT_APPLICABLE, FLAKY) for f in rel)

    return {
        "complete": ok,
        "engine": engine.name if engine.supports_real_browser else "%s (non-browser adapter)" % engine.name,
        "plan_ready": True,
        "smoke_passed": ok,
        "responsive_passed": _group_ok(manifest, "responsive."),
        "console_passed": _group_ok(manifest, "console."),
        "network_passed": _group_ok(manifest, "network."),
        "form_passed": _group_ok_or_none(manifest, "form."),
        "measurement_passed": cat("MEASUREMENT_PLAN"),
        "security_privacy_passed": cat("SECURITY_PRIVACY_REVIEW"),
        "reduced_motion_passed": _group_ok_or_none(manifest, "motion."),
        "keyboard_smoke_passed": _group_ok_or_none(manifest, "keyboard."),
        "visual_regression_status": _visual_status(manifest),
        "frozen_fixture_integrity": manifest["frozen_fixture_integrity"],
        "flaky_tests": manifest["flaky_tests"],
        "blocked_reason": manifest["blocked_reason"],
        "implementation_verified": bool(ok and engine.supports_real_browser and not is_production),
        "production_verified": bool(ok and engine.supports_real_browser and is_production),
        "exception": {"applied": False, "reason": None},
    }


def _group_ok(manifest, prefix):
    rel = [f for f in manifest["findings"] if f["check_id"].startswith(prefix)]
    return bool(rel) and all(f["verdict"] in (PASS, NOT_APPLICABLE, FLAKY) for f in rel)


def _group_ok_or_none(manifest, prefix):
    rel = [f for f in manifest["findings"] if f["check_id"].startswith(prefix)]
    if not rel:
        return None
    return all(f["verdict"] in (PASS, NOT_APPLICABLE, FLAKY) for f in rel)


def _visual_status(manifest):
    rel = [f for f in manifest["findings"] if f["check_id"].startswith("visual.")]
    if not rel:
        return "NOT_RUN"
    if any(f["verdict"] == BLOCKED for f in rel):
        return "BASELINE_MISSING"
    if any(f["verdict"] == FAIL for f in rel):
        return "DIFF_DETECTED"
    return "MATCH"


def _write_summary(path, m):
    lines = ["# Browser & Regression QA — %s" % m["run_id"], "",
             "- environment: **%s**" % m["environment"],
             "- engine: **%s** (real browser: %s)" % (m["engine"], m["engine_real_browser"]),
             "- git SHA: `%s`" % m["git_sha"],
             "- matrix jobs: %d | duration: %ss" % (m["matrix_jobs"], m["duration_s"]),
             "- frozen fixture integrity: **%s** — %s" % (m["frozen_fixture_integrity"],
                                                          m["frozen_integrity_detail"]),
             "- verdicts: %s" % m["verdict_counts"], "",
             "## Failures / Blocked", ""]
    bad = [f for f in m["findings"] if f["verdict"] in (FAIL, BLOCKED)]
    if not bad:
        lines.append("_none_")
    for f in bad:
        lines.append("- **%s** `%s` @ %s:%s — %s _(owner: %s)_"
                     % (f["verdict"], f["check_id"], f["route"], f["viewport"],
                        f.get("detail", ""), f.get("owning_spec") or f["requirement_source"]))
    if m["flaky_tests"]:
        lines += ["", "## Flaky (recorded, not passed)", ""] + ["- " + t for t in m["flaky_tests"]]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def _find_repo_root(start):
    d = os.path.abspath(start)
    while d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, ".git")):
            return d
        d = os.path.dirname(d)
    return os.path.abspath(start)


def _git_sha(repo_root):
    import subprocess
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_root,
                                       encoding="utf-8", stderr=subprocess.DEVNULL).strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Website Director Browser & Regression QA runner")
    ap.add_argument("--plan", required=True, help="path to browser-qa-manifest.json")
    ap.add_argument("--engine", default="simulation", choices=["simulation", "playwright"])
    ap.add_argument("--mode", default="smoke", choices=["smoke", "regression"])
    ap.add_argument("--evidence", default=None, help="evidence output directory")
    ap.add_argument("--retries", type=int, default=2, help="bounded flake retry budget")
    ap.add_argument("--project-root", default=None)
    args = ap.parse_args(argv)
    evidence = args.evidence or os.path.join(os.path.dirname(os.path.abspath(args.plan)),
                                             "evidence", "browser-qa")
    return run(args.plan, args.engine, evidence, args.mode, args.retries, args.project_root)


if __name__ == "__main__":
    raise SystemExit(main())
