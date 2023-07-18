# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 13:06:59 2023

@author: ellio
"""

import numpy as np

def readWords(path, skiplines=[]):
    bitstrings = []
    words = []
    
    # open the file
    with open(path, "r") as fid:
        lineNum = 0
        
        for line in fid.readlines():
            # if the line number is in the list of lines to skip, then skip
            if(lineNum in skiplines):
                lineNum += 1
                continue
            
            string = line.split("\n")[0]
            
            if(len(string) <= 6):
                bitstrings.append(''.join(format(ord(i), '08b') for i in string))
                words.append(string)
            else:
                print('uh oh we got a goof', string, len(string))
                for i in string:
                    print(i)
            
            #lineNum += 1
            
    return bitstrings, words

def writeWordsToFile(path1, bitstrings):
    with open(path1, "w") as fid:
        for i in range(0, len(words)):
            fid.write(bitstrings[i] + "\n")
            
    # with open(path2, "w") as fid:
    #     for i in range(0, len(words)):
    #         fid.write(bitstrings[i] + "\n")

readPath = r"C:\Users\ellio\Programs\Datasets\Radio Dataset\mindwords.txt"
#writePath1 = r"C:\Users\ellio\Programs\Datasets\mindwords2.txt"
writePath2 = r"C:\Users\ellio\Programs\Datasets\Radio Dataset\mindbits.txt"
# skiplines = np.arange(0, 10, 1, dtype=int)

bitstrings, words = readWords(readPath)

print("Bitstrings: ", bitstrings[0])
print("Words: ", words[0])

print("Bitstring: ", bitstrings[65], " Word: ", words[65])

print('last ones:', bitstrings[-1], words[-1])
writeWordsToFile(writePath2, bitstrings)

