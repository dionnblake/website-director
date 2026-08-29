"use strict";

const { normalizeContext, boundedResult } = require("./contract");

const ADAPTER_ID = "REFERENCE_STYLE_GROUNDING";

function evaluate(context = {}) {
  const input = normalizeContext(context, ADAPTER_ID);
  const references = Array.isArray(input.referenceField) ? input.referenceField : [];
  const antiReferences = Array.isArray(input.antiReferences) ? input.antiReferences : [];

  return boundedResult(ADAPTER_ID, "IMPLEMENTATION_SPECIALIST", input, {
    activation: "CORE_CONDITIONAL",
    upstreamKnowledge: [
      "codeswithroh/tastemaker:skills/tastemaker/SKILL.md",
      "codeswithroh/tastemaker:skills/tastemaker/ideagram/SKILL.md"
    ],
    projectLocalMemory: {
      enabled: true,
      references,
      antiReferences,
      styleLock: input.styleLock || null,
      globalProfileInherited: false
    },
    boundedGuidance: [
      "Ground the visual thesis in the supplied project references.",
      "Record anti-references and structural diversification rules.",
      "Treat palette, contrast, typography direction, and style lock as inputs to Website Director judgment.",
      "Return design guidance only; do not own IA, SEO, conversion, publishing, or approval."
    ],
    findings: []
  });
}

module.exports = { ADAPTER_ID, evaluate };
