"""
Unit and Integration Validation Suite for Mystery Sequence Identifier Pipeline.
Validates sequence parsing, sequence type detection, organism title parsing, and report writing.
"""

import os
import unittest
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

from unittest.mock import patch, MagicMock
import io
import shutil

from sequence_io import parse_fasta, detect_sequence_type, extract_organism_from_title
from blast_engine import run_blast
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


class TestBlastEngine(unittest.TestCase):

    def setUp(self):
        self.test_cache_dir = "cache/test_blast_cache"
        os.makedirs(self.test_cache_dir, exist_ok=True)
        self.seq_record = SeqRecord(Seq("ATGCGATCGATCGATCGATC"), id="mock_seq_001")

    def tearDown(self):
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir)

    def test_blast_cached_result_retrieval(self):
        xml_filepath = os.path.join(self.test_cache_dir, "blast_mock_seq_001.xml")
        with open(xml_filepath, "w", encoding="utf-8") as f:
            f.write("<BlastOutput>Cached Mock Result</BlastOutput>")

        res_path = run_blast(self.seq_record, cache_dir=self.test_cache_dir, force_reblast=False)
        self.assertEqual(os.path.abspath(xml_filepath), res_path)

    @patch("Bio.Blast.NCBIWWW.qblast")
    def test_blast_mock_remote_query(self, mock_qblast):
        mock_handle = io.StringIO("<BlastOutput>Valid Mock Remote Result</BlastOutput>")
        mock_qblast.return_value = mock_handle

        res_path = run_blast(self.seq_record, cache_dir=self.test_cache_dir, force_reblast=True)
        self.assertTrue(os.path.exists(res_path))
        mock_qblast.assert_called_once()
        with open(res_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("<BlastOutput>", content)

    @patch("Bio.Blast.NCBIWWW.qblast")
    def test_blast_retry_mechanism_on_failure(self, mock_qblast):
        mock_handle = io.StringIO("<BlastOutput>Recovered Result</BlastOutput>")
        mock_qblast.side_effect = [Exception("Network Timeout"), mock_handle]

        res_path = run_blast(
            self.seq_record,
            cache_dir=self.test_cache_dir,
            force_reblast=True,
            max_retries=3,
            retry_delay=0
        )
        self.assertTrue(os.path.exists(res_path))
        self.assertEqual(mock_qblast.call_count, 2)


if __name__ == "__main__":
    unittest.main()

