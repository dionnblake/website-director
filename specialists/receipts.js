"use strict";

const REQUIRED_FIELDS = [
  "SPECIALIST",
  "ADAPTER_ID",
  "TRIGGER",
  "DECISION_OR_PHASE",
  "ROLE",
  "WHY_SELECTED",
  "ALTERNATIVES_CONSIDERED",
  "SPECIALIST_BUDGET_POSITION",
  "MATERIALLY_AFFECTED_OUTPUT",
  "OUTCOME"
];

function createRoutingReceipt(input = {}) {
  const missing = REQUIRED_FIELDS.filter((field) => input[field] === undefined || input[field] === null);
  if (missing.length) {
    throw new Error(`Routing receipt missing required fields: ${missing.join(", ")}`);
  }
  if (!Number.isInteger(input.SPECIALIST_BUDGET_POSITION) || input.SPECIALIST_BUDGET_POSITION < 1) {
    throw new TypeError("SPECIALIST_BUDGET_POSITION must be a positive integer");
  }
  if (!Array.isArray(input.ALTERNATIVES_CONSIDERED)) {
    throw new TypeError("ALTERNATIVES_CONSIDERED must be an array");
  }
  if (typeof input.MATERIALLY_AFFECTED_OUTPUT !== "boolean") {
    throw new TypeError("MATERIALLY_AFFECTED_OUTPUT must be boolean");
  }

  return Object.freeze({
    receipt_version: 1,
    created_at: input.created_at || new Date().toISOString(),
    ...input
  });
}

function validateRoutingReceipt(receipt) {
  return REQUIRED_FIELDS.every((field) => receipt && receipt[field] !== undefined && receipt[field] !== null);
}

module.exports = { REQUIRED_FIELDS, createRoutingReceipt, validateRoutingReceipt };
