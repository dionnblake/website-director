"use strict";

const authority = require("./config/authority.json");
const capabilityMap = require("./config/capability-map.json");
const registry = require("./config/registry.json");
const adapters = require("./adapters");
const { createRoutingReceipt } = require("./receipts");

class RoutingError extends Error {}
class SpecialistBudgetError extends RoutingError {}

const DEFAULT_ROUTE_BUDGET = authority.specialist_budget.DEFAULT_EXTERNAL_SPECIALIST_CEILING;
const adapterRegistry = new Map(registry.adapters.map((adapter) => [adapter.id, adapter]));

function assertBudgetException(exception) {
  const fields = [
    "decision_or_phase",
    "specialists_already_active",
    "additional_specialist_requested",
    "missing_capability",
    "why_existing_specialists_cannot_supply_it",
    "expected_material_contribution"
  ];
  const missing = fields.filter((field) => exception?.[field] === undefined || exception?.[field] === null || exception?.[field] === "");
  if (missing.length) {
    throw new SpecialistBudgetError(`SPECIALIST_BUDGET_EXCEPTION missing: ${missing.join(", ")}`);
  }
  if (!Array.isArray(exception.specialists_already_active)) {
    throw new SpecialistBudgetError("SPECIALIST_BUDGET_EXCEPTION specialists_already_active must be an array");
  }
}

function createRouter() {
  function route(decision = {}) {
    if (!decision || typeof decision !== "object" || Array.isArray(decision)) {
      throw new RoutingError("Website Director routing requires a decision object");
    }

    const capabilityClass = String(decision.capabilityClass || "").toUpperCase();
    const definition = capabilityMap.routes[capabilityClass];
    if (!definition) throw new RoutingError(`No deterministic route for capability class: ${capabilityClass || "unspecified"}`);

    const phase = decision.phase || "unspecified";
    if (phase !== "unspecified" && !definition.allowed_phases.includes(phase)) {
      throw new RoutingError(`${capabilityClass} is not eligible for phase ${phase}`);
    }

    if (definition.requires_explicit_activation && decision.explicitActivation !== true) {
      return {
        authorityOwner: "WEBSITE_DIRECTOR",
        capabilityClass,
        phase,
        selectedAdapters: [],
        receipts: [],
        recommendation: definition.recommendation,
        activation: "DORMANT",
        budget: { used: 0, ceiling: DEFAULT_ROUTE_BUDGET }
      };
    }

    if (
      capabilityClass === "LANDING_CONVERSION" &&
      !adapters.LANDING_CONVERSION.ELIGIBLE_PAGE_TYPES.includes(String(decision.pageType || "").toLowerCase())
    ) {
      return {
        authorityOwner: "WEBSITE_DIRECTOR",
        capabilityClass,
        phase,
        selectedAdapters: [],
        receipts: [],
        recommendation: "LANDING_CONVERSION_NOT_ELIGIBLE_FOR_PAGE_TYPE",
        activation: "DORMANT",
        budget: { used: 0, ceiling: DEFAULT_ROUTE_BUDGET }
      };
    }

    if (definition.primary === null) {
      return {
        authorityOwner: "WEBSITE_DIRECTOR",
        capabilityClass,
        phase,
        selectedAdapters: [],
        receipts: [],
        recommendation: definition.recommendation || "NO_ADAPTER_REGISTERED",
        activation: "DORMANT",
        budget: { used: 0, ceiling: DEFAULT_ROUTE_BUDGET }
      };
    }

    const selectedAdapters = [definition.primary];
    let recommendation = definition.recommendation || null;
    if (definition.secondary && decision.includeSecondary === true) {
      if (adapters[definition.secondary]) {
        selectedAdapters.push(definition.secondary);
      } else {
        recommendation = "NORMALIZED_ADAPTER_REQUIRED_BEFORE_EXECUTION";
      }
    }
    if (definition.validator) selectedAdapters.push(definition.validator);

    const ceiling = Number.isInteger(decision.specialistBudget) ? decision.specialistBudget : DEFAULT_ROUTE_BUDGET;
    if (selectedAdapters.length > ceiling) {
      if (!decision.specialistBudgetException) {
        throw new SpecialistBudgetError("SPECIALIST_BUDGET_EXCEPTION required when the decision exceeds its specialist ceiling");
      }
      assertBudgetException(decision.specialistBudgetException);
    }

    const alternatives = Object.values(capabilityMap.routes)
      .flatMap((candidate) => [candidate.primary, candidate.secondary, candidate.validator])
      .filter(Boolean)
      .filter((id) => !selectedAdapters.includes(id));

    const receipts = selectedAdapters.map((adapterId, index) => {
      const adapter = adapters[adapterId];
      if (!adapter) throw new RoutingError(`Adapter is not executable or registered: ${adapterId}`);
      return createRoutingReceipt({
        SPECIALIST: adapterRegistry.get(adapterId)?.source || adapterId,
        ADAPTER_ID: adapterId,
        TRIGGER: decision.trigger || capabilityClass,
        DECISION_OR_PHASE: decision.currentDecision || phase,
        ROLE: adapterRegistry.get(adapterId)?.role || (adapterId.endsWith("VALIDATOR") ? "VALIDATOR" : index === 0 ? "PRIMARY" : "SECONDARY"),
        WHY_SELECTED: decision.whySelected || `Deterministic ${capabilityClass} route for the current Website Director decision`,
        ALTERNATIVES_CONSIDERED: alternatives,
        SPECIALIST_BUDGET_POSITION: index + 1,
        MATERIALLY_AFFECTED_OUTPUT: decision.materiallyAffectedOutput === true,
        OUTCOME: "ROUTED",
        ...(decision.specialistBudgetException ? { SPECIALIST_BUDGET_EXCEPTION: decision.specialistBudgetException } : {})
      });
    });

    return {
      authorityOwner: "WEBSITE_DIRECTOR",
      capabilityClass,
      phase,
      activation: definition.activation,
      selectedAdapters,
      receipts,
      recommendation,
      budget: {
        used: selectedAdapters.length,
        ceiling,
        exception: decision.specialistBudgetException || null
      }
    };
  }

  function activate(plan, context = {}) {
    if (!plan || plan.authorityOwner !== "WEBSITE_DIRECTOR") {
      throw new RoutingError("Only Website Director may activate a routing plan");
    }
    return plan.selectedAdapters.map((adapterId) => {
      const adapter = adapters[adapterId];
      if (!adapter || typeof adapter.evaluate !== "function") {
        throw new RoutingError(`No normalized executable adapter for ${adapterId}`);
      }
      return adapter.evaluate({
        ...context,
        phase: context.phase || plan.phase,
        currentDecision: context.currentDecision || plan.capabilityClass
      });
    });
  }

  function routeAndActivate(decision = {}, context = {}) {
    const plan = route(decision);
    return { plan, results: activate(plan, context) };
  }

  return Object.freeze({ route, activate, routeAndActivate });
}

module.exports = {
  DEFAULT_ROUTE_BUDGET,
  RoutingError,
  SpecialistBudgetError,
  assertBudgetException,
  createRouter
};
