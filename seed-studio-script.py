import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt




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

    #Calculate FFT
    fftArray = np.fft.fft(myArray)

    #Calculate 
    freqs = np.fft.fftfreq(1024, d = 1024)


    #Phase angle calculation

    #decision alg goes here

    #Calculate average sound
    avg = np.average(myArray)
    avgScaler = np.product(avg)
    avgScaler = avgScaler/SOUND_STABILIZER

     #time since last noise - if longer than threshold, lower threshold
    if timeSinceLast > MAX_THRESH_PERIOD:
        threshold -= DEC_VAL

    timeSinceLast += TIME_LIT


   #plots data
    for i in range(8):
        axs[i].clear()
        axs[i].plot(myArray[i])
    plt.pause(0.001)

