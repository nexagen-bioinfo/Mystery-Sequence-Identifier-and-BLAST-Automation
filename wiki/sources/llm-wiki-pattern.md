---
title: "LLM Wiki: A Pattern for Building Personal Knowledge Bases using LLMs"
type: source
tags:
  - knowledge-base/wiki
  - llm/architecture
  - obsidian/pkm
  - agents/workflows
created: 2026-08-19
updated: 2026-08-19
sources:
  - "[[llm-wiki-pattern]]"
aliases:
  - LLM Wiki Pattern
  - Personal Knowledge Base Manifesto
---

# LLM Wiki: A Pattern for Building Personal Knowledge Bases using LLMs

## Summary
The **LLM Wiki Pattern** is an architectural paradigm for creating persistent, compounding personal knowledge bases. Rather than treating document analysis as transient, stateless Retrieval-Augmented Generation (RAG) where knowledge is repeatedly rediscovered from scratch, the LLM continuously maintains and cross-references a structured markdown wiki situated between the user and immutable raw source documents.

## Key Principles & Contrasts

| Dimension | Traditional RAG / Search | Persistent LLM Wiki |
| :--- | :--- | :--- |
| **Statefulness** | Stateless per query; re-indexes and chunks on the fly | Persistent, compounding graph of markdown files |
| **Knowledge Compilation** | Fragmented retrieval at runtime | Pre-compiled, synthesized, and continuously updated |
| **Cross-Referencing** | Disconnected chunks | Bidirectional wikilinks, entity hierarchies, and contradiction flags |
| **Division of Labor** | User asks and stitches fragments together | LLM is the **architect/bookkeeper**; User is the **curator/explorer** |
| **Viewer / IDE** | Chatbot UI / Blackbox search | Obsidian / Markdown viewer with visual Graph View and Dataview queries |

## Three-Layer Architecture
1. **Raw Sources (`raw/`)**: Immutable source documents (papers, articles, transcripts, notes, web clips, sequence data). Source of truth.
2. **The Wiki (`wiki/`)**: Compounding markdown layer maintained exclusively by the LLM (`sources/`, `entities/`, `concepts/`, `synthesis/`, `index.md`, `log.md`).
3. **The Schema (`AGENTS.md`)**: Operational guidelines, frontmatter standards, and prompt protocols dictating ingestion, querying, and linting.

## Core Workflows
- **Ingest**: The LLM analyzes a source from `raw/`, creates a structured summary in `wiki/sources/`, updates relevant entity/concept pages, indexes entries in `wiki/index.md`, and writes to `wiki/log.md`.
- **Query**: Searches the wiki catalog, answers questions with inline citations, and persists high-value exploratory findings to `wiki/synthesis/`.
- **Lint**: Periodically scans for dead links, orphan pages, stale claims, and knowledge gaps.

## Related Wiki Pages
- [[Compounding-Knowledge-Graph]]
- [[Obsidian]]
- [[Obsidian-LLM-Wiki-Guide]]
- [[Automated-Bioinformatics-Knowledge-Compounding]]
- [[Pipeline-Architecture]]
