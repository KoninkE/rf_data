import gnuradio as gnu
import numpy as np
import random
from os import listdir
import read_file as rd
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

def loadDataset(basePath):
    signals = []
    mods = []
    carriers = []

    for path in listdir(basePath):
        for folder in listdir(basePath + '\\' + path):
            for fileName in listdir(basePath + '\\' + path + '\\' + folder):
                sig, carrier, mod = rd.openCSV(basePath + '\\' + path + '\\' + folder + '\\' + fileName)
                signals.append(sig)
                mods.append(mod)
                carriers.append(carrier)

    return signals, mods, carriers

# from: https://mario-rodriguez.medium.com/channel-simulation-in-wireless-communication-with-python-code-cd4f65805192
def add_noise(signal, desired_snr):
    signal_power = sum(abs(signal) ** 2) / len(signal)
    power_dB = 10 * np.log10(signal_power)
    noise_dB = power_dB - desired_snr
    noise_val = 10 ** (noise_dB / 10)
    noise_mean = 0
    noise_std = np.sqrt(noise_val)
    noise = np.random.normal(noise_mean, noise_std, size = len(signal))

    return signal + noise

def bp_params(lowcut, highcut, sample_rate, order):
    return butter(order, [lowcut, highcut], fs=sample_rate, btype='band', analog=False)

# from: https://stackoverflow.com/questions/25191620/creating-lowpass-filter-in-scipy-understanding-methods-and-units
def bp_filter(signal, low_cut, high_cut, sample_rate, order=5):
    param_a, param_b = bp_params(low_cut, high_cut, sample_rate, order)
    return lfilter(param_b, param_a, signal)

basePath = r"C:\Users\ellio\Programs\Datasets\Radio Dataset\wav_files"

snr = 5
sampleRate = 15 * 900000000
signals, mods, carriers = loadDataset(basePath)
labels = [mods[i] + ' @\n ' + carriers[i] + ' Hz' for i in range(0, len(signals))]
filtered_sig = bp_filter(signals[0], 0.7e9, 0.95e9, sampleRate)
# noisy_sig = add_noise(signals[0], snr)

a, b = bp_params(0.7e9, 0.95e9, sampleRate, 6)
w, h = freqz(b, a, fs=sampleRate, worN=8000)
plt.plot(w, np.abs(h), 'b')
plt.show()

# plt.plot(signals[0])
# plt.title(labels[0] + " No Noise")
# plt.show()
#
# plt.plot(filtered_sig)
# plt.title(labels[0] + " Filtered")
# plt.show()
#
# plt.plot(noisy_sig)
# plt.title(labels[0] + " " + str(snr) + " SNR")
# plt.show()