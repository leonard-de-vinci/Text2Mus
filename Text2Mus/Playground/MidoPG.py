import mido
import time
import numpy as np
import rtmidi

import Core.Midi2Image as m2i

from mido import MidiFile, Message, tempo2bpm
pathtest = "D:/musics/130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]/T/T/"
pathtest2 = "D:/musics/130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]/Jazz_www.thejazzpage.de_MIDIRip/"
print(mido.get_output_names())
port = mido.open_output(mido.get_output_names()[0])



mid = m2i.MidiFile(pathtest2 + 'autleave.mid')
length = mid.length

print('Song length: {} minutes, {} seconds, {} ticks'.format(int(length / 60),int(length % 60),(mid.get_total_ticks())))

reltime = 0

import matplotlib as plt
#array = m2i.getImageFromMidi(pathtest + 'TOTO.Africa K.mid')

Midi = m2i.MidiFile(pathtest2+'atrain2.mid')
array,chans = Midi.getArrayData()
#np.save('toto',array)
#Midi.RollToMidi(np.load("toto.npy"))
#array = np.load('toto.npy')
#print(array)


from PIL import Image
img = Image.fromarray(array[2,:,:10000], 'L')
img.show()
print('almost done')
    #np.set_printoptions(threshold=np.nan)
    
    #img.save("c:/users/youness/documents/Visual Studio 2017/Projects/Text2Mus/Text2Mus/bonobo.bmp","BMP")
#BPM = 60000000/mid.get_tempo()
#pulseLength=60/(BPM*mid.ticks_per_beat)
#print(mid.get_tempo())

#for msg in mid.play():
#    print(reltime)
#    #port.send(msg)
#    if msg.type == 'program_change':
#        print(msg," This is an instrument")
#    if msg.type == 'set_tempo':
#        print('Tempo changed to {:.1f} BPM.'.format(tempo2bpm(msg.tempo)))
#    reltime+= mid.duration2ticks(msg.time)
#print(mid.get_total_ticks())
