import pyaudio
import wave
from scipy.io.wavfile import read,write
import numpy as np
import matplotlib.pyplot as plt
import math

plt.switch_backend("TkAgg")

#define stream chunk
chunk = 44100

np.set_printoptions(threshold=10000000)

def main():

    #open a wav format music
    f = wave.open("snowy_mono.wav","r")
    timeMatrix = read("snowy_mono.wav")
    timeSignal = timeMatrix[1]
    plt.plot(timeSignal)
    plt.show()
    #encode phase
    encodedTimeSignal = phaseCode(timeSignal)

    plt.plot(encodedTimeSignal)
    plt.show()

    # Cast encoded signal to a playable .wav file
    #write("test.wav", 44100, encodedSignal)

    #playMusic(f)

def phaseCode(timeSignal):
    signalLength = len(timeSignal)

    n = 4  # n is the number of signal blocks
    l = int(signalLength/n)  # l is the length of each signal block
    m = int(l/4)  # m is the lenght of the message

    timeBlocks = []  # the time domain version of each block
    freqBlocks = []  # the frequency content of each block
    magMatrices = []  # matrices of magnitude for each block
    phaseMatrices = []  # matrices of phase for each block
    phaseDeltas = []  # difference in phase between each block and the first block every freq
    encodedPhaseBlocks = []  # frequency blocks for the encoded signal
    encodedTimeBlocks = []  # time blocks for the encoded signal

    # separates timeSignal into n time blocks of length l each
    for x in range(n):
        timeBlocks.append(timeSignal[l*(x):l*(x+1)])

    for block in timeBlocks:
        # Fourier Transform of the block
        freqMatrix = np.fft.fft(block)

        # Extract Magnitude and Phase plane from frequency plan
        magMatrices.append(np.absolute(freqMatrix))
        phaseMatrices.append(np.angle(freqMatrix))

    # finds and stores all phase differences between blocks
    for x in range(1,len(phaseMatrices)):
        currentDelta = []
        for y in range(l):
            currentMatrix = phaseMatrices[x]
            previousMatrix = phaseMatrices[x-1]
            currentDelta.append(currentMatrix[y] - previousMatrix[y])
        phaseDeltas.append(currentDelta)

    # generates the phase matrix for the message
    messagePhases = generateTestMessagePhases(l)

    # puts message phase matrix into the first block
    for i in range(0,m):
        phaseMatrices[0][int(l/2)-m+i] = messagePhases[i]
        phaseMatrices[0][int(l/2)+1+i] = -messagePhases[m-1-i]

    encodedPhaseBlocks.append(phaseMatrices[0])
    encodedPhaseTotal = encodedPhaseBlocks[0]

    previousPhaseBlock = encodedPhaseBlocks[0]

    for i in range(1,n):
        currentPhaseBlock = []
        for k in range(0,l):
            currentPhaseBlock.append(previousPhaseBlock[k] + phaseDeltas[i-1][k])
        previousPhaseBlock = currentPhaseBlock
        encodedPhaseTotal = encodedPhaseTotal + currentPhaseBlock

    plt.plot(encodedPhaseBlocks[0])
    plt.show()
    plt.plot(encodedPhaseTotal)
    plt.show()

    # Inverse fourier transform back into time domain
    encodedSignal = np.fft.ifft(encodedFreqTotal)
    encodedSignal = np.int16(encodedSignal)

    return encodedSignal

def generateTestMessagePhases(l):
    messagePhases = []

    for x in range(int(l/8)):
        messagePhases.append(math.pi/2)

    for x in range(int(l/8)):
        messagePhases.append(-math.pi/2)
    return messagePhases
def playMusic(f):
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
