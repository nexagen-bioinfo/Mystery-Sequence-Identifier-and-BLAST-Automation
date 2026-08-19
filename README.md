# Mystery Sequence Identifier & BLAST Automation Pipeline — Participant 3 Scope (`suleiman` branch)

This branch contains the isolated scope for **Participant 3 (Suleiman)**: **XML Parser & Report Generator Module** (`report_writer.py`).

---

## Participant 3 Scope & Deliverables

| Module | Description | Test Suite | Demo Script |
| :--- | :--- | :--- | :--- |
| [`report_writer.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/report_writer.py) | BioPython `Bio.Blast.NCBIXML` XML parsing, statistical filtering (E-value $\le 10^{-5}$, Identity % $\ge 90\%$), Top 5 alignment selection, and CSV/Excel report generation. | [`test_report_writer.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/test_report_writer.py) | [`demo_report_writer.py`](file:///Users/macbookairm2/Documents/GitHub/Mystery-Sequence-Identifier-and-BLAST-Automation/demo_report_writer.py) |

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

## Running Participant 3 Module & Tests

### Run Unit Tests
```bash
python test_report_writer.py
```

### Run Interactive Demo
```bash
python demo_report_writer.py
```

---

## Module API Documentation

```python
from report_writer import parse_blast_xml, export_reports

# Parse raw BLAST XML file and apply statistical filtering
results = parse_blast_xml(
    xml_filepath="cache/blast_PZ716984_1.xml",
    max_evalue=1e-5,
    min_identity=90.0,
    top_n=5
)

# Export structured CSV and Excel (.xlsx) reports
report_paths = export_reports(
    results,
    output_dir="reports",
    base_name="final_report"
)
```

---

## License & Organization
NEXAGEN Scientific Initiative (2026)