"use strict";

const FORBIDDEN_CONTEXT_FLAGS = [
  "stackMutationRequested",
  "installDependencyRequested",
  "replaceStackRequested",
  "publishRequested",
  "deployRequested",
  "externalWriteRequested"
];

function normalizeContext(context, adapterId) {
  if (!context || typeof context !== "object" || Array.isArray(context)) {
    throw new TypeError(`${adapterId} requires a decision context object`);
  }

  const forbiddenFlag = FORBIDDEN_CONTEXT_FLAGS.find((flag) => context[flag] === true);
  if (forbiddenFlag) {
    throw new Error(`${adapterId} cannot perform ${forbiddenFlag}`);
  }

  return {
    ...context,
    phase: context.phase || "unspecified",
    currentDecision: context.currentDecision || "unspecified",
    projectLocalDesignMemory: context.projectLocalDesignMemory !== false,
    globalTastemakerProfileAutoInheritance: false
  };
}

function boundedResult(adapterId, role, context, payload = {}) {
  return Object.freeze({
    adapterId,
    role,
    decision: context.currentDecision,
    phase: context.phase,
    authorityOwner: "WEBSITE_DIRECTOR",
    bounded: true,
    canSelectSpecialists: false,
    canMutateStack: false,
    canPublish: false,
    canDeploy: false,
    materiallyAffectedOutput: context.materiallyAffectedOutput === true,
    ...payload
  });
}

module.exports = {
  FORBIDDEN_CONTEXT_FLAGS,
  normalizeContext,
  boundedResult
};
