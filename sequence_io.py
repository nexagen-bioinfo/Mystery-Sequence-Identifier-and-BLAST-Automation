"""
sequence_io.py
==============
NEXAGEN Scientific Initiative — Mystery Sequence Identifier
İştirakçı 1: Sequence Manager & Entrez Interface

Bu modul 3 əsas məsuliyyəti yerinə yetirir:
1. FASTA faylını/mətni Bio.SeqIO ilə təhlükəsiz oxumaq.
2. Ardıcıllığın növünü (DNT, RNT və ya Zülal) avtomatik təyin etmək və uyğun BLAST alətini (blastn vs blastp) seçmək.
3. NCBI Accession ID üçün Bio.Entrez istifadə edərək orqanizm adı və gen təsvirini çəkmək.
"""

import os
import io
from typing import Dict, Union, Optional
from Bio import SeqIO, Entrez
from Bio.SeqRecord import SeqRecord


def parse_fasta(input_source: str) -> SeqRecord:
    """
    FASTA formatındakı fayl yolunu və ya raw FASTA mətni qəbul edir və Bio.SeqRecord obyektini qaytarır.

    :param input_source: Fayl yolu (path) və ya FASTA formatında mətn string-i
    :return: SeqRecord obyekti
    :raises ValueError: Əgər daxiletmə düzgün FASTA formatında deyilsə
    :raises FileNotFoundError: Əgər fayl tapılmazsa
    """
    if not input_source or not isinstance(input_source, str):
        raise ValueError("Daxil edilən məlumat boş ola bilməz və string olmalıdır.")

    # Əgər input verilən fayl yoludursa
    if os.path.exists(input_source):
        try:
            with open(input_source, "r") as handle:
                records = list(SeqIO.parse(handle, "fasta"))
            if not records:
                raise ValueError(f"'{input_source}' faylında heç bir FASTA ardıcıllığı tapılmadı.")
            return records[0]  # İlk ardıcıllığı qaytarırıq
        except Exception as e:
            raise ValueError(f"FASTA faylını oxuyarkən xəta baş verdi: {e}")

    # Əgər input raw FASTA mətndirsə (məsələn: ">seq1\nATGCG...")
    elif input_source.strip().startswith(">"):
        try:
            string_handle = io.StringIO(input_source.strip())
            records = list(SeqIO.parse(string_handle, "fasta"))
            if not records:
                raise ValueError("Daxil edilən mətndə keçərli FASTA ardıcıllığı tapılmadı.")
            return records[0]
        except Exception as e:
            raise ValueError(f"FASTA mətnini pars edərkən xəta baş verdi: {e}")
    else:
        raise FileNotFoundError(f"Fayl tapılmadı və ya daxil edilən mətn FASTA formatında deyil: '{input_source}'")


def detect_sequence_type(seq_record: SeqRecord) -> Dict[str, Union[str, int]]:
    """
    SeqRecord obyektindəki ardıcıllığı analiz edərək onun DNT, RNT və ya Zülal (Protein) olduğunu təyin edir
    və uyğun BLAST alətini (blastn vs blastp) və verilənlər bazasını (nt vs nr) seçir.

    :param seq_record: Bio.SeqRecord obyekti
    :return: Ardıcıllıq məlumatları olan lüğət (dict)
    """
    sequence_str = str(seq_record.seq).upper().strip()
    if not sequence_str:
        raise ValueError("Ardıcıllıq zənciri boşdur.")

    # Nukleotid (DNT/RNT) simvolları (kənarlaşdırma payı ilə N daxil olmaqla)
    dna_rna_chars = set("ATCGUN")
    
    # Ardıcıllıqdakı simvolların neçə faizinin nukleotid olduğunu hesablayaq
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


def fetch_ncbi_metadata(accession_id: str, email: str = "nexagen.bioinfo@gmail.com", db: Optional[str] = None) -> Dict[str, str]:
    """
    NCBI Accession ID üçün Bio.Entrez istifadə edərək orqanizmin tam taksonomik adını və gen təsvirini (definition) çəkir.

    :param accession_id: NCBI Accession ID (məsələn: 'NM_001301717' və ya 'NP_001005353')
    :param email: NCBI Entrez tələbinə uyğun istifadəçi e-poçtu
    :param db: 'nucleotide' və ya 'protein'. Əgər verilməzsə avtomatik sorğulanır.
    :return: {"accession_id": ..., "organism": ..., "definition": ...}
    """
    Entrez.email = email
    
    # DB təyin olunmayıbsa avtomatik sınayırıq (nucleotide -> protein)
    databases_to_try = [db] if db else ["nucleotide", "protein"]
    
    for target_db in databases_to_try:
        try:
            handle = Entrez.esummary(db=target_db, id=accession_id, retmode="xml")
            records = Entrez.read(handle)
            handle.close()

            if records:
                # ESummary cavabından məlumatı çıxarırıq
                doc_sum = records[0]
                organism = doc_sum.get("Organism", "Naməlum Orqanizm")
                definition = doc_sum.get("Title", doc_sum.get("Caption", "Təsvir tapılmadı"))
                
                return {
                    "accession_id": accession_id,
                    "organism": organism,
                    "definition": definition,
                    "database_used": target_db
                }
        except Exception:
            continue

    # Əgər esummary tapmasa fallback olaraq efetch sınaya bilərik
    return {
        "accession_id": accession_id,
        "organism": "Təyin olunmadı",
        "definition": "Metadata əldə edilə bilmədi",
        "database_used": "none"
    }



