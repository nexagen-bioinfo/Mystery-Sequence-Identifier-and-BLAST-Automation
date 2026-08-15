"""
Sequence Manager and Entrez Interface Module.
Handles FASTA parsing, sequence type detection, and NCBI Entrez metadata retrieval.
"""

import os
import io
from typing import Dict, Union, Optional
from Bio import SeqIO, Entrez
from Bio.SeqRecord import SeqRecord


def parse_fasta(input_source: str) -> SeqRecord:
    """
    Parses a FASTA file path or FASTA formatted string.

    :param input_source: File path or raw FASTA string
    :return: SeqRecord object
    """
    if not input_source or not isinstance(input_source, str):
        raise ValueError("Input source must be a non-empty string.")

    if os.path.exists(input_source):
        try:
            with open(input_source, "r") as handle:
                records = list(SeqIO.parse(handle, "fasta"))
            if not records:
                raise ValueError(f"No FASTA sequence found in '{input_source}'.")
            return records[0]
        except Exception as e:
            raise ValueError(f"Error reading FASTA file: {e}")
    elif input_source.strip().startswith(">"):
        try:
            string_handle = io.StringIO(input_source.strip())
            records = list(SeqIO.parse(string_handle, "fasta"))
            if not records:
                raise ValueError("No valid FASTA sequence found in string input.")
            return records[0]
        except Exception as e:
            raise ValueError(f"Error parsing FASTA string: {e}")
    else:
        raise FileNotFoundError(f"File not found or invalid FASTA input: '{input_source}'")


def detect_sequence_type(seq_record: SeqRecord) -> Dict[str, Union[str, int]]:
    """
    Analyzes sequence composition to determine whether it is DNA, RNA, or Protein,
    and selects the corresponding BLAST program and database.

    :param seq_record: SeqRecord object
    :return: Dictionary containing sequence metadata and BLAST parameters
    """
    sequence_str = str(seq_record.seq).upper().strip()
    if not sequence_str:
        raise ValueError("Sequence is empty.")

    dna_rna_chars = set("ATCGUN")
    valid_nuc_count = sum(1 for char in sequence_str if char in dna_rna_chars)
    nuc_ratio = valid_nuc_count / len(sequence_str)

    if nuc_ratio >= 0.90:
        if "U" in sequence_str and "T" not in sequence_str:
            seq_type = "RNA"
        else:
            seq_type = "DNA"
        blast_program = "blastn"
        database = "nt"
    else:
        seq_type = "PROTEIN"
        blast_program = "blastp"
        database = "nr"

    return {
        "sequence_id": seq_record.id,
        "sequence_type": seq_type,
        "blast_program": blast_program,
        "database": database,
        "length": len(sequence_str)
    }


def extract_organism_from_title(title: str) -> str:
    """
    Extracts organism name from a sequence title or NCBI definition line.
    
    :param title: Definition line or sequence title
    :return: Extracted organism name or 'Unknown Organism'
    """
    if not title:
        return "Unknown Organism"

    # Strip leading GI / accession identifier prefix (e.g. "gi|887494115|gb|KT232088.1| ...")
    if "|" in title and len(title.split("|")) > 2:
        title = title.split("|")[-1].strip()

    if "[" in title and "]" in title:
        parts = title.split("[")
        for part in reversed(parts):
            if "]" in part:
                cand = part.split("]")[0].strip()
                if cand:
                    return cand

    for keyword in [" segment ", " genes for ", " gene for ", " genes ", " gene ", " complete cds ", " partial cds ", " mRNA", " genomic ", " chromosome ", " viral cRNA"]:
        if keyword in title:
            cand = title.split(keyword)[0].strip()
            if cand:
                return cand

    return "Unknown Organism"


def fetch_ncbi_metadata(accession_id: str, email: str = "user@example.com", db: Optional[str] = None) -> Dict[str, str]:
    """
    Fetches organism name and definition for a given accession ID using NCBI Entrez.

    :param accession_id: NCBI Accession ID
    :param email: User email required by NCBI Entrez policy
    :param db: Target database ('nucleotide' or 'protein')
    :return: Dictionary containing accession_id, organism, and definition
    """
    Entrez.email = email
    databases_to_try = [db] if db else ["nucleotide", "protein"]

    for target_db in databases_to_try:
        try:
            handle = Entrez.efetch(db=target_db, id=accession_id, rettype="gb", retmode="text")
            seq_rec = SeqIO.read(handle, "gb")
            handle.close()

            organism = seq_rec.annotations.get("organism", "Unknown Organism")
            definition = seq_rec.description if seq_rec.description else "No description available"

            if organism != "Unknown Organism":
                return {
                    "accession_id": accession_id,
                    "organism": organism,
                    "definition": definition,
                    "database_used": target_db
                }
        except Exception:
            pass

        try:
            handle = Entrez.esummary(db=target_db, id=accession_id, retmode="xml")
            records = Entrez.read(handle)
            handle.close()

            if records:
                doc_sum = records[0]
                title = doc_sum.get("Title", doc_sum.get("Caption", "No description available"))
                organism = doc_sum.get("Organism", "Unknown Organism")
                if organism == "Unknown Organism" and title:
                    organism = extract_organism_from_title(title)
                return {
                    "accession_id": accession_id,
                    "organism": organism,
                    "definition": title,
                    "database_used": target_db
                }
        except Exception:
            continue

    return {
        "accession_id": accession_id,
        "organism": "Unknown Organism",
        "definition": "Metadata unavailable",
        "database_used": "none"
    }

