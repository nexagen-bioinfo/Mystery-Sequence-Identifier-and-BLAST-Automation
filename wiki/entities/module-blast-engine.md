---
title: "Module: blast_engine.py"
type: entity
tags:
  - module/python
  - blast/engine
  - caching/xml
created: 2026-08-17
updated: 2026-08-18
sources:
  - "[[codebase-blast-pipeline]]"
  - "[[altschul-1990-blast]]"
aliases:
  - blast_engine
  - BLAST Engine Module
---

# Module: `blast_engine.py`

The **BLAST Engine** manages local standalone [[NCBI-BLAST]] CLI execution (`blastn`/`blastp` via subprocess) and remote NCBI QBLAST web service communication, caching raw XML results and handling automatic fallback.

---

## Functions & API Reference

### 1. `run_blast(seq_record, mode="auto", db=None, num_threads=4, cache_dir="cache", force_reblast=False, max_retries=3, retry_delay=10, hitlist_size=10, expect=1e-5) -> str`
- **Purpose**: Main orchestrator for sequence alignment execution.
- **Modes**:
  - `mode="auto"`: Checks if local binary and custom database exist; if so executes locally, otherwise queries remote NCBI API.
  - `mode="local"`: Forces local BLAST+ CLI execution via `subprocess`.
  - `mode="remote"`: Forces remote NCBI QBLAST execution via `Bio.Blast.NCBIWWW.qblast`.
- **Caching**: Generates deterministic XML files (`cache/blast_<safe_id>.xml`) to skip redundant queries.

### 2. `run_local_blast(seq_record, db, output_xml_path, program="blastn", num_threads=4, hitlist_size=10, expect=1e-5) -> str`
- **Purpose**: Spawns local `blastn`/`blastp` process with `-outfmt 5` (XML output), multi-threading (`-num_threads`), and E-value thresholding.

### 3. `run_remote_blast(seq_record, output_xml_path, program, database, max_retries=3, retry_delay=10, hitlist_size=10, expect=1e-5) -> str`
- **Purpose**: Submits queries to NCBI web servers with retry backoff loop and XML integrity validation (`<BlastOutput>`).

### 4. `check_local_blast_available(program: str) -> bool`
- **Purpose**: Utilizes `shutil.which` to detect if BLAST+ binaries reside in system `$PATH`.

---

## Related Documentation
- [[codebase-blast-pipeline]]
- [[NCBI-BLAST]]
- [[Remote-vs-Local-BLAST]]
- [[Local-BLAST-Installation-and-Indexing]]
- [[Pipeline-Architecture]]
- [[Seed-and-Extend-Heuristic]]
