import os
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import logging

# --- CONFIGURATION (Change parameters here, not in the logic) ---
DATA_DIR = 'data'
RESULTS_DIR = 'results'
FS = 100000        # Sampling Frequency
CARRIER = 23400    # DHO Carrier Frequency
OFFSET = 428.5     # The "Genie" Offset
ZOOM_RANGE = (22900, 23000) 

# Setup logging to see errors in GitHub Actions
logging.basicConfig(level=logging.INFO)

def get_signal(mat_data):
    """Dynamically finds the signal array in the .mat file."""
    if 'data' in mat_data:
        return mat_data['data'].flatten()
    # Fallback to first non-metadata key
    for key in mat_data.keys():
        if not key.startswith('__'):
            return mat_data[key].flatten()
    raise ValueError("No signal array found in file.")

def process_phase(signal, filename):
    """Plots Time-Series for Phase data."""
    plt.plot(signal)
    plt.title(f"Phase Data: {filename}")
    plt.ylabel("Degrees")

def process_amplitude(signal, filename):
    """Plots FFT for Amplitude data with Hanning Window."""
    # Windowing
    window = np.hanning(len(signal))
    windowed = signal * window
    
    # FFT Math
    fft_data = np.fft.fft(windowed)
    freqs = np.fft.fftfreq(len(signal), 1/FS)
    
    # Extract positive side
    mask = freqs >= 0
    f_pos = freqs[mask]
    mag_pos = 20 * np.log10(np.abs(fft_data[mask]) + 1e-6)
    
    # Plotting
    plt.plot(f_pos, mag_pos)
    plt.title(f"Spectral Scan: {filename}")
    plt.xlim(ZOOM_RANGE)
    plt.axvline(x=CARRIER - OFFSET, color='r', linestyle='--', label='428.5 Hz Offset')
    plt.legend()

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.mat')]
    
    for filename in files:
        file_path = os.path.join(DATA_DIR, filename)
        try:
            data = scipy.io.loadmat(file_path)
            signal = get_signal(data)
            
            plt.figure(figsize=(10, 6))
            
            # Logic: Determine if Phase (-180 to 180) or Amplitude
            if np.max(signal) <= 180 and np.min(signal) >= -180:
                process_phase(signal, filename)
            else:
                process_amplitude(signal, filename)
            
            plt.savefig(os.path.join(RESULTS_DIR, f"scan_{filename}.png"))
            plt.close()
            logging.info(f"Successfully processed {filename}")
            
        except Exception as e:
            logging.error(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    main()
            
