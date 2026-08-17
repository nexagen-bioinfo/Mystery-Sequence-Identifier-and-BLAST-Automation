---
title: "Benchmark Test Sequences & Validation Suite"
type: synthesis
tags:
  - bioinformatics/benchmark
  - data/validation
  - testing/sequences
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - Benchmark Sequences
  - Test Datasets
---

# Benchmark Test Sequences & Validation Suite

The pipeline repository provides four standard benchmark sequences in `data/` (retrieved via [`download_data.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/download_data.py)) to validate [[Sequence-Type-Inference]], remote [[NCBI-BLAST]] execution, and [[BLAST-Alignment-Filtering]].

---

## Benchmark Datasets

| Accession / ID | Biological Origin | Molecule / Type | Length | Expected Program & Database | Source Repository |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`NC_012920`** | *Homo sapiens* Mitochondrion (Complete Genome) | Circular DNA | 16,569 bp | `blastn` on `nt` | NCBI RefSeq |
| **`AC_000021`** | Human Mastadenovirus C (Strain Adenoid 6) | Viral DNA | 35,937 bp | `blastn` on `nt` | NCBI RefSeq |
| **`PZ716984`** | Influenza C virus (C/Manombo/MVAN24_8S_3909/2024) | Viral RNA (Segment 7, NEP/NS1 genes) | 900 bp | `blastn` on `nt` | NCBI GenBank |
| **`9GE4`** | Human Nucleosome Core Particle (Histones H2A.Z, H2B, H3.1, H4 + 152bp DNA) | Multi-chain Protein & DNA complex | Multi-record | `blastp` on `nr` (Protein chains) | RCSB PDB |

---

## Validation Scenarios

### 1. Viral RNA Identification (`PZ716984.fasta`)
- **Behavior**: Evaluated with `detect_sequence_type()`, resolves to `RNA` (contains nucleotide characters and specific viral coding sequences).
- **BLAST Run**: Query against `nt` yields top alignment matches against Influenza C virus strains with $\ge 98\%$ identity and $E\text{-value} = 0.0$.
- **Report**: Successfully exported to `reports/report_PZ716984.csv` and `reports/report_PZ716984.xlsx`.

### 2. Multi-Record PDB Complex (`9GE4.fasta`)
- **Behavior**: Contains both polypeptide chains (Histones H2A.Z, H2B, H3, H4) and synthetic nucleosome DNA oligonucleotides.
- **Handling**: Exercises multi-FASTA parsing in `sequence_io.py` (`parse_fasta` takes the first record or can be extended for batch multi-record processing).

---

## Cross-References
- [[codebase-blast-pipeline]]
- [[Pipeline-Architecture]]
- [[Sequence-Type-Inference]]
- [[BLAST-Alignment-Filtering]]
- [[FASTA-Format]]
