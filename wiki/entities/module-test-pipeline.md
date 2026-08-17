---
title: "Module: test_pipeline.py"
type: entity
tags:
  - module/python
  - testing/unittest
  - quality-assurance
created: 2026-08-18
updated: 2026-08-18
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - test_pipeline
  - Automated Test Suite
---

# Module: `test_pipeline.py`

The **Automated Test Suite** provides end-to-end regression testing and unit validation across sequence parsing, biological type classification, NCBI definition line regex parsing, synthetic BLAST XML filtering, CSV export generation, and local binary detection.

---

## Test Cases Breakdown

### 1. `test_sequence_type_detection()`
- **Target**: `detect_sequence_type()` in [[module-sequence-io]].
- **Validation**:
  - DNA input (`ATGCGATC...`) $\rightarrow$ classified as `DNA`, sets program `blastn` and database `nt`.
  - RNA input (`AUGCGAUC...`) $\rightarrow$ classified as `RNA`, sets program `blastn` and database `nt`.
  - Protein input (`MKTLLLT...`) $\rightarrow$ classified as `Protein`, sets program `blastp` and database `nr`.

### 2. `test_organism_extraction()`
- **Target**: `extract_organism_from_title()` in [[module-sequence-io]].
- **Validation**:
  - Bracketed organism extraction: `... [Homo sapiens]` $\rightarrow$ `Homo sapiens`.
  - `PREDICTED:` header syntax: `PREDICTED: Mus musculus hemoglobin...` $\rightarrow$ `Mus musculus`.
  - Fallback unstructured headers.

### 3. `test_parse_blast_xml_filtering()`
- **Target**: `parse_blast_xml()` in [[module-report-writer]].
- **Validation**:
  - Ingests mock multi-hit BLAST XML payload containing high-identity (`NC_012920`, $E = 1.2 \times 10^{-45}$, 98% identity) and low-identity (`XM_001`, $E = 0.05$, 35% identity) hits.
  - Verifies strict threshold filtering (`max_evalue=1e-5`, `min_identity=90.0`) selects only top match.
  - Verifies relaxed thresholding retains all hits with proper bit score ranking.

### 4. `test_export_reports()`
- **Target**: `export_reports()` in [[module-report-writer]].
- **Validation**:
  - Exports test hit dictionaries to a temporary directory.
  - Validates CSV header structure and data row fidelity (`utf-8-sig`).

### 5. `test_local_blast_checker()`
- **Target**: `check_local_blast_available()` in [[module-blast-engine]].
- **Validation**:
  - Ensures safe non-crashing execution of `shutil.which` across different host environments.

---

## CLI Execution

```bash
# Run test suite
python -m unittest test_pipeline.py -v
```

---

## Related Documentation
- [[codebase-blast-pipeline]]
- [[module-sequence-io]]
- [[module-blast-engine]]
- [[module-report-writer]]
- [[Pipeline-Architecture]]
