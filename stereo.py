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

#init decision alg variables
threshold = 0
timeSinceLast = 0
noiseSlope = 0
totalNoise = 0
sampleNum = 0
MAX_THRESH_PERIOD = 3
SHARP = 10

with open("/tmp/audio_pipe", "rb") as f:
    while True:
        print("\/")
        audio_data = f.read(chunk_size)
        audio_array = np.frombuffer(audio_data, dtype=np.int32)
        left_channel = audio_array[::2]
        right_channel = audio_array[1::2]
       
        #decision alg goes here

        #get average sound FIX
        avg_sound = (left_channel * right_channel) /2
        
        #if the audio value is lower than threshold, ignore
        for x in avg_sound:
            if x > threshold:
                #time since last noise - if longer than threshold, lower threshold
                if timeSinceLast > MAX_THRESH_PERIOD:
                    threshold -= 1
                
                #if the audio value is extremely sharp, color differently
                #plot out the information
                #use phase-angle to get the direction of the sound
                if noiseSlope >= 10:
                    axs[0].clear()
                    axs[0].plot(left_channel, color = "red")
                    axs[1].clear()
                    axs[1].plot(right_channel, color = "red")
                    plt.pause(0.01)
                else:
                    axs[0].clear()
                    axs[0].plot(left_channel, color="green")
                    axs[1].clear()
                    axs[1].plot(right_channel, color="green")
                    plt.pause(0.01)
            
            totalNoise += x
            sampleNum += 1
            noiseSlope = totalNoise / sampleNum

        timeSinceLast += 0.01
        