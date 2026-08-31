import os
import json

pilot_dir = r"projects/v2-5-1-signature-choreography-certification-pilot"
os.makedirs(os.path.join(pilot_dir, "css"), exist_ok=True)
os.makedirs(os.path.join(pilot_dir, "js"), exist_ok=True)
os.makedirs(os.path.join(pilot_dir, "evidence"), exist_ok=True)

# 1. site-profile.json
profile = {
  "schema_version": "2.5.1",
  "project_name": "ARC//FORGE Advanced Fabrication & Engineering Studio",
  "domain": "arcforge.engineering",
  "creative_ambition": "SHOWCASE",
  "visual_intensity": "HIGH",
  "motion_appetite": "CINEMATIC",
  "signature_choreography": {
    "status": "selected_direction_ready",
    "mold_breaking_opportunity": "HIGH",
    "interaction_level": "2_FEATURE",
    "primary_pattern": "PINNED_HORIZONTAL_SCROLLYTELLING",
    "supporting_pattern": "SCROLL_DRIVEN_ASSEMBLY",
    "interaction_budget": "MODERATE",
    "novelty_budget": "MODERATE",
    "mobile_strategy": "REFLOWED",
    "reduced_motion_strategy": "STATIC_VERTICAL_EXPANDED",
    "creative_justification": "Translates the 5-stage precision fabrication journey into a tangible lateral atelier walkthrough."
  },
  "locks": {
    "design_direction_locked": False,
    "information_architecture_locked": False,
    "content_structure_locked": False,
    "design_system_locked": False,
    "motion_direction_locked": False
  },
  "handoff": {
    "status": "ready_for_review",
    "acceptance_status": "READY_FOR_REVIEW"
  }
}

with open(os.path.join(pilot_dir, "site-profile.json"), "w", encoding="utf-8") as f:
    json.dump(profile, f, indent=2)

# 2. SIGNATURE-INTERACTION-BRIEF.md
brief_content = """# Signature Interaction Brief: ARC//FORGE

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
"""

with open(os.path.join(pilot_dir, "SIGNATURE-INTERACTION-BRIEF.md"), "w", encoding="utf-8") as f:
    f.write(brief_content)

print("Created pilot profile and brief.")
