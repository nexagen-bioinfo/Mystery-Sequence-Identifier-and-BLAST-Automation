---
title: "Local Standalone BLAST+ Installation and Database Indexing"
type: synthesis
tags:
  - blast/cli
  - performance/optimization
  - high-throughput/bioinformatics
created: 2026-08-18
updated: 2026-08-18
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - Local BLAST Guide
  - makeblastdb Guide
  - Standalone BLAST+ Execution
---

# Local Standalone BLAST+ Installation and Database Indexing

This guide details the technical blueprint for deploying and operating a standalone **NCBI BLAST+** execution engine alongside the Python automation pipeline.

---

## 1. Installation & Environment Setup

Standalone BLAST+ binaries (`blastn`, `blastp`, `blastx`, `makeblastdb`, `blastdbcmd`) can be deployed via multiple channels:

### Option A: Conda / Bioconda (Recommended)
```bash
conda create -n blast-env -c bioconda blast
conda activate blast-env
```

### Option B: Precompiled NCBI Binaries
- Download from NCBI FTP: `ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/`
- Add binary directory to system `$PATH`.

---

## 2. Formatting Custom Databases with `makeblastdb`

To search mystery sequences against local reference genomes or custom sequence collections:

### For Nucleotide Databases (DNA/RNA):
```bash
makeblastdb -in custom_references.fasta \
            -dbtype nucl \
            -title "Custom_Nucl_DB" \
            -out db/custom_nucl \
            -parse_seqids
```

### For Protein Databases:
```bash
makeblastdb -in proteins.fasta \
            -dbtype prot \
            -title "Custom_Prot_DB" \
            -out db/custom_prot \
            -parse_seqids
```

`-parse_seqids` enables fast retrieval of sequence headers and alignment sub-ranges using `blastdbcmd`.

---

## 3. High-Throughput Execution Command

To execute high-speed local batch alignments producing tabular TSV output compatible with pipeline statistical filtering:

```bash
blastn -query data/NC_012920.fasta \
       -db db/custom_nucl \
       -evalue 1e-5 \
       -num_threads 8 \
       -max_target_seqs 10 \
       -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle" \
       -out results/local_blast_hits.tsv
```

---

## 4. Integration with Python Pipeline

Local execution can be incorporated into [`blast_engine.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/blast_engine.py) via Python's `subprocess` or `Bio.Blast.Applications.NcbiblastnCommandline`:

```python
import subprocess

def run_local_blast(query_path: str, db_path: str, program: str = "blastn", evalue: float = 1e-5, threads: int = 4) -> str:
    output_xml = f"cache/local_{program}_results.xml"
    cmd = [
        program,
        "-query", query_path,
        "-db", db_path,
        "-evalue", str(evalue),
        "-num_threads", str(threads),
        "-outfmt", "5",  # XML format for Bio.Blast.NCBIXML parsing
        "-out", output_xml
    ]
    subprocess.run(cmd, check=True)
    return output_xml
```

---

## Cross-References
- [[Remote-vs-Local-BLAST]]
- [[Pipeline-Architecture]]
- [[module-blast-engine]]
- [[Karlin-Altschul-Statistics]]
