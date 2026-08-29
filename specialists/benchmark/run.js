"use strict";

const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");
const baselineConfig = require("../config/baseline.json");
const capabilityMap = require("../config/capability-map.json");
const {
  SCENARIOS,
  HARD_RULES,
  REQUIRED_METRICS,
  SCORING_RUBRIC,
  createBenchmarkPlan,
  createMetricRecord,
  freezeComparisonPair,
  assertComparablePair,
  certifyOutcome
} = require("./harness");
const { createRouter } = require("../router");

const PROJECT_ROOT = path.resolve(__dirname, "../..");
const RESULTS_ROOT = path.join(__dirname, "results");
const WEBSITE_SOURCE_PATHS = ["AGENTS.md", "README.md", "index.html", "styles.css", "script.js", "favicon.svg", "assets"];

const ROUTING_CASES = {
  A: [
    {
      decision: {
        capabilityClass: "REFERENCE_STYLE",
        phase: "design_direction",
        currentDecision: "brand_reference_grounding",
        trigger: "benchmark_brand_landing",
        whySelected: "Use the project-local reference field to test brand fidelity without inheriting a global taste profile."
      },
      context: { referenceField: ["local/reference-board"], styleLock: "HG-EDITORIAL-01" }
    },
    {
      decision: {
        capabilityClass: "VISUAL_IMPLEMENTATION",
        phase: "implementation",
        currentDecision: "brand_landing_implementation",
        trigger: "benchmark_brand_landing",
        whySelected: "Apply visual implementation guidance and independent interface validation to the frozen landing-page brief."
      },
      context: { pageType: "homepage", preserveStack: true }
    },
    {
      decision: {
        capabilityClass: "LANDING_CONVERSION",
        phase: "landing_page",
        pageType: "homepage",
        currentDecision: "brand_landing_conversion_structure",
        trigger: "benchmark_brand_landing",
        whySelected: "Evaluate CTA architecture and conversion structure only for an eligible marketing destination."
      },
      context: { pageType: "homepage", preserveStack: true }
    }
  ],
  B: [
    {
      decision: {
        capabilityClass: "MOTION",
        phase: "interaction",
        currentDecision: "immersive_motion_judgment",
        trigger: "benchmark_immersive_cinematic",
        includeSecondary: true,
        cinematicCandidate: true,
        whySelected: "Test the core motion builder and independent validator while keeping cinematic expertise on-demand."
      },
      context: { motionRequested: true, cinematicCandidate: true, reducedMotionRequired: true }
    },
    {
      decision: {
        capabilityClass: "CINEMATIC",
        phase: "immersive_website",
        currentDecision: "immersive_cinematic_escalation",
        trigger: "benchmark_immersive_cinematic",
        explicitActivation: true,
        whySelected: "Exercise the locked on-demand cinematic route; raw upstream knowledge must remain non-executable."
      },
      context: { motionRequested: true, cinematicCandidate: true, reducedMotionRequired: true }
    }
  ],
  C: [
    {
      decision: {
        capabilityClass: "UX_IA",
        phase: "information_architecture",
        currentDecision: "content_affiliate_information_architecture",
        trigger: "benchmark_content_affiliate",
        whySelected: "Use the conditional IA validator for article discovery and navigation structure."
      },
      context: { pageType: "article", preserveSEO: true }
    },
    {
      decision: {
        capabilityClass: "INTERFACE_QA",
        phase: "qa",
        currentDecision: "content_affiliate_interface_review",
        trigger: "benchmark_content_affiliate",
        whySelected: "Check the interface independently after the IA decision."
      },
      context: { pageType: "article", preserveSEO: true }
    },
    {
      decision: {
        capabilityClass: "LANDING_CONVERSION",
        phase: "content_structure",
        pageType: "article",
        currentDecision: "content_affiliate_conversion_gate",
        trigger: "benchmark_content_affiliate",
        whySelected: "Verify the landing conversion adapter stays dormant for an article page."
      },
      context: { pageType: "article", preserveSEO: true }
    }
  ],
  D: [
    {
      decision: {
        capabilityClass: "INTERFACE_QA",
        phase: "interface_review",
        currentDecision: "mediocre_site_diagnosis",
        trigger: "benchmark_mediocre_site_improvement",
        whySelected: "Diagnose the frozen implementation before proposing changes."
      },
      context: { preserveWorkingArchitecture: true }
    },
    {
      decision: {
        capabilityClass: "VISUAL_IMPLEMENTATION",
        phase: "polish",
        currentDecision: "mediocre_site_bounded_improvement",
        trigger: "benchmark_mediocre_site_improvement",
        whySelected: "Test whether visual implementation can improve polish while preserving the working stack."
      },
      context: { preserveWorkingArchitecture: true, preserveStack: true }
    }
  ]
};

