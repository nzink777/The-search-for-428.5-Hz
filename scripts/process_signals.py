import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np

results_dir = 'results'
os.makedirs(results_dir, exist_ok=True)
data_dir = 'data'
files = [f for f in os.listdir(data_dir) if f.endswith('.mat')]

for filename in files:
    file_path = os.path.join(data_dir, filename)
    data = scipy.io.loadmat(file_path)
    raw_signal = data['data'].flatten()
    
    plt.figure(figsize=(10, 6))
    
    # DECISION: Is this Phase or Amplitude?
    if np.max(raw_signal) <= 180 and np.min(raw_signal) >= -180:
        # It's Phase Data: Plot Time Series
        print(f"{filename} detected as PHASE data. Plotting time-series.")
        plt.plot(raw_signal)
        plt.title(f"Time-Series (Phase): {filename}")
        plt.ylabel("Degrees")
    else:
        # It's Amplitude Data: Plot Spectrum
        print(f"{filename} detected as AMPLITUDE data. Plotting FFT.")
        plt.magnitude_spectrum(raw_signal, Fs=100000, scale='dB')
        plt.title(f"Spectral Scan (Amplitude): {filename}")
        plt.xlim(22000, 24000) # Zoom into DHO band
        plt.axvline(x=23400 - 428.5, color='r', linestyle='--', label='428.5 Hz Sideband')

    plt.savefig(os.path.join(results_dir, f"scan_{filename}.png"))
    plt.close()
    
