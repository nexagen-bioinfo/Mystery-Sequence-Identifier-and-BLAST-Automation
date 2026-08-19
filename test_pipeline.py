"""
Unit and Integration Validation Suite for Mystery Sequence Identifier Pipeline.
Validates sequence parsing, sequence type detection, organism title parsing, and report writing.
"""

import os
import unittest
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

from sequence_io import parse_fasta, detect_sequence_type, extract_organism_from_title
from report_writer import export_reports


class TestSequenceIO(unittest.TestCase):

    def test_dna_sequence_detection(self):
        rec = SeqRecord(Seq("ATGCGATCGATCGATCGATC"), id="test_dna")
        meta = detect_sequence_type(rec)
        self.assertEqual(meta["sequence_type"], "DNA")
        self.assertEqual(meta["blast_program"], "blastn")
        self.assertEqual(meta["database"], "nt")

    def test_rna_sequence_detection(self):
        rec = SeqRecord(Seq("AUGCGAUCGAUCGAUCGAUC"), id="test_rna")
        meta = detect_sequence_type(rec)
        self.assertEqual(meta["sequence_type"], "RNA")
        self.assertEqual(meta["blast_program"], "blastn")
        self.assertEqual(meta["database"], "nt")

    def test_protein_sequence_detection(self):
        rec = SeqRecord(Seq("MKWVTFISLLFLFSSAYSRGVFRRDTHKSEIAHRFKDLGEEHFKGLVLIAFSQYLQQCPFDEHVKLVNELTEFAKTCVADESHAGCEKSLHTLFGDELCKVASLRETYGDMADCCEKQEPERNECFLSHKDDSPDLPKLKPDPNTLCDEFKADEKKFWGKYLYEIARRHPYFYAPELLYYANKYNGVFQECCQAEDKGACLLPKIETMREKVLTSSARQRLRCASIQKFGERALKAWSVARLSQKFPKAEFVEVTKLVTDLTKVHKECCHGDLLECADDRADLAKYICDNQDTISSKLKECCDKPLLEKSHCIAEVEKDAIPENLPPLTADFAEDKDVCKNYQEAKDAFLGSFLYEYSRRHPEYAVSVLLRLAKEYEATLEECCAKDDPHACYSTVFDKLKHLVDEPQNLIKQNCDQFEKLGEYGFQNALIVRYTRKVPQVSTPTLVEVSRSLGKVGTRCCTKPESERMPCTEDYLSLILNRLCVLHEKTPVSEKVTKCCTESLVNRRPCFSALTPDETYVPKAFDEKLFTFHADICTLPDTEKQIKKQTALVELLKHKPKATEEQLKTVMENFVAFVDKCCAADDKEACFAVEGPKLVVSTQTALA"), id="test_protein")
        meta = detect_sequence_type(rec)
        self.assertEqual(meta["sequence_type"], "PROTEIN")
        self.assertEqual(meta["blast_program"], "blastp")
        self.assertEqual(meta["database"], "nr")

    def test_organism_extraction(self):
        title_with_bracket = "gi|123456|ref|NC_012920.1| Homo sapiens mitochondrion, complete genome [Homo sapiens]"
        self.assertEqual(extract_organism_from_title(title_with_bracket), "Homo sapiens")

        title_with_keyword = "Human adenovirus 2 complete genome"
        self.assertEqual(extract_organism_from_title(title_with_keyword), "Human adenovirus 2")

    def test_parse_fasta_benchmark_files(self):
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        for filename in ["NC_012920.fasta", "AC_000021.fasta", "9GE4.fasta", "PZ716984.fasta"]:
            filepath = os.path.join(data_dir, filename)
            if os.path.exists(filepath):
                rec = parse_fasta(filepath)
                meta = detect_sequence_type(rec)
                self.assertIsNotNone(rec.id)
                self.assertIn(meta["sequence_type"], ["DNA", "RNA", "PROTEIN"])

    def test_export_reports_mock(self):
        sample_results = [{
            "Accession ID": "NC_012920.1",
            "Organism Name": "Homo sapiens",
            "Definition": "Homo sapiens mitochondrion, complete genome",
            "Alignment Length": 16569,
            "Bit Score": 30500.0,
            "E-value": 0.0,
            "Identity (%)": 100.0
        }]
        out = export_reports(sample_results, output_dir="cache/test_reports", base_name="test_out")
        self.assertTrue(os.path.exists(out["csv"]))
        if out["excel"]:
            self.assertTrue(os.path.exists(out["excel"]))


if __name__ == "__main__":
    unittest.main()
