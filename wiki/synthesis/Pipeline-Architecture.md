---
title: "Pipeline Architecture & Dataflow"
type: synthesis
tags:
  - architecture/pipeline
  - bioinformatics/workflow
created: 2026-08-17
updated: 2026-08-18
sources:
  - "[[codebase-blast-pipeline]]"
  - "[[altschul-1990-blast]]"
aliases:
  - System Architecture
  - BLAST Pipeline Workflow
---

# Pipeline Architecture & Dataflow

## Overview
The **Mystery Sequence Identifier** pipeline automates the end-to-end identification of unknown biological sequences from input FASTA files to final statistical summary reports with support for both local high-performance standalone BLAST+ CLI and remote NCBI WWW API execution.

```mermaid
flowchart TD
    A[Input FASTA / String] --> B[sequence_io.py: parse_fasta]
    B --> C[sequence_io.py: detect_sequence_type]
    C -->|DNA / RNA| D[Program: blastn, Default DB: nt]
    C -->|Protein| E[Program: blastp, Default DB: nr]
    D --> F[blast_engine.py: run_blast]
    E --> F
    F -->|Local Mode: subprocess| F1[Local blastn/blastp CLI]
    F -->|Remote Mode: Bio.Blast.NCBIWWW| F2[NCBI QBLAST Server]
    F1 --> G[cache/blast_*.xml]
    F2 --> G
    G --> H[report_writer.py: parse_blast_xml]
    H -->|Filter: E-value <= 1e-5, Identity >= 90%| I[Top N Hits & Organism Resolution]
    I -->|If organism unknown| J[sequence_io.py: fetch_ncbi_metadata Entrez]
    J --> I
    I --> K[report_writer.py: export_reports]
    K --> L[reports/*.csv]
    K --> M[reports/*.xlsx]
```

---

## Component Breakdown

| Module | Core Responsibility | Key Technologies |
| :--- | :--- | :--- |
| [`sequence_io.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/sequence_io.py) | [[FASTA-Format]] ingestion, [[Sequence-Type-Inference]], [[NCBI-Entrez]] metadata retrieval | `Bio.SeqIO`, `Bio.Entrez` |
| [`blast_engine.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/blast_engine.py) | Dual local/remote execution, CLI subprocess bridge, retry backoff, XML caching | `subprocess`, `Bio.Blast.NCBIWWW` |
| [`report_writer.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/report_writer.py) | XML parsing, [[BLAST-Alignment-Filtering]], CSV/Excel export | `Bio.Blast.NCBIXML`, `pandas`, `openpyxl` |
| [`main.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/main.py) | CLI argument orchestration (`--mode`, `--db`, `--threads`) | `argparse` |
| [`download_data.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/download_data.py) | Test dataset retrieval from NCBI & RCSB PDB | `urllib`, `Bio.Entrez` |
| [`test_pipeline.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/test_pipeline.py) | Automated test suite for inference, filtering, and exports | `unittest` |

---

## Caching Strategy
Alignment executions against remote NCBI servers or large local databases are disk-cached via deterministic XML filenames:
`cache/blast_<safe_sequence_id>.xml`

Subsequent runs on the same sequence bypass query execution unless `--force-reblast` (`-f`) is specified.

---

## Cross-References
- [[codebase-blast-pipeline]]
- [[NCBI-BLAST]]
- [[NCBI-Entrez]]
- [[NCBI-Taxonomy-Resolution]]
- [[Biopython]]
- [[Sequence-Type-Inference]]
- [[BLAST-Alignment-Filtering]]
- [[Substitution-Matrices-PAM-BLOSUM]]
- [[Karlin-Altschul-Statistics]]
- [[Seed-and-Extend-Heuristic]]
- [[Double-Indexing-and-Reduced-Alphabets]]
- [[Remote-vs-Local-BLAST]]
- [[Local-BLAST-Installation-and-Indexing]]
- [[Heuristic-Alignment-Paradigms-BLAST-DIAMOND-MMseqs2]]
- [[FASTA-Format]]
