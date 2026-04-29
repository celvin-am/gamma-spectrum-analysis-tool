import numpy as np
from scipy.signal import find_peaks

# ==========================================
# 1. FUNGSI PEMBACA FILE .Spe
# ==========================================
def baca_file_spe(nama_file):
    counts = []
    in_data_block = False

    with open(nama_file, 'r') as file:
        for line in file:
            line = line.strip()

            if line == '$DATA:':
                in_data_block = True
                continue

            if in_data_block:
                if line.startswith('$'):
                    break

                parts = line.split()
                if len(parts) == 1:
                    counts.append(int(parts[0]))

    return np.array(counts)


print("=== MENCARI TITIK PUNCAK UNTUK KALIBRASI ===")

# ==========================================
# 2. MENCARI PUNCAK Cs-137
# ==========================================
try:
    counts_cs = baca_file_spe("data/raw/BGO Cs137 0deg 300sec.Spe")
    smooth_cs = np.convolve(counts_cs, np.ones(5) / 5, mode='same')

    peaks_cs, _ = find_peaks(smooth_cs, prominence=50)
    valid_peaks_cs = [p for p in peaks_cs if p > 100]

    if len(valid_peaks_cs) == 0:
        print("⚠️ Tidak ada peak Cs-137 yang valid terdeteksi.")
    else:
        peak_cs137 = max(valid_peaks_cs, key=lambda p: smooth_cs[p])
        print(f"✅ Peak Cs-137 (Energi 662 keV)  terdeteksi di Channel : {peak_cs137}")

except Exception as e:
    print(f"Gagal memproses Cs-137: {e}")


# ==========================================
# 3. MENCARI PUNCAK Co-60
# ==========================================
try:
    counts_co = baca_file_spe("data/raw/BGO Co60 0deg 600sec.Spe")
    smooth_co = np.convolve(counts_co, np.ones(5) / 5, mode='same')

    peaks_co, _ = find_peaks(smooth_co, prominence=30)
    valid_peaks_co = [p for p in peaks_co if p > 100]

    top_2_co = sorted(valid_peaks_co, key=lambda p: smooth_co[p], reverse=True)[:2]
    top_2_co.sort()

    if len(top_2_co) >= 1:
        print(f"✅ Peak Co-60 1 (Energi 1173 keV) terdeteksi di Channel : {top_2_co[0]}")
    else:
        print("⚠️ Peak Co-60 pertama belum terdeteksi.")

    if len(top_2_co) >= 2:
        print(f"✅ Peak Co-60 2 (Energi 1332 keV) terdeteksi di Channel : {top_2_co[1]}")
    else:
        print("⚠️ Peak Co-60 kedua belum terdeteksi dengan parameter saat ini.")

except Exception as e:
    print(f"Gagal memproses Co-60: {e}")
