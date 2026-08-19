import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ==============================================================================
# Mystery Sequence Identifier — İştirakçı 1 (Sequence Manager & Entrez Interface)
# ==============================================================================

import os
import io
from typing import Dict, Union, Optional

# BioPython kitabxanaları
try:
    from Bio import SeqIO, Entrez
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
except ImportError:
    # Əgər Google Colab və ya Replit işlədirsinizsə:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "biopython"])
    from Bio import SeqIO, Entrez
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord


# ------------------------------------------------------------------------------
# 1. FASTA Oxuma Funksiyası
# ------------------------------------------------------------------------------
def parse_fasta(input_source: str) -> SeqRecord:
    """Fayl yolunu və ya xammal FASTA mətnini Bio.SeqIO ilə təhlükəsiz oxuyur."""
    if not input_source or not isinstance(input_source, str):
        raise ValueError("Daxil edilən mənbə boş olmamalıdır.")

    if os.path.exists(input_source):
        with open(input_source, "r", encoding="utf-8") as handle:
            records = list(SeqIO.parse(handle, "fasta"))
        if not records:
            raise ValueError(f"'{input_source}' faylında ardıcıllıq tapılmadı.")
        return records[0]
    elif input_source.strip().startswith(">"):
        string_handle = io.StringIO(input_source.strip())
        records = list(SeqIO.parse(string_handle, "fasta"))
        if not records:
            raise ValueError("FASTA mətnində ardıcıllıq tapılmadı.")
        return records[0]
    else:
        raise FileNotFoundError(f"Fayl və ya düzgün FASTA mətni tapılmadı: '{input_source}'")


# ------------------------------------------------------------------------------
# 2. Ardıcıllıq Növünün Təyini (DNA / RNA / Protein)
# ------------------------------------------------------------------------------
def detect_sequence_type(seq_record: SeqRecord) -> Dict[str, Union[str, int]]:
    """DNT, RNT və ya Zülal olduğunu hesablayır və BLAST parametrlərini seçir."""
    sequence_str = str(seq_record.seq).upper().strip()
    if not sequence_str:
        raise ValueError("Ardıcıllıq boşdur.")

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


# ------------------------------------------------------------------------------
# 3. Başlıqdan Orqanizm Adının Çıxarılması
# ------------------------------------------------------------------------------
def extract_organism_from_title(title: str) -> str:
    """NCBI təsvir sətrindən orqanizmin adını çıxarır."""
    if not title:
        return "Unknown Organism"

    title = title.strip()
    if "|" in title and len(title.split("|")) > 2:
        title = title.split("|")[-1].strip()

    for prefix in ["PREDICTED: ", "RecName: Full=", "UNVERIFIED: "]:
        if title.startswith(prefix):
            title = title[len(prefix):].strip()

    if "[" in title and "]" in title:
        parts = title.split("[")
        for part in reversed(parts):
            if "]" in part:
                cand = part.split("]")[0].strip()
                if cand:
                    return cand

    earliest_idx = -1
    for keyword in [
        " segment", " genes for", " gene for", " genes", " gene",
        " complete cds", " partial cds", " mrna", " genomic",
        " chromosome", " viral crna", " mitochondrion", " chloroplast",
        " hemoglobin", " subunit", " protein", " isolate", " strain"
    ]:
        idx = title.lower().find(keyword)
        if idx != -1:
            if earliest_idx == -1 or idx < earliest_idx:
                earliest_idx = idx

    if earliest_idx > 0:
        cand = title[:earliest_idx].strip().rstrip(",").strip()
        if cand:
            return cand

    words = title.split()
    if len(words) >= 2 and words[0][0].isupper() and words[1].islower():
        return f"{words[0]} {words[1]}"

    return title if title else "Unknown Organism"


# ------------------------------------------------------------------------------
# 4. NCBI Entrez Metadata Sorğusu
# ------------------------------------------------------------------------------
def fetch_ncbi_metadata(accession_id: str, email: str = "user@example.com", db: Optional[str] = None) -> Dict[str, str]:
    """Bio.Entrez ilə orqanizm və gen məlumatını çəkir."""
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


# ==============================================================================
# TESTLƏRİN İCRASI
# ==============================================================================
print("==========================================================================")
print("  Participant 1 (Adiba) -- Test Results")
print("==========================================================================")

# 1. DNA test
dna_rec = SeqRecord(Seq("ATGCGATCGATCGATCGATCGATC"), id="test_dna")
print("\n[1] DNA Test:", detect_sequence_type(dna_rec))

# 2. Protein test
prot_rec = SeqRecord(Seq("MKTLLLTLLLLLLLLWVEAKL"), id="test_prot")
print("\n[2] Protein Test:", detect_sequence_type(prot_rec))

# 3. Entrez Metadata test (sends query to NCBI)
print("\n[3] Sending NCBI Entrez query...")
meta = fetch_ncbi_metadata("NC_012920")
print("Entrez Result:", meta)

print("\n==========================================================================")
