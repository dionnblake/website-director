# Signature Interaction Brief: ARC//FORGE

> **Brand:** ARC//FORGE Advanced Fabrication & Precision Engineering  
> **Creative Ambition:** SHOWCASE  
> **Interaction Level:** 2_FEATURE  
> **Master Pattern:** PAT-01 (PINNED_HORIZONTAL_SCROLLYTELLING)  
> **Supporting Pattern:** PAT-04 (SCROLL_DRIVEN_ASSEMBLY)  
> **Status:** READY_FOR_REVIEW

---

## 1. Context & Opportunity Analysis
- **Expected Industry Pattern:** Generic 3-column capability grid with static stock photos of sparks and CNC mills.
- **What Competitors Normally Do:** Vertical card stack showing 'Milling', 'Lathe', 'Welding', 'Assembly' with standard text.
- **Mold-Breaking Opportunity:** `HIGH`.
- **Justification:** ARC//FORGE transforms raw elemental billets into monolithic aerospace systems. A lateral spatial atelier walkthrough communicates physical material transformation across physical distance.

---

## 2. Signature Mechanic Specification
- **Primary Pattern:** `PINNED_HORIZONTAL_SCROLLYTELLING` (`PAT-01`)
- **Supporting Pattern:** `SCROLL_DRIVEN_ASSEMBLY` (`PAT-04`)
- **Execution:** Pinned container scrubbing a 5-chapter horizontal track (`100vw` * 5 = `500vw`). During chapter 4, modular bracket layers translate and lock into final chassis assembly.
- **Orientation Strategy:** Persistent chapter HUD (`01 RAW`, `02 FORM`, `03 PRECISION`, `04 ASSEMBLY`, `05 OUTPUT`), progress scrubber rail, and dual exit indicators.

---

## 3. Brand & Story Test
- **Why It Belongs to THIS Brand:** The lateral motion mimics the linear gantries of industrial gantry mills and clean-room assembly lines.
- **Story Communicated:** "This interaction communicates the relentless physical transformation of raw metallurgy into micron-tolerance aerospace structures."
- **Could 20 Other Brands Use This Unchanged?:** `NO`. Grounded entirely in metallurgical phase change and CNC workflow.
- **Novelty Without Purpose?:** `FALSE`.

---

## 4. Responsive & Accessibility Guardrails
- **Mobile Strategy:** `REFLOWED` (converts cleanly to vertical cards at <= 768px).
- **Reduced Motion Strategy:** Lateral translation and pinning disabled; instant static vertical reading sequence.
- **JS Failure Degradation:** Full semantic HTML content visible in standard vertical layout.
