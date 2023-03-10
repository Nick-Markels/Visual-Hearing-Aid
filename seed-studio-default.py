import pyaudio
import wave
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
    # extract channel 0 data from 8 channels, if you want to extract channel 1, please change to [1::8]
    ch0 = np.fromstring(data,dtype=np.int16)[0::8]
    ch1 = np.fromstring(data,dtype=np.int16)[1::8]
    ch2 = np.fromstring(data,dtype=np.int16)[2::8]
    ch3 = np.fromstring(data,dtype=np.int16)[3::8]
    ch4 = np.fromstring(data,dtype=np.int16)[4::8]
    ch5 = np.fromstring(data,dtype=np.int16)[5::8]
    ch6 = np.fromstring(data,dtype=np.int16)[6::8]
    ch7 = np.fromstring(data,dtype=np.int16)[7::8]
    #frames.append(a.tostring())

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