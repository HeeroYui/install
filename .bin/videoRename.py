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


list_auto_replace = [
	"Chuggington",
	"Caliméro",
	"Le livre de la jungle",
	"Barbapapa",
	"Oum le dauphin blanc",
	"Les Minijusticiers",
	"Octonauts",
	"Les Enquêtes de Mirette",
	"Julius Jr",
	"Paw Patrol, la Pat'Patrouille",
	"Rusty Rivets"
	]

def change_order_special(data):
	basic_dir = os.path.dirname(data)
	tmp = os.path.basename(data)
	for elem in list_auto_replace:
		if tmp[-len(elem)-3:] == " - " + elem:
			tmp = elem + " - " + tmp[:-len(elem)-3]
			print("")
			print("")
			print("")
			print("")
			print("")
			print("*************************************************************************")
			print("replace : " + data)
			print("        : " + os.path.join(basic_dir,tmp))
			return os.path.join(basic_dir,tmp)
	return data


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
	val = data.split("_Arte_")
	if len(val) == 2:
		return val[0]
	return data

def replace_generic_saison_and_name(data):
	for elem in [ "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
		data = data.replace("S0" + elem + "E01", "- Saison " + elem + " Episode 1 -");
		data = data.replace("S0" + elem + "E02", "- Saison " + elem + " Episode 2 -");
		data = data.replace("S0" + elem + "E03", "- Saison " + elem + " Episode 3 -");
		data = data.replace("S0" + elem + "E04", "- Saison " + elem + " Episode 4 -");
		data = data.replace("S0" + elem + "E05", "- Saison " + elem + " Episode 5 -");
		data = data.replace("S0" + elem + "E06", "- Saison " + elem + " Episode 6 -");
		data = data.replace("S0" + elem + "E07", "- Saison " + elem + " Episode 7 -");
		data = data.replace("S0" + elem + "E08", "- Saison " + elem + " Episode 8 -");
		data = data.replace("S0" + elem + "E09", "- Saison " + elem + " Episode 9 -");
		data = data.replace("S0" + elem + "E10", "- Saison " + elem + " Episode 10 -");
		data = data.replace("S0" + elem + "E11", "- Saison " + elem + " Episode 11 -");
		data = data.replace("S0" + elem + "E12", "- Saison " + elem + " Episode 12 -");
		data = data.replace("S0" + elem + "E13", "- Saison " + elem + " Episode 13 -");
		data = data.replace("S0" + elem + "E14", "- Saison " + elem + " Episode 14 -");
		data = data.replace("S0" + elem + "E15", "- Saison " + elem + " Episode 15 -");
		data = data.replace("S0" + elem + "E16", "- Saison " + elem + " Episode 16 -");
		data = data.replace("S0" + elem + "E17", "- Saison " + elem + " Episode 17 -");
		data = data.replace("S0" + elem + "E18", "- Saison " + elem + " Episode 18 -");
		data = data.replace("S0" + elem + "E19", "- Saison " + elem + " Episode 19 -");
		data = data.replace("S0" + elem + "E20", "- Saison " + elem + " Episode 20 -");
		data = data.replace("S0" + elem + "E21", "- Saison " + elem + " Episode 21 -");
		data = data.replace("S0" + elem + "E22", "- Saison " + elem + " Episode 22 -");
		data = data.replace("S0" + elem + "E23", "- Saison " + elem + " Episode 23 -");
		data = data.replace("S0" + elem + "E24", "- Saison " + elem + " Episode 24 -");
		data = data.replace("S0" + elem + "E25", "- Saison " + elem + " Episode 25 -");
		data = data.replace("S0" + elem + "E26", "- Saison " + elem + " Episode 26 -");
		data = data.replace("S0" + elem + "E27", "- Saison " + elem + " Episode 27 -");
		data = data.replace("S0" + elem + "E28", "- Saison " + elem + " Episode 28 -");
		data = data.replace("S0" + elem + "E29", "- Saison " + elem + " Episode 29 -");
		data = data.replace("S0" + elem + "E30", "- Saison " + elem + " Episode 30 -");
		data = data.replace("S0" + elem + "E31", "- Saison " + elem + " Episode 31 -");
		data = data.replace("S0" + elem + "E32", "- Saison " + elem + " Episode 32 -");
		data = data.replace("S0" + elem + "E33", "- Saison " + elem + " Episode 33 -");
		data = data.replace("S0" + elem + "E34", "- Saison " + elem + " Episode 34 -");
		data = data.replace("S0" + elem + "E35", "- Saison " + elem + " Episode 35 -");
		data = data.replace("S0" + elem + "E36", "- Saison " + elem + " Episode 36 -");
		data = data.replace("S0" + elem + "E37", "- Saison " + elem + " Episode 37 -");
		data = data.replace("S0" + elem + "E38", "- Saison " + elem + " Episode 38 -");
		data = data.replace("S0" + elem + "E39", "- Saison " + elem + " Episode 39 -");
		data = data.replace("S0" + elem + "E40", "- Saison " + elem + " Episode 40 -");
		data = data.replace("S0" + elem + "E41", "- Saison " + elem + " Episode 41 -");
		data = data.replace("S0" + elem + "E42", "- Saison " + elem + " Episode 42 -");
		data = data.replace("S0" + elem + "E43", "- Saison " + elem + " Episode 43 -");
		data = data.replace("S0" + elem + "E44", "- Saison " + elem + " Episode 44 -");
		data = data.replace("S0" + elem + "E45", "- Saison " + elem + " Episode 45 -");
		data = data.replace("S0" + elem + "E46", "- Saison " + elem + " Episode 46 -");
		data = data.replace("S0" + elem + "E47", "- Saison " + elem + " Episode 47 -");
		data = data.replace("S0" + elem + "E48", "- Saison " + elem + " Episode 48 -");
		data = data.replace("S0" + elem + "E49", "- Saison " + elem + " Episode 49 -");
		data = data.replace("S0" + elem + "E50", "- Saison " + elem + " Episode 50 -");
		data = data.replace("S0" + elem + "E51", "- Saison " + elem + " Episode 51 -");
		data = data.replace("S0" + elem + "E52", "- Saison " + elem + " Episode 52 -");
		data = data.replace("S0" + elem + "E53", "- Saison " + elem + " Episode 53 -");
		data = data.replace("S0" + elem + "E54", "- Saison " + elem + " Episode 54 -");
		data = data.replace("S0" + elem + "E55", "- Saison " + elem + " Episode 55 -");
		data = data.replace("S0" + elem + "E56", "- Saison " + elem + " Episode 56 -");
		data = data.replace("S0" + elem + "E57", "- Saison " + elem + " Episode 57 -");
		data = data.replace("S0" + elem + "E58", "- Saison " + elem + " Episode 58 -");
		data = data.replace("S0" + elem + "E59", "- Saison " + elem + " Episode 59 -");
		data = data.replace("S0" + elem + "E60", "- Saison " + elem + " Episode 60 -");
		data = data.replace("S0" + elem + "E61", "- Saison " + elem + " Episode 61 -");
		data = data.replace("S0" + elem + "E62", "- Saison " + elem + " Episode 62 -");
		data = data.replace("S0" + elem + "E63", "- Saison " + elem + " Episode 63 -");
		data = data.replace("S0" + elem + "E64", "- Saison " + elem + " Episode 64 -");
		data = data.replace("S0" + elem + "E65", "- Saison " + elem + " Episode 65 -");
		data = data.replace("S0" + elem + "E66", "- Saison " + elem + " Episode 66 -");
		data = data.replace("S0" + elem + "E67", "- Saison " + elem + " Episode 67 -");
		data = data.replace("S0" + elem + "E68", "- Saison " + elem + " Episode 68 -");
		data = data.replace("S0" + elem + "E69", "- Saison " + elem + " Episode 69 -");
		data = data.replace("S0" + elem + "E70", "- Saison " + elem + " Episode 70 -");
		data = data.replace("S0" + elem + "E71", "- Saison " + elem + " Episode 71 -");
		data = data.replace("S0" + elem + "E72", "- Saison " + elem + " Episode 72 -");
		data = data.replace("S0" + elem + "E73", "- Saison " + elem + " Episode 73 -");
		data = data.replace("S0" + elem + "E74", "- Saison " + elem + " Episode 74 -");
		data = data.replace("S0" + elem + "E75", "- Saison " + elem + " Episode 75 -");
		data = data.replace("S0" + elem + "E76", "- Saison " + elem + " Episode 76 -");
		data = data.replace("S0" + elem + "E77", "- Saison " + elem + " Episode 77 -");
		data = data.replace("S0" + elem + "E78", "- Saison " + elem + " Episode 78 -");
		data = data.replace("S0" + elem + "E79", "- Saison " + elem + " Episode 79 -");
		data = data.replace("S0" + elem + "E80", "- Saison " + elem + " Episode 80 -");
		data = data.replace("S0" + elem + "E81", "- Saison " + elem + " Episode 81 -");
		data = data.replace("S0" + elem + "E82", "- Saison " + elem + " Episode 82 -");
		data = data.replace("S0" + elem + "E83", "- Saison " + elem + " Episode 83 -");
		data = data.replace("S0" + elem + "E84", "- Saison " + elem + " Episode 84 -");
		data = data.replace("S0" + elem + "E85", "- Saison " + elem + " Episode 85 -");
		data = data.replace("S0" + elem + "E86", "- Saison " + elem + " Episode 86 -");
		data = data.replace("S0" + elem + "E87", "- Saison " + elem + " Episode 87 -");
		data = data.replace("S0" + elem + "E88", "- Saison " + elem + " Episode 88 -");
		data = data.replace("S0" + elem + "E89", "- Saison " + elem + " Episode 89 -");
		data = data.replace("S0" + elem + "E90", "- Saison " + elem + " Episode 90 -");
		data = data.replace("S0" + elem + "E91", "- Saison " + elem + " Episode 91 -");
		data = data.replace("S0" + elem + "E92", "- Saison " + elem + " Episode 92 -");
		data = data.replace("S0" + elem + "E93", "- Saison " + elem + " Episode 93 -");
		data = data.replace("S0" + elem + "E94", "- Saison " + elem + " Episode 94 -");
		data = data.replace("S0" + elem + "E95", "- Saison " + elem + " Episode 95 -");
		data = data.replace("S0" + elem + "E96", "- Saison " + elem + " Episode 96 -");
		data = data.replace("S0" + elem + "E97", "- Saison " + elem + " Episode 97 -");
		data = data.replace("S0" + elem + "E98", "- Saison " + elem + " Episode 98 -");
		data = data.replace("S0" + elem + "E99", "- Saison " + elem + " Episode 99 -");
	return data

def rename_group(list_element, extention):
	for elem in list_files:
		reduced_name = rm_date(elem[:-(len(extention)+1)])
		reduced_name = change_order_special(reduced_name)
		reduced_name = replace_generic_saison_and_name(reduced_name)
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




