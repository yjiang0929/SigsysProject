import pyaudio
import wave

from scipy.io.wavfile import read,write
import numpy as np
import matplotlib.pyplot as plt

plt.switch_backend("TkAgg")

SIGNAL_LENGTH = 223590 # length of origin signal
NUM_BLOCKS = 10 # number of time blocks
MESSAGE_LENGTH = 215 # length of encoded message

def main():

    # open the received music clip
    timematrix = read("encoded.wav")
    timeSignal = timematrix[1]
    plt.plot(timeSignal)
    plt.show()

    # extrack encoded information
    encodedMessage = phaseDecode(timeSignal)
    print(encodedMessage)

def phaseDecode(timeSignal):
    block_length = int(SIGNAL_LENGTH / NUM_BLOCKS)
    print(block_length)

    # extract the first time block of the system
    time_block = timeSignal[0:block_length]
    encodedMessage = '0b'

    # Fourier transform of the block and extract phase plane
    freq_matrix = np.fft.fft(time_block)
    phase_matrix = np.angle(freq_matrix)
    plt.plot(phase_matrix)
    plt.show()

    for i in range(MESSAGE_LENGTH):
        count = 0
        for j in range(10):
            if phase_matrix[int(block_length/2)+(i*10+j)+1] > 0:
                count += 1
            else:
                count += -1
        if count > 0:
            encodedMessage += '0'
        else:
            encodedMessage += '1'
    unbinMessage = int(encodedMessage, 2)
    print(encodedMessage)
    textMessage = unbinMessage.to_bytes((unbinMessage.bit_length() +7)//8, 'big').decode()

    return textMessage

if __name__ == "__main__":
    main()
