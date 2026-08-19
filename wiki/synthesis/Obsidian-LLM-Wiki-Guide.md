---
title: "Obsidian & LLM Wiki: System Guide & Workflow Architecture"
type: synthesis
tags:
  - obsidian/guide
  - llm-wiki/architecture
  - workflows/pkm
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
  - "[[llm-wiki-pattern]]"
aliases:
  - Obsidian & LLM Wiki Guide
  - How Obsidian Works with LLM Wiki
---

# Obsidian & LLM Wiki: System Guide & Workflow Architecture

> **Core Idea**: Traditional RAG systems query raw documents from scratch on every prompt without compounding knowledge. An **LLM Wiki** maintains an evolving, interlinked markdown knowledge base where the LLM does the bookkeeping, and you explore the graph in [[Obsidian]].

---

## 1. The Tri-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Raw Sources (`raw/`)                                     │
│    Immutable source of truth: papers, PDFs, notes, code     │
└──────────────────────────────┬──────────────────────────────┘
                               │ Ingest & Cross-link
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. The Wiki (`wiki/`)                                       │
│    • Entities (`wiki/entities/`): Tools, modules, APIs      │
│    • Concepts (`wiki/concepts/`): Algorithms, math, methods │
│    • Synthesis (`wiki/synthesis/`): System architectures    │
│    • Index (`wiki/index.md`): Master catalog                │
│    • Log (`wiki/log.md`): Append-only audit history         │
└──────────────────────────────┬──────────────────────────────┘
                               │ Governed by
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Operational Schema (`AGENTS.md`)                         │
│    Rules for Ingest, Query, and Lint protocols              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Obsidian as the IDE for Knowledge

In this paradigm:
- **The Wiki** is the codebase.
- **The LLM** is the software developer maintaining the codebase.
- **[[Obsidian]]** is the IDE where you browse, search, and navigate the output.

### Key Obsidian Features Used:
1. **Interactive Graph View (`Cmd+G` / `Ctrl+G`)**:
   - Visualizes relationships between modules (`module-sequence-io`), concepts (`Sequence-Type-Inference`), algorithms (`Karlin-Altschul-Statistics`), and external entities (`NCBI-BLAST`).
   - High-density hubs naturally reveal core system components.
2. **Bidirectional Wikilinks**:
   - Every page uses wikilink syntax to create bidirectional links. Enables instant backlink tracking — opening any concept page shows all pipeline files and synthesis documents referencing it.
3. **YAML Frontmatter & Dataview**:
   - Every file contains metadata (`type`, `tags`, `sources`, `created`, `updated`) allowing dynamic Dataview queries.
4. **Local Attachments & Web Clipper**:
   - Save clipped web assets and figures to `raw/assets/` via hotkey (`Ctrl+Shift+D`), preventing broken external URL links.

---

## 3. The 3 Core Operational Protocols

### Protocol A: Ingest (`ingest`)
When a new document or source is introduced:
1. LLM reads and extracts key claims, methods, and entities.
2. Creates a dedicated `wiki/sources/<source-name>.md`.
3. Creates new entity/concept pages or updates existing ones.
4. Adds cross-links and resolves contradictions with existing knowledge.
5. Updates `wiki/index.md` and appends to `wiki/log.md`.

### Protocol B: Query & Compound (`query`)
When you ask an investigative question:
1. LLM consults `wiki/index.md` and relevant wiki pages.
2. Generates a synthesized response with citations.
3. If the answer provides a valuable comparison or new synthesis, it is filed back into `wiki/synthesis/` as a permanent knowledge asset.

### Protocol C: Lint & Health-Check (`lint`)
Maintains graph health:
1. Detects broken links or uncreated hubs.
2. Audits orphan nodes (pages with no incoming connections).
3. Identifies knowledge gaps and proposes target concepts to document.

---

## Cross-References
- [[Compounding-Knowledge-Graph]]
- [[llm-wiki-pattern]]
- [[Obsidian]]
- [[Automated-Bioinformatics-Knowledge-Compounding]]
- [[Pipeline-Architecture]]
- [[codebase-blast-pipeline]]
- [[module-sequence-io]]
- [[module-blast-engine]]
- [[module-report-writer]]
- [[module-main-cli]]
- [[module-download-data]]
