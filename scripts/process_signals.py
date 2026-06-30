import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import os

def analyze_signal(mat_file_path, output_dir):
    # Load .mat file
    data = scipy.io.loadmat(mat_file_path)
    # Extract time series (usually under 'data' or similar key)
    # Assuming 'data' key exists; you may need to inspect the file structure
    raw_signal = data['data'].flatten() 
    
    # 1. FFT Analysis
    n = len(raw_signal)
    sampling_rate = 100000 # Verify this in the .mat metadata
    fft_data = np.fft.fft(raw_signal)
    freqs = np.fft.fftfreq(n, d=1/sampling_rate)
    
    # 2. Focus on the 428.5 Hz sideband relative to DHO (23.4 kHz)
    # We look for peaks at 23400 +/- 428.5
    target_sideband = 23400 - 428.5
    
    # Generate visualization
    plt.figure(figsize=(10, 6))
    plt.magnitude_spectrum(raw_signal, Fs=sampling_rate, scale='dB')
    plt.xlim(22000, 24000) # Zoom into DHO band
    plt.title(f"Spectral Scan: {os.path.basename(mat_file_path)}")
    plt.axvline(x=target_sideband, color='r', linestyle='--', label='Target 428.5 Hz Offset')
    plt.savefig(os.path.join(output_dir, f"scan_{os.path.basename(mat_file_path)}.png"))
    plt.close()

# Logic to loop through data/ directory
