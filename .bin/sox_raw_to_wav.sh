#!/bin/bash

listFiles=" `find . -name "*.raw"`  "

for iii in $listFiles
do
	echo "* File : '$iii' '${iii::-3}wav'"
	sox -r 48000 -e signed -b 16 -c 1 $iii ${iii::-3}wav
done

