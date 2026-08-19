---
title: "Organism: Homo sapiens (Human)"
type: entity
tags:
  - organism/eukaryota
  - taxonomy/taxid-9606
  - benchmark/sequence
  - genetics/mitochondrial
created: 2026-08-19
updated: 2026-08-19
sources:
  - "[[codebase-blast-pipeline]]"
  - "[[Benchmark-Test-Sequences]]"
aliases:
  - Homo sapiens
  - Human
  - TaxID: 9606
---

# Organism: *Homo sapiens* (Human)

## Overview
***Homo sapiens*** (NCBI Taxonomy ID: **9606**) is the primary model organism for human genetic, medical, and evolutionary studies. In this repository's benchmark validation suite, *Homo sapiens* is represented by the complete Revised Cambridge Reference Sequence (rCRS) of the mitochondrial genome ([`NC_012920.fasta`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/data/NC_012920.fasta)).

## Genomic & Benchmark Profile

| Property | Value |
| :--- | :--- |
| **Taxonomy ID** | `9606` |
| **Lineage** | Eukaryota $\rightarrow$ Metazoa $\rightarrow$ Chordata $\rightarrow$ Mammalia $\rightarrow$ Primates $\rightarrow$ Hominidae $\rightarrow$ *Homo* |
| **Benchmark Sequence** | [`NC_012920.1`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/data/NC_012920.fasta) (Mitochondrial Genome) |
| **Sequence Type** | DNA |
| **Length** | 16,569 bp |
| **Target BLAST Program** | `blastn` against `nt` |
| **Expected Alignment** | $\text{Identity} \ge 99.9\%$, $\text{E-value} = 0.0$, $\text{Bit Score} > 30,000$ |

## Related Wiki Pages
- [[Benchmark-Test-Sequences]]
- [[NCBI-Taxonomy-Resolution]]
- [[Sequence-Type-Inference]]
- [[Karlin-Altschul-Statistics]]
- [[Automated-Bioinformatics-Knowledge-Compounding]]
- [[Pipeline-Architecture]]
