import numpy as np
import matplotlib.pyplot as plt

raw = np.load("raw_A.npy")
filt = np.load("filt_A.npy")
time = np.load("time_A.npy")

plt.figure()
plt.plot(raw, label="Raw")
plt.plot(filt, label="Filtered (Cloud)")
plt.legend()
plt.title("Skenario A - Cloud Filtering")
plt.xlabel("Sample")
plt.ylabel("Acceleration")

plt.figure()
plt.plot(time)
plt.title("Processing Time (Cloud)")
plt.xlabel("Sample")
plt.ylabel("ms")

print("Average time Cloud:", np.mean(time), "ms")

plt.show()