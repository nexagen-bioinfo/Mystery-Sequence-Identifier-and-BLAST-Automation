---
title: "Mystery Sequence Identifier & BLAST Automation Codebase"
type: source
tags:
  - bioinformatics/blast
  - codebase/python
  - pipeline/automation
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - BLAST Automation Codebase
  - Mystery Sequence Pipeline Source
---

# Mystery Sequence Identifier & BLAST Automation Codebase

## Summary
The **Mystery Sequence Identifier & BLAST Automation Pipeline** is a modular Python bioinformatics tool designed to identify unknown biological DNA, RNA, or Protein sequences in [[FASTA-Format]]. It classifies the sequence type, executes remote [[NCBI-BLAST]] queries against NCBI `nt`/`nr` databases, applies statistical filtering on alignment results, and outputs reports in CSV and Excel formats.

## Key Architecture & Modules
- **Sequence Manager & Entrez Interface** ([`sequence_io.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/sequence_io.py)): Implements FASTA parsing, [[Sequence-Type-Inference]], and [[NCBI-Entrez]] metadata enrichment (`efetch`/`esummary`).
- **Remote BLAST Engine** ([`blast_engine.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/blast_engine.py)): Connects to NCBI WWW BLAST API via `Bio.Blast.NCBIWWW.qblast`, handles network retries with exponential/fixed backoff, and caches raw XML responses locally in `cache/`.
- **XML Parser & Report Generator** ([`report_writer.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/report_writer.py)): Parses XML via `Bio.Blast.NCBIXML`, executes [[BLAST-Alignment-Filtering]] based on E-value and identity thresholds, and exports structured reports.
- **CLI Orchestrator** ([`main.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/main.py)): CLI interface with options `--input`, `--evalue`, `--identity`, `--top`, and `--force-reblast`.
- **Data Ingestion Script** ([`download_data.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/download_data.py)): Pre-populates test sequences from NCBI and RCSB PDB into `data/`.

## Key Dependencies
- `biopython`: [[Biopython]] for `SeqIO`, `Entrez`, `NCBIWWW`, and `NCBIXML`.
- `pandas` & `openpyxl`: Tabular report generation.

## Related Wiki Pages
- [[Pipeline-Architecture]]
- [[Sequence-Type-Inference]]
- [[BLAST-Alignment-Filtering]]
- [[Karlin-Altschul-Statistics]]
- [[Substitution-Matrices-PAM-BLOSUM]]
- [[NCBI-Taxonomy-Resolution]]
- [[Remote-vs-Local-BLAST]]
- [[Local-BLAST-Installation-and-Indexing]]
- [[NCBI-BLAST]]
- [[NCBI-Entrez]]
- [[Biopython]]
- [[FASTA-Format]]
