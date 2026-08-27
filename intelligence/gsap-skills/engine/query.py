#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Website Director GSAP Motion Implementation Engine Query Adapter.
Provides official GreenSock implementation guidance, lifecycle patterns, cleanup recipes,
ScrollTrigger setups, and framework-specific integrations.

Provenance:
  Upstream Repo: https://github.com/greensock/gsap-skills
  Commit SHA: aed9cfd3277740755f6bfc1155c7aa645403b760
  License: MIT (GreenSock)
  Status: Official Motion Implementation Engine
"""

import argparse
import io
import json
import re
import sys
from pathlib import Path

# Force UTF-8 stdout on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_DIR = Path(__file__).parent.parent
SKILLS_DIR = BASE_DIR / "skills"

PROVENANCE = {
    "source_engine": "Official GreenSock GSAP Skills Engine",
    "source_repo": "https://github.com/greensock/gsap-skills",
    "source_sha": "aed9cfd3277740755f6bfc1155c7aa645403b760",
    "license": "MIT (Copyright (c) 2026 GreenSock)",
    "skills_available": [
        "gsap-core",
        "gsap-timeline",
        "gsap-scrolltrigger",
        "gsap-plugins",
        "gsap-utils",
        "gsap-react",
        "gsap-frameworks",
        "gsap-performance"
    ]
}

RECIPES = {
    "react-usegsap-basic": {
        "title": "React / Next.js useGSAP Basic Animation with Scoped Selector",
        "framework": "react",
        "imports": "import gsap from 'gsap';\nimport { useGSAP } from '@gsap/react';\nimport { useRef } from 'react';",
        "code": """// Register plugin (in root or component module)
gsap.registerPlugin(useGSAP);

export default function HeroSection() {
  const container = useRef(null);

  useGSAP(() => {
    // Scoped selector automatically scoped to container.current
    gsap.from('.hero-headline', {
      y: 40,
      autoAlpha: 0,
      duration: 1,
      ease: 'power3.out'
    });
    
    gsap.from('.hero-card', {
      y: 30,
      autoAlpha: 0,
      duration: 0.8,
      stagger: 0.15,
      ease: 'power2.out',
      delay: 0.3
    });
  }, { scope: container }); // Automatic cleanup on unmount!

  return (
    <section ref={container} className="hero-section">
      <h1 className="hero-headline">Precision Engineering</h1>
      <div className="hero-card">Card 1</div>
      <div className="hero-card">Card 2</div>
    </section>
  );
}""",
        "cleanup_method": "useGSAP({ scope: container }) automatically reverts all tweens/timelines created inside on unmount.",
        "reduced_motion": "Wrap animations in gsap.matchMedia() or check window.matchMedia('(prefers-reduced-motion: reduce)')."
    },
    "react-scrolltrigger": {
        "title": "React / Next.js ScrollTrigger with matchMedia & Reduced Motion",
        "framework": "react",
        "imports": "import gsap from 'gsap';\nimport { ScrollTrigger } from 'gsap/ScrollTrigger';\nimport { useGSAP } from '@gsap/react';\nimport { useRef } from 'react';",
        "code": """if (typeof window !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger, useGSAP);
}

export default function FeatureSection() {
  const container = useRef(null);

  useGSAP(() => {
    const mm = gsap.matchMedia();

    // Standard Desktop & Motion Enabled
    mm.add('(prefers-reduced-motion: no-preference)', () => {
      gsap.from('.feature-card', {
        scrollTrigger: {
          trigger: container.current,
          start: 'top 75%',
          end: 'bottom 25%',
          toggleActions: 'play none none reverse'
        },
        y: 50,
        autoAlpha: 0,
        duration: 0.9,
        stagger: 0.2,
        ease: 'power2.out'
      });
    });

    // Reduced Motion Fallback
    mm.add('(prefers-reduced-motion: reduce)', () => {
      gsap.from('.feature-card', {
        scrollTrigger: {
          trigger: container.current,
          start: 'top 85%'
        },
        autoAlpha: 0,
        duration: 0.3,
        ease: 'none'
      });
    });
  }, { scope: container });

  return (
    <section ref={container} className="feature-section">
      <div className="feature-card">Feature A</div>
      <div className="feature-card">Feature B</div>
    </section>
  );
}""",
        "cleanup_method": "useGSAP automatically reverts matchMedia and kills ScrollTriggers on unmount.",
        "reduced_motion": "Built-in via gsap.matchMedia() condition."
    },
    "vue-lifecycle-cleanup": {
        "title": "Vue 3 / Nuxt 3 gsap.context Scoped Lifecycle & Cleanup",
        "framework": "vue",
        "imports": "import { ref, onMounted, onUnmounted } from 'vue';\nimport gsap from 'gsap';",
        "code": """<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import gsap from 'gsap';

