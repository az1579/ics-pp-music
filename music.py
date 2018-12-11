
import librosa
import numpy as np


sr = 44100

def update_wav(midi_object, my_name): #Done
    # input: updated matrix
    # updates the wav file for the current user, based on changes made by everybody
    # returns updated matrix
    synthesized_midi = midi_object.synthesize()
    np_song = np.array(synthesized_midi)
    librosa.output.write_wav('Music.wav', np_song, sr)