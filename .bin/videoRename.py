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






def rm_date(data):
	val = data.split("_France 2_")
	if len(val) == 2:
		return val[0]
	val = data.split("_France 3_")
	if len(val) == 2:
		return val[0]
	val = data.split("_France 4_")
	if len(val) == 2:
		return val[0]
	val = data.split("_France 5_")
	if len(val) == 2:
		return val[0]
	val = data.split("_France O_")
	if len(val) == 2:
		return val[0]
	val = data.split("_NT1_")
	if len(val) == 2:
		return val[0]
	val = data.split("_TF1_")
	if len(val) == 2:
		return val[0]
	val = data.split("_TMC_")
	if len(val) == 2:
		return val[0]
	val = data.split("_Gulli_")
	if len(val) == 2:
		return val[0]
	return data


def rename_group(list_element, extention):
	for elem in list_files:
		reduced_name = rm_date(elem[:-(len(extention)+1)])
		print("file: " + reduced_name)
		# remove the date in the channel ...
		val = reduced_name.split(" - ")
		if len(val) == 1:
			#standard film ...
			print("        FILM")
			if val[0] + "." + extention != elem:
				print("        ==> rename ...")
				print("            " + elem)
				print("            " + val[0] + "." + extention)
				out = val[0] + "." + extention
				if os.path.isfile(out):
					print("            " + out + " ==> exist ...")
					offset = 0
					while offset < 98:
						offset += 1
						out = val[0] + "__________" + str(offset) + "." + extention
						if os.path.isfile(out):
							print("            " + out + " ==> exist ...")
						else:
							break
					if offset >= 98:
						print("            " + out + " ==> Cen not move ...")
						continue
				cmd_line = "mv " + elem.replace(" ", "\ ").replace("'", "\\'") + " " + out.replace(" ", "\ ").replace("'", "\\'")
				ret = run_command(cmd_line)
		elif len(val) == 2:
			print("        ???")
			valll = val[0] + " - " + val[1]
			if valll + "." + extention != elem:
				print("        ==> rename ...")
				print("            " + elem)
				print("            " + valll + "." + extention)
				out = valll + "." + extention
				if os.path.isfile(out):
					offset = 0
					while offset < 98:
						offset += 1
						out = valll + "__________" + str(offset) + "." + extention
						if os.path.isfile(out):
							print("            " + out + " ==> exist ...")
						else:
							break
					if offset >= 98:
						print("            " + out + " ==> Cen not move ...")
						continue
				cmd_line = "mv " + elem.replace(" ", "\ ").replace("'", "\\'") + " " + out.replace(" ", "\ ").replace("'", "\\'")
				ret = run_command(cmd_line)
			
		elif    val[1][:6] == "Saison" \
		     or val[1][1:7] == "pisode":
			# remove space ... not needed to parse ...
			tmp = val[1].replace(" ", "")
			saison_id = -1
			episode_id = -1
			if tmp[:6] == "Saison":
				# start with saison ...
				tmp = tmp[6:]
				parts = tmp.split("pisode")
				if len(parts) == 1:
					# only the saison ID
					saison_id = int(parts[0])
				else:
					vallllll = ""
					for vvv in parts[0]:
						if vvv not in "0123456789":
							break
						vallllll += vvv
					saison_id = int(vallllll)
					while len(parts[1]) > 0 and parts[1][0] not in "0123456789":
						parts[1] = parts[1][1:]
					episode_id = int(parts[1])
			else:
				# start with Episode
				while len(tmp) > 0 and tmp[0] not in "0123456789":
					tmp = tmp[1:]
				parts = tmp.split("Saison")
				if len(parts) == 1:
					# only the Episode ID
					episode_id = int(parts[0])
				else:
					saison_id = int(parts[1])
					episode_id = int(parts[0])
			print("        SERIE TV")
			special_element = "s"
			if saison_id == -1:
				special_element += "XX"
			elif saison_id < 10:
				special_element += "0" + str(saison_id)
			else:
				special_element += str(saison_id)
			special_element += "-e"
			if episode_id == -1:
				special_element += "XX"
			elif episode_id < 10:
				special_element += "0" + str(episode_id)
			else:
				special_element += str(episode_id)
			
			valll = val[0] + "-" + special_element + "-" + val[2]
			if valll + "." + extention != elem:
				print("        ==> rename ...")
				print("            " + elem)
				print("            " + valll + "." + extention)
				out = valll + "." + extention
				if os.path.isfile(out):
					print("            " + out + " ==> exist ...")
					offset = 0
					while offset < 98:
						offset += 1
						out = valll + "__________" + str(offset) + "." + extention
						if os.path.isfile(out):
							print("            " + out + " ==> exist ...")
						else:
							break
					if offset >= 98:
						print("            " + out + " ==> Cen not move ...")
						continue
				cmd_line = "mv " + elem.replace(" ", "\ ").replace("'", "\\'") + " " + out.replace(" ", "\ ").replace("'", "\\'")
				ret = run_command(cmd_line)
				
		else:
			print("        ??????????????")
		

for extention in ["ts","avi","mkv","mp4"]:
	list_files = get_list_of_file_in_path(".", ["*."+extention])
	
	rename_group(list_files, extention)




