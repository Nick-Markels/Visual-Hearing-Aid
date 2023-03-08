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
myArray = []
myArray = np.array(myArray)

while True:
    data = stream.read(CHUNK, exception_on_overflow = False)
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

    tmp = np.vstack((ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7))
    #myArray = np.hstack((myArray, tmp))
    myArray = tmp

    fig, axs = plt.subplots(8, sharex=True)
    for i in range(8):
        axs[i].plot(myArray[i])
        plt.pause(0.001)

