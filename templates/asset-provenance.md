# ASSET PROVENANCE & RIGHTS-EVIDENCE RECORD

> **Project:** [Project Name]  
> **Schema Version:** 2.12.0
> **Governance:** ASSET-DIRECTOR-PROTOCOL.md §13 and EVIDENCE-PROVENANCE-PROTOCOL.md
> **Rule:** Every visual asset used in production must have a traceable origin, evidence of permitted use appropriate to its risk, and an asset-level provenance reference. This record does not certify legal ownership, exclusivity, copyright, or compliance. Reference site imagery from galleries/competitors is strictly prohibited.

---

## 1. Asset Provenance Ledger

| Asset ID | Role | Origin | Creator / Provider | License / Rights Basis | Acquisition Date | Permitted Web Usage | Modifications / Retouching | Evidence Ref | SHA-256 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[asset-01]` | `[ROLE]` | `[ORIGIN]` | `[CREATOR_NAME]` | `[LICENSE_OR_ATTESTATION]` | `[YYYY-MM-DD]` | `[PERMITTED_SCOPE]` | `[MODIFICATIONS]` | `[asset-01]` | `[SHA256]` |

*(Table initializes empty for new projects. Populate as assets are acquired and audited.)*

---

## 2. Generated Media Seed & Prompt Registry (If Applicable)

| Asset ID | Provider / Tool | Prompt / Art Direction Seed | Date Generated | Source Inputs | Output SHA-256 | Artifact Check Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[asset-id]` | [Provider and Tool] | [Exact Art Direction Brief / Seed] | [YYYY-MM-DD] | [Input References] | [SHA256] | [PASS / FAIL] |

---

## 3. Copyright & Third-Party Reference Audit

- **Competitor / Showcase Gallery Asset Ingestion:** [VERIFIED ZERO (0 external reference assets copied)]
- **Stock License Verification:** [Status of stock receipts / licenses]
- **Human Likeness Consent:** [Status of signed model releases / client consent]  
- **Cross-cutting ledger:** [templates/evidence-ledger.json path or project ledger path]
- **Unresolved high-risk items:** [NONE / list]
- **Production approval:** [NOT_APPROVED / owner approval reference]

## 4. Asset Director boundary

Asset Director owns visual asset strategy, generation, selection, optimization,
and readiness. The cross-cutting provenance ledger owns source identity, rights
evidence, attribution, permitted use, and traceability. Keep
assets.provenance_status in site-profile.json distinct from
provenance.complete. A production-ready external or high-risk asset without a
passing ledger reference is blocked.
