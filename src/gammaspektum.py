import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# =========================
# 1. LOAD DATA YANG BENAR
# =========================
# Kita gunakan Pandas agar lebih rapi dalam membaca nama kolom CSV
df = pd.read_csv("data/processed/Cs-137_Spectrum_Real.csv")
channel = df['Channel'].values
counts = df['Counts'].values

# =========================
# 2. SMOOTHING (Menghaluskan Grafik)
# =========================
# Meratakan grafik agar fluktuasi statistik (noise) tidak dianggap sebagai puncak
smooth_counts = np.convolve(counts, np.ones(7)/7, mode='same')

# =========================
# 3. DETEKSI SEMUA PEAK (PUNCAK)
# =========================
# prominence=50 berarti kita hanya mencari puncak yang menonjol (seperti gunung asli), 
# bukan sekadar gundukan kecil akibat noise detektor.
peaks, properties = find_peaks(smooth_counts, height=100, prominence=50)

peak_channels = channel[peaks]
peak_counts = smooth_counts[peaks]
print("Semua peak terdeteksi di channel:", peak_channels)

# =========================
# 4. FILTER PEAK MASUK AKAL (Area Cs-137)
# =========================
# Photopeak Cs-137 biasanya ada di energi 662 keV. Kita cari di rentang channel 600 - 750.
valid_mask = (peak_channels > 600) & (peak_channels < 750)
valid_channels = peak_channels[valid_mask]
valid_counts = peak_counts[valid_mask]

# =========================
# 5. PILIH PHOTOPEAK UTAMA
# =========================
if len(valid_channels) > 0:
    max_index = np.argmax(valid_counts)
    photopeak_channel = valid_channels[max_index]
    photopeak_count = valid_counts[max_index]

    print(f"✅ Photopeak Cs-137 valid ditemukan di channel: {photopeak_channel}")
    print(f"✅ Jumlah cacahan (counts): {round(photopeak_count)}")
else:
    print("❌ Tidak ditemukan peak dalam area tersebut.")
    photopeak_channel = None

# =========================
# 6. VISUALISASI KE GRAFIK PINTAR
# =========================
plt.figure(figsize=(10,6))

# Gambar data asli (warna biru, transparan)
plt.plot(channel, counts, label="Data Mentah (Ada Noise)", alpha=0.3, color='blue')

# Gambar garis halus hasil smoothing (merah tua)
plt.plot(channel, smooth_counts, label="Garis Halus (Smooth)", linewidth=2, color='darkred')

# Beri tanda silang hitam pada semua puncak yang ditemukan
plt.plot(peak_channels, peak_counts, "kx", markersize=8, label="Puncak Terdeteksi")

# Beri titik hijau terang pada target utama kita (Cs-137)
if photopeak_channel is not None:
    plt.plot(photopeak_channel, photopeak_count, "go", markersize=10, label=f"Cs-137 Photopeak (Ch {int(photopeak_channel)})")
    plt.axvline(photopeak_channel, color='green', linestyle='--', alpha=0.5)

plt.title("Analisis Spektrum Gamma Cs-137")
plt.xlabel("Channel (Mewakili Energi Radiasi)")
plt.ylabel("Counts (Jumlah Radiasi)")
plt.legend()
plt.grid(True, alpha=0.3)

# Tampilkan ke layar
plt.show()