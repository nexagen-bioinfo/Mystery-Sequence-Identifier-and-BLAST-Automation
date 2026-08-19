"""
Unit Tests for Module 1: Sequence Manager & Entrez Interface (Participant 1 - Adiba)
Tests FASTA parsing (file and string), sequence type classification, title organism extraction, and Entrez metadata resolution.
"""

import os
import tempfile
import unittest
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from sequence_io import (
    parse_fasta,
    detect_sequence_type,
    extract_organism_from_title,
    fetch_ncbi_metadata
)


class TestSequenceIO(unittest.TestCase):

    def test_parse_fasta_from_file(self):
        """Test parsing FASTA format from a file path."""
        fasta_content = ">mystery_seq_1 Test Description\nATGCGATCGATCGATCGATC\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".fasta", delete=False, encoding="utf-8") as tf:
            tf.write(fasta_content)
            temp_path = tf.name

        try:
            record = parse_fasta(temp_path)
            self.assertEqual(record.id, "mystery_seq_1")
            self.assertEqual(str(record.seq), "ATGCGATCGATCGATCGATC")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_parse_fasta_from_string(self):
        """Test parsing FASTA formatted raw string directly."""
        fasta_str = ">string_seq\nAUGCGAUCGAUCGAUCGAUC\n"
        record = parse_fasta(fasta_str)
        self.assertEqual(record.id, "string_seq")
        self.assertEqual(str(record.seq), "AUGCGAUCGAUCGAUCGAUC")

    def test_parse_fasta_invalid_inputs(self):
        """Test error handling on invalid or non-existent inputs."""
        with self.assertRaises(ValueError):
            parse_fasta("")

        with self.assertRaises(FileNotFoundError):
            parse_fasta("non_existent_file.fasta")

    def test_detect_dna_sequence(self):
        """Test DNA classification and BLAST parameter selection (blastn / nt)."""
        dna_rec = SeqRecord(Seq("ATGCGATCGATCGATCGATCGATC"), id="test_dna")
        res = detect_sequence_type(dna_rec)
        self.assertEqual(res["sequence_type"], "DNA")
        self.assertEqual(res["blast_program"], "blastn")
        self.assertEqual(res["database"], "nt")
        self.assertEqual(res["length"], 24)

    def test_detect_rna_sequence(self):
        """Test RNA classification and BLAST parameter selection (blastn / nt)."""
        rna_rec = SeqRecord(Seq("AUGCGAUCGAUCGAUCGAUCGAUC"), id="test_rna")
        res = detect_sequence_type(rna_rec)
        self.assertEqual(res["sequence_type"], "RNA")
        self.assertEqual(res["blast_program"], "blastn")
        self.assertEqual(res["database"], "nt")
        self.assertEqual(res["length"], 24)

    def test_detect_protein_sequence(self):
        """Test Protein classification and BLAST parameter selection (blastp / nr)."""
        prot_rec = SeqRecord(Seq("MKTLLLTLLLLLLLLWVEAKL"), id="test_prot")
        res = detect_sequence_type(prot_rec)
        self.assertEqual(res["sequence_type"], "PROTEIN")
        self.assertEqual(res["blast_program"], "blastp")
        self.assertEqual(res["database"], "nr")
        self.assertEqual(res["length"], 21)

    def test_extract_organism_from_title(self):
        """Test extracting organism names from NCBI header strings."""
        # Bracketed organism name
        title1 = "gi|123456|ref|NC_012920.1| Homo sapiens mitochondrion, complete genome [Homo sapiens]"
        self.assertEqual(extract_organism_from_title(title1), "Homo sapiens")

        # Organism followed by keyword
        title2 = "Mus musculus hemoglobin subunit beta gene, complete cds"
        self.assertEqual(extract_organism_from_title(title2), "Mus musculus")

        # Unknown title fallback
        self.assertEqual(extract_organism_from_title(""), "Unknown Organism")

    def test_fetch_ncbi_metadata_structure(self):
        """Test metadata dictionary structure returned by fetch_ncbi_metadata."""
        meta = fetch_ncbi_metadata("NON_EXISTENT_ACCESSION_99999")
        self.assertIn("accession_id", meta)
        self.assertIn("organism", meta)
        self.assertIn("definition", meta)


if __name__ == "__main__":
    unittest.main()
