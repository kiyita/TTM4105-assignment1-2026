import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from numpy import pi
from scripts.binary_generator import gen_binary_array

def generate_fdma_signal(symbol_duration, simulation_time, users):
    sample_rate = 1000
    t = np.arange(0, simulation_time, 1/sample_rate)
    num_of_samples_per_symbol = sample_rate*symbol_duration
    num_of_symbols =  int(np.floor(np.size(t)/num_of_samples_per_symbol))
    symbols = []
    for i in range(users):
        symbols.append(gen_binary_array(num_of_symbols, num_of_samples_per_symbol, np.random.randint(0, 10000)))


    carrier_frequency = 60 # (Hz)
    carrier_signal = np.sin(2*pi*carrier_frequency*t)
    f, ask_signal, fft_spectrum, magnitude_spectrum = [], [], [], []
    for i in range(users):
        f.append(carrier_frequency*symbols[i]*(i+1))
        ask_signal.append(np.sin(2*pi*f[i]*t[:len(f[i])]))
        fft_spectrum.append(np.fft.fft(ask_signal[i]))
        magnitude_spectrum.append(np.abs(fft_spectrum[i]))

    frequencies = np.fft.fftfreq(len(fft_spectrum[0]), d=1 / sample_rate)
    colors = list(mcolors.XKCD_COLORS.keys())
 

    # Plot the magnitude spectrum
    figure, axis = plt.subplots(users)
    axis[0].set_title("Binary digital data")
    for i in range(users):
        axis[i].plot(t[:len(symbols[i])], symbols[i], color=colors[-i])
    plt.tight_layout()
    plt.show()
    plt.figure()
    for i in range(users):
        plt.plot(frequencies, magnitude_spectrum[i], color=colors[-i])
    plt.ylim(0, 200)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("Frequency Domain Representation")
    plt.grid(True)
    plt.show()