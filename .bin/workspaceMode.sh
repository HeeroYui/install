#!/bin/bash

dir=`pwd`
dir="$1/plop"
while [ $dir != "/" ] ; do
	dir="$(dirname "$dir")"
	if [ -e "$dir/.bashTitle.txt" ] ; then
		#echo "find=$dir/.bashTitle.txt"
		out="$(cat $dir/.bashTitle.txt | tr -d '\n')"
		echo -en $out
		break
	fi
	#echo "dir=$dir"
done

