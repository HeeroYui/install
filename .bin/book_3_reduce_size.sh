#!/bin/bash

# user input
MAXLEN=1700
SOURCE_DIR="WorkInProgress_2"
DESTINATION_DIR="WorkInProgress_3"

nb_elem=0
for i in $SOURCE_DIR/*png; do
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
for iii in *.png; do
	if [ -e $iii ] ; then
		idelem=`expr $idelem + 1`
		echo "#resize file (" $idelem "/" $nb_elem "): " $SOURCE_DIR/$iii " ==> " $DESTINATION_DIR/${iii::-4}.jpg
		convert $iii -resize ${MAXLEN}x${MAXLEN} ../$DESTINATION_DIR/${iii::-4}.jpg
	fi
done

cd ..

