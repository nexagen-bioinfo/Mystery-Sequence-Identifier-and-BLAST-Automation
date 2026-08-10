"""
tests/test_sequence_io.py
=========================
sequence_io.py modulu üçün unit testlər
"""

import os
import unittest
from sequence_io import parse_fasta, detect_sequence_type, fetch_ncbi_metadata


class TestSequenceIO(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.path.dirname(__file__)
        self.dna_file = os.path.join(self.test_dir, "sample_dna.fasta")
        self.protein_file = os.path.join(self.test_dir, "sample_protein.fasta")

        # Test FASTA fayllarını yaradırıq
        with open(self.dna_file, "w") as f:
            f.write(">seq_dna_test\nATGACAGACCAACAGAAAGCTCTGGTCGACCAGTGGAAGAAAGTCGAGGCC\n")

        with open(self.protein_file, "w") as f:
            f.write(">seq_protein_test\nGLSDGEWQLVLNVWGKVEADIPGHGQEVLIRLFKGHPETLEKFDKFKHLKS\n")

    def tearDown(self):
        # Test fayllarını təmizləyirik
        if os.path.exists(self.dna_file):
            os.remove(self.dna_file)
        if os.path.exists(self.protein_file):
            os.remove(self.protein_file)

    def test_parse_fasta_file(self):
        record = parse_fasta(self.dna_file)
        self.assertEqual(record.id, "seq_dna_test")
        self.assertTrue(str(record.seq).startswith("ATGAC"))

    def test_parse_fasta_string(self):
        raw_fasta = ">raw_seq\nATGCGATCG"
        record = parse_fasta(raw_fasta)
        self.assertEqual(record.id, "raw_seq")
        self.assertEqual(str(record.seq), "ATGCGATCG")

    def test_detect_dna(self):
        record = parse_fasta(self.dna_file)
        result = detect_sequence_type(record)
        self.assertEqual(result["sequence_type"], "DNA")
        self.assertEqual(result["blast_program"], "blastn")
        self.assertEqual(result["database"], "nt")

    def test_detect_protein(self):
        record = parse_fasta(self.protein_file)
        result = detect_sequence_type(record)
        self.assertEqual(result["sequence_type"], "PROTEIN")
        self.assertEqual(result["blast_program"], "blastp")
        self.assertEqual(result["database"], "nr")

    def test_fetch_ncbi_metadata(self):
        # Məşhur DNT accession ID: NM_001301717 (Homo sapiens)
        metadata = fetch_ncbi_metadata("NM_001301717.2")
        self.assertIn("organism", metadata)
        self.assertEqual(metadata["accession_id"], "NM_001301717.2")


if __name__ == "__main__":
    unittest.main()
