# Mystery Sequence Identifier & BLAST Automation Pipeline (`main` branch)

A modular bioinformatics pipeline for identifying unknown biological DNA, RNA, or Protein sequences (in FASTA format), integrating with NCBI (National Center for Biotechnology Information) databases, and exporting structured analysis reports (CSV and Excel format).

---

## 🏗 Pipeline Architecture & Work Division (3 Participants)

The unified pipeline in the `main` branch integrates the core modules developed across the 3 participant branches:

| Participant / Branch | Module Scope | Deliverable | Description |
| :--- | :--- | :--- | :--- |
| **Participant 1** (`adiba`) | Sequence Manager & Entrez Interface | [`sequence_io.py`](sequence_io.py) | FASTA parsing, sequence type inference (`blastn` vs `blastp`), and NCBI Entrez metadata retrieval. |
| **Participant 2** (`mehriban`) | Remote BLAST Engine | [`blast_engine.py`](blast_engine.py) | `Bio.Blast.NCBIWWW` query execution (`nt` vs `nr`), retry/timeout handling, and raw XML caching system. |
| **Participant 3** (`suleiman`) | XML Parser & Report Generator | [`report_writer.py`](report_writer.py) | `Bio.Blast.NCBIXML` parsing, statistical filtering ($E \le 10^{-5}$, Identity $\ge 90\%$), and CSV/Excel report generation. |

---

## 🚀 Quick Start & Installation

1. **Activate Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Unified Pipeline**:
   ```bash
   python main.py --input data/mystery_sequence.fasta
   ```

---

## 💻 CLI Options (`main.py`)

```bash
# Custom E-value, Identity %, and Top Hits cutoff:
python main.py --input data/PZ716984.fasta --evalue 1e-10 --identity 95.0 --top 10

# Force remote BLAST query (ignore local XML cache):
python main.py --input data/PZ716984.fasta --force-reblast
```

### CLI Parameter Details:
- `--input` / `-i`: **(Required)** Path to input FASTA sequence file.
- `--evalue` / `-e`: Maximum E-value cutoff *(Default: 1e-5)*.
- `--identity` / `-id`: Minimum Identity percentage cutoff *(Default: 90.0)*.
- `--top` / `-t`: Number of top alignment matches to report *(Default: 5)*.
- `--force-reblast` / `-f`: Bypass local cache and force new NCBI query.

---

## 🧪 Running Unit Tests

Run the full unified pipeline test suite:
```bash
python test_pipeline.py
```

---

## 📁 Directory Structure

```
├── sequence_io.py       # Participant 1 Module (Sequence Input & Entrez)
├── blast_engine.py      # Participant 2 Module (Remote NCBI BLAST Engine)
├── report_writer.py     # Participant 3 Module (XML Parser & Report Generator)
├── main.py              # Unified CLI Entry Point (Pipeline Orchestrator)
├── test_pipeline.py     # Comprehensive Test Suite
├── cache/               # Raw NCBI BLAST XML Cache Directory
├── reports/             # Generated CSV and Excel Analysis Reports
└── data/                # Benchmark Test FASTA Sequences
```

---

## 📜 License and Community
NEXAGEN Scientific Initiative — Bioinformatics & AI Initiative (2026)