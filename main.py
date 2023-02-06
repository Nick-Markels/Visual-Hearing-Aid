import matplotlib.pyplot as plt
import numpy as np

print("hello world")

chunk_size = 8192
fig, ax = plt.subplots()

with open("/tmp/audio_pipe", "rb") as f:
    while True:
        audio_data = f.read(chunk_size)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        print("t")
        ax.clear()
        ax.plot(audio_array)
        plt.pause(0.01)

