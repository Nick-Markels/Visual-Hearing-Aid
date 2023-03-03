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

fig, axs = plt.subplots(8, sharex=True)
fig.suptitle('Channels')

channel_arrays = [[] for _ in range(RESPEAKER_CHANNELS)]

for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    decoded = np.fromstring(data, "int16")
    decoded = decoded.string((8, CHUNK))
    split = np.split(decoded, 8)
    ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8 = split
    axs[0].clear()
    axs[1].clear()
    axs[2].clear()
    axs[3].clear()
    axs[5].clear()
    axs[6].clear()
    axs[6].clear()
    axs[0].plot(ch1)
    axs[1].plot(ch2)
    axs[2].plot(ch3)
    axs[3].plot(ch4)
    axs[4].plot(ch5)
    axs[5].plot(ch6)
    axs[6].plot(ch7)
    axs[7].plot(ch8)
  
    plt.pause(0.0000625)

  
 
print("* done recording")
 
stream.stop_stream()
stream.close()
p.terminate()

