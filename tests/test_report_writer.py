"""
tests/test_report_writer.py
============================
report_writer.py modulu üçün unit testlər
"""

import os
import unittest
from report_writer import parse_blast_xml, export_reports


class TestReportWriter(unittest.TestCase):

    def setUp(self):
        self.output_dir = os.path.join(os.path.dirname(__file__), "test_reports")
        self.xml_file = os.path.join(os.path.dirname(__file__), "sample_blast.xml")
        
        # Test üçün nümunə simulyasiya olunmuş BLAST XML yaratmaq
        xml_content = """<?xml version="1.0"?>
<!DOCTYPE BlastOutput PUBLIC "-//NCBI//NCBI BlastOutput/EN" "http://www.ncbi.nlm.nih.gov/dtd/NCBI_BlastOutput.dtd">
<BlastOutput>
  <BlastOutput_program>blastn</BlastOutput_program>
  <BlastOutput_version>BLASTN 2.15.0+</BlastOutput_version>
  <BlastOutput_reference>Reference</BlastOutput_reference>
  <BlastOutput_db>nt</BlastOutput_db>
  <BlastOutput_query-ID>Query_1</BlastOutput_query-ID>
  <BlastOutput_query-def>test_seq</BlastOutput_query-def>
  <BlastOutput_query-len>300</BlastOutput_query-len>
  <BlastOutput_param>
    <Parameters>
      <Parameters_expect>10</Parameters_expect>
      <Parameters_sc-match>1</Parameters_sc-match>
      <Parameters_sc-mismatch>-2</Parameters_sc-mismatch>
      <Parameters_gap-open>0</Parameters_gap-open>
      <Parameters_gap-extend>0</Parameters_gap-extend>
      <Parameters_filter>L;m;</Parameters_filter>
    </Parameters>
  </BlastOutput_param>
  <BlastOutput_iterations>
    <Iteration>
      <Iteration_iter-num>1</Iteration_iter-num>
      <Iteration_hits>
        <Hit>
          <Hit_num>1</Hit_num>
          <Hit_id>gi|12345|gb|NM_001301717.2|</Hit_id>
          <Hit_def>Homo sapiens myoglobin (MB), mRNA [Homo sapiens]</Hit_def>
          <Hit_accession>NM_001301717.2</Hit_accession>
          <Hit_len>1100</Hit_len>
          <Hit_hsps>
            <Hsp>
              <Hsp_num>1</Hsp_num>
              <Hsp_bit-score>500.0</Hsp_bit-score>
              <Hsp_score>270</Hsp_score>
              <Hsp_evalue>0.0</Hsp_evalue>
              <Hsp_align-len>300</Hsp_align-len>
              <Hsp_identity>295</Hsp_identity>
              <Hsp_gaps>0</Hsp_gaps>
            </Hsp>
          </Hit_hsps>
        </Hit>
      </Iteration_hits>
    </Iteration>
  </BlastOutput_iterations>
</BlastOutput>"""
        with open(self.xml_file, "w", encoding="utf-8") as f:
            f.write(xml_content)

    def tearDown(self):
        if os.path.exists(self.xml_file):
            os.remove(self.xml_file)
        if os.path.exists(self.output_dir):
            for f in os.listdir(self.output_dir):
                os.remove(os.path.join(self.output_dir, f))
            os.rmdir(self.output_dir)

    def test_parse_blast_xml(self):
        hits = parse_blast_xml(self.xml_file, fetch_organism=False)
        self.assertEqual(len(hits), 1)
        hit = hits[0]
        self.assertEqual(hit["Accession ID"], "NM_001301717.2")
        self.assertEqual(hit["Organism Name"], "Homo sapiens")
        self.assertAlmostEqual(hit["Identity (%)"], 98.33, places=1)
        self.assertEqual(hit["E-value"], 0.0)

    def test_export_reports(self):
        hits = parse_blast_xml(self.xml_file, fetch_organism=False)
        paths = export_reports(hits, output_dir=self.output_dir, base_name="test_report")
        
        self.assertTrue(os.path.exists(paths["csv"]))
        self.assertTrue(os.path.exists(paths["excel"]))
        self.assertGreater(os.path.getsize(paths["csv"]), 0)
        self.assertGreater(os.path.getsize(paths["excel"]), 0)


if __name__ == "__main__":
    unittest.main()
