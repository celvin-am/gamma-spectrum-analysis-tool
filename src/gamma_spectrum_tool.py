"""
Gamma Spectrum Analysis Tool

Fungsi utama:
1. Membaca file spektrum gamma format .Spe.
2. Melakukan kalibrasi energi dari channel ke keV.
3. Mendeteksi photopeak pada spektrum.
4. Mengidentifikasi radionuklida berdasarkan energi gamma referensi.
5. Menyimpan grafik hasil analisis.
6. Menyimpan laporan hasil analisis dalam format TXT dan CSV.

Metode:
- Kalibrasi energi menggunakan regresi linear:
  Energi = m * Channel + c
- Peak detection menggunakan scipy.signal.find_peaks.
- Identifikasi radionuklida dilakukan secara kualitatif dengan pencocokan energi photopeak
  terhadap database energi gamma referensi.

Batasan:
- Database referensi masih terbatas pada Cs-137 dan Co-60.
- Identifikasi bersifat kualitatif, bukan kuantifikasi aktivitas.
- Program ini tidak menghitung efisiensi detektor, aktivitas, maupun ketidakpastian statistik lengkap.
"""

from pathlib import Path
import argparse
import csv

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


# ============================================================
# 1. KONFIGURASI DATA DAN OUTPUT
# ============================================================

DEFAULT_FILES = [
    "data/raw/BGO Cs137 0deg 300sec.Spe",
    "data/raw/BGO Co60 0deg 600sec.Spe",
]

OUTPUT_FIGURES_DIR = Path("output/figures")
OUTPUT_REPORTS_DIR = Path("output/reports")


# ============================================================
# 2. TITIK KALIBRASI ENERGI
# ============================================================
# Titik kalibrasi berasal dari hasil peak detection awal:
# - Cs-137: channel 338 -> 662.0 keV
# - Co-60 : channel 594 -> 1173.2 keV
#
# Dengan dua titik ini, kalibrasi linear dapat dihitung secara langsung.
# Jika nanti tersedia titik kalibrasi tambahan yang valid, array ini dapat diperluas.

CALIBRATION_CHANNELS = np.array([338, 594], dtype=float)
CALIBRATION_ENERGIES_KEV = np.array([662.0, 1173.2], dtype=float)


# ============================================================
# 3. DATABASE REFERENSI RADIONUKLIDA
# ============================================================
# Energi referensi dalam satuan keV.
# Nilai ini digunakan untuk pencocokan photopeak secara kualitatif.

GAMMA_REFERENCE_DATABASE = [
    {
        "radionuclide": "Cs-137",
        "energy_keV": 661.7,
        "peak_name": "Photopeak utama Cs-137",
        "required_for_strong_identification": 1,
    },
    {
        "radionuclide": "Co-60",
        "energy_keV": 1173.2,
        "peak_name": "Photopeak pertama Co-60",
        "required_for_strong_identification": 2,
    },
    {
        "radionuclide": "Co-60",
        "energy_keV": 1332.5,
        "peak_name": "Photopeak kedua Co-60",
        "required_for_strong_identification": 2,
    },
]


# ============================================================
# 4. FUNGSI DASAR
# ============================================================

def calculate_energy_calibration():
    """
    Menghitung koefisien kalibrasi energi linear.

    Returns
    -------
    tuple
        m, c untuk persamaan Energi = m * Channel + c
    """
    m, c = np.polyfit(CALIBRATION_CHANNELS, CALIBRATION_ENERGIES_KEV, 1)
    return float(m), float(c)


def channel_to_energy(channel, slope, intercept):
    """
    Mengubah channel menjadi energi dalam keV.
    """
    return (slope * channel) + intercept


