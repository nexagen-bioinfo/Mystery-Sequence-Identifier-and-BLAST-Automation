# Mystery Sequence Identifier & BLAST Automation Pipeline — Participant 2 Scope (`mehriban` branch)

This branch contains the isolated scope for **Participant 2 (Mehriban)**: **Remote BLAST Engine Module** (`blast_engine.py`).

---

## Participant 2 Scope & Deliverables

| Module | Description | Test Suite | Demo Script |
| :--- | :--- | :--- | :--- |
| [`blast_engine.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/blast_engine.py) | BioPython `Bio.Blast.NCBIWWW.qblast()` query execution (`blastn` vs `blastp`), retry & timeout handling, and raw XML caching system (`cache/`). | [`test_blast_engine.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/test_blast_engine.py) | [`demo_blast.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/demo_blast.py) |

---

## Installation & Setup

1. **Activate Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running Participant 2 Module & Tests

### Run Unit Tests
```bash
python test_blast_engine.py
```

### Run Interactive Demo
```bash
python demo_blast.py
```

---

## Module API Documentation

```python
from blast_engine import run_blast, detect_sequence_type

# Detect sequence composition (DNA, RNA, or Protein)
info = detect_sequence_type(seq_record)

# Execute remote BLAST query and cache raw XML result
xml_filepath = run_blast(
    seq_record,
    cache_dir="cache",
    force_reblast=False,
    max_retries=5,
    retry_delay=30
)
```

---

## License & Organization
NEXAGEN Scientific Initiative (2026)