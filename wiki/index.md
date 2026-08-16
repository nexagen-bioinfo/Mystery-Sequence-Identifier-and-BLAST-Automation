# Wiki Index

Welcome to the Persistent LLM Knowledge Base. This index is dynamically maintained by the LLM on every ingestion and synthesis cycle.

---

## 📚 Synthesis & Overviews
- [[Pipeline-Architecture]] — End-to-end dataflow, component breakdown, caching strategy, and sequence identification workflow.

---

## 💡 Concepts & Methods
- [[Sequence-Type-Inference]] — Nucleotide vs. protein composition heuristics and BLAST program/database selection.
- [[BLAST-Alignment-Filtering]] — Statistical cutoffs (E-value, Identity %, Bit Score), ranking, and taxonomy resolution fallback.
- [[FASTA-Format]] — Sequence text representation, header parsing, and sanitization.

---

## 🏷️ Entities & Tools
- [[Biopython]] — Python bioinformatics tool suite (`SeqIO`, `Entrez`, `NCBIWWW`, `NCBIXML`).
- [[NCBI-BLAST]] — Remote sequence search tool, `blastn`/`blastp` algorithms, and `nt`/`nr` databases.
- [[NCBI-Entrez]] — NCBI E-utilities web service API (`efetch`, `esummary`) for sequence downloads and taxonomic metadata.

---

## 📄 Ingested Sources
- [[codebase-blast-pipeline]] — Comprehensive architectural analysis of the Mystery Sequence Identifier & BLAST Automation codebase.
