"use strict";

const { normalizeContext, boundedResult } = require("./contract");

const ADAPTER_ID = "MOTION_IMPLEMENTATION";
const MOTION_CLASSES = [
  "NO_MOTION",
  "MICRO_INTERACTION",
  "STATE_TRANSITION",
  "EXPLANATORY_MOTION",
  "MARKETING_MOTION",
  "CINEMATIC_CANDIDATE"
];

function classifyMotion(input) {
  if (MOTION_CLASSES.includes(input.motionClass)) return input.motionClass;
  if (input.cinematicCandidate === true) return "CINEMATIC_CANDIDATE";
  if (input.motionRequested === false) return "NO_MOTION";
  if (input.motionType === "state") return "STATE_TRANSITION";
  if (input.motionType === "explanatory") return "EXPLANATORY_MOTION";
  if (input.motionType === "marketing") return "MARKETING_MOTION";
  return "MICRO_INTERACTION";
}

function evaluate(context = {}) {
  const input = normalizeContext(context, ADAPTER_ID);
  const motionClass = classifyMotion(input);
  const cinematic = motionClass === "CINEMATIC_CANDIDATE";

  return boundedResult(ADAPTER_ID, "IMPLEMENTATION_SPECIALIST", input, {
    activation: "CORE_CONDITIONAL",
    upstreamKnowledge: [
      "emilkowalski/skills:skills/animate/SKILL.md",
      "emilkowalski/skills:skills/emil-design-eng/SKILL.md",
      "emilkowalski/skills:skills/find-animation-opportunities/SKILL.md"
    ],
    motionClass,
    firstQuestion: "SHOULD_THIS_ANIMATE",
    cinematicSpecialistRecommended: cinematic,
    specialistRecommendation: cinematic ? "CINEMATIC_SPECIALIST_RECOMMENDED" : null,
    boundedGuidance: [
      "Choose whether motion is necessary before choosing a technique.",
      "Prefer interruptible, responsive, GPU-safe properties and reduced-motion equivalents.",
      "Use the existing project capability before considering a new library.",
      "Return a recommendation when the decision is cinematic; do not activate another specialist."
    ],
    findings: []
  });
}

module.exports = { ADAPTER_ID, MOTION_CLASSES, classifyMotion, evaluate };
