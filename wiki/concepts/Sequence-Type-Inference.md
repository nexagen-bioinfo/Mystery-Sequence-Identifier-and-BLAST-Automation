---
title: "Sequence Type Inference"
type: concept
tags:
  - bioinformatics/sequence-analysis
  - algorithms/heuristics
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - Sequence Detection
  - Nucleotide vs Protein Detection
---

# Sequence Type Inference

**Sequence Type Inference** is the mechanism used to determine whether an arbitrary, unlabeled biological sequence in [[FASTA-Format]] is DNA, RNA, or Protein, which directly dictates which [[NCBI-BLAST]] algorithm and database to target.

## Algorithm in `sequence_io.py`

The pipeline implements a character-frequency heuristic in `detect_sequence_type()`:

```python
dna_rna_chars = set("ATCGUN")
valid_nuc_count = sum(1 for char in sequence_str if char in dna_rna_chars)
nuc_ratio = valid_nuc_count / len(sequence_str)
```

### Classification Rules
1. **Nucleotide Detection (`nuc_ratio >= 0.90`)**:
   - **RNA**: If `"U"` is present and `"T"` is absent.
     - BLAST Program: `blastn`
     - Database: `nt`
   - **DNA**: If `"T"` is present or no `"U"` is present.
     - BLAST Program: `blastn`
     - Database: `nt`
2. **Protein Detection (`nuc_ratio < 0.90`)**:
   - If nucleotide character ratio is below 90%, the sequence is classified as `PROTEIN`.
     - BLAST Program: `blastp`
     - Database: `nr`

## Significance
Automating this step prevents common user errors when invoking BLAST tools and enables hands-free pipeline execution on unknown mystery sequences.

## Cross-References
- [[FASTA-Format]]
- [[NCBI-BLAST]]
- [[Pipeline-Architecture]]
