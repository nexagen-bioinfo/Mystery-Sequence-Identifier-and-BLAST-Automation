"""
Main CLI Pipeline Script.
Integrates sequence parsing, local/remote BLAST query execution, XML filtering, and report generation.

Usage:
    python main.py --input data/PZ716984.fasta
    python main.py --input data/PZ716984.fasta --mode local --db nt --threads 8
"""

import os
import sys
import argparse
from sequence_io import parse_fasta, detect_sequence_type
from blast_engine import run_blast
from report_writer import parse_blast_xml, export_reports


def main():
    parser = argparse.ArgumentParser(
        description="Mystery Sequence Identifier & BLAST Automation Pipeline (Local & Remote)"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input FASTA file (e.g. data/PZ716984.fasta)"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["auto", "local", "remote"],
        default="auto",
        help="BLAST execution mode: 'auto' (detect local if db provided, else remote), 'local', or 'remote' (default: auto)"
    )
    parser.add_argument(
        "--db", "-d",
        default=None,
        help="Target BLAST database path or name (e.g. 'nt', 'nr', or local db path)"
    )
    parser.add_argument(
        "--threads", "-j",
        type=int,
        default=4,
        help="Number of CPU threads for local BLAST execution (default: 4)"
    )
    parser.add_argument(
        "--force-reblast", "-f",
        action="store_true",
        help="Force re-query regardless of cached XML"
    )
    parser.add_argument(
        "--evalue", "-e",
        type=float,
        default=1e-5,
        help="Maximum E-value cutoff (default: 1e-5)"
    )
    parser.add_argument(
        "--identity", "-id",
        type=float,
        default=90.0,
        help="Minimum identity percentage cutoff (default: 90.0)"
    )
    parser.add_argument(
        "--top", "-t",
        type=int,
        default=5,
        help="Number of top hits to include in report (default: 5)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="reports",
        help="Directory to save generated CSV and Excel reports (default: reports)"
    )

    args = parser.parse_args()

    print("==========================================================================")
    print("Mystery Sequence Identifier & BLAST Automation Pipeline")
    print("==========================================================================")

    print(f"\n[STEP 1] Parsing input FASTA file: '{args.input}'")
    seq_record = parse_fasta(args.input)
    print(f"Sequence ID: {seq_record.id}")

    seq_info = detect_sequence_type(seq_record)
    print(f"Sequence Type: {seq_info['sequence_type']}")
    print(f"Selected BLAST Program: {seq_info['blast_program'].upper()} | Default DB: {seq_info['database']}")
    print(f"Sequence Length: {seq_info['length']} bp/aa")

    print(f"\n[STEP 2] Executing BLAST search (Mode: {args.mode.upper()})...")
    xml_filepath = run_blast(
        seq_record,
        mode=args.mode,
        db=args.db,
        num_threads=args.threads,
        force_reblast=args.force_reblast,
        expect=args.evalue
    )

    print(f"\n[STEP 3] Parsing and filtering BLAST XML output...")
    print(f"Filter settings: E-value <= {args.evalue} | Identity >= {args.identity}%")
    top_hits = parse_blast_xml(
        xml_filepath,
        max_evalue=args.evalue,
        min_identity=args.identity,
        top_n=args.top
    )

    print(f"Top matches identified: {len(top_hits)}")

    if top_hits:
        print("\n--------------------------------------------------------------------------")
        print(f"{'Accession ID':<15} | {'Identity (%)':<12} | {'E-value':<10} | {'Organism Name'}")
        print("--------------------------------------------------------------------------")
        for hit in top_hits:
            print(f"{hit['Accession ID']:<15} | {hit['Identity (%)']:<12.2f} | {hit['E-value']:<10.1e} | {hit['Organism Name']}")
        print("--------------------------------------------------------------------------")

        base_name = f"report_{str(seq_record.id).replace('|', '_').replace('/', '_')}"
        reports = export_reports(top_hits, output_dir=args.output_dir, base_name=base_name)

        print("\nPipeline execution completed successfully.")
        print(f"CSV Report: {reports['csv']}")
        if reports.get('excel'):
            print(f"Excel Report: {reports['excel']}")
    else:
        print("\nNo alignment hits satisfied the specified filter criteria.")


if __name__ == "__main__":
    main()
