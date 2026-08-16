---
title: "Script: download_data.py"
type: entity
tags:
  - script/data-fetcher
  - benchmarks/ncbi-pdb
created: 2026-08-17
updated: 2026-08-17
sources:
  - "[[codebase-blast-pipeline]]"
aliases:
  - download_data
  - Data Fetcher Script
---

# Script: `download_data.py`

The **Data Fetcher Script** automatically pulls the 4 benchmark validation sequences from NCBI Entrez and RCSB PDB into the `data/` directory.

---

## Accessions Catalog

```python
ACCESSIONS = [
    {"id": "NC_012920", "type": "dna", "db": "nucleotide", "source": "ncbi"},
    {"id": "AC_000021", "type": "dna", "db": "nucleotide", "source": "ncbi"},
    {"id": "PZ716984", "type": "rna", "db": "nucleotide", "source": "ncbi"},
    {"id": "9GE4", "type": "protein", "db": "pdb", "source": "rcsb"}
]
```

---

## Mechanics
1. **NCBI E-Utilities**: For `NC_012920`, `AC_000021`, and `PZ716984`, queries `Entrez.efetch(db="nucleotide", id=acc_id, rettype="fasta", retmode="text")`.
2. **RCSB PDB Direct Fetch**: For `9GE4`, uses `urllib.request` against `https://www.rcsb.org/fasta/entry/9GE4`.
3. **Validation**: Verifies that the downloaded string starts with `>` before writing to `data/<accession_id>.fasta`.

---

## Related Documentation
- [[codebase-blast-pipeline]]
- [[Benchmark-Test-Sequences]]
- [[NCBI-Entrez]]
- [[FASTA-Format]]
