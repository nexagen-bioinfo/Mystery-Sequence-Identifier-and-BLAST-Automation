# Mystery Sequence Identifier & BLAST Automation Pipeline

A modular bioinformatics pipeline for identifying unknown biological DNA, RNA, or Protein sequences (in FASTA format), integrating with NCBI (National Center for Biotechnology Information) databases, and exporting structured analysis reports (CSV and Excel format).

---

## Architecture and Work Division

The project is structured into three main modules:

| Participant | Responsibility | Output Module |
| :--- | :--- | :--- |
| **Participant 1** | FASTA file parsing, sequence type detection (DNA, RNA, Protein), BLAST tool selection (`blastn` vs `blastp`), and NCBI Entrez metadata retrieval. | [`sequence_io.py`](sequence_io.py) |
| **Participant 2** | Remote query execution via `Bio.Blast.NCBIWWW` against `nt` or `nr` databases, network timeout/exception handling, and raw XML caching. | [`blast_engine.py`](blast_engine.py) |
| **Participant 3** | XML parsing using `Bio.Blast.NCBIXML`, statistical filtering (E-value / Identity %), and CSV/Excel report generation. | [`report_writer.py`](report_writer.py) |

---

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/nexagen-bioinfo/Mystery-Sequence-Identifier-and-BLAST-Automation.git
cd Mystery-Sequence-Identifier-and-BLAST-Automation
```

### 2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
# venv\Scripts\activate   # Windows
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

Run the pipeline from the command line using `main.py`:

```bash
python main.py --input data/PZ716984.fasta
```

### CLI Arguments

```bash
# Specify custom E-value, Identity %, and Top Hıts threshold:
python main.py --input data/PZ716984.fasta --evalue 1e-10 --identity 95.0 --top 10

# Force remote BLAST query ignoring cached XML:
python main.py --input data/PZ716984.fasta --force-reblast
```

#### Argument Details:
* `--input` / `-i`: **(Required)** Path to input FASTA sequence file.
* `--evalue` / `-e`: Maximum E-value cutoff *(Default: 1e-5)*.
* `--identity` / `-id`: Minimum Identity percentage cutoff *(Default: 90.0)*.
* `--top` / `-t`: Number of top alignment matches to report *(Default: 5)*.
* `--force-reblast` / `-f`: Bypass local cache and force new NCBI query.

---

## Project Structure and Output Files

* **`cache/`**: Contains raw XML response files returned from NCBI queries to prevent redundant network requests.
* **`reports/`**: Output directory for generated CSV and Excel reports.
* **`data/`**: Sample FASTA sequences for testing and validation.

---

## License and Author Information

NEXAGEN Scientific Initiative (2026)