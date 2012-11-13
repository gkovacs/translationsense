#! /bin/sh
for file in Chinese/*.sgm-utf8.txt
do
	file_name="${file##Chinese/}"
	new_file_name="${file_name%%.sgm-utf8.txt}.seg.txt"
	./stanford-segmenter/segment.sh -k ctb $file UTF-8 0 > Chinese_seg/$new_file_name
done