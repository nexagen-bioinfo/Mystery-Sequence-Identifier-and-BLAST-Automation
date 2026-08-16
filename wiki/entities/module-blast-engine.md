---
title: "Module: blast_engine.py"
type: entity
tags:
  - module/python
  - blast/engine
  - caching/xml
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - blast_engine
  - BLAST Engine Module
---

# Module: `blast_engine.py`

The **Remote BLAST Engine** manages network communication with the remote NCBI BLAST QBLAST web service, manages local caching of raw XML results, and handles network resilience.

---

## Functions & API Reference

### `run_blast(seq_record, cache_dir="cache", force_reblast=False, max_retries=3, retry_delay=10, hitlist_size=10, expect=1e-5) -> str`

- **Purpose**: Executes a remote BLAST query or retrieves a previously cached XML file.
- **Workflow**:
  1. **Deterministic Cache Check**:
     - Computes safe filename: `cache/blast_<sanitized_id>.xml`.
     - If file exists and `force_reblast=False`, loads directly from disk.
  2. **Parameter Selection**:
     - Calls `detect_sequence_type()` from [[module-sequence-io]] to dynamically set `program` (`blastn`/`blastp`) and `database` (`nt`/`nr`).
  3. **Resilient Network Execution**:
     - Invokes `Bio.Blast.NCBIWWW.qblast()`.
     - Wraps execution in a retry loop (default `3` attempts with `10s` backoff between attempts).
     - Validates that the returned payload contains the closing `<BlastOutput>` tag to prevent corrupted partial downloads.
  4. **Persistence**:
     - Writes the verified XML string to the local `cache/` directory.
- **Returns**: Absolute filesystem path to the XML cache file.

---

## Related Documentation
- [[codebase-blast-pipeline]]
- [[NCBI-BLAST]]
- [[Remote-vs-Local-BLAST]]
- [[Pipeline-Architecture]]
