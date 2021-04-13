#!/bin/bash -l

cat ./list_* | while read line
do
		mkdir $line
		for index in $(seq -w 0 13)
		do
				mv calc_*/${line}_${index}/CH4_coords.dat ${line}/CH4_coords_${index}.dat
		done
#		mv calc_*/${line}_01 ${line}/
done
