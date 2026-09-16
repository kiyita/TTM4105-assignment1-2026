import matplotlib.pyplot as plt # matplot lib is the premiere plotting lib for Python: https://matplotlib.org/
import scripts
from scripts import signal
from scripts import audio

import scipy.io.wavfile as wav
from scipy.signal import firwin, lfilter

import numpy, scipy.optimize

# Not in use
def sample_frequencies(real_world_signal1_freq, real_world_signal2_freq, real_world_signal3_freq, real_world_signal4_freq):


    total_time_in_secs = 0.2

    # Create our "real-world" continuous signals (which is obviously not possible on a digital computer, so we fake it)
    real_world_continuous_speed = 10000
    #real_world_signal1_freq = 5
    time, real_world_signal1 = scripts.signal.create_sine_wave(real_world_signal1_freq, real_world_continuous_speed, 
                                                   total_time_in_secs, return_time = True)

    #real_world_signal2_freq = 10
    real_world_signal2 = scripts.signal.create_sine_wave(real_world_signal2_freq, real_world_continuous_speed, 
                                                   total_time_in_secs)

    #real_world_signal3_freq = 20
    real_world_signal3 = scripts.signal.create_sine_wave(real_world_signal3_freq, real_world_continuous_speed, 
                                                   total_time_in_secs)

    #real_world_signal4_freq = 60
    real_world_signal4 = scripts.signal.create_sine_wave(real_world_signal4_freq, real_world_continuous_speed, 
                                                   total_time_in_secs)

    # Create the sampled versions of these continuous signals
    resample_factor = 250 # should be an integer
    sampled_time = time[::resample_factor]
    sampled_signal1 = real_world_signal1[::resample_factor]
    sampled_signal2 = real_world_signal2[::resample_factor]
    sampled_signal3 = real_world_signal3[::resample_factor]
    sampled_signal4 = real_world_signal4[::resample_factor]
    sampling_rate = real_world_continuous_speed / resample_factor
    print(f"Sampling rate: {sampling_rate} Hz")

    # Visualize the sampled versions
    fig, axes = plt.subplots(4, 1, figsize=(15,13))
    axes[0].plot(time, real_world_signal1)
    axes[0].axhline(0, color="gray", linestyle="-", linewidth=0.5)
    axes[0].plot(sampled_time, sampled_signal1, linestyle='None', alpha=0.8, marker='s', color='black')
    axes[0].vlines(sampled_time, ymin=0, ymax=sampled_signal1, linestyle='-.', alpha=0.8, color='black')
    axes[0].set_ylabel("Amplitude")
    axes[0].set_xlabel("Time (secs)")
    axes[0].set_title(f"{real_world_signal1_freq}Hz signal sampled at {sampling_rate}Hz")

    axes[1].plot(time, real_world_signal2)
    axes[1].axhline(0, color="gray", linestyle="-", linewidth=0.5)
    axes[1].plot(sampled_time, sampled_signal2, linestyle='None', alpha=0.8, marker='s', color='black')
    axes[1].vlines(sampled_time, ymin=0, ymax=sampled_signal2, linestyle='-.', alpha=0.8, color='black')
    axes[1].set_ylabel("Amplitude")
    axes[1].set_xlabel("Time (secs)")
    axes[1].set_title(f"{real_world_signal2_freq}Hz signal sampled at {sampling_rate}Hz")

    axes[2].plot(time, real_world_signal3)
    axes[2].axhline(0, color="gray", linestyle="-", linewidth=0.5)
    axes[2].plot(sampled_time, sampled_signal3, linestyle='None', alpha=0.8, marker='s', color='black')
    axes[2].vlines(sampled_time, ymin=0, ymax=sampled_signal3, linestyle='-.', alpha=0.8, color='black')
    axes[2].set_ylabel("Amplitude")
    axes[2].set_xlabel("Time (secs)")
    axes[2].set_title(f"{real_world_signal3_freq}Hz signal sampled at {sampling_rate}Hz")

    axes[3].plot(time, real_world_signal4)
    axes[3].axhline(0, color="gray", linestyle="-", linewidth=0.5)
    axes[3].plot(sampled_time, sampled_signal4, linestyle='None', alpha=0.8, marker='s', color='black')
    axes[3].vlines(sampled_time, ymin=0, ymax=sampled_signal4, linestyle='-.', alpha=0.8, color='black')
    axes[3].set_ylabel("Amplitude")
    axes[3].set_xlabel("Time (secs)")
    axes[3].set_title(f"{real_world_signal4_freq}Hz signal sampled at {sampling_rate}Hz")

    fig.tight_layout(pad = 3.0)
    
    
