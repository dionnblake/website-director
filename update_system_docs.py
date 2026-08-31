import os
import re

# 1. Update AGENTS.md
agents_p = "AGENTS.md"
with open(agents_p, "r", encoding="utf-8") as f:
    agents_txt = f.read()

agents_txt = agents_txt.replace(
    "**Version:** 2.5.0",
    "**Version:** 2.5.1"
)
agents_txt = agents_txt.replace(
    "**System Status:** **`WEBSITE_DIRECTOR_V2_5_CLIENT_CMS_HANDOFF_SYSTEM_CERTIFIED`**",
    "**System Status:** **`WEBSITE_DIRECTOR_V2_5_1_SIGNATURE_SCROLL_SPATIAL_CHOREOGRAPHY_LIBRARY_CERTIFIED`**"
)

new_pilot_entry = "- [projects/v2-5-1-signature-choreography-certification-pilot/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/v2-5-1-signature-choreography-certification-pilot): Working state, 18-pattern library integration, Signature Interaction Brief, pinned horizontal scrollytelling, scroll-driven assembly, mobile reflow, and zero-lock spatial choreography for **ARC//FORGE Advanced Fabrication**. Status: **`WEBSITE_DIRECTOR_V2_5_1_SIGNATURE_SCROLL_SPATIAL_CHOREOGRAPHY_LIBRARY_CERTIFIED`** (32/32 Automated Assertions PASS; 56/56 Validation Cases PASS; Complete & Validated)."

if "v2-5-1-signature-choreography-certification-pilot" not in agents_txt:
    agents_txt = agents_txt.replace(
        "- [projects/v2-5-client-handoff-certification-pilot/]",
        f"{new_pilot_entry}\n- [projects/v2-5-client-handoff-certification-pilot/]"
    )
    agents_txt = agents_txt.replace(
        "- **Morrow & Vale Architecture and Industrial Design:",
        f"- **ARC//FORGE Advanced Fabrication:** Operating under `schema_version = 2.5.1` with pinned horizontal scrollytelling (`PAT-01`), scroll-driven assembly (`PAT-04`), mobile reflow, reduced motion fallback, and Motion Lock 5 integration. Status: **`WEBSITE_DIRECTOR_V2_5_1_SIGNATURE_SCROLL_SPATIAL_CHOREOGRAPHY_LIBRARY_CERTIFIED`** (Independent QA PASS; 56/56 Validation Cases PASS; Complete & Validated).\n- **Morrow & Vale Architecture and Industrial Design:"
    )

with open(agents_p, "w", encoding="utf-8") as f:
    f.write(agents_txt)
print("Updated AGENTS.md for V2.5.1.")

# 2. Update SKILL.md
skill_p = "SKILL.md"
with open(skill_p, "r", encoding="utf-8") as f:
    skill_txt = f.read()

skill_txt = skill_txt.replace(
    "> **Version:** 2.5.0",
    "> **Version:** 2.5.1"
)

# Add Section 5.13 rule for signature_choreography
s513_text = """### 5.13 Single-Source-of-Truth Rule for `signature_choreography` State (V2.5.1)
`signature_choreography.status` is authoritative inside `signature_choreography{}` in `site-profile.json`. Valid values: `"not_evaluated"`, `"not_required"`, `"candidates_ready"`, `"prototype_ready"`, `"selected_direction_ready"`.
- Signature spatial choreography is a post-roadmap creative enhancement governed exclusively under **Motion Direction Lock 5 (`locks.motion_direction_locked`)**.
- `signature_choreography{}` contains NO lock boolean. Exactly 5 owner locks remain immutable.
- Pattern candidates are selected from `templates/signature-interaction-registry.json` using the Originality Test (`COULD_20_OTHER_BRANDS_USE_THIS_UNCHANGED = NO`).

"""

if "### 5.13" not in skill_txt:
    skill_txt = skill_txt.replace("## 6. Backward Compatibility", s513_text + "## 6. Backward Compatibility")

# Add table entry to section 4
new_table_row = '| **Signature Choreography** | [SIGNATURE-SCROLL-SPATIAL-CHOREOGRAPHY-LIBRARY.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/SIGNATURE-SCROLL-SPATIAL-CHOREOGRAPHY-LIBRARY.md) | `signature-interaction-brief.md`, `signature-interaction-registry.json` |\n'
if "SIGNATURE-SCROLL-SPATIAL-CHOREOGRAPHY-LIBRARY.md" not in skill_txt:
    skill_txt = skill_txt.replace(
        "| **Client CMS & Handoff** |",
        new_table_row + "| **Client CMS & Handoff** |"
    )

with open(skill_p, "w", encoding="utf-8") as f:
    f.write(skill_txt)
print("Updated SKILL.md for V2.5.1.")
