import mido
import Core.Midi2Image as m2i
from Core.DataGenerator import DataGenerator as G
import os
from Core.AutoEncoder import AutoMidi as AM
import numpy as np
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
o = []
p= []
for i in range (5):
    o.append(a[i])
    p.append(b[i])
o = iter(o)
model = AM()
model.autoencoder.summary()
#model.trainGenerator(o,p)
d = model.GetDecoder()

from Core.TextEmbedder import TextEmbedder as TE

emb = TE("D:/glove.6B.100d.txt")

popo = emb.Vectorize("hello")

a =  d.predict(np.array([popo],dtype = np.float32))
print(a)

m2i.Roll2Midi(a[0],1)

#a = m2i.MidiFile("D:/musics/130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]/Jazz_www.thejazzpage.de_MIDIRip/autleave.mid",1)

#b = a.get_Array2()
#print(b.any())