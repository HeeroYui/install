#!/bin/bash


if [ -z $1 ] ; then
	echo "you must set the name of the folder to compress : $0 \"FOLDER_NAME\""
	exit -1
fi
folder=$1_`date +%Y-%m-%d_%Hh%Mm%Ss`.tar.gz

# clean tmp files:
cd $1
rm -rvf `find . -name "*~"` `find . -name "*.bck"`
cd ..
#compresse Data
tar czvf $folder $1

