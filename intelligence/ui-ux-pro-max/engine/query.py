#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Website Director Design Intelligence Query Adapter (UI/UX Pro Max Engine).
Provides structured multi-domain recommendation synthesis, product profiles, and provenance.

Usage:
  python query.py --domain style --query "minimal editorial"
  python query.py --domain color --query "luxury architecture"
  python query.py --domain typography --query "modern elegant serif"
  python query.py --domain ux --query "navigation hierarchy"
  python query.py --product "fintech investment platform"
  python query.py --stack "nextjs" --query "image optimization"

Provenance:
  Engine: UI/UX Pro Max Design Intelligence
  Upstream Repo: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
  Commit SHA: e4f45473691e4b389519ee4bc359a3d6df666c26
  License: MIT
"""

import argparse
import io
import json
import sys
from pathlib import Path

# Force UTF-8 stdout on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from core import search_domain, search_stack, load_csv, AVAILABLE_STACKS

PROVENANCE = {
    "source_engine": "UI/UX Pro Max Design Intelligence",
    "source_repo": "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill",
    "source_sha": "e4f45473691e4b389519ee4bc359a3d6df666c26",
    "source_version": "2.13.0",
    "license": "MIT",
    "motion_presets_status": "DEFERRED"
}

def synthesize_product_intelligence(product_query):
    """
    Synthesize complete design intelligence candidates for a product/industry type:
    1. Product profile & industry conventions
    2. Primary & secondary candidate styles
    3. Recommended color palette & roles
    4. Typography pairing options
    5. Landing page pattern
    6. Critical UX guidelines & common pitfalls
    """
    prod_results = search_domain("product", product_query, max_results=3)
    reasoning_results = search_domain("reasoning", product_query, max_results=2)
    
    top_prod = prod_results["results"][0] if prod_results["results"] else {}
    top_reason = reasoning_results["results"][0] if reasoning_results["results"] else {}
    
    primary_style_name = top_prod.get("Primary Style Recommendation", product_query)
    style_results = search_domain("style", primary_style_name, max_results=3)
    
    color_results = search_domain("color", product_query, max_results=2)
    typo_results = search_domain("typography", product_query, max_results=3)
    ux_results = search_domain("ux", product_query, max_results=4)
    landing_results = search_domain("landing", top_prod.get("Landing Page Pattern", product_query), max_results=2)
    
    synthesis = {
        "provenance": PROVENANCE,
        "query": product_query,
        "product_type": top_prod.get("Product Type", product_query),
        "industry_profile": {
            "keywords": top_prod.get("Keywords", ""),
            "target_audience": top_reason.get("Target Audience", ""),
            "key_traits": top_reason.get("Key Traits", ""),
            "layout_strategy": top_reason.get("Layout Strategy", ""),
            "conversion_triggers": top_reason.get("Conversion Triggers", ""),
            "trust_builders": top_reason.get("Trust Builders", ""),
            "common_pitfalls": top_reason.get("Common Pitfalls", "")
        },
        "candidate_styles": [
            {
                "style_id": s.get("Style ID", ""),
                "category": s.get("Style Category", ""),
                "type": s.get("Type", ""),
                "best_for": s.get("Best For", ""),
                "effects": s.get("Effects & Animation", ""),
                "score": s.get("_score", 0)
            }
            for s in style_results.get("results", [])
        ],
        "candidate_palette": color_results.get("results", [{}])[0] if color_results.get("results") else {},
        "candidate_typography": [
            {
                "pairing_name": t.get("Font Pairing Name", ""),
                "heading_font": t.get("Heading Font", ""),
                "body_font": t.get("Body Font", ""),
                "mood": t.get("Mood/Style Keywords", ""),
                "best_for": t.get("Best For", ""),
                "google_fonts_url": t.get("Google Fonts URL", "")
            }
            for t in typo_results.get("results", [])
        ],
        "candidate_landing_pattern": landing_results.get("results", [{}])[0] if landing_results.get("results") else {},
        "ux_guardrails": [
            {
                "issue": u.get("Issue", ""),
                "category": u.get("Category", ""),
                "description": u.get("Description", ""),
                "do": u.get("Do", ""),
                "dont": u.get("Don't", ""),
                "severity": u.get("Severity", "")
            }
            for u in ux_results.get("results", [])
        ]
    }
    return synthesis

def format_markdown(data):
    lines = []
    lines.append(f"# Design Intelligence Synthesis: {data.get('product_type', data.get('query', ''))}")
    lines.append("")
    lines.append(f"> **Engine:** {PROVENANCE['source_engine']} (v{PROVENANCE['source_version']})  ")
    lines.append(f"> **Provenance SHA:** `{PROVENANCE['source_sha']}`  ")
    lines.append(f"> **Motion Presets:** `{PROVENANCE['motion_presets_status']}` (Deferred to dedicated GSAP subsystem)  ")
    lines.append("")
    
    ind = data.get("industry_profile", {})
    if ind:
        lines.append("## 1. Industry & Audience Intelligence")
        lines.append(f"- **Target Audience:** {ind.get('target_audience', 'N/A')}")
        lines.append(f"- **Key Traits:** {ind.get('key_traits', 'N/A')}")
        lines.append(f"- **Layout Strategy:** {ind.get('layout_strategy', 'N/A')}")
        lines.append(f"- **Conversion Triggers:** {ind.get('conversion_triggers', 'N/A')}")
        lines.append(f"- **Trust Builders:** {ind.get('trust_builders', 'N/A')}")
        lines.append(f"- **Common Pitfalls:** {ind.get('common_pitfalls', 'N/A')}")
        lines.append("")
        
    styles = data.get("candidate_styles", [])
    if styles:
        lines.append("## 2. Candidate Styles (RECOMMENDED, Not Locked)")
        for s in styles:
            lines.append(f"- **{s.get('style_id')}** ({s.get('category')}): {s.get('best_for')} | *Effects:* {s.get('effects')}")
        lines.append("")
        
    pal = data.get("candidate_palette", {})
    if pal:
        lines.append("## 3. Candidate Color Palette (Subject to Brand Lock)")
        lines.append(f"- **Primary:** `{pal.get('Primary')}` (On Primary: `{pal.get('On Primary')}`)")
        lines.append(f"- **Secondary:** `{pal.get('Secondary')}` | **Accent:** `{pal.get('Accent')}`")
        lines.append(f"- **Surfaces:** Background `{pal.get('Background')}`, Card `{pal.get('Card')}`, Border `{pal.get('Border')}`")
        lines.append(f"- **Notes:** {pal.get('Notes', 'N/A')}")
        lines.append("")
        
    typos = data.get("candidate_typography", [])
    if typos:
        lines.append("## 4. Candidate Typography Pairings")
        for t in typos:
            lines.append(f"- **{t.get('pairing_name')}**: Heading `{t.get('heading_font')}` + Body `{t.get('body_font')}` (*Mood: {t.get('mood')}*)")
        lines.append("")
        
    ux = data.get("ux_guardrails", [])
    if ux:
        lines.append("## 5. Domain UX Guardrails & Rules")
        for u in ux:
            lines.append(f"- **[{u.get('severity', 'UX')}] {u.get('issue')}**: {u.get('description')} (✓ Do: {u.get('do')})")
        lines.append("")
        
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Website Director Design Intelligence Engine (UI/UX Pro Max)")
    parser.add_argument("--domain", choices=["style", "color", "chart", "landing", "product", "ux", "typography", "icons", "reasoning", "react", "web"], help="Specific query domain")
    parser.add_argument("--query", "-q", default="", help="Search query string")
    parser.add_argument("--product", "-p", help="Synthesize complete product-type intelligence")
    parser.add_argument("--stack", "-s", help="Query implementation stack guidelines")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--max-results", "-n", type=int, default=3, help="Max results count")
    
    args = parser.parse_args()
    
    if args.product:
        synth = synthesize_product_intelligence(args.product)
        if args.json:
            print(json.dumps(synth, indent=2, ensure_ascii=False))
        else:
            print(format_markdown(synth))
        return
        
    if args.stack:
        res = search_stack(args.stack, args.query, max_results=args.max_results)
        res["provenance"] = PROVENANCE
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print(f"## Stack Implementation Guidance: {args.stack.upper()}\n")
            for r in res.get("results", []):
                print(f"- **{r.get('Guideline', r.get('Issue', r.get('Category', '')))}**: {r.get('Description', r.get('Recommendation', ''))}")
                if r.get("Code Good"):
                    print(f"  ```\n  {r.get('Code Good')}\n  ```")
        return
        
    if args.domain and args.query:
        res = search_domain(args.domain, args.query, max_results=args.max_results)
        res["provenance"] = PROVENANCE
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print(f"## Design Intelligence Results: Domain '{args.domain}' (Query: '{args.query}')\n")
            for r in res.get("results", []):
                title = r.get("Style ID") or r.get("Product Type") or r.get("Font Pairing Name") or r.get("Issue") or r.get("Data Type") or r.get("Pattern Name") or "Result"
                print(f"### {title} (Score: {r.get('_score', 0)})")
                for k, v in r.items():
                    if k not in ["_score"] and v:
                        print(f"- **{k}**: {v}")
                print("")
        return
        
    parser.print_help()

if __name__ == "__main__":
    main()
