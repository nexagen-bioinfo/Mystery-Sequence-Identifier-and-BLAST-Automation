# 🧬 Mystery Sequence Identifier & BLAST Automation Pipeline

**NEXAGEN Scientific Initiative — Bioinformatika və Süni İntellekt Təşəbbüsü (2026)**

Bu proqram naməlum bioloji DNT/RNT və ya Zülal ardıcıllıqlarını (FASTA formatında) avtomatik təyin edən, NCBI (National Center for Biotechnology Information) bazaları ilə inteqrasiya olunan və identifikasiya hesabatları (CSV və Excel) hazırlayan modulyar bioinformatika boru kəməridir (pipeline).

---

## 🏛️ Layihə Arxitekturası və Modullar

Layihə 3 əsas modula bölünür:

| Rol / İştirakçı | Məsuliyyət Sahəsi | Çıxış Faylı / Modul |
| :--- | :--- | :--- |
| **İştirakçı 1** | FASTA oxuyucu, DNT/RNT/Zülal növünün təyini, BLAST alətinin (`blastn` vs `blastp`) seçilməsi və NCBI Entrez metadata sorğuları. | [`sequence_io.py`](sequence_io.py) |
| **İştirakçı 2** | `Bio.Blast.NCBIWWW` ilə `nt` və ya `nr` bazalarına uzaqdan sorğu göndərilməsi, Timeout/Exception Handling və XML keçləmə sistemi. | [`blast_engine.py`](blast_engine.py) |
| **İştirakçı 3** | `Bio.Blast.NCBIXML` vasitəsilə XML faylının pars edilməsi, E-value/Identity filtrlənməsi və CSV/Excel eksportu. | [`report_writer.py`](report_writer.py) |

---

## ⚙️ Quraşdırılma (Installation)

### 1. Repozitoriyanı klonlayın:
```bash
git clone https://github.com/nexagen-bioinfo/Mystery-Sequence-Identifier-and-BLAST-Automation.git
cd Mystery-Sequence-Identifier-and-BLAST-Automation
```

### 2. Virtual mühiti (venv) yaradın və aktivləşdirin:
```bash
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
# venv\Scripts\activate   # Windows
```

### 3. Tələb olunan asılılıqları quraşdırın:
```bash
pip install -r requirements.txt
```

---

## 🚀 İstifadə Qaydası (Usage)

Bütün boru kəməri terminaldan tək əmrlə `main.py` skripti vasitəsilə icra olunur:

```bash
python main.py --input data/PZ716984.fasta
```

### 🎛️ Əlavə Seçimlər və Parametrlər (CLI Options):

```bash
# E-value və Identity filtrlərini özünüz təyin edin:
python main.py --input data/PZ716984.fasta --evalue 1e-10 --identity 95.0 --top 10

# Keşlənmiş XML-ə baxmadan yenidən NCBI-a sorğu göndərmək üçün:
python main.py --input data/PZ716984.fasta --force-reblast
```

#### Parametr Açıqlamaları:
* `--input` / `-i`: **(Məcburi)** Analiz ediləcək FASTA faylının yolu.
* `--evalue` / `-e`: Maksimum E-value həddi *(Default: 1e-5)*.
* `--identity` / `-id`: Minimum Oxşarlıq Faizi (Identity %) *(Default: 90.0)*.
* `--top` / `-t`: Hesabata daxil ediləcək ən yaxşı matç sayısı *(Default: 5)*.
* `--force-reblast` / `-f`: Keş faylını yeniləyərək təzədən NCBI-a sorğu göndərir.

---

## 📂 Çıxış Faylları (Output Deliverables)

Boru kəməri icra olunduqda aşağıdakı qovluqlar və fayllar avtomatik yaradılır:

1. **`cache/`**: NCBI-dan gələn xammal XML faylları müvəqqəti saxlanc kimi buraya yazılır (təkrar sorğuların qarşısını alır).
2. **`reports/`**: Səliqəli CSV və Excel hesabatları buraya eksport edilir (sütunlar: *Accession ID, Organism Name, Definition, Alignment Length, Bit Score, E-value, Identity %*).

---

## 🧪 Unit Testlərin İcra Edilməsi

Bütün modulların düzgün işlədiyini yoxlamaq üçün test suitini icra edin:

```bash
python -m unittest discover tests
```

---

## 📜 Lisenziya və İştirakçılar

* **Təşkilat:** NEXAGEN Scientific Initiative
* **İl:** 2026