def read_spe_file(file_path):
    """
    Membaca file spektrum gamma format .Spe.

    File .Spe biasanya memiliki blok data yang diawali oleh '$DATA:'.
    Program hanya mengambil baris numerik satu kolom setelah blok tersebut.

    Parameters
    ----------
    file_path : str or Path
        Lokasi file .Spe.

    Returns
    -------
    tuple
        channel, counts
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")

    counts = []
    in_data_block = False

    with file_path.open("r", errors="replace") as file:
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
                    try:
                        counts.append(int(parts[0]))
                    except ValueError:
                        pass

    if len(counts) == 0:
        raise ValueError(f"Tidak ada data counts yang terbaca dari file: {file_path}")

    channel = np.arange(len(counts))
    counts = np.array(counts, dtype=float)

    return channel, counts


def smooth_spectrum(counts, window_size=7):
    """
    Menghaluskan spektrum menggunakan moving average sederhana.

    Smoothing digunakan untuk mengurangi fluktuasi statistik agar peak detection
    tidak terlalu sensitif terhadap noise.
    """
    if window_size < 1:
        raise ValueError("window_size harus minimal 1.")

    kernel = np.ones(window_size) / window_size
    return np.convolve(counts, kernel, mode="same")


# ============================================================
# 5. PEAK DETECTION
# ============================================================

def detect_peaks(channel, counts, slope, intercept, min_channel=100):
    """
    Mendeteksi peak spektrum gamma.

    Parameter penting:
    - min_channel digunakan untuk mengabaikan area channel rendah yang dapat berisi
      noise elektronik atau struktur spektrum yang bukan photopeak utama.
    - prominence dibuat dinamis agar dapat menyesuaikan level counts pada spektrum.

    Returns
    -------
    tuple
        peak_list, smoothed_counts, prominence_value
    """
    smoothed_counts = smooth_spectrum(counts, window_size=7)

    if min_channel >= len(counts):
        raise ValueError("min_channel lebih besar daripada jumlah channel data.")

    analysis_area = smoothed_counts[min_channel:]

    if len(analysis_area) == 0:
        raise ValueError("Area analisis kosong.")

    # Prominence konservatif:
    # - minimal 10 counts
    # - atau 3 persen dari nilai maksimum area analisis
    prominence_value = max(10.0, 0.03 * float(np.max(analysis_area)))

    peak_indices, properties = find_peaks(
        smoothed_counts,
        prominence=prominence_value,
        distance=15
    )

    peak_indices = np.array([idx for idx in peak_indices if idx >= min_channel])

    peak_list = []

    for idx in peak_indices:
        peak_list.append({
            "channel": int(channel[idx]),
            "energy_keV": float(channel_to_energy(channel[idx], slope, intercept)),
            "counts": float(counts[idx]),
            "smoothed_counts": float(smoothed_counts[idx]),
            "prominence": float(properties["prominences"][list(peak_indices).index(idx)])
            if "prominences" in properties and len(properties["prominences"]) > 0 else None
        })

    peak_list = sorted(
        peak_list,
        key=lambda item: item["smoothed_counts"],
        reverse=True
    )

    return peak_list, smoothed_counts, prominence_value


# ============================================================
# 6. IDENTIFIKASI RADIONUKLIDA
# ============================================================

def match_reference_peaks(peak_list, tolerance_keV=10.0):
    """
    Mencocokkan peak terdeteksi terhadap database energi referensi.

    Pendekatan yang digunakan:
    - Setiap energi referensi hanya dicocokkan dengan satu peak terdekat.
    - Peak dianggap cocok jika selisih energinya <= tolerance_keV.
    - Pendekatan ini lebih konservatif daripada mencocokkan semua peak yang masuk toleransi.

    Returns
    -------
    list
        Daftar peak yang cocok dengan referensi.
    """
    matched_peaks = []

    for reference in GAMMA_REFERENCE_DATABASE:
        candidates = []

        for peak in peak_list:
            difference = abs(peak["energy_keV"] - reference["energy_keV"])

            if difference <= tolerance_keV:
                candidates.append({
                    "radionuclide": reference["radionuclide"],
                    "reference_energy_keV": reference["energy_keV"],
                    "detected_energy_keV": peak["energy_keV"],
                    "energy_difference_keV": difference,
                    "channel": peak["channel"],
                    "counts": peak["counts"],
                    "smoothed_counts": peak["smoothed_counts"],
                    "peak_name": reference["peak_name"],
                })

        if candidates:
            best_candidate = min(candidates, key=lambda item: item["energy_difference_keV"])
            matched_peaks.append(best_candidate)

    return matched_peaks


def build_radionuclide_conclusion(matched_peaks):
    """
    Menyusun kesimpulan identifikasi.

    Aturan:
    - Cs-137: dapat diidentifikasi jika photopeak 661.7 keV cocok.
    - Co-60: teridentifikasi kuat jika dua photopeak utamanya cocok.
    - Co-60: indikatif jika hanya satu dari dua photopeak utamanya cocok.
    """
    conclusions = []

    matched_by_nuclide = {}

    for item in matched_peaks:
        nuclide = item["radionuclide"]
        matched_by_nuclide.setdefault(nuclide, [])
        matched_by_nuclide[nuclide].append(item)

    for nuclide, items in matched_by_nuclide.items():
        matched_reference_energies = sorted(
            set(round(item["reference_energy_keV"], 1) for item in items)
        )

        if nuclide == "Co-60":
            has_1173 = 1173.2 in matched_reference_energies
            has_1332 = 1332.5 in matched_reference_energies

            if has_1173 and has_1332:
                status = "Teridentifikasi kuat"
                reason = (
                    "Dua photopeak utama Co-60, yaitu 1173.2 keV dan 1332.5 keV, "
                    "terdeteksi pada spektrum."
                )
            else:
                status = "Indikatif"
                reason = (
                    "Hanya satu dari dua photopeak utama Co-60 yang terdeteksi. "
                    "Identifikasi perlu dikonfirmasi dengan data atau parameter tambahan."
                )

        elif nuclide == "Cs-137":
            status = "Teridentifikasi berdasarkan satu photopeak"
            reason = (
                "Photopeak utama Cs-137 sekitar 661.7 keV terdeteksi pada spektrum."
            )

        else:
            status = "Teridentifikasi"
            reason = "Peak terdeteksi cocok dengan database referensi."

        conclusions.append({
            "radionuclide": nuclide,
            "status": status,
            "reason": reason,
            "matched_reference_energies": matched_reference_energies,
        })

    return conclusions


# ============================================================
# 7. OUTPUT TEKS
# ============================================================

def format_analysis_report(file_path, slope, intercept, prominence_value,
                           peak_list, matched_peaks, conclusions):
    """
    Membuat laporan analisis dalam bentuk string.
    """
    lines = []

    lines.append("=" * 72)
    lines.append("GAMMA SPECTRUM ANALYSIS TOOL")
    lines.append("=" * 72)
    lines.append(f"File dianalisis        : {file_path}")
    lines.append(f"Rumus kalibrasi        : Energi (keV) = {slope:.4f} * Channel + {intercept:.4f}")
    lines.append(f"Prominence peak        : {prominence_value:.2f}")
    lines.append(f"Jumlah peak terdeteksi : {len(peak_list)}")
    lines.append("")

    lines.append("DAFTAR PEAK TERDETEKSI")
    lines.append("-" * 72)
    lines.append(f"{'No':<4} {'Channel':<10} {'Energi (keV)':<15} {'Counts':<12} {'Smooth':<12}")
    lines.append("-" * 72)

    if not peak_list:
        lines.append("Tidak ada peak terdeteksi.")
    else:
        for idx, peak in enumerate(peak_list, start=1):
            lines.append(
                f"{idx:<4} "
                f"{peak['channel']:<10} "
                f"{peak['energy_keV']:<15.2f} "
                f"{peak['counts']:<12.0f} "
                f"{peak['smoothed_counts']:<12.2f}"
            )

    lines.append("")
    lines.append("PEAK YANG COCOK DENGAN REFERENSI")
    lines.append("-" * 72)

    if not matched_peaks:
        lines.append("Tidak ada peak yang cocok dengan database referensi.")
    else:
        lines.append(
            f"{'Radionuklida':<14} "
            f"{'E Ref':<10} "
            f"{'E Deteksi':<12} "
            f"{'Selisih':<10} "
            f"{'Channel':<8}"
        )
        lines.append("-" * 72)

        for item in matched_peaks:
            lines.append(
                f"{item['radionuclide']:<14} "
                f"{item['reference_energy_keV']:<10.1f} "
                f"{item['detected_energy_keV']:<12.2f} "
                f"{item['energy_difference_keV']:<10.2f} "
                f"{item['channel']:<8}"
            )

    lines.append("")
    lines.append("KESIMPULAN IDENTIFIKASI")
    lines.append("-" * 72)

    if not conclusions:
        lines.append("Belum ada radionuklida yang dapat diidentifikasi secara meyakinkan.")
    else:
        for item in conclusions:
            lines.append(f"- {item['radionuclide']} | {item['status']}")
            lines.append(f"  Alasan: {item['reason']}")

    lines.append("")

    return "\n".join(lines)


# ============================================================
# 8. SIMPAN GRAFIK DAN FILE HASIL
# ============================================================

def save_figure(file_path, channel, counts, smoothed_counts, slope, intercept,
                matched_peaks, show_plot=True):
    """
    Menyimpan grafik spektrum energi.
    """
    OUTPUT_FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    file_path = Path(file_path)
    output_name = file_path.stem.replace(" ", "_")
    output_path = OUTPUT_FIGURES_DIR / f"gamma_analysis_{output_name}.png"

    energy = channel_to_energy(channel, slope, intercept)

    plt.figure(figsize=(10, 6))
    plt.plot(energy, counts, alpha=0.4, label="Data mentah")
    plt.plot(energy, smoothed_counts, linewidth=1.5, label="Data smoothing")

    used_labels = set()

    for item in matched_peaks:
        label = f"{item['radionuclide']} {item['reference_energy_keV']} keV"

        if label not in used_labels:
            plt.axvline(
                item["reference_energy_keV"],
                linestyle="--",
                linewidth=1,
                label=label
            )
            used_labels.add(label)

    plt.title(f"Gamma Spectrum Analysis - {file_path.name}")
    plt.xlabel("Energi (keV)")
    plt.ylabel("Counts")
    plt.xlim(0, 1500)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)

    if show_plot:
        plt.show()
    else:
        plt.close()

    return output_path


def save_txt_report(file_path, report_text):
    """
    Menyimpan laporan analisis ke file TXT.
    """
    OUTPUT_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    file_path = Path(file_path)
    output_name = file_path.stem.replace(" ", "_")
    output_path = OUTPUT_REPORTS_DIR / f"gamma_analysis_{output_name}.txt"

    output_path.write_text(report_text, encoding="utf-8")

    return output_path


def save_csv_results(file_path, matched_peaks):
    """
    Menyimpan hasil identifikasi ke file CSV.
    """
    OUTPUT_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    file_path = Path(file_path)
    output_name = file_path.stem.replace(" ", "_")
    output_path = OUTPUT_REPORTS_DIR / f"gamma_analysis_{output_name}.csv"

    fieldnames = [
        "file",
        "radionuclide",
        "reference_energy_keV",
        "detected_energy_keV",
        "energy_difference_keV",
        "channel",
        "counts",
        "peak_name",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for item in matched_peaks:
            writer.writerow({
                "file": str(file_path),
                "radionuclide": item["radionuclide"],
                "reference_energy_keV": f"{item['reference_energy_keV']:.1f}",
                "detected_energy_keV": f"{item['detected_energy_keV']:.2f}",
                "energy_difference_keV": f"{item['energy_difference_keV']:.2f}",
                "channel": item["channel"],
                "counts": f"{item['counts']:.0f}",
                "peak_name": item["peak_name"],
            })

    return output_path


# ============================================================
# 9. PIPELINE ANALISIS
# ============================================================

def analyze_spectrum(file_path, tolerance_keV=10.0, min_channel=100, show_plot=True):
    """
    Menjalankan satu pipeline analisis lengkap untuk satu file .Spe.
    """
    slope, intercept = calculate_energy_calibration()

    channel, counts = read_spe_file(file_path)

    peak_list, smoothed_counts, prominence_value = detect_peaks(
        channel=channel,
        counts=counts,
        slope=slope,
        intercept=intercept,
        min_channel=min_channel,
    )

    matched_peaks = match_reference_peaks(
        peak_list=peak_list,
        tolerance_keV=tolerance_keV,
    )

    conclusions = build_radionuclide_conclusion(matched_peaks)

    report_text = format_analysis_report(
        file_path=file_path,
        slope=slope,
        intercept=intercept,
        prominence_value=prominence_value,
        peak_list=peak_list,
        matched_peaks=matched_peaks,
        conclusions=conclusions,
    )

    figure_path = save_figure(
        file_path=file_path,
        channel=channel,
        counts=counts,
        smoothed_counts=smoothed_counts,
        slope=slope,
        intercept=intercept,
        matched_peaks=matched_peaks,
        show_plot=show_plot,
    )

    txt_report_path = save_txt_report(file_path, report_text)
    csv_report_path = save_csv_results(file_path, matched_peaks)

    return {
        "file": file_path,
        "report_text": report_text,
        "figure_path": figure_path,
        "txt_report_path": txt_report_path,
        "csv_report_path": csv_report_path,
        "matched_peaks": matched_peaks,
        "conclusions": conclusions,
    }


# ============================================================
# 10. COMMAND LINE INTERFACE
# ============================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Gamma Spectrum Analysis Tool untuk analisis spektrum gamma .Spe"
    )

    parser.add_argument(
        "files",
        nargs="*",
        help=(
            "File .Spe yang akan dianalisis. "
            "Jika kosong, program memakai file default di data/raw."
        )
    )

    parser.add_argument(
        "--tolerance",
        type=float,
        default=10.0,
        help="Toleransi pencocokan energi dalam keV. Default: 10 keV."
    )

    parser.add_argument(
        "--min-channel",
        type=int,
        default=100,
        help="Channel minimum untuk analisis peak. Default: 100."
    )

    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Tidak menampilkan grafik di layar, hanya menyimpan file PNG."
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    files_to_analyze = args.files if args.files else DEFAULT_FILES
    show_plot = not args.no_show

    print("=" * 72)
    print("GAMMA SPECTRUM ANALYSIS TOOL")
    print("=" * 72)
    print(f"Jumlah file dianalisis : {len(files_to_analyze)}")
    print(f"Toleransi energi       : ±{args.tolerance:.1f} keV")
    print(f"Minimum channel        : {args.min_channel}")
    print("")

    all_results = []

    for file_path in files_to_analyze:
        try:
            result = analyze_spectrum(
                file_path=file_path,
                tolerance_keV=args.tolerance,
                min_channel=args.min_channel,
                show_plot=show_plot,
            )

            all_results.append(result)

            print(result["report_text"])
            print(f"Grafik disimpan ke : {result['figure_path']}")
            print(f"Laporan TXT        : {result['txt_report_path']}")
            print(f"Laporan CSV        : {result['csv_report_path']}")
            print("")

        except Exception as error:
            print(f"Gagal menganalisis file: {file_path}")
            print(f"Penyebab: {error}")
            print("")

    print("=" * 72)
    print("ANALISIS SELESAI")
    print("=" * 72)
    print(f"Total file berhasil dianalisis: {len(all_results)}")


if __name__ == "__main__":
    main()
