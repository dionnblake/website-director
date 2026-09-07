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
_REPO_ROOT = os.path.dirname(_HERE)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from assertions import evaluate  # noqa: E402
from engine.base import (BLOCKED, FAIL, FLAKY, NOT_APPLICABLE, PASS,
                         TEST_ENVIRONMENT_NOISE, load_engine)  # noqa: E402
from guards.frozen_integrity_guard import FrozenIntegrityGuard  # noqa: E402
from framework_validation.cinematic_inspiration import (  # noqa: E402
    build_rendered_visual_evidence, required_surface_ids)

DEFAULT_VIEWPORTS = {
    "smoke": [390, 768, 1440],
    "regression": [360, 375, 390, 428, 768, 1024, 1280, 1440],
}


REQUIRED_CHECK_FUNCTIONS = (
    "check_observation_coverage", "check_motion", "check_brand_tokens",
    "check_reduced_motion", "check_forms", "check_accessibility",
)
REQUIRED_FRAMEWORK_MODULES = (
    "framework_validation.owner_intent",
    "framework_validation.cinematic_inspiration",
)
DESIGN_FIRST_MODULE = "framework_validation.design_first_flow"


def _module_receipt(name):
    import hashlib
    import importlib

    try:
        module = importlib.import_module(name)
    except Exception as exc:  # noqa: BLE001 - a missing module is reported, never assumed present
        return {"module": name, "status": "MISSING", "path": None, "sha256": None,
                "detail": "%s: %s" % (type(exc).__name__, exc)}, None
    path = getattr(module, "__file__", None)
    digest = None
    if path and os.path.isfile(path):
        with open(path, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
    return {"module": name, "status": "LOADED", "path": path, "sha256": digest}, module


def harness_identity(plan, catalog_module=None):
    """Prove which files this process actually imported before it reviews anything.

    Checking that a file exists somewhere in the repository proves nothing about
    the harness that runs.  This resolves the loaded modules, hashes them, and
    fails closed when the catalogue is missing checks that a current review
    depends on - the stale/mixed distribution that let a v2-10-era harness report
    a clean sweep without ever owning a runtime motion or brand check.
    """
    if catalog_module is None:
        from assertions import catalog as catalog_module  # noqa: PLC0415

    modules = []
    missing_modules = []
    catalog_path = getattr(catalog_module, "__file__", None)
    catalog_receipt = {"module": getattr(catalog_module, "__name__", "assertions.catalog"),
                       "status": "LOADED", "path": catalog_path, "sha256": None}
    if catalog_path and os.path.isfile(catalog_path):
        import hashlib
        with open(catalog_path, "rb") as fh:
            catalog_receipt["sha256"] = hashlib.sha256(fh.read()).hexdigest()
    modules.append(catalog_receipt)

    required_modules = list(REQUIRED_FRAMEWORK_MODULES)
    visual_cfg = plan.get("visual_evidence", {}) if isinstance(plan, dict) else {}
    surfaces = visual_cfg.get("required_surfaces") or visual_cfg.get("required_render_set") or []
    surface_names = [str(item.get("surface_id") or item.get("id")) if isinstance(item, dict) else str(item)
                     for item in (surfaces if isinstance(surfaces, list) else [])]
    if any(name.upper().endswith("FULL_HOMEPAGE") for name in surface_names):
        required_modules.append(DESIGN_FIRST_MODULE)
    for name in required_modules:
        receipt, _module = _module_receipt(name)
        modules.append(receipt)
        if receipt["status"] != "LOADED":
            missing_modules.append(name)

    missing_checks = [name for name in REQUIRED_CHECK_FUNCTIONS
                      if not callable(getattr(catalog_module, name, None))]
    registered = {getattr(item, "__name__", str(item))
                  for item in getattr(catalog_module, "ALL_CHECKS", [])}
    unregistered = [name for name in REQUIRED_CHECK_FUNCTIONS
                    if name not in missing_checks and registered and name not in registered]
    status = "BLOCKED" if (missing_checks or missing_modules or unregistered) else "PASS"
    return {
        "status": status,
        "modules": modules,
        "missing_checks": missing_checks,
        "unregistered_checks": unregistered,
        "missing_modules": missing_modules,
        "python": sys.executable,
        "import_paths": [path for path in sys.path[:8]],
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

    # A required visual review gets explicit, named surface jobs.  This keeps
    # the ordinary route matrix backward-compatible while making it impossible
    # to claim the required render set from an unlabeled screenshot hash.
    visual_cfg = plan.get("visual_evidence", {})
    if isinstance(visual_cfg, dict) and visual_cfg.get("required") is True:
        route_defaults = {
            (route.get("path") or route.get("route")): route
            for route in plan.get("routes", []) if isinstance(route, dict)
        }
        first_route = next(iter(route_defaults), "/")
        raw_surfaces = visual_cfg.get("required_surfaces") or visual_cfg.get("required_render_set")
        if isinstance(raw_surfaces, dict):
            raw_surfaces = raw_surfaces.get("surfaces") or raw_surfaces.get("items")
        if not isinstance(raw_surfaces, list):
            raw_surfaces = list(required_surface_ids(visual_cfg))
        seen = set()
        for item in raw_surfaces:
            if isinstance(item, str):
                surface_id = item
                item = {}
            elif isinstance(item, dict):
                surface_id = item.get("surface_id") or item.get("id")
            else:
                continue
            if not surface_id or surface_id in seen:
                continue
            seen.add(surface_id)
            default_mobile = "MOBILE_" in surface_id
            default_reduced = surface_id == "REDUCED_MOTION_STATE"
            # One convention for both surface vocabularies: cinematic_inspiration
            # uses *_FULL_PAGE, design_first_flow uses *_FULL_HOMEPAGE.  A surface
            # whose identity claims the whole page must capture the whole page.
            whole_page = surface_id.endswith(("FULL_PAGE", "FULL_HOMEPAGE"))
            default_capture = "FULL_PAGE" if whole_page else "VIEWPORT"
            requested_capture = str(item.get("capture", default_capture)).upper()
            capture_override_rejected = None
            if whole_page and requested_capture != "FULL_PAGE":
                # A full-page label with a viewport override is a dishonest
                # review claim.  Normalize it and say so in the evidence rather
                # than accepting ~9% of the page under a whole-page name.
                capture_override_rejected = requested_capture
                requested_capture = "FULL_PAGE"
            route = item.get("route") or item.get("path") or first_route
            route_cfg = route_defaults.get(route, {})
            jobs.append({
                "route": route,
                "viewport": int(item.get("viewport", 390 if default_mobile else 1440)),
                "browser": item.get("browser", browsers[0]),
                "reduced_motion": bool(item.get("reduced_motion", default_reduced)),
                "interactions": item.get("interactions", route_cfg.get("interactions", [])),
                "surface_id": surface_id,
                "capture": requested_capture,
                "capture_override_rejected": capture_override_rejected,
            })
    return jobs


def run(plan_path: str, engine_name: str, evidence_dir: str, mode: str,
        retries: int, project_root: str) -> int:
    plan = _load(plan_path)
    project_root = os.path.abspath(project_root or os.path.dirname(plan_path))
    repo_root = plan.get("repo_root") or _find_repo_root(project_root)
    # The assertion catalogue resolves an owner-contract reference relative to
    # the plan, then the project, then the repository.
    plan.setdefault("plan_dir", os.path.dirname(os.path.abspath(plan_path)))
    plan.setdefault("project_root", project_root)
    plan.setdefault("repo_root", repo_root)

    guard = FrozenIntegrityGuard(repo_root, plan.get("protected_paths", ["projects/"]),
                                 run_id="browser-qa-%d" % int(time.time()))
    guard.snapshot()

    engine_config = dict(plan.get("engine_config", {}))
    visual_cfg = plan.get("visual_evidence", {})
    visual_required = isinstance(visual_cfg, dict) and visual_cfg.get("required") is True
    if visual_required:
        # The Playwright adapter keeps these artifacts in memory until the
        # runner writes them to the designated evidence directory.  Simulation
        # remains a dry-run engine and therefore emits no real receipts.
        engine_config["capture_render_artifacts"] = True
    # Runtime specialist checks consume their canonical plan blocks through the
    # same engine. They do not create a second runner or a second state owner.
    if plan.get("localization") and "localization" not in engine_config:
        engine_config["localization"] = plan["localization"]
    if plan.get("application") and "application" not in engine_config:
        engine_config["application"] = plan["application"]
    if plan.get("motion") and "motion" not in engine_config:
        engine_config["motion"] = plan["motion"]
    if plan.get("owner_intent") and "owner_intent" not in engine_config:
        engine_config["owner_intent"] = plan["owner_intent"]
    if "owner_intent" not in engine_config:
        # A contract supplied by reference must reach the adapter too, or an
        # owner-required brand check would have no rendered roles to read.
        from assertions.catalog import owner_authority as _owner_authority
        _resolved = _owner_authority(plan)
        if isinstance(_resolved.get("contract"), dict):
            engine_config["owner_intent"] = _resolved["contract"]
    if plan.get("brand_runtime") and "brand_runtime" not in engine_config:
        engine_config["brand_runtime"] = plan["brand_runtime"]
    for observation_key in ("runtime_observations", "observations"):
        if plan.get(observation_key) and observation_key not in engine_config:
            engine_config[observation_key] = plan[observation_key]
    engine = load_engine(engine_name, project_root, engine_config)
    # Prove the loaded harness before it is allowed to judge anything.
    loaded_harness = harness_identity(plan)
    run_id = "bqa-%s" % time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    started = time.time()
    findings_json: List[Dict[str, Any]] = []
    verdict_counts: Counter = Counter()
    flaky_tests: List[str] = []
    observations_json: List[Dict[str, Any]] = []
    blocked_reason = None

    try:
        available = engine.available()
    except Exception as exc:  # noqa: BLE001
        blocked_reason = _blocked_reason("engine.available()", exc)
    else:
        if not available:
            blocked_reason = "BLOCKED_ENVIRONMENT: BROWSER_QA_ENGINE '%s' unavailable in this environment" % engine_name

    if loaded_harness["status"] != "PASS":
        blocked_reason = ("BLOCKED_STALE_HARNESS: the loaded assertion catalogue is missing %s "
                          "and the loaded framework modules are missing %s; a review cannot be "
                          "claimed from a harness that does not own the checks"
                          % (loaded_harness["missing_checks"] + loaded_harness["unregistered_checks"],
                             loaded_harness["missing_modules"]))

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
                    _append_blocked_job(findings_json, verdict_counts, job, blocked_reason,
                                        observations_json=observations_json)
                    continue
                try:
                    job_blocked_reason = _run_job(
                        engine, plan, job, retries, findings_json, verdict_counts, flaky_tests,
                        observations_json, evidence_dir=evidence_dir, run_id=run_id,
                        persist_render_artifacts=visual_required)
                except Exception as exc:  # noqa: BLE001
                    job_blocked_reason = _blocked_reason("browser QA job", exc)
                    _append_blocked_job(findings_json, verdict_counts, job, job_blocked_reason,
                                        check_id="engine.runtime", observations_json=observations_json)
                if job_blocked_reason is not None:
                    blocked_reason = job_blocked_reason
        else:
            for job in jobs:
                _append_blocked_job(findings_json, verdict_counts, job, blocked_reason,
                                    observations_json=observations_json)
    finally:
        try:
            engine.stop()
        except Exception as exc:  # noqa: BLE001
            stop_reason = _blocked_reason("engine.stop()", exc)
            blocked_reason = "%s; %s" % (blocked_reason, stop_reason) if blocked_reason else stop_reason

    integrity = guard.verify()
    is_production = plan.get("environment") == "production" or \
        any(str(r.get("path", "")).startswith("https://") for r in plan.get("routes", []))
    build_identity = _build_identity(repo_root, project_root, plan)
    git_sha = build_identity["git_sha"]
    owner_compliance = _owner_requirement_boundary(
        plan, observations_json, findings_json, verdict_counts, engine.name)
    owner_visual_coverage = (owner_compliance.get("coverage") or {}).get("visual_evidence", "NOT_REQUIRED")
    if not visual_required and owner_visual_coverage == "REQUIRED":
        # Omitting the visual_evidence block cannot turn an owner-required
        # rendered review into "not applicable".
        verdict_counts[BLOCKED] += 1
        findings_json.append({
            "check_id": "visual.evidence.owner_required_review_not_declared",
            "title": "OWNER_REQUIRED_VISUAL_EVIDENCE_NOT_DECLARED", "verdict": BLOCKED,
            "requirement_source": "OWNER_INTENT", "owning_spec": "templates/owner-intent.json",
            "route": "__visual_evidence__", "viewport": 0, "browser": engine.name,
            "reduced_motion": False, "method": "VISUAL_COMPARISON",
            "detail": ("the current owner contract requires rendered visual evidence but the plan "
                       "declares no visual_evidence block; no capture set is invented here"),
            "evidence": {"owner_contract_source": owner_compliance.get("owner_contract_source")},
        })
    if visual_required:
        visual_evidence = build_rendered_visual_evidence(
            visual_cfg, observations_json, run_id=run_id, git_sha=git_sha,
            build_identity=build_identity, evidence_root=evidence_dir)
        for issue in visual_evidence["issues"]:
            code = issue["code"]
            verdict_counts[BLOCKED] += 1
            findings_json.append({
                "check_id": "visual.evidence." + code.lower(),
                "title": code,
                "verdict": BLOCKED,
                "requirement_source": "BROWSER_QA_PLAN",
                "owning_spec": "BROWSER-REGRESSION-QA-PROTOCOL.md",
                "route": "__visual_evidence__",
                "viewport": 0,
                "browser": engine.name,
                "reduced_motion": False,
                "method": "VISUAL_COMPARISON",
                "detail": issue["detail"],
                "evidence": {"code": code, "required_surfaces": visual_evidence["required_surfaces"]},
            })
    else:
        visual_evidence = {
            "required": False,
            "status": "NOT_REQUIRED",
            "required_surfaces": [],
            "captured_surfaces": [],
            "issues": [],
        }

    passed = (verdict_counts[FAIL] == 0 and verdict_counts[BLOCKED] == 0
              and verdict_counts[FLAKY] == 0 and integrity.ok and blocked_reason is None)
    manifest = {
        "run_id": run_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_sha": git_sha,
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
        "build_identity": build_identity,
        "loaded_harness": loaded_harness,
        "owner_requirement_compliance": owner_compliance,
        "visual_evidence": visual_evidence,
        "observations": observations_json,
        "findings": findings_json,
        "overall": ("PASS" if passed else "BLOCKED"
                    if blocked_reason or verdict_counts[BLOCKED]
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


def _owner_requirement_boundary(plan, observations, findings_json, verdict_counts, engine_name):
    """Run the existing owner-compliance audit once, at the completion boundary.

    The per-observation checks answer "did this route behave?".  This answers
    "were the owner's explicit constraints satisfied by this candidate?", and
    its result is folded into the run verdict rather than written to a report
    nobody consumes.  It runs once per run, not inside every observation.
    """
    from assertions.catalog import owner_authority

    authority = owner_authority(plan)
    summary = {
        "status": authority.get("status"),
        "owner_contract_source": authority.get("contract_source"),
        "coverage": authority.get("coverage"),
        "requirements": [],
        "issues": [],
    }
    if authority.get("status") in ("NOT_DECLARED", "HISTORICAL"):
        return summary

    def _emit(check_id, title, verdict, detail, evidence):
        verdict_counts[verdict] += 1
        findings_json.append({
            "check_id": check_id, "title": title, "verdict": verdict,
            "requirement_source": "OWNER_INTENT", "owning_spec": "templates/owner-intent.json",
            "route": "__owner_requirements__", "viewport": 0, "browser": engine_name,
            "reduced_motion": False, "method": "REQUIREMENT_AUDIT",
            "detail": detail, "evidence": evidence,
        })

    if authority.get("status") == "BLOCKED":
        _emit("owner.contract-resolution", "Current owner contract resolves before completion",
              BLOCKED, str(authority.get("blocked_reason")),
              {"contract_source": authority.get("contract_source"),
               "issues": authority.get("issues", [])})
        summary["issues"] = list(authority.get("issues", []))
        return summary

    from framework_validation.owner_intent import audit_owner_requirement_compliance

    motion_rows = [row for observation in observations
                   for row in (observation.get("motion_observations") or [])
                   if isinstance(row, dict) and not observation.get("reduced_motion")]
    rendered_colors = next((observation.get("rendered_colors") for observation in observations
                            if observation.get("rendered_colors")), [])
    identities = {str(observation.get("engine_identity", "")).upper() for observation in observations}
    runtime_evidence = {
        "engine_identity": "REAL_BROWSER" if "REAL_BROWSER" in identities else (
            sorted(identities)[0] if identities else None),
        "runtime_observed": bool(motion_rows),
        "motion_observations": motion_rows,
        "rendered": {"rendered_colors": rendered_colors},
        "rendered_colors": rendered_colors,
    }
    implemented = plan.get("owner_implementation")
    implemented = dict(implemented) if isinstance(implemented, dict) else {}
    implemented.setdefault("brand", plan.get("brand_implementation",
                                             plan.get("implementation_tokens", {})))
    audit = audit_owner_requirement_compliance(
        authority.get("contract") or {},
        plan.get("locked_decisions") or {},
        implemented,
        runtime_evidence,
    )
    summary.update({
        "status": audit.get("OWNER_REQUIREMENT_COMPLIANCE"),
        "requirements": audit.get("requirements", []),
        "issues": audit.get("issues", []),
        "motion": audit.get("motion"),
        "motion_trace_status": (audit.get("motion_trace") or {}).get("status"),
        "brand_status": (audit.get("brand") or {}).get("status"),
        "runtime_motion_rows": len(motion_rows),
    })
    for issue in audit.get("issues", []):
        _emit("owner.requirement." + str(issue.get("code", "ISSUE")).lower(),
              str(issue.get("code", "OWNER_REQUIREMENT_ISSUE")),
              BLOCKED if issue.get("blocking") else FAIL,
              str(issue.get("detail", "")),
              {"code": issue.get("code"), "contract_source": authority.get("contract_source")})
    if not audit.get("issues"):
        _emit("owner.requirement-compliance", "Explicit owner requirements are satisfied",
              PASS, "requirements=%d" % len(audit.get("requirements", [])),
              {"contract_source": authority.get("contract_source"),
               "requirements": audit.get("requirements", [])})
    return summary


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


def _finding_key(finding):
    scope = (finding.evidence or {}).get("sequence_id") or ""
    return "%s|%s" % (finding.check_id, scope)


def _run_job(engine, plan, job, retries, findings_json, verdict_counts, flaky_tests,
             observations_json=None, evidence_dir=None, run_id=None,
             persist_render_artifacts=False):
    """Bounded flake policy (protocol sec 21): FAIL then PASS on retry == FLAKY,
    never an unconditional PASS. A check that fails every attempt is FAIL."""
    attempts: List[Dict[str, Any]] = []
    for attempt in range(retries + 1):
        try:
            if job.get("surface_id"):
                obs = engine.observe_surface(
                    job["route"], job["viewport"],
                    reduced_motion=job["reduced_motion"], browser=job["browser"],
                    interactions=job.get("interactions"),
                    capture=job.get("capture", "VIEWPORT"),
                )
            else:
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
            if observations_json is not None:
                observations_json.append(_blocked_observation_snapshot(job, detail, attempt + 1))
            return detail
        if observations_json is not None:
            observations_json.append(_observation_snapshot(
                obs, job, attempt + 1, evidence_dir=evidence_dir, run_id=run_id,
                persist_render_artifacts=persist_render_artifacts))
        fx_flaky = (obs.raw or {}).get("flaky")
        if fx_flaky:
            phase = "first_run" if attempt == 0 else "retry"
            verdict = fx_flaky.get(phase, PASS)
            results = {"fixture.flaky-probe": _mk("fixture.flaky-probe", "Flaky-probe fixture",
                                                  verdict, "BROWSER_QA_PLAN", job,
                                                  detail="phase=%s" % phase)}
        else:
            # Keyed by check *and* its scope: a per-sequence finding must not
            # overwrite its sibling, or one working sequence would hide the
            # stationary one beside it.  The key is stable across attempts, so
            # the flake policy is unchanged.
            results = {_finding_key(f): _to_dict(f, job) for f in evaluate(obs, plan)}
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
                               % (rec["check_id"], job["route"], job["viewport"],
                                  " rm" if job["reduced_motion"] else "", len(attempts) - 1))
        rec["verdict"] = v
        rec["attempts"] = len(attempts)
        verdict_counts[v] += 1
        findings_json.append(rec)
    return None


def _blocked_reason(operation: str, exc: Exception) -> str:
    detail = str(exc).strip().splitlines()[0] if str(exc).strip() else exc.__class__.__name__
    return "BLOCKED_ENVIRONMENT: %s failed: %s" % (operation, detail)


def _append_blocked_job(findings_json, verdict_counts, job, detail, check_id="engine.availability",
                        observations_json=None):
    verdict_counts[BLOCKED] += 1
    findings_json.append({"check_id": check_id, "verdict": BLOCKED,
                          "route": job["route"], "viewport": job["viewport"],
                          "browser": job["browser"],
                          "reduced_motion": job.get("reduced_motion", False),
                          "requirement_source": "BROWSER_QA_PLAN", "detail": detail})
    if observations_json is not None:
        observations_json.append(_blocked_observation_snapshot(job, detail, 1))


def _safe_filename(value):
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in str(value))


def _png_dimensions(payload):
    """Read width/height from the PNG IHDR chunk.  No new dependency."""
    magic = bytes([137, 80, 78, 71, 13, 10, 26, 10])
    if len(payload) < 24 or payload[:8] != magic:
        return None, None
    return (int.from_bytes(payload[16:20], "big"), int.from_bytes(payload[20:24], "big"))


def _verify_capture(payload, capture, raw, job):
    """Prove a full-page label with the image, not with the label.

    The surface name and the requested capture mode are claims.  The pixels,
    the document height, and the below-the-fold element count are evidence.
    """
    width, height = _png_dimensions(payload)
    metrics = raw.get("page_metrics") or {}
    scroll_height = metrics.get("scroll_height")
    client_height = metrics.get("client_height")
    issues = []
    verdict = "VERIFIED"
    surface_id = str(job.get("surface_id") or "")
    claims_whole_page = surface_id.endswith(("FULL_PAGE", "FULL_HOMEPAGE")) or capture == "FULL_PAGE"
    if height is None:
        verdict, issues = "NOT_VERIFIED", ["CAPTURE_DIMENSIONS_UNREADABLE"]
    elif claims_whole_page:
        if not scroll_height:
            verdict, issues = "NOT_VERIFIED", ["PAGE_METRICS_UNAVAILABLE"]
        elif height < scroll_height * 0.95:
            verdict = "FAIL"
            issues.append("FULL_PAGE_CAPTURE_TRUNCATED: image %spx vs document %spx" % (height, scroll_height))
        if metrics.get("below_fold_elements") in (0, None) and scroll_height and client_height                 and scroll_height > client_height * 1.5:
            issues.append("BELOW_FOLD_CONTENT_NOT_OBSERVED")
        if metrics.get("images_total") and metrics.get("images_complete") is not None                 and metrics["images_complete"] < metrics["images_total"]:
            issues.append("IMAGES_INCOMPLETE_AT_CAPTURE: %s/%s" % (
                metrics["images_complete"], metrics["images_total"]))
    elif scroll_height and client_height and height > client_height * 1.5:
        issues.append("VIEWPORT_CAPTURE_EXCEEDS_VIEWPORT")
    if job.get("capture_override_rejected"):
        issues.append("CAPTURE_OVERRIDE_REJECTED: %s override normalized to FULL_PAGE for a "
                      "whole-page surface" % job["capture_override_rejected"])
    return {"verdict": "FAIL" if any(item.startswith("FULL_PAGE_CAPTURE_TRUNCATED") for item in issues)
            else verdict,
            "image_width": width, "image_height": height,
            "document_height": scroll_height, "viewport_height": client_height,
            "render_readiness": raw.get("render_readiness"),
            "below_fold_elements": metrics.get("below_fold_elements"),
            "images_complete": metrics.get("images_complete"),
            "images_total": metrics.get("images_total"),
            "claims_whole_page": claims_whole_page,
            "issues": issues}


def _persist_render_artifacts(obs, job, attempt, evidence_dir=None, run_id=None,
                              persist_render_artifacts=False):
    if not persist_render_artifacts or not evidence_dir:
        return {}
    raw = obs.raw or {}
    shot = raw.get("screenshot_bytes")
    if not isinstance(shot, (bytes, bytearray)):
        return {
            "actual_rendered": False,
            "engine_identity": raw.get("engine_identity", obs.engine),
            "render_capture": raw.get("render_capture", job.get("capture", "VIEWPORT")),
        }
    surface = _safe_filename(job.get("surface_id") or "%s_%s" % (job["route"], job["viewport"]))
    stem = "%s__%s__attempt-%d" % (_safe_filename(run_id or "render"), surface, attempt)
    render_dir = os.path.join(evidence_dir, "rendered")
    os.makedirs(render_dir, exist_ok=True)
    shot_path = os.path.join(render_dir, stem + ".png")
    with open(shot_path, "wb") as fh:
        fh.write(bytes(shot))

    import hashlib
    capture = str(raw.get("render_capture", job.get("capture", "VIEWPORT"))).upper()
    result = {
        "actual_rendered": str(raw.get("engine_identity", "")).upper() == "REAL_BROWSER",
        "engine_identity": raw.get("engine_identity", obs.engine),
        "render_capture": capture,
        "screenshot_path": os.path.relpath(shot_path, evidence_dir).replace("\\", "/"),
        "screenshot_sha256": hashlib.sha256(bytes(shot)).hexdigest(),
        "capture_verification": _verify_capture(bytes(shot), capture, raw, job),
    }
    for key, suffix in (("rendered_dom", ".html"), ("rendered_css", ".css")):
        content = raw.get(key)
        if not isinstance(content, str) or not content.strip():
            continue
        path = os.path.join(render_dir, stem + suffix)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        result[key + "_path"] = os.path.relpath(path, evidence_dir).replace("\\", "/")
    return result


def _observation_snapshot(obs, job, attempt, evidence_dir=None, run_id=None,
                          persist_render_artifacts=False):
    render_receipt = _persist_render_artifacts(
        obs, job, attempt, evidence_dir=evidence_dir, run_id=run_id,
        persist_render_artifacts=persist_render_artifacts)
    all_console_errors = [m.text for m in obs.console if m.level == "error"]
    bad_console = [m.text for m in obs.console
                   if m.level == "error" and m.classification != TEST_ENVIRONMENT_NOISE]
    bad_network = [n.url for n in obs.network if not n.ok and not n.blocked_allowed]
    responsive_status = "NOT_RUN"
    if obs.layout is not None:
        responsive_status = "FAIL" if obs.layout.has_horizontal_overflow else "PASS"
    keyboard_status = "NOT_RUN"
    if obs.keyboard is not None:
        keyboard_status = "PASS" if all((
            obs.keyboard.primary_nav_reachable, obs.keyboard.visible_focus_ring,
            obs.keyboard.menu_toggle_operable, obs.keyboard.no_keyboard_trap,
            obs.keyboard.primary_cta_reachable)) else "FAIL"
    accessibility_status = "NOT_RUN"
    if obs.a11y is not None:
        accessibility_status = ("PASS" if obs.a11y.engine_status == "RAN"
                                and not obs.a11y.violations else obs.a11y.engine_status)
    return {
        "route": job["route"], "viewport": job["viewport"], "browser": job["browser"],
        "surface_id": job.get("surface_id"),
        "render_capture": render_receipt.get("render_capture", job.get("capture")),
        "reduced_motion": job.get("reduced_motion", False), "engine": obs.engine,
        "engine_identity": (obs.raw or {}).get("engine_identity", obs.engine),
        "engine_version": (obs.raw or {}).get("engine_version", "unknown"),
        "attempt": attempt, "form_observations": [f.raw for f in obs.forms if f.raw]
        or (obs.raw or {}).get("form_observations", []),
        "mobile_nav_observation": (obs.raw or {}).get("mobile_nav_observation", {}),
        "analytics_events": [{"name": e.name, "params": e.params, "count": e.count,
                              "trigger": e.trigger} for e in obs.analytics_events],
        "motion_observations": list(getattr(obs, "motion_observations", []) or
                                     (obs.raw or {}).get("motion_observations", [])),
        "rendered_colors": (obs.raw or {}).get("rendered_colors", []),
        "console_status": "FAIL" if bad_console else "PASS",
        "console_errors": all_console_errors,
        "console_environment_noise": [m.text for m in obs.console
                                       if m.level == "error"
                                       and m.classification == TEST_ENVIRONMENT_NOISE],
        "network_status": "FAIL" if bad_network else "PASS",
        "responsive_status": responsive_status,
        "keyboard_status": keyboard_status,
        "accessibility_status": accessibility_status,
        "screenshot_evidence_ref": render_receipt.get("screenshot_path") or obs.render_signature or None,
        "actual_rendered": render_receipt.get("actual_rendered", False),
        "screenshot_path": render_receipt.get("screenshot_path"),
        "screenshot_sha256": render_receipt.get("screenshot_sha256"),
        "capture_verification": render_receipt.get("capture_verification"),
        "capture_override_rejected": job.get("capture_override_rejected"),
        "rendered_dom_path": render_receipt.get("rendered_dom_path"),
        "rendered_css_path": render_receipt.get("rendered_css_path"),
        "result": "OBSERVATION_EMITTED",
        "observation_status": (obs.raw or {}).get("observation_status", "EMITTED"),
    }


def _blocked_observation_snapshot(job, detail, attempt):
    return {
        "route": job["route"], "viewport": job["viewport"], "browser": job["browser"],
        "surface_id": job.get("surface_id"),
        "render_capture": job.get("capture"),
        "reduced_motion": job.get("reduced_motion", False), "engine": "unavailable",
        "attempt": attempt, "form_observations": "BLOCKED_OBSERVATION_MISSING",
        "mobile_nav_observation": "BLOCKED_OBSERVATION_MISSING",
        "motion_observations": "BLOCKED_OBSERVATION_MISSING",
        "analytics_events": [], "observation_status": "BLOCKED_ENVIRONMENT",
        "actual_rendered": False, "screenshot_path": None, "screenshot_sha256": None,
        "blocked_reason": detail,
    }


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


def _content_digest(root, relative_paths):
    """Digest the reviewed bytes themselves.

    A HEAD SHA cannot identify a working tree that carries uncommitted changes,
    so evidence is bound to the content that was actually served.
    """
    import hashlib

    digest = hashlib.sha256()
    counted = 0
    for relative in sorted(relative_paths or []):
        base = os.path.join(root, relative)
        if os.path.isfile(base):
            walked = [base]
        elif os.path.isdir(base):
            walked = sorted(os.path.join(folder, name)
                            for folder, _dirs, names in os.walk(base) for name in names)
        else:
            continue
        for path in walked:
            try:
                with open(path, "rb") as fh:
                    payload = fh.read()
            except OSError:
                continue
            digest.update(os.path.relpath(path, root).replace("\\", "/").encode("utf-8"))
            digest.update(hashlib.sha256(payload).digest())
            counted += 1
    return {"content_sha256": digest.hexdigest() if counted else None, "file_count": counted}


def _build_identity(repo_root, project_root, plan):
    import subprocess

    sha = _git_sha(repo_root)
    try:
        dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=repo_root,
                                             encoding="utf-8", stderr=subprocess.DEVNULL).strip())
    except Exception:  # noqa: BLE001
        dirty = None
    sources = plan.get("build_content_paths")
    if not isinstance(sources, list) or not sources:
        sources = [name for name in ("site", "src", "public", "dist")
                   if os.path.isdir(os.path.join(project_root, name))]
    if not sources:
        # No conventional build directory: digest the served content itself,
        # skipping evidence output, caches, and dependency trees.
        skip = {"evidence", "node_modules", ".git", "__pycache__", ".venv", "work"}
        sources = sorted(name for name in os.listdir(project_root)
                         if name not in skip and not name.startswith("."))
    content = _content_digest(project_root, sources)
    return {
        "git_sha": sha,
        "working_tree_dirty": dirty,
        "content_paths": sources,
        "content_sha256": content["content_sha256"],
        "content_file_count": content["file_count"],
        # When the tree is dirty a HEAD SHA alone cannot identify these bytes.
        "build_id": content["content_sha256"] or sha,
    }


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
