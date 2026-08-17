---
title: "Schema: AGENTS.md (Operational Protocol)"
type: entity
tags:
  - schema/protocol
  - llm-wiki/schema
  - agents/standards
created: 2026-08-18
updated: 2026-08-18
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - AGENTS.md
  - LLM Wiki Protocol
  - System Schema
---

# Schema: `AGENTS.md` (Operational Protocol)

The **Operational Protocol** defines the structural schema, naming conventions, metadata specifications, and workflow triggers governing the maintenance of this persistent LLM Wiki.

---

## Protocol Specifications

### 1. Three-Tier System Philosophy
- **Raw Sources (`raw/`)**: Immutable source files. Read-only.
- **The Wiki (`wiki/`)**: Compounding knowledge graph written and maintained by the LLM.
- **The Human**: Curator, explorer, and decision-maker.

### 2. Standard Workflows
- **`ingest`**: Source analysis $\rightarrow$ structured source summary $\rightarrow$ update/create concepts/entities $\rightarrow$ update `index.md` $\rightarrow$ append to `log.md`.
- **`query`**: Interrogate graph $\rightarrow$ synthesize citations $\rightarrow$ persist novel comparisons into `wiki/synthesis/`.
- **`lint`**: Graph health check $\rightarrow$ dead link detection $\rightarrow$ orphan auditing $\rightarrow$ knowledge gap proposal.

### 3. Frontmatter & Linking Rules
- YAML metadata block on every markdown file (`title`, `type`, `tags`, `created`, `updated`, `sources`, `aliases`).
- Double bracket Obsidian wikilinks (`[[Page Name]]`).

---

## Related Documentation
- [[Obsidian-LLM-Wiki-Guide]]
- [[wiki/index.md]]
- [[wiki/log.md]]
