"""
Unit Test Suite for Participant 2 (Mehriban) - Remote BLAST Engine Module.
"""

import os
import io
import shutil
import unittest
from unittest.mock import patch
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

from blast_engine import run_blast, detect_sequence_type


class TestBlastEngine(unittest.TestCase):

    def setUp(self):
        self.test_cache_dir = "cache/test_blast_cache"
        os.makedirs(self.test_cache_dir, exist_ok=True)
        self.seq_record = SeqRecord(Seq("ATGCGATCGATCGATCGATC"), id="mock_seq_001")

    def tearDown(self):
        if os.path.exists(self.test_cache_dir):
            shutil.rmtree(self.test_cache_dir)

    def test_sequence_type_detection(self):
        dna_rec = SeqRecord(Seq("ATGCGATCGATC"), id="dna_test")
        meta = detect_sequence_type(dna_rec)
        self.assertEqual(meta["sequence_type"], "DNA")
        self.assertEqual(meta["blast_program"], "blastn")
        self.assertEqual(meta["database"], "nt")

        protein_rec = SeqRecord(Seq("MKWVTFISLLFLFSSAYSRGVFRRDTHKSEIAHRFKDLGEEHFKGLVLIAFSQYLQQCPFDEHVKLVNELTEFAKTCVA"), id="prot_test")
        meta_prot = detect_sequence_type(protein_rec)
        self.assertEqual(meta_prot["sequence_type"], "PROTEIN")
        self.assertEqual(meta_prot["blast_program"], "blastp")
        self.assertEqual(meta_prot["database"], "nr")

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
