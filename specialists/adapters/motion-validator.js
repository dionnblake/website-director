"use strict";

const { normalizeContext, boundedResult } = require("./contract");

const ADAPTER_ID = "MOTION_VALIDATOR";
const REVIEW_AREAS = [
  "necessity",
  "restraint",
  "easing",
  "timing",
  "responsiveness",
  "interruptibility",
  "gpu_safe_properties",
  "hover_gating",
  "pointer_assumptions",
  "reduced_motion",
  "layout_property_animation",
  "repeated_animation_fatigue",
  "performance",
  "consistency"
];

function evaluate(context = {}) {
  const input = normalizeContext(context, ADAPTER_ID);

  return boundedResult(ADAPTER_ID, "VALIDATOR", input, {
    activation: "CORE_CONDITIONAL",
    upstreamKnowledge: [
      "emilkowalski/skills:skills/review-animations/SKILL.md",
      "emilkowalski/skills:skills/improve-animations/SKILL.md"
    ],
    reviewAreas: REVIEW_AREAS,
    selfCertification: false,
    findings: Array.isArray(input.motionFindings) ? input.motionFindings : [],
    boundedGuidance: [
      "Validate the implementation independently from the motion builder.",
      "Flag unnecessary movement, layout-property animation, pointer-only assumptions, and reduced-motion gaps.",
      "Treat performance and responsive evidence as required for a pass."
    ]
  });
}

module.exports = { ADAPTER_ID, REVIEW_AREAS, evaluate };
