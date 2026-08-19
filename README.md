# Mystery Sequence Identifier — Module 1: Sequence Manager & Entrez Interface

**İştirakçı 1 (Adiba)** — NEXAGEN Scientific Initiative (2026)

Bu modul naməlum bioloji nümunələrin (`FASTA` formatında DNT, RNT və ya Zülal ardıcıllıqları) daxil edilməsini, növünün avtomatik aşkarlanmasını, uyğun BLAST proqramının seçilməsini və NCBI Entrez vasitəsilə metadata (orqanizm adı, gen təsviri) çəkilməsini təmin edir.

---

## 🛠 Modulun Əsas Məsuliyyətləri və Funksiyaları

| Funksiya | Təsvir | Giriş Parametri | Çıxış |
| :--- | :--- | :--- | :--- |
| `parse_fasta(input_source)` | `Bio.SeqIO` ilə `.fasta` faylını və ya xammal FASTA mətnini təhlükəsiz oxuyur. | Fayl yolu və ya FASTA mətni | `Bio.SeqRecord.SeqRecord` |
| `detect_sequence_type(seq_record)` | Ardıcıllığı analiz edərək `DNA`, `RNA` və ya `PROTEIN` növünü təyin edir, `blastn`/`nt` və ya `blastp`/`nr` seçir. | `SeqRecord` obyekti | Metadata lüğəti (`dict`) |
| `extract_organism_from_title(title)` | NCBI başlıqlarından və gen təsvirlərindən orqanizmin elmi adını çıxarır. | Başlıq mətni (`str`) | Orqanizm adı (`str`) |
| `fetch_ncbi_metadata(accession_id)` | `Bio.Entrez` (`efetch` və `esummary`) vasitəsilə Accession ID üçün tam taksonomik məlumatları çəkir. | Accession ID (`str`) | Metadata lüğəti (`dict`) |

---

## 🚀 Quraşdırma və İstifadə

### 1. Asılılıqların quraşdırılması:
```bash
pip install -r requirements.txt
```

### 2. Python kodunda istifadə nümunəsi:
```python
from sequence_io import parse_fasta, detect_sequence_type, fetch_ncbi_metadata

# 1. FASTA faylını oxumaq
record = parse_fasta("data/PZ716984.fasta")
print(f"ID: {record.id}, Uzunluq: {len(record.seq)}")

# 2. Ardıcıllığın növünü və BLAST proqramını təyin etmək
seq_info = detect_sequence_type(record)
print("Ardıcıllıq Növü:", seq_info["sequence_type"])       # Məs: DNA
print("Seçilmiş BLAST:", seq_info["blast_program"])        # Məs: blastn
print("Hədəf Baza:", seq_info["database"])                 # Məs: nt

# 3. Accession ID üçün NCBI Entrez məlumatını gətirmək
meta = fetch_ncbi_metadata("NC_012920")
print("Orqanizm:", meta["organism"])                       # Məs: Homo sapiens
print("Təsvir:", meta["definition"])
```

---

## 🧪 Unit Testlərin İcrası

Modul 1-in bütün funksiyalarını fərdi şəkildə test etmək üçün:

```bash
python -m unittest test_sequence_io.py
```

---

## 📁 Qovluq Strukturu

```
├── sequence_io.py         # Modul 1: Əsas çıxış kodu (SeqIO və Entrez)
├── test_sequence_io.py    # Modul 1 üçün xüsusi Unit Testlər
├── requirements.txt       # Layihə asılılıqları (BioPython)
├── README.md              # İştirakçı 1 sənədləşməsi
└── data/                  # Test üçün nümunə FASTA ardıcıllıqları
```