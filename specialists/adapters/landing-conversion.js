"use strict";

const { normalizeContext, boundedResult } = require("./contract");

const ADAPTER_ID = "LANDING_CONVERSION";
const ELIGIBLE_PAGE_TYPES = [
  "homepage",
  "campaign_landing_page",
  "product_landing_page",
  "affiliate_conversion_page",
  "lead_generation_page",
  "sales_page",
  "major_marketing_destination"
];

function evaluate(context = {}) {
  const input = normalizeContext(context, ADAPTER_ID);
  const pageType = String(input.pageType || "").toLowerCase();
  const eligible = ELIGIBLE_PAGE_TYPES.includes(pageType);

  return boundedResult(ADAPTER_ID, "IMPLEMENTATION_SPECIALIST", input, {
    activation: "CORE_CONDITIONAL_BY_PAGE_TYPE",
    upstreamKnowledge: ["elayadesign/ai-design-skills:skills/landing-page-design/SKILL.md"],
    eligible,
    status: eligible ? "ready_for_bounded_guidance" : "not_eligible",
    boundedGuidance: eligible
      ? [
          "Improve page sequencing, message hierarchy, CTA architecture, trust support, lead capture, and friction reduction.",
          "Keep IA, SEO, brand, lifecycle, and owner approval with Website Director."
        ]
      : [],
    findings: []
  });
}

module.exports = { ADAPTER_ID, ELIGIBLE_PAGE_TYPES, evaluate };
