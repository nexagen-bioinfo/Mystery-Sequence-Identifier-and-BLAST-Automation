---
title: "DIAMOND (Sequence Aligner)"
type: entity
tags:
  - entity/tool
  - bioinformatics/alignment
  - high-throughput/proteomics
created: 2026-08-18
updated: 2026-08-18
sources:
  - "[[buchfink-2021-diamond]]"
aliases:
  - DIAMOND Aligner
  - diamond
---

# DIAMOND

**DIAMOND** is a high-throughput sequence alignment software package designed specifically for protein and translated nucleotide searching against massive reference databases (such as NCBI `nr` or UniProt).

---

## 🔑 Key Features & Performance

- **Speed**: 500x to 20,000x faster than [[NCBI-BLAST]] `blastp` and `blastx`.
- **Modes**:
  - `diamond blastp`: Protein query vs. protein database.
  - `diamond blastx`: Translated nucleotide query vs. protein database.
  - `--ultra-sensitive` / `--very-sensitive` / `--fast`: Tunable sensitivity presets.
- **Underlying Technologies**:
  - [[Double-Indexing-and-Reduced-Alphabets]] for cache-efficient seed lookups.
  - Spaced seed shapes (`110100111`).
  - SIMD-accelerated banded dynamic programming (AVX2/AVX-512).

---

## 🛠️ CLI Example Commands

```bash
# 1. Format database
diamond makedb --in nr.faa -d nr

# 2. Run high-throughput search with BLAST-compatible tab/xml output
diamond blastp -q query.fasta -d nr -o matches.tsv --outfmt 6 -p 16 --very-sensitive
```

---

## 🔗 Related Pages
- [[buchfink-2021-diamond]]
- [[Double-Indexing-and-Reduced-Alphabets]]
- [[Seed-and-Extend-Heuristic]]
- [[NCBI-BLAST]]
- [[MMseqs2]]
- [[Heuristic-Alignment-Paradigms-BLAST-DIAMOND-MMseqs2]]
