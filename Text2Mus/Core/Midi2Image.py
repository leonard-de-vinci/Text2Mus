import mido
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import colorConverter
import random

class MidiFile(mido.MidiFile):

    def __init__(self, filename, sampleRate):

        mido.MidiFile.__init__(self, filename)
        self.sr = sampleRate
        self.meta = {}
        with open("./Core/ProgramNames.txt","r") as f:
            data = [i.replace("\n","") for i in f.readlines()]
            self.programN = data[:-1]
        self.events = self.get_events()
        

    def get_events(self):
        mid = self
        #print(mid)

        # There is > 16 channel in midi.tracks. However there is only 16 channel related to "music" events.
        # We store music events of 16 channel in the list "events" with form [[ch1],[ch2]....[ch16]]
        # Lyrics and meta data used a extra channel which is not include in "events"

        events = [[] for x in range(16)]

        # Iterate all event in the midi and extract to 16 channel form
        for track in mid.tracks:
            for msg in track:
                try:
                    channel = msg.channel
                    events[channel].append(msg)
                except AttributeError:
                    try:
                        if type(msg) != type(mido.UnknownMetaMessage):
                            self.meta[msg.type] = msg.dict()
                        else:
                            pass
                    except:
                        print("error",type(msg))

        return events

    def get_BPM(self) :
        tempo = self.get_tempo()
        self.BPM = 60000000/tempo
        return self.BPM

    def get_pulselength(self):
        self.pulseLength=60/(BPM*mid.ticks_per_beat)
        return self.pulseLength

    def duration2ticks(self,duration):
        return int((duration*1000000)*self.ticks_per_beat)/self.get_tempo()

    def get_tempo(self):
        try:
            return self.meta["set_tempo"]["tempo"]
        except:
            return 500000

    def get_total_ticks(self):
        max_ticks = 0
        for channel in range(16):
            ticks = sum(msg.time for msg in self.events[channel])
            if ticks > max_ticks:
                max_ticks = ticks
        return max_ticks
    
    def getArrayData(self):
        events = self.get_events()
        # Identify events, then translate to piano roll
        # choose a sample ratio(sr) to down-sample through time axis
        sr = self.sr

        # compute total length in tick unit
        length = self.get_total_ticks()

        # allocate memory to numpy array
        roll = np.zeros((16, 128, length,2), dtype=np.float32)
        tempo = self.get_tempo()
        # use a register array to save the state(no/off) for each key
        note_register = [int(-1) for x in range(129)]

        # use a register array to save the state(program_change) for each channel
        timbre_register = [1 for x in range(16)]

        for i, chan in enumerate(events):
            time_counter = 0
            volume = 100
            # Volume would change by control change event (cc) cc7 & cc11
            # Volume 0-100 is mapped to 0-127

            #print("channel", i, "start")
            for msg in chan:
                if msg.type == "control_change":
                    if msg.control == 7:
                        volume = msg.value
                        # directly assign volume
                    if msg.control == 11:
                        volume = volume * msg.value // 127
                        # change volume by percentage
                    # print("cc", msg.control, msg.value, "duration", msg.time)

                if msg.type == "program_change":
                    timbre_register[i] = msg.program
                    #print("channel", idx, "pc", msg.program, "time", time_counter, "duration", msg.time)



                if msg.type == "note_on":
                    #for n in range(time_counter//sr,int(time_counter+self.duration2ticks(msg.time))//sr):
                    try:
                        roll[i,msg.note,time_counter] = np.array([msg.velocity,msg.time], dtype=np.float32) 
                    except:
                        continue
           
                if msg.type == "note_off":
                    roll[i,msg.note,time_counter] = np.array([-1,-1], dtype=np.float32)

                time_counter += msg.time


        return roll, timbre_register

    def getPianoOnly(self):
        event = []
        for i in self.events:
            for j in i:
                if j.type =="program_change":
                    if j.program == 0:
                        event = i
                        break
        

        sr = self.sr

        # compute total length in tick unit
        length = self.get_total_ticks()
        # allocate memory to numpy array
        roll = np.zeros((128, length//sr,2), dtype=np.float32)
        reltime = 0
        for idx,msg in enumerate(event):
            if msg.type =="note_on":
                roll[msg.note,int(reltime)] = np.array([msg.velocity,msg.time])
            reltime+=msg.time
        return roll
    
        

    def get_roll(self):
        events = self.get_events()
        # Identify events, then translate to piano roll
        # choose a sample ratio(sr) to down-sample through time axis
        sr = self.sr

        # compute total length in tick unit
        length = self.get_total_ticks()

        # allocate memory to numpy array
        roll = np.zeros((16, 128, 10000), dtype="float32")
        if lenth>10000:
            limit = random.randint(0,length-10001)
        else :
            limit = random.randint(0,length-5001)
        # use a register array to save the state(no/off) for each key
        note_register = [int(-1) for x in range(128)]

        # use a register array to save the state(program_change) for each channel
        timbre_register = [1 for x in range(16)]


        for idx, channel in enumerate(events):

            time_counter = 0
            volume = 100
            # Volume would change by control change event (cc) cc7 & cc11
            # Volume 0-100 is mapped to 0-127

            #print("channel", idx, "start")
            for msg in channel:
                if time_counter<limit:
                    time_counter+=msg.time
                    continue
                elif time_counter>limit+10000:
                    return roll
                elif msg.type == "control_change":
                    if msg.control == 7:
                        volume = msg.value
                        # directly assign volume
                    if msg.control == 11:
                        volume = volume * msg.value // 127
                        # change volume by percentage
                    # print("cc", msg.control, msg.value, "duration", msg.time)

                elif msg.type == "program_change":
                    timbre_register[idx] = msg.program

                    #print("channel", idx, "pc", msg.program, "time", time_counter, "duration", msg.time)



                elif msg.type == "note_on":
                    print("there's a note on in ",idx)
                    note_on_start_time = time_counter // sr
                    note_on_end_time = (time_counter + msg.time) // sr
                    intensity = 127
					# When a note_on event *ends* the note start to be play 
					# Record end time of note_on event if there is no value in register
					# When note_off event happens, we fill in the color
                    if note_register[msg.note] == -1:
                        note_register[msg.note] = (note_on_end_time,intensity)
                    else:
					# When note_on event happens again, we also fill in the color
                        old_end_time = note_register[msg.note][0]
                        old_intensity = note_register[msg.note][1]
                        roll[idx, msg.note, old_end_time: note_on_end_time] = old_intensity
                        note_register[msg.note] = (note_on_end_time,intensity)


                elif msg.type == "note_off":
                    #print("off", msg.note, "time", time_counter, "duration", msg.time, "velocity", msg.velocity)
                    note_off_start_time = time_counter // sr
                    note_off_end_time = (time_counter + msg.time) // sr
                    note_on_end_time = note_register[msg.note][0]
                    intensity = 0
					# fill in color
                    roll[idx, msg.note, note_on_end_time:note_off_end_time] = intensity

                    note_register[msg.note] = -1  # reinitialize register

                else:
                    time_counter += msg.time

                # TODO : velocity -> done, but not verified
                # TODO: Pitch wheel
                # TODO: Channel - > Program Changed / Timbre catagory
                # TODO: real time scale of roll

            # if there is a note not closed at the end of a channel, close it
            for key, data in enumerate(note_register):
                if data != -1:
                    note_on_end_time = data[0]
                    intensity = data[1]
                    # print(key, note_on_end_time)
                    note_off_start_time = time_counter // sr
                    roll[idx, key, note_on_end_time:] = intensity
                note_register[idx] = -1

        return roll
    def get_Array2(self):
        events = self.get_events()
        # Identify events, then translate to piano roll
        # choose a sample ratio(sr) to down-sample through time axis
        sr = self.sr

        # compute total length in tick unit
        length = self.get_total_ticks()
        roll = np.zeros((16, 128, length), dtype="float32")
        if length>10000:
            limit = random.randint(0,length-10001)
        else :
            limit = 0
        # allocate memory to numpy array
        tempo = self.get_tempo()
        # use a register array to save the state(no/off) for each key
        note_register = [int(-1) for x in range(129)]

        # use a register array to save the state(program_change) for each channel
        timbre_register = [1 for x in range(16)]

        for i, chan in enumerate(events):
            time_counter = 0
            volume = 100
            # Volume would change by control change event (cc) cc7 & cc11
            # Volume 0-100 is mapped to 0-127

            #print("channel", i, "start")
            for msg in chan:
                if msg.type == "control_change":
                    if msg.control == 7:
                        volume = msg.value
                        # directly assign volume
                    if msg.control == 11:
                        volume = volume * msg.value // 127
                        # change volume by percentage
                    # print("cc", msg.control, msg.value, "duration", msg.time)

                if msg.type == "program_change":
                    timbre_register[i] = msg.program
                    #print("channel", idx, "pc", msg.program, "time", time_counter, "duration", msg.time)



                if msg.type == "note_on":
                    #for n in range(time_counter//sr,int(time_counter+self.duration2ticks(msg.time))//sr):
                    try:
                        roll[i,msg.note,time_counter:int(time_counter+msg.time)] = msg.velocity
                    except:
                        continue
           
                if msg.type == "note_off":
                    if time_counter==length:
                        roll[i,msg.note,time_counter-1] = -1
                    else :
                        roll[i,msg.note,time_counter-1] = -1

                time_counter += msg.time


        if length>10000:
            return roll[:,:,limit:limit+10000]
        else :
            a = np.zeros((16,128,10000))
            a[:roll.shape[0],:roll.shape[1],:roll.shape[2]]=roll
            return a




def Roll2Midi(roll, program):
    #Step 1 Get notes arrays
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    np.set_printoptions(threshold=np.nan)
    print(roll[64])
    track.append(mido.Message('program_change', program=program, time=0))
    swap = np.swapaxes(roll,0,1)
    
    for height, i in enumerate(swap):
        happened = 0
        for time, j in enumerate(i):
            if np.all([j,np.array([-1,-1], dtype=np.float32)]):
                track.append(mido.Message('note_off', note = height))

            elif not np.all([j,np.array([-1,-1], dtype=np.float32)]):
                print("j =",j)
                track.append(mido.Message('note_on', velocity=127, time = 100, note = height))
        return mid