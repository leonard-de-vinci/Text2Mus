import time
import numpy as np
import mido
import Core.Midi2Image as m2i
import os


with open("./Core/ProgramNames.txt","r") as f:
    data = [i.replace("\n","") for i in f.readlines()]
    programN = data[:-1]

from mido import MidiFile, Message, tempo2bpm
pathtest = "D:/musics/130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]/"
datasetPath = "D:/musics/dataset/"
midPath = "D:/musics/AllinOne/"
for i in programN:
    try :
        os.mkdir(datasetPath+i)
    except :
        print("Folder not created")
listfiles =[]
for root, subdirs, files in os.walk(pathtest):
    for f in files:
        if ".mid" in f:
            listfiles.append(root+"/"+f)
print(len(listfiles))
import sys
for idx,f in enumerate(listfiles):
    try :
        Midi = m2i.MidiFile(f,1)
        #array,programs = Midi.getArrayData()
        array = Midi.getPianoOnly()
        
    except :
        print(sys.exc_info())
        continue  
    if array is None:
        continue
    #sArray = []
    #for i,chan in enumerate(array):
    #    if np.any(chan) :
    #        sArray.append((programN[i],chan))
    #del array
    try :
        #for s in sArray:
        #    np.savez_compressed(datasetPath+s[0]+"/"+(f.split("/")[-1].replace(".mid","")),s[1])
        np.savez_compressed(datasetPath+"Piano 1"+"/"+(f.split("/")[-1].replace(".mid","")),array)
    except :
        print("Impossible to save this file")
    print(str(idx)+"/"+str(len(listfiles))+" files treated")
    


