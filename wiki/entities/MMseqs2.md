---
title: "MMseqs2 (Many-against-Many Sequence Searching)"
type: entity
tags:
  - entity/tool
  - bioinformatics/alignment
  - high-throughput/clustering
created: 2026-08-18
updated: 2026-08-18
sources:
  - "[[steinegger-2017-mmseqs2]]"
aliases:
  - MMseqs2
  - mmseqs
---

# MMseqs2

**MMseqs2** (Many-against-Many sequence searching) is an open-source software suite designed for sequence searching, clustering, and taxonomy classification across ultra-large scale protein and nucleotide sequence collections.

---

## 🔑 Key Capabilities

- **Cascaded Search**: 3-stage search pipeline ($k$-mer match $\rightarrow$ ungapped diagonal filter $\rightarrow$ vectorized banded Smith-Waterman).
- **Sequence Clustering**: Linear-time clustering (`mmseqs cluster` and `mmseqs linclust`) capable of clustering billions of sequences into representative centroids.
- **Taxonomy Assignment**: `mmseqs taxonomy` assigns taxonomic IDs via fast LCA (Lowest Common Ancestor) analysis.
- **Profile Search**: `mmseqs search -a` replaces PSI-BLAST and profile HMM searches with orders of magnitude speedups.

---

## 🛠️ CLI Example Commands

```bash
# 1. Create DBs
mmseqs createdb query.fasta queryDB
mmseqs createdb target.fasta targetDB

# 2. Run cascaded search
mmseqs search queryDB targetDB resultDB tmp --threads 16 -s 7.5

# 3. Convert results to BLAST-compatible format
mmseqs convertalis queryDB targetDB resultDB results.m8
```

---

## 🔗 Related Pages
- [[steinegger-2017-mmseqs2]]
- [[Seed-and-Extend-Heuristic]]
- [[Double-Indexing-and-Reduced-Alphabets]]
- [[DIAMOND]]
- [[NCBI-BLAST]]
- [[Heuristic-Alignment-Paradigms-BLAST-DIAMOND-MMseqs2]]
