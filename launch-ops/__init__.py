"""Launch & Post-Launch Operations subsystem (Website Director V2.10).

Policy is canonical in ``../LAUNCH-OPERATIONS-PROTOCOL.md``. This package holds
the deterministic validators that back Phase 12.25 (``validator.py`` -- the
``launch_ops{}`` state machine, the release-readiness gate, the owner
deployment-authorization boundary, the production-verification checks, and the
rollback-trigger evaluator).

Like ``browser-qa/``, this directory name contains a hyphen; import its modules
by putting the directory on ``sys.path`` and importing ``validator`` directly:

    sys.path.insert(0, os.path.join(repo_root, "launch-ops"))
    from validator import evaluate_release_readiness

It performs no network access, launches no browser, deploys nothing, and never
writes ``site-profile.json``. Production *browser* verification is delegated to
the V2.8 ``browser-qa/`` harness in ``environment = "production"`` mode.
"""
