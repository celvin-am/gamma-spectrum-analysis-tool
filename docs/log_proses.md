# Log Proses Pengerjaan Proyek

## Identitas Proyek
Judul sementara:
Gamma Spectrum Analysis Tool Berbasis Python untuk Analisis Spektrum Cs-137 dan Co-60 Menggunakan Detektor BGO

## Struktur Folder
Folder proyek telah dirapikan menjadi:
- data/raw: menyimpan data spektrum asli format .Spe
- data/processed: menyimpan data CSV hasil olahan/simulasi
- src: menyimpan script Python
- output/figures: menyimpan grafik hasil analisis
- output/reports: menyimpan proposal dan laporan
- docs: menyimpan dokumentasi proses dan metodologi

## Data Mentah
Data mentah yang digunakan:
1. BGO Cs137 0deg 300sec.Spe
2. BGO Co60 0deg 600sec.Spe

Kedua data disimpan pada folder:
data/raw/

## Environment Python
Virtual environment telah dibuat menggunakan:
python3 -m venv .venv

Library yang telah diinstal:
- numpy
- matplotlib
- scipy
- pandas

Environment telah diuji dengan import seluruh library dan berhasil.

## Tahap 1: Pembacaan Spektrum Cs-137
Script:
src/baca_dataawal_specs137.py

Hasil:
- File .Spe Cs-137 berhasil dibaca.
- Total channel: 1024.
- Grafik spektrum channel vs counts berhasil ditampilkan.
- Photopeak utama terlihat jelas di sekitar channel 338.

## Tahap 2: Peak Detection untuk Titik Kalibrasi
Script:
src/cari_titik_kalibrasi.py

Hasil:
- Peak Cs-137 terdeteksi pada channel 338.
- Peak Co-60 pertama terdeteksi pada channel 594.
- Peak Co-60 kedua belum terdeteksi otomatis dengan parameter saat ini.

Keputusan sementara:
Kalibrasi energi awal menggunakan dua titik:
- Channel 338 = 662 keV dari Cs-137
- Channel 594 = 1173.2 keV dari Co-60

## Tahap 3: Kalibrasi Energi
Script:
src/kalibrasi_energi.py

Hasil kalibrasi linear:
Energi (keV) = 1.9969 × Channel - 12.9437

Hasil:
- Spektrum Cs-137 berhasil ditampilkan dalam satuan energi keV.
- Garis referensi 662 keV sesuai dengan photopeak Cs-137.

## Tahap 4: Identifikasi Radionuklida
Script:
src/identifikasi_radionuklida.py

Metode:
Identifikasi dilakukan dengan mencocokkan energi photopeak hasil kalibrasi terhadap database energi gamma referensi sederhana.

Database referensi:
- Cs-137: 661.7 keV
- Co-60: 1173.2 keV
- Co-60: 1332.5 keV

Hasil Cs-137:
- Peak terdeteksi pada channel 339
- Energi terdeteksi: 664.01 keV
- Energi referensi: 661.7 keV
- Selisih: 2.31 keV
- Kesimpulan: Cs-137 teridentifikasi berdasarkan satu photopeak utama

Hasil Co-60:
- Peak pertama terdeteksi pada channel 595
- Energi terdeteksi: 1175.21 keV
- Energi referensi: 1173.2 keV
- Selisih: 2.01 keV

- Peak kedua terdeteksi pada channel 672
- Energi terdeteksi: 1328.97 keV
- Energi referensi: 1332.5 keV
- Selisih: 3.53 keV

Kesimpulan:
Co-60 teridentifikasi kuat karena dua photopeak referensi Co-60 berhasil terdeteksi.

Output grafik:
- output/figures/identifikasi_BGO_Cs137_0deg_300sec.png
- output/figures/identifikasi_BGO_Co60_0deg_600sec.png
