# LLM Wiki: A pattern for building personal knowledge bases using LLMs

## The Core Idea

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation. Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up. NotebookLM, ChatGPT file uploads, and most RAG systems work this way.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources. When you add a new source, the LLM doesn't just index it for later retrieval. It reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims, strengthening or challenging the evolving synthesis. The knowledge is compiled once and then *kept current*, not re-derived on every query.

This is the key difference: **the wiki is a persistent, compounding artifact.** The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read. The wiki keeps getting richer with every source you add and every question you ask.

You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work — the summarizing, cross-referencing, filing, and bookkeeping that makes a knowledge base actually useful over time. In practice, I have the LLM agent open on one side and Obsidian open on the other. The LLM makes edits based on our conversation, and I browse the results in real time — following links, checking the graph view, reading the updated pages. Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.

## Architecture

There are three layers:

1. **Raw sources (`raw/`)**: Your curated collection of source documents. Articles, papers, images, data files. These are immutable — the LLM reads from them but never modifies them. This is your source of truth.
2. **The wiki (`wiki/`)**: A directory of LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, an overview, a synthesis. The LLM owns this layer entirely. It creates pages, updates them when new sources arrive, maintains cross-references, and keeps everything consistent. You read it; the LLM writes it.
3. **The schema (`AGENTS.md` / `CLAUDE.md`)**: A document that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki.

## Operations

- **Ingest**: Process a new source into the raw collection. The LLM reads the source, discusses key takeaways, writes a summary page in the wiki, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log.
- **Query**: Ask questions against the wiki. The LLM searches for relevant pages, reads them, and synthesizes an answer with citations. Good answers can be filed back into the wiki as permanent synthesis pages.
- **Lint**: Periodically health-check the wiki. Look for contradictions between pages, stale claims, orphan pages with no inbound links, missing concepts, unlinked cross-references, and knowledge gaps.

## Indexing and Logging

- **`index.md`**: Content-oriented catalog of everything in the wiki — each page listed with a link, a one-line summary, and metadata. Organized by category (entities, concepts, sources, synthesis).
- **`log.md`**: Append-only chronological record of what happened and when (`## [YYYY-MM-DD] ingest | Title`).

## Tips and Tooling

- **Obsidian Web Clipper**: Quick web article clipping to markdown.
- **Local Attachments (`raw/assets/`)**: Download images locally so the LLM can reference them reliably.
- **Graph View**: Visualizing clusters, hubs, and orphan pages in real time.
- **Marp & Dataview**: Presentation decks and dynamic frontmatter queries.
- **Search CLI (`qmd`)**: Hybrid BM25/vector search for scaling beyond hundreds of pages.
