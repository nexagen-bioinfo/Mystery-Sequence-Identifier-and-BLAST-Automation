# Wiki Index

Welcome to the Persistent LLM Knowledge Base. This index is dynamically maintained by the LLM on every ingestion and synthesis cycle.

---

## 📚 Synthesis & Overviews
- [[Obsidian-LLM-Wiki-Guide]] — Comprehensive architectural guide explaining how Obsidian integrates with the LLM Wiki pattern.
- [[Pipeline-Architecture]] — End-to-end dataflow, component breakdown, caching strategy, and sequence identification workflow.
- [[Benchmark-Test-Sequences]] — Overview of validation dataset suite (`NC_012920`, `AC_000021`, `PZ716984`, `9GE4`), biological significance, and expected BLAST behaviors.
- [[Remote-vs-Local-BLAST]] — Comparative evaluation of remote `Bio.Blast.NCBIWWW` API vs. local standalone `BLAST+` CLI installation.
- [[Local-BLAST-Installation-and-Indexing]] — Concrete guide for standalone NCBI BLAST+ deployment, `makeblastdb` custom database formatting, and high-throughput multi-threaded search.

---

## 💡 Concepts & Methods
- [[Sequence-Type-Inference]] — Nucleotide vs. protein composition heuristics and BLAST program/database selection.
- [[BLAST-Alignment-Filtering]] — Statistical cutoffs (E-value, Identity %, Bit Score), ranking, and taxonomy resolution fallback.
- [[Karlin-Altschul-Statistics]] — Mathematical theory of local sequence alignments, Gumbel distribution, E-values, bit score normalization ($\lambda$, $K$).
- [[Substitution-Matrices-PAM-BLOSUM]] — Evolutionary log-odds matrix principles, BLOSUM62 default, PAM distance models, and affine gap penalty functions.
- [[NCBI-Taxonomy-Resolution]] — Taxonomic identifier (TaxID) mapping, definition line header heuristics, Entrez fallback chain, and phylogenetic lineage traversal.
- [[FASTA-Format]] — Sequence text representation, header parsing, and sanitization.

---

## 🏷️ Entities & Code Modules
- [[module-sequence-io]] — Documentation for [`sequence_io.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/sequence_io.py) (FASTA parsing, type detection, Entrez metadata).
- [[module-blast-engine]] — Documentation for [`blast_engine.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/blast_engine.py) (Remote NCBI query execution, retry loop, XML caching).
- [[module-report-writer]] — Documentation for [`report_writer.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/report_writer.py) (XML parser, statistical filtering, CSV/Excel export).
- [[module-main-cli]] — Documentation for [`main.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/main.py) (CLI options, orchestrator lifecycle).
- [[module-download-data]] — Documentation for [`download_data.py`](file:///c:/Users/User/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/download_data.py) (NCBI & RCSB benchmark data puller).
- [[Biopython]] — Python bioinformatics tool suite (`SeqIO`, `Entrez`, `NCBIWWW`, `NCBIXML`).
- [[NCBI-BLAST]] — Remote sequence search tool, `blastn`/`blastp` algorithms, and `nt`/`nr` databases.
- [[NCBI-Entrez]] — NCBI E-utilities web service API (`efetch`, `esummary`) for sequence downloads and taxonomic metadata.

---

## 📄 Ingested Sources
- [[codebase-blast-pipeline]] — Comprehensive architectural analysis of the Mystery Sequence Identifier & BLAST Automation codebase.
