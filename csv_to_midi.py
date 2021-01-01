"""
This is the csv to midi module. 
"""

import re
import os
#import random
import sys
import argparse
from fractions import Fraction
 
import music21
import pandas as pd
# defines numerical values for notes
notes = ['C', 'D-', 'D', 'E-', 'E', 'F', 'G-', 'G', 'A-', 'A', 'B-', 'B']
note_to_num = dict([[n, i] for i, n in enumerate(notes)])
num_to_note = dict([[v, k] for k, v in note_to_num.items()])

same_note = {'A#': 'B-', 'C#': 'D-', 'D#': 'E-', 'F#': 'G-', 'G#': 'A-'}


def split_note(note):
	"""Return tuple of strings representing the tone and its octave. 

	>>> split_note("A-7") 
	"A-", "7"
	"""
	assert re.fullmatch('[A-G](#|-)?[0-7]', note) is not None, 'Note not formatted correctly.'
	return note[:-1], int(note[-1])


def name_to_num(name):
	"""Return integer representing "note number", given string name (tone and octave combined). 
	
	>>> name_to_num("A-7")
	104
	"""
	
	note, octave = split_note(name)
	b = ""
	if note in same_note:
		b = note_to_num[same_note[note]]
	else:
		b = note_to_num[note]
	a = (octave + 1) * 12
	return a + b


def produce_midi(filename, df, desired_tempo, output_dir_name):
	s1 = music21.stream.Stream()
	mm1 = music21.tempo.MetronomeMark(number=desired_tempo)
	s1.append(mm1)

	running_offset = 0 # essentially, the current total duration we are at while processing the midi file
	for index, row in df.iterrows():
		curr_duration = row[3]
		#This rounds durations to real music note types, will include as optional flag sometime in the future
		# if curr_duration < 0.07 and curr_duration > 0.0:
			# note_type = '16th'
		# elif curr_duration < 0.15:
			# note_type = 'eighth'
		# elif curr_duration < 0.30:
			# note_type = 'quarter'
		# elif curr_duration < 0.4: 
			# print("triplet")
		# elif curr_duration < 0.6:
			# note_type = 'half'
		# else: 
			# note_type = "whole" 

		x = music21.note.Note(name_to_num(row[1]), duration=music21.duration.Duration(Fraction(curr_duration)))
		#print(x.note_type)
		x.volume.velocity = row[4] 
		# x.offset = row[2] * 4 + running_offset # this is measures
		x.offset = row[2] + running_offset # this is quarter notes, so all time measurement is consistent
		
		s1.insert(x)
		
		# This code generates random chords for some of the notes, just ignore it
		# interval_range = random.choice([0, 0, 7, 9])
		# i = interval.Interval(interval_range)
		# y = i.transposeNote(x)
		# y.offset = x.offset
		# s1.insert(y)

	# Removes note if too short
	# for note in s1:
		# if note.duration.quarterLength < 0.01:
			# s1.remove(note)

	s1.write("midi", output_dir_name + "/" + filename[:-4] + ".mid")
	
def is_dir(dirname):
    """Checks if a path is an actual directory"""
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname


def main():
	#us = music21.environment.UserSettings()
	#us.getSettingsPath()
	# print command line arguments
	parser = argparse.ArgumentParser()

	parser.add_argument("input_dir_name", help="name of input directory of csv files",
                    type=str)
	parser.add_argument("-o", "--output_dir_name", help="name of output directory of midi files, if argument not specified, will create one with suffix output-midis",
					type=str)
	parser.add_argument("-t", "--tempo", help="desired tempo",
                    type=int)			
	
	args = parser.parse_args()
	is_dir(args.input_dir_name)
	
	input_dir = os.fsencode(args.input_dir_name)
	output_dir_name = args.output_dir_name
	
	if not output_dir_name: 
		output_dir_name = args.input_dir_name + "-output-midis"
		
	if not os.path.exists(output_dir_name):
		os.makedirs(output_dir_name)
		
	print("Outputting mid files in to " + output_dir_name)
	for file in os.listdir(input_dir):
		
		filename = os.fsdecode(file)
		print("Processing " + filename + " in to " + filename[:-4] + ".mid")
		df = pd.read_csv(args.input_dir_name + "/" + filename, engine='python')
		df_tempo = df.iloc[1,5] 
		if args.tempo: 
			produce_midi(filename, df, args.tempo, output_dir_name)
		else: 
			produce_midi(filename, df, df_tempo, output_dir_name) 
		
	print("Done creating midis!")


if __name__ == "__main__":
	main()
