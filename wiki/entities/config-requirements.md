---
title: "Config: requirements.txt"
type: entity
tags:
  - config/dependencies
  - python/packaging
created: 2026-08-18
updated: 2026-08-18
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - requirements.txt
  - Project Dependencies
---

# Config: `requirements.txt`

The **Dependencies Configuration** specifies core third-party Python packages required to run the sequence identification pipeline, alignment engine, XML parsing, and tabular report generation.

---

## Package Manifest

| Package | Minimum Version | Primary Purpose | Used By |
| :--- | :--- | :--- | :--- |
| **`biopython`** | `>=1.80` | FASTA IO, Entrez E-utilities, NCBIWWW remote QBLAST, NCBIXML parsing | [[module-sequence-io]], [[module-blast-engine]], [[module-report-writer]], [[module-download-data]] |
| **`pandas`** | `>=2.0.0` | Dataframe transformation and tabular formatting for alignment hits | [[module-report-writer]] |
| **`openpyxl`** | `>=3.1.0` | Excel spreadsheet engine supporting `.xlsx` export | [[module-report-writer]] |

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Related Documentation
- [[codebase-blast-pipeline]]
- [[Biopython]]
- [[module-report-writer]]
- [[Pipeline-Architecture]]
