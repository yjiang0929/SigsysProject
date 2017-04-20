import pyaudio
import wave
from scipy.io.wavfile import read,write
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend("TkAgg")

def main():
    np.set_printoptions(threshold=10000000)

    #define stream chunk
    chunk = 44100

    #open a wav format music
    f = wave.open("snowy_mono.wav","r")
    timeMatrix = read("snowy_mono.wav")
    signal = timeMatrix[1]

    # Fourier Transform of the original signal
    freqMatrix = np.fft.fft(signal[chunk*0:chunk*5])

    # Extract Magnitude and Phase plane from frequency plan
    magMatrix = np.absolute(freqMatrix)
    phaseMatrix = np.angle(freqMatrix)

    # Inverse fourier transform back into time domain
    encodedSignal = np.fft.ifft(freqMatrix)
    encodedSignal = np.int16(encodedSignal)
    # plt.plot(encodedSignal)
    # plt.show()

    # Cast encoded signal to a playable .wav file
    write("test.wav", 44100, encodedSignal)

    #instantiate PyAudio
    p = pyaudio.PyAudio()
    #open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                channels = f.getnchannels(),
                rate = f.getframerate(),
                output = True)
    #read data
    data = f.readframes(chunk)

    #play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

    #stop stream
    stream.stop_stream()
    stream.close()

    #close PyAudio
    p.terminate()

if __name__ == "__main__":
    main()
