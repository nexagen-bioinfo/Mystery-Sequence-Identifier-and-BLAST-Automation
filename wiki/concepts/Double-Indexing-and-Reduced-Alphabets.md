---
title: "Double Indexing and Reduced Alphabets"
type: concept
tags:
  - concept/algorithm
  - bioinformatics/alignment
  - high-throughput/optimization
created: 2026-08-18
updated: 2026-08-18
sources:
  - "[[buchfink-2021-diamond]]"
  - "[[steinegger-2017-mmseqs2]]"
aliases:
  - Double Indexing
  - Reduced Amino Acid Alphabet
---

# Double Indexing and Reduced Alphabets

Modern sequence aligners such as [[DIAMOND]] and [[MMseqs2]] achieve multi-thousand-fold acceleration over classical [[NCBI-BLAST]] through two computational breakthroughs: **Double Indexing** and **Reduced Amino Acid Alphabets**.

---

## 🚀 1. Double Indexing

### The Bottleneck in Single Indexing
- Traditional BLAST indexes only the query sequences (or builds a database index) and scans the target database line-by-line.
- On large databases (e.g. NCBI `nr` with >100 million proteins), this results in non-contiguous, cache-thrashing random memory lookups.

### The Double Indexing Solution
1. **Bilateral Partitioning**: Both query batches and database blocks are partitioned and loaded into memory simultaneously.
2. **Seed Sorting**: Lists of seed tuples from both sets are sorted lexicographically by seed key.
3. **Linear Merging**: Matching seeds are identified via sequential list intersection (merge-join) in CPU cache without random pointer lookups.

---

## 🧬 2. Reduced Amino Acid Alphabets

### Principle
The standard 20 amino acid alphabet yields $20^k$ possible $k$-mers ($20^4 = 160,000$, $20^6 = 64,000,000$). Many amino acid substitutions (e.g. Leucine $\leftrightarrow$ Isoleucine) are conservative and biochemically interchangeable.

By grouping biochemically similar residues into representative bins, the alphabet size $|\Sigma|$ is reduced from 20 to 10–11 letters:

| Group ID | Representative Residues | Biochemical Characteristic |
| :--- | :--- | :--- |
| **1** | $\{K, R, H\}$ | Basic / Positively Charged |
| **2** | $\{D, E\}$ | Acidic / Negatively Charged |
| **3** | $\{L, I, V, M\}$ | Aliphatic / Branched Hydrophobic |
| **4** | $\{F, Y, W\}$ | Aromatic |
| **5** | $\{S, T, N, Q\}$ | Polar / Neutral |
| **6** | $\{A, G\}$ | Tiny / Conformational |
| **7** | $\{C\}$ | Disulfide-capable |
| **8** | $\{P\}$ | Helix-breaking |

### Impact on Hash Space & Sensitivity
- An 11-letter alphabet reduces $k=6$ combinations from $20^6 = 6.4 \times 10^7$ down to $11^6 = 1.77 \times 10^6$ (a 97% reduction in index size).
- Preserves high seeding sensitivity for homologous proteins while fitting indexing tables entirely inside high-speed L3 CPU cache.

---

## 🔬 Related Pages
- [[Seed-and-Extend-Heuristic]]
- [[DIAMOND]]
- [[MMseqs2]]
- [[NCBI-BLAST]]
- [[Substitution-Matrices-PAM-BLOSUM]]
- [[Heuristic-Alignment-Paradigms-BLAST-DIAMOND-MMseqs2]]
