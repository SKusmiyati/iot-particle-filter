import numpy as np
import matplotlib.pyplot as plt

raw = np.load("raw_B.npy")
filt = np.load("filt_B.npy")

# samakan panjang (penting)
min_len = min(len(raw), len(filt))
raw = raw[:min_len]
filt = filt[:min_len]

plt.figure()

plt.plot(raw, label="Raw (Edge)")
plt.plot(filt, label="Filtered (Edge)")

plt.legend()
plt.title("Skenario B - Edge Filtering")
plt.xlabel("Sample")
plt.ylabel("Acceleration")

# statistik tambahan
print("STD Raw:", np.std(raw))
print("STD Filtered:", np.std(filt))
print("Noise reduction:", np.std(raw) - np.std(filt))

plt.show()