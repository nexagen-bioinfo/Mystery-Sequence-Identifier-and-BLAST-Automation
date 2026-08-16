---
title: "Module: sequence_io.py"
type: entity
tags:
  - module/python
  - sequence-analysis/io
  - entrez/metadata
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - sequence_io
  - Sequence IO Module
---

# Module: `sequence_io.py`

The **Sequence Manager and Entrez Interface** module is responsible for loading input sequences, classifying their biological type, and enriching alignment hits with taxonomy metadata via NCBI Entrez.

---

## Functions & API Reference

### 1. `parse_fasta(input_source: str) -> SeqRecord`
- **Purpose**: Parses a biological sequence into a [[Biopython]] `SeqRecord` object.
- **Inputs**: File path (e.g. `data/PZ716984.fasta`) or a raw multi-line FASTA string starting with `>`.
- **Error Handling**: Raises `ValueError` if the sequence is empty or improperly formatted; raises `FileNotFoundError` if the file path is non-existent.

### 2. `detect_sequence_type(seq_record: SeqRecord) -> Dict[str, Union[str, int]]`
- **Purpose**: Implements the [[Sequence-Type-Inference]] algorithm.
- **Logic**:
  - Valid nucleotide set: `A, T, C, G, U, N`.
  - Calculates $\text{nuc\_ratio} = \frac{\text{valid nucleotide count}}{\text{total sequence length}}$.
  - If $\text{nuc\_ratio} \ge 0.90$:
    - Contains `U` and no `T` $\rightarrow$ **`RNA`** (Target: `blastn`, DB: `nt`).
    - Contains `T` or no `U` $\rightarrow$ **`DNA`** (Target: `blastn`, DB: `nt`).
  - If $\text{nuc\_ratio} < 0.90$ $\rightarrow$ **`PROTEIN`** (Target: `blastp`, DB: `nr`).
- **Returns**: Dictionary with `sequence_id`, `sequence_type`, `blast_program`, `database`, and `length`.

### 3. `extract_organism_from_title(title: str) -> str`
- **Purpose**: Heuristic parser to extract scientific organism names from NCBI definition lines.
- **Mechanics**:
  - Strips GI accession prefixes (e.g., `gi|887494115|gb|KT232088.1|`).
  - Looks for bracketed taxonomy markers (e.g., `[Homo sapiens]`).
  - Scans for standard genomic keyword boundaries (` complete cds `, ` mRNA `, ` segment `, ` gene `).

### 4. `fetch_ncbi_metadata(accession_id: str, email: str = "user@example.com", db: Optional[str] = None) -> Dict[str, str]`
- **Purpose**: Interrogates [[NCBI-Entrez]] E-Utilities as a fallback when hit titles lack taxonomy information.
- **Fallback Chain**:
  1. `Entrez.efetch(db=target_db, id=accession_id, rettype="gb", retmode="text")` to read full GenBank taxonomy annotations.
  2. `Entrez.esummary(db=target_db, id=accession_id, retmode="xml")` to parse document summary titles and captions.

---

## Related Documentation
- [[codebase-blast-pipeline]]
- [[Sequence-Type-Inference]]
- [[FASTA-Format]]
- [[NCBI-Entrez]]
- [[Pipeline-Architecture]]
