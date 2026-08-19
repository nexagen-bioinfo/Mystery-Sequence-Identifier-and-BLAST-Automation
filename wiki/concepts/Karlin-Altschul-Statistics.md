---
title: "Karlin-Altschul Statistics"
type: concept
tags:
  - bioinformatics/blast
  - statistics/alignment
  - theory/mathematics
created: 2026-08-17
updated: 2026-08-19
sources:
  - "[[codebase-blast-pipeline]]"
  - "[[altschul-1990-blast]]"
  - "[[altschul-1997-gapped-blast]]"
aliases:
  - Karlin-Altschul Theory
  - BLAST Statistical Theory
  - E-value Mathematics
---

# Karlin-Altschul Statistics

**Karlin-Altschul statistics** provide the mathematical foundation for evaluating the statistical significance of local biological sequence alignments in [[NCBI-BLAST]].

---

## 1. The High-Scoring Segment Pair (HSP) Distribution

Under a random sequence model with independent and identically distributed residues, the distribution of maximal segment scores $S$ follows an **Extreme Value Distribution (Gumbel Distribution)** rather than a Gaussian distribution:

$$P(S \ge x) = 1 - \exp(-K m n e^{-\lambda x})$$

Where:
- $m$: Effective length of query sequence
- $n$: Effective length of database (search space size)
- $K$: Natural scale parameter for search space size
- $\lambda$: Natural scale parameter for scoring matrix

---

## 2. E-value (Expectation Value)

The **E-value** represents the expected number of distinct local alignments with score $\ge S$ that would occur purely by chance in a database of size $n$:

$$E = K \cdot m \cdot n \cdot e^{-\lambda S}$$

### Properties:
- An $E$-value close to $0$ (e.g., $E \le 10^{-5}$) denotes an alignment that is extremely improbable to have arisen by random chance, indicating true biological homology.
- As database size $n$ increases over time, the $E$-value for a fixed raw score $S$ increases proportionally.

---

## 3. Bit Score ($S'$)

To make alignment scores independent of the specific scoring system ($\lambda$ and $K$), raw scores are normalized into **bit scores**:

$$S' = \frac{\lambda S - \ln K}{\ln 2}$$

Using the bit score, the $E$-value can be rewritten directly as:

$$E = m \cdot n \cdot 2^{-S'}$$

---

## 4. Gapped & Profile Parameter Estimation

While ungapped parameters $(\lambda, K)$ can be computed analytically from substitution matrix marginal frequencies, gapped alignment parameters $(\lambda_g, K_g)$ lack an exact closed-form solution:
- **Empirical Simulation**: [[altschul-1997-gapped-blast|Altschul et al. (1997)]] established precomputed empirical parameters $(\lambda_g, K_g)$ derived from millions of simulated alignments over random sequences.
- **Profile / PSSM Scaling**: In [[Position-Specific-Iterated-BLAST|PSI-BLAST]], each column of the PSSM is scaled such that the overall matrix satisfies the characteristic equation:
  $$\sum_{j=1}^{20} q_j e^{\lambda S_{i, j}} = 1$$
  maintaining rigorous $E$-value comparability across iterations.

---

## Application in the Pipeline
In [`report_writer.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/report_writer.py) and [[BLAST-Alignment-Filtering]]:
- Hits are filtered using the user-defined $E$-value threshold (`max_evalue = 1e-5`).
- Ties in $E$-value are resolved using normalized `Bit Score` descending.

---

## Cross-References
- [[altschul-1990-blast]]
- [[altschul-1997-gapped-blast]]
- [[Two-Hit-Seed-Heuristic]]
- [[Position-Specific-Iterated-BLAST]]
- [[BLAST-Alignment-Filtering]]
- [[Substitution-Matrices-PAM-BLOSUM]]
- [[NCBI-BLAST]]
- [[PSI-BLAST]]
- [[Pipeline-Architecture]]
- [[Remote-vs-Local-BLAST]]
- [[Local-BLAST-Installation-and-Indexing]]
