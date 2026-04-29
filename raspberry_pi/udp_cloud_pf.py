import socket
import numpy as np
import time

# =========================
# UDP
# =========================
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5000))

# =========================
# Particle Filter Config
# =========================
N = 1000
SIGMA_PROC = 20.0   # process noise
SIGMA_MEAS = 70.0   # measurement noise (variance ~ 5000)

particles = np.random.normal(0, 100, size=N)
weights = np.ones(N) / N

# =========================
# Logging
# =========================
raw_list, filt_list, time_list = [], [], []

def particle_filter(z):
    global particles, weights

    # Predict
    particles += np.random.normal(0, SIGMA_PROC, size=N)

    # Update (Gaussian likelihood)
    diff = particles - z
    weights = np.exp(-(diff**2) / (2 * SIGMA_MEAS**2))

    sum_w = np.sum(weights)
    if sum_w < 1e-12:
        weights = np.ones(N) / N
    else:
        weights /= sum_w

    # Resample (systematic-like via choice)
    idx = np.random.choice(np.arange(N), size=N, p=weights)
    # jitter kecil untuk hindari degeneracy
    particles = particles[idx] + np.random.normal(0, 5, size=N)

    return np.mean(particles)

print("Cloud PF logging... CTRL+C to stop")

try:
    while True:
        data, _ = sock.recvfrom(1024)

        try:
            ax = float(data.decode().split(",")[0])

            t0 = time.time()
            est = particle_filter(ax)
            t1 = time.time()

            dt_ms = (t1 - t0) * 1000

            raw_list.append(ax)
            filt_list.append(est)
            time_list.append(dt_ms)

            print(f"RAW={ax:.2f}  FILT={est:.2f}  TIME={dt_ms:.3f} ms")

        except Exception as e:
            print("Parse error:", data, e)

except KeyboardInterrupt:
    np.save("raw_A.npy", raw_list)
    np.save("filt_A.npy", filt_list)
    np.save("time_A.npy", time_list)

    print("\nSaved: raw_A.npy, filt_A.npy, time_A.npy")