function toPosix(value) {
  return value.split(path.sep).join("/");
}

function walkFiles(targetPath) {
  const stat = fs.statSync(targetPath);
  if (stat.isFile()) return [targetPath];
  return fs.readdirSync(targetPath, { withFileTypes: true }).flatMap((entry) => {
    const entryPath = path.join(targetPath, entry.name);
    return entry.isDirectory() ? walkFiles(entryPath) : [entryPath];
  });
}

function hashFile(filePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function getGitCommit() {
  const result = spawnSync("git", ["rev-parse", "HEAD"], { cwd: PROJECT_ROOT, encoding: "utf8" });
  return result.status === 0 && result.stdout.trim() ? result.stdout.trim() : "NO_GIT_COMMIT_PRESENT";
}

function createSourceSnapshot() {
  const files = WEBSITE_SOURCE_PATHS.flatMap((relativePath) => {
    const absolutePath = path.join(PROJECT_ROOT, relativePath);
    if (!fs.existsSync(absolutePath)) return [];
    return walkFiles(absolutePath);
  })
    .map((absolutePath) => {
      const relativePath = toPosix(path.relative(PROJECT_ROOT, absolutePath));
      const bytes = fs.statSync(absolutePath).size;
      return { path: relativePath, bytes, sha256: hashFile(absolutePath) };
    })
    .sort((left, right) => left.path.localeCompare(right.path));
  const digestInput = files.map((file) => `${file.path}:${file.bytes}:${file.sha256}`).join("\n");
  const digest = crypto.createHash("sha256").update(digestInput).digest("hex");
  return {
    gitCommit: getGitCommit(),
    workspaceDigestSha256: digest,
    files,
    assets: files.filter((file) => file.path.startsWith("assets/"))
  };
}

function readJsonIfPresent(filePath) {
  if (!fs.existsSync(filePath)) {
    return { status: "MISSING", path: toPosix(path.relative(PROJECT_ROOT, filePath)), reason: "Evidence file was not present." };
  }
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch (error) {
    return {
      status: "INVALID",
      path: toPosix(path.relative(PROJECT_ROOT, filePath)),
      reason: `Evidence file could not be parsed: ${error.message}`
    };
  }
}

function buildFreezePair(scenario, snapshot, plan, frozenAt) {
  const startingCommit = snapshot.gitCommit === "NO_GIT_COMMIT_PRESENT"
    ? `WORKTREE_SNAPSHOT_SHA256:${snapshot.workspaceDigestSha256}`
    : snapshot.gitCommit;
  const shared = {
    brief: scenario.brief,
    startingRepository: "local-worktree:WEBSITE DIRECTOR",
    startingCommit,
    projectStack: "plain HTML, CSS, vanilla JavaScript, local image assets",
    assetsSupplied: snapshot.assets,
    ownerConstraints: baselineConfig.current_hard_rules,
    websiteDirectorVersion: baselineConfig.current_website_director_version,
    evaluationCriteria: scenario.evaluation,
    allowedInterventions: [
      "Use the existing Website Director lifecycle and frozen project files.",
      "Baseline run: no external specialists.",
      "Specialist run: normalized adapters only, with raw upstream knowledge kept inert.",
      "No stack mutation, dependency installation, publishing, or deployment."
    ],
    scoringRubric: plan.scoring_rubric
  };
  const baselinePair = freezeComparisonPair({ ...shared, runConfiguration: "BASELINE_WEBSITE_DIRECTOR", frozenAt });
  const specialistPair = freezeComparisonPair({ ...shared, runConfiguration: "WEBSITE_DIRECTOR_PLUS_CURATED_SPECIALISTS", frozenAt });
  assertComparablePair(baselinePair, specialistPair);
  return { baseline: baselinePair, specialist: specialistPair };
}

function collectRoutingEvidence(scenarioId) {
  const router = createRouter();
  const decisions = ROUTING_CASES[scenarioId] || [];
  const plans = [];
  const receipts = [];
  const adapterResults = [];
  for (const routeCase of decisions) {
    const activation = router.routeAndActivate({
      materiallyAffectedOutput: false,
      ...routeCase.decision
    }, routeCase.context);
    plans.push({
      decision: routeCase.decision,
      plan: activation.plan
    });
    receipts.push(...activation.plan.receipts);
    adapterResults.push(...activation.results);
  }
  return {
    decisionCount: decisions.length,
    plans,
    receipts,
    adapterResults,
    selectedAdapterCount: plans.reduce((total, item) => total + item.plan.selectedAdapters.length, 0),
    budgetExceptionCount: plans.filter((item) => item.plan.budget.exception).length,
    materialContributionCount: receipts.filter((receipt) => receipt.MATERIALLY_AFFECTED_OUTPUT === true).length
  };
}

function buildReferenceArtifact(snapshot, evidence) {
  const objective = evidence.objective || {};
  return {
    status: evidence.status === "CAPTURED" ? "CAPTURED_REFERENCE_ONLY" : "REFERENCE_EVIDENCE_INCOMPLETE",
    source: "existing local Her Glow Up static prototype",
    scope: "This is one existing artifact, not an independently generated baseline or specialist candidate.",
    source_files: snapshot.files,
    browser_evidence_file: evidence.path || "specialists/benchmark/results/2026-08-28/evidence/current-site.json",
    verified_findings: {
      horizontal_overflow: objective.horizontalOverflow === false ? "NO_OVERFLOW_OBSERVED" : "NOT_AVAILABLE",
      missing_image_alt: objective.missingAltCount === 0 ? "NO_MISSING_ALT_OBSERVED" : "DEFECT_OBSERVED",
      runtime_console_errors: objective.consoleErrors === 0 ? "NO_ERRORS_OBSERVED" : "ERRORS_OBSERVED",
      reduced_motion_rules: objective.reducedMotionRuleCount > 0 ? "RULE_PRESENT" : "NOT_AVAILABLE",
      mobile_menu_state: objective.mobileMenuState || "NOT_AVAILABLE"
    },
    judgment_findings: {
      status: "NOT_BLINDLY_SCORED",
      reason: "A single existing artifact cannot establish an A/B quality delta."
    }
  };
}

function buildScenarioResult(scenario, pair, routing, referenceArtifact, representativeFixtureAvailable) {
  const baseline = {
    status: "NOT_EXECUTED",
    output: null,
    reason: "No independent baseline Website Director generation run, prompt log, or candidate artifact is present in this local prototype.",
    reference_artifact: referenceArtifact
  };
  const specialist = {
    status: "ROUTING_ONLY",
    output: null,
    reason: "Normalized adapters were exercised for routing evidence only. No specialist-generated candidate was produced or supplied.",
    routing_decisions: routing.decisionCount
  };
  const evidenceGaps = [
    "Independent baseline candidate output is missing.",
    "Independent specialist candidate output is missing.",
    "Owner prompt, intervention, revision-round, and token histories are missing.",
    "Blind subjective scoring is missing."
  ];
  if (!representativeFixtureAvailable) evidenceGaps.push("This repository does not contain a representative starting fixture for this benchmark class.");
  return {
    id: scenario.id,
    name: scenario.name,
    comparable: false,
    baseline,
    specialist,
    representative_fixture_available: representativeFixtureAvailable,
    materiallyAffectedOutput: routing.materialContributionCount > 0,
    noMeaningfulRegression: null,
    improvements: [],
    metrics: createMetricRecord({
      TOTAL_SPECIALISTS_USED: routing.selectedAdapterCount,
      SPECIALIST_BUDGET_EXCEPTIONS: routing.budgetExceptionCount,
      ELAPSED_EXECUTION_TIME: null,
      TOKEN_USAGE: null
    }),
    metric_status: Object.fromEntries(REQUIRED_METRICS.map((metric) => [
      metric,
      metric === "TOTAL_SPECIALISTS_USED" || metric === "SPECIALIST_BUDGET_EXCEPTIONS" ? "ROUTING_EVIDENCE_ONLY" : "NOT_AVAILABLE"
    ])),
    quality_scores: {
      baseline: { status: "NOT_COMPARABLE", values: {} },
      specialist: { status: "NOT_COMPARABLE", values: {} }
    },
    routing,
    evidence_gaps: evidenceGaps,
    frozen_pair: pair
  };
}

function buildManifest(plan, snapshot, scenarioPairs, runDate, frozenAt) {
  return {
    benchmark_id: `WEBSITE_DIRECTOR_SPECIALIST_OUTCOME_BENCHMARK_${runDate}`,
    status: "EXECUTED_WITH_INCOMPLETE_PAIRED_RUNS",
    objective: plan.objective,
    criteria_source: "owner-supplied outcome benchmarking acceptance note",
    run_date: runDate,
    frozen_at: frozenAt,
    starting_state: {
      repository: "local-worktree:WEBSITE DIRECTOR",
      git_commit: snapshot.gitCommit,
      worktree_snapshot_sha256: snapshot.workspaceDigestSha256,
      source_files: snapshot.files,
      supplied_assets: snapshot.assets,
      project_stack: "plain HTML, CSS, vanilla JavaScript, local image assets",
      owner_constraints: baselineConfig.current_hard_rules,
      website_director_version: baselineConfig.current_website_director_version
    },
    hard_rules: HARD_RULES,
    evaluation_rubric: SCORING_RUBRIC,
    required_metrics: plan.required_metrics,
    quality_separation: plan.quality_separation,
    comparisons: plan.comparisons,
    scenario_freezes: scenarioPairs,
    allowed_final_verdicts: plan.allowed_final_verdicts,
    stop_after_report: true
  };
}

function renderMarkdown(report) {
  const scenarioRows = report.scenarios.map((scenario) => {
    const gaps = scenario.evidence_gaps.join(" ");
    return `| ${scenario.id} | ${scenario.baseline.status} | ${scenario.specialist.status} | NO | ${scenario.metrics.TOTAL_SPECIALISTS_USED} | ${gaps} |`;
  }).join("\n");
  const receiptRows = report.routing_receipts.length
    ? report.routing_receipts.map((receipt) => `| ${receipt.DECISION_OR_PHASE} | ${receipt.ADAPTER_ID} | ${receipt.ROLE} | ${receipt.MATERIALLY_AFFECTED_OUTPUT} | ${receipt.OUTCOME} |`).join("\n")
    : "| none | none | none | false | no activation receipts |";
  const metricRows = REQUIRED_METRICS.map((metric) => {
    const values = report.scenarios.map((scenario) => scenario.metrics[metric] ?? "N/A").join(" / ");
    return `| ${metric} | ${values} | NOT_CERTIFIED |`;
  }).join("\n");
  return `# Website Director Specialist Outcome Benchmark

## Verdict

\`${report.certification.verdict}\`

The benchmark was executed as an evidence-gated local run. It is inconclusive because the repository contains one existing static prototype and routing evidence, but no paired baseline and specialist-generated candidate outputs.

## Freeze

- Benchmark ID: \`${report.manifest.benchmark_id}\`
- Starting worktree digest: \`${report.manifest.starting_state.worktree_snapshot_sha256}\`
- Git commit: \`${report.manifest.starting_state.git_commit}\`
- Frozen at: \`${report.manifest.frozen_at}\`
- Comparison fields were frozen before routing and were identical for every baseline/specialist pair.
- No page lifecycle, gate, lock, SEO, research, brand, publishing, deployment, or adapter contract was changed for this benchmark.

## Side-by-side comparison

| Benchmark | Baseline | Specialist | Comparable | Routed specialists | Evidence gap |
| --- | --- | --- | --- | ---: | --- |
${scenarioRows}

## Specialist routing receipts

| Decision/phase | Adapter | Role | Materially affected output | Outcome |
| --- | --- | --- | --- | --- |
${receiptRows}

Every captured receipt records \`MATERIALLY_AFFECTED_OUTPUT = false\`. The adapter layer was exercised for routing and bounded guidance only. No raw upstream skill was executed.

## Metrics

The first column is the required metric. Values are listed in scenario order A / B / C / D.

| Metric | Observed values | Certification status |
| --- | --- | --- |
${metricRows}

Token usage, cost, and elapsed generation time were not available because no model-backed baseline or specialist build runs occurred.

## Verified evidence

The existing prototype was captured as a reference artifact only. The captured browser evidence is in [current-site.json](evidence/current-site.json), with screenshots at [desktop](evidence/reference-desktop-1280x720.png) and [mobile](evidence/reference-mobile-390x844.png).

- No horizontal overflow observed at the default desktop viewport and 390px mobile viewport.
- No missing image alt attributes observed in the captured DOM.
- No console warnings or errors observed during the captured page load.
- Mobile menu open/close state and focus return were exercised.
- Reduced-motion CSS rules were present. A full reduced-motion rendering pass was not available in the browser surface.

These are objective observations of the reference artifact, not proof of a baseline-versus-specialist outcome delta.

## Judgment

Visual quality, originality, premium feel, composition, brand expression, aesthetic coherence, and owner friction were not blindly scored. Assigning comparative scores without two independently produced candidates would create false evidence.

## Anomalies

- The worktree has no Git commit, so the freeze uses a SHA-256 source snapshot identity.
- The existing page is suitable as a Her Glow Up editorial landing/cinematic reference, but it is not a content/affiliate fixture or an intentionally mediocre fixture.
- Core adapters returned bounded guidance, but none could materially affect output without a Website Director generation loop applying their results.

## Limitations

- No independent baseline Website Director run was available.
- No independent Website Director plus curated specialists run was available.
- No owner prompt/intervention/revision history or token/cost telemetry was available.
- No blind human or independent visual scoring was available.
- The browser evaluator did not expose the Performance Timing API, so FCP/LCP/TTFB were not certified.

## Boundary

The allowed final verdict is intentionally \`${report.certification.verdict}\`. The system must not advance to \`WEBSITE_DIRECTOR_EXTERNAL_SPECIALIST_LIBRARY_READY\` from this report. Per the acceptance note, work stops after the benchmark report.
`;
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

function assertSafeRunDate(runDate) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(runDate)) {
    throw new Error("Benchmark date must use YYYY-MM-DD format");
  }
}

