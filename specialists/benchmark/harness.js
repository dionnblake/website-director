"use strict";

const FREEZE_FIELDS = [
  "brief",
  "startingRepository",
  "startingCommit",
  "projectStack",
  "assetsSupplied",
  "ownerConstraints",
  "websiteDirectorVersion",
  "evaluationCriteria",
  "allowedInterventions",
  "scoringRubric"
];

const REQUIRED_METRICS = [
  "OWNER_PROMPT_ITERATIONS",
  "OWNER_INTERVENTIONS",
  "OWNER_REVISION_ROUNDS",
  "TOTAL_SPECIALISTS_USED",
  "SPECIALIST_BUDGET_EXCEPTIONS",
  "BUILD_STEPS",
  "BUILD_FAILURES",
  "RESPONSIVE_DEFECTS",
  "ACCESSIBILITY_DEFECTS",
  "MOTION_DEFECTS",
  "VISUAL_QA_SCORE",
  "GENERIC_AI_PATTERN_COUNT",
  "BRAND_FIDELITY_SCORE",
  "PERFORMANCE_ISSUES",
  "TOKEN_USAGE",
  "ELAPSED_EXECUTION_TIME"
];

const METRICS = [...REQUIRED_METRICS, "SPECIALIST_ROUTING_DECISIONS"];

const HARD_RULES = [
  "Do not modify the six CORE adapters or conditional UX/IA validator merely to improve benchmark results.",
  "Do not promote additional LIBRARY or ON-DEMAND skills into CORE during benchmarking.",
  "Do not change Website Director phases, gates, locks, SEO integration, research requirements, brand controls, publishing boundaries, or orchestration authority.",
  "Do not deploy or publish anything.",
  "Do not alter the benchmark criteria after seeing results.",
  "Use equivalent starting conditions for baseline and specialist runs.",
  "Preserve all benchmark artifacts, routing receipts, screenshots, scores, and machine-readable results.",
  "Do not declare success merely because the specialist architecture runs correctly."
];

const QUALITY_SEPARATION = {
  VERIFIED: [
    "overflow",
    "responsive defects",
    "contrast",
    "accessibility failures",
    "missing reduced-motion handling",
    "runtime errors",
    "broken interaction states",
    "measurable performance failures"
  ],
  JUDGMENT: [
    "visual quality",
    "originality",
    "premium feel",
    "composition quality",
    "brand expression",
    "aesthetic coherence"
  ]
};

const SCORING_RUBRIC = {
  scale: "0-5 per dimension, with evidence status recorded separately",
  verified_dimensions: [
    "responsive_quality",
    "accessibility",
    "motion_safety",
    "performance",
    "runtime_integrity"
  ],
  judgment_dimensions: [
    "visual_quality",
    "brand_fidelity",
    "conversion_structure",
    "originality",
    "interaction_quality",
    "owner_friction"
  ],
  score_statuses: ["VERIFIED", "JUDGMENT", "NOT_AVAILABLE", "NOT_COMPARABLE"]
};

const SCENARIOS = [
  {
    id: "A",
    name: "BRAND_LANDING_PAGE",
    brief: "Build a brand and marketing landing page from the frozen starting conditions.",
    evaluation: ["visual hierarchy", "brand fidelity", "typography", "composition", "responsive quality", "CTA architecture", "conversion structure", "perceived polish", "generic-AI design patterns", "accessibility"]
  },
  {
    id: "B",
    name: "IMMERSIVE_CINEMATIC_PAGE",
    brief: "Build an immersive cinematic page requiring stronger art direction and motion judgment.",
    evaluation: ["visual storytelling", "imagery and art direction", "motion judgment", "animation restraint", "originality", "scroll behavior", "reduced-motion support", "accessibility", "responsive behavior", "performance"]
  },
  {
    id: "C",
    name: "CONTENT_AFFILIATE_SITE",
    brief: "Build a content and affiliate site with useful discovery, conversion, and SEO-compatible structure.",
    evaluation: ["information architecture", "content hierarchy", "article discovery", "conversion structure", "affiliate usability", "SEO compatibility", "visual hierarchy", "responsive behavior", "accessibility", "brand fidelity"]
  },
  {
    id: "D",
    name: "EXISTING_MEDIOCRE_SITE_IMPROVEMENT",
    brief: "Improve the same intentionally mediocre and generic starting implementation in both runs.",
    evaluation: ["diagnosis quality", "improvement magnitude", "restraint", "preservation of working architecture", "generic-AI-pattern reduction", "UI polish", "accessibility", "responsive quality", "owner revision burden"]
  }
];

