# LLM Wiki Schema & Operational Protocol

This document defines the schema, conventions, and operational workflows for maintaining this persistent LLM Wiki.

---

## 1. System Philosophy

- **Raw Sources (`raw/`)**: Immutable source documents (papers, articles, transcripts, notes, web clips). The LLM reads from these but never modifies them.
- **The Wiki (`wiki/`)**: The persistent, compounding knowledge base. Written and maintained by the LLM, viewed by the human in Obsidian or any markdown viewer.
- **The Human**: Curator, explorer, and decision-maker. Drops sources, guides focus, asks questions.
- **The LLM**: Architect, summarizer, cross-referencer, indexer, and bookkeeper.

---

## 2. Directory Structure

```
├── raw/                      # Immutable source files
│   └── assets/               # Clipped images and attachments
├── wiki/                     # LLM-maintained persistent knowledge base
│   ├── index.md              # Content catalog and navigation hub
│   ├── log.md                # Append-only chronological activity log
│   ├── sources/              # Structured summaries of ingested sources
│   ├── entities/             # Pages for specific people, tools, databases, organisms, organizations
│   ├── concepts/             # Core topics, theories, methods, domain mechanisms
│   └── synthesis/            # High-level overviews, comparisons, query deep-dives
└── AGENTS.md                 # This operational schema
```

---

## 3. Formatting & Linking Conventions

### Frontmatter (YAML)
Every page in `wiki/` must include YAML frontmatter for Obsidian/Dataview compatibility:

```markdown
---
title: "Page Title"
type: concept | entity | source | synthesis
tags:
  - domain/subtopic
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - "[[source-key]]"
aliases:
  - Alternative Name
---
```

### Wikilinks
- Use Obsidian-style double bracket links: `[[Page Name]]` or `[[Page Name|Custom Display Text]]`.
- Always prefer linking to existing pages when an entity or concept is mentioned.
- If a referenced entity/concept does not have a page yet but is notable, link it in advance (e.g., `[[BLAST+]]`) so it appears in graph view and will resolve when created.

---

## 4. Core Workflows

### A. Ingest Protocol (`ingest`)
Triggered when the user asks to ingest or process a source from `raw/`.

1. **Read & Analyze**: Thoroughly examine the source document.
2. **Draft Source Summary**: Create `wiki/sources/<source-name>.md` with metadata, key takeaways, claims, methodology, and direct citations.
3. **Cross-Reference & Update Existing Pages**:
   - Identify relevant existing entity, concept, or synthesis pages in `wiki/`.
   - Update those pages to incorporate new insights, data, or nuances.
   - Flag contradictions with older sources explicitly (e.g., `> [!WARNING] Contradiction with [[source-a]]...`).
4. **Create New Entity/Concept Pages**: Create dedicated pages for any new core entities or concepts introduced by the source.
5. **Update Index**: Add/update links and 1-line descriptions in `wiki/index.md`.
6. **Append Log**: Add a log entry in `wiki/log.md` with:
   ```markdown
   ## [YYYY-MM-DD] ingest | <Source Title>
   - **Source**: `raw/<filename>` -> `[[<source-name>]]`
   - **Pages Created**: `[[Page1]]`, `[[Page2]]`
   - **Pages Updated**: `[[Page3]]`, `[[Page4]]`
   - **Summary**: <1-2 sentence overview of what was added>
   ```

---

### B. Query & Compound Protocol (`query`)
Triggered when the user asks a question against the knowledge base.

1. **Catalog Search**: Check `wiki/index.md` and inspect relevant pages in `wiki/`.
2. **Synthesize Response**: Formulate an answer referencing existing wiki pages (`[[Page]]`) and citing sources.
3. **Persist Valuable Findings**: If the query yielded a novel comparison, thematic synthesis, or deep analysis, offer to file it as a permanent page under `wiki/synthesis/<topic>.md`.
4. **Log**: Record the synthesis in `wiki/log.md`.

---

### C. Lint & Health-Check Protocol (`lint`)
Triggered periodically or on request to maintain wiki health.

1. **Check for Broken Links / Uncreated Hubs**: Identify unlinked concepts or dead wikilinks.
2. **Check for Orphan Pages**: Identify pages with zero incoming links.
3. **Contradiction / Stale Claims Audit**: Reconcile evolving information across multiple sources.
4. **Gap Analysis**: Suggest 2-3 specific questions or search queries that would bridge gaps in the current knowledge graph.
5. **Log**: Record the lint results in `wiki/log.md`.
