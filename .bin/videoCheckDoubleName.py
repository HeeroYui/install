#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
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

##
## @brief Execute the command with no get of output
##
def run_command(cmd_line):
	# prepare command line:
	args = shlex.split(cmd_line)
	print("[INFO] cmd = " + str(args))
	try:
		# create the subprocess
		p = subprocess.Popen(args)
	except subprocess.CalledProcessError as e:
		print("[ERROR] subprocess.CalledProcessError : " + str(args))
		return False
	#except:
	#	debug.error("Exception on : " + str(args))
	# launch the subprocess:
	output, err = p.communicate()
	# Check error :
	if p.returncode == 0:
		return True
	else:
		return False



##
## @brief Get list of all Files in a specific path (with a regex)
## @param[in] path (string) Full path of the machine to search files (start with / or x:)
## @param[in] regex (string) Regular expression to search data
## @param[in] recursive (bool) List file with recursive search
## @param[in] remove_path (string) Data to remove in the path
## @return (list) return files requested
##
def get_list_of_file_in_path(path, filter, recursive = False, remove_path=""):
	out = []
	if os.path.isdir(os.path.realpath(path)):
		tmp_path = os.path.realpath(path)
	else:
		print("[E] path does not exist : '" + str(path) + "'")
	
	for root, dirnames, filenames in os.walk(tmp_path):
		deltaRoot = root[len(tmp_path):]
		while     len(deltaRoot) > 0 \
		      and (    deltaRoot[0] == '/' \
		            or deltaRoot[0] == '\\' ):
			deltaRoot = deltaRoot[1:]
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
	return out;


full_list = []

for extention in ["ts","avi","mkv","mp4"]:
	list_files = get_list_of_file_in_path(".", ["*."+extention], recursive=True)
	for elem in list_files:
		# find format -sXX-eXX-
		tmp = elem.split("/")[-1].split("-s")
		if len(tmp) != 2:
			print("[W] 1 ??? " + elem)
			print("    ==> " + str(tmp))
			continue
		base = tmp[0]
		tmp = tmp[1].split("-e")
		if len(tmp) != 2:
			print("[W] 2 ??? " + elem)
			print("    ==> " + str(tmp))
			continue
		if tmp[1][2] == "-":
			name = tmp[1][2:-len(extention)]
		else:
			print("[W] 3 missing '-' at pos 2 " + elem)
			print("    ==> " + str(tmp[1]))
			continue
		
		full_list.append({
		    "name":name,
		    "base":base,
		    "file":elem
		    })
		

def file_size(path):
	if not os.path.isfile(path):
		return 0
	statinfo = os.stat(path)
	return statinfo.st_size

def get_list(name):
	out = []
	for elem in full_list:
		if elem["name"] == name:
			out.append(elem)
	return out


# check naming correllation
for elem in full_list:
	tmp = get_list(elem["name"])
	if len(tmp) == 1:
		# normal case ...
		continue
	print("Duplicate Name:")
	first = True
	for elem_tmp in tmp:
		if elem["file"] == elem_tmp["file"]:
			print("    * " + elem_tmp["file"] + "    " + str(int(file_size(elem_tmp["file"])/1024/1024)) + " MB")
			first = False
		else:
			if first == True:
				break
			print("    - " + elem_tmp["file"] + "    " + str(int(file_size(elem_tmp["file"])/1024/1024)) + " MB")