const main = ref(null);
let ctx;

onMounted(() => {
  ctx = gsap.context(() => {
    gsap.from('.box', {
      xPercent: -50,
      autoAlpha: 0,
      duration: 1,
      ease: 'power2.out'
    });
  }, main.value); // Scoped to main ref
});

onUnmounted(() => {
  ctx.revert(); // Critical: Reverts all animations and kills listeners
});
</script>

<template>
  <div ref="main" class="container">
    <div class="box">Animated Box</div>
  </div>
</template>""",
        "cleanup_method": "ctx.revert() called inside onUnmounted() cleans up all tweens, timelines, and ScrollTriggers.",
        "reduced_motion": "Use gsap.matchMedia() inside gsap.context()."
    },
    "svelte-lifecycle-cleanup": {
        "title": "Svelte / SvelteKit gsap.context Lifecycle & Cleanup",
        "framework": "svelte",
        "imports": "import { onMount, onDestroy } from 'svelte';\nimport gsap from 'gsap';",
        "code": """<script>
  import { onMount, onDestroy } from 'svelte';
  import gsap from 'gsap';

  let container;
  let ctx;

  onMount(() => {
    ctx = gsap.context(() => {
      gsap.from('.card', {
        y: 40,
        autoAlpha: 0,
        duration: 0.8,
        ease: 'power2.out'
      });
    }, container);
  });

  onDestroy(() => {
    if (ctx) ctx.revert();
  });
</script>

<div bind:this={container} class="container">
  <div class="card">Svelte Card</div>
