# Basic Local Alignment Search Tool (BLAST)

- **Authors**: Stephen F. Altschul, Warren Gish, Webb Miller, Eugene W. Myers, David J. Lipman
- **Journal**: Journal of Molecular Biology (JMB), Vol. 215, Iss. 3, pp. 403-410
- **Year**: 1990
- **DOI**: 10.1016/S0022-2836(05)80360-2

---

## Abstract & Key Highlights

A new approach to rapid sequence similarity searching, directly approximating alignments that optimize a measure of local similarity, the Maximal Segment Pair (MSP) score. The basic algorithm is simple and robust; it can be implemented in a number of ways and applied in a variety of contexts including straightforward DNA and protein sequence database searches, motif searches, and gene identification.

### Core Mathematical Formulations & Concepts

1. **Maximal Segment Pair (MSP)**:
   - A segment is a contiguous subsequence of fixed length.
   - An alignment of two segments of equal length is scored using a substitution matrix (e.g. PAM120, BLOSUM62) without gaps.
   - The MSP is defined as the highest-scoring pair of identical-length segments chosen from 2 sequences.

2. **Karlin-Altschul Extreme Value Distribution**:
   - The number of MSPs with score at least $S$ expected to occur by chance between random sequences of length $m$ and $n$ is:
     $$E = K \cdot m \cdot n \cdot e^{-\lambda S}$$
   - Where $K$ and $\lambda$ are scaling parameters uniquely determined by the background letter frequencies and the scoring matrix.
   - Bit score normalization:
     $$S' = \frac{\lambda S - \ln K}{\ln 2}$$
   - $E$-value in terms of bit score $S'$ and search space $N = m \cdot n$:
     $$E = N \cdot 2^{-S'}$$

3. **Algorithmic Heuristic (Seed-and-Extend)**:
   - **Word Size ($w$)**: For proteins, typically $w = 3$; for DNA, $w = 11$ or $w = 28$ (Megablast).
   - **Neighborhood Generation**: Compile a list of all words of length $w$ that score at least $T$ (threshold) when aligned against any $w$-mer in the query.
   - **Hit Detection**: Rapidly scan the database for exact matches to any word in the neighborhood list using a deterministic finite automaton (DFA) or hash table.
   - **Hit Extension**: Extend hit in both directions without gaps until the running alignment score drops by more than $X$ below the maximum score achieved so far.
