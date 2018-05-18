#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
##

##
## read a path (ref) reference all file sith their sha1 and chek the second folder (src)
## to check if this qhaone exist or not if it exist, it can move to the dst folder or just remove it.
##


import os
import shutil
import errno
import fnmatch
import stat
import sys
import subprocess
import shlex
import re
import copy

import hashlib

# get the size of the console:
def get_console_size():
	rows, columns = os.popen('stty size', 'r').read().split()
	return {
		'x': int(columns),
		'y': int(rows)
	}

CONSOLE_SIZE = get_console_size()
def clear_line():
	print("\r" + " "*CONSOLE_SIZE["x"] + "\r", end="")

#print("Console size = " + str(CONSOLE_SIZE))

def get_sha512(filename, reduce=True):
	BLOCKSIZE = 16000
	hasher = hashlib.sha512()
	#hasher = hashlib.md5()
	with open(filename, 'rb') as afile:
		buf = afile.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			if reduce == True:
				return hasher.hexdigest()
			buf = afile.read(BLOCKSIZE)
	return copy.deepcopy(hasher.hexdigest())


##
## @brief Get list of all Files in a specific path (with a regex)
## @param[in] path (string) Full path of the machine to search files (start with / or x:)
## @param[in] regex (string) Regular expression to search data
## @param[in] recursive (bool) List file with recursive search
## @param[in] remove_path (string) Data to remove in the path
## @return (list) return files requested
##
def get_list_of_file_in_path(path, filter="*", recursive = False, remove_path=""):
	out = []
	if os.path.isdir(os.path.realpath(path)):
		tmp_path = os.path.realpath(path)
	else:
		print("[E] path does not exist : '" + str(path) + "'")
	last_x = 0
	for root, dirnames, filenames in os.walk(tmp_path):
		deltaRoot = root[len(tmp_path):]
		while     len(deltaRoot) > 0 \
		      and (    deltaRoot[0] == '/' \
		            or deltaRoot[0] == '\\' ):
			deltaRoot = deltaRoot[1:]
		clear_line()
		last_x = len(str(deltaRoot))
		print("[I] path: '" + str(deltaRoot) + "'", end="")
		#ilter some stupid path ... thumbnails=>perso @eaDir synology
		if    ".thumbnails" in deltaRoot \
		   or "@eaDir" in deltaRoot:
			continue
		if     recursive == False \
		   and deltaRoot != "":
			return out
		tmpList = []
		for elem in filter:
			tmpppp = fnmatch.filter(filenames, elem)
			for elemmm in tmpppp:
				tmpList.append(elemmm)
		# Import the module :
		for cycleFile in tmpList:
			#for cycleFile in filenames:
			add_file = os.path.join(tmp_path, deltaRoot, cycleFile)
			if len(remove_path) != 0:
				if add_file[:len(remove_path)] != remove_path:
					print("[E] Request remove start of a path that is not the same: '" + add_file[:len(remove_path)] + "' demand remove of '" + str(remove_path) + "'")
				else:
					add_file = add_file[len(remove_path)+1:]
			out.append(add_file)
	print("")
	return out;


import argparse

parser = argparse.ArgumentParser(description='Check comparison between 2 path.')
parser.add_argument('--ref',
                    type=str,
                    action='store',
                    default="",
                    help='Reference path (the sha512 sources)')
parser.add_argument('--src',
                    type=str,
                    action='store',
                    default="",
                    help='Path to check that data is duplicated (remove data that is duplicated)')
parser.add_argument('--dst',
                    type=str,
                    action='store',
                    default="out_store_rebut",
                    help='Path to move duplication (move here data that is duplicated)')
parser.add_argument('--ref_remove_double',
                    action='store_true',
                    default=False,
                    help='remove double find in the base reference')
parser.add_argument('--src_remove_double',
                    action='store_true',
                    default=False,
                    help='remove double find in the src reference')

args = parser.parse_args()

print("[I] ref=" + args.ref)
print("[I] src=" + args.src)
print("[I] dst=" + args.dst)

if args.ref == "":
	print("[ERROR] Missing ref")
	exit(-1)
if args.src == "":
	print("[ERROR] Missing src")
	exit(-1)
if args.dst == "":
	print("[ERROR] Missing dst")
	exit(-1)

def check_file(data):
	out = ""
	for elem in str(data):
		if elem in "azertyuiopqsdfghjklmwxcvbn1234567890AZERTYUIOPQSDFGHJKLMWXCVBNéèçà@.- _?:!*+/\<>()[]{}=°|#~²":
			out += elem
	return out

print("===================================================")
print("[I] Create List of files REF ...")
print("===================================================")
list_files_ref = get_list_of_file_in_path(args.ref, recursive=True)

curent_DB = {}

print("===================================================")
print("[I] Generate sha512 ...")
print("===================================================")
ref_duplicate = 0
src_missing = 0

file_in_double = open("fileInDouble.txt", "w")
file_not_in_ref = open("fileNotInRef.txt", "w")

