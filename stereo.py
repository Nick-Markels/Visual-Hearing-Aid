import matplotlib.pyplot as plt
import numpy as np

print("hello world")

chunk_size = 8192
fig, axs = plt.subplots(2, sharex=True)

with open("/tmp/audio_pipe", "rb") as f:
    while True:
        audio_data = f.read(chunk_size)
        audio_array = np.frombuffer(audio_data, dtype=np.int64)
        left_channel = audio_array[::2]
        right_channel = audio_array[1::2]
        axs[0].clear()
        axs[0].plot(left_channel)
        axs[1].clear()
        axs[1].plot(right_channel)
        plt.pause(0.01)