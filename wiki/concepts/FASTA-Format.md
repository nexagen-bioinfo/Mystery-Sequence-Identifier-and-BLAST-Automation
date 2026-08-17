---
title: "FASTA Format"
type: concept
tags:
  - bioinformatics/file-formats
  - data/standards
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - FASTA
  - Sequence File Format
---

# FASTA Format

**FASTA format** is a text-based format for representing either nucleotide sequences or amino acid (protein) sequences, in which nucleotides or amino acids are represented using single-letter codes.

## Structure
- Begins with a single-line description line starting with a greater-than symbol (`>`):
  ```text
  >gi|887494115|gb|KT232088.1| Measles virus strain Edmonston B, complete genome
  AGAGAGAAAAGGGTCCTGTGCTAACCCAG...
  ```
- Followed by lines of sequence data.

## Pipeline Handling in `sequence_io.py`
The parser in [`sequence_io.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/sequence_io.py) (`parse_fasta`):
1. Detects whether the input is a valid filesystem path or a raw FASTA text string.
2. Uses `Bio.SeqIO.parse()` to instantiate a `Bio.SeqRecord.SeqRecord`.
3. Sanitizes headers and extracts sequence length.

## Cross-References
- [[Sequence-Type-Inference]]
- [[Biopython]]
- [[Pipeline-Architecture]]
- [[module-sequence-io]]
