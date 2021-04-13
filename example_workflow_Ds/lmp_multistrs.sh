#!/bin/bash

# launch py3 env
source ~/venv_py3/bin/activate

cat ./list_* | while read line
do 
		echo $line
		./lmp_multitest_1str_14inp.py file.data $line
done
