---
title: "NCBI Entrez"
type: entity
tags:
  - bioinformatics/entrez
  - api/ncbi
  - databases/metadata
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - Entrez
  - NCBI E-Utilities
---

# NCBI Entrez

**Entrez** is the NCBI's primary search and retrieval system across health and biological data. The pipeline leverages Entrez E-utilities (via [[Biopython]]'s `Bio.Entrez`) for downloading sequences and enriching BLAST alignment hits with taxonomic metadata.

## E-Utilities Employed
1. **`efetch`**:
   - Used in [`download_data.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/download_data.py) to download complete FASTA sequences by Accession ID.
   - Used in [`sequence_io.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/sequence_io.py) (`fetch_ncbi_metadata`) to retrieve GenBank (`rettype="gb"`) records and parse organism taxonomy annotations.
2. **`esummary`**:
   - Used as a fallback in [`sequence_io.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/sequence_io.py) to fetch document summaries when `efetch` fails or full GenBank records are missing.

## Entrez Policy & Requirements
NCBI requires callers to identify themselves by providing an email address (`Entrez.email = "..."`). Failure to supply an email or exceeding request limits (typically 3 requests/sec without API key) can lead to request throttling.

## Cross-References
- [[Biopython]]
- [[NCBI-BLAST]]
- [[Pipeline-Architecture]]
