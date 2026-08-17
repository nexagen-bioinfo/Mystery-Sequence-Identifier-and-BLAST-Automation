---
title: "Altschul et al. (1990) - Basic Local Alignment Search Tool (BLAST)"
type: source
tags:
  - source/paper
  - bioinformatics/alignment
  - blast/statistics
created: 2026-08-18
updated: 2026-08-18
sources:
  - "raw/altschul1990_blast.md"
aliases:
  - Altschul 1990
  - BLAST Paper
---

# Altschul et al. (1990) — Basic Local Alignment Search Tool

## Citation
- **Authors**: Stephen F. Altschul, Warren Gish, Webb Miller, Eugene W. Myers, David J. Lipman
- **Publication**: *Journal of Molecular Biology*, 215(3):403–410, 1990
- **DOI**: [10.1016/S0022-2836(05)80360-2](https://doi.org/10.1016/S0022-2836(05)80360-2)
- **Primary Source**: [`raw/altschul1990_blast.md`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/raw/altschul1990_blast.md)

---

## Executive Summary
This landmark publication introduced the **BLAST** heuristic alignment algorithm, replacing exhaustive quadratic dynamic programming ($O(M \cdot N)$ Smith-Waterman) with a high-speed **seed-and-extend** heuristic underpinned by the [[Karlin-Altschul-Statistics]] extreme value distribution.

---

## Key Methodological Principles

### 1. Maximal Segment Pair (MSP) Formulation
- An MSP is defined as the highest-scoring pair of equal-length contiguous segments between query $Q$ and subject $S$, scored without gaps via a substitution matrix (e.g. [[Substitution-Matrices-PAM-BLOSUM]]).
- Unlike global Needleman-Wunsch alignment, MSP searches for localized evolutionary conservation islands.

### 2. Algorithmic Seed-and-Extend Steps
1. **Neighborhood Generation**:
   - For every $w$-mer in the query ($w=3$ for proteins, $w=11$ for nucleotides), generate all possible words of length $w$ whose substitution score with the query word exceeds threshold $T$.
2. **DFA / Hash Indexing**:
   - Construct a Deterministic Finite Automaton (DFA) or hash table from the neighborhood list.
3. **Database Scanning & Hit Detection**:
   - Scan target database at linear speed to identify exact matches to the neighborhood words.
4. **Ungapped Diagonal Extension**:
   - Extend hits bidirectionally until the cumulative alignment score falls $X$ below the running maximum ($X$-drop cutoff).

### 3. Statistical Significance
- Integrates the [[Karlin-Altschul-Statistics]] framework:
  $$E = K \cdot m \cdot n \cdot e^{-\lambda S}$$
- Bit score transformation:
  $$S' = \frac{\lambda S - \ln K}{\ln 2}, \quad E = m \cdot n \cdot 2^{-S'}$$

---

## Connections to Knowledge Graph
- **Concepts**: [[Karlin-Altschul-Statistics]], [[Substitution-Matrices-PAM-BLOSUM]], [[Seed-and-Extend-Heuristic]], [[BLAST-Alignment-Filtering]]
- **Entities**: [[NCBI-BLAST]], [[Biopython]], [[DIAMOND]], [[MMseqs2]]
- **Synthesis**: [[Remote-vs-Local-BLAST]], [[Heuristic-Alignment-Paradigms-BLAST-DIAMOND-MMseqs2]]
