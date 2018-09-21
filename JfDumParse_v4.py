#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

##########################
# ARGUMENTS VERIFICATION #
########################################################
if len(sys.argv) != 3:
    print("\tUSAGE : {} fastaFile threshold")
    sys.exit(1)
########################################################
    
#############
# Constants #
########################################################
NAME_FILE = sys.argv[1]

try:
    TH = int(sys.argv[2]) #threshold 
except ValueError:
    print("\tUSAGE : {} fastaFile threshold")
    print("THRESHOLH VALUE NEED TO BE AN INTEGER !")
    sys.exit(1)

if "." in NAME_FILE:
    BASE, EXT = NAME_FILE.split(".")
else:
    BASE = NAME_FILE
    EXT = "fa"
    
BUFFER_SIZE = 10000
VERIF = True
########################################################

#################
# Files opening #
########################################################
try:
    file = open(NAME_FILE, 'r')
except FileNotFoundError:
    print("Open file problem.")
    sys.exit(1)

kmerX = open("{}_kmer_{}X.{}".format(BASE, TH, EXT), 'w')
kmerU = open("{}_kmer_{}U.{}".format(BASE, TH, EXT), 'w')

########################################################

#######################
# FORMAT VERIFICATION #
######################################################
count = 0
if VERIF:
    # Verification of the structure 
    odd = True
    for l in file:
        if odd:
            if l[0] != ">":
                print("There is a problem in file at line {}.".format(count+1))
                sys.exit(1)
            odd = False
        else:
            odd = True
        count+=1
    
    # Number of line verification
    if count%2 != 0:
        print("Odd number of lines!!")
        print("Maybe something is missing !!!")
        sys.exit(1)
    
    # Point at the beginning of the file
    file.seek(0, 0)
    
    # Measure the number of line in one buffer
    linesBuffer = len(file.readlines(BUFFER_SIZE))
    
    # Point again at the beginning of the file
    file.seek(0, 0)

print("There are {} sequences in {} : ".format(count//2, NAME_FILE), end="")
######################################################


# Capture the total number of buffer according to displays the progress
totalBuffers = count/linesBuffer

# Initialize progress
loop = 0

# At each loop turn a buffer is processed
while True:
    if VERIF:
        sys.stdout.write('\r')
        sys.stdout.write("There are {} sequences in {} : {}%".format(count//2, NAME_FILE, str(int(loop/totalBuffers*100))))
        sys.stdout.flush()
        
    # Lists that contain less and more thresholds sequences coming from the current buffer
    kmerU_List = []
    kmerX_List = []
    
    # content of a buffer
    res = file.readlines(BUFFER_SIZE)
    
    # if there are missing lines in the buffer, we add them
    while len(res)%2 != 0 and res[-1] != "\n":
        res.append(file.readline())
    
    # If the buffer is empty, we have reached the end of the file
    # So we go out
    if  not res:
        break
    
    # if there is content in the buffer, we treat it
    else:
        i=0
        while i < len(res):
            # if the abundance of the sequence is less than or equal to the threshold value
            # We add id and the sequence to the lessList buffer
            if int(res[i][1:]) >= TH:
                kmerX_List.append("".join([res[i], res[i+1]]))
            
            # if the abundance of the sequence is above the threshold value
            # We add id and the sequence to the moreList buffer
            else:
                kmerUList.append("".join([res[i], res[i+1]]))

            i+=2
    
    # Now that we have completed the lists using the current buffer, 
    # we can empty their contents in the corresponding files
    kmerU.writelines(kmerU_List)
    kmerX.writelines(kmerX_List)
    loop+=1

# close opended files objects
kmerX.close()
kmerU.close()
file.close()

print("\nDONE !!!\n")
