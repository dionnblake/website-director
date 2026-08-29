"use strict";

const { normalizeContext, boundedResult } = require("./contract");

const ADAPTER_ID = "INTERFACE_QUALITY_VALIDATOR";

const REVIEW_AREAS = [
  "layout",
  "grouping",
  "hierarchy",
  "typography",
  "readability",
  "wrapping",
  "color_semantics",
  "contrast",
  "accessibility",
  "keyboard_usability",
  "focus_states",
  "interface_writing",
  "button_labels",
  "error_states",
  "empty_states",
  "ui_polish",
  "interaction_affordances",
  "responsive_defects",
  "narrow_width_behavior"
];

function evaluate(context = {}) {
  const input = normalizeContext(context, ADAPTER_ID);
  const suppliedFindings = Array.isArray(input.interfaceFindings) ? input.interfaceFindings : [];

  return boundedResult(ADAPTER_ID, "VALIDATOR", input, {
    activation: "CORE",
    upstreamKnowledge: [
      "jakubkrehel/skills:skills/better-layout/SKILL.md",
      "jakubkrehel/skills:skills/better-typography/SKILL.md",
      "jakubkrehel/skills:skills/better-colors/SKILL.md",
      "jakubkrehel/skills:skills/better-accessibility/SKILL.md",
      "jakubkrehel/skills:skills/better-writing/SKILL.md",
      "jakubkrehel/skills:skills/better-ui/SKILL.md"
    ],
    consolidatedReview: true,
    reviewAreas: REVIEW_AREAS,
    findings: suppliedFindings,
    boundedGuidance: [
      "Return one consolidated interface review rather than recursively invoking six upstream skills.",
      "Separate observed defects from recommendations and preserve Website Director ownership of the final decision.",
      "Treat missing evidence as unverified, not as a pass."
    ]
  });
}

module.exports = { ADAPTER_ID, REVIEW_AREAS, evaluate };
