---
title: "Altschul et al. (1997) — Gapped BLAST and PSI-BLAST"
type: source
tags:
  - bioinformatics/alignment
  - algorithm/heuristic
  - source/paper
created: 2026-08-19
updated: 2026-08-19
sources:
  - "[[raw/altschul1997_gapped_blast.md]]"
aliases:
  - Gapped BLAST
  - PSI-BLAST Paper
  - Altschul 1997
---

# Source Summary: Altschul et al. (1997) — Gapped BLAST and PSI-BLAST

**Full Citation:** Altschul SF, Madden TL, Schäffer AA, Zhang J, Zhang Z, Miller W, Lipman DJ. *Gapped BLAST and PSI-BLAST: a new generation of protein database search programs*. Nucleic Acids Res. 1997 Sep 1;25(17):3389-402. doi: 10.1093/nar/25.17.3389.

---

## 🔬 Core Contributions

This landmark publication introduced **NCBI BLAST 2.0**, fundamentally transforming sequence searching from ungapped segment pair matching into gapped local dynamic programming and iterative profile-driven homology modeling:

1. **[[Two-Hit-Seed-Heuristic]]**: Introduced a two-hit thresholding requirement on the same diagonal ($A \le 40$ residues), reducing unpromising ungapped extensions by $\sim 90\%$ while enabling a lower threshold $T=11$, delivering a $\mathbf{3\times}$ speed improvement over original [[altschul-1990-blast|BLAST 1990]].
2. **Gapped Local Extension**: Replaced post-hoc Poisson sum statistics with banded dynamic programming using an $X_g$-dropoff cutoff triggered from high-scoring ungapped central seeds.
3. **[[Position-Specific-Iterated-BLAST|PSI-BLAST]]**: Introduced automated iterative Position-Specific Scoring Matrix (PSSM) generation from significant query hits ($E \le 0.005$), expanding sensitivity deep into the protein twilight zone ($<25\%$ sequence identity).

---

## 📐 Mathematical & Algorithmic Foundations

### 1. Two-Hit Seeding Condition
Let $D = i - j$ be the diagonal offset between query position $i$ and database position $j$. An extension is executed if and only if two hits $(i_1, j_1)$ and $(i_2, j_2)$ satisfy:
$$i_1 - j_1 = i_2 - j_2 = D \quad \text{and} \quad 0 < i_2 - i_1 \le A \quad (A = 40)$$
where both hits score $\ge T$ (default $T=11$ for [[Substitution-Matrices-PAM-BLOSUM|BLOSUM62]]).

### 2. Gapped Karlin-Altschul Parameters
For gapped alignments, analytical computation of $\lambda$ and $K$ is non-trivial. The paper established pre-computed empirical estimation of $(\lambda_g, K_g)$ via extensive Monte Carlo simulations with random sequences across standard affine gap penalties ($G_{open} = 11, G_{ext} = 1$):
$$E = K_g \cdot m \cdot n \cdot e^{-\lambda_g S}$$

### 3. PSSM Log-Odds Construction
Observed residue frequencies $f_i$ at column $i$ of the Multiple Sequence Alignment (weighted by Henikoff sequence weights) are merged with pseudo-counts derived from [[Substitution-Matrices-PAM-BLOSUM|BLOSUM62]] conditional probabilities $q_{j|k}$:
$$g_{i, j} = \frac{\alpha f_{i, j} + \beta \sum_k f_{i, k} q_{j|k}}{\alpha + \beta}$$
The resulting position-specific score for residue $j$ at query position $i$ is:
$$S_{i, j} = \frac{1}{\lambda} \ln \left( \frac{g_{i, j}}{q_j} \right)$$

---

## 🔗 Cross-References & Wiki Integration
- **Direct Lineage**: Evolution from [[altschul-1990-blast|Altschul et al. 1990 (Original BLAST)]].
- **Algorithmic Mechanics**: Foundational to [[Seed-and-Extend-Heuristic]], [[Two-Hit-Seed-Heuristic]], and [[Substitution-Matrices-PAM-BLOSUM]].
- **Entities**: Implemented in [[NCBI-BLAST]] and [[PSI-BLAST]].
- **Next-Gen Successors**: Paved the way for spaced seeds in [[buchfink-2021-diamond|DIAMOND]] and cascaded profile clustering in [[steinegger-2017-mmseqs2|MMseqs2]].
- **Synthesis Overview**: Analyzed in [[Heuristic-Alignment-Paradigms-BLAST-DIAMOND-MMseqs2]] and [[Profile-Search-and-Remote-Homology]].
