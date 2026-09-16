import numpy as np
import cmath


def message_and_noise_generation(bits_per_symbol, power, noise, N):
    different_angles = ((np.arange(2**bits_per_symbol)%(2**bits_per_symbol)) * (2*np.pi / (2**bits_per_symbol))) + (np.pi / (2**bits_per_symbol))
    different_values = np.array([cmath.rect(power, angle) for angle in different_angles])
    messages = ((np.random.randint(N, size = (N))%(2**bits_per_symbol)) * (2*np.pi / (2**bits_per_symbol))) + (np.pi / (2**bits_per_symbol))
    message_bits = np.array([cmath.rect(power, angle) for angle in messages])
    n = noise * (np.random.randn(N) + 1j*np.random.randn(N))/np.sqrt(2)
    combined_signal = message_bits + n
    correct_messages, wrong_messages = [], []
    for combined_value, message_bit in zip(combined_signal, message_bits):
        if different_values[np.abs(different_values - combined_value).argmin()] == message_bit:
            correct_messages.append(combined_value)
        else:
            wrong_messages.append(combined_value)
    return correct_messages, wrong_messages

def qam_target_generation(bits_per_symbol):
 #   if bits_per_symbol == 2:
  #      target_values = [np.complex128(-1-1j), np.complex128(-1+1j), np.complex128(1-1j), np.complex128(1+1j)]
   #     return target_values
    #else:
    odd_numbers = np.arange(1-((2**(bits_per_symbol/2))), (2**(bits_per_symbol/2)), 2)
    target_values = []
    for i in odd_numbers:
        for k in odd_numbers:
            target_values.append((i + 1j*k)/odd_numbers.max())
    return target_values

def qam_message_generation(target_values, power, N):
    messages = []
    for i in range(N):
        messages.append(power * target_values[np.random.randint(0, len(target_values))])
    return messages

def qam_noise_message_generation(messages, N, noise):
    n = noise * (np.random.randn(N) + 1j*np.random.randn(N))/np.sqrt(2)
    return messages + n

def qam_message_filter(target_values, messages, noisy_messages):
    correct_messages, wrong_messages = [], []
    for noisy_message, message in zip(noisy_messages, messages):
        if target_values[np.abs(target_values - noisy_message).argmin()] == message:
            correct_messages.append(noisy_message)
        else:
            wrong_messages.append(noisy_message)
    return correct_messages, wrong_messages

