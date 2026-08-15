"""
XML Parser and Report Generator Module.
Parses BLAST XML results, applies statistical filtering, and exports CSV/Excel reports.
"""

import os
from typing import List, Dict, Any, Optional
import pandas as pd
from Bio.Blast import NCBIXML
from sequence_io import fetch_ncbi_metadata, extract_organism_from_title


def parse_blast_xml(
    xml_filepath: str,
    max_evalue: float = 1e-5,
    min_identity: float = 90.0,
    top_n: int = 5,
    fetch_organism: bool = True
) -> List[Dict[str, Any]]:
    """
    Parses BLAST XML output, applies filtering rules, and returns top N alignment hits.

    :param xml_filepath: Path to the XML file
    :param max_evalue: Maximum E-value threshold
    :param min_identity: Minimum identity percentage threshold
    :param top_n: Number of top matches to return
    :param fetch_organism: Resolve organism name via Entrez if missing
    :return: List of filtered alignment hit dictionaries
    """
    if not os.path.exists(xml_filepath):
        raise FileNotFoundError(f"XML file not found: {xml_filepath}")

    results = []

    with open(xml_filepath, "r", encoding="utf-8") as xml_handle:
        blast_records = list(NCBIXML.parse(xml_handle))

    for record in blast_records:
        for alignment in record.alignments:
            accession_id = alignment.accession if alignment.accession else alignment.hit_id
            full_title = alignment.title if alignment.title else alignment.hit_def

            for hsp in alignment.hsps:
                e_value = float(hsp.expect)
                align_length = int(hsp.align_length)
                bit_score = float(hsp.bits)
                identity_pct = (hsp.identities / align_length) * 100.0 if align_length > 0 else 0.0

                if e_value <= max_evalue and identity_pct >= min_identity:
                    organism_name = extract_organism_from_title(full_title)
                    definition = full_title

                    if fetch_organism and organism_name == "Unknown Organism" and accession_id:
                        meta = fetch_ncbi_metadata(accession_id)
                        organism_name = meta.get("organism", organism_name)
                        if meta.get("definition") and meta["definition"] != "No description available":
                            definition = meta["definition"]

                    results.append({
                        "Accession ID": accession_id,
                        "Organism Name": organism_name,
                        "Definition": definition,
                        "Alignment Length": align_length,
                        "Bit Score": round(bit_score, 2),
                        "E-value": e_value,
                        "Identity (%)": round(identity_pct, 2)
                    })

    results.sort(key=lambda x: (x["E-value"], -x["Bit Score"]))

    seen_accessions = set()
    top_results = []
    for item in results:
        acc = item["Accession ID"]
        if acc not in seen_accessions:
            seen_accessions.add(acc)
            top_results.append(item)
        if len(top_results) == top_n:
            break

    return top_results


def export_reports(
    results: List[Dict[str, Any]],
    output_dir: str = "reports",
    base_name: str = "blast_report"
) -> Dict[str, str]:
    """
    Exports filtered results to CSV and Excel format.

    :param results: List of filtered alignment results
    :param output_dir: Directory to save generated reports
    :param base_name: Base filename for output files
    :return: Dictionary containing file paths for CSV and Excel files
    """
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.abspath(os.path.join(output_dir, f"{base_name}.csv"))
    excel_path = os.path.abspath(os.path.join(output_dir, f"{base_name}.xlsx"))

    columns = [
        "Accession ID",
        "Organism Name",
        "Definition",
        "Alignment Length",
        "Bit Score",
        "E-value",
        "Identity (%)"
    ]

    df = pd.DataFrame(results, columns=columns) if results else pd.DataFrame(columns=columns)

    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"[REPORT] CSV report created: {csv_path}")

    try:
        df.to_excel(excel_path, index=False, engine="openpyxl")
        print(f"[REPORT] Excel report created: {excel_path}")
    except Exception as e:
        print(f"Warning: openpyxl error during Excel export: {e}")
        excel_path = ""

    return {"csv": csv_path, "excel": excel_path}
