import pyaudio
import wave
from scipy.io.wavfile import read,write
import numpy as np
import matplotlib.pyplot as plt
import random
import math

plt.switch_backend("TkAgg")

#define stream chunk
chunk = 44100

np.set_printoptions(threshold=10000000)

def main():

    #open a wav format music
    timeMatrix = read("snowy_clip.wav")
    timeSignal = timeMatrix[1]
    # plt.plot(timeSignal)
    # plt.show()
    #encode phase
    encodedTimeSignal = phaseCode(timeSignal)

    # plt.plot(encodedTimeSignal)
    # plt.show()

    # Cast encoded signal to a playable .wav file
    write("test.wav", 44100, encodedTimeSignal)

    # f = wave.open("snowy_mono.wav","r")
    # playMusic(f)

def matrixAppend(mat1, mat2):
    try:
        mat1 = np.vstack((mat1,mat2))
    except:
        mat1 = np.concatenate((mat1,mat2))
    return mat1

def phaseCode(timeSignal):
    signalLength = len(timeSignal)

    num_blocks = 5  # n is the number of signal blocks
    block_length = int(signalLength/num_blocks)  # l is the length of each signal block
    message_length = int(block_length/8)  # m is the lenght of the message

    timeBlocks = np.array([])  # the time domain version of each block
    freqBlocks = np.array([])  # the frequency content of each block
    magMatrices = np.array([])  # matrices of magnitude for each block
    phaseMatrices = np.array([])  # matrices of phase for each block
    phaseDeltas = np.array([])  # difference in phase between each block and the first block every freq
    encodedPhaseBlocks = np.array([])  # frequency blocks for the encoded signal
    encodedTimeBlocks = np.array([])  # time blocks for the encoded signal
    encodedFreqTotal = np.array([]) # full encoded frequency signal

    # separates timeSignal into n time blocks of length l each
    for x in range(num_blocks):
        timeBlocks = matrixAppend(timeBlocks,timeSignal[block_length*(x):block_length*(x+1)])

    for block in timeBlocks:
        # Fourier Transform of the block
        freqMatrix = np.fft.fft(block)

        # Extract Magnitude and Phase plane from frequency plane
        magMatrices = matrixAppend(magMatrices, np.absolute(freqMatrix))
        phaseMatrices = matrixAppend(phaseMatrices, np.angle(freqMatrix))

    # finds and stores all phase differences between blocks
    for x in range(1,len(phaseMatrices)):
        currentDelta = []
        for y in range(block_length):
            currentMatrix = phaseMatrices[x]
            previousMatrix = phaseMatrices[x-1]
            currentDelta = np.append(currentDelta, currentMatrix[y] - previousMatrix[y])
        phaseDeltas = matrixAppend(phaseDeltas, currentDelta)
    print("Phase Difference Captured")

    # generates random message for the phase
    messagePhases = generateTestMessagePhases(block_length)

    # puts message phase matrix into the first block
    for i in range(0,message_length):
        phaseMatrices[0][int(block_length/2)-message_length+i] = messagePhases[i]
        phaseMatrices[0][int(block_length/2)+1+i] = -messagePhases[message_length-1-i]

    # add phase difference to every other phase segment
    encodedPhaseBlocks = matrixAppend(encodedPhaseBlocks, phaseMatrices[0])
    previousPhaseBlock = encodedPhaseBlocks
    for i in range(1,num_blocks):
        currentPhaseBlock = np.array([])
        for k in range(0,block_length):
            currentPhaseBlock = np.append(currentPhaseBlock, previousPhaseBlock[k] + phaseDeltas[i-1][k])
        previousPhaseBlock = currentPhaseBlock
        encodedPhaseBlocks =matrixAppend(encodedPhaseBlocks, currentPhaseBlock)

    # plot the first phase segment
    plt.plot(encodedPhaseBlocks[0])
    plt.show()

    # combine phase and magnitude blocks into frequency blocks
    for i in range(num_blocks):
        encodedFreqBlock = np.array([])
        for j in range(block_length):
            encodedFreqBlock = np.append(encodedFreqBlock, magMatrices[i][j] * (math.cos(encodedPhaseBlocks[i][j])+ 1j * math.sin(encodedPhaseBlocks[i][j])))
        encodedFreqTotal = np.append(encodedFreqTotal, encodedFreqBlock)
    plt.plot(encodedFreqTotal)
    plt.show()

    # Inverse fourier transform back into time domain
    encodedSignal = np.fft.ifft(encodedFreqTotal)
    encodedSignal = np.int16(encodedSignal)
    plt.plot(encodedSignal)
    plt.show()

    return encodedSignal

def generateTestMessagePhases(l):
    messagePhases = np.array([])

    for x in range(int(l/8)):
        messagePhases = np.append(messagePhases, random.choice([math.pi/2,-math.pi/2]))

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
