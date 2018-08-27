#!/usr/bin/python3
import os
import fnmatch
import glob

print("Start rename group ...")

def extract_id(value):
	id = ""
	for elem in value:
		if    elem == '0' \
		   or elem == '1' \
		   or elem == '2' \
		   or elem == '3' \
		   or elem == '4' \
		   or elem == '5' \
		   or elem == '6' \
		   or elem == '7' \
		   or elem == '8' \
		   or elem == '9':
			id += elem
		else:
			break
	return int(id)
base_name = "Trollhunters.S01E"
out_name = "Troll hunters-s01-e"
files = glob.glob(base_name + "*")
max = 0
for file in files:
	id = extract_id(file[len(base_name):])
	if id > max:
		max = id

print("number of Element: " + str(max))

nb_char = 1
if max>99999:
	nb_char = 6
elif max>9999:
	nb_char = 5
elif max>999:
	nb_char = 4
elif max>99:
	nb_char = 3
elif max>9:
	nb_char = 2

def get_id(id):
	val = str(id)
	while len(val)<nb_char:
		val = "0" + val
	return val

for file in files:
	#print("file: " + file)
	id = extract_id(file[len(base_name):])
	#print("    id " + get_id(id))
	outfile = out_name + get_id(id) + "-.mkv"
	#exit(-1)
	if file != outfile:
		print("rename " + file + " ==> " + outfile)
		os.rename(file, outfile)

exit(0)
