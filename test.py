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
    audio_array = np.frombuffer(data, dtype=np.int16)
    print("length " + audio_array.len())
    frames.append(data)
 
print("* done recording")