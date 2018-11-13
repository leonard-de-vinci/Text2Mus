import mido
import time
import numpy as np
import rtmidi

import Core.Midi2Image as m2i

from mido import MidiFile, Message, tempo2bpm
pathtest = "D:/musics/130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]/T/T/"
print(mido.get_output_names())
port = mido.open_output(mido.get_output_names()[0])



mid = MidiFile(pathtest + 'TOTO.Africa K.mid')
length = mid.length

print('Song length: {} minutes, {} seconds.'.format(int(length / 60),
        int(length % 60)))
print('Tracks:')
for i, track in enumerate(mid.tracks):
    print('  {:2d}: {!r}'.format(i, track.name.strip()))

reltime = 0

import matplotlib as plt
array = m2i.getImageFromMidi(pathtest + 'TOTO.Africa K.mid')

#Midi = m2i.MidiFile(pathtest+'TOTO.Africa K.mid')
#np.save('toto',array)
#Midi.RollToMidi(np.load("toto.npy"))
#array = np.load('toto.npy')
#print(array)
from PIL import Image
for i in range(15):
    img = Image.fromarray(array[i], 'RGBA')
    img.show()

#for msg in mid.play():
#    print(msg.time)
#    port.send(msg)
#    if msg.type == 'program_change':
#        print(msg," This is an instrument")
#    if msg.type == 'set_tempo':
#        print('Tempo changed to {:.1f} BPM.'.format(tempo2bpm(msg.tempo)))
