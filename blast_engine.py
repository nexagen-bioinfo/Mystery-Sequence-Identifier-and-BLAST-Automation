"""
blast_engine.py
===============
NEXAGEN Scientific Initiative — Mystery Sequence Identifier
İştirakçı 2: Remote BLAST Engine

Bu modul 3 əsas məsuliyyəti yerinə yetirir:
1. Bio.Blast.NCBIWWW.qblast() vasitəsilə nt (nucleotide) və ya nr (protein) bazalarına sorğu göndərmək.
2. Şəbəkə xətaları və server gözləmələri zamanı Timeout & Exception Handling (təkrar cəhd məntiqi) təmin etmək.
3. Serverdən gələn xammal (raw) XML nəticəsini 'cache/' qovluğuna saxlamaq.
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
    SeqRecord obyektini qəbul edir, avtomatik blastn/blastp seçir və NCBI-a sorğu göndərir.
    Nəticəni raw XML kimi keşkə faylına yazır və XML faylının yolunu (path) qaytarır.

    :param seq_record: Bio.SeqRecord obyekti
    :param cache_dir: Müvəqqəti XML faylının saxlanılacağı qovluq
    :param force_reblast: Əgər True olarsa, keşə baxmadan yenidən NCBI-a müraciət edir
    :param max_retries: Şəbəkə xətası olduqda maksimum təkrar cəhd sayısı
    :param retry_delay: Təkrar cəhdlər arası gözləmə müddəti (saniyə)
    :param hitlist_size: Qaytarılacaq maksimum uyğunluq sayı
    :param expect: E-value həddi (cutoff)
    :return: Saxlanılan XML faylının mütləq (absolute) yolu
    """
    os.makedirs(cache_dir, exist_ok=True)
    
    # Keş faylının adını təyin edirik
    safe_seq_id = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in str(seq_record.id))
    xml_filename = f"blast_{safe_seq_id}.xml"
    xml_filepath = os.path.abspath(os.path.join(cache_dir, xml_filename))

    # 1. Əgər keş faylı artıq varsa və force_reblast=False-dursa, birbaşa keşdən oxuyuruq
    if os.path.exists(xml_filepath) and not force_reblast:
        print(f"⚡ [CACHE] '{seq_record.id}' üçün nəticə keşdən oxundu: {xml_filepath}")
        return xml_filepath

    # 2. İştirakçı 1-in funksiyası vasitəsilə ardıcıllıq növünü təyin edirik
    seq_info = detect_sequence_type(seq_record)
    program = seq_info["blast_program"]   # 'blastn' və ya 'blastp'
    database = seq_info["database"]       # 'nt' və ya 'nr'

    print(f"🌐 [NCBI BLAST] '{seq_record.id}' üçün {program.upper()} sorğusu göndərilir...")
    print(f"   Program: {program} | Baza: {database} | Uzunluq: {seq_info['length']} bp/aa")

    fasta_data = seq_record.format("fasta")

    # 3. Exception Handling & Retry Logic ilə NCBI-a sorğu göndəririk
    attempt = 0
    raw_xml_data = None

    while attempt < max_retries:
        attempt += 1
        try:
            print(f"   ⌛ NCBI serverinə müraciət edilir (Cəhd {attempt}/{max_retries})... Bu 15-60 saniyə çəkə bilsin.")
            
            # NCBIWWW.qblast sorğusu
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
                print("   ✅ NCBI-dan keçərli XML cavabı alındı!")
                break
            else:
                print("   ⚠️ Xəbərdarlıq: Serverdən gələn XML tam deyil. Yenidən cəhd olunur...")

        except Exception as e:
            print(f"   ❌ Şəbəkə/Server xətası baş verdi (Cəhd {attempt}): {e}")
            if attempt < max_retries:
                print(f"   💤 {retry_delay} saniyə gözlənilir və yenidən cəhd edilir...")
                time.sleep(retry_delay)

    if not raw_xml_data:
        raise RuntimeError(f"'{seq_record.id}' üçün {max_retries} cəhddən sonra NCBI BLAST sorğusu uğursuz oldu.")

    # 4. Raw XML nəticəsini keş faylına yazırıq
    with open(xml_filepath, "w", encoding="utf-8") as xml_file:
        xml_file.write(raw_xml_data)

    print(f"💾 [SAVED] Raw XML keşkə yazıldı: {xml_filepath}")
    return xml_filepath



