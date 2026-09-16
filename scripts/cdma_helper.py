import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from numpy import pi
from binary_generator import gen_binary_array

def generate_walsh_hadamard(n):
    if n == 1:
        return np.array([[1]])
    else:
        H = generate_walsh_hadamard(n // 2)
        return np.block([[H, H], [H, -H]])
# 


def generate_cdma_signal(simulation_time, symbol_duration, users):
    # Set time-array and carrier signal
    if users <= 1:
        print("Users must be 2 or more")
        return
    sample_rate = 1000#int(200 * users / symbol_duration)
    carrier_frequency = 800*symbol_duration # (Hz)
    num_sequences = users
    expon = 0
    while (2**expon)-users < 0:
        expon += 1
    carrier_frequency = 400*expon*symbol_duration
    walsh_hadamard_matrix = generate_walsh_hadamard(2**expon)
    chipping_sequences = walsh_hadamard_matrix[:users]
    chipping_sequences = chipping_sequences.astype(int)

    t = np.arange(0, simulation_time, 1/sample_rate)
    carrier_signal = np.sin(2*pi*carrier_frequency*t)   # signal = A * sin(2πft + φ)
    # Create binary stream of data
    num_of_samples_per_symbol = int(sample_rate*symbol_duration)
    num_of_symbols =  int(np.floor(np.size(t)/num_of_samples_per_symbol))
    symbols = []
    for i in range(users):
        symbols.append(gen_binary_array(num_of_symbols, (num_of_samples_per_symbol), np.random.randint(0, 10000))) # numofsamples //len(chipping_sequences[0]))*len(chipping_sequences[0]
    extended_chipping_sequences = []
    i = 0
    for seq in chipping_sequences:
        extended_chipping_sequences.append([])
        for j in range(num_of_symbols):
            for chip in seq:
                extended_chipping_sequences[i].extend(np.tile(chip, num_of_samples_per_symbol//len(seq)))
        i += 1
    # Generate the CDMA signal
    cdma_signal = np.zeros_like(symbols[0][:len(extended_chipping_sequences[0])])
    for i in range(num_sequences):
        cdma_signal += symbols[i][:len(extended_chipping_sequences[i])] * extended_chipping_sequences[i]
    cdma_signal_AM = cdma_signal * carrier_signal[:len(cdma_signal)]
    
    colors = list(mcolors.XKCD_COLORS.keys())

    #Binary waveform and CDMA modulation waveform Plots
    figure, axis = plt.subplots(users)
    for i in range(len(symbols)):
        axis[i].plot(t[:len(symbols[i])], symbols[i], color=colors[-i])
    axis[0].set_title("Binary digital data")
    plt.show()
    
    figure, axis = plt.subplots(users)
    for i in range(len(chipping_sequences)):
        axis[i].bar(range(len(chipping_sequences[i])), chipping_sequences[i], width=1, align='edge', edgecolor=colors[-i], facecolor='none')
        axis[i].set_ylim(-1.2, 1.2)
        axis[i].set_yticks([-1, 0, 1])
    axis[0].set_title("Chipping Sequences")
    plt.show()
    
    #Binary waveform and CDMA modulation waveform Plots
    figure, axis = plt.subplots(users)
    for i in range(len(symbols)):
        axis[i].plot(t[:len(extended_chipping_sequences[i])], symbols[i][:len(extended_chipping_sequences[i])]*extended_chipping_sequences[i], color=colors[-i])
    axis[0].set_title("Chipped data-sequences")
    plt.show()
    
    fft_spectrum = np.fft.fft(cdma_signal_AM)
    magnitude_spectrum = np.abs(fft_spectrum)
    frequencies = np.fft.fftfreq(len(fft_spectrum), d=1 / sample_rate)
    
    print("Notice that in the amplitude-modulated signal, negative chip-values will be phase-shifted 180 degrees.")
    figure, axis = plt.subplots(3)
    axis[0].plot(t[:len(cdma_signal)], cdma_signal, color='blue')
    axis[0].set_title('CDMA "data". Sum of chipped signals')
    axis[0].set_ylim(-users-0.2, users - 0.2)
    axis[0].set_yticks(range(-users, users+1))
    axis[0].yaxis.grid(True, linestyle='--', alpha=0.6)
    axis[1].plot(t[:len(cdma_signal_AM)], cdma_signal_AM, color='red')
    axis[1].set_title('Amplitude-modulated CDMA-"data"')
    axis[1].set_yticks(range(-users, users+1))
    axis[1].yaxis.grid(True, linestyle='--', alpha=0.6)
    axis[2].plot(frequencies, magnitude_spectrum, color='green')
    axis[2].set_title('Frequency spectrum of signal')
    plt.tight_layout()
    plt.show()
