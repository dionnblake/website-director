"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");
const fs = require("node:fs");
const path = require("node:path");
const authority = require("../config/authority.json");
const registry = require("../config/registry.json");
const { buildValidationReport } = require("../validate");
const { createRouter, SpecialistBudgetError } = require("../router");
const { validateRoutingReceipt } = require("../receipts");
const { freezeComparisonPair, assertComparablePair } = require("../benchmark/harness");
const motion = require("../adapters/motion-implementation");
const landing = require("../adapters/landing-conversion");
const reference = require("../adapters/reference-style-grounding");

test("technical validation is fail-closed and passes the pinned architecture", () => {
  const report = buildValidationReport();
  assert.equal(report.status, "WEBSITE_DIRECTOR_SPECIALIST_ARCHITECTURE_IMPLEMENTED");
  assert.equal(report.validation_fail, 0);
  assert.equal(report.counts.total_discovered_skills, 268);
  assert.equal(report.counts.total_registered_skills, 268);
});

test("registry keeps the six core and one conditional-core boundaries", () => {
  assert.deepEqual(registry.adapters.filter((adapter) => adapter.status === "CORE").map((adapter) => adapter.id), authority.core_adapter_ids);
  assert.deepEqual(registry.adapters.filter((adapter) => adapter.status === "CONDITIONAL_CORE").map((adapter) => adapter.id), authority.conditional_core_adapter_ids);
});

test("router deterministically selects primary plus validator and emits complete receipts", () => {
  const router = createRouter();
  const plan = router.route({ capabilityClass: "MOTION", phase: "interaction", currentDecision: "hero_motion", trigger: "approved_motion_need" });
  assert.deepEqual(plan.selectedAdapters, ["MOTION_IMPLEMENTATION", "MOTION_VALIDATOR"]);
  assert.equal(plan.budget.used, 2);
  assert.equal(plan.receipts.length, 2);
  assert.ok(plan.receipts.every(validateRoutingReceipt));
  assert.equal(plan.receipts[0].ROLE, "IMPLEMENTATION_SPECIALIST");
});

test("complex motion routing exposes an on-demand secondary without executing raw upstream knowledge", () => {
  const router = createRouter();
  const plan = router.route({ capabilityClass: "MOTION", phase: "interaction", includeSecondary: true });
  assert.deepEqual(plan.selectedAdapters, ["MOTION_IMPLEMENTATION", "MOTION_VALIDATOR"]);
  assert.equal(plan.recommendation, "NORMALIZED_ADAPTER_REQUIRED_BEFORE_EXECUTION");
  assert.equal(plan.budget.used, 2);
});

test("router keeps cinematic routing dormant without explicit Website Director activation", () => {
  const router = createRouter();
  const plan = router.route({ capabilityClass: "CINEMATIC", phase: "immersive_website" });
  assert.equal(plan.activation, "DORMANT");
  assert.deepEqual(plan.selectedAdapters, []);
  assert.equal(plan.recommendation, "CINEMATIC_SPECIALIST_RECOMMENDED");
});

test("cinematic routing remains dormant even after recommendation until an adapter exists", () => {
  const router = createRouter();
  const plan = router.route({ capabilityClass: "CINEMATIC", phase: "immersive_website", explicitActivation: true });
  assert.equal(plan.activation, "DORMANT");
  assert.deepEqual(plan.selectedAdapters, []);
  assert.equal(plan.recommendation, "CINEMATIC_SPECIALIST_RECOMMENDED");
});

test("router requires a complete budget exception above the ceiling", () => {
  const router = createRouter();
  assert.throws(
    () => router.route({ capabilityClass: "VISUAL_IMPLEMENTATION", phase: "implementation", specialistBudget: 1 }),
    SpecialistBudgetError
  );
  const plan = router.route({
    capabilityClass: "VISUAL_IMPLEMENTATION",
    phase: "implementation",
    specialistBudget: 1,
    specialistBudgetException: {
      decision_or_phase: "implementation",
      specialists_already_active: ["VISUAL_IMPLEMENTATION"],
      additional_specialist_requested: "INTERFACE_QUALITY_VALIDATOR",
      missing_capability: "independent interface validation",
      why_existing_specialists_cannot_supply_it: "builder cannot self-certify",
      expected_material_contribution: "catch responsive and accessibility defects"
    }
  });
  assert.equal(plan.receipts[1].SPECIALIST_BUDGET_EXCEPTION.missing_capability, "independent interface validation");
});

test("landing conversion remains dormant for non-landing page types", () => {
  const router = createRouter();
  const plan = router.route({ capabilityClass: "LANDING_CONVERSION", phase: "landing_page", pageType: "article" });
  assert.equal(plan.activation, "DORMANT");
  assert.deepEqual(plan.selectedAdapters, []);
  assert.equal(landing.evaluate({ pageType: "article" }).eligible, false);
});

test("motion adapter asks whether to animate and recommends cinematic routing without activating it", () => {
  assert.equal(motion.classifyMotion({ motionRequested: false }), "NO_MOTION");
  const result = motion.evaluate({ currentDecision: "immersive_hero", cinematicCandidate: true });
  assert.equal(result.motionClass, "CINEMATIC_CANDIDATE");
  assert.equal(result.specialistRecommendation, "CINEMATIC_SPECIALIST_RECOMMENDED");
  assert.equal(result.canSelectSpecialists, false);
});

test("adapters reject stack mutation requests and reference grounding disables global taste inheritance", () => {
  assert.throws(() => reference.evaluate({ installDependencyRequested: true }), /cannot perform/);
  const result = reference.evaluate({ referenceField: ["local/reference-board"], styleLock: "HG-EDITORIAL-01" });
  assert.equal(result.projectLocalMemory.globalProfileInherited, false);
  assert.equal(result.canMutateStack, false);
});

test("adapter source files contain no router import or route call", () => {
  const adapterDirectory = path.join(__dirname, "..", "adapters");
  const files = fs.readdirSync(adapterDirectory).filter((file) => file.endsWith(".js") && file !== "index.js" && file !== "contract.js");
  for (const file of files) {
    const source = fs.readFileSync(path.join(adapterDirectory, file), "utf8");
    assert.doesNotMatch(source, /require\s*\(\s*["']\.\.\/?router|require\s*\(\s*["']\.\/?router|\.route\s*\(/);
  }
});

test("benchmark pairs cannot drift after freeze", () => {
  const shared = {
    brief: "same",
    startingRepository: "fixture",
    startingCommit: "abc",
    projectStack: "plain-html",
    assetsSupplied: [],
    ownerConstraints: ["local-only"],
    websiteDirectorVersion: "prototype-unversioned",
    evaluationCriteria: ["quality"],
    allowedInterventions: ["bounded"],
    scoringRubric: { quality: 1 }
  };
  const baseline = freezeComparisonPair({ ...shared, frozenAt: "2026-08-28T00:00:00Z" });
  const specialist = freezeComparisonPair({ ...shared, frozenAt: "2026-08-28T00:00:00Z" });
  assert.equal(assertComparablePair(baseline, specialist), true);
  assert.throws(() => assertComparablePair(baseline, { ...specialist, brief: "changed after baseline" }), /frozen field differs/);
});
