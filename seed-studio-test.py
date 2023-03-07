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
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"
PNG_OUTPUT_FILENAME = "output.png"

p = pyaudio.PyAudio()

stream = p.open(
            rate=RESPEAKER_RATE,
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,)

print("* recording")

frames = [] 

for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    # extract all 8 channels using numpy
    a = np.fromstring(data,dtype=np.int16)[0::8]
    frames.append(a)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

# create a new figure
fig, axs = plt.subplots(RESPEAKER_CHANNELS, 1, figsize=(10, 15), sharex=True)

# plot each channel on its own subplot
for i in range(RESPEAKER_CHANNELS):
    axs[i].plot(frames[-1][i::RESPEAKER_CHANNELS])
    axs[i].set_ylabel("Channel {}".format(i+1))

# set the x-label on the bottom subplot
axs[-1].set_xlabel("Time (samples)")

# save the figure to a PNG file
plt.savefig(PNG_OUTPUT_FILENAME)

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(1)
wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
wf.setframerate(RESPEAKER_RATE)
wf.writeframes(b''.join(frames))
wf.close()