---
title: "NCBI BLAST"
type: entity
tags:
  - bioinformatics/blast
  - tools/alignment
  - databases/ncbi
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - BLAST
  - Basic Local Alignment Search Tool
  - BLAST WWW
---

# NCBI BLAST

The **Basic Local Alignment Search Tool (BLAST)** is an algorithm and web/CLI suite developed by the NCBI for comparing primary biological sequence information (such as amino-acid sequences of proteins or nucleotides of DNA/RNA sequences).

## Key Programs Used
- **`blastn`**: Nucleotide-nucleotide BLAST. Compares a nucleotide query sequence against a nucleotide database (`nt`).
- **`blastp`**: Protein-protein BLAST. Compares an amino acid query sequence against a protein database (`nr`).

## Target Databases
- **`nt` (Nucleotide Collection)**: Comprehensive non-redundant database of GenBank, EMBL, DDBJ, and RefSeq nucleotide sequences.
- **`nr` (Non-Redundant Protein Database)**: Non-redundant protein database containing entries from GenBank translations, PDB, SwissProt, PIR, and PRF.

## API Integration in Pipeline
In this codebase, BLAST queries are dispatched via `Bio.Blast.NCBIWWW.qblast` in [`blast_engine.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/blast_engine.py). Results are streamed as raw XML format and locally cached in `cache/` as `blast_<sequence_id>.xml`.

## Cross-References
- [[Biopython]]
- [[BLAST-Alignment-Filtering]]
- [[Karlin-Altschul-Statistics]]
- [[Substitution-Matrices-PAM-BLOSUM]]
- [[Remote-vs-Local-BLAST]]
- [[Local-BLAST-Installation-and-Indexing]]
- [[Sequence-Type-Inference]]
- [[Pipeline-Architecture]]
- [[module-blast-engine]]
