---
title: "Module: report_writer.py"
type: entity
tags:
  - module/python
  - reports/generator
  - parsing/xml
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - report_writer
  - Report Writer Module
---

# Module: `report_writer.py`

The **XML Parser and Report Generator** parses raw BLAST XML files into structured Python dictionaries, applies statistical quality filtering, and exports the results to CSV and Excel.

---

## Functions & API Reference

### 1. `parse_blast_xml(xml_filepath: str, max_evalue: float = 1e-5, min_identity: float = 90.0, top_n: int = 5, fetch_organism: bool = True) -> List[Dict[str, Any]]`
- **Purpose**: Parses alignment hits from XML, applies user cutoffs, and sorts by significance.
- **Workflow**:
  1. Opens XML via `Bio.Blast.NCBIXML.parse()`.
  2. For each alignment HSP:
     - Computes $\text{Identity (\%)} = \frac{\text{identities}}{\text{align\_length}} \times 100$.
     - Evaluates $\text{E-value} \le \text{max\_evalue}$ and $\text{Identity} \ge \text{min\_identity}$.
     - Resolves organism name using `extract_organism_from_title()` or triggers `fetch_ncbi_metadata()` if unknown.
  3. Sorts all passing matches by `(E-value ascending, -Bit Score descending)`.
  4. Deduplicates hits on `Accession ID` to guarantee diverse accession coverage.
  5. Slices and returns top `N` results.

### 2. `export_reports(results: List[Dict[str, Any]], output_dir: str = "reports", base_name: str = "blast_report") -> Dict[str, str]`
- **Purpose**: Serializes filtered hit records to CSV and Excel (`.xlsx`).
- **Columns**: `Accession ID`, `Organism Name`, `Definition`, `Alignment Length`, `Bit Score`, `E-value`, `Identity (%)`.
- **Encodings**: Uses `utf-8-sig` (CSV) for Excel UTF-8 compatibility and `openpyxl` engine for native Excel spreadsheets.

---

## Related Documentation
- [[codebase-blast-pipeline]]
- [[BLAST-Alignment-Filtering]]
- [[Karlin-Altschul-Statistics]]
- [[Pipeline-Architecture]]