const MINIMUM_PASS_CONDITION = {
  no_meaningful_accessibility_regression: true,
  no_meaningful_responsive_quality_regression: true,
  no_increase_in_owner_revision_rounds_overall: true,
  no_systemic_token_explosion: true,
  clear_improvement_in_at_least_two: ["visual quality", "brand fidelity", "motion quality", "originality", "conversion structure", "interaction quality"],
  substantial_improvement_in_at_least_one_visually_demanding_benchmark: true,
  routing_remains_understandable_and_narrow: true,
  specialist_activations_materially_affected_output: true
};

function freezeComparisonPair(input = {}) {
  const missing = FREEZE_FIELDS.filter((field) => input[field] === undefined || input[field] === null);
  if (missing.length) throw new Error(`Benchmark pair is not frozen; missing: ${missing.join(", ")}`);
  return Object.freeze({
    freeze_version: 1,
    frozen: true,
    frozen_at: input.frozenAt || new Date().toISOString(),
    ...input
  });
}

function assertComparablePair(baselinePair, specialistPair) {
  if (!baselinePair?.frozen || !specialistPair?.frozen) {
    throw new Error("Benchmark comparison requires two frozen pairs");
  }
  if (baselinePair.freeze_version !== specialistPair.freeze_version) {
    throw new Error("Benchmark comparison is invalid; freeze versions differ");
  }
  for (const field of FREEZE_FIELDS) {
    if (JSON.stringify(baselinePair[field]) !== JSON.stringify(specialistPair[field])) {
      throw new Error(`Benchmark comparison is invalid; frozen field differs: ${field}`);
    }
  }
  return true;
}

function createMetricRecord(values = {}) {
  return Object.fromEntries(REQUIRED_METRICS.map((metric) => [metric, values[metric] ?? null]));
}

