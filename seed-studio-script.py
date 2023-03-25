import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

#starting values
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 8 
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 2  # refer to input device id
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output.wav"

#opens audio stream
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
fig, axs = plt.subplots(8, sharex=True)


#starts infinite loop
while True:

    #reads chunk of data from audio stream
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

    #creates array of data from 8 channels
    #myArray8 = np.vstack((ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7))
    myArray = np.vstack((ch0, ch1, ch2, ch3, ch4, ch5))
    fftArray = np.fft.fft(myArray)


   
   #plots data
    for i in range(8):
        axs[i].clear()
        axs[i].plot(myArray[i])
    plt.pause(0.001)