</div>""",
        "cleanup_method": "ctx.revert() in onDestroy() ensures zero memory leaks.",
        "reduced_motion": "Support via gsap.matchMedia()."
    },
    "vanilla-scrolltrigger-pinning": {
        "title": "Vanilla JS ScrollTrigger Pinned Sequence with Proper Cleanup",
        "framework": "vanilla",
        "imports": "import gsap from 'gsap';\nimport { ScrollTrigger } from 'gsap/ScrollTrigger';\ngsap.registerPlugin(ScrollTrigger);",
        "code": """export function initPinnedSection(sectionElement) {
  const ctx = gsap.context(() => {
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: sectionElement,
        start: 'top top',
        end: '+=1500',
        scrub: 1,
        pin: true,
        anticipatePin: 1,
        invalidateOnRefresh: true
      }
    });

    tl.to('.panel-1', { autoAlpha: 0, scale: 0.95, duration: 1 })
      .from('.panel-2', { autoAlpha: 0, scale: 1.05, duration: 1 }, '<0.5')
      .to('.panel-2', { autoAlpha: 0, scale: 0.95, duration: 1 })
      .from('.panel-3', { autoAlpha: 0, scale: 1.05, duration: 1 }, '<0.5');
  }, sectionElement);

  // Return teardown function
  return () => ctx.revert();
}""",
        "cleanup_method": "Invoking the returned teardown function executes ctx.revert(), unpinning DOM and destroying ScrollTrigger.",
        "reduced_motion": "On reduced motion, bypass pinning and present stacked static cards."
    }
}

def load_skill_doc(skill_name):
    clean_name = skill_name if skill_name.startswith("gsap-") else f"gsap-{skill_name}"
    doc_path = SKILLS_DIR / clean_name / "SKILL.md"
    if not doc_path.exists():
        return {"error": f"Skill {clean_name} not found. Available: {PROVENANCE['skills_available']}"}
    with open(doc_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    return {
        "skill": clean_name,
        "path": str(doc_path.relative_to(BASE_DIR)),
        "content": content
    }

def get_framework_guidance(framework):
    fw = framework.lower().strip()
    if fw in ["react", "nextjs", "next.js", "next"]:
        return {
            "framework": "React / Next.js",
            "package": "@gsap/react",
            "recommended_hook": "useGSAP()",
            "rules": [
                "Always use useGSAP() with a scope ref instead of vanilla useEffect().",
                "Ensure SSR safety: Only register plugins on client or within useGSAP/useEffect.",
                "Use contextSafe() for event handlers or async callbacks to keep them inside GSAP context.",
                "Zero manual tween.kill() required when useGSAP() scope is defined (auto-reverts on unmount)."
            ],
            "recipe_key": "react-usegsap-basic"
        }
    elif fw in ["vue", "nuxt", "nuxtjs", "vue3"]:
        return {
            "framework": "Vue 3 / Nuxt 3",
            "recommended_pattern": "gsap.context() in onMounted() + ctx.revert() in onUnmounted()",
            "rules": [
                "Store context in a component-scoped variable: let ctx = gsap.context(...)",
                "Scope selectors to container element reference (main.value).",
                "Always call ctx.revert() in onUnmounted() to prevent orphaned triggers.",
                "In Nuxt, wrap GSAP imports in client-only plugins or check import.meta.client."
            ],
            "recipe_key": "vue-lifecycle-cleanup"
        }
    elif fw in ["svelte", "sveltekit"]:
        return {
            "framework": "Svelte / SvelteKit",
            "recommended_pattern": "gsap.context() in onMount() + ctx.revert() in onDestroy()",
            "rules": [
                "Initialize context in onMount() and bind to container element.",
                "Always call ctx.revert() in onDestroy().",
                "Use gsap.matchMedia() inside context for responsive and reduced motion."
            ],
            "recipe_key": "svelte-lifecycle-cleanup"
        }
    else:
        return {
            "framework": "Vanilla JS / Multi-Page",
            "recommended_pattern": "gsap.context() returning teardown function",
            "rules": [
                "Encapsulate page animation in init() function returning ctx.revert().",
                "Always call ScrollTrigger.refresh() after DOM or image layout shifts.",
                "Clean up on SPA page transitions."
            ],
            "recipe_key": "vanilla-scrolltrigger-pinning"
        }

def main():
    parser = argparse.ArgumentParser(description="Website Director GSAP Implementation Engine Query Adapter")
    parser.add_argument("--skill", "-s", help="Query official skill documentation (e.g. core, react, scrolltrigger, performance)")
    parser.add_argument("--framework", "-f", help="Get framework-specific lifecycle guidance (react, nextjs, vue, svelte, vanilla)")
    parser.add_argument("--recipe", "-r", help="Get copy-paste ready, production-hardened GSAP recipe")
    parser.add_argument("--list-skills", action="store_true", help="List all available official skills")
    parser.add_argument("--list-recipes", action="store_true", help="List all available official recipes")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    
    args = parser.parse_args()
    
    if args.list_skills:
        data = {"provenance": PROVENANCE, "skills": PROVENANCE["skills_available"]}
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print("Official GSAP Skills Available:")
            for s in PROVENANCE["skills_available"]:
                print(f"- {s}")
        return
        
    if args.list_recipes:
        data = {"provenance": PROVENANCE, "recipes": list(RECIPES.keys())}
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print("Available GSAP Production Recipes:")
            for k, v in RECIPES.items():
                print(f"- {k}: {v['title']} ({v['framework']})")
        return
        
    if args.recipe:
        if args.recipe in RECIPES:
            rec = RECIPES[args.recipe]
            rec["provenance"] = PROVENANCE
            if args.json:
                print(json.dumps(rec, indent=2))
            else:
                print(f"# GSAP Recipe: {rec['title']}\n")
                print(f"**Framework:** `{rec['framework']}`\n")
                print(f"### Imports\n```javascript\n{rec['imports']}\n```\n")
                print(f"### Implementation\n```javascript\n{rec['code']}\n```\n")
                print(f"**Cleanup Guarantee:** {rec['cleanup_method']}\n")
                print(f"**Reduced Motion:** {rec['reduced_motion']}\n")
        else:
            print(f"Error: Unknown recipe '{args.recipe}'. Available: {list(RECIPES.keys())}")
        return
        
    if args.framework:
        fw_info = get_framework_guidance(args.framework)
        rec_data = RECIPES.get(fw_info.get("recipe_key"), {})
        fw_info["example_recipe"] = rec_data
        fw_info["provenance"] = PROVENANCE
        if args.json:
            print(json.dumps(fw_info, indent=2))
        else:
            print(f"# GSAP Implementation Guide: {fw_info['framework']}\n")
            print(f"> **Engine:** {PROVENANCE['source_engine']} (SHA: `{PROVENANCE['source_sha'][:10]}`)\n")
            print("## Core Rules")
            for r in fw_info["rules"]:
                print(f"- {r}")
            print("\n## Canonical Implementation Pattern")
            print(f"```javascript\n{rec_data.get('code', '')}\n```")
        return
        
    if args.skill:
        doc = load_skill_doc(args.skill)
        doc["provenance"] = PROVENANCE
        if args.json:
            print(json.dumps(doc, indent=2))
        else:
            print(doc.get("content", doc.get("error", "")))
        return
        
    parser.print_help()

if __name__ == "__main__":
    main()
