"""
tests/test_blast_engine.py
===========================
blast_engine.py modulu üçün unit və keçid testləri
"""

import os
import unittest
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from blast_engine import run_blast


class TestBlastEngine(unittest.TestCase):

    def setUp(self):
        self.cache_dir = os.path.join(os.path.dirname(__file__), "test_cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        self.seq_rec = SeqRecord(
            Seq("ATGACAGACCAACAGAAAGCTCTGGTCGACCAGTGGAAGA"),
            id="test_seq_engine",
            description="Test sequence for BLAST engine"
        )

    def tearDown(self):
        # Test qovluğunu təmizləyirik
        if os.path.exists(self.cache_dir):
            for f in os.listdir(self.cache_dir):
                os.remove(os.path.join(self.cache_dir, f))
            os.rmdir(self.cache_dir)

    def test_cache_creation_and_reading(self):
        # 1. Müvəqqəti simulyasiya edilmiş XML keş faylı yaradırıq
        fake_xml_filename = "blast_test_seq_engine.xml"
        fake_xml_path = os.path.join(self.cache_dir, fake_xml_filename)
        
        with open(fake_xml_path, "w", encoding="utf-8") as f:
            f.write("<BlastOutput><Header>Simulated XML</Header></BlastOutput>")

        # 2. force_reblast=False olduqda run_blast həmin faylı birbaşa qaytarmalıdır (NCBI-a müraciət etmədən)
        result_path = run_blast(self.seq_rec, cache_dir=self.cache_dir, force_reblast=False)
        self.assertEqual(os.path.abspath(fake_xml_path), result_path)
        
        with open(result_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("<BlastOutput>", content)


if __name__ == "__main__":
    unittest.main()
