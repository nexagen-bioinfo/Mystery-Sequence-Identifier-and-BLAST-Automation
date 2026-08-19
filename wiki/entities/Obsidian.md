---
title: "Obsidian Markdown IDE"
type: entity
tags:
  - tools/ide
  - obsidian/markdown
  - pkm/graph-view
created: 2026-08-19
updated: 2026-08-19
sources:
  - "[[llm-wiki-pattern]]"
aliases:
  - Obsidian
  - Obsidian App
---

# Obsidian Markdown IDE

## Overview
**Obsidian** functions as the local graphical viewer and Integrated Development Environment (IDE) for the persistent knowledge base. While the LLM acts as the autonomous programmer/maintainer modifying markdown files, the user interacts with Obsidian to explore visual link topologies, browse live previews, render Dataview tables, and follow associative trails.

## Core Capabilities in the LLM Wiki Paradigm
- **Graph View**: Real-time visualization of interconnected hubs, semantic clusters, and isolated nodes.
- **Bidirectional Links**: Native support for bidirectional wikilinks and embedded section transclusions.
- **Dataview Plugin**: Executes dynamic SQL-like queries across YAML frontmatter (`type`, `tags`, `sources`, `created`).
- **Obsidian Web Clipper & Local Assets**: Clips web sources and saves media attachments locally to `raw/assets/` via hotkeys (e.g. `Ctrl+Shift+D`), preventing broken external URL links.
- **Marp Plugin**: Compiles wiki markdown pages into slide decks directly inside Obsidian.

## Key Hotkeys & Settings Recommendations
- **Attachment folder path**: Configured to `raw/assets/` in *Settings -> Files and links*.
- **Download attachments hotkey**: Configured to `Ctrl+Shift+D` to download remote images into local repository storage.

## Related Wiki Pages
- [[llm-wiki-pattern]]
- [[Obsidian-LLM-Wiki-Guide]]
- [[Compounding-Knowledge-Graph]]
- [[Automated-Bioinformatics-Knowledge-Compounding]]
