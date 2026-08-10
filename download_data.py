"""
download_data.py
================
NCBI Entrez və RCSB PDB vasitəsilə təyin olunmuş Accession nömrələrinin FASTA
ardıcıllıqlarını avtomatik endirib data/ qovluğuna yazan skript.
"""

import os
import urllib.request
from Bio import Entrez

# Entrez e-poçt konfiqurasiyası
Entrez.email = "nexagen.bioinfo@gmail.com"

# Yüklənəcək accession nömrələri siyahısı
ACCESSIONS = [
    {"id": "NC_012920", "type": "dna", "db": "nucleotide", "source": "ncbi"},
    {"id": "AC_000021", "type": "dna", "db": "nucleotide", "source": "ncbi"},
    {"id": "PZ716984", "type": "rna", "db": "nucleotide", "source": "ncbi"},
    {"id": "9GE4", "type": "protein", "db": "pdb", "source": "rcsb"}
]

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def download_fasta(acc_info: dict) -> bool:
    acc_id = acc_info["id"]
    source = acc_info["source"]
    output_path = os.path.join(DATA_DIR, f"{acc_id}.fasta")

    print(f"⌛ '{acc_id}' ({acc_info['type'].upper()}) endirilir...")

    try:
        fasta_data = ""
        if source == "ncbi":
            handle = Entrez.efetch(db=acc_info["db"], id=acc_id, rettype="fasta", retmode="text")
            fasta_data = handle.read()
            handle.close()
        elif source == "rcsb":
            url = f"https://www.rcsb.org/fasta/entry/{acc_id}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as response:
                fasta_data = response.read().decode("utf-8")

        if fasta_data and fasta_data.strip().startswith(">"):
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(fasta_data)
            print(f"✅ Müvəffəqiyyətlə yazıldı: {output_path} ({len(fasta_data)} bayt)")
            return True
        else:
            print(f"❌ Xəta: '{acc_id}' üçün keçərli FASTA cavabı alınmadı.")
            return False
    except Exception as e:
        print(f"❌ '{acc_id}' endirilərkən xəta baş verdi: {e}")
        return False


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("--- Accession FASTA Endirmə Prosesi Başladı ---\n")
    
    success_count = 0
    for item in ACCESSIONS:
        if download_fasta(item):
            success_count += 1
            
    print(f"\n✨ Tamamlandı: {len(ACCESSIONS)}-dən {success_count} FASTA faylı data/ qovluğuna saxlanıldı.")


if __name__ == "__main__":
    main()
