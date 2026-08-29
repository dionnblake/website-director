"use strict";

const { normalizeContext, boundedResult } = require("./contract");

const ADAPTER_ID = "UX_IA_VALIDATOR";
const REVIEW_AREAS = [
  "navigation",
  "hierarchy",
  "reading_order",
  "information_grouping",
  "content_discovery",
  "progressive_disclosure",
  "page_relationships",
  "flow_structure",
  "mobile_navigation",
  "task_progression"
];

function evaluate(context = {}) {
  const input = normalizeContext(context, ADAPTER_ID);

  return boundedResult(ADAPTER_ID, "VALIDATOR", input, {
    activation: "CONDITIONAL_CORE",
    upstreamKnowledge: [
      "Owl-Listener/designer-skills:ux-strategy/skills/information-architecture/SKILL.md",
      "Owl-Listener/designer-skills:interaction-design/skills/navigation-patterns/SKILL.md",
      "Owl-Listener/designer-skills:ux-strategy/skills/experience-map/SKILL.md"
    ],
    reviewAreas: REVIEW_AREAS,
    findings: Array.isArray(input.iaFindings) ? input.iaFindings : [],
    boundedGuidance: [
      "Challenge navigation, hierarchy, discovery, and flow when Website Director activates this conditional validator.",
      "Do not replace the existing architecture or research lifecycle independently."
    ]
  });
}

module.exports = { ADAPTER_ID, REVIEW_AREAS, evaluate };
