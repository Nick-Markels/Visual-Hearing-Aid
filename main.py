import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess
import threading

pipe_path = '/tmp/audio_pipe'

if not os.path.exists(pipe_path):
    print("audio_pipe does not exist, creating FIFO...")
    os.mkfifo(pipe_path)

def start_recording():
    print("Starting Recording")
    subprocess.run(["arecord", "-D", "plughw:1", "-c2", "-r", "48000", "-f", "S32_LE", "-t", "raw", "-V", "stereo", "-v", "/tmp/audio_pipe"])

threading.Thread(target=start_recording).start()

chunk_size = 8192
fig, axs = plt.subplots(2, sharex=True)

with open("/tmp/audio_pipe", "rb") as f:
    while True:
        print("\/")
        audio_data = f.read(chunk_size)
        audio_array = np.frombuffer(audio_data, dtype=np.int32)
        left_channel = audio_array[::2]
        right_channel = audio_array[1::2]
        axs[0].clear()
        axs[0].plot(left_channel)
        axs[1].clear()
        axs[1].plot(right_channel)
        plt.pause(0.01)

