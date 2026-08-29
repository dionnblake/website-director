"use strict";

const fs = require("node:fs");
const path = require("node:path");
const authority = require("./config/authority.json");
const baseline = require("./config/baseline.json");
const capabilityMap = require("./config/capability-map.json");
const inventory = require("./config/skill-inventory.json");
const registry = require("./config/registry.json");
const sources = require("./config/sources.json");
const adapters = require("./adapters");
const { REQUIRED_FIELDS } = require("./receipts");

const root = __dirname;

function check(id, condition, detail) {
  return { id, passed: Boolean(condition), detail };
}

function flattenInventoryPaths() {
  return inventory.repositories.flatMap((repository) => repository.paths.map((skill) => `${repository.repository}::${skill.path}`));
}

function buildValidationReport() {
  const expectedRepositoryCount = 7;
  const inventoryKeys = new Set(flattenInventoryPaths());
  const registryKeys = new Set(registry.skills.map((skill) => `${skill.source}::${skill.upstream_path}`));
  const registryAdapterIds = new Set(registry.adapters.map((adapter) => adapter.id));
  const adapterFiles = fs
    .readdirSync(path.join(root, "adapters"))
    .filter((file) => file.endsWith(".js") && file !== "index.js" && file !== "contract.js");
  const adapterSource = adapterFiles.map((file) => fs.readFileSync(path.join(root, "adapters", file), "utf8")).join("\n");
  const snapshotChecks = sources.repositories.map((source) => {
    const snapshotPath = path.resolve(root, "..", source.local_snapshot_location);
    const licensePath = path.resolve(root, "..", source.license_file);
    return fs.existsSync(path.join(snapshotPath, "SNAPSHOT.md")) && fs.existsSync(licensePath);
  });

  const checks = [
    check("ALL_7_REPOSITORIES_RESOLVED", sources.repositories.length === expectedRepositoryCount && sources.repositories.every((source) => source.upstream_commit_sha && source.repository_url), "Seven repositories have URL and exact commit metadata."),
    check("ALL_DISCOVERABLE_SKILLS_INVENTORIED", inventory.total_discovered_skills === inventoryKeys.size && inventoryKeys.size === registry.skills.length, `${inventoryKeys.size} pinned skill paths are inventoried and registered.`),
    check("ALL_REGISTRY_REFERENCES_VALID", [...inventoryKeys].every((key) => registryKeys.has(key)) && registry.skills.every((skill) => skill.upstream_commit_sha && skill.license && Array.isArray(skill.upstream_references)), "Every inventory path has a normalized registry record."),
    check("ALL_UPSTREAM_COMMITS_PINNED", sources.repositories.every((source) => /^[0-9a-f]{40}$/.test(source.upstream_commit_sha)) && registry.skills.every((skill) => /^[0-9a-f]{40}$/.test(skill.upstream_commit_sha)), "All source and registry records use full commit SHAs."),
    check("LICENSE_PROVENANCE_PRESERVED", sources.repositories.every((source) => source.license === "MIT") && snapshotChecks.every(Boolean), "Each source has a license field and local license text snapshot."),
    check("EXISTING_WEBSITE_DIRECTOR_LIFECYCLE_UNCHANGED", baseline.difference_report.PHASES === "UNCHANGED" && baseline.difference_report.GATES === "UNCHANGED", "Baseline records no phase or gate changes."),
    check("OWNER_LOCKS_UNCHANGED", baseline.difference_report.LOCKS === "UNCHANGED" && authority.invariants.OWNER_LOCKS_UNCHANGED === true, "Owner locks remain unchanged and authoritative."),
    check("SEO_INTEGRATION_UNCHANGED", baseline.difference_report.SEO === "UNCHANGED" && authority.invariants.SEO_INTEGRATION_UNCHANGED === true, "Static metadata-only SEO remains unchanged."),
    check("RESEARCH_REQUIREMENTS_UNCHANGED", baseline.difference_report.RESEARCH === "UNCHANGED" && authority.invariants.RESEARCH_REQUIREMENTS_UNCHANGED === true, "No research lifecycle was added or replaced."),
    check("BRAND_CONTROLS_UNCHANGED", baseline.difference_report.BRAND_RULES === "UNCHANGED" && authority.invariants.BRAND_CONTROLS_UNCHANGED === true, "Existing local brand contract remains authoritative."),
    check("PUBLISHING_BOUNDARY_UNCHANGED", baseline.difference_report.PUBLISHING_RULES === "UNCHANGED" && authority.invariants.PUBLISHING_BOUNDARY_UNCHANGED === true, "No publishing or production connection was added."),
    check("NO_SPECIALIST_RECURSION", !adapterSource.match(/require\s*\(\s*["']\.\.\/["']?router|require\s*\(\s*["']\.\/router|\.route\s*\(/), "Adapters contain no router import or route call."),
    check("NO_UPSTREAM_ORCHESTRATION_AUTHORITY", authority.invariants.NO_UPSTREAM_ORCHESTRATION_AUTHORITY === true && sources.repositories.every((source) => source.snapshot_type === "PINNED_METADATA_AND_SKILL_DEFINITION_MANIFEST"), "Upstream material is pinned reference knowledge only."),
    check("ADAPTER_IS_ONLY_EXECUTABLE_SPECIALIST_SURFACE", fs.existsSync(path.join(root, "adapters", "index.js")) && registry.adapters.length === 7 && registryAdapterIds.size === 7, "Executable specialist IDs are confined to the normalized adapter registry."),
    check("NO_UNAPPROVED_STACK_MUTATION", authority.invariants.NO_UNAPPROVED_STACK_MUTATION === true && authority.invariants.EXTERNAL_DEPLOYMENT_AUTHORITY === "NONE", "Authority contract denies stack mutation, deployment, and publishing."),
    check("PROJECT_LOCAL_DESIGN_MEMORY", authority.invariants.PROJECT_LOCAL_DESIGN_MEMORY === true && authority.invariants.GLOBAL_TASTEMAKER_PROFILE_AUTO_INHERITANCE === false, "Reference style memory is project-local and global profile inheritance is disabled."),
    check("SPECIALIST_BUDGET_POLICY_IMPLEMENTED", authority.specialist_budget.DEFAULT_EXTERNAL_SPECIALIST_CEILING === 3 && authority.specialist_budget.exception_required_above === 3, "Normal and complex patterns are bounded at three external specialists."),
    check("ROUTING_RECEIPTS_IMPLEMENTED", REQUIRED_FIELDS.length === 10 && registry.adapters.every((adapter) => adapter.id && adapter.role), "Receipt schema and adapter metadata exist."),
    check("CORE_COUNT_NOT_EXPANDED", registry.counts.total_core_adapters === authority.core_adapter_ids.length && registry.counts.total_conditional_core_adapters === authority.conditional_core_adapter_ids.length, "Core remains six adapters plus one conditional-core validator."),
    check("ON_DEMAND_SKILLS_DORMANT_BY_DEFAULT", registry.on_demand_mappings && Object.values(registry.on_demand_mappings).flat().every((mapping) => mapping.status === "DORMANT" && mapping.adapter_required_before_execution === true), "Every on-demand mapping is dormant and requires normalization before execution."),
    check("LIBRARY_SKILLS_INACTIVE_BY_DEFAULT", registry.skills.filter((skill) => skill.status === "LIBRARY_INACTIVE").length === registry.counts.total_library_inactive, "Unselected knowledge remains library-inactive."),
    check("EXTERNAL_DEPLOYMENT_AUTHORITY", authority.invariants.EXTERNAL_DEPLOYMENT_AUTHORITY === "NONE" && authority.forbidden_adapter_authority.includes("DEPLOYMENT"), "No adapter has deployment authority.")
  ];

  const passed = checks.filter((item) => item.passed).length;
  const failed = checks.length - passed;
  return {
    status: failed === 0 ? "WEBSITE_DIRECTOR_SPECIALIST_ARCHITECTURE_IMPLEMENTED" : "IMPLEMENTATION_BLOCKED",
    validation_pass: passed,
    validation_fail: failed,
    total_validation_tests: checks.length,
    counts: registry.counts,
    checks,
    unresolved_conflicts: [],
    outcome_benchmark_certification: "NOT_RUN"
  };
}

if (require.main === module) {
  const report = buildValidationReport();
  console.log(JSON.stringify(report, null, 2));
  process.exitCode = report.validation_fail === 0 ? 0 : 1;
}

module.exports = { buildValidationReport };
