"""
Unit Test Suite for Participant 3 (Suleiman) - XML Parser & Report Generator Module.
"""

import os
import shutil
import unittest
from report_writer import parse_blast_xml, export_reports, extract_organism_from_title


class TestReportWriter(unittest.TestCase):

    def setUp(self):
        self.test_reports_dir = "cache/test_reports_suleiman"
        os.makedirs(self.test_reports_dir, exist_ok=True)
        self.xml_filepath = "cache/blast_PZ716984_1.xml"

    def tearDown(self):
        if os.path.exists(self.test_reports_dir):
            shutil.rmtree(self.test_reports_dir)

    def test_extract_organism_from_title(self):
        title_with_bracket = "gi|123456|ref|NC_012920.1| Homo sapiens mitochondrion, complete genome [Homo sapiens]"
        self.assertEqual(extract_organism_from_title(title_with_bracket), "Homo sapiens")

        title_with_keyword = "Human adenovirus 2 complete genome"
        self.assertEqual(extract_organism_from_title(title_with_keyword), "Human adenovirus 2")

    def test_parse_blast_xml_if_cache_exists(self):
        if os.path.exists(self.xml_filepath):
            results = parse_blast_xml(self.xml_filepath, max_evalue=1e-5, min_identity=90.0, top_n=5)
            self.assertIsInstance(results, list)
            self.assertGreater(len(results), 0)
            first_hit = results[0]
            self.assertIn("Accession ID", first_hit)
            self.assertIn("Organism Name", first_hit)
            self.assertIn("Identity (%)", first_hit)
            self.assertGreaterEqual(first_hit["Identity (%)"], 90.0)
            self.assertLessEqual(first_hit["E-value"], 1e-5)

    def test_export_reports(self):
        sample_results = [{
            "Accession ID": "KT232088",
            "Organism Name": "Influenza C virus",
            "Definition": "Influenza C virus segment 7...",
            "Alignment Length": 900,
            "Bit Score": 1606.28,
            "E-value": 0.0,
            "Identity (%)": 99.56
        }]
        out = export_reports(sample_results, output_dir=self.test_reports_dir, base_name="test_report_suleiman")
        self.assertTrue(os.path.exists(out["csv"]))
        if out["excel"]:
            self.assertTrue(os.path.exists(out["excel"]))


if __name__ == "__main__":
    unittest.main()
