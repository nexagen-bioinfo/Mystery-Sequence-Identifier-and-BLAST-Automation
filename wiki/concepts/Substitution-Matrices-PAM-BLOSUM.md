---
title: "Substitution Matrices: PAM and BLOSUM"
type: concept
tags:
  - bioinformatics/alignment
  - blast/scoring
  - algorithms/matrices
created: 2026-08-18
updated: 2026-08-18
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - BLOSUM62
  - PAM Matrices
  - Scoring Matrices
  - Protein Alignment Scoring
---

# Substitution Matrices: PAM and BLOSUM

**Substitution matrices** quantify the biological likelihood of one amino acid mutating into another over evolutionary time. They provide the fundamental scoring system for protein alignments in `blastp`, `blastx`, `tblastn`, and `tblastx`.

---

## 1. Log-Odds Scoring Principle

For two amino acids $i$ and $j$, the substitution score $s(i,j)$ is derived from the **log-odds ratio** of the observed target frequency $q_{ij}$ relative to the expected random background frequency $p_i \cdot p_j$:

$$s(i,j) = \frac{1}{\lambda} \ln \left( \frac{q_{ij}}{p_i \cdot p_j} \right)$$

- **Positive scores**: Mutational substitutions observed more frequently than random chance (physicochemically conservative changes, e.g., Isoleucine $\leftrightarrow$ Valine).
- **Zero score**: Neutral substitutions occurring at background random chance.
- **Negative scores**: Deleterious or rare mutations that disrupt protein structure/function (e.g., Tryptophan $\leftrightarrow$ Aspartic Acid).

---

## 2. PAM vs. BLOSUM Matrices

| Dimension | PAM (Point Accepted Mutation) | BLOSUM (Blocks Substitution Matrix) |
| :--- | :--- | :--- |
| **Origin & Author** | Margaret Dayhoff et al. (1978) | Steven & Jorja Henikoff (1992) |
| **Model Foundation** | Evolutionary extrapolation from closely related proteins (1% divergence = PAM1). | Direct observation of ungapped local conserved blocks (BLOCKS database). |
| **Numbering Meaning** | **Higher number** = Greater evolutionary distance / divergence.<br>• *PAM30 / PAM70*: Close homologs.<br>• *PAM250*: Distant homologs. | **Lower number** = Greater evolutionary distance / divergence.<br>• *BLOSUM80*: Close homologs ($\ge 80\%$ identity).<br>• *BLOSUM62*: General purpose ($\approx 62\%$ identity).<br>• *BLOSUM45*: Distant homologs ($\approx 45\%$ identity). |
| **BLAST Default** | Legacy default for older tools. | **BLOSUM62** is the standard default for [[NCBI-BLAST]] `blastp`. |

---

## 3. Affine Gap Penalty Model

To account for biological insertions and deletions (indels), alignment algorithms apply an **affine gap penalty** function:

$$\text{Gap Penalty} = G_{\text{open}} + (k - 1) \cdot G_{\text{extend}}$$

Where:
- $G_{\text{open}}$: Gap existence cost (typically high, e.g. 11 for BLOSUM62) reflecting the energetic/evolutionary cost of introducing an indel.
- $G_{\text{extend}}$: Gap extension cost (typically lower, e.g. 1 for BLOSUM62) reflecting that extending an existing gap is more probable than creating a new one.
- $k$: Total length of the gap.

---

## 4. Relationship to Karlin-Altschul Statistics

Every matrix and gap penalty combination has unique Karlin-Altschul statistical parameters ($\lambda$, $K$). Changing the scoring matrix changes the scale parameter $\lambda$, directly impacting bit score calculation and E-value estimation:

$$S' = \frac{\lambda S - \ln K}{\ln 2}$$

---

## Cross-References
- [[Karlin-Altschul-Statistics]]
- [[BLAST-Alignment-Filtering]]
- [[NCBI-BLAST]]
- [[Pipeline-Architecture]]
