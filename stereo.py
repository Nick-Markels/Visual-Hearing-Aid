import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess
import threading


#location of audio stream
pipe_path = '/tmp/audio_pipe'

#checks if the path exists
if not os.path.exists(pipe_path):
    print("audio_pipe does not exist, creating FIFO...")
    os.mkfifo(pipe_path)
    
#begin recording
print("Starting Recording")
subprocess.Popen(["arecord", "-D", "plughw:1", "-c2", "-r", "48000", "-f", "S32_LE", "-t", "raw", "-V", "stereo", "-v", "/tmp/audio_pipe"])

#init plotting
chunk_size = 8192
fig, axs = plt.subplots(2, sharex=True)

with open("/tmp/audio_pipe", "rb") as f:
    while True:
        print("\/")
        audio_data = f.read(chunk_size)
        audio_array = np.frombuffer(audio_data, dtype=np.int32)
        left_channel = audio_array[::2]
        right_channel = audio_array[1::2]
       
        #decision alg goes here

        #plot out the information
        axs[0].clear()
        axs[0].plot(left_channel)
        axs[1].clear()
        axs[1].plot(right_channel)
        plt.pause(0.01)