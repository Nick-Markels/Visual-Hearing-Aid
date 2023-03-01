import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
 
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

# convert the audio data to a NumPy array
samples = np.frombuffer(b''.join(frames), dtype=np.int16)

# reshape the array to an array with shape (n_channels, -1)
samples = samples.reshape((RESPEAKER_CHANNELS, -1), order='F')

# plot each channel
t = np.arange(samples.shape[1]) / RESPEAKER_RATE
fig, axs = plt.subplots(nrows=RESPEAKER_CHANNELS, sharex=True)
for i in range(RESPEAKER_CHANNELS):
    axs[i].plot(t, samples[i])
    axs[i].set_ylabel(f'Channel {i+1}')
axs[-1].set_xlabel('Time (s)')

plt.show()

 
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(RESPEAKER_CHANNELS)
wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
wf.setframerate(RESPEAKER_RATE)
wf.writeframes(b''.join(frames))
wf.close()
