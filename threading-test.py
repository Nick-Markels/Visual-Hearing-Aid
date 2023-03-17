import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess
import threading
from scipy.fft import fft, fftfreq

pipe_path = '/tmp/audio_pipe'

if not os.path.exists(pipe_path):
    print("audio_pipe does not exist, creating FIFO...")
    os.mkfifo(pipe_path)

def start_recording():
    print("Starting Recording")
    subprocess.Popen(["arecords", "-D", "plughw:1", "-c2", "-r", "48000", "-f", "S32_LE", "-t", "raw", "-V", "stereo", "-v", "/tmp/audio_pipe"])

start_recording()

chunk_size = 8192
fig, axs = plt.subplots(2, sharex=True)

#set up frequency
N = 1024
freqs = np.fft.fftfreq(N, d = 1024)
with open("/tmp/audio_pipe", "rb") as f:
    while True:
        print("\/")
        audio_data = f.read(chunk_size)
        audio_array = np.frombuffer(audio_data, dtype=np.int32)
        left_channel = audio_array[::2]
        right_channel = audio_array[1::2]
        t = np.linspace(0,1,1024)
        left_fft = np.fft.fft(left_channel)
        right_fft = np.fft.fft(right_channel)
        left_mag = np.abs(left_fft)
        right_mag = np.abs(right_fft)
        
        axs[0].clear()
        axs[0].plot(freqs, left_mag)
        axs[1].clear()
        axs[1].plot(freqs, right_mag)
        plt.pause(0.01)

