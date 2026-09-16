import numpy as np

def gen_binary_array(Nsymbols, Nsamples, seed):
    if seed is None:
        print("You forgot to provide your student number as seed")
        return
    
    else:
        np.random.seed(seed)
    
    arr = np.random.choice([0, 1], size=Nsymbols)
    
    symbols = np.repeat(arr, Nsamples)

    return symbols