---
title: "PSI-BLAST (Position-Specific Iterated BLAST)"
type: entity
tags:
  - bioinformatics/tool
  - cli/executable
  - blast/profile
created: 2026-08-19
updated: 2026-08-19
sources:
  - "[[altschul-1997-gapped-blast]]"
aliases:
  - psiblast
  - PSI-BLAST CLI
  - Position-Specific Iterated BLAST Tool
---

# PSI-BLAST (`psiblast`)

**`psiblast`** is a standalone CLI tool in the [[NCBI-BLAST|NCBI BLAST+]] software suite that implements iterative profile searching for high-sensitivity protein sequence identification and remote homology detection.

---

## 🛠️ CLI Syntax & Core Options

```bash
psiblast \
  -query query.fasta \
  -db nr \
  -num_iterations 3 \
  -inclusion_ethresh 0.005 \
  -out_pssm checkpoint.pssm \
  -out_ascii_pssm checkpoint.ascii.pssm \
  -out results.xml \
  -outfmt 5 \
  -num_threads 16
```

### Key Parameter Reference:
- `-query <file>`: Input FASTA query protein sequence.
- `-db <name>`: Target BLAST formatted database (e.g., `nr`, `swissprot`, `refseq_protein`).
- `-num_iterations <int>`: Maximum number of iterative search rounds (default: `1`, typical: `3` to `5`).
- `-inclusion_ethresh <float>`: $E$-value cutoff for including hits into the next iteration's PSSM (default: `0.002`).
- `-out_pssm <file>`: Output binary checkpoint file storing the generated PSSM.
- `-in_pssm <file>`: Use a precomputed PSSM directly as query scoring matrix without running initial rounds.
- `-out_ascii_pssm <file>`: Export human-readable ASCII PSSM containing log-odds scores and information content.
- `-comp_based_stats <int>`: Composition-based score adjustment (`0` = none, `1` = composition-based statistics, `2` = conditioned composition-based score matrix adjustment, default: `2`).

---

## 🔬 Scientific Applications

1. **Remote Homology Search**: Identifying ancestral structural relatives when sequence identity falls below $20\%$.
2. **Domain Architecture Annotation**: Building conserved domain PSSMs (foundational to the NCBI CDD database).
3. **Sequence Checkpointing**: Generating PSSMs for downstream structural prediction (e.g., secondary structure prediction in PSIPRED, early AlphaFold input features).

---

## 🔗 Related Pages
- **Foundational Source**: [[altschul-1997-gapped-blast]]
- **Underlying Concept**: [[Position-Specific-Iterated-BLAST]], [[Two-Hit-Seed-Heuristic]], [[Karlin-Altschul-Statistics]]
- **Parent Suite**: [[NCBI-BLAST]], [[Biopython]]
- **Modern Alternatives**: [[MMseqs2]] (`mmseqs search -s 7`), HH-suite (`hhblits`), DIAMOND (`diamond blastp --ultra-sensitive`)
- **Synthesis Overview**: [[Profile-Search-and-Remote-Homology]], [[Heuristic-Alignment-Paradigms-BLAST-DIAMOND-MMseqs2]]
