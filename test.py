import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
 
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 8 
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 2  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
 
p = pyaudio.PyAudio()
 
stream = p.open(
            rate=RESPEAKER_RATE,
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,)
 
print("* recording")

fig, axs = plt.subplots(RESPEAKER_CHANNELS, sharex=True, sharey=True, figsize=(8,8))
fig.suptitle('Channels')

channel_arrays = [[] for _ in range(RESPEAKER_CHANNELS)]

for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    audio_array = np.frombuffer(data, dtype=np.int16)
    audio_array = audio_array.reshape((CHUNK, RESPEAKER_CHANNELS))
    
    for j in range(RESPEAKER_CHANNELS):
        channel_arrays[j].append(audio_array[:, j])
        axs[j].plot(audio_array[:, j], linewidth=0.5)
 
print("* done recording")
 
stream.stop_stream()
stream.close()
p.terminate()

channel1, channel2, channel3, channel4, channel5, channel6, channel7, channel8 = [np.concatenate(channel_arrays[i]) for i in range(RESPEAKER_CHANNELS)]

# Plot each channel separately
plt.figure(figsize=(8, 8))
plt.subplot(8, 1, 1)
plt.plot(channel1)
plt.title("Channel 1")
plt.subplot(8, 1, 2)
plt.plot(channel2)
plt.title("Channel 2")
plt.subplot(8, 1, 3)
plt.plot(channel3)
plt.title("Channel 3")
plt.subplot(8, 1, 4)
plt.plot(channel4)
plt.title("Channel 4")
plt.subplot(8, 1, 5)
plt.plot(channel5)
plt.title("Channel 5")
plt.subplot(8, 1, 6)
plt.plot(channel6)
plt.title("Channel 6")
plt.subplot(8, 1, 7)
plt.plot(channel7)
plt.title("Channel 7")
plt.subplot(8, 1, 8)
plt.plot(channel8)
plt.title("Channel 8")
plt.tight_layout()
plt.show()
