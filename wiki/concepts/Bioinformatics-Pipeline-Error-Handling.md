---
title: "Bioinformatics Pipeline Error Handling & Edge Cases"
type: concept
tags:
  - bioinformatics/blast
  - error-handling/resilience
  - ncbi/entrez-rate-limits
  - python/pipeline
created: 2026-08-19
updated: 2026-08-19
sources:
  - "[[codebase-blast-pipeline]]"
  - "[[llm-wiki-pattern]]"
aliases:
  - BLAST Error Handling
  - NCBI Rate Limit Mitigation
  - Sequence Ambiguity Handling
---

# Bioinformatics Pipeline Error Handling & Edge Cases

## Overview
High-throughput sequence identification pipelines encounter real-world edge cases including network transient drops, NCBI HTTP 429 rate limits, non-standard IUPAC degenerate characters, XML parsing exceptions, and ambiguous taxonomic definitions. Robust bioinformatics automation requires defensive error boundaries at each pipeline stage.

## Key Edge Cases & Mitigation Strategies

```
Sequence Input ──▶ [Composition Sanity Check] (IUPAC / Length > 0)
                          │
Remote BLAST   ──▶ [Exponential Backoff + XML Disk Caching] (HTTP 429 / 503)
                          │
NCBI XML Parse ──▶ [Safe Iteration + Zero-Hit Guard]
                          │
Taxonomy Lookup──▶ [Title Regex ──▶ Entrez efetch ──▶ Entrez esummary ──▶ Fallback]
```

### 1. NCBI Entrez & WWW BLAST Rate Limiting
- **NCBI Policy**: Without an API key, NCBI limits remote requests to a maximum of 3 requests per second; with an API key, up to 10 requests per second.
- **Handling**: 
  - Mandatory configuration of `Entrez.email` and `Entrez.api_key`.
  - Exponential backoff retry loops with jitter (`blast_engine.py` retries up to 3 times on `HTTPError` / connection timeouts).
  - Deterministic local file caching in `cache/<md5_hash>.xml` to avoid duplicate queries.

### 2. Degenerate & Ambiguous Nucleotide Handling
- Standard DNA/RNA nucleotides (`A, T, C, G, U`) coexist with IUPAC ambiguity codes (`R, Y, S, W, K, M, B, D, H, V, N`).
- `sequence_io.py` utilizes a ratio threshold:
  $$\text{NucRatio} = \frac{\text{Count}(A, T, C, G, U, N)}{\text{Total Length}} \ge 0.90$$
  Sequences below $0.90$ are classified as `PROTEIN` and routed to `blastp` against `nr`.

### 3. XML Parsing & Empty Alignments
- `report_writer.py` guards against empty alignment files (`Bio.Blast.NCBIXML.parse`) by returning an empty list rather than raising an unhandled exception when query yields 0 HSPs passing E-value cutoffs.

### 4. Taxonomy Resolution Fallback Chain
- Definition lines from NCBI BLAST frequently bundle GI numbers, accession IDs, and organism names into irregular formats.
- The pipeline executes a 4-tier fallback:
  1. Regex bracket extraction (`[Organism Name]`)
  2. Keyword slicing (`segment`, `gene for`, `genomic`, `mRNA`)
  3. `Entrez.efetch` on GenBank record (`annotations['organism']`)
  4. `Entrez.esummary` XML docsum parsing.

## Related Wiki Pages
- [[NCBI-Taxonomy-Resolution]]
- [[BLAST-Alignment-Filtering]]
- [[module-blast-engine]]
- [[module-sequence-io]]
- [[module-report-writer]]
- [[Automated-Bioinformatics-Knowledge-Compounding]]
