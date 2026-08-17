---
title: "BLAST Alignment Filtering"
type: concept
tags:
  - bioinformatics/blast
  - algorithms/statistics
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - Alignment Filtering
  - HSP Scoring
---

# BLAST Alignment Filtering

**BLAST Alignment Filtering** is the process of eliminating low-significance or low-quality local alignments to identify true biological homologs and organism origins.

## Metrics & Statistical Criteria

1. **Expect Value (E-value)**:
   - Describes the number of hits one can expect to see by chance when searching a database of a particular size.
   - Lower E-values indicate higher statistical significance (closer to 0 represents true homology).
   - Default pipeline cutoff: `E-value <= 1e-5`.

2. **Percent Identity (%)**:
   - The percentage of identical residues over the alignment length:
     $$\text{Identity (\%)} = \frac{\text{identities}}{\text{align\_length}} \times 100$$
   - Default pipeline cutoff: `Identity >= 90.0%`.

3. **Bit Score**:
   - A normalized measure of alignment quality independent of database size. Higher bit scores represent better alignments.

4. **Hit Deduping & Ranking**:
   - Hits in [`report_writer.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/report_writer.py) are sorted primarily by **E-value ascending** and secondarily by **Bit Score descending**.
   - Multiple High-Scoring Segment Pairs (HSPs) belonging to the same Accession ID are deduplicated to retain only the top alignment hit per sequence record.

## Taxonomy Resolution Fallback
If the alignment title does not yield an organism name (e.g. returns `"Unknown Organism"`), the pipeline automatically triggers [[NCBI-Entrez]] metadata resolution using `fetch_ncbi_metadata()` to query GenBank / Entrez Summary endpoints (see [[NCBI-Taxonomy-Resolution]]).

## Cross-References
- [[NCBI-BLAST]]
- [[NCBI-Entrez]]
- [[NCBI-Taxonomy-Resolution]]
- [[Karlin-Altschul-Statistics]]
- [[Substitution-Matrices-PAM-BLOSUM]]
- [[Pipeline-Architecture]]
- [[module-report-writer]]