def frequency_sweep():
    sampling_rate, freq_sweep_44100 = sp.io.wavfile.read('data/audio/FrequencySweep_0-22050Hz_30secs.wav')
    #sampling_rate, audio_data_44100 = sp.io.wavfile.read('data/audio/greenday.wav')

    quantization_bits = 16
    print(f"{quantization_bits}-bit audio") # we assume 16 bit audio
    print(f"Sampling rate: {sampling_rate} Hz")
    print(f"Number of channels = {len(freq_sweep_44100.shape)}")
    print(f"Total samples: {freq_sweep_44100.shape[0]}")

    if len(freq_sweep_44100.shape) == 2:
        # convert to mono
        print("Converting stereo audio file to mono")
        freq_sweep_44100 = freq_sweep_44100.sum(axis=1) / 2

    # Set a zoom area (a bit hard to see but highlighted in red in spectrogram)
    xlim_zoom = (11500, 13500)
    makelab.signal.plot_signal_and_spectrogram(freq_sweep_44100, sampling_rate, quantization_bits, xlim_zoom = xlim_zoom)
    ipd.Audio(freq_sweep_44100, rate=sampling_rate)
    
    
    
    # The initial frequency guess is given by the peak frequency in the frequency domain using FFT. The fitting result is almost perfect assuming there is only one dominant frequency (other than the zero frequency peak).
    # https://stackoverflow.com/questions/16716302/how-do-i-fit-a-sine-curve-to-my-data-with-pylab-and-numpy
