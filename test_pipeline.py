"""
Automated Test Suite for Mystery Sequence Identifier & BLAST Automation Pipeline.
Tests sequence detection, title organism extraction, BLAST XML parsing, filtering, and report exports.
"""

import os
import tempfile
import unittest
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from sequence_io import detect_sequence_type, extract_organism_from_title
from report_writer import parse_blast_xml, export_reports
from blast_engine import check_local_blast_available


SAMPLE_BLAST_XML = """<?xml version="1.0"?>
<!DOCTYPE BlastOutput PUBLIC "-//NCBI//NCBI BlastOutput/EN" "NCBI_BlastOutput.dtd">
<BlastOutput>
  <BlastOutput_program>blastn</BlastOutput_program>
  <BlastOutput_version>BLASTN 2.12.0+</BlastOutput_version>
  <BlastOutput_reference>Stephen F. Altschul et al. 1990</BlastOutput_reference>
  <BlastOutput_db>nt</BlastOutput_db>
  <BlastOutput_query-ID>Query_1</BlastOutput_query-ID>
  <BlastOutput_query-def>Test Sequence</BlastOutput_query-def>
  <BlastOutput_query-len>100</BlastOutput_query-len>
  <BlastOutput_iterations>
    <Iteration>
      <Iteration_iter-num>1</Iteration_iter-num>
      <Iteration_query-ID>Query_1</Iteration_query-ID>
      <Iteration_query-def>Test Sequence</Iteration_query-def>
      <Iteration_query-len>100</Iteration_query-len>
      <Iteration_hits>
        <Hit>
          <Hit_num>1</Hit_num>
          <Hit_id>gi|123456|ref|NC_012920.1|</Hit_id>
          <Hit_def>Homo sapiens mitochondrion, complete genome [Homo sapiens]</Hit_def>
          <Hit_accession>NC_012920</Hit_accession>
          <Hit_len>16569</Hit_len>
          <Hit_hsps>
            <Hsp>
              <Hsp_num>1</Hsp_num>
              <Hsp_bit-score>185.2</Hsp_bit-score>
              <Hsp_score>100</Hsp_score>
              <Hsp_evalue>1.2e-45</Hsp_evalue>
              <Hsp_query-from>1</Hsp_query-from>
              <Hsp_query-to>100</Hsp_query-to>
              <Hsp_hit-from>1</Hsp_hit-from>
              <Hsp_hit-to>100</Hsp_hit-to>
              <Hsp_identity>98</Hsp_identity>
              <Hsp_positive>98</Hsp_positive>
              <Hsp_gaps>0</Hsp_gaps>
              <Hsp_align-len>100</Hsp_align-len>
              <Hsp_qseq>GATCACAGGTCTATCACCCTATTAACCACTCACGGGAGCTCTCCATGCATTTGGTATTTTCGTCTGGGGGGTGTGCACGCGATAGCATTGCGAGACGCTG</Hsp_qseq>
              <Hsp_hseq>GATCACAGGTCTATCACCCTATTAACCACTCACGGGAGCTCTCCATGCATTTGGTATTTTCGTCTGGGGGGTGTGCACGCGATAGCATTGCGAGACGCTG</Hsp_hseq>
              <Hsp_midline>||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||</Hsp_midline>
            </Hsp>
          </Hit_hsps>
        </Hit>
        <Hit>
          <Hit_num>2</Hit_num>
          <Hit_id>gi|789012|ref|XM_001.1|</Hit_id>
          <Hit_def>Mus musculus predicted sequence [Mus musculus]</Hit_def>
          <Hit_accession>XM_001</Hit_accession>
          <Hit_len>5000</Hit_len>
          <Hit_hsps>
            <Hsp>
              <Hsp_num>1</Hsp_num>
              <Hsp_bit-score>60.0</Hsp_bit-score>
              <Hsp_score>32</Hsp_score>
              <Hsp_evalue>0.05</Hsp_evalue>
              <Hsp_query-from>1</Hsp_query-from>
              <Hsp_query-to>50</Hsp_query-to>
              <Hsp_hit-from>10</Hsp_hit-from>
              <Hsp_hit-to>60</Hsp_hit-to>
              <Hsp_identity>35</Hsp_identity>
              <Hsp_positive>35</Hsp_positive>
              <Hsp_gaps>0</Hsp_gaps>
              <Hsp_align-len>50</Hsp_align-len>
              <Hsp_qseq>GATCACAGGTCTATCACCCTATTAACCACTCACGGGAGCTCTCCATGCAT</Hsp_qseq>
              <Hsp_hseq>GATCACAGGTCTATCACCCTATTAACCACTCACGGGAGCTCTCCATGCAT</Hsp_hseq>
              <Hsp_midline>||||||||||||||||||||||||||||||||||||||||||||||||||</Hsp_midline>
            </Hsp>
          </Hit_hsps>
        </Hit>
      </Iteration_hits>
    </Iteration>
  </BlastOutput_iterations>
</BlastOutput>
"""


