import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. DATA REFERENSI (STANDAR KALIBRASI)
# ==========================================
# Anggap kita sudah mengukur dua sumber standar di laboratorium:
# Cs-137 (Energi 662 keV) muncul di Channel 660
# Co-60  (Energi 1173 keV) muncul di Channel 1170
# Co-60  (Energi 1332 keV) muncul di Channel 1330

channels_terukur = np.array([660, 1170, 1330])
energi_sebenarnya = np.array([662.0, 1173.2, 1332.5])

# ==========================================
# 2. MENGHITUNG RUMUS KALIBRASI (y = mx + c)
# ==========================================
# Fungsi np.polyfit(x, y, 1) akan otomatis mencari garis regresi linear terbaik.
# Angka '1' di akhir berarti kita membuat garis lurus (derajat 1).
m, c = np.polyfit(channels_terukur, energi_sebenarnya, 1)

print("=== HASIL KALIBRASI ===")
print(f"Nilai m (slope)     : {m:.4f}")
print(f"Nilai c (intercept) : {c:.4f}")
print(f"Rumus Resmi         : Energi = ({m:.4f} * Channel) + {c:.4f}")

# ==========================================
# 3. VISUALISASI GRAFIK KALIBRASI
# ==========================================
plt.figure(figsize=(8, 5))

# Menggambar titik data referensi kita (warna merah)
plt.plot(channels_terukur, energi_sebenarnya, 'ro', markersize=8, label='Titik Data Standar')

# Menggambar garis lurus hasil perhitungan komputer (warna biru)
garis_x = np.linspace(0, 1500, 100) # Membuat rentang channel dari 0 sampai 1500
garis_y = m * garis_x + c           # Menerapkan rumus kalibrasi
plt.plot(garis_x, garis_y, 'b-', linewidth=2, label='Garis Kalibrasi (Regresi)')

plt.title("Grafik Kalibrasi Energi Detektor Gamma")
plt.xlabel("Channel")
plt.ylabel("Energi (keV)")
plt.legend()
plt.grid(True, linestyle='--')

# Tampilkan grafik
plt.show()