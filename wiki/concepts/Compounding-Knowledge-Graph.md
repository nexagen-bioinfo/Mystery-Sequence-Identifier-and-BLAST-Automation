---
title: "Compounding Knowledge Graph Architecture"
type: concept
tags:
  - knowledge-graph/theory
  - pkm/compounding
  - associative-trails/memex
  - llm/synthesis
created: 2026-08-19
updated: 2026-08-19
sources:
  - "[[llm-wiki-pattern]]"
aliases:
  - Compounding Knowledge Base
  - Associative Knowledge Graph
  - Memex Associative Trails
---

# Compounding Knowledge Graph Architecture

## Overview
A **Compounding Knowledge Graph** is an associative, continuously evolving network of structured markdown documents where knowledge is synthesized once, cross-linked bidirectionally, and kept current by an LLM maintainer. Rather than discarding the results of complex syntheses or document ingestions, every insight is filed back into the graph, compounding its utility over time.

```
       [Raw Sources: raw/]  (Immutable truth)
               │
               ▼ (Ingest Protocol)
      ┌────────────────────────────────────────┐
      │          The Persistent Wiki           │
      │  ┌──────────────┐    ┌──────────────┐  │
      │  │   Sources    │───▶│   Entities   │  │
      │  └──────────────┘    └──────┬───────┘  │
      │         │                   │          │
      │         ▼                   ▼          │
      │  ┌──────────────┐    ┌──────────────┐  │
      │  │  Syntheses   │◀───│   Concepts   │  │
      │  └──────────────┘    └──────────────┘  │
      └────────────────────────────────────────┘
               ▲
               │ (Query & Compound Protocol)
          [LLM + Human Pair] 
```

## Core Tenets

### 1. Zero-Cost Maintenance & Bookkeeping
Human-maintained wikis frequently fail because the maintenance burden (cross-linking, reformatting, reconciling contradictions) increases quadratically with graph size ($O(N^2)$). In a compounding LLM wiki:
- The human directs queries, curates sources, and navigates.
- The LLM performs all routine bookkeeping across dozens of files simultaneously.

### 2. Pre-Compiled Synthesis vs. Runtime RAG
Traditional Retrieval-Augmented Generation (RAG) breaks texts into arbitrary chunks and performs semantic vector search at runtime. This causes critical issues:
- **Fragile multi-hop synthesis**: If a question requires connecting 5 distinct sources, vector search often misses intermediate bridging nodes.
- **Forgotten discoveries**: Novel user-agent discoveries disappear when the chat session terminates.
In a compounding graph, multi-hop pathways are explicitly instantiated as bidirectional wikilinks, and deep exploratory answers are saved as permanent `synthesis/` pages.

### 3. Associative Trails & Memex Heritage
Inspired by Vannevar Bush's 1945 *Memex* concept, the graph creates associative trails between entities, biological mechanisms, and software modules:
- An organism TaxID links to its sequence characteristics, alignment statistics, and benchmark runs.
- Contradictions across sources are flagged with Obsidian callouts (`> [!WARNING]`).

## Related Wiki Pages
- [[llm-wiki-pattern]]
- [[Obsidian]]
- [[Obsidian-LLM-Wiki-Guide]]
- [[Automated-Bioinformatics-Knowledge-Compounding]]
- [[Pipeline-Architecture]]
