#!/bin/bash

listFiles=" `find . -name "*.php"`  "
listFiles+=" `find . -name "*.java"`  "
listFiles+=" `find . -name "*.cpp"`  "
listFiles+=" `find . -name "*.cxx"`  "
listFiles+=" `find . -name "*.c"`  "
listFiles+=" `find . -name "*.h"` "
listFiles+=" `find . -name "*.hpp"` "
listFiles+=" `find . -name "*.hxx"` "
listFiles+=" `find . -name "*.inl"` "
listFiles+=" `find . -name "*.java"` "
listFiles+=" `find . -name "*.m"` "
listFiles+=" `find . -name "*.mm"` "
listFiles+=" `find . -name "*.mk"` "
listFiles+=" `find . -name "*.md"` "
listFiles+=" `find . -name "*.js"` "
listFiles+=" `find . -name "*.pro"` "
listFiles+=" `find . -name "*.qml"` "
listFiles+=" `find . -name "*.qrc"` "
listFiles+=" `find . -name "*.xml"` "
listFiles+=" `find . -name "*.json"` "
listFiles+=" `find . -name "*.py"` "
listFiles+=" `find . -name "*.rst"` "
listFiles+=" `find . -name "*.in"` "
listFiles+=" `find . -name "*.txt"` "
listFiles+=" `find . -name "*.cfg"` "

echo "Replace : \"$1\" ==> \"$2\""

for iii in $listFiles
do
	echo "* File : "$iii
	sed -ri "s|$1|$2|" $iii
	#sed -ri 'N; s/[ \t]*\n[\t ]*else/ else/' $iii
	#sed -ri 'N; s/[ \t]*\n[\t ]*\{/ \{/' $iii
	#sed -ri 'N; s/[ \t]*\n[\t ]*\{/ \{/' $iii
	#sed -ri 'N; s/[ \t]*\n[\t ]*\{/ \{/' $iii
	#sed -ri 'N; s/[ \t]*\n[\t ]*\{/ \{/' $iii
done

