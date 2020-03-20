###===================
#!/bin/bash
#PBS -l select=1:ncpus=1:mem=6gb:pcmem=6gb -l walltime=20:00:00
#PBS -l cput=20:00:00
#PBS -q high_pri
#PBS -W group_list=mstrout
###-------------------

echo "Node name:"
hostname

cd /extra/abureyanahmed/spanner_ml
module load python/3.5/3.5.5
python3 create_data.py training_data4.txt 100000
python3 create_data.py testing_data4.txt 100000
python3 run_mlp.py training_data4.txt testing_data4.txt


