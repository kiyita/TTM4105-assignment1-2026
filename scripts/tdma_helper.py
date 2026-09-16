import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from numpy import pi
from scripts.binary_generator import gen_binary_array

def generate_tdma_signal(simulation_time, symbol_duration, users):
    carrier_frequency = users*2/symbol_duration # (Hz)
    sample_rate = int(users*200/symbol_duration)
    t = np.arange(0, simulation_time, 1/sample_rate)
    num_of_samples_per_symbol = sample_rate*symbol_duration
    num_of_symbols =  int(np.floor(np.size(t)/num_of_samples_per_symbol))
    symbols = []
    for i in range(users):
        symbols.append(gen_binary_array(num_of_symbols, num_of_samples_per_symbol, np.random.randint(0, 10000)))
    simulation_time = simulation_time // 1
    sum_symbols = []
    for second in range(simulation_time):
        start_index = second * sample_rate
        end_index = (second + 1) * sample_rate
        for i in range(users):
            sum_symbols = np.concatenate((sum_symbols, symbols[i][start_index:end_index:users]))
    carrier_frequency = 150*users*symbol_duration # (Hz)
    carrier_signal = np.sin(2*pi*carrier_frequency*t)
    f_1 = carrier_frequency*symbols[0]
    ask_signal_1 = np.sin(2*pi*f_1*t[:len(f_1)])
    f = carrier_frequency*sum_symbols
    ask_signal = np.sin(2*pi*f*t[:len(f)])

    colors = list(mcolors.XKCD_COLORS.keys())
    # Binary waveform and PSK modulation waveform Plots
    figure, axis = plt.subplots(users+1, constrained_layout=True) # Change to 6 if you want to plot the PSK modulated signal
    axis[0].set_title("Binary digital data")
    for i in range(users):
            axis[i].plot(t[:len(symbols[i])], symbols[i], color=colors[-i])
    axis[users].plot(t[:len(ask_signal_1)], ask_signal_1, color=colors[-0])
    axis[users].set_title("ASK modulated signal of first data signal")
    plt.show()
    figure, axis = plt.subplots(2, constrained_layout=True) # Change to 6 if you want to plot the PSK modulated signal
    for second in range(simulation_time):
        for i in range(users):  # Iterate over the 4 TDMA slots
            start = second * sample_rate + i * (sample_rate // users)
            end = second * sample_rate + (i + 1) * (sample_rate // users)
            if len(t[start:end]) == len(sum_symbols[start:end]):
                axis[0].plot(t[start:end], sum_symbols[start:end], color=colors[-i])
                axis[1].plot(t[start:end], ask_signal[start:end], color=colors[-i])
            else:
                axis[0].plot(t[start:start+len(sum_symbols[start:end])], sum_symbols[start:end], color=colors[-i])
                axis[1].plot(t[start:start+len(sum_symbols[start:end])], ask_signal[start:end], color=colors[-i])
    axis[0].set_title("Combined TDM signal")
    axis[1].set_title("ASK modulated TDM-signal")
    axis[1].set_xlabel("Time")
    axis[1].set_ylabel("Amplitude")
    plt.show()