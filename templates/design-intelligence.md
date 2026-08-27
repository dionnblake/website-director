# DESIGN INTELLIGENCE & CANDIDATE SYNTHESIS REPORT

> **Project Name:** [Insert Project Name]  
> **Evaluation Date:** [YYYY-MM-DD]  
> **Protocol:** `DESIGN-INTELLIGENCE-PROTOCOL.md` (Website Director V1.4.0)  
> **Source Engine:** UI/UX Pro Max Design Intelligence (v2.13.0, SHA: `e4f45473691e4b389519ee4bc359a3d6df666c26`)  
> **Readiness Gate:** `[DESIGN_INTELLIGENCE_COMPLETE]`  

---

## 1. Project Context & Query Metadata

| Metadata Field | Project Value |
| :--- | :--- |
| **Product / Site Type** | [e.g., Fintech Wealth Management Platform] |
| **Primary Industry** | [e.g., Financial Services / Private Wealth] |
| **Target Audience** | [e.g., High-Net-Worth Individuals & Family Offices] |
| **Approved Tech Stack** | [e.g., Next.js 14, Tailwind CSS, TypeScript] |
| **Fixed Brand Assets** | [e.g., Logo provided; Primary Color #0A192F fixed by client] |

---

## 2. Industry & Audience Intelligence

- **Target Audience Mindset:** [Summary of expectations and cognitive load tolerance]
- **Key Industry Traits:** [e.g., Institutional stability, data privacy, analytical precision]
- **Layout Strategy Recommendation:** [e.g., Asymmetric editorial split with modular metrics]
- **Trust Builders Required:** [e.g., SEC registration notice, SOC2 Type II badge, audited case studies]
- **Common Domain Pitfalls:** [e.g., Excessive flashy animations, confusing tiered pricing, generic stock photos]

---

## 3. Candidate Styles & Selection Rationale

| Candidate Style ID | Category | Key Characteristics & Effects | Fit Score | Status (`SELECTED` / `REJECTED`) | Selection / Rejection Rationale |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **1. [Style ID 1]** | [Category] | [Effects / Radius / Geometry] | [High/Med] | `[SELECTED]` | [Rationale why this embodies brand] |
| **2. [Style ID 2]** | [Category] | [Effects / Radius / Geometry] | [High/Med] | `[REJECTED]` | [Rationale why rejected] |
| **3. [Style ID 3]** | [Category] | [Effects / Radius / Geometry] | [High/Med] | `[REJECTED]` | [Rationale why rejected] |

### Style Combination Governance (If Applicable):
- **Primary Style (80%):** `[Primary Style Name]`
- **Supporting Style (20%):** `[Supporting Style Name]`
- **Supporting Scope:** `[e.g., Hero canvas and interactive card hover states only]`
- **Conflict Check:** `VERIFIED (Zero token or typographic collisions)`

---

## 4. Color & Palette Synthesis

| Token Role | Recommended Value | Final Selected Value | Source / Justification |
| :--- | :--- | :--- | :--- |
| **Primary** | `[Hex / HSL]` | `[Hex / HSL]` | `[Client Brand Lock / UIUX Recommendation]` |
| **On Primary** | `[Hex / HSL]` | `[Hex / HSL]` | `[Contrast Math Verified $\ge 4.5:1$]` |
| **Secondary** | `[Hex / HSL]` | `[Hex / HSL]` | `[Harmonious Supporting Accent]` |
| **Accent** | `[Hex / HSL]` | `[Hex / HSL]` | `[Conversion CTA Focal Color]` |
| **Background** | `[Hex / HSL]` | `[Hex / HSL]` | `[Surface Luminance Plane]` |
| **Card / Surface** | `[Hex / HSL]` | `[Hex / HSL]` | `[Elevation Layer 1]` |
| **Border** | `[Hex / HSL]` | `[Hex / HSL]` | `[Subtle Hairline Contrast]` |

---

## 5. Typography Pairing Synthesis

| Role | Recommended Font | Final Selected Font | Classification | Google Fonts / CDN Import | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Display / H1** | `[Font Name]` | `[Font Name]` | `[Serif / Sans / Display]` | `[Import URL]` | [Brand character & scale] |
| **Heading / H2-H4**| `[Font Name]` | `[Font Name]` | `[Sans / Serif]` | `[Import URL]` | [Structural clarity] |
| **Body Copy** | `[Font Name]` | `[Font Name]` | `[Geometric / Neutral Sans]`| `[Import URL]` | [Readability at 65-75ch] |
| **Data / Numbers** | `[Font Name]` | `[Font Name]` | `[Mono / Tabular]` | `[Import URL]` | `tabular-nums` verified |

---

## 6. Critical UX Guardrails & Stack Best Practices

### 6.1 Domain UX Guardrails
- **[Rule 1]:** [Specific UX rule, e.g., Visible form labels near fields with error summary]
- **[Rule 2]:** [Specific UX rule, e.g., Touch target $\ge 44\text{px}$ on all navigation triggers]

### 6.2 Tech Stack Implementation Guidance (`[Approved Stack]`)
- **[Stack Practice 1]:** [e.g., Next.js `next/image` with `priority` on LCP hero image]
- **[Stack Practice 2]:** [e.g., Tailwind CSS `@layer components` for token encapsulation]

---

## 7. Provenance & Subsystem Audit Trail

- **Search Queries Executed:**
  1. `python intelligence/ui-ux-pro-max/engine/query.py --product "[Product Query]"`
  2. `python intelligence/ui-ux-pro-max/engine/query.py --domain [Domain] --query "[Query]"`
- **Precedence Hierarchy Adhered:** `VERIFIED (Owner Requirements & Brand Locks > Database Recommendations)`
- **Design System Invariant:** `VERIFIED (Zero MASTER.md generated; tokens mapped directly to design-system.md)`
- **Lock Invariant:** `VERIFIED (No existing locks mutated silently)`
- **Readiness Gate Status:** `DESIGN_INTELLIGENCE_COMPLETE`
