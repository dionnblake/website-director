#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max Core BM25 Search Engine for Website Director Design Intelligence.
Self-contained, zero-external-dependency search over vendored design intelligence datasets.

Provenance:
  Source Repo: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
  Commit SHA: e4f45473691e4b389519ee4bc359a3d6df666c26
  License: MIT (Next Level Builder)
"""

import csv
import difflib
import re
from pathlib import Path
from math import log
from collections import defaultdict

DATA_DIR = Path(__file__).parent.parent / "data"
MAX_RESULTS = 5

CSV_CONFIG = {
    "style": {
        "file": "styles.csv",
        "search_cols": ["Style ID", "Style Category", "Aliases", "Keywords", "Best For", "Type", "AI Prompt Keywords"],
        "output_cols": ["Style ID", "Style Category", "Aliases", "Status", "Parent Style ID", "Preferred Mode", "Type", "Keywords", "Primary Colors", "Effects & Animation", "Best For", "Light Mode ✓", "Dark Mode ✓", "Performance", "Accessibility", "Framework Compatibility", "Complexity", "AI Prompt Keywords", "CSS/Technical Keywords", "Implementation Checklist", "Design System Variables"]
    },
    "color": {
        "file": "colors.csv",
        "search_cols": ["Product Type", "Notes"],
        "output_cols": ["Product Type", "Primary", "On Primary", "Secondary", "On Secondary", "Accent", "On Accent", "Background", "Foreground", "Card", "Card Foreground", "Muted", "Muted Foreground", "Border", "Destructive", "On Destructive", "Ring", "Notes"]
    },
    "chart": {
        "file": "charts.csv",
        "search_cols": ["Data Type", "Keywords", "Best Chart Type", "When to Use", "When NOT to Use", "Accessibility Notes"],
        "output_cols": ["Data Type", "Keywords", "Best Chart Type", "Secondary Options", "When to Use", "When NOT to Use", "Data Volume Threshold", "Color Guidance", "Accessibility Grade", "Accessibility Risk", "Accessibility Notes", "A11y Fallback", "Library Recommendation", "Interactive Level"]
    },
    "landing": {
        "file": "landing.csv",
        "search_cols": ["Pattern ID", "Pattern Name", "Aliases", "Keywords", "Conversion Optimization", "Section Order"],
        "output_cols": ["Pattern ID", "Pattern Name", "Aliases", "Keywords", "Section Order", "Primary CTA Placement", "Color Strategy", "Conversion Optimization"]
    },
    "product": {
        "file": "products.csv",
        "search_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Key Considerations"],
        "output_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Secondary Styles", "Landing Page Pattern", "Dashboard Style (if applicable)", "Color Palette Focus"]
    },
    "ux": {
        "file": "ux-guidelines.csv",
        "search_cols": ["Category", "Issue", "Description", "Platform"],
        "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]
    },
    "typography": {
        "file": "typography.csv",
        "search_cols": ["Font Pairing Name", "Category", "Mood/Style Keywords", "Best For", "Heading Font", "Body Font"],
        "output_cols": ["Font Pairing Name", "Category", "Heading Font", "Body Font", "Mood/Style Keywords", "Best For", "Google Fonts URL", "CSS Import", "Tailwind Config", "Notes"]
    },
    "icons": {
        "file": "icons.csv",
        "search_cols": ["Category", "Icon Name", "Keywords", "Best For", "Library"],
        "output_cols": ["Category", "Icon Name", "Keywords", "Library", "Import Code", "Usage", "Best For", "Style", "Semantic Role", "Allowed Contexts"]
    },
    "reasoning": {
        "file": "ui-reasoning.csv",
        "search_cols": ["Product Type", "Target Audience", "Key Traits", "Layout Strategy", "Conversion Triggers", "Trust Builders"],
        "output_cols": ["Product Type", "Target Audience", "Key Traits", "Layout Strategy", "Conversion Triggers", "Trust Builders", "Accessibility Focus", "Common Pitfalls"]
    },
    "react": {
        "file": "react-performance.csv",
        "search_cols": ["Category", "Issue", "Keywords", "Description"],
        "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]
    },
    "web": {
        "file": "app-interface.csv",
        "search_cols": ["Category", "Issue", "Keywords", "Description"],
        "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"]
    }
}

AVAILABLE_STACKS = {
    "react": "stacks/react.csv",
    "nextjs": "stacks/nextjs.csv",
    "vue": "stacks/vue.csv",
    "svelte": "stacks/svelte.csv",
    "astro": "stacks/astro.csv",
    "swiftui": "stacks/swiftui.csv",
    "react-native": "stacks/react-native.csv",
    "flutter": "stacks/flutter.csv",
    "nuxtjs": "stacks/nuxtjs.csv",
    "nuxt-ui": "stacks/nuxt-ui.csv",
    "html-tailwind": "stacks/html-tailwind.csv",
    "shadcn": "stacks/shadcn.csv",
    "jetpack-compose": "stacks/jetpack-compose.csv",
    "threejs": "stacks/threejs.csv",
    "angular": "stacks/angular.csv",
    "laravel": "stacks/laravel.csv"
}

def tokenize(text):
    if not text:
        return []
    return [w.lower() for w in re.findall(r'\b[A-Za-z0-9_\-\.\#]+\b', str(text))]

class BM25Index:
    def __init__(self, corpus, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.doc_len = [len(doc) for doc in corpus]
        self.avgdl = sum(self.doc_len) / max(len(corpus), 1)
        self.doc_freqs = defaultdict(int)
        self.inverted_index = defaultdict(list)
        
        for doc_id, doc in enumerate(corpus):
            seen = set()
            for token in doc:
                if token not in seen:
                    self.doc_freqs[token] += 1
                    seen.add(token)
                self.inverted_index[token].append(doc_id)
        
        self.N = len(corpus)

    def get_scores(self, query_tokens):
        scores = defaultdict(float)
        for token in query_tokens:
            if token not in self.doc_freqs:
                continue
            df = self.doc_freqs[token]
            idf = log((self.N - df + 0.5) / (df + 0.5) + 1.0)
            
            # Count frequency in docs
            doc_counts = defaultdict(int)
            for doc_id in self.inverted_index[token]:
                doc_counts[doc_id] += 1
                
            for doc_id, tf in doc_counts.items():
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (self.doc_len[doc_id] / self.avgdl))
                scores[doc_id] += idf * (numerator / max(denominator, 1e-6))
        return scores

def load_csv(rel_path):
    path = DATA_DIR / rel_path
    if not path.exists():
        return []
    with open(path, mode="r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        return list(reader)

def search_domain(domain, query, max_results=MAX_RESULTS):
    if domain not in CSV_CONFIG:
        return {"error": f"Unknown domain: {domain}", "domain": domain, "results": []}
    
    config = CSV_CONFIG[domain]
    rows = load_csv(config["file"])
    if not rows:
        return {"error": f"Empty or missing file: {config['file']}", "domain": domain, "results": []}
    
    corpus = []
    for row in rows:
        text = " ".join(str(row.get(col, "")) for col in config["search_cols"])
        corpus.append(tokenize(text))
    
    bm25 = BM25Index(corpus)
    query_tokens = tokenize(query)
    scores = bm25.get_scores(query_tokens)
    
    if not scores:
        # Fallback substring match
        sub_results = []
        q_lower = query.lower()
        for idx, row in enumerate(rows):
            text = " ".join(str(row.get(col, "")).lower() for col in config["search_cols"])
            if q_lower in text:
                sub_results.append((idx, 1.0))
        sorted_docs = sorted(sub_results, key=lambda x: x[1], reverse=True)[:max_results]
    else:
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_results]
    
    results = []
    for doc_id, score in sorted_docs:
        row = rows[doc_id]
        filtered = {k: row.get(k, "") for k in config["output_cols"] if k in row}
        filtered["_score"] = round(score, 3)
        results.append(filtered)
        
    return {
        "domain": domain,
        "query": query,
        "file": config["file"],
        "total_matches": len(results),
        "results": results
    }

def search_stack(stack_name, query="", max_results=MAX_RESULTS):
    stack_key = stack_name.lower().strip()
    if stack_key not in AVAILABLE_STACKS:
        return {"error": f"Unknown stack: {stack_name}. Available: {list(AVAILABLE_STACKS.keys())}", "results": []}
    
    rel_path = AVAILABLE_STACKS[stack_key]
    rows = load_csv(rel_path)
    if not rows:
        return {"error": f"No data for stack {stack_name}", "results": []}
    
    if not query:
        return {
            "stack": stack_name,
            "file": rel_path,
            "results": rows[:max_results]
        }
        
    corpus = [tokenize(" ".join(str(v) for v in row.values())) for row in rows]
    bm25 = BM25Index(corpus)
    query_tokens = tokenize(query)
    scores = bm25.get_scores(query_tokens)
    
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_results]
    results = [rows[doc_id] for doc_id, _ in sorted_docs]
    return {
        "stack": stack_name,
        "query": query,
        "file": rel_path,
        "results": results
    }
