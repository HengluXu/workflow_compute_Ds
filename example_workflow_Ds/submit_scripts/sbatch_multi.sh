#!/bin/bash -l

for dir in calc_*
do
		cd $dir
		sbatch job*
		cd ..
done
