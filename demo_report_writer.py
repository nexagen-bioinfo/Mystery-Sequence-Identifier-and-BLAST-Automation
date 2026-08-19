"""
Interactive Demo Script for Participant 3 (Suleiman) - XML Parser & Report Generator Module.
Demonstrates parsing raw BLAST XML output, applying statistical filtering, and exporting CSV/Excel reports.
"""

import os
from report_writer import parse_blast_xml, export_reports


def main():
    print("==========================================================================")
    print("Participant 3 (Suleiman) - XML Parser & Report Generator Demo")
    print("==========================================================================")

    sample_xml = "cache/blast_PZ716984_1.xml"

    if not os.path.exists(sample_xml):
        print(f"Warning: Sample XML cache file not found at '{sample_xml}'.")
        print("Please ensure a valid BLAST XML file exists in cache/.")
        return

    print(f"\n[1] Parsing & Filtering BLAST XML: '{sample_xml}'")
    print("    Filter Settings: E-value <= 1e-05 | Identity >= 90.0% | Top Matches: 5")

    results = parse_blast_xml(
        xml_filepath=sample_xml,
        max_evalue=1e-5,
        min_identity=90.0,
        top_n=5,
        fetch_organism=False
    )

    print(f"\n[2] Filtered Results ({len(results)} matches found):\n")
    print("-" * 80)
    print(f"{'Accession ID':<15} | {'Identity (%)':<12} | {'E-value':<10} | {'Organism Name'}")
    print("-" * 80)

    for item in results:
        print(f"{item['Accession ID']:<15} | {item['Identity (%)']:<12.2f} | {item['E-value']:<10.1e} | {item['Organism Name']}")

    print("-" * 80)

    # Step 3: Export CSV and Excel reports
    print("\n[3] Exporting CSV and Excel Reports...")
    out_files = export_reports(results, output_dir="reports", base_name="demo_report_suleiman")

    print(f"\n[SUCCESS] CSV Report: {out_files['csv']}")
    if out_files['excel']:
        print(f"[SUCCESS] Excel Report: {out_files['excel']}")

    print("==========================================================================")


if __name__ == "__main__":
    main()
