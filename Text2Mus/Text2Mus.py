import mido
import Core.Midi2Image as m2i
from Core.DataGenerator import DataGenerator as G
import os
from Core.AutoEncoder import AutoMidi as AM
path = "D:/musics/130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]/"

listfiles = []
for root, subdirs, files in os.walk(path):
    for f in files:
        if ".mid" in f:
            listfiles.append(root+"/"+f)
ln = len(listfiles)

rd = int(len(listfiles)/5)
training = [i for i in listfiles[:ln-rd]]
validation = [i for i in listfiles[ln-rd+1:]]

a = G(training)
b= G(validation)

model = AM()
model.autoencoder.summary()
model.trainGenerator(a,b)

#a = m2i.MidiFile("D:/musics/130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]/Jazz_www.thejazzpage.de_MIDIRip/autleave.mid",1)

#b = a.get_Array2()
#print(b.any())