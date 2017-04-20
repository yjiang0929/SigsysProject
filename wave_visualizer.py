import pyaudio
import wave
from scipy.io.wavfile import read
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
    # tmFile = open("timeMatrix.txt",'wb')
    # numpy.savetxt(tmFile,tm[1])
    # tmFile.close()

    # plt.plot(timeMatrix[1])
    # plt.show()
    signal = timeMatrix[1]
    freqMatrix = np.fft.fft(signal[chunk*0:chunk*1])
    magMatrix = np.absolute(freqMatrix)
    phaseMatrix = np.angle(freqMatrix)
    plt.plot(phaseMatrix)
    plt.show()

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
