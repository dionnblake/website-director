"use strict";

const { normalizeContext, boundedResult } = require("./contract");

const ADAPTER_ID = "VISUAL_IMPLEMENTATION";

function evaluate(context = {}) {
  const input = normalizeContext(context, ADAPTER_ID);

  return boundedResult(ADAPTER_ID, "IMPLEMENTATION_SPECIALIST", input, {
    activation: "CORE",
    upstreamKnowledge: ["ConardLi/garden-skills:skills/web-design-engineer/SKILL.md"],
    stackPolicy: "preserve_existing_healthy_project_capability",
    boundedGuidance: [
      "Convert already-approved research, brand, IA, content, SEO, and design direction into frontend implementation.",
      "Use the existing project stack and preserve healthy architecture.",
      "Prioritize hierarchy, responsive composition, component coherence, interaction detail, and anti-generic execution.",
      "Report a dependency recommendation as guidance only; never install or replace a stack."
    ],
    findings: []
  });
}

module.exports = { ADAPTER_ID, evaluate };