def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = numpy.array(tt)
    yy = numpy.array(yy)
    ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(numpy.fft.fft(yy))
    guess_freq = abs(ff[numpy.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = numpy.std(yy) * 2.**0.5
    guess_offset = numpy.mean(yy)
    guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * numpy.sin(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*numpy.pi)
    fitfunc = lambda t: A * numpy.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}
    
    
    
def sample_frequency(frequency=10, sample_rate=20, shift_wave=0):
    

    total_time_in_secs = 0.2

    # Create our "real-world" continuous signals (which is obviously not possible on a digital computer, so we fake it)
    real_world_continuous_speed = 10000
    
    # NOT SHIFTED
    #time, real_world_signal1 = scripts.signal.create_sine_wave(frequency, real_world_continuous_speed, 
    #                                               total_time_in_secs, return_time = True)
    
    # SHIFTED wave
    time, real_world_signal1 = scripts.signal.create_shifted_sine_wave(frequency, real_world_continuous_speed, 
                                                   total_time_in_secs, return_time = True, shift = shift_wave)
    
    
    # Create the sampled versions of these continuous signals
    
    #resample_factor = 250 # should be an integer
    resample_factor = round(real_world_continuous_speed / sample_rate)
    
    
    sampled_time = time[::resample_factor]
    
    sampled_signal1 = real_world_signal1[::resample_factor]
    
    sampling_rate = sample_rate
    
    print(f"Sampling rate: {sampling_rate} Hz")

    # Visualize the initial signal
    fig, axes = plt.subplots(4, 1, figsize=(15,15))
    axes[0].plot(time, real_world_signal1)
    axes[0].axhline(0, color="gray", linestyle="-", linewidth=0.5)
    # axes[0].plot(sampled_time, sampled_signal1, linestyle='None', alpha=0.8, marker='s', color='black')
    # axes[0].vlines(sampled_time, ymin=0, ymax=sampled_signal1, linestyle='-.', alpha=0.8, color='black')
    axes[0].set_ylabel("Amplitude")
    axes[0].set_xlabel("Time (secs)")
    axes[0].set_title(f"{frequency}Hz signal")
    axes[0].legend([f"Original {frequency}Hz signal"])
    
    # Visualize the sampling of the initial signal
    axes[1].plot(time, real_world_signal1)
    axes[1].plot(sampled_time, sampled_signal1, linestyle='None', alpha=0.8, marker='s', color='black')
    axes[1].vlines(sampled_time, ymin=0, ymax=sampled_signal1, linestyle='-.', alpha=0.8, color='black')
    axes[1].set_ylabel("Amplitude")
    axes[1].set_xlabel("Time (secs)")
    axes[1].set_title(f"{frequency}Hz signal sampled at {sampling_rate}Hz")
    axes[1].axhline(0, color="gray", linestyle="-", linewidth=0.5)
    axes[1].legend([f"Original {frequency}Hz signal", f"Samples at {sampling_rate}Hz"])
    
    # Reconstruct signal
    res = fit_sin(sampled_time, sampled_signal1)
    N = 100
    tt2 = numpy.linspace(0, total_time_in_secs, 10*N)
    
    # Visualize the reconstructed signal from the samples
    axes[2].plot(tt2, res["fitfunc"](tt2), "r-", label="y fit curve", linewidth=2)
    axes[2].plot(sampled_time, sampled_signal1, linestyle='None', alpha=0.8, marker='s', color='black')
    axes[2].vlines(sampled_time, ymin=0, ymax=sampled_signal1, linestyle='-.', alpha=0.8, color='black')
    axes[2].set_ylabel("Amplitude")
    axes[2].set_xlabel("Time (secs)")
    axes[2].set_title(f"{frequency}Hz signal reconstructed with a sample rate of {sampling_rate}Hz")
    axes[2].axhline(0, color="gray", linestyle="-", linewidth=0.5)
    axes[2].legend([f"Reconstructed Signal", f"Samples"])
    
    
    # Add frequency annotation to the plot
    reconstructed_frequency = res["freq"]
    axes[2].text(0.5, 0.9, f"Reconstructed Frequency: {reconstructed_frequency:.2f} Hz", 
                 transform=axes[2].transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
    
    
    # Comparison
    axes[3].plot(time, real_world_signal1)
    axes[3].plot(tt2, res["fitfunc"](tt2), "r-", label="y fit curve", linewidth=2)
    axes[3].plot(sampled_time, sampled_signal1, linestyle='None', alpha=0.8, marker='s', color='black')
    axes[3].vlines(sampled_time, ymin=0, ymax=sampled_signal1, linestyle='-.', alpha=0.8, color='black')
    axes[3].set_ylabel("Amplitude")
    axes[3].set_xlabel("Time (secs)")
    axes[3].set_title(f"Comparison")
    axes[3].axhline(0, color="gray", linestyle="-", linewidth=0.5)
    axes[3].legend([f"Original Signal", f"Reconstructed Signal"])


    fig.tight_layout(pad = 3.0)
    
def apply_fir_filter(input_file, output_file, cutoff=1000, numtaps=201):
    """
    Applies an FIR filter to a WAV file.

    Args:
        input_file (str): Path to the input WAV file.
        output_file (str): Path to the output filtered WAV file.
        cutoff (int, optional): Cutoff frequency (Hz). Defaults to 1000.
        numtaps (int, optional): Number of filter taps. Defaults to 201.
    """

    sample_rate, audio_data = wav.read(input_file)
    nyq_rate = sample_rate / 2.0

    # Create filter coefficients
    coefficients = firwin(numtaps, cutoff / nyq_rate)

    # Apply the filter
    filtered_audio = lfilter(coefficients, 1.0, audio_data)

    # Write the filtered audio (make sure output file has .wav extension)
    wav.write(output_file, sample_rate, filtered_audio.astype(numpy.int16))
    
def apply_bandpass_filter(input_file, output_file, lowcut=500, highcut=1500, numtaps=201):
    """
    Applies a bandpass FIR filter to a WAV file.

    Args:
        input_file (str): Path to the input WAV file.
        output_file (str): Path to the output filtered WAV file.
        lowcut (int, optional): Low cutoff frequency (Hz). Defaults to 500.
        highcut (int, optional): High cutoff frequency (Hz). Defaults to 1500.
        numtaps (int, optional): Number of filter taps. Defaults to 201.
    """

    sample_rate, audio_data = wav.read(input_file)
    nyq_rate = sample_rate / 2.0

    # Create filter coefficients for bandpass filter
    coefficients = firwin(numtaps, [lowcut / nyq_rate, highcut / nyq_rate], pass_zero=False)

    # Apply the filter
    filtered_audio = lfilter(coefficients, 1.0, audio_data)

    # Write the filtered audio (make sure output file has .wav extension)
    wav.write(output_file, sample_rate, filtered_audio.astype(numpy.int16))

    

def signal_quantization(input_file, output_file, quantization_bits, original_quantization=16):
    sampling_rate, audio_data = wav.read(input_file)
    print(f"Sampling rate: {sampling_rate} Hz")

    if len(audio_data.shape) == 2:
        # convert to mono
        audio_data = convert_to_mono(audio_data)
    
    length_in_secs = audio_data.shape[0] / sampling_rate
    print(f"Original {original_quantization}-bit audio ranges from -{2**(original_quantization - 1)} to {2**(original_quantization - 1) - 1}")
    
    audio_data_float = audio_data / 2**(original_quantization - 1) #
    
    
    audio_data_newbit = audio_data_float * 2**quantization_bits
    audio_data_newbit = audio_data_newbit.astype(int)
    print(f"New {quantization_bits}-bit audio ranges from -{2**(quantization_bits - 1)} to {2**(quantization_bits - 1) - 1}")
    print(f"Max value: {numpy.max(audio_data_newbit)} Avg value: {numpy.mean(audio_data_newbit):.2f}")

    return audio_data_newbit, sampling_rate



def mu_law_companding(audio_data, mu=255):
    # Apply μ-law companding
    audio_data = numpy.sign(audio_data) * numpy.log1p(mu * numpy.abs(audio_data)) / numpy.log1p(mu)
    return audio_data

def mu_law_expanding(audio_data, mu=255):
    # Apply μ-law expanding
    audio_data = numpy.sign(audio_data) * (1 / mu) * (numpy.expm1(numpy.abs(audio_data) * numpy.log1p(mu)))
    return audio_data

def signal_quantization_nonlinear(input_file, output_file, quantization_bits, original_quantization=16, mu=255):
    sampling_rate, audio_data = wav.read(input_file)
    print(f"Sampling rate: {sampling_rate} Hz")

    if len(audio_data.shape) == 2:
        # Convert to mono
        audio_data = convert_to_mono(audio_data)
    
    length_in_secs = audio_data.shape[0] / sampling_rate
    print(f"Original {original_quantization}-bit audio ranges from -{2**(original_quantization - 1)} to {2**(original_quantization - 1) - 1}")
    
    audio_data_float = audio_data / 2**(original_quantization - 1)
    
    # Apply μ-law companding
    audio_data_companded = mu_law_companding(audio_data_float, mu)
    
    # Quantize the companded signal
    audio_data_newbit = numpy.round(audio_data_companded * (2**(quantization_bits - 1) - 1))
    audio_data_newbit = audio_data_newbit.astype(int)
    print(f"New {quantization_bits}-bit audio ranges from -{2**(quantization_bits - 1)} to {2**(quantization_bits - 1) - 1}")
    print(f"Max value: {numpy.max(audio_data_newbit)} Avg value: {numpy.mean(audio_data_newbit):.2f}")

    # Apply μ-law expanding
    audio_data_expanded = mu_law_expanding(audio_data_newbit / (2**(quantization_bits - 1) - 1), mu)
    
    # Convert back to original quantization range
    audio_data_final = (audio_data_expanded * 2**(original_quantization - 1)).astype(numpy.int16)
    
    wav.write(output_file, sampling_rate, audio_data_final)
    return audio_data_final, sampling_rate



