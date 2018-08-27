#!/bin/bash

# user input
MAXLEN=1200
DESTINATION_DIR="WorkInProgress"

nb_elem=0
for i in *.JPG; do
    nb_elem=`expr $nb_elem + 1`
done
echo "number of element: $nb_elem"

idelem=0
idcover=0
zero=0

[ -d $DESTINATION_DIR ] || mkdir $DESTINATION_DIR
for iii in *.JPG; do
	echo "element $iii"
	if [ -e $iii ] ; then
		if [ $idcover -eq $zero ] ; then
			idcover=1
			echo "#egami-cutter file (" $idelem "/" $nb_elem "): " $iii " ==> " $DESTINATION_DIR/cover.png
			egami-cutter -i=$iii -o=$DESTINATION_DIR/cover.png
		else
			idelem=`expr $idelem + 1`
			echo "#egami-cutter file (" $idelem "/" $nb_elem "): " $iii " ==> " $DESTINATION_DIR/page_$idelem.png
			egami-cutter -i=$iii -o=$DESTINATION_DIR/page_$idelem.png
		fi
	fi
done