last_x = 0
iii = 0
for elem in list_files_ref:
	iii += 1
	value_progress = float(iii) / float(len(list_files_ref))
	value_progress1 = int(value_progress*100)
	value_progress2 = int(value_progress*10000 - value_progress1*100)
	clear_line()
	print("[I] processing " + str(iii) + "/" + str(len(list_files_ref)) + "        " + str(value_progress1) + "." + str(value_progress2) + "/100        " + check_file(elem), end='')
	last_x = len(elem)
	sys.stdout.flush()
	value_sha512 = get_sha512(elem)
	# check if the element is not a duplication ...
	if value_sha512 in curent_DB.keys():
		## print("\n[ERROR] Double element in the data-base (reduced ...):")
		print(" ... ", end="")
		# need to check with a not reduce sha512
		value_src_sha512_full = get_sha512(elem,reduce=False)
		# a reduce sha512 can have many distint file depending on it ...
		for elem_previous in curent_DB[value_sha512]:
			if "sha512" not in elem_previous.keys():
				#print("calculate previous from : '" + elem_previous["file"] + "'")
				elem_previous["sha512"] = get_sha512(elem_previous["file"],reduce=False)
		add_in_db = True
		for elem_previous in curent_DB[value_sha512]:
			"""
			print("check: ")
			print("    " + elem_previous["sha512"])
			print("    " + value_src_sha512_full)
			print("    " + value_sha512)
			"""
			if elem_previous["sha512"] == value_src_sha512_full:
				if args.ref_remove_double == True:
					print("\n    ==> remove double in reference: '" + check_file(elem) + "'")
					os.remove(elem)
					add_in_db = False
				else:
					ref_duplicate += 1
					print("\n[ERROR] Double element in the data-base:      " + check_file(ref_duplicate))
					print("    sha512=" + str(value_sha512))
					print("    ref      =" + check_file(elem_previous["file"]))
					print("    ref(copy)=" + check_file(elem))
					file_in_double.write(check_file(elem_previous["file"]) + "\n")
					file_in_double.write(check_file(elem) + "\n")
					file_in_double.write("--------------------------------------------------------------------\n")
				break
		if add_in_db == True:
			print("apend new : " + str(len(curent_DB[value_sha512])))
			curent_DB[value_sha512].append({"file":elem,"sha512":value_src_sha512_full})
			print("apend new : " + str(len(curent_DB[value_sha512])))
	else:
		curent_DB[value_sha512] = [{"file":elem}]
print("")

"""
for elem in curent_DB.keys():
	print("    " + str(elem) + " - " + str(curent_DB[elem]))
"""

print("===================================================")
print("[I] Create List of files SRC ...")
print("===================================================")
list_files_src = get_list_of_file_in_path(args.src, recursive=True)

print("===================================================")
print("[I] Generate sha512 ...")
print("===================================================")
last_x = 0
iii = 0
for elem in list_files_src:
	iii += 1
	value_progress = float(iii) / float(len(list_files_src))
	value_progress1 = int(value_progress*100)
	value_progress2 = int(value_progress*10000 - value_progress1*100)
	clear_line()
	print("[I] processing " + str(iii) + "/" + str(len(list_files_src)) + "        " + str(value_progress1) + "." + str(value_progress2) + "/100        " + check_file(elem), end='')
	last_x = len(elem)
	sys.stdout.flush()
	value_sha512 = get_sha512(elem, reduce=True)
	# check if the element is not a duplication ...
	if value_sha512 not in curent_DB.keys():
		src_missing += 1
		"""
		print("\n[INFO] Find element not in the dB:      " + str(src_missing))
		print("    sha512=" + str(value_sha512))
		print("    src=" + check_file(elem))
		"""
		print(" (add)")
		curent_DB[value_sha512] = [{"file":elem}]
		file_not_in_ref.write(str(elem + "\n"))
	else:
		value_src_sha512_full = get_sha512(elem, reduce=False)
		for elem_previous in curent_DB[value_sha512]:
			if "sha512" not in elem_previous.keys():
				print("calculate previous from : '" + elem_previous["file"] + "'")
				elem_previous["sha512"] = get_sha512(elem_previous["file"], reduce=False)
		add_in_db = True
		for elem_previous in curent_DB[value_sha512]:
			"""
			print("check: ")
			print("    " + elem_previous["sha512"])
			print("    " + value_src_sha512_full)
			print("    " + value_sha512)
			"""
			if elem_previous["sha512"] == value_src_sha512_full:
				if args.src_remove_double == True:
					print("\n    ==> remove double in source: '" + check_file(elem) + "'")
					os.remove(elem)
					add_in_db = False
				else:
					print("\n    ==> must move double in source in destination: '" + check_file(elem) + "'")
				break
		if add_in_db == True:
			src_missing += 1
			"""
			print("\n[INFO] Find element not in the dB (FULL):      " + str(src_missing))
			print("    sha512=" + str(value_sha512))
			print("    src=" + check_file(elem))
			"""
			print(" (add 2)")
			file_not_in_ref.write(check_file(elem) + "\n")
			curent_DB[value_sha512].append({"file":elem,"sha512":value_src_sha512_full})
print("")

file_not_in_ref.close()
print("Duplicate file in reference : " + str(ref_duplicate))
print("Missing file in reference : " + str(src_missing))
