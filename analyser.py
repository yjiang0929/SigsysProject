import pyaudio
import wave

from scipy.io.wavfile import read,write
import numpy as np
import matplotlib.pyplot as plt

plt.switch_backend("TkAgg")

SIGNAL_LENGTH = 223591 # length of origin signal
NUM_BLOCKS = 10 # number of time blocks
MESSAGE_LENGTH = 2794 # length of encoded message

def main():

    # open the received music clip
    timematrix = read("encoded.wav")
    timeSignal = timematrix[1][0:SIGNAL_LENGTH]
    plt.plot(timeSignal)
    plt.show()

    # extrack encoded information
    encodedMessage = phaseDecode(timeSignal)
    print(encodedMessage)

def phaseDecode(timeSignal):
    block_length = int(SIGNAL_LENGTH / NUM_BLOCKS)

    # extract the first time block of the system
    time_block = timeSignal[0:block_length]
    encodedMessage = np.array([])

    # Fourier transform of the block and extract phase plane
    freq_matrix = np.fft.fft(time_block)
    phase_matrix = np.angle(freq_matrix)
    plt.plot(phase_matrix)
    plt.show()

    for i in range(MESSAGE_LENGTH):
        if phase_matrix[int(block_length/2)+1+i] > 0:
            encodedMessage = np.append(encodedMessage, [1])
        else:
            encodedMessage = np.append(encodedMessage, [0])

    return encodedMessage

if __name__ == "__main__":
    main()
