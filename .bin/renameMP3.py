#!/usr/bin/python
#
# Desmond Cox
# April 10, 2008

"""Project Music

Renames audio files based on metadata

Usage: renameMP3.py [options]

Options:
  -d ...,   --directory=...             Specify which directory to work in 
                                        (default is the current directory)
  -f ...,   --format=...                Specify the naming format
  -l,       --flatten                   Move all files into the same root
                                        directory
  -r,       --recursive                 Work recursively on the specified 
                                        directory
  -t,       --test                      Only display the new file names; nothing
                                        will be renamed
  -h,       --help                      Display this help
  
Formatting:
  The following information is available to be used in the file name:
  album    artist    title    track
  
  To specify a file name format, enter the desired format enclosed in quotation
  marks. The words album, artist, title, and track will be replaced by values
  retrieved from the audio file's metadata.
  
  For example, --format="artist - album [track] title" will rename music files
  with the name format:
  Sample Artist - Sample Album [1] Sample Title
  
  The following characters are of special importance to the operating system 
  and cannot be used in the file name:
  \    :    *    ?    "    <    >    |

  (=) is replaced by the directory path separator, so to move files into
  artist and album subdirectories, the following format can be used:
  "artist(=)album(=)track - title"
  
  If no format is provided, the default format is the same as used in the above
  example.

Examples:
  renameMP3.py                       Renames music files in the current 
                                     directory
  renameMP3.py -d /music/path/       Renames music files in /music/path/
  renameMP3.py -f "title -- artist"  Renames music files in the current
                                     directory with the name format:
                                     Sample Title -- Sample Artist.mp3
  renameMP3.py -d . -r --flatten

pip install mutagen --user
pip install easyid3 --user
pip install soundscrape --user

"""

### Imports ###

import time
import re
import os
import getopt
import sys
import fnmatch

import mutagen.easyid3
import mutagen.oggvorbis

### Exceptions ###
class FormatError(Exception):
	"""
	Exception raised due to improper formatting
	"""
	pass

class DirectoryError(Exception):
	"""
	Exception raised due to a non-existent directory
	"""
	pass

### Definitions ###

def create_directory_of_file(file):
	path = os.path.dirname(file)
	try:
		os.stat(path)
	except:
		os.makedirs(path)

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

def print_mangle(data):
	out = ""
	for elem in data:
		try:
			if elem in "AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn1234567890)_-()éèà@ù!/:.;,?*µ%$£}{[]><":
				out += elem
		except:
			pass
	return out
	
##
## @brief Get list of all Files in a specific path (with a regex)
## @param[in] path (string) Full path of the machine to search files (start with / or x:)
## @param[in] regex (string) Regular expression to search data
## @param[in] recursive (bool) List file with recursive search
## @param[in] remove_path (string) Data to remove in the path
## @return (list) return files requested
##
def get_list_of_file_in_path(path, filter="*", recursive = False, remove_path=""):
	print(" ******** " + path)
	out = []
	if os.path.isdir(os.path.realpath(path)):
		tmp_path = os.path.realpath(path)
	else:
		print("[E] path does not exist : '" + str(path) + "'")
	last_x = 0
	for root, dirnames, file_names in os.walk(tmp_path):
		deltaRoot = root[len(tmp_path):]
		while     len(deltaRoot) > 0 \
		      and (    deltaRoot[0] == '/' \
		            or deltaRoot[0] == '\\' ):
			deltaRoot = deltaRoot[1:]
		clear_line()
		print("[I] path: '" + print_mangle(str(deltaRoot)) + "'", end="")
		#ilter some stupid path ... thumbnails=>perso @eaDir synology
		if    ".thumbnails" in deltaRoot \
		   or "@eaDir" in deltaRoot:
			continue
		if     recursive == False \
		   and deltaRoot != "":
			return out
		tmpList = []
		for elem in filter:
			tmpppp = fnmatch.filter(file_names, elem)
			for elemmm in tmpppp:
				tmpList.append(elemmm)
		# Import the module :
		for cycleFile in tmpList:
			#for cycleFile in file_names:
			add_file = os.path.join(tmp_path, deltaRoot, cycleFile)
			if len(remove_path) != 0:
				if add_file[:len(remove_path)] != remove_path:
					print("[E] Request remove start of a path that is not the same: '" + add_file[:len(remove_path)] + "' demand remove of '" + str(remove_path) + "'")
				else:
					add_file = add_file[len(remove_path)+1:]
			out.append(add_file)
	print(" len out " + str(len(out)))
	return out;



