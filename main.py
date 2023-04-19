import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess
import threading
import scipy.signal as signal

#Designate location of where audio FIFO is located
pipe_path = '/tmp/audio_pipe'

#Checks if FIFO exists, if not creates it
if not os.path.exists(pipe_path):
    print("audio_pipe does not exist, creating FIFO...")
    os.mkfifo(pipe_path)

#Sends start recording command to linux terminal
#to start recording stereo audio to the audio FIFO
def start_recording():
    print("Starting Recording")
subprocess = subprocess.Popen(["arecord", "-D", "plughw:1", "-c2", "-r", "48000", "-f", "S32_LE", "-t", "raw", "-V", "stereo", "-v", "/tmp/audio_pipe"])


start_recording()

chunk_size = 8192
fig, axs = plt.subplots(2, sharex=True)

#init decision alg variables
threshold = 0
timeSinceLast = 0
noiseSlope = 0
totalNoise = 0
sampleNum = 0
MAX_THRESH_PERIOD = 3
SHARP = 60
DEC_VAL = 1
TIME_LIT = 0.01
SOUND_STABILIZER= 200000000000000

#Define the positions of the microphones in the array
mic_positions = np.array([1/2, np.sqrt(3)/2], [1,0], [1/2, -(np.sqrt(3)/2)], [-1/2, -(np.sqrt(3))/2], [-1,0], [-1/2, np.sqrt(3)/2])

# Initialize variables for recording and processing audio data in chunks
fs = 44100  # Sampling frequency
duration = chunk_size / fs  # Duration of each chunk in seconds
n_samples = chunk_size * len(mic_positions)
signals = np.zeros((len(mic_positions), n_samples))
xcorr = np.zeros((len(mic_positions), len(mic_positions), n_samples))
delay_times = np.zeros((len(mic_positions), len(mic_positions)))
speed_of_sound = 343  # Speed of sound in meters per second
A = np.zeros((len(mic_positions) - 1, 2))
b = np.zeros((len(mic_positions) - 1,))
estimated_direction = None
estimated_distance = None
sound_source_locations = []

with open("/tmp/audio_pipe", "rb") as f:
    while True:
        print("\/")
        audio_data = f.read(chunk_size)
        audio_array = np.frombuffer(audio_data, dtype=np.int32)
        left_channel = audio_array[::2]
        right_channel = audio_array[1::2]

        # Add new samples to the end of each audio signal buffer
        for i in range(len(mic_positions)):
            signals[i, :-chunk_size] = signals[i, chunk_size:]
            signals[i, -chunk_size:] = audio_array[i::len(mic_positions)]

        # Calculate the cross-correlation between each pair of microphones
        for i in range(len(mic_positions)):
            for j in range(len(mic_positions)):
                if i != j:
                    xcorr[i, j, :] = signal.correlate(signals[i, :], signals[j, :], mode='same')

        # Find the delay times between each pair of microphones
        for i in range(len(mic_positions)):
            for j in range(len(mic_positions)):
                if i != j:
                    peak_index = np.argmax(np.abs(xcorr[i, j, :]))
                    delay_times[i, j] = (peak_index - n_samples // 2) / fs

        # Estimate the direction of the sound source using triangulation
        if np.any(delay_times != 0):
            for i in range(len(mic_positions) - 1):
                A[i, :] = mic_positions[i + 1, :] - mic_positions[0, :]
                b[i] = (delay_times[i + 1, 0] - delay_times[0, 0]) * speed_of_sound
            estimated_direction, estimated_distance = np.linalg.lstsq(A, b, rcond=None)[0]
            estimated_direction = np.rad2deg(np.arctan2(estimated_direction[1], estimated_direction[0]))

        # Calculate the x and y coordinates of the sound source
        if estimated_direction is not None:
            x = estimated_distance * np.cos(np.deg2rad(estimated_direction))
            y = estimated_distance * np.sin(np.deg2rad(estimated_direction))
            sound_source_locations.append((x,y))
        

        #phase angle alg here - used for LED output decisions
        
        #get average sound
        avg_right = np.average(right_channel)
        avg_left = np.average(left_channel)
        avg_sound = (avg_right * avg_left) / SOUND_STABILIZER

        #this is currently just the pythagorean theorem
        angle_dir = np.sqrt( np.sqare(avg_right) + np.square(avg_left))

        #decision alg goes here

        #get average sound
        avg_right = np.average(right_channel)
        avg_left = np.average(left_channel)
        avg_sound = (avg_right * avg_left) / SOUND_STABILIZER
        
        print(avg_sound)
        
        #time since last noise - if longer than threshold, lower threshold
        if timeSinceLast > MAX_THRESH_PERIOD:
            threshold -= DEC_VAL
        
        #if the audio value is extremely sharp, color differently
        #plot out the information
        #use phase-angle to get the direction of the sound
        if avg_sound >= SHARP:
            axs[0].clear()
            axs[0].plot(left_channel, color = "red")
            axs[1].clear()
            axs[1].plot(right_channel, color = "red")
            plt.pause(TIME_LIT)
        else:
            #if the audio value is lower than threshold, ignore
            if avg_sound > threshold:
                axs[0].clear()
                axs[0].plot(left_channel, color="green")
                axs[1].clear()
                axs[1].plot(right_channel, color="green")
                plt.pause(TIME_LIT) 

        timeSinceLast += TIME_LIT
        

