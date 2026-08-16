---
title: "Script: main.py"
type: entity
tags:
  - script/cli
  - orchestrator/entrypoint
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - main
  - Pipeline CLI Orchestrator
---

# Script: `main.py`

The **CLI Orchestrator** serves as the user-facing command-line interface for the Mystery Sequence Identifier pipeline.

---

## CLI Flags & Arguments

| Flag | Short | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `--input` | `-i` | `str` | *Required* | Path to the query FASTA file (e.g. `data/PZ716984.fasta`). |
| `--force-reblast` | `-f` | `bool` | `False` | Forces a fresh remote NCBI query even if local XML cache exists. |
| `--evalue` | `-e` | `float` | `1e-5` | Statistical expectation cutoff for alignment hits. |
| `--identity` | `-id` | `float` | `90.0` | Minimum sequence percent identity threshold ($0.0 - 100.0\%$). |
| `--top` | `-t` | `int` | `5` | Maximum number of ranked accession matches to report. |

---

## Execution Lifecycle

```
[STEP 1: Parse & Classify]
   └── Calls sequence_io.parse_fasta() & detect_sequence_type()
   └── Outputs detected Sequence Type, BLAST Program, Database, Length

[STEP 2: Query Execution]
   └── Calls blast_engine.run_blast()
   └── Checks local cache or submits remote NCBIWWW query

[STEP 3: Parse & Filter]
   └── Calls report_writer.parse_blast_xml()
   └── Displays formatted terminal summary table

[STEP 4: Export Reports]
   └── Calls report_writer.export_reports()
   └── Writes reports/report_<id>.csv & reports/report_<id>.xlsx
```

---

## Related Documentation
- [[codebase-blast-pipeline]]
- [[Pipeline-Architecture]]
- [[module-sequence-io]]
- [[module-blast-engine]]
- [[module-report-writer]]
