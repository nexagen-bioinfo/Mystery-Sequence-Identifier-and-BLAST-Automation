"""
Interactive Demo Script for Participant 1 (Adiba).
Demonstrates sequence parsing, automated type detection, and NCBI Entrez metadata queries.

Usage:
    python demo.py
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from sequence_io import parse_fasta, detect_sequence_type, fetch_ncbi_metadata

def main():
    print("==========================================================================")
    print("  Participant 1 (Adiba) -- Sequence Manager & Entrez Interface Demo")
    print("==========================================================================")

    # 1. DNT Ardıcıllığı Testi
    print("\n[1] DNA Sequence Detection Test:")
    dna_rec = SeqRecord(Seq("ATGCGATCGATCGATCGATCGATC"), id="mystery_dna_sample")
    dna_info = detect_sequence_type(dna_rec)
    print(f"  - Sequence ID:    {dna_info['sequence_id']}")
    print(f"  - Sequence Type:  {dna_info['sequence_type']}")
    print(f"  - BLAST Program:  {dna_info['blast_program']}")
    print(f"  - Target DB:      {dna_info['database']}")
    print(f"  - Length:         {dna_info['length']} bp")

    # 2. RNT Ardıcıllığı Testi
    print("\n[2] RNA Sequence Detection Test:")
    rna_rec = SeqRecord(Seq("AUGCGAUCGAUCGAUCGAUCGAUC"), id="mystery_rna_sample")
    rna_info = detect_sequence_type(rna_rec)
    print(f"  - Sequence ID:    {rna_info['sequence_id']}")
    print(f"  - Sequence Type:  {rna_info['sequence_type']}")
    print(f"  - BLAST Program:  {rna_info['blast_program']}")
    print(f"  - Target DB:      {rna_info['database']}")
    print(f"  - Length:         {rna_info['length']} bp")

    # 3. Zülal (Protein) Ardıcıllığı Testi
    print("\n[3] Protein Sequence Detection Test:")
    prot_rec = SeqRecord(Seq("MKTLLLTLLLLLLLLWVEAKL"), id="mystery_protein_sample")
    prot_info = detect_sequence_type(prot_rec)
    print(f"  - Sequence ID:    {prot_info['sequence_id']}")
    print(f"  - Sequence Type:  {prot_info['sequence_type']}")
    print(f"  - BLAST Program:  {prot_info['blast_program']}")
    print(f"  - Target DB:      {prot_info['database']}")
    print(f"  - Length:         {prot_info['length']} aa")

    # 4. Fayldan FASTA Oxuma Testi
    print("\n[4] FASTA File Parsing Test ('data/PZ716984.fasta'):")
    try:
        file_rec = parse_fasta("data/PZ716984.fasta")
        file_info = detect_sequence_type(file_rec)
        print(f"  - Parsed ID:      {file_rec.id}")
        print(f"  - Sequence Type:  {file_info['sequence_type']}")
        print(f"  - Sequence Len:   {len(file_rec.seq)} bp")
    except Exception as e:
        print(f"  - Error reading file: {e}")

    # 5. NCBI Entrez Metadata Sorğusu Testi
    print("\n[5] NCBI Entrez Metadata Query Test ('NC_012920'):")
    print("  - Connecting to NCBI Entrez server...")
    try:
        meta = fetch_ncbi_metadata("NC_012920")
        print(f"  - Accession ID:   {meta['accession_id']}")
        print(f"  - Organism Name:  {meta['organism']}")
        print(f"  - Gene Def:       {meta['definition']}")
    except Exception as e:
        print(f"  - Entrez query error: {e}")

    print("\n==========================================================================")
    print("  All Participant 1 tests executed successfully!")
    print("==========================================================================")

if __name__ == "__main__":
    main()
