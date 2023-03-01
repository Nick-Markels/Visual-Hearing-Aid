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
 
frames = []
 
for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
 
print("* done recording")
 
stream.stop_stream()
stream.close()
p.terminate()
 
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(RESPEAKER_CHANNELS)
wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
wf.setframerate(RESPEAKER_RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Convert frames to NumPy array
samples = np.frombuffer(b''.join(frames), dtype=np.int16)

# Reshape data into an array of shape (num_channels, CHUNK)
num_channels = 8
samples_per_channel = len(samples) // num_channels
samples = samples.reshape((num_channels, samples_per_channel))

# Plot each channel's waveform
fig, axs = plt.subplots(num_channels, 1, figsize=(8, 6), sharex=True)
for i in range(num_channels):
    axs[i].plot(samples[i])
    axs[i].set_ylabel(f"Channel {i}")
axs[-1].set_xlabel("Sample index")
plt.tight_layout()

# Save plot to file
plt.savefig("output.png")