function certifyOutcome(scenarioResults = []) {
  if (!Array.isArray(scenarioResults) || scenarioResults.length !== SCENARIOS.length) {
    return {
      verdict: "WEBSITE_DIRECTOR_SPECIALIST_OUTCOME_BENCHMARK_INCONCLUSIVE",
      reasons: ["All four representative benchmark classes require a result record."]
    };
  }

  const incomplete = scenarioResults.flatMap((scenario) => {
    const reasons = [];
    if (scenario.comparable !== true) reasons.push("baseline and specialist outputs are not comparable");
    if (scenario.baseline?.status !== "COMPLETE") reasons.push(`baseline status is ${scenario.baseline?.status || "MISSING"}`);
    if (scenario.specialist?.status !== "COMPLETE") reasons.push(`specialist status is ${scenario.specialist?.status || "MISSING"}`);
    return reasons.length ? [{ scenario: scenario.id, reasons }] : [];
  });

  if (incomplete.length) {
    return {
      verdict: "WEBSITE_DIRECTOR_SPECIALIST_OUTCOME_BENCHMARK_INCONCLUSIVE",
      reasons: incomplete
    };
  }

  const missingMetricEvidence = scenarioResults.flatMap((scenario) => {
    const missingSides = ["baseline", "specialist"].filter((side) => {
      const metrics = scenario[side]?.metrics;
      return !metrics || REQUIRED_METRICS.some((metric) => metrics[metric] === undefined || metrics[metric] === null);
    });
    return missingSides.length ? [{ scenario: scenario.id, missing_sides: missingSides }] : [];
  });
  if (missingMetricEvidence.length) {
    return {
      verdict: "WEBSITE_DIRECTOR_SPECIALIST_OUTCOME_BENCHMARK_INCONCLUSIVE",
      reasons: [{ issue: "required metrics are incomplete", scenarios: missingMetricEvidence }]
    };
  }

  const improvements = new Set(scenarioResults.flatMap((scenario) => scenario.improvements || []));
  const noRegression = scenarioResults.every((scenario) => scenario.noMeaningfulRegression === true);
  const materialContribution = scenarioResults.some((scenario) => scenario.materiallyAffectedOutput === true);
  const revisionRoundsComparable = scenarioResults.every((scenario) => {
    const baselineRounds = scenario.baseline?.metrics?.OWNER_REVISION_ROUNDS;
    const specialistRounds = scenario.specialist?.metrics?.OWNER_REVISION_ROUNDS;
    return Number.isFinite(baselineRounds) && Number.isFinite(specialistRounds) && specialistRounds <= baselineRounds;
  });
  const noSystemicTokenExplosion = scenarioResults.every((scenario) => scenario.noSystemicTokenExplosion === true);
  const routingUnderstandable = scenarioResults.every((scenario) => scenario.routingUnderstandable === true);
  const demandingBenchmarkImproved = scenarioResults.some((scenario) => scenario.visuallyDemanding === true && scenario.substantialVisuallyDemandingImprovement === true);
  const pass = noRegression && improvements.size >= 2 && materialContribution && revisionRoundsComparable && noSystemicTokenExplosion && routingUnderstandable && demandingBenchmarkImproved;

  return {
    verdict: pass ? "WEBSITE_DIRECTOR_SPECIALIST_OUTCOME_BENCHMARK_PASSED" : "WEBSITE_DIRECTOR_SPECIALIST_OUTCOME_BENCHMARK_FAILED",
    reasons: pass ? [] : ["Complete paired results did not satisfy every minimum pass condition."]
  };
}

function createBenchmarkPlan() {
  return {
    status: "READY_FOR_OUTCOME_EXECUTION",
    outcome_certification: "NOT_RUN",
    objective: "Determine whether the curated specialist architecture produces better websites with lower or equal owner friction than baseline Website Director.",
    hard_rules: HARD_RULES,
    pass_condition: MINIMUM_PASS_CONDITION,
    freeze_fields: FREEZE_FIELDS,
    scenarios: SCENARIOS,
    metrics: METRICS,
    required_metrics: REQUIRED_METRICS,
    quality_separation: QUALITY_SEPARATION,
    scoring_rubric: SCORING_RUBRIC,
    comparisons: ["BASELINE_WEBSITE_DIRECTOR", "WEBSITE_DIRECTOR_PLUS_CURATED_SPECIALISTS"],
    required_outputs: ["benchmark manifest", "baseline results", "specialist results", "side-by-side comparison", "routing receipts", "quality scores", "defect counts", "token and cost comparison where available", "screenshots and evidence", "anomalies", "limitations", "final certification verdict"],
    allowed_final_verdicts: ["WEBSITE_DIRECTOR_SPECIALIST_OUTCOME_BENCHMARK_PASSED", "WEBSITE_DIRECTOR_SPECIALIST_OUTCOME_BENCHMARK_FAILED", "WEBSITE_DIRECTOR_SPECIALIST_OUTCOME_BENCHMARK_INCONCLUSIVE"],
    stop_after_report: true
  };
}

module.exports = {
  FREEZE_FIELDS,
  REQUIRED_METRICS,
  METRICS,
  HARD_RULES,
  QUALITY_SEPARATION,
  SCORING_RUBRIC,
  SCENARIOS,
  MINIMUM_PASS_CONDITION,
  freezeComparisonPair,
  assertComparablePair,
  createMetricRecord,
  certifyOutcome,
  createBenchmarkPlan
};
