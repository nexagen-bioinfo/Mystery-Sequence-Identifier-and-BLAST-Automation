"""
report_writer.py
================
NEXAGEN Scientific Initiative — Mystery Sequence Identifier
İştirakçı 3: XML Parser & Report Generator

Bu modul 3 əsas məsuliyyəti yerinə yetirir:
1. Bio.Blast.NCBIXML modulu vasitəsilə XML faylını pars etmək.
2. Gələn nəticələri statistik filtrlərdən keçirmək (E-value < 1e-5 və Identity % > 90%).
3. Ən yaxşı 5 hit (Top 5 Alignment Matches) üçün CSV və Excel formatında səliqəli hesabat yaratmaq.
"""

import os
from typing import List, Dict, Any, Optional
import pandas as pd
from Bio.Blast import NCBIXML
from sequence_io import fetch_ncbi_metadata


def parse_blast_xml(
    xml_filepath: str,
    max_evalue: float = 1e-5,
    min_identity: float = 90.0,
    top_n: int = 5,
    fetch_organism: bool = True
) -> List[Dict[str, Any]]:
    """
    BLAST XML faylını oxuyur, filtrləyir və ən yaxşı top_n uyğunluğu qaytarır.

    :param xml_filepath: XML faylının yolu
    :param max_evalue: Maksimum E-value həddi (default 1e-5)
    :param min_identity: Minimum Identity % həddi (default 90.0%)
    :param top_n: Qaytarılacaq ən yaxşı uyğunluq sayı (default 5)
    :param fetch_organism: NCBI Entrez vasitəsilə orqanizm adını dəqiqləşdirmək
    :return: Filtrlənmiş uyğunluqlar siyahısı (dict)
    """
    if not os.path.exists(xml_filepath):
        raise FileNotFoundError(f"XML faylı tapılmadı: {xml_filepath}")

    results = []

    with open(xml_filepath, "r", encoding="utf-8") as xml_handle:
        blast_records = list(NCBIXML.parse(xml_handle))

    for record in blast_records:
        for alignment in record.alignments:
            accession_id = alignment.accession if alignment.accession else alignment.hit_id
            full_title = alignment.title if alignment.title else alignment.hit_def

            for hsp in alignment.hsps:
                e_value = float(hsp.expect)
                align_length = int(hsp.align_length)
                bit_score = float(hsp.bits)
                identity_pct = (hsp.identities / align_length) * 100.0 if align_length > 0 else 0.0

                # 1. Filtrləmə qaydaları: E-value < 1e-5 VƏ Identity % > 90%
                if e_value <= max_evalue and identity_pct >= min_identity:
                    
                    # Orqanizm adını başlıqdan və ya Entrez-dən çəkirik
                    organism_name = "Naməlum Orqanizm"
                    definition = full_title
                    
                    # Başlıqdan Orqanizm adını süzmək (məsələn [Homo sapiens])
                    if "[" in full_title and "]" in full_title:
                        try:
                            organism_name = full_title.split("[")[-1].split("]")[0]
                        except Exception:
                            pass

                    # İştirakçı 1-in Entrez funksiyası ilə Orqanizm adını zənginləşdiririk
                    if fetch_organism and organism_name == "Naməlum Orqanizm" and accession_id:
                        meta = fetch_ncbi_metadata(accession_id)
                        organism_name = meta.get("organism", organism_name)
                        if meta.get("definition") and meta["definition"] != "Təsvir tapılmadı":
                            definition = meta["definition"]

                    results.append({
                        "Accession ID": accession_id,
                        "Organism Name": organism_name,
                        "Definition": definition,
                        "Alignment Length": align_length,
                        "Bit Score": round(bit_score, 2),
                        "E-value": e_value,
                        "Identity (%)": round(identity_pct, 2)
                    })

    # Nəticələri E-value-yə (kiçikdən böyüyə) və Bit Score-a (böyükdən kiçiyə) görə çeşidləyirik
    results.sort(key=lambda x: (x["E-value"], -x["Bit Score"]))

    # Unikal Accession ID-lər üzrə ən yaxşı top_n nəticəni saxlayırıq
    seen_accessions = set()
    top_results = []
    for item in results:
        acc = item["Accession ID"]
        if acc not in seen_accessions:
            seen_accessions.add(acc)
            top_results.append(item)
        if len(top_results) == top_n:
            break

    return top_results


def export_reports(
    results: List[Dict[str, Any]],
    output_dir: str = "reports",
    base_name: str = "blast_report"
) -> Dict[str, str]:
    """
    Filtrlənmiş nəticələri CSV və Excel fayllarına eksport edir.

    :param results: Filtrlənmiş nəticələr siyahısı
    :param output_dir: Hesabat fayllarının saxlanacağı qovluq
    :param base_name: Hesabat faylının əsas adı
    :return: {"csv": csv_path, "excel": excel_path}
    """
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.abspath(os.path.join(output_dir, f"{base_name}.csv"))
    excel_path = os.path.abspath(os.path.join(output_dir, f"{base_name}.xlsx"))

    # Sütunların ardıcıllığını təyin edirik
    columns = [
        "Accession ID",
        "Organism Name",
        "Definition",
        "Alignment Length",
        "Bit Score",
        "E-value",
        "Identity (%)"
    ]

    df = pd.DataFrame(results, columns=columns) if results else pd.DataFrame(columns=columns)

    # 1. CSV Eksportu
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"📄 [REPORT CSV] Səliqəli CSV yaradıldı: {csv_path}")

    # 2. Excel Eksportu
    try:
        df.to_excel(excel_path, index=False, engine="openpyxl")
        print(f"📊 [REPORT EXCEL] Səliqəli Excel yaradıldı: {excel_path}")
    except Exception as e:
        print(f"⚠️ Excel eksportu zamanı openpyxl xətası (CSV yenə də hazırdır): {e}")
        excel_path = ""

    return {"csv": csv_path, "excel": excel_path}