class TestPipeline(unittest.TestCase):

    def test_sequence_type_detection(self):
        # 1. DNA Sequence
        dna_rec = SeqRecord(Seq("ATGCGATCGATCGATCGA"), id="seq_dna")
        dna_res = detect_sequence_type(dna_rec)
        self.assertEqual(dna_res["sequence_type"], "DNA")
        self.assertEqual(dna_res["blast_program"], "blastn")
        self.assertEqual(dna_res["database"], "nt")

        # 2. RNA Sequence
        rna_rec = SeqRecord(Seq("AUGCGAUCGAUCGAUCGA"), id="seq_rna")
        rna_res = detect_sequence_type(rna_rec)
        self.assertEqual(rna_res["sequence_type"], "RNA")
        self.assertEqual(rna_res["blast_program"], "blastn")
        self.assertEqual(rna_res["database"], "nt")

        # 3. Protein Sequence
        prot_rec = SeqRecord(Seq("MKTLLLTLLLLLLLLWVEAKL"), id="seq_prot")
        prot_res = detect_sequence_type(prot_rec)
        self.assertEqual(prot_res["sequence_type"], "Protein")
        self.assertEqual(prot_res["blast_program"], "blastp")
        self.assertEqual(prot_res["database"], "nr")

    def test_organism_extraction(self):
        # Case 1: Bracketed organism
        title1 = "gi|123|ref|NC_012920.1| Homo sapiens mitochondrion [Homo sapiens]"
        self.assertEqual(extract_organism_from_title(title1), "Homo sapiens")

        # Case 2: PREDICTED syntax
        title2 = "PREDICTED: Mus musculus hemoglobin subunit beta (Hbb-b1)"
        self.assertEqual(extract_organism_from_title(title2), "Mus musculus")

        # Case 3: Fallback plain title
        title3 = "Synthetic construct cloning vector"
        self.assertIn("Synthetic construct", extract_organism_from_title(title3))

    def test_parse_blast_xml_filtering(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False, encoding="utf-8") as tf:
            tf.write(SAMPLE_BLAST_XML)
            xml_path = tf.name

        try:
            # Test default filtering (evalue <= 1e-5, identity >= 90.0) -> only Hit 1 should match
            hits = parse_blast_xml(xml_path, max_evalue=1e-5, min_identity=90.0, top_n=5, fetch_organism=False)
            self.assertEqual(len(hits), 1)
            self.assertEqual(hits[0]["Accession ID"], "NC_012920")
            self.assertEqual(hits[0]["Organism Name"], "Homo sapiens")
            self.assertEqual(hits[0]["Identity (%)"], 98.0)
            self.assertAlmostEqual(hits[0]["E-value"], 1.2e-45)

            # Test relaxed filtering (evalue <= 1.0, identity >= 50.0) -> both hits match
            relaxed_hits = parse_blast_xml(xml_path, max_evalue=1.0, min_identity=50.0, top_n=5, fetch_organism=False)
            self.assertEqual(len(relaxed_hits), 2)
            self.assertEqual(relaxed_hits[0]["Accession ID"], "NC_012920")
            self.assertEqual(relaxed_hits[1]["Accession ID"], "XM_001")
        finally:
            if os.path.exists(xml_path):
                os.remove(xml_path)

    def test_export_reports(self):
        sample_results = [{
            "Accession ID": "NC_012920",
            "Organism Name": "Homo sapiens",
            "Definition": "Homo sapiens mitochondrion, complete genome",
            "Alignment Length": 100,
            "Bit Score": 185.2,
            "E-value": 1.2e-45,
            "Identity (%)": 98.0
        }]

        with tempfile.TemporaryDirectory() as temp_dir:
            reports = export_reports(sample_results, output_dir=temp_dir, base_name="test_report")
            self.assertTrue(os.path.exists(reports["csv"]))
            with open(reports["csv"], "r", encoding="utf-8-sig") as f:
                content = f.read()
                self.assertIn("Accession ID,Organism Name", content)
                self.assertIn("NC_012920,Homo sapiens", content)

    def test_local_blast_checker(self):
        # Should return boolean without throwing exception
        res = check_local_blast_available("blastn")
        self.assertIsInstance(res, bool)


if __name__ == "__main__":
    unittest.main()
