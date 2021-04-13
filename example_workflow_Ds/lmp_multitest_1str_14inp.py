#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np

def modify_data(strname, dirname):
    # ./file.data/data.*
    with open('./file.data/data.%s'%(strname)) as fi:
        data = fi.readlines()
    
    # remove 'bond coeff'*4 and 'bonds'*4
    for i, item in enumerate(data):
        if item.startswith('Masses'):
            index_mass = i
            continue
        if item.startswith('Bond Coeffs'):
            index_bondc = i
            continue
        if item.startswith('Pair Coeffs'):
            index_pairc = i
            continue
        if item.startswith('Atoms'):
            index_atoms = i
            continue
        if item.startswith('Bonds'):
            index_bonds = i
            continue
    
    # atom type for CH4
    length_type = index_bondc-index_mass-2
    #length_pair = index_atoms-index_pairc-2
    atom_type ='           %i atom types\n'%length_type
    CH4_mass = '    %i    16.040000000 # CH4\n\n'%length_type
    CH4_pair = '    %i        0.294106        3.730000 # CH4 CH4\n\n'%length_type
    
    # write data.* file
    # line 1-3,  line 9,  line 14 afterwards
    with open('%s/data.COF'%(dirname), 'w') as fp:
        fp.writelines(data[0:3])
        fp.write(atom_type)
        fp.writelines(data[13:index_bondc-1])
        fp.write(CH4_mass)
        fp.writelines(data[index_pairc:index_atoms-1])
        fp.write(CH4_pair)
        fp.writelines(data[index_atoms:index_bonds])
    
    return length_type
        
def modify_CH4(dirname, length_type):
    # change atom type of CH4 for different structures
    CH4_coords = ['# methane\n\n', 
                '     1 atoms\n\n', 
                'Coords\n\n', 
                '     1      0.00000      0.00000      0.00000\n\n', 
                'Types\n\n', 
                '     1      %i  # CH4\n\n'%(length_type), 
                'Charges\n\n', 
                '     1      0.00000\n']
    with open('%s/CH4.molecule'%(dirname), 'w') as fp:
        fp.writelines(CH4_coords)

def modify_inp(dirname, length_type, thermostat, num_CH4, stime, temp, interaction):
    # read input template
    ## change: 
    ## 1. random seeds 2. atom type in group information
    ## 1. thermostat 2. num_CH4 3. simulation time 4. temparature 5. with/without interaction

    # open in.thermostat 
    with open('./in.%s'%thermostat) as fi:
        line_in = fi.readlines()

    # find line index for parameters
    for i, item in enumerate(line_in):
        item = item.strip()
        if item.startswith('group'):
            index_group = i
        if item.endswith('random seed'):
            index_rsd = i
        if item.endswith('CH4 inserted'):
            index_nmol = i
        if item.endswith('simulation temperature'):
            index_temp = i
        if item.endswith('10ns'):
            index_stime = i
        if item.startswith('neigh_modify'):
            index_interaction = i
    # change parameters
    line_in[index_group-1] = 'group           CH4      type    %i\n'%length_type
    line_in[index_group  ] = 'group           fram     type    1:%i\n'%(length_type-1)
    line_in[index_rsd]  = 'variable        rsd   equal %i\n'%(int(np.random.rand()*100000))

    line_in[index_nmol] = 'variable        nmol  equal %i\n'%(num_CH4)
    line_in[index_temp] = 'variable        stemp equal %f\n'%(temp)
    line_in[index_stime] = 'variable        tdc   equal %i\n'%(int(stime*1e6))
    if interaction:
#        line_in[index_interaction]='neigh_modify    exclude group CH4 CH4       # exclude pairwise interaction'
        line_in[index_interaction]='# neigh_modify    exclude group CH4 CH4\n'# exclude pairwise interaction'
    
    # write in.COF
    with open('%s/in.COF'%(dirname), 'w') as fp:
        fp.writelines(line_in)

def create_input(thermostat,NP,stime,temp,interaction,list_str,jobs):
    # create dirs for each test
    # eg: NH_16CH4_10ns_298K_include
    #     NH_16CH4_10ns_298K
    if interaction:
        dir_simu='%s_%sCH4_%sns_%sK_include'%(thermostat,NP,stime,temp)
    else:
        dir_simu='%s_%sCH4_%sns_%sK'%(thermostat,NP,stime,temp)
    os.makedirs(dir_simu)

    # create linker*_00-13 in each dir_simu for different structures
    # eg: NH_16CH4_10ns_298K/linker*_00-13
    for i_str in list_str:
        i_str=i_str.strip()
        # parallel jobs
        for index in range(jobs):
            # create linker*_00 folder
            name_dir = '%s/%s_%.2i'%(dir_simu, i_str, index)
            os.makedirs(name_dir)
            # create 3files: data.* in.* CH4.molecule
            length_type = modify_data(i_str, name_dir)
            modify_CH4(name_dir, length_type)
            modify_inp(name_dir, length_type, 
                    thermostat,NP,stime,temp,interaction)
    print('%s created'%dir_simu)

if __name__  ==  "__main__":
    # run by './lmp.py 

    # different tests
    list_thermostat = ['NH']    #'NH','langevin','csvr', in.* file required
    list_num_CH4 = [16]         # n(CH4): 16 and 32
    list_time = [10]         # simulation time 10ns, 20ns
    list_temp = [298]           # temperature 298K

    # structures files
    path_data=['./file.data']
    list_structure=open('./list_5str').readlines()   # only 1 str for test
    core = 14           # parallel jobs

    for i_thermo in list_thermostat:
        for i_num in list_num_CH4:
            for i_time in list_time:
                for i_temp in list_temp:
                        # True for interacting particles
                        # False for non-interacting particles
                        create_input(i_thermo,i_num,i_time,i_temp,True, list_structure,core)
                        create_input(i_thermo,i_num,i_time,i_temp,False,list_structure,core)

