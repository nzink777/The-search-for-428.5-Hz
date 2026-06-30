import os
import scipy.io
import matplotlib.pyplot as plt

# Ensure results directory exists
results_dir = 'results'
os.makedirs(results_dir, exist_ok=True)

data_dir = 'data'
files = [f for f in os.listdir(data_dir) if f.endswith('.mat')]

if not files:
    print(f"Warning: No .mat files found in {data_dir}. Pipeline exiting.")
    exit(0) # Exit cleanly, don't trigger an error

for filename in files:
    file_path = os.path.join(data_dir, filename)
    print(f"Processing {filename}...")
    
    try:
        data = scipy.io.loadmat(file_path)
        # Check if 'data' key exists, if not, list available keys
        if 'data' not in data:
            print(f"Keys in {filename}: {list(data.keys())}")
            continue
            
        raw_signal = data['data'].flatten()
        # ... (rest of your FFT and plot logic)
        plt.savefig(os.path.join(results_dir, f"scan_{filename}.png"))
        plt.close()
    except Exception as e:
        print(f"Failed to process {filename}: {e}")
