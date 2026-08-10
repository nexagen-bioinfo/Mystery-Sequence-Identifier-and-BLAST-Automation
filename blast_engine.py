"""
Remote BLAST Engine Module.
Executes remote NCBI BLAST queries and manages XML caching and retry logic.
"""

import os
import time
from typing import Optional, Dict, Any
from Bio.Blast import NCBIWWW
from Bio.SeqRecord import SeqRecord
from sequence_io import detect_sequence_type


def run_blast(
    seq_record: SeqRecord,
    cache_dir: str = "cache",
    force_reblast: bool = False,
    max_retries: int = 3,
    retry_delay: int = 10,
    hitlist_size: int = 10,
    expect: float = 1e-5
) -> str:
    """
    Executes a remote BLAST query for a given SeqRecord and caches the raw XML output.

    :param seq_record: SeqRecord object containing sequence data
    :param cache_dir: Directory where raw XML files are cached
    :param force_reblast: Force a new query even if cache exists
    :param max_retries: Maximum number of retry attempts on network error
    :param retry_delay: Delay in seconds between retries
    :param hitlist_size: Number of hits to retrieve
    :param expect: E-value threshold
    :return: Absolute path to the cached XML file
    """
    os.makedirs(cache_dir, exist_ok=True)

    safe_seq_id = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in str(seq_record.id))
    xml_filename = f"blast_{safe_seq_id}.xml"
    xml_filepath = os.path.abspath(os.path.join(cache_dir, xml_filename))

    if os.path.exists(xml_filepath) and not force_reblast:
        print(f"[CACHE] Reading cached BLAST result for '{seq_record.id}': {xml_filepath}")
        return xml_filepath

    seq_info = detect_sequence_type(seq_record)
    program = seq_info["blast_program"]
    database = seq_info["database"]

    print(f"[NCBI BLAST] Submitting {program.upper()} query for '{seq_record.id}'...")
    print(f"Program: {program} | Database: {database} | Length: {seq_info['length']} bp/aa")

    fasta_data = seq_record.format("fasta")

    attempt = 0
    raw_xml_data = None

    while attempt < max_retries:
        attempt += 1
        try:
            print(f"Contacting NCBI server (Attempt {attempt}/{max_retries})...")
            result_handle = NCBIWWW.qblast(
                program=program,
                database=database,
                sequence=fasta_data,
                hitlist_size=hitlist_size,
                expect=expect
            )
            raw_xml_data = result_handle.read()
            result_handle.close()

            if raw_xml_data and "<BlastOutput>" in raw_xml_data:
                print("Valid XML response received from NCBI.")
                break
            else:
                print("Warning: Incomplete XML response received. Retrying...")

        except Exception as e:
            print(f"Network error (Attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                print(f"Waiting {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)

    if not raw_xml_data:
        raise RuntimeError(f"NCBI BLAST query failed for '{seq_record.id}' after {max_retries} attempts.")

    with open(xml_filepath, "w", encoding="utf-8") as xml_file:
        xml_file.write(raw_xml_data)

    print(f"[SAVED] Raw XML cached to: {xml_filepath}")
    return xml_filepath
