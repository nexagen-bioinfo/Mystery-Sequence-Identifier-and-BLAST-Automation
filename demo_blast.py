"""
Interactive Demo Script for Participant 2 (Mehriban) - Remote BLAST Engine Module.
Demonstrates running remote NCBI BLAST queries and caching raw XML output.
"""

from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from blast_engine import run_blast, detect_sequence_type


def main():
    print("==========================================================================")
    print("Participant 2 (Mehriban) - Remote BLAST Engine Demo")
    print("==========================================================================")

    # Sample DNA Sequence (900 bp)
    sample_seq = (
        "AAATGTCCGACAAAACAGTCAAATCAACAAATTTAATGGCATTTGTAGCCACAAAAATGTTAGAGAGACAAGAAGATTTAGACACATGCACTGAAATGCAAGTAGAAAAAATGAAAACGTCAACAAAAGCTAGGCTGAGAACAGAATCTTCTTTTGCACCTAGAACGTGGGAAGATGCAATAAAAGATGGTGAGCTTCTATTCAACGGGACGATTCTGCAAGCAGAGTCTCCTACACTGACGCCAGCGTCCGTAGAAACGAAGGGAAAGAAACTTCCTATTGATTTTGCTCCAAGCAACATAGCACCAATTGGGCAAAATCCAATCTATTTGTCACCATGTATTCCTAACTTTGATGGAAACGTCTGGGAAGCAACGATGTATCATCATCGTGGAGCAACTTTAACAAAGACAATGAATTGCAACTGTTTTCAAAGAACAATTTGGTGCCATCCAAATCCTTCACGTATGAGATTGAGCTATGCATTTGTTTTGTATTGCAGAAATACTAAGAAGATCTGTGGATACCTCATCGCTAGACAGGTGGCCGGAATTGAAACAGGAATTAGAAAATGTTTCAGATGCATTAAAAGCGGATTCGTTATGGCTACCGATGAAATCTCTCTCACTATACTCCGAAGTATCAAATCAGGAGCTCAGCTCGATCCCTATTGGGGAAATGAAACACCAGATATTGACAAGACTGAAGCTTATATGCTCTCGCTTAGAGAAGCTGGACCATAACCTGAGCAAAGCAGTCTTGGGAATCCAAAATTCTGAAGATCTTATTTTGATTATACATAACAGAGATGTTTGTAAAAACATTATATTAATGATAAAATCTTTGTGCAATTCACTTATATAATTGTTTTAAGTTATTATTCCAAAGTTAAAAAACCCC"
    )
    rec = SeqRecord(Seq(sample_seq), id="demo_seq_PZ716984")

    # Step 1: Detect sequence type
    info = detect_sequence_type(rec)
    print(f"\n[1] Sequence ID: {info['sequence_id']}")
    print(f"    Detected Type: {info['sequence_type']}")
    print(f"    BLAST Program: {info['blast_program']} | Database: {info['database']}")

    # Step 2: Run remote BLAST query (or read from cache)
    print("\n[2] Executing run_blast()...")
    xml_path = run_blast(rec, cache_dir="cache", force_reblast=False)

    print(f"\n[SUCCESS] Raw BLAST XML stored at: {xml_path}")
    print("==========================================================================")


if __name__ == "__main__":
    main()
