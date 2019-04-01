#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2016, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
##
import os
import fnmatch
import sys
import subprocess
import shlex
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
def get_list_of_file_in_path(path, regex="*", recursive = True, remove_path=""):
	out = []
	if os.path.isdir(os.path.realpath(path)):
		tmp_path = os.path.realpath(path)
		tmp_rule = regex
	else:
		debug.error("path does not exist : '" + str(path) + "'")
	
	for root, dirnames, filenames in os.walk(tmp_path):
		deltaRoot = root[len(tmp_path):]
		while     len(deltaRoot) > 0 \
		      and (    deltaRoot[0] == '/' \
		            or deltaRoot[0] == '\\' ):
			deltaRoot = deltaRoot[1:]
		if     recursive == False \
		   and deltaRoot != "":
			return out
		tmpList = filenames
		if len(tmp_rule) > 0:
			tmpList = fnmatch.filter(filenames, tmp_rule)
		# Import the module :
		for cycleFile in tmpList:
			#for cycleFile in filenames:
			add_file = os.path.join(tmp_path, deltaRoot, cycleFile)
			if len(remove_path) != 0:
				if add_file[:len(remove_path)] != remove_path:
					print("ERROR : Request remove start of a path that is not the same: '" + add_file[:len(remove_path)] + "' demand remove of '" + str(remove_path) + "'")
				else:
					add_file = add_file[len(remove_path)+1:]
			out.append(add_file)
	return out;

list_files = get_list_of_file_in_path('.', "*.cpp")
list_files += get_list_of_file_in_path('.', "*.hpp")
list_files += get_list_of_file_in_path('.', "*.cxx")
list_files += get_list_of_file_in_path('.', "*.hxx")
list_files += get_list_of_file_in_path('.', "*.c")
list_files += get_list_of_file_in_path('.', "*.h")
list_files += get_list_of_file_in_path('.', "*.C")
list_files += get_list_of_file_in_path('.', "*.H")
#list_files += get_list_of_file_in_path('.', "*.qml")

for elem in list_files:
	print("format code: " + elem)
	cmd_line = "clang-format -i " + elem.replace(" ", "\ ").replace("'", "\\'")
	ret = run_command(cmd_line)