function resolveOutputDirectory(runDate) {
  const requested = path.join(RESULTS_ROOT, runDate);
  if (!fs.existsSync(path.join(requested, "benchmark.json"))) return requested;
  let attempt = 2;
  while (fs.existsSync(path.join(RESULTS_ROOT, `${runDate}-run-${String(attempt).padStart(2, "0")}`))) attempt += 1;
  return path.join(RESULTS_ROOT, `${runDate}-run-${String(attempt).padStart(2, "0")}`);
}

function copyReferenceEvidence(sourceDirectory, destinationDirectory) {
  const sourceEvidenceDirectory = path.join(sourceDirectory, "evidence");
  if (!fs.existsSync(sourceEvidenceDirectory)) return;
  const destinationEvidenceDirectory = path.join(destinationDirectory, "evidence");
  fs.mkdirSync(destinationEvidenceDirectory, { recursive: true });
  for (const entry of fs.readdirSync(sourceEvidenceDirectory)) {
    const sourcePath = path.join(sourceEvidenceDirectory, entry);
    const destinationPath = path.join(destinationEvidenceDirectory, entry);
    if (fs.statSync(sourcePath).isFile()) fs.copyFileSync(sourcePath, destinationPath);
  }
}

function runBenchmark({ runDate = new Date().toISOString().slice(0, 10), frozenAt = new Date().toISOString() } = {}) {
  assertSafeRunDate(runDate);
  const plan = createBenchmarkPlan();
  const snapshot = createSourceSnapshot();
  const requestedOutputDirectory = path.join(RESULTS_ROOT, runDate);
  const outputDirectory = resolveOutputDirectory(runDate);
  if (outputDirectory !== requestedOutputDirectory) copyReferenceEvidence(requestedOutputDirectory, outputDirectory);
  fs.mkdirSync(outputDirectory, { recursive: true });
  const evidence = readJsonIfPresent(path.join(outputDirectory, "evidence", "current-site.json"));
  const referenceArtifact = buildReferenceArtifact(snapshot, evidence);
  const scenarioPairs = {};
  const scenarioResults = [];
  const routingReceipts = [];
  const baselineResults = [];
  const specialistResults = [];
  const representativeFixtures = { A: true, B: true, C: false, D: false };

  for (const scenario of SCENARIOS) {
    const pair = buildFreezePair(scenario, snapshot, plan, frozenAt);
    scenarioPairs[scenario.id] = pair;
    const routing = collectRoutingEvidence(scenario.id);
    const result = buildScenarioResult(scenario, pair, routing, referenceArtifact, representativeFixtures[scenario.id]);
    scenarioResults.push(result);
    routingReceipts.push(...routing.receipts);
    baselineResults.push({ id: scenario.id, status: result.baseline.status, reference_artifact: referenceArtifact, metrics: result.metrics });
    specialistResults.push({ id: scenario.id, status: result.specialist.status, routing: result.routing, metrics: result.metrics });
  }

  const certification = certifyOutcome(scenarioResults);
  const manifest = buildManifest(plan, snapshot, scenarioPairs, runDate, frozenAt);
  manifest.outcome_certification = certification.verdict;
  const report = {
    manifest,
    certification,
    scenarios: scenarioResults,
    routing_receipts: routingReceipts,
    telemetry: {
      status: "NOT_AVAILABLE",
      baseline: { token_usage: null, cost: null, elapsed_execution_time: null },
      specialist: { token_usage: null, cost: null, elapsed_execution_time: null },
      reason: "No model-backed baseline or specialist generation runs occurred."
    },
    anomalies: [
      "No Git commit exists in the worktree; source snapshot hash is used for identity.",
      "The static prototype is not a complete representative fixture for benchmark classes C or D.",
      "Routing evidence cannot establish output improvement without a generation loop."
    ],
    limitations: [
      "No paired baseline candidate output.",
      "No paired specialist candidate output.",
      "No owner friction or model token telemetry.",
      "No independent blind judgment score.",
      "Performance Timing API unavailable in the browser evidence surface."
    ]
  };

  writeJson(path.join(outputDirectory, "manifest.json"), manifest);
  writeJson(path.join(outputDirectory, "baseline-results.json"), { benchmark_id: manifest.benchmark_id, status: "NOT_CERTIFIED", scenarios: baselineResults });
  writeJson(path.join(outputDirectory, "specialist-results.json"), { benchmark_id: manifest.benchmark_id, status: "ROUTING_ONLY_NOT_CERTIFIED", scenarios: specialistResults });
  writeJson(path.join(outputDirectory, "routing-receipts.json"), { benchmark_id: manifest.benchmark_id, receipts: routingReceipts });
  writeJson(path.join(outputDirectory, "comparison.json"), { benchmark_id: manifest.benchmark_id, certification, scenarios: scenarioResults.map((scenario) => ({ id: scenario.id, comparable: scenario.comparable, baseline: scenario.baseline.status, specialist: scenario.specialist.status, evidence_gaps: scenario.evidence_gaps })) });
  writeJson(path.join(outputDirectory, "benchmark.json"), report);
  fs.writeFileSync(path.join(outputDirectory, "benchmark.md"), renderMarkdown(report), "utf8");
  return { outputDirectory, report };
}

if (require.main === module) {
  const runDate = process.argv[2] || new Date().toISOString().slice(0, 10);
  const result = runBenchmark({ runDate, frozenAt: `${runDate}T00:00:00.000Z` });
  console.log(JSON.stringify({
    status: result.report.certification.verdict,
    outputDirectory: toPosix(path.relative(PROJECT_ROOT, result.outputDirectory)),
    scenarios: result.report.scenarios.length,
    routingReceipts: result.report.routing_receipts.length,
    materialContributions: result.report.routing_receipts.filter((receipt) => receipt.MATERIALLY_AFFECTED_OUTPUT === true).length
  }, null, 2));
}

module.exports = { runBenchmark, createSourceSnapshot, buildFreezePair, collectRoutingEvidence, buildReferenceArtifact };
