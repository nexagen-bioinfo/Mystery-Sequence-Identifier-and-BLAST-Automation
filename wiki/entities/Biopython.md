---
title: "Biopython"
type: entity
tags:
  - library/python
  - bioinformatics/tools
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - biopython
  - Bio
---

# Biopython

**Biopython** is an open-source collection of Python tools for computational molecular biology. It provides standard parsers, alignments, and interfaces to major bioinformatics web services.

## Biopython Modules Used in the Pipeline
- **`Bio.SeqIO`**:
  - Handles parsing and writing sequence file formats (primarily [[FASTA-Format]] and GenBank format).
  - Used in [`sequence_io.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/sequence_io.py) and [`download_data.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/download_data.py).
- **`Bio.SeqRecord`**:
  - Encapsulates sequence data (`.seq`), identifier (`.id`), and annotations.
- **`Bio.Blast.NCBIWWW`**:
  - Provides `qblast` function for submitting asynchronous BLAST queries to NCBI's remote servers.
  - Used in [`blast_engine.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/blast_engine.py).
- **`Bio.Blast.NCBIXML`**:
  - Parses BLAST XML output records into alignment objects containing High-Scoring Segment Pairs (HSPs).
  - Used in [`report_writer.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/report_writer.py).
- **`Bio.Entrez`**:
  - Communicates with NCBI E-Utilities (`efetch`, `esummary`).
  - Used in [`sequence_io.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/sequence_io.py) and [`download_data.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/download_data.py).

## Cross-References
- [[NCBI-BLAST]]
- [[NCBI-Entrez]]
- [[Pipeline-Architecture]]
