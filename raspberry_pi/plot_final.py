import numpy as np
import matplotlib.pyplot as plt

filt_A = np.load("filt_A.npy")
filt_B = np.load("filt_B.npy")

# align panjang
m = min(len(filt_A), len(filt_B))
filt_A = filt_A[:m]
filt_B = filt_B[:m]

plt.plot(filt_A, label="Cloud (A)")
plt.plot(filt_B, label="Edge (B)")

plt.legend()
plt.title("Perbandingan Filtering A vs B")
plt.xlabel("Sample")
plt.ylabel("Acceleration")

print("STD Cloud:", np.std(filt_A))
print("STD Edge :", np.std(filt_B))
print("Mean diff:", np.mean(np.abs(filt_A - filt_B)))

plt.show()