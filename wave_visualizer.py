import pyaudio
import wave
from scipy.io.wavfile import read
import numpy

def main():
    #define stream chunk
    chunk = 44100

    #open a wav format music
    f = wave.open("snowy.wav","r")
    tm = read("snowy.wav")
    tmFile = open("timeMatrix.txt",'w')
    tempString = numpy.array_str(tm[1])
    tmFile.write(tempString)
    tmFile.close()
    print(tm)
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
