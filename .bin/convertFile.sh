#!/bin/bash

# user input
MAXLEN=1200
RESIZE_DIR_NAME="resized_picture"

nb_elem=0
for i in *jpg *.jpeg *.JPG *.JPEG; do
    nb_elem=`expr $nb_elem + 1`
done

idelem=0

[ -d $RESIZE_DIR_NAME ] || mkdir $RESIZE_DIR_NAME
for i in *.jpg *.jpeg *.JPG *.JPEG; do
	if [ -e $i ] ; then
		idelem=`expr $idelem + 1`
		echo "#convert file (" $idelem "/" $nb_elem "): " $i " ==> " $RESIZE_DIR_NAME/$i
		convert $i -resize ${MAXLEN}x${MAXLEN} $RESIZE_DIR_NAME/$i
	fi
done


