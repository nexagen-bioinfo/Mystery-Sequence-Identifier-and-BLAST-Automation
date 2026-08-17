"""
BLAST Engine Module.
Executes both Local BLAST+ CLI and Remote NCBI BLAST queries with XML caching and retry logic.
"""

import os
import time
import shutil
import tempfile
import subprocess
from typing import Optional, Dict, Any
from Bio.Blast import NCBIWWW
from Bio.SeqRecord import SeqRecord
from sequence_io import detect_sequence_type


def check_local_blast_available(program: str) -> bool:
    """
    Checks if a local BLAST+ executable (e.g. 'blastn', 'blastp') is in the system PATH.
    """
    return shutil.which(program) is not None


def run_local_blast(
    seq_record: SeqRecord,
    db: str,
    output_xml_path: str,
    program: str = "blastn",
    num_threads: int = 4,
    hitlist_size: int = 10,
    expect: float = 1e-5
) -> str:
    """
    Executes a local BLAST+ CLI search via subprocess and writes XML (outfmt 5) output.

    :param seq_record: SeqRecord to query
    :param db: Path or name of the formatted BLAST database
    :param output_xml_path: Path where XML output should be saved
    :param program: BLAST executable ('blastn' or 'blastp')
    :param num_threads: Number of CPU threads
    :param hitlist_size: Maximum target sequences to return
    :param expect: E-value cutoff
    :return: Absolute path to the output XML file
    """
    if not check_local_blast_available(program):
        raise FileNotFoundError(
            f"Local BLAST executable '{program}' not found in system PATH. "
            "Please install NCBI BLAST+ or use remote mode."
        )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".fasta", delete=False, encoding="utf-8") as temp_fasta:
        temp_fasta.write(seq_record.format("fasta"))
        temp_fasta_path = temp_fasta.name

    try:
        cmd = [
            program,
            "-query", temp_fasta_path,
            "-db", db,
            "-out", output_xml_path,
            "-outfmt", "5",  # XML format compatible with NCBIXML parser
            "-max_target_seqs", str(hitlist_size),
            "-evalue", str(expect),
            "-num_threads", str(num_threads)
        ]

        print(f"[LOCAL BLAST+] Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(f"[LOCAL BLAST+] Local execution completed successfully.")
        return os.path.abspath(output_xml_path)

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        raise RuntimeError(f"Local BLAST+ execution failed: {error_msg}")
    finally:
        if os.path.exists(temp_fasta_path):
            os.remove(temp_fasta_path)


def run_remote_blast(
    seq_record: SeqRecord,
    output_xml_path: str,
    program: str,
    database: str,
    max_retries: int = 3,
    retry_delay: int = 10,
    hitlist_size: int = 10,
    expect: float = 1e-5
) -> str:
    """
    Executes a remote NCBI BLAST query via NCBIWWW.qblast and saves XML output.
    """
    print(f"[NCBI BLAST] Submitting remote {program.upper()} query for '{seq_record.id}'...")
    print(f"Program: {program} | Database: {database}")

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

    with open(output_xml_path, "w", encoding="utf-8") as xml_file:
        xml_file.write(raw_xml_data)

    return os.path.abspath(output_xml_path)


def run_blast(
    seq_record: SeqRecord,
    mode: str = "auto",
    db: Optional[str] = None,
    num_threads: int = 4,
    cache_dir: str = "cache",
    force_reblast: bool = False,
    max_retries: int = 3,
    retry_delay: int = 10,
    hitlist_size: int = 10,
    expect: float = 1e-5
) -> str:
    """
    Executes a BLAST query (Local or Remote) and caches the raw XML output.

    :param seq_record: SeqRecord object containing sequence data
    :param mode: Execution mode ('auto', 'local', 'remote')
    :param db: Database name or path (optional for auto/remote; uses 'nt' or 'nr' by default)
    :param num_threads: Number of threads for local execution
    :param cache_dir: Directory where raw XML files are cached
    :param force_reblast: Force a new query even if cache exists
    :param max_retries: Maximum number of retry attempts on network error (remote mode)
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
    remote_db = seq_info["database"]

    target_db = db if db else remote_db

    # Mode resolution
    if mode == "local":
        run_local_blast(
            seq_record=seq_record,
            db=target_db,
            output_xml_path=xml_filepath,
            program=program,
            num_threads=num_threads,
            hitlist_size=hitlist_size,
            expect=expect
        )
    elif mode == "remote":
        run_remote_blast(
            seq_record=seq_record,
            output_xml_path=xml_filepath,
            program=program,
            database=target_db,
            max_retries=max_retries,
            retry_delay=retry_delay,
            hitlist_size=hitlist_size,
            expect=expect
        )
    else:  # auto
        if check_local_blast_available(program) and db:
            print(f"[AUTO] Local BLAST+ detected and custom database specified. Using local mode.")
            run_local_blast(
                seq_record=seq_record,
                db=target_db,
                output_xml_path=xml_filepath,
                program=program,
                num_threads=num_threads,
                hitlist_size=hitlist_size,
                expect=expect
            )
        else:
            print(f"[AUTO] Using remote NCBI BLAST query.")
            run_remote_blast(
                seq_record=seq_record,
                output_xml_path=xml_filepath,
                program=program,
                database=remote_db,
                max_retries=max_retries,
                retry_delay=retry_delay,
                hitlist_size=hitlist_size,
                expect=expect
            )

    print(f"[SAVED] Raw XML cached to: {xml_filepath}")
    return xml_filepath
