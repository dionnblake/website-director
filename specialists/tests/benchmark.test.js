"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");
const {
  REQUIRED_METRICS,
  SCENARIOS,
  createBenchmarkPlan,
  createMetricRecord,
  certifyOutcome,
  freezeComparisonPair,
  assertComparablePair
} = require("../benchmark/harness");
const { collectRoutingEvidence, createSourceSnapshot } = require("../benchmark/run");

test("benchmark plan preserves all four classes and required outcome metrics", () => {
  const plan = createBenchmarkPlan();
  assert.equal(plan.status, "READY_FOR_OUTCOME_EXECUTION");
  assert.deepEqual(SCENARIOS.map((scenario) => scenario.id), ["A", "B", "C", "D"]);
  assert.deepEqual(plan.required_metrics, REQUIRED_METRICS);
  assert.equal(plan.stop_after_report, true);
});

test("metric records are explicit about missing evidence", () => {
  const record = createMetricRecord({ TOTAL_SPECIALISTS_USED: 2 });
  assert.equal(record.TOTAL_SPECIALISTS_USED, 2);
  assert.equal(record.OWNER_REVISION_ROUNDS, null);
  assert.deepEqual(Object.keys(record), REQUIRED_METRICS);
});

test("outcome certification stays inconclusive without paired completed runs", () => {
  const result = certifyOutcome(SCENARIOS.map((scenario) => ({
    id: scenario.id,
    comparable: false,
    baseline: { status: "NOT_EXECUTED" },
    specialist: { status: "ROUTING_ONLY" }
  })));
  assert.equal(result.verdict, "WEBSITE_DIRECTOR_SPECIALIST_OUTCOME_BENCHMARK_INCONCLUSIVE");
  assert.equal(result.reasons.length, 4);
});

test("complete-looking pairs still require every metric before certification", () => {
  const result = certifyOutcome(SCENARIOS.map((scenario) => ({
    id: scenario.id,
    comparable: true,
    baseline: { status: "COMPLETE", metrics: {} },
    specialist: { status: "COMPLETE", metrics: {} }
  })));
  assert.equal(result.verdict, "WEBSITE_DIRECTOR_SPECIALIST_OUTCOME_BENCHMARK_INCONCLUSIVE");
  assert.match(result.reasons[0].issue, /required metrics/);
});

test("cinematic benchmark routing remains on-demand and records no material output contribution", () => {
  const routing = collectRoutingEvidence("B");
  assert.equal(routing.decisionCount, 2);
  assert.deepEqual(routing.receipts.map((receipt) => receipt.ADAPTER_ID), ["MOTION_IMPLEMENTATION", "MOTION_VALIDATOR"]);
  assert.equal(routing.selectedAdapterCount, 2);
  assert.equal(routing.materialContributionCount, 0);
  assert.equal(routing.plans[1].plan.activation, "DORMANT");
  assert.deepEqual(routing.plans[1].plan.selectedAdapters, []);
});

test("source snapshot identity is content-based when the worktree has no commit", () => {
  const snapshot = createSourceSnapshot();
  assert.match(snapshot.workspaceDigestSha256, /^[0-9a-f]{64}$/);
  assert.ok(snapshot.files.some((file) => file.path === "index.html"));
  assert.ok(snapshot.assets.length > 0);
  assert.ok(snapshot.files.every((file) => !file.path.startsWith("specialists/benchmark/results/")));
});

test("freeze pairs reject drift in any frozen field", () => {
  const shared = {
    brief: "brief",
    startingRepository: "fixture",
    startingCommit: "snapshot",
    projectStack: "plain-html",
    assetsSupplied: [],
    ownerConstraints: ["local-only"],
    websiteDirectorVersion: "prototype-unversioned",
    evaluationCriteria: ["quality"],
    allowedInterventions: ["bounded"],
    scoringRubric: { scale: "0-5" }
  };
  const baseline = freezeComparisonPair({ ...shared, frozenAt: "2026-08-28T00:00:00.000Z" });
  const specialist = freezeComparisonPair({ ...shared, frozenAt: "2026-08-28T00:00:00.000Z" });
  assert.equal(assertComparablePair(baseline, specialist), true);
  assert.throws(() => assertComparablePair(baseline, { ...specialist, frozen: false }), /two frozen pairs/);
  assert.throws(() => assertComparablePair(baseline, { ...specialist, brief: "drift" }), /frozen field differs/);
});
