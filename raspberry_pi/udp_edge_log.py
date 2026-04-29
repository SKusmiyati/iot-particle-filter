import socket
import numpy as np

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5000))

raw_list, filt_list = [], []

print("Edge logging... CTRL+C")

try:
    while True:
        data,_ = sock.recvfrom(1024)
        val = data.decode().split(",")

        raw = float(val[0])
        filt = float(val[1])

        raw_list.append(raw)
        filt_list.append(filt)

        print(f"RAW={raw:.2f} FILT={filt:.2f}")

except KeyboardInterrupt:
    np.save("raw_B.npy", raw_list)
    np.save("filt_B.npy", filt_list)
    print("\nSaved raw_B.npy, filt_B.npy")