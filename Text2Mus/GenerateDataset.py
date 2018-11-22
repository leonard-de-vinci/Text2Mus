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

for idx,f in enumerate(listfiles):
    try :
        Midi = m2i.MidiFile(f)
        array,programs = Midi.getArrayData()
    except :
        print("Midi file does not load")
        continue  
    sArray = []
    for i,chan in enumerate(array):
        if np.any(chan) :
            sArray.append((programN[i],chan))
    del array
    try :
        for s in sArray:
            np.savez_compressed(datasetPath+s[0]+"/"+(f.split("/")[-1].replace(".mid","")),s[1])
    except :
        print("Impossible to save this file")
    print(str(idx)+"/"+str(len(listfiles))+" files treated")
    if idx == 9:
        break


port = mido.open_output(mido.get_output_names()[0])
file = os.listdir("D:/musics/dataset/Piano 1/")[0]
popo = np.load("D:/musics/dataset/Piano 1/009count.npz")['arr_0']
print(popo)
MidTemp = m2i.Roll2Midi(popo,0)

for i in MidTemp.play():
    print(i)
    port.send(i)