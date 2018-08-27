#!/bin/bash

# user input
MAXLEN=1700
SOURCE_DIR="WorkInProgress_3"
DESTINATION_DIR="WorkInProgress_4"

nb_elem=0
for i in $SOURCE_DIR/*jpg; do
    nb_elem=`expr $nb_elem + 1`
done

idelem=0

if [ -d $SOURCE_DIR ] ; then
	echo "WIP exist ==> continue"
else
	echo "WIP does not exist ==> break"
	exit -1
fi

[ -d $DESTINATION_DIR ] || mkdir $DESTINATION_DIR

cd $SOURCE_DIR
for iii in *.jpg; do
	if [ -e $iii ] ; then
		idelem=`expr $idelem + 1`
		echo "#brightness file (" $idelem "/" $nb_elem "): " $SOURCE_DIR/$iii " ==> " $DESTINATION_DIR/$iii
		convert $iii -brightness-contrast 30x45 ../$DESTINATION_DIR/$iii
	fi
done

cd ..

