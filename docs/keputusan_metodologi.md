# Keputusan Metodologi

## Metode Radioanalisis
Metode yang digunakan adalah spektrometri gamma berbasis analisis spektrum energi.

Tahapan utama:
1. Membaca data spektrum gamma dari file .Spe.
2. Menampilkan spektrum counts terhadap channel.
3. Melakukan smoothing sederhana untuk mengurangi fluktuasi statistik.
4. Mendeteksi photopeak menggunakan metode peak detection.
5. Melakukan kalibrasi energi dari channel ke keV.
6. Mengidentifikasi radionuklida berdasarkan energi photopeak.

## Jenis Detektor
Detektor yang digunakan adalah BGO (Bismuth Germanate).

Alasan:
- Data eksperimen yang tersedia berasal dari pengukuran menggunakan detektor BGO.
- BGO dapat digunakan untuk mendeteksi radiasi gamma.
- Resolusi energi BGO tidak setinggi HPGe, tetapi cukup untuk analisis dasar spektrum gamma dan kalibrasi energi.

## Sumber Radioaktif
Sumber yang digunakan:
1. Cs-137
   - Energi photopeak referensi: sekitar 662 keV
2. Co-60
   - Energi photopeak referensi: sekitar 1173.2 keV dan 1332.5 keV

## Kalibrasi Energi
Model kalibrasi yang digunakan adalah regresi linear:

Energi = m × Channel + c

Titik kalibrasi awal:
- Channel 338 → 662 keV
- Channel 594 → 1173.2 keV

Hasil:
Energi (keV) = 1.9969 × Channel - 12.9437

## Batasan Sementara
- Peak kedua Co-60 belum terdeteksi otomatis dengan parameter peak detection saat ini.
- Produk masih berada pada tahap prototype awal.
- Identifikasi radionuklida masih akan dikembangkan berdasarkan pencocokan energi photopeak terhadap tabel referensi sederhana.

## Identifikasi Radionuklida

Identifikasi radionuklida dilakukan secara kualitatif dengan metode pencocokan energi photopeak. Energi peak yang terdeteksi dari spektrum dikonversi dari channel ke keV menggunakan persamaan kalibrasi energi, kemudian dibandingkan dengan energi gamma referensi.

Toleransi pencocokan energi yang digunakan adalah ±10 keV. Nilai ini digunakan agar identifikasi lebih konservatif dan mengurangi kemungkinan false positive.

Aturan interpretasi:
- Cs-137 diidentifikasi apabila photopeak sekitar 661.7 keV terdeteksi.
- Co-60 dinyatakan teridentifikasi kuat apabila dua photopeak utamanya, yaitu 1173.2 keV dan 1332.5 keV, terdeteksi.
- Jika hanya satu photopeak Co-60 terdeteksi, statusnya dianggap indikatif, bukan identifikasi kuat.

Hasil akhir menunjukkan:
- Cs-137 teridentifikasi dari photopeak 664.01 keV.
- Co-60 teridentifikasi kuat dari dua photopeak 1175.21 keV dan 1328.97 keV.