class AudioFile:
	"""
	A generic audio file 
	"""
	def __init__(self, file_name):
		self.file_name = file_name
		self.move_folder = ""
		self.file_ext = os.path.splitext(file_name)[1].lower()
		self.file_path = os.path.split(file_name)[0] + os.path.sep
		try:
			self.data = getattr(self, "parse_%s" % self.file_ext[1:])()
		except:
			self.data = None
			self.move_folder = "zzz_error/"
		# call the appropriate method based on the file type
		if self.data == None:
			return
		self.generate()

	def generate(self):
		def lookup(key, default):
			return self.data[key][0] if ( key in self.data.keys() and 
			                              self.data[key][0] ) else default
		self.artist = lookup("artist", "No Artist")
		self.album = lookup("album", "No Album")
		self.title = lookup("title", "No Title")
		self.track = lookup("tracknumber", "0")
		if self.track != "0":
			self.track = self.track.split("/")[0].lstrip("0")
		# In regards to track numbers, self.data["tracknumber"] returns numbers 
		# in several different formats: 1, 1/10, 01, or 01/10. Wanting a 
		# consistent format, the returned string is split at the "/" and leading
		# zeros are stripped.
		try:
			if int(self.track) < 10:
				self.track = "0" + self.track
		except:
			pass
	
	def parse_mp3(self):
		data = mutagen.easyid3.EasyID3(self.file_name)
		return data

	def parse_ogg(self):
		return mutagen.oggvorbis.Open(self.file_name)

	def rename(self, newfile_name, flatten=False):
		def unique_name(newfile_name, count=0):
			"""
			Returns a unique name if a file already exists with the supplied 
			name
			"""
			c = "_(%s)" % str(count) if count else ""
			prefix = directory + os.path.sep if flatten else self.file_path
			testfile_name = prefix + newfile_name + c + self.file_ext
			if os.path.isfile(testfile_name):
				count += 1
				return unique_name(newfile_name, count)
			else:
				return testfile_name
		if self.file_name == newfile_name:
			return
		new_name = unique_name(newfile_name)
		create_directory_of_file(new_name)
		os.renames(self.file_name, new_name)
		# Note: this function is quite simple at the moment; it does not support
		# multiple file extensions, such as "sample.txt.backup", which would 
		# only retain the ".backup" file extension.

	def clean_file_name(self, format):
		"""
		Generate a clean file name based on metadata
		"""
		if self.data == None:
			return self.move_folder + self.file_name
		rawfile_name = format % {"artist": self.artist,
								"album": self.album,
								"title": self.title,
								"track": self.track}
		rawfile_name.encode("ascii", "replace")
		# encode is used to override the default encode error-handing mode;
		# which is to raise a UnicodeDecodeError
		clean_file_name = re.sub(restrictedCharPattern, "+", rawfile_name)
		# remove restricted file_name characters (\, :, *, ?, ", <, >, |) from
		# the supplied string
		if self.move_folder != "":
			clean_file_name = self.move_folder + self.move_folder

		return (self.file_name, clean_file_name.replace("(=)", os.path.sep))

### Main ###

def main(argv):
	global directory
	directory = os.getcwd()
	format = "%(artist)s/%(album)s/%(track)s-%(title)s"
	flatten = False
	recursive = False
	test = False
 
	def verifyFormat(format):
		"""
		Verify the supplied file_name format
		"""	
		if re.search(restrictedCharPattern, format):
			raise(FormatError, "supplied format contains restricted characters")

		if not re.search(formatPattern, format):
			raise(FormatError, "supplied format does not contain any metadata keys")
			# the supplied format must contain at least one of "artist", 
			# "album", "title", or "track", or all files will be named 
			# identically
		
		format = format.replace("artist", "%(artist)s")
		format = format.replace("album", "%(album)s")
		format = format.replace("title", "%(title)s")
		format = format.replace("track", "%(track)s")
		return format
		
	def verifyDirectory(directory):
		"""
		Verify the supplied directory path
		"""
		if os.path.isdir(directory):
			return os.path.abspath(directory)
		
		else:
			raise(DirectoryError, "supplied directory cannot be found")
	
	def usage():
		print(__doc__)
	
	try:
		opts, args = getopt.getopt(argv, "d:f:hlrt", ["directory=", 
													  "format=", 
													  "help", 
													  "flatten", 
													  "recursive", 
													  "test"])
	except getopt.error:
		usage()
		print("\n***Error: %s***" % error)
		sys.exit(1)
	except error:
		usage()
		print("\n***Error: %s***" % error)
		sys.exit(1)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-f", "--format"):
			try:
				format = verifyFormat(arg)
			except FormatError:
				print("\n***Error: %s***" % error)
				sys.exit(2)
			except error:
				print("\n***Error: %s***" % error)
				sys.exit(2)
		elif opt in ("-d", "--directory"):
			"""
			try:
				directory = verifyDirectory(arg)
			
			except DirectoryError:
				print("\n***Error: %s***" % error)
				sys.exit(3)
			except error:
				print("\n***Error: %s***" % error)
				sys.exit(3)
			"""
			directory = arg
		elif opt in ("-l", "--flatten"):
			flatten = True
		elif opt in ("-r", "--recursive"):
			recursive = True
		elif opt in ("-t", "--test"):
			test = True
	work(directory, format, flatten, recursive, test)

def safety(message):
	print("\n***Attention: %s***" % message)
	#safety = raw_input("Enter 'ok' to continue (any other response will abort): ")
	safety = "ok"
	if safety.lower().strip() != "ok":
		print("\n***Attention: aborting***")
		sys.exit()



def work(directory, format, flatten, recursive, test):
	#fileList = get_list_of_file_in_path(directory, [".mp3", ".ogg"], recursive)
	fileList = get_list_of_file_in_path(directory, ["*.*"], recursive=recursive)
	try:
		if test:
			safety("testing mode; nothing will be renamed")
			print("\n***Attention: starting***")
			for f in fileList:
				current = AudioFile(f)
				print(current.clean_file_name(format))
				
		else:
			count = 0
			total = len(fileList)
			safety("all audio files in %s will be renamed : %d " % (directory, total))
			print("\n***Attention: starting***")
			start = time.time()
			for file in fileList:
				count += 1
				current = AudioFile(file)
				src_file_name, new_tmp_file_name = current.clean_file_name(format)
				if src_file_name == new_tmp_file_name:
					continue
				current.rename(new_tmp_file_name, flatten)
				new_tmp_file_name = print_mangle(new_tmp_file_name)
				print("Renamed %d of %d : %s" % (count, total, new_tmp_file_name))
			print("\n%d files renamed in %f seconds" % (len(fileList), 
														time.time() - start))
	except:
		print("\n***Error: %s***" % file)
		raise
		
if __name__ == "__main__":
	restrictedCharPattern = re.compile('[\\\:\*\?"<>\|]')
	formatPattern = re.compile('artist|album|title|track')

	main(sys.argv[1:])
