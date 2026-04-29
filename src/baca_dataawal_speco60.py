import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# ==========================================
# 1. FUNGSI UNTUK MEMBACA FILE .Spe ASLI
# ==========================================
def baca_file_spe(nama_file):
    counts = []
    in_data_block = False
    
    with open(nama_file, 'r') as file:
        for line in file:
            line = line.strip() # Menghapus spasi berlebih
            
            # Mencari tanda dimulainya data
            if line == '$DATA:':
                in_data_block = True
                continue
            
            if in_data_block:
                # Jika ketemu tanda '$' lagi, berarti blok data sudah habis
                if line.startswith('$'): 
                    break
                
                # Membaca angka
                parts = line.split()
                if len(parts) == 1: # Memastikan hanya mengambil baris yang berisi 1 angka murni
                    counts.append(int(parts[0]))
                    
    return np.array(counts)

# ==========================================
# 2. EKSEKUSI DATA
# ==========================================
# Ganti nama file ini dengan nama file .Spe yang kamu dapatkan nanti!
file_asli = "data/raw/BGO Co60 0deg 600sec.Spe" 

try:
    # Membaca counts dan membuat channel otomatis (0, 1, 2, 3...)
    counts = baca_file_spe(file_asli)
    channel = np.arange(len(counts))
    
    print(f"Berhasil membaca data! Total channel: {len(channel)}")
    
    # Visualisasi Cepat
    plt.figure(figsize=(10,5))
    plt.plot(channel, counts, color='blue', linewidth=1)
    plt.title("Spektrum Gamma Asli (Format .Spe)")
    plt.xlabel("Channel")
    plt.ylabel("Counts")
    plt.grid(True, alpha=0.3)
    plt.show()
    
except FileNotFoundError:
    print(f"File '{file_asli}' belum ada di foldermu. Silakan cari file .Spe dulu ya!")