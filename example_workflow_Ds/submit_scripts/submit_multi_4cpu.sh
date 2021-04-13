#!/bin/bash

list='list_5str'
stime=72 # hours
cpu=4
num=`cat $list | wc -l`
node=$((${num}*${cpu}/2-1)) # str*14*cpu/28
task_per_node=$((28/${cpu}))

echo $num
echo $node 
echo ${task_per_node}

rm -rf calc_* list_calc

for line in $(cat ./${list})
do
		for index in `seq -w 0 1 13`
		do
			echo ${line}_${index} >> list_calc
		done
done

for n in `seq -w 0 1 ${node}`
do
		echo $n
  		dir_name=calc_${n}
  		mkdir $dir_name
 		head -n ${task_per_node} list_calc | while read line
 		do
				mv ${line} ${dir_name}/
 				echo ${line}
 		done
		sed -i -e "1,${task_per_node}d" list_calc
done

# # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # 

for dir in calc_*
do 
	cd $dir
	# submit and configure files
	# "job_lammps"
	cat > job_lammps << EOF
#!/bin/bash -l

#SBATCH --chdir ./ 
#SBATCH --nodes 1
#SBATCH --ntasks 28
#SBATCH --mem 28672
#SBATCH --time ${stime}:00:00

module purge
module load intel intel-mpi intel-mkl
export OMP_NUM_THREADS=4

for dir in linker*
do
	cd \$dir
	srun -n 4 --exclusive --mem=4G /home/hxu/Utils/lammps-12Dec18_dof/src/lmp_mpi -in in.COF &
	cd ..
done

wait
EOF
 	cd ..
done
# 	# "task_*"
# 	i=0
# 	for subdir in linker*
# 	do
# 		cat > task_$i << EOF
# #!/bin/bash
# 
# module purge
# module load intel intel-mpi intel-mkl
# export OMP_NUM_THREADS=$cpu
# 
# cd $subdir
# srun /home/hxu/Utils/lammps-12Dec18/src/lmp_mpi -in in.COF
# cd ..
# 
# EOF
# 		chmod +x task_*
# 		let "i++"
# 	done
