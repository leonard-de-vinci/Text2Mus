import mido
import time
import rtmidi
from mido import MidiFile, Message, tempo2bpm
pathtest = "D:/musics/130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]/7/"
port = mido.open_output(mido.get_output_names()[0])
mid = MidiFile(pathtest + '7_POWERL.mid')
length = mid.length

print('Song length: {} minutes, {} seconds.'.format(int(length / 60),
        int(length % 60)))
print('Tracks:')
for i, track in enumerate(mid.tracks):
    print('  {:2d}: {!r}'.format(i, track.name.strip()))


for msg in mid.play():
    if not msg.is_meta:
        port.send(msg)
        #time.sleep(msg.time)
    
    if msg.type == 'set_tempo':
        print('Tempo changed to {:.1f} BPM.'.format(tempo2bpm(msg.tempo)))

