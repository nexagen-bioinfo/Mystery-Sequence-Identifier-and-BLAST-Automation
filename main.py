"""
main.py
=======
NEXAGEN Scientific Initiative — Mystery Sequence Identifier & BLAST Automation

Bu skript bütün 3 iştirakçının modullarını (sequence_io, blast_engine, report_writer)
birlaşdirərək terminaldan tək əmrlə işləyən tam avtomatlaşdırılmış bioinformatika boru kəməridir (pipeline).

İstifadə qaydası:
    python main.py --input data/PZ716984.fasta
"""

import os
import sys
import argparse
from sequence_io import parse_fasta, detect_sequence_type
from blast_engine import run_blast
from report_writer import parse_blast_xml, export_reports


def main():
    parser = argparse.ArgumentParser(
        description="NEXAGEN Mystery Sequence Identifier & BLAST Automation Pipeline"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Analiz ediləcək FASTA faylının yolu (məsələn: data/PZ716984.fasta)"
    )
    parser.add_argument(
        "--force-reblast", "-f",
        action="store_true",
        help="Keş faylına baxmadan yenidən NCBI BLAST sorğusu göndər"
    )
    parser.add_argument(
        "--evalue", "-e",
        type=float,
        default=1e-5,
        help="Maksimum E-value həddi (default: 1e-5)"
    )
    parser.add_argument(
        "--identity", "-id",
        type=float,
        default=90.0,
        help="Minimum Identity %% həddi (default: 90.0)"
    )
    parser.add_argument(
        "--top", "-t",
        type=int,
        default=5,
        help="Hesabata daxil ediləcək top hit sayısı (default: 5)"
    )

    args = parser.parse_args()

    print("==========================================================================")
    print("🚀 NEXAGEN Mystery Sequence Identifier & BLAST Automation Pipeline")
    print("==========================================================================")

    # Addım 1: FASTA Oxunması (İştirakçı 1)
    print(f"\n[ADDIM 1] FASTA faylı oxunur: '{args.input}'")
    seq_record = parse_fasta(args.input)
    print(f"   ► Ardıcıllıq ID: {seq_record.id}")

    # Addım 2: Növ və BLAST Aləti Seçimi (İştirakçı 1)
    seq_info = detect_sequence_type(seq_record)
    print(f"   ► Ardıcıllıq Növü: {seq_info['sequence_type']}")
    print(f"   ► Seçilmiş BLAST Aləti: {seq_info['blast_program'].upper()} | Baza: {seq_info['database']}")
    print(f"   ► Zəncir Uzunluğu: {seq_info['length']} bp/aa")

    # Addım 3: Remote BLAST Sorğusu & Keşləmə (İştirakçı 2)
    print(f"\n[ADDIM 2] NCBI BLAST sorğusu icra olunur...")
    xml_filepath = run_blast(seq_record, force_reblast=args.force_reblast)

    # Addım 4: XML Pars Edilməsi və Filtrləmə (İştirakçı 3)
    print(f"\n[ADDIM 3] BLAST Nəticələri pars edilir və filtrlənir...")
    print(f"   ► Filtrlər: E-value <= {args.evalue} | Identity >= {args.identity}%")
    top_hits = parse_blast_xml(
        xml_filepath,
        max_evalue=args.evalue,
        min_identity=args.identity,
        top_n=args.top
    )

    print(f"   ► Tapılan Ən Yaxşı Top Match Sayı: {len(top_hits)}")

    # Terminalda Nəticələrin Səliqəli Göstərilməsi
    if top_hits:
        print("\n--------------------------------------------------------------------------")
        print(f"{'Accession ID':<15} | {'Identity (%)':<12} | {'E-value':<10} | {'Organism Name'}")
        print("--------------------------------------------------------------------------")
        for hit in top_hits:
            print(f"{hit['Accession ID']:<15} | {hit['Identity (%)']:<12.2f} | {hit['E-value']:<10.1e} | {hit['Organism Name']}")
        print("--------------------------------------------------------------------------")

        # Addım 5: CSV və Excel Hesabatının Yaradılması (İştirakçı 3)
        base_name = f"report_{seq_record.id.replace('|', '_').replace('/', '_')}"
        reports = export_reports(top_hits, base_name=base_name)
        
        print("\n✨ BORU KƏMƏRİ UĞURLA TAMAMLANDI!")
        print(f"   📄 CSV Hesabatı: {reports['csv']}")
        if reports.get('excel'):
            print(f"   📊 Excel Hesabatı: {reports['excel']}")
    else:
        print("\n⚠️ Verilmiş filtrlərə uyğun heç bir hit tapılmadı.")


if __name__ == "__main__":
    main()
