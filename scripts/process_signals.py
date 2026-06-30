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
    print(f"--- ANALYZING: {filename} ---")
    
    try:
        data = scipy.io.loadmat(file_path)
        # SENSOR 1: Print all available keys to ensure we grab the right one
        print(f"Available keys: {list(data.keys())}")
        
        # Adjust 'data' to the correct key if needed
        if 'data' in data:
            raw_signal = data['data'].flatten()
        else:
            # If 'data' isn't found, pick the first array that looks like data
            # This is a fallback to find the signal automatically
            key = [k for k in data.keys() if not k.startswith('__')][0]
            raw_signal = data[key].flatten()
            print(f"Using key: {key}")

        # SENSOR 2: Print data health
        print(f"Signal stats - Min: {np.min(raw_signal)}, Max: {np.max(raw_signal)}, Mean: {np.mean(raw_signal)}")
        
        # FFT Plotting
        n = len(raw_signal)
        # If Fs is not in file, standard VLF sample rates are often 100kHz or 192kHz
        fs = 100000 
        
        plt.figure(figsize=(10, 6))
        # Use log scale (dB) to make faint signals visible
        plt.magnitude_spectrum(raw_signal, Fs=fs, scale='dB')
        plt.title(f"Spectral Scan: {filename}")
        plt.grid(True)
        
        plt.savefig(os.path.join(results_dir, f"scan_{filename}.png"))
        plt.close()
        print("Visualization saved successfully.")
        
    except Exception as e:
        print(f"Error processing {filename}: {e}")
