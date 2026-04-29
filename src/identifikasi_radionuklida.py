import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import find_peaks


# ============================================================
# 1. KONFIGURASI KALIBRASI ENERGI
# ============================================================
# Hasil kalibrasi dari dua titik:
# Cs-137: channel 338 -> 662 keV
# Co-60 : channel 594 -> 1173.2 keV

M_KALIBRASI = 1.9969
C_KALIBRASI = -12.9437


# ============================================================
# 2. DATABASE REFERENSI ENERGI GAMMA
# ============================================================
DATABASE_GAMMA = [
    {
        "radionuklida": "Cs-137",
        "energi_referensi": 661.7,
        "nama_peak": "Photopeak utama Cs-137"
    },
    {
        "radionuklida": "Co-60",
        "energi_referensi": 1173.2,
        "nama_peak": "Photopeak pertama Co-60"
    },
    {
        "radionuklida": "Co-60",
        "energi_referensi": 1332.5,
        "nama_peak": "Photopeak kedua Co-60"
    }
]


# ============================================================
# 3. FUNGSI PEMBACA FILE .Spe
# ============================================================
def baca_file_spe(nama_file):
    counts = []
    in_data_block = False

    with open(nama_file, "r") as file:
        for line in file:
            line = line.strip()

            if line == "$DATA:":
                in_data_block = True
                continue

            if in_data_block:
                if line.startswith("$"):
                    break

                parts = line.split()
                if len(parts) == 1:
                    counts.append(int(parts[0]))

    if len(counts) == 0:
        raise ValueError("Data counts tidak ditemukan di dalam file .Spe.")

    channel = np.arange(len(counts))
    counts = np.array(counts)

    return channel, counts


# ============================================================
# 4. KONVERSI CHANNEL KE ENERGI
# ============================================================
def channel_ke_energi(channel):
    return (M_KALIBRASI * channel) + C_KALIBRASI


# ============================================================
# 5. DETEKSI PEAK
# ============================================================
def deteksi_peak(channel, counts, min_channel=100):
    smooth_counts = np.convolve(counts, np.ones(7) / 7, mode="same")

    area_analisis = smooth_counts[min_channel:]

    if len(area_analisis) == 0:
        raise ValueError("Area analisis kosong.")

    # Prominence dibuat dinamis tetapi tidak terlalu rendah.
    # Ini mengurangi false peak dari fluktuasi statistik.
    prominence_dinamis = max(10, 0.03 * np.max(area_analisis))

    peaks, properties = find_peaks(
        smooth_counts,
        prominence=prominence_dinamis,
        distance=15
    )

    peaks = np.array([p for p in peaks if p >= min_channel])

    hasil_peak = []

    for p in peaks:
        hasil_peak.append({
            "channel": int(channel[p]),
            "energi": float(channel_ke_energi(channel[p])),
            "counts": float(counts[p]),
            "smooth_counts": float(smooth_counts[p])
        })

    hasil_peak = sorted(
        hasil_peak,
        key=lambda x: x["smooth_counts"],
        reverse=True
    )

    return hasil_peak, smooth_counts, prominence_dinamis


# ============================================================
# 6. PENCOCOKAN PEAK DENGAN REFERENSI
# ============================================================
def cocokkan_peak_referensi(hasil_peak, toleransi_keV=10):
    """
    Setiap energi referensi hanya dicocokkan ke satu peak terdekat.
    Pendekatan ini lebih konservatif daripada mencocokkan semua peak
    yang berada di dalam rentang toleransi.
    """

    hasil_cocok = []

    for ref in DATABASE_GAMMA:
        kandidat = []

        for peak in hasil_peak:
            selisih = abs(peak["energi"] - ref["energi_referensi"])

            if selisih <= toleransi_keV:
                kandidat.append({
                    "radionuklida": ref["radionuklida"],
                    "energi_referensi": ref["energi_referensi"],
                    "nama_peak": ref["nama_peak"],
                    "energi_terdeteksi": peak["energi"],
                    "selisih_keV": selisih,
                    "channel": peak["channel"],
                    "counts": peak["counts"],
                    "smooth_counts": peak["smooth_counts"]
                })

        if len(kandidat) > 0:
            kandidat_terbaik = min(kandidat, key=lambda x: x["selisih_keV"])
            hasil_cocok.append(kandidat_terbaik)

    return hasil_cocok


# ============================================================
# 7. KESIMPULAN RADIONUKLIDA
# ============================================================
def buat_kesimpulan_radionuklida(hasil_cocok):
    """
    Aturan interpretasi:
    - Cs-137 dapat diidentifikasi jika photopeak 661.7 keV cocok.
    - Co-60 kuat jika dua photopeak 1173.2 keV dan 1332.5 keV cocok.
    - Co-60 indikatif jika hanya satu dari dua photopeak cocok.
    """

    kesimpulan = []

    energi_co60 = [
        item["energi_referensi"]
        for item in hasil_cocok
        if item["radionuklida"] == "Co-60"
    ]

    energi_cs137 = [
        item["energi_referensi"]
        for item in hasil_cocok
        if item["radionuklida"] == "Cs-137"
    ]

    if 1173.2 in energi_co60 and 1332.5 in energi_co60:
        kesimpulan.append({
            "radionuklida": "Co-60",
            "status": "Teridentifikasi kuat",
            "alasan": "Dua photopeak referensi Co-60, yaitu 1173.2 keV dan 1332.5 keV, terdeteksi."
        })
    elif 1173.2 in energi_co60 or 1332.5 in energi_co60:
        kesimpulan.append({
            "radionuklida": "Co-60",
            "status": "Indikatif",
            "alasan": "Hanya satu dari dua photopeak utama Co-60 yang terdeteksi."
        })

    if 661.7 in energi_cs137:
        kesimpulan.append({
            "radionuklida": "Cs-137",
            "status": "Teridentifikasi berdasarkan satu photopeak",
            "alasan": "Photopeak referensi Cs-137 sekitar 661.7 keV terdeteksi."
        })

    return kesimpulan


