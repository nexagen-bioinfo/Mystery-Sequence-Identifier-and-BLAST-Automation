# MMseqs2 Enables Sensitive Protein Sequence Searching for the Analysis of Massive Datasets

- **Authors**: Martin Steinegger, Johannes Söding
- **Journal**: Nature Biotechnology, Vol. 35, Iss. 11, pp. 1026-1028
- **Year**: 2017
- **DOI**: 10.1038/nbt.3988

---

## Abstract & Key Innovations

MMseqs2 (Many-against-Many sequence searching) is an open-source software suite for fast, sensitive sequence searching and clustering of huge protein and nucleotide sequence sets. It runs 4-5 orders of magnitude faster than BLAST at comparable sensitivity.

### 3-Stage Cascaded Search Architecture

1. **Stage 1: $k$-mer Matching with Consecutive & Spaced $k$-mers**:
   - Compiles short $k$-mers ($k=7$) using a 21-letter or reduced alphabet.
   - Generates similar $k$-mer lists based on a substitution matrix (BLOSUM62) with score threshold $S_{kmer}$.
   - Evaluates consecutive identical/similar $k$-mer hits on the same diagonal.

2. **Stage 2: Ungapped Alignment Filter**:
   - Performs rapid diagonal extension without gaps using vectorization.
   - Filters out >99% of false-positive seed matches before reaching full gapped alignment.

3. **Stage 3: Vectorized Banded Smith-Waterman Alignment**:
   - Performs SSE2/AVX2 vectorized banded dynamic programming with affine gap penalties.
   - Computes rigorous Karlin-Altschul E-values and bit scores.

4. **Iterative Profile & Hidden Markov Model (HMM) Searching**:
   - Extends to `mmseqs search -a` and profile searches, replacing PSI-BLAST and HMMER with 100x speed advantages.
