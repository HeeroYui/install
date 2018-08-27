#!/bin/bash

echo "Download all epub of www.feedbooks.com/book/xxx.epub"
#for iii in {0..5000}
#do
#    echo "* File : "$iii
#    #wget --content-disposition -t 1 --timeout=5 www.feedbooks.com/book/$iii.epub
#done

for iii in {2961..0}
do
    echo "* File : "$iii
    wget --content-disposition -t 1 --timeout=5 www.ebooksgratuits.com/newsendbook.php?id=$iii\&format=epub
done

