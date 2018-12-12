import librosa
import pretty_midi
import numpy as np
import pygame
import pyaudio
import wave


def update_wav(midi_object, my_name): #Done
    # input: updated matrix
    # updates the wav file for the current user, based on changes made by everybody
    # returns updated matrix
    synthesized_midi = midi_object.synthesize()
    np_song = np.array(synthesized_midi)
    librosa.output.write_wav(my_name + '-song.wav', np_song, 44100)


def song(string, my_name): # 'bpm120 C4 8 C3 A4 8 A4 8' # the number by itself is the length of the note before it. If no number for a note, then quarter note by default
    notes = string.split(' ')
    velocity = 100
    music = pretty_midi.PrettyMIDI()
    cello_program = pretty_midi.instrument_name_to_program('Cello')
    cello = pretty_midi.Instrument(program=cello_program)

    bpm = int(notes[0][3:])
    i = 1
    start = 0.0

    while i < len(notes):
        cur_note = notes[i]
        pitch_num = pretty_midi.note_name_to_number(cur_note)
        if i < len(notes) - 1 and notes[i+1].isdigit(): #check if next item is tempo, or just next note
            note_len = int(notes[i+1])
            i += 2
        else:
            note_len = 4 # default is quarter note
            i += 1
        note_len = 1.0 / note_len # quarter note (4) is actually 1/4
        end = start + get_note_length(bpm, note_len)
        new_note = pretty_midi.Note(velocity, pitch_num, start, end)
        cello.notes.append(new_note)
        start = end

    music.instruments.append(cello)

    update_wav(music, my_name)
    x = cello.notes
    #return ' '.join(x)


def get_note_length(bpm, note_length): #note length is a fraction (or 1.0 if it's a whole note)
    #for 60 bpm, a 1/4 note gives 1.0 second; a 1/2 note is 2.0 seconds
    #for 120 bpm, a 1/4 note gives 0.5 seconds
    return (4 * note_length) * (60 / bpm)



if __name__ == '__main__':
    song('bpm120 C4 8 C3 A4 8 A4 8', 'test')
