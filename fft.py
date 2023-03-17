from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt

def pdm_to_fft(data):
    t = np.linspace(0,1,1024)
    fft = np.fft.fft(data)
    fft_mag = np.abs(fft)
    fft_freq = np.fft.fftfreq(len(data), t[0] - t[1])
    return fft_mag, fft_freq