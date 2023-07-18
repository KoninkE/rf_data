# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 10:02:57 2023

@author: ellio
"""

import FSK_gen, APSK_gen
import radio_aid
import numpy as np
import os
import random
from math import ceil
from itertools import cycle, islice
# import gnuradio as gnu

def randSubstet(dataSet, wordData, subsetSize):
    subset = []
    words = []
    
    for i in range(0, subsetSize):
        r = random.randint(0, len(dataSet) - 1)
        subset.append(dataSet[r])
        words.append(wordData[r])
        
    return subset, words

# generates the On-Off Keying Modulation
def genOOK(data, carrierFreq, sampleRate, symbolRate):
    groupedBits = radio_aid.groupBits(data, 1)
    symbols = APSK_gen.mapSymbols(groupedBits, mod="OOK")
    inPhase, quadPhase = APSK_gen.apskModulation(symbols, sampleRate, symbolRate)
    return inPhase, quadPhase

# generates the 2-Ampitude Shift Keying Modulation
def genASK2(data, carrierFreq, sampleRate, symbolRate):
    groupedBits = radio_aid.groupBits(data, 1)
    symbols = APSK_gen.mapSymbols(groupedBits, mod="2ASK")
    inPhase, quadPhase = APSK_gen.apskModulation(symbols, sampleRate, symbolRate)
    return inPhase, quadPhase

# generates the 4-Ampitude Shift Keying Modulation
def genASK4(data, carrierFreq, sampleRate, symbolRate):
    groupedBits = radio_aid.groupBits(data, 2)
    symbols = APSK_gen.mapSymbols(groupedBits, mod="4ASK")
    inPhase, quadPhase = APSK_gen.apskModulation(symbols, sampleRate, symbolRate)
    return inPhase, quadPhase

def genFSK2(data, carriers, sampleRate, symbolRate):
    groupedBits = radio_aid.groupBits(data, 1)
    return FSK_gen.modulateFSK2(groupedBits, carriers, sampleRate, symbolRate)

def genFSK4(data, carriers, sampleRate, symbolRate):
    groupedBits = radio_aid.groupBits(data, 2)
    return FSK_gen.modulateFSK4(groupedBits, carriers, sampleRate, symbolRate)

# generates the Binary Phase Shift Keyig Modulation
def genBPSK(data, carrierFreq, sampleRate, symbolRate):
    groupedBits = radio_aid.groupBits(data, 1)
    symbols = APSK_gen.mapSymbols(groupedBits, mod="BPSK")
    inPhase, quadPhase = APSK_gen.apskModulation(symbols, sampleRate, symbolRate)
    return inPhase, quadPhase

# generates the Quadrature Phase Shift Keying Modulation
def genQPSK(data, carrierFreq, sampleRate, symbolRate):
    groupedBits = radio_aid.groupBits(data, 2)
    symbols = APSK_gen.mapSymbols(groupedBits, mod="QPSK")
    inPhase, quadPhase = APSK_gen.apskModulation(symbols, sampleRate, symbolRate)
    return inPhase, quadPhase

# generates the 16-Phase Shift Keying Modulation
def genPSK16(data, carrierFreq, sampleRate, symbolRate):
    groupedBits = radio_aid.groupBits(data, 4)
    symbols = APSK_gen.mapSymbols(groupedBits, mod="16PSK")
    inPhase, quadPhase = APSK_gen.apskModulation(symbols, sampleRate, symbolRate)
    return inPhase, quadPhase

# generates the 16-Quadrature Amplitude Modulation
def genQAM16(data, carrierFreq, sampleRate, symbolRate):
    groupedBits = radio_aid.groupBits(data, 4)
    symbols = APSK_gen.mapSymbols(groupedBits, mod="16QAM")
    inPhase, quadPhase = APSK_gen.apskModulation(symbols, sampleRate, symbolRate)
    return inPhase, quadPhase

# creates folders in base directory if they don't already exists
def checkPath(basePath, carriers):
    modulationExtensions = ['\OOK', '\ASK2', '\ASK4', '\FSK2', '\FSK4', '\BPSK', '\QPSK', '\PSK16', '\QAM16']
    carrierExtensions = ['\\' + str(carrier) for carrier in carriers]
    
    for mod in modulationExtensions:
        if(os.path.exists(basePath + mod) == False):
            os.makedirs(basePath + mod)
        for carrier in carrierExtensions:
            if(os.path.exists(basePath + mod + carrier) == False):
                os.makedirs(basePath + mod + carrier)

def writeAPSK(path, iqData, sampleRate, carrier, extendLen = -1):
    inPhase = iqData[0]
    quadPhase = iqData[1]
    
    times = np.arange(0, (1 / sampleRate) * len(inPhase), 1 / sampleRate)
    
    if(len(times) > len(inPhase)):
        times = times[0:-1]
    elif(len(times) < len(inPhase)):
        times = np.append(times, (1 / sampleRate) + times[-1])
    
    iSig = inPhase * np.sin(2 * np.pi * carrier * times)
    qSig = quadPhase * np.cos(2 * np.pi * carrier * times)
    
    if(extendLen > len(iSig)):
        iSig = extendSig(iSig, extendLen)
        qSig = extendSig(qSig, extendLen)
    
    radio_aid.writeToWav(path, iSig, qSig, sampleRate)
    
def writeFSK(path, iqData, sampleRate, extendLen = -1):
    iSig = iqData[0]
    qSig = iqData[1]
    
    if(extendLen > len(iSig)):
        iSig = extendSig(iSig, extendLen)
        qSig = extendSig(qSig, extendLen)
    
    radio_aid.writeToWav(path, iSig, qSig, sampleRate)
    
def genPath(basePath, modulation, carrierFreq, word):
    wordIter = 1
    
    while(os.path.exists(basePath + modulation + '\\' + str(carrierFreq) + '\\' + word + str(wordIter) + '.csv') == True):
        wordIter += 1
        
    # globalPath = basePath + modulation + '\\' + str(carrierFreq) + '\\' + word + str(wordIter) + '.wav'
    globalPath = basePath + modulation + '\\' + str(carrierFreq) + '\\' + word + str(wordIter) + '.csv'
                   
    return globalPath

# repeats the signal so it is of a certain length
def extendSig(sig, totLen):
    newSig = list(islice(cycle(sig), totLen))
    return newSig

def dataset_gen(bitData, wordData, carrierFreqs, sigsPerCarrier, basePath, symbolRate, fskOffset, SNRs=[], sampleRate = -1):
    if(sampleRate == -1):
        sampleRate = max(carrierFreqs) * 15
    
    checkPath(basePath, carrierFreqs)
    
    extendLength = ceil((sampleRate / symbolRate) * len(max(bitData, key=len)))
    
    for carrier in carrierFreqs:
        for i in range(0, sigsPerCarrier):
            
            data, words = randSubstet(bitData, wordData, 9)

            # generate OOK signal and save it to csv file
            path = genPath(basePath, '\OOK', carrier, words[0])
            # iSig, qSig = genOOK(data[0], carrier, sampleRate, symbolRate)
            writeAPSK(path, genOOK(data[0], carrier, sampleRate, symbolRate), sampleRate, carrier, extendLen=extendLength)

            # generate 2-ASK signal and save it to csv file
            path = genPath(basePath, '\ASK2', carrier, words[1])
            # iSig, qSig = genASK2(data[1], carrier, sampleRate, symbolRate)
            writeAPSK(path, genASK2(data[1], carrier, sampleRate, symbolRate), sampleRate, carrier, extendLen=extendLength)

            # generate 4-ASK signal and save it to csv file
            path = genPath(basePath, '\ASK4', carrier, words[2])
            # iSig, qSig = genASK4(data[2], carrier, sampleRate, symbolRate)
            writeAPSK(path, genASK4(data[2], carrier, sampleRate, symbolRate), sampleRate, carrier, extendLen=extendLength)

            # generate BPSK signal and save it to csv file
            path = genPath(basePath, '\BPSK', carrier, words[3])
            # iSig, qSig = genBPSK(data[3], carrier, sampleRate, symbolRate)
            writeAPSK(path, genBPSK(data[3], carrier, sampleRate, symbolRate), sampleRate, carrier, extendLen=extendLength)

            # generate QPSK signal and save it to csv file
            path = genPath(basePath, '\QPSK', carrier, words[4])
            # iSig, qSig = genQPSK(data[4], carrier, sampleRate, symbolRate)
            writeAPSK(path, genQPSK(data[4], carrier, sampleRate, symbolRate), sampleRate, carrier, extendLen=extendLength)

            # generate 16-PSK signal and save it to csv file
            path = genPath(basePath, '\PSK16', carrier, words[5])
            # iSig, qSig = genPSK16(data[5], carrier, sampleRate, symbolRate)
            writeAPSK(path, genPSK16(data[5], carrier, sampleRate, symbolRate), sampleRate, carrier, extendLen=extendLength)

            # generate 16-QAM signal and save it to csv file
            path = genPath(basePath, '\QAM16', carrier, words[6])
            # iSig, qSig = genQAM16(data[6], carrier, sampleRate, symbolRate)
            writeAPSK(path, genQAM16(data[6], carrier, sampleRate, symbolRate), sampleRate, carrier, extendLen=extendLength)

            # generate 2-FSK signal and save it to csv file
            carriers = [carrier, carrier + fskOffset]
            path = genPath(basePath, '\FSK2', carrier, words[7])
            # iSig, qSig = genFSK2(data[7], carriers, sampleRate, symbolRate)
            writeFSK(path, genFSK2(data[7], carriers, sampleRate, symbolRate), sampleRate, extendLen=extendLength)

            # generate 4-FSK signal and save it to csv file
            carriers = [carrier + (i * fskOffset) for i in range(0, 4)]
            path = genPath(basePath, '\FSK4', carrier, words[8])
            # iSig, qSig = genFSK4(data[8], carriers, sampleRate, symbolRate)
            writeFSK(path, genFSK4(data[8], carriers, sampleRate, symbolRate), sampleRate, extendLen=extendLength)
    

bitPath = r"C:\Users\ellio\Programs\Datasets\Radio Dataset\rand_bits.txt"
wordPath = r"C:\Users\ellio\Programs\Datasets\Radio Dataset\rand_words.txt"
basePath = r"C:\Users\ellio\Programs\Datasets\Radio Dataset\wav_files"
bitData = radio_aid.convToFloat(radio_aid.readBitArray(bitPath), 2)
wordData = radio_aid.readWordArray(wordPath)

# carrierFreqs = [902500000, 905000000, 907500000, 910000000, 912500000, 915000000, 917500000, 922500000, 925000000]
carrierFreqs = [5000000, 10000000, 50000000, 75000000, 100000000, 200000000, 500000000, 750000000, 900000000]
dataset_gen(bitData, wordData, carrierFreqs, 25, basePath, 250000000, 100000)
    
