#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Website Director Distinctive Frontend Design Evaluation Helper.
Evaluates design direction candidates against subject-grounding, hero thesis,
structural meaning, signature element, boldness budget, and anti-interchangeability rules.

Provenance:
  Upstream Repo: https://github.com/anthropics/claude-plugins-official
  Upstream Path: plugins/frontend-design/skills/frontend-design/SKILL.md
  Commit SHA: b819188d2eea14e0400556ca29dbd1179a7c595b
  License: Apache License 2.0
  Version: NONE / NOT PUBLISHED
  Status: Integrated Distinctiveness & Intentionality Discipline
"""

import argparse
import io
import json
import re
import sys
from pathlib import Path

# Force UTF-8 stdout
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

PROVENANCE = {
    "source_engine": "Anthropic Frontend Design Distinctiveness Discipline",
    "source_repo": "https://github.com/anthropics/claude-plugins-official",
    "source_path": "plugins/frontend-design/skills/frontend-design/SKILL.md",
    "source_sha": "b819188d2eea14e0400556ca29dbd1179a7c595b",
    "source_version": "NONE / NOT PUBLISHED",
    "source_license": "Apache-2.0"
}

AI_DEFAULT_CLUSTERS = [
    {
        "name": "Cluster 1: Warm Cream & Terracotta Serif",
        "description": "Warm cream background (~#F4F1EA), high-contrast editorial serif display, terracotta/clay accent.",
        "risk": "Common default for lifestyle, architecture, or artisanal SaaS regardless of actual subject."
    },
    {
        "name": "Cluster 2: Dark Mode Neon Acid",
        "description": "Near-black background (#0A0A0A), bright acid-green, neon cyan, or vermilion glow accent, pill tags.",
        "risk": "Universal default for AI, devtools, and cyber-security startups without distinct product mechanics."
    },
    {
        "name": "Cluster 3: Broadsheet Dense Monospace",
        "description": "Dense multi-column layout, hairline 1px borders everywhere, zero border-radius, typewriter/mono labels.",
        "risk": "Overused as a shorthand for 'technical' or 'serious' without actual editorial information density."
    }
]

def evaluate_design_direction(direction_text):
    findings = []
    score = 100
    
    # 1. Check Subject Grounding
    has_subject_world = bool(re.search(r'(subject_world|subject\'s world|materials|instruments|artifacts|vernacular)', direction_text, re.I))
    if not has_subject_world:
        findings.append({
            "rule": "GROUND_IN_SUBJECT",
            "severity": "WARNING",
            "message": "Design proposal lacks explicit grounding in the subject's world (materials, tools, vernacular, physical context)."
        })
        score -= 15
        
    # 2. Check Hero Thesis
    has_hero_thesis = bool(re.search(r'(hero_thesis|hero is a thesis|thesis statement|characteristic thing)', direction_text, re.I))
    if not has_hero_thesis:
        findings.append({
            "rule": "HERO_IS_A_THESIS",
            "severity": "WARNING",
            "message": "Hero section does not declare a specific thesis or opening focal encounter."
        })
        score -= 15
        
    # 3. Check Generic Hero Formula Trope
    is_template_hero = bool(re.search(r'(headline\s*\+\s*paragraph\s*\+\s*two buttons\s*\+\s*three stats|big number with a small label.*gradient accent)', direction_text, re.I))
    if is_template_hero:
        findings.append({
            "rule": "ANTI_TEMPLATE_HERO",
            "severity": "FAIL",
            "message": "Hero uses uncurated template formula (headline + paragraph + 2 buttons + 3 stats + gradient) without project justification."
        })
        score -= 20
        
    # 4. Check Structural Meaning (Artificial 01/02/03 Numbering)
    has_decorative_numbering = bool(re.search(r'(01\s*/\s*02\s*/\s*03\s*on\s*features|decorative\s*numbering|numbering\s*cards\s*without\s*sequence)', direction_text, re.I))
    if has_decorative_numbering:
        findings.append({
            "rule": "STRUCTURE_MUST_ENCODE_INFORMATION",
            "severity": "FAIL",
            "message": "Decorative numbering (01/02/03) used on non-sequential content. Structural markers must encode genuine sequential or hierarchical truth."
        })
        score -= 20

    # 5. Check Signature Element & Boldness Budget
    has_signature = bool(re.search(r'(signature_element|signature element|one memorable|boldness budget)', direction_text, re.I))
    if not has_signature:
        findings.append({
            "rule": "SIGNATURE_ELEMENT",
            "severity": "WARNING",
            "message": "No single memorable signature element identified, or boldness budget is unbounded."
        })
        score -= 15
        
    # 6. Anti-Interchangeability Pre-Check (5-Competitor Test)
    interchangeable_flag = bool(re.search(r'(could this design fit 5 competitors|interchangeable|generic saas layout)', direction_text, re.I) and "FAIL" in direction_text)
    if interchangeable_flag:
        findings.append({
            "rule": "ANTI_INTERCHANGEABILITY",
            "severity": "FAIL",
            "message": "Direction failed the 5-competitor interchangeability test. Proposal would fit competitors if logo/copy were swapped."
        })
        score -= 25

    verdict = "PASS" if score >= 80 and not any(f["severity"] == "FAIL" for f in findings) else "REVISE_REQUIRED"
    
    return {
        "score": max(0, score),
        "verdict": verdict,
        "findings": findings,
        "provenance": PROVENANCE
    }

def evaluate_ux_writing(copy_text):
    findings = []
    
    # Check for passive/vague submit buttons
    if re.search(r'\b(submit|click here|learn more)\b', copy_text, re.I):
        findings.append({
            "rule": "ACTION_DESCRIPTIVE_LABELS",
            "severity": "SUGGESTION",
            "message": "Vague generic labels found ('Submit', 'Click Here', 'Learn More'). Prefer action-descriptive verbs ('Save changes', 'Schedule Demo', 'Explore Architecture')."
        })
        
    # Check for internal system terminology
    if re.search(r'\b(webhook|backend endpoint|database row|payload schema)\b', copy_text, re.I):
        findings.append({
            "rule": "USER_PERSPECTIVE_VOCABULARY",
            "severity": "SUGGESTION",
            "message": "Internal implementation terminology detected. Write from the user's perspective (what users recognize and control)."
        })

    return {
        "findings": findings,
        "provenance": PROVENANCE
    }

def main():
    parser = argparse.ArgumentParser(description="Website Director Distinctive Frontend Design Evaluation Helper")
    parser.add_argument("--eval-direction", "-d", help="Evaluate a design direction specification file")
    parser.add_argument("--eval-copy", "-c", help="Evaluate UI copy/writing sample file")
    parser.add_argument("--list-defaults", action="store_true", help="List known AI design default clusters")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    if args.list_defaults:
        data = {"provenance": PROVENANCE, "clusters": AI_DEFAULT_CLUSTERS}
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print("# Known AI Design Default Clusters (Awareness, Not Permanent Bans):\n")
            for c in AI_DEFAULT_CLUSTERS:
                print(f"### {c['name']}")
                print(f"- **Description:** {c['description']}")
                print(f"- **Risk:** {c['risk']}\n")
        return
        
    if args.eval_direction:
        path = Path(args.eval_direction)
        if not path.exists():
            print(f"Error: File {path} not found.")
            sys.exit(1)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        res = evaluate_design_direction(text)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"# Distinctiveness Evaluation Report\n")
            print(f"**Verdict:** `{res['verdict']}` (Score: {res['score']}/100)\n")
            if res["findings"]:
                print("## Findings:")
                for f in res["findings"]:
                    print(f"- **[{f['severity']}] {f['rule']}:** {f['message']}")
            else:
                print("✓ All distinctiveness, subject-grounding, and structural meaning checks passed.")
        return
        
    if args.eval_copy:
        path = Path(args.eval_copy)
        if not path.exists():
            print(f"Error: File {path} not found.")
            sys.exit(1)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        res = evaluate_ux_writing(text)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"# UX Writing Evaluation Report\n")
            if res["findings"]:
                for f in res["findings"]:
                    print(f"- **[{f['severity']}] {f['rule']}:** {f['message']}")
            else:
                print("✓ UX copy follows user-perspective and active-label standards.")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
