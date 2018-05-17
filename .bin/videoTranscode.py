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
def get_list_of_file_in_path(path, regex="*", recursive = False, remove_path=""):
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

#ffmpeg -i 000.ts -threads 0 -vcodec libx264 -crf 20 -force_key_frames expr:gte\(t,n_forced*1\) -s 720x540 -acodec mp2 -ac 2 -ab 192k -ar 48000 -async 1 -deinterlace 000_transcoded.ts
#ffmpeg -i 000.ts -threads 0 -vcodec libx264 -crf 20 -force_key_frames expr:gte\(t,n_forced*1\) -acodec mp2 -ac 2 -ab 192k -ar 48000 -async 1 -deinterlace 000_transcoded.ts

list_files_ts = get_list_of_file_in_path('.', "*.ts")
list_files_flv = get_list_of_file_in_path('.', "*.flv")
list_files_mp4 = get_list_of_file_in_path('.', "*.mp4")
list_files_avi = get_list_of_file_in_path('.', "*.avi")
list_files_mkv = get_list_of_file_in_path('.', "*.mkv")
list_files_wmv = get_list_of_file_in_path('.', "*.wmv")

# remove all encoded element in the other files (TS)
for elem_mkv in list_files_mkv:
	index = 0
	for elem_ts in list_files_ts:
		if elem_mkv[:-3]+"ts" == elem_ts:
			break;
		index += 1
	if index != len(list_files_ts):
		print("[INFO] remove from list '" + list_files_ts[index] + "' ==> already transcoded")
		del list_files_ts[index]



# remove all encoded element in the other files (FLV)
for elem_mkv in list_files_mkv:
	index = 0
	for elem_flv in list_files_flv:
		if elem_mkv[:-3]+"flv" == elem_flv:
			break;
		index += 1
	if index != len(list_files_flv):
		print("[INFO] remove from list '" + list_files_flv[index] + "' ==> already transcoded")
		del list_files_flv[index]


# remove all encoded element in the other files (mp4)
for elem_mkv in list_files_mkv:
	index = 0
	for elem_mp4 in list_files_mp4:
		if elem_mkv[:-3]+"mp4" == elem_mp4:
			break;
		index += 1
	if index != len(list_files_mp4):
		print("[INFO] remove from list '" + list_files_mp4[index] + "' ==> already transcoded")
		del list_files_mp4[index]


# remove all encoded element in the other files (TS)
for elem_mkv in list_files_mkv:
	index = 0
	for elem_avi in list_files_avi:
		if elem_mkv[:-3]+"ts" == elem_avi:
			break;
		index += 1
	if index != len(list_files_avi):
		print("[INFO] remove from list '" + list_files_avi[index] + "' ==> already transcoded")
		del list_files_avi[index]


# remove all encoded element in the other files (TS)
for elem_mkv in list_files_mkv:
	index = 0
	for elem_wmv in list_files_wmv:
		if elem_mkv[:-3]+"wmv" == elem_wmv:
			break;
		index += 1
	if index != len(list_files_wmv):
		print("[INFO] remove from list '" + list_files_wmv[index] + "' ==> already transcoded")
		del list_files_wmv[index]

print("list of elements TS : ")
for elem in list_files_ts:
	print("    - '" + elem + "'")
print("list of elements MP4 : ")
for elem in list_files_mp4:
	print("    - '" + elem + "'")
print("list of elements FLV : ")
for elem in list_files_flv:
	print("    - '" + elem + "'")
print("list of elements AVI : ")
for elem in list_files_avi:
	print("    - '" + elem + "'")
print("list of elements WMV : ")
for elem in list_files_wmv:
	print("    - '" + elem + "'")
print("list of elements MKV : ")
for elem in list_files_mkv:
	print("    - '" + elem + "'")



def trancode_local(list_of_file=[], extention="ts", total_count_of_file=0, offset=0) :
	print("Start strancoding: '." + extention + "' ... " + str(len(list_of_file)))
	id_elem = 0
	for elem in list_of_file:
		id_elem += 1
		print("    ========================================================================================")
		print("    == " + str(offset+id_elem) + " / " + str(total_count_of_file))
		print("    == Trancode: '" + elem.replace("'", "\'") + "'")
		print("    ========================================================================================")
		cmd_line = "ffmpeg -i "
		cmd_line += elem.replace(" ", "\ ").replace("'", "\\'")
		#cmd_line += " -threads 4 -vcodec libx264 -crf 22 -force_key_frames expr:gte\(t,n_forced*1\) -acodec mp2 -ac 2 -ab 192k -ar 48000 -async 1 -deinterlace tmp_transcoded.mkv"
		cmd_line += " -threads 4 -vcodec copy -acodec mp2 -ac 2 -ab 192k -ar 48000 -async 1 -deinterlace tmp_transcoded.mkv"
		ret = run_command(cmd_line)
		print(" ret value = " + str(ret))
		if ret == False:
			print("[ERROR]    Trancode: error occured ...")
			exit(-1)
		print("    move in: '" + elem[:-len(extention)] + "mkv'")
		cmd_line = "mv tmp_transcoded.mkv " + elem.replace(" ", "\ ").replace("'", "\\'")[:-len(extention)] + "mkv"
		ret = run_command(cmd_line)
		cmd_line = "mv " + elem.replace(" ", "\ ").replace("'", "\\'") + " last_transcoded.ts"
		ret = run_command(cmd_line)
	

offset = 0;
trancode_local(list_files_ts  , "ts",  len(list_files_ts) + len(list_files_mp4) + len(list_files_flv) + len(list_files_avi) + len(list_files_wmv), offset)
offset += len(list_files_ts);
trancode_local(list_files_mp4 , "mp4", len(list_files_ts) + len(list_files_mp4) + len(list_files_flv) + len(list_files_avi) + len(list_files_wmv), offset)
offset += len(list_files_mp4);
trancode_local(list_files_flv , "flv", len(list_files_ts) + len(list_files_mp4) + len(list_files_flv) + len(list_files_avi) + len(list_files_wmv), offset)
offset += len(list_files_flv);
trancode_local(list_files_avi , "avi", len(list_files_ts) + len(list_files_mp4) + len(list_files_flv) + len(list_files_avi) + len(list_files_wmv), offset)
offset += len(list_files_avi);
trancode_local(list_files_wmv , "wmv", len(list_files_ts) + len(list_files_mp4) + len(list_files_flv) + len(list_files_avi) + len(list_files_wmv), offset)