# ============================================================
# 8. TAMPILKAN HASIL
# ============================================================
def tampilkan_hasil(nama_file, hasil_peak, hasil_cocok, kesimpulan, prominence):
    print("\n============================================================")
    print("HASIL ANALISIS SPEKTRUM GAMMA")
    print("============================================================")
    print(f"File dianalisis        : {nama_file}")
    print(f"Rumus kalibrasi        : Energi (keV) = {M_KALIBRASI:.4f} * Channel + {C_KALIBRASI:.4f}")
    print(f"Prominence peak        : {prominence:.2f}")
    print(f"Jumlah peak terdeteksi : {len(hasil_peak)}")

    print("\nDAFTAR PEAK TERDETEKSI")
    print("------------------------------------------------------------")
    print(f"{'No':<4} {'Channel':<10} {'Energi (keV)':<15} {'Counts':<10}")
    print("------------------------------------------------------------")

    for i, peak in enumerate(hasil_peak, start=1):
        print(
            f"{i:<4} "
            f"{peak['channel']:<10} "
            f"{peak['energi']:<15.2f} "
            f"{peak['counts']:<10.0f}"
        )

    print("\nPEAK YANG COCOK DENGAN REFERENSI")
    print("------------------------------------------------------------")

    if len(hasil_cocok) == 0:
        print("Tidak ada peak yang cocok dengan database referensi.")
    else:
        print(
            f"{'Radionuklida':<14} "
            f"{'E Ref':<10} "
            f"{'E Deteksi':<12} "
            f"{'Selisih':<10} "
            f"{'Channel':<8}"
        )
        print("------------------------------------------------------------")

        for item in hasil_cocok:
            print(
                f"{item['radionuklida']:<14} "
                f"{item['energi_referensi']:<10.1f} "
                f"{item['energi_terdeteksi']:<12.2f} "
                f"{item['selisih_keV']:<10.2f} "
                f"{item['channel']:<8}"
            )

    print("\nKESIMPULAN IDENTIFIKASI")
    print("------------------------------------------------------------")

    if len(kesimpulan) == 0:
        print("Belum ada radionuklida yang dapat diidentifikasi secara meyakinkan.")
    else:
        for item in kesimpulan:
            print(f"- {item['radionuklida']} | {item['status']}")
            print(f"  Alasan: {item['alasan']}")


# ============================================================
# 9. SIMPAN GRAFIK
# ============================================================
def simpan_grafik(nama_file, channel, counts, smooth_counts, hasil_cocok):
    energi = channel_ke_energi(channel)

    output_dir = Path("output/figures")
    output_dir.mkdir(parents=True, exist_ok=True)

    nama_output = Path(nama_file).stem.replace(" ", "_")
    path_output = output_dir / f"identifikasi_{nama_output}.png"

    plt.figure(figsize=(10, 6))
    plt.plot(energi, counts, alpha=0.4, label="Data mentah")
    plt.plot(energi, smooth_counts, linewidth=1.5, label="Data smoothing")

    label_dipakai = set()

    for item in hasil_cocok:
        label = f"{item['radionuklida']} {item['energi_referensi']} keV"

        if label not in label_dipakai:
            plt.axvline(
                item["energi_referensi"],
                linestyle="--",
                linewidth=1,
                label=label
            )
            label_dipakai.add(label)

    plt.title(f"Identifikasi Radionuklida - {Path(nama_file).name}")
    plt.xlabel("Energi (keV)")
    plt.ylabel("Counts")
    plt.xlim(0, 1500)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path_output, dpi=300)
    plt.show()

    print(f"\nGrafik disimpan ke: {path_output}")


# ============================================================
# 10. PROGRAM UTAMA
# ============================================================
def analisis_file(nama_file):
    channel, counts = baca_file_spe(nama_file)

    hasil_peak, smooth_counts, prominence = deteksi_peak(
        channel,
        counts,
        min_channel=100
    )

    hasil_cocok = cocokkan_peak_referensi(
        hasil_peak,
        toleransi_keV=10
    )

    kesimpulan = buat_kesimpulan_radionuklida(hasil_cocok)

    tampilkan_hasil(
        nama_file,
        hasil_peak,
        hasil_cocok,
        kesimpulan,
        prominence
    )

    simpan_grafik(
        nama_file,
        channel,
        counts,
        smooth_counts,
        hasil_cocok
    )


if __name__ == "__main__":
    file_uji = [
        "data/raw/BGO Cs137 0deg 300sec.Spe",
        "data/raw/BGO Co60 0deg 600sec.Spe"
    ]

    for file in file_uji:
        analisis_file(file)
