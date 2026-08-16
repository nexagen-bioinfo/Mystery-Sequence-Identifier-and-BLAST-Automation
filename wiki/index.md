# Wiki Index

Welcome to the Persistent LLM Knowledge Base. This index is dynamically maintained by the LLM on every ingestion and synthesis cycle.

---

## 📚 Synthesis & Overviews
- [[Pipeline-Architecture]] — End-to-end dataflow, component breakdown, caching strategy, and sequence identification workflow.
- [[Benchmark-Test-Sequences]] — Overview of validation dataset suite (`NC_012920`, `AC_000021`, `PZ716984`, `9GE4`), biological significance, and expected BLAST behaviors.
- [[Remote-vs-Local-BLAST]] — Comparative evaluation of remote `Bio.Blast.NCBIWWW` API vs. local standalone `BLAST+` CLI installation.

---

## 💡 Concepts & Methods
- [[Sequence-Type-Inference]] — Nucleotide vs. protein composition heuristics and BLAST program/database selection.
- [[BLAST-Alignment-Filtering]] — Statistical cutoffs (E-value, Identity %, Bit Score), ranking, and taxonomy resolution fallback.
- [[Karlin-Altschul-Statistics]] — Mathematical theory of local sequence alignments, Gumbel distribution, E-values, bit score normalization ($\lambda$, $K$).
- [[FASTA-Format]] — Sequence text representation, header parsing, and sanitization.

---

## 🏷️ Entities & Tools
- [[Biopython]] — Python bioinformatics tool suite (`SeqIO`, `Entrez`, `NCBIWWW`, `NCBIXML`).
- [[NCBI-BLAST]] — Remote sequence search tool, `blastn`/`blastp` algorithms, and `nt`/`nr` databases.
- [[NCBI-Entrez]] — NCBI E-utilities web service API (`efetch`, `esummary`) for sequence downloads and taxonomic metadata.

---

## 📄 Ingested Sources
- [[codebase-blast-pipeline]] — Comprehensive architectural analysis of the Mystery Sequence Identifier & BLAST Automation codebase.
