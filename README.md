# Gamma Spectrum Analysis Tool

## 1. Deskripsi Proyek

**Gamma Spectrum Analysis Tool** adalah program Python sederhana untuk menganalisis spektrum gamma dari file data berformat `.Spe`. Program ini dikembangkan sebagai produk fungsional untuk proyek radioanalisis dengan topik **Gamma Spectrum Analysis Tool (Python / Excel)**, tetapi implementasi proyek ini menggunakan **Python**.

Program ini dapat digunakan untuk:

1. Membaca data spektrum gamma dari file `.Spe`.
2. Menampilkan dan menyimpan grafik spektrum gamma.
3. Melakukan smoothing data spektrum.
4. Mendeteksi photopeak menggunakan metode peak detection.
5. Melakukan kalibrasi energi dari channel ke satuan keV.
6. Mengidentifikasi radionuklida berdasarkan pencocokan energi photopeak terhadap energi gamma referensi.
7. Menyimpan hasil analisis dalam format `.txt`, `.csv`, dan `.png`.

Program ini dibuat sebagai prototype produk nyata yang menunjukkan bagaimana metode spektrometri gamma digunakan dalam praktik radioanalisis.

---

## 2. Latar Belakang

Spektrometri gamma merupakan salah satu metode radioanalisis yang digunakan untuk mengidentifikasi radionuklida berdasarkan energi sinar gamma yang dipancarkan. Setiap radionuklida memiliki energi gamma karakteristik yang dapat muncul sebagai photopeak pada spektrum hasil pengukuran.

Dalam pengukuran spektrum gamma, data awal biasanya masih berupa hubungan antara **channel** dan **counts**. Channel belum langsung menunjukkan energi radiasi. Oleh karena itu, diperlukan proses **kalibrasi energi** agar channel dapat dikonversi menjadi energi dalam satuan keV.

Setelah spektrum dikalibrasi, posisi photopeak dapat dibandingkan dengan energi referensi radionuklida. Dengan cara ini, radionuklida seperti **Cs-137** dan **Co-60** dapat diidentifikasi secara kualitatif.

---

## 3. Tujuan Program

Tujuan utama program ini adalah membuat tool analisis spektrum gamma berbasis Python yang mampu:

- membaca data spektrum gamma dari file `.Spe`;
- melakukan visualisasi spektrum;
- mendeteksi photopeak;
- melakukan kalibrasi energi;
- mengidentifikasi radionuklida berdasarkan energi photopeak;
- menyimpan hasil analisis agar dapat digunakan dalam laporan atau dokumentasi proyek.

---

## 4. Metode Radioanalisis

Metode radioanalisis yang digunakan adalah:

**Spektrometri gamma berbasis analisis photopeak dan kalibrasi energi.**

Tahapan analisis yang digunakan:

1. Data spektrum gamma dibaca dari file `.Spe`.
2. Data counts diplot terhadap channel.
3. Data dihaluskan menggunakan moving average.
4. Photopeak dideteksi menggunakan `scipy.signal.find_peaks`.
5. Channel photopeak dikonversi menjadi energi menggunakan persamaan kalibrasi linear.
6. Energi peak terdeteksi dibandingkan dengan energi gamma referensi.
7. Radionuklida diidentifikasi secara kualitatif berdasarkan kecocokan energi.

---

## 5. Jenis Detektor

Data spektrum yang digunakan berasal dari pengukuran menggunakan detektor:

**BGO (Bismuth Germanate)**

Detektor BGO merupakan detektor sintilasi yang dapat digunakan untuk mendeteksi radiasi gamma. BGO memiliki efisiensi deteksi gamma yang baik karena densitas dan nomor atom efektifnya tinggi. Namun, resolusi energinya tidak setajam detektor HPGe, sehingga identifikasi pada program ini dibuat secara kualitatif dan menggunakan toleransi energi yang konservatif.

---

## 6. Data yang Digunakan

Data mentah disimpan pada folder:

```text
data/raw/

File data utama:

data/raw/BGO Cs137 0deg 300sec.Spe
data/raw/BGO Co60 0deg 600sec.Spe

Data tambahan/simulasi disimpan pada folder:

data/processed/

File data tambahan:

data/processed/Cs-137_Spectrum_Real.csv
data/processed/cs137_realistic.csv

Pada tool utama gamma_spectrum_tool.py, data utama yang dianalisis adalah file .Spe dari Cs-137 dan Co-60.

7. Struktur Folder Proyek

Struktur folder proyek:

radioanalisis/
│
├── data/
│   ├── raw/
│   │   ├── BGO Cs137 0deg 300sec.Spe
│   │   └── BGO Co60 0deg 600sec.Spe
│   │
│   └── processed/
│       ├── Cs-137_Spectrum_Real.csv
│       └── cs137_realistic.csv
│
├── docs/
│   ├── log_proses.md
│   └── keputusan_metodologi.md
│
├── notebooks/
│
├── output/
│   ├── figures/
│   └── reports/
│
├── src/
│   ├── baca_dataawal_specs137.py
│   ├── baca_dataawal_speco60.py
│   ├── cari_titik_kalibrasi.py
│   ├── kalibrasi_energi.py
│   ├── identifikasi_radionuklida.py
│   ├── gamma_spectrum_tool.py
│   ├── gammaspektum.py
│   ├── kalibrasi.py
│   └── data.py
│
├── README.md
├── requirements.txt
└── .gitignore

Keterangan folder:

Folder/File	Fungsi
data/raw/	Menyimpan data spektrum asli dari alat
data/processed/	Menyimpan data olahan atau simulasi
src/	Menyimpan script Python
docs/	Menyimpan dokumentasi proses dan keputusan metodologi
output/figures/	Menyimpan grafik hasil analisis
output/reports/	Menyimpan laporan hasil analisis dalam TXT dan CSV
requirements.txt	Daftar library Python yang dibutuhkan
README.md	Dokumentasi penggunaan proyek
8. Environment dan Dependensi

Program dibuat menggunakan Python dan beberapa library utama:

numpy
matplotlib
scipy
pandas
8.1 Membuat Virtual Environment

Dari folder utama proyek, jalankan:

python3 -m venv .venv

Aktifkan environment:

source .venv/bin/activate

Jika berhasil, terminal akan menampilkan tanda seperti:

(.venv)
8.2 Instalasi Dependensi

Install library dari requirements.txt:

pip install -r requirements.txt

Jika requirements.txt belum tersedia, install manual:

pip install numpy matplotlib scipy pandas

Simpan daftar library:

pip freeze > requirements.txt
8.3 Mengecek Environment

Jalankan:

python -c "import numpy, matplotlib, scipy, pandas; print('environment siap')"

Jika berhasil, terminal akan menampilkan:

environment siap
9. Kalibrasi Energi

Kalibrasi energi dilakukan untuk mengubah channel menjadi energi dalam satuan keV.

Model kalibrasi yang digunakan adalah model linear:

Energi (keV) = m × Channel + c

Titik kalibrasi yang digunakan:

Radionuklida	Channel	Energi Referensi
Cs-137	338	662.0 keV
Co-60	594	1173.2 keV

Hasil kalibrasi:

Energi (keV) = 1.9969 × Channel - 12.9437

Pada program utama, nilai slope dan intercept dihitung dari titik kalibrasi tersebut menggunakan numpy.polyfit.

10. Database Referensi Radionuklida

Database referensi yang digunakan masih sederhana dan terbatas pada radionuklida yang digunakan dalam data uji.

Radionuklida	Energi Gamma Referensi	Keterangan
Cs-137	661.7 keV	Photopeak utama Cs-137
Co-60	1173.2 keV	Photopeak pertama Co-60
Co-60	1332.5 keV	Photopeak kedua Co-60

Identifikasi dilakukan dengan mencocokkan energi peak hasil deteksi terhadap database referensi tersebut.

Toleransi pencocokan energi default:

±10 keV

Toleransi ini digunakan agar identifikasi lebih konservatif dan mengurangi kemungkinan false positive.

11. Cara Menjalankan Program Utama

Program utama berada di:

src/gamma_spectrum_tool.py
11.1 Menjalankan Analisis Default

Program akan menganalisis dua file default:

data/raw/BGO Cs137 0deg 300sec.Spe
data/raw/BGO Co60 0deg 600sec.Spe

Perintah:

python src/gamma_spectrum_tool.py
11.2 Menjalankan Tanpa Menampilkan Grafik

Jika hanya ingin menyimpan grafik tanpa membuka jendela plot:

python src/gamma_spectrum_tool.py --no-show
11.3 Menganalisis Satu File Tertentu

Contoh untuk Cs-137:

python src/gamma_spectrum_tool.py "data/raw/BGO Cs137 0deg 300sec.Spe"

Contoh untuk Co-60:

python src/gamma_spectrum_tool.py "data/raw/BGO Co60 0deg 600sec.Spe"
11.4 Mengubah Toleransi Energi

Default toleransi adalah ±10 keV. Untuk mengubah toleransi:

python src/gamma_spectrum_tool.py --tolerance 15
11.5 Mengubah Minimum Channel Analisis

Default minimum channel adalah 100. Untuk mengubah:

python src/gamma_spectrum_tool.py --min-channel 80
12. Output Program

Program menghasilkan tiga jenis output:

Grafik spektrum dalam format PNG.
Laporan analisis dalam format TXT.
Hasil identifikasi dalam format CSV.
12.1 Output Grafik

Disimpan di:

output/figures/

Contoh file:

output/figures/gamma_analysis_BGO_Cs137_0deg_300sec.png
output/figures/gamma_analysis_BGO_Co60_0deg_600sec.png
12.2 Output Laporan TXT

Disimpan di:

output/reports/

Contoh file:

output/reports/gamma_analysis_BGO_Cs137_0deg_300sec.txt
output/reports/gamma_analysis_BGO_Co60_0deg_600sec.txt
12.3 Output CSV

Disimpan di:

output/reports/

Contoh file:

output/reports/gamma_analysis_BGO_Cs137_0deg_300sec.csv
output/reports/gamma_analysis_BGO_Co60_0deg_600sec.csv
13. Hasil Uji Program
13.1 Hasil Uji Cs-137

File:

data/raw/BGO Cs137 0deg 300sec.Spe

Hasil:

Parameter	Nilai
Channel peak	339
Energi terdeteksi	664.00 keV
Energi referensi	661.7 keV
Selisih energi	2.30 keV
Status	Teridentifikasi berdasarkan satu photopeak

Interpretasi:

Cs-137 berhasil diidentifikasi karena photopeak terdeteksi pada energi 664.00 keV, sangat dekat dengan energi referensi Cs-137 sebesar 661.7 keV.

13.2 Hasil Uji Co-60

File:

data/raw/BGO Co60 0deg 600sec.Spe

Photopeak pertama:

Parameter	Nilai
Channel peak	595
Energi terdeteksi	1175.20 keV
Energi referensi	1173.2 keV
Selisih energi	2.00 keV

Photopeak kedua:

Parameter	Nilai
Channel peak	672
Energi terdeteksi	1328.96 keV
Energi referensi	1332.5 keV
Selisih energi	3.54 keV

Status:

Co-60 teridentifikasi kuat

Interpretasi:

Co-60 berhasil diidentifikasi kuat karena dua photopeak utamanya, yaitu sekitar 1173.2 keV dan 1332.5 keV, berhasil terdeteksi.

14. Contoh Output Terminal

Contoh ringkasan output program:

========================================================================
GAMMA SPECTRUM ANALYSIS TOOL
========================================================================
Jumlah file dianalisis : 2
Toleransi energi       : ±10.0 keV
Minimum channel        : 100

========================================================================
GAMMA SPECTRUM ANALYSIS TOOL
========================================================================
File dianalisis        : data/raw/BGO Cs137 0deg 300sec.Spe
Rumus kalibrasi        : Energi (keV) = 1.9969 * Channel + -12.9437
Prominence peak        : 135.10
Jumlah peak terdeteksi : 1

PEAK YANG COCOK DENGAN REFERENSI
------------------------------------------------------------------------
Cs-137         661.7      664.00       2.30       339

KESIMPULAN IDENTIFIKASI
------------------------------------------------------------------------
- Cs-137 | Teridentifikasi berdasarkan satu photopeak
  Alasan: Photopeak utama Cs-137 sekitar 661.7 keV terdeteksi pada spektrum.

========================================================================
GAMMA SPECTRUM ANALYSIS TOOL
========================================================================
File dianalisis        : data/raw/BGO Co60 0deg 600sec.Spe
Rumus kalibrasi        : Energi (keV) = 1.9969 * Channel + -12.9437
Prominence peak        : 10.00
Jumlah peak terdeteksi : 2

PEAK YANG COCOK DENGAN REFERENSI
------------------------------------------------------------------------
Co-60          1173.2     1175.20      2.00       595
Co-60          1332.5     1328.96      3.54       672

KESIMPULAN IDENTIFIKASI
------------------------------------------------------------------------
- Co-60 | Teridentifikasi kuat
  Alasan: Dua photopeak utama Co-60, yaitu 1173.2 keV dan 1332.5 keV, terdeteksi pada spektrum.
15. Alur Kerja Program

Alur kerja program:

Input file .Spe
      ↓
Baca data counts
      ↓
Buat array channel
      ↓
Smoothing spektrum
      ↓
Deteksi peak dengan find_peaks
      ↓
Kalibrasi channel ke energi keV
      ↓
Pencocokan energi peak dengan energi referensi
      ↓
Identifikasi radionuklida
      ↓
Simpan grafik, TXT, dan CSV
16. Script Penting
16.1 Program Utama
src/gamma_spectrum_tool.py

Fungsi:

menjalankan analisis lengkap;
membaca file .Spe;
mendeteksi peak;
melakukan kalibrasi energi;
mengidentifikasi radionuklida;
menyimpan output.
16.2 Script Pendukung
src/cari_titik_kalibrasi.py

Fungsi:

mencari titik peak awal untuk kalibrasi energi.
src/kalibrasi_energi.py

Fungsi:

menghitung dan menampilkan hasil kalibrasi energi.
src/identifikasi_radionuklida.py

Fungsi:

prototype awal fitur identifikasi radionuklida.
src/baca_dataawal_specs137.py
src/baca_dataawal_speco60.py

Fungsi:

membaca dan menampilkan spektrum awal Cs-137 dan Co-60.
17. Validitas Metode

Program ini dapat dipertanggungjawabkan karena:

Kalibrasi energi dilakukan menggunakan titik referensi dari sumber standar Cs-137 dan Co-60.
Persamaan kalibrasi dibuat secara linear, sesuai pendekatan dasar pada analisis spektrum gamma.
Peak detection dilakukan menggunakan scipy.signal.find_peaks, bukan pemilihan manual sepenuhnya.
Identifikasi radionuklida dilakukan berdasarkan pencocokan energi photopeak terhadap energi gamma referensi.
Toleransi energi dibuat konservatif, yaitu ±10 keV.
Co-60 hanya dinyatakan teridentifikasi kuat jika dua photopeak utamanya terdeteksi.
Output grafik, TXT, dan CSV disimpan agar hasil dapat diperiksa ulang.
18. Batasan Program

Program ini masih memiliki beberapa batasan:

Database referensi hanya mencakup Cs-137 dan Co-60.
Identifikasi radionuklida masih bersifat kualitatif.
Program belum menghitung aktivitas radioaktif.
Program belum menghitung efisiensi detektor.
Program belum melakukan koreksi background.
Program belum melakukan koreksi dead time.
Program belum menghitung ketidakpastian statistik secara lengkap.
Kalibrasi energi masih menggunakan model linear dua titik.
Program belum memiliki antarmuka GUI atau dashboard.

Batasan ini masih sesuai untuk tahap prototype proyek individu, karena fokus utama proyek adalah membuat tool sederhana yang dapat menunjukkan alur analisis spektrum gamma secara praktis.

19. Rencana Pengembangan Lanjutan

Pengembangan lanjutan yang dapat dilakukan:

Menambah database energi gamma radionuklida lain.
Menambahkan background correction.
Menambahkan Gaussian fitting untuk estimasi centroid peak yang lebih presisi.
Menambahkan perhitungan FWHM dan resolusi energi.
Menambahkan estimasi ketidakpastian energi.
Menambahkan fitur ekspor PDF otomatis.
Membuat antarmuka sederhana menggunakan Streamlit.
Menambahkan pilihan input file dari user.
Menambahkan laporan otomatis yang lebih lengkap.
20. Kesimpulan

Gamma Spectrum Analysis Tool telah berhasil dibuat sebagai prototype fungsional berbasis Python. Program ini mampu membaca data spektrum gamma, melakukan kalibrasi energi, mendeteksi photopeak, dan mengidentifikasi radionuklida Cs-137 serta Co-60 berdasarkan energi gamma referensi.

Hasil uji menunjukkan:

Cs-137 teridentifikasi dari photopeak 664.00 keV dengan selisih 2.30 keV terhadap referensi 661.7 keV.
Co-60 teridentifikasi kuat dari dua photopeak, yaitu 1175.20 keV dan 1328.96 keV, dengan selisih masing-masing 2.00 keV dan 3.54 keV terhadap energi referensi.

Dengan demikian, program ini telah memenuhi fungsi utama sebagai produk sederhana untuk analisis spektrum gamma berbasis Python.