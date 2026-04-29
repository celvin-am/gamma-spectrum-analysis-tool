import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. TITIK KALIBRASI ENERGI
# ==========================================
# Cs-137: 662 keV pada channel 338
# Co-60 : 1173.2 keV pada channel 594
channels = np.array([338, 594])
energi = np.array([662.0, 1173.2])

# ==========================================
# 2. REGRESI LINEAR: Energi = m * Channel + c
# ==========================================
m, c = np.polyfit(channels, energi, 1)

print("=== HASIL KALIBRASI ENERGI ===")
print(f"Nilai m (slope)      : {m:.4f}")
print(f"Nilai c (intercept)  : {c:.4f}")
print(f"Rumus Kalibrasi      : Energi (keV) = ({m:.4f} * Channel) + {c:.4f}")


# ==========================================
# 3. FUNGSI PEMBACA FILE .Spe
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


# ==========================================
# 4. TERAPKAN KALIBRASI KE SPEKTRUM Cs-137
# ==========================================
try:
    counts_cs = baca_file_spe("data/raw/BGO Cs137 0deg 300sec.Spe")
    channel_asli = np.arange(len(counts_cs))

    energi_terkalibrasi = (m * channel_asli) + c

    plt.figure(figsize=(10, 6))
    plt.plot(
        energi_terkalibrasi,
        counts_cs,
        linewidth=1.5,
        label="Spektrum Cs-137"
    )

    plt.axvline(
        662,
        linestyle="--",
        linewidth=2,
        label="Referensi Cs-137 662 keV"
    )

    plt.title("Spektrum Gamma Cs-137 Terkalibrasi Energi")
    plt.xlabel("Energi (keV)")
    plt.ylabel("Counts")
    plt.xlim(0, 1500)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

except Exception as e:
    print(f"Gagal memuat atau memproses file Cs-137: {e}")
