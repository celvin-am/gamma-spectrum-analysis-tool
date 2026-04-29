import numpy as np
import pandas as pd

# Membuat data channel (0 sampai 1023)
channels = np.arange(0, 1024)

# Membuat pola spektrum radiasi Cs-137 tiruan yang realistis
counts = 1000 * np.exp(-channels / 200) # Background (radiasi alam)
counts += 200 / (1 + np.exp((channels - 477) / 10)) # Compton edge
counts += 1500 * np.exp(-0.5 * ((channels - 662) / 5)**2) # Photopeak Cs-137 di channel 662

# Menambahkan noise (fluktuasi detektor asli)
np.random.seed(42)
counts = np.random.poisson(counts)

# Menyimpan ke dalam file CSV
df = pd.DataFrame({'Channel': channels, 'Counts': counts})
df.to_csv('Cs-137_Spectrum_Real.csv', index=False)
print("File Cs-137_Spectrum_Real.csv berhasil dibuat!")