#!/usr/bin/env python2
import glob as glob
import os as os
import re
import shutil as shutil
import signal as signal
import subprocess as sp
import sys as sys
from lib import build 
from lib import setup
from lib import scripts 
from lib import analysis 

pmf_dist = []
rest_wgt = []
components = []  

a_steps1 = 0
a_steps2 = 0
l_steps1 = 0
l_steps2 = 0
t_steps1 = 0
t_steps2 = 0
c_steps1 = 0
c_steps2 = 0
r_steps1 = 0
r_steps2 = 0
u_steps1 = 0
u_steps2 = 0
m_steps1 = 0
m_steps2 = 0
n_steps1 = 0
n_steps2 = 0

# Read arguments that define input file and stage
if len(sys.argv) < 5:
  scripts.help_message()
  sys.exit(0)
for i in [1, 3]:
  if '-i' == sys.argv[i].lower():
    input_file = sys.argv[i + 1]
  elif '-s' == sys.argv[i].lower():
    stage = sys.argv[i + 1]
  else:
    scripts.help_message()
    sys.exit(1)

# Open input file
with open(input_file) as f_in:       
    # Remove spaces and tabs
    lines = (line.strip(' \t\n\r') for line in f_in)
    lines = list(line for line in lines if line)  # Non-blank lines in a list

for i in range(0, len(lines)):
    # split line using the equal sign, and remove text after #
    if not lines[i][0] == '#':
        lines[i] = lines[i].split('#')[0].split('=')

# Read parameters from input file 
for i in range(0, len(lines)):
    if not lines[i][0] == '#':
        lines[i][0] = lines[i][0].strip().lower()
        lines[i][1] = lines[i][1].strip()
        if lines[i][0] == 'temperature':
            temperature = scripts.check_input('float', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'eq_steps':
            eq_steps = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'smd_steps':
            smd_steps = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'a_steps1':
            a_steps1 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'a_steps2':
            a_steps2 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'l_steps1':
            l_steps1 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'l_steps2':
            l_steps2 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 't_steps1':
            t_steps1 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 't_steps2':
            t_steps2 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'u_steps1':
            u_steps1 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'u_steps2':
            u_steps2 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'c_steps1':
            c_steps1 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'c_steps2':
            c_steps2 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'r_steps1':
            r_steps1 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'r_steps2':
            r_steps2 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'm_steps1':
            m_steps1 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'm_steps2':
            m_steps2 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'n_steps1':
            n_steps1 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'n_steps2':
            n_steps2 = scripts.check_input('int', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'system':
            system = lines[i][1]
        elif lines[i][0] == 'rec_chain':
            rec_chain = lines[i][1]
        elif lines[i][0] == 'lig_chain':
            lig_chain = lines[i][1]
        elif lines[i][0] == 'fe_type':
            if lines[i][1].lower() == 'rest':
                fe_type = lines[i][1].lower()
            elif lines[i][1].lower() == 'pmf':
                fe_type = lines[i][1].lower()
            elif lines[i][1].lower() == 'all':
                fe_type = lines[i][1].lower()
            elif lines[i][1].lower() == 'express':
                fe_type = lines[i][1].lower()
            elif lines[i][1].lower() == 'merged':
                fe_type = lines[i][1].lower()
            elif lines[i][1].lower() == 'custom':
                fe_type = lines[i][1].lower()
            else:
                print('Free energy type not recognized, please choose all, rest (restraints only), pmf (umbrella sampling only), or custom')
                sys.exit(1)
        elif lines[i][0] == 'blocks':
            blocks = scripts.check_input('int', lines[i][1], input_file, lines[i][0])
        elif lines[i][0] == 'num_sim':
            num_sim = scripts.check_input('int', lines[i][1], input_file, lines[i][0])
        elif lines[i][0] == 'water_model':
            if lines[i][1].lower() == 'tip3p':
                water_model = lines[i][1].upper()
            elif lines[i][1].lower() == 'tip4pew':
                water_model = lines[i][1].upper()
            elif lines[i][1].lower() == 'spce':
                water_model = lines[i][1].upper()
            else:
                print('Water model not supported. Please choose TIP3P, TIP4PEW or SPCE')
                sys.exit(1)
        elif lines[i][0] == 'neutralize_only':
            if lines[i][1].lower() == 'yes':
                neut = 'yes'
            elif lines[i][1].lower() == 'no':
                neut = 'no'
            else:
                print('Wrong input! Please choose neutralization only or add extra ions')
                sys.exit(1)
        elif lines[i][0] == 'cation':
            cation = lines[i][1]
        elif lines[i][0] == 'anion':
            anion = lines[i][1]
        elif lines[i][0] == 'ion_conc':
            ion_conc = scripts.check_input('float', lines[i][1], input_file, lines[i][0])
        elif lines[i][0] == 'boxsize_x':
            boxsize_x = scripts.check_input('float', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'boxsize_y':
            boxsize_y = scripts.check_input('float', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'boxsize_z':
            boxsize_z = scripts.check_input('float', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'box_z_center':
            box_z_center = scripts.check_input('float', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'boxsize_ligand':
            boxsize_ligand = scripts.check_input('float', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'rec_trans_force':
            rec_trans_force = scripts.check_input('float', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'rec_orient_force':
            rec_orient_force = scripts.check_input('float', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'rec_rmsd_force':
            rec_rmsd_force = scripts.check_input('float', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'lig_trans_force':
            lig_trans_force = scripts.check_input('float', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'lig_orient_force':
            lig_orient_force = scripts.check_input('float', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'lig_rmsd_force':
            lig_rmsd_force = scripts.check_input('float', lines[i][1], input_file, lines[i][0]) 
        elif lines[i][0] == 'pmf_dist':
            strip_line = lines[i][1].strip('\'\"-,.:;#()][').split()
            for j in range(0, len(strip_line)):
                pmf_dist.append(scripts.check_input('float', strip_line[j], input_file, lines[i][0]))
        elif lines[i][0] == 'rest_wgt':
            strip_line = lines[i][1].strip('\'\"-,.:;#()][').split()
            for j in range(0, len(strip_line)):
                rest_wgt.append(scripts.check_input('float', strip_line[j], input_file, lines[i][0]))
        elif lines[i][0] == 'components':
            strip_line = lines[i][1].strip('\'\"-,.:;#()][').split()
            for j in range(0, len(strip_line)):
                components.append(strip_line[j])
        elif lines[i][0] == 'rec_restr':
            rec_restr = lines[i][1]
        elif lines[i][0] == 'lig_restr':
            lig_restr = lines[i][1]
        elif lines[i][0] == 'restartfreq':
            rstfreq = lines[i][1]
        elif lines[i][0] == 'dcdfreq':
            dcdfreq = lines[i][1]
        elif lines[i][0] == 'xstfreq':
            xstfreq = lines[i][1]
        elif lines[i][0] == 'outputpressure':
            outpr = lines[i][1]
        elif lines[i][0] == 'outputenergies':
            outen = lines[i][1]
        elif lines[i][0] == 'colvarstrajfrequency':
            clvfr = lines[i][1]
        elif lines[i][0] == 'cutoff':
            cutoff = lines[i][1]
        elif lines[i][0] == 'langevindamping':
            gamma = lines[i][1]
        elif lines[i][0] == 'timestep':
            tstep = lines[i][1]
        elif lines[i][0] == 'force_field':
            ffield = lines[i][1]


# Define free energy components
if fe_type == 'rest':
  components = ['c', 'a', 'l', 't', 'r'] 
elif fe_type == 'pmf':
  components = ['u'] 
elif fe_type == 'all':
  components = ['c', 'a', 'l', 't', 'r', 'u'] 
elif fe_type == 'express':
  components = [ 'm', 'n', 'u' ] 
elif fe_type == 'merged':
  components = [ 'm', 'n' ] 

# Define number of steps for all stages
dic_steps1 = {}
dic_steps2 = {}
dic_steps1['a'] = a_steps1
dic_steps2['a'] = a_steps2
dic_steps1['l'] = l_steps1
dic_steps2['l'] = l_steps2
dic_steps1['t'] = t_steps1
dic_steps2['t'] = t_steps2
dic_steps1['c'] = c_steps1
dic_steps2['c'] = c_steps2
dic_steps1['r'] = r_steps1
dic_steps2['r'] = r_steps2
dic_steps1['m'] = m_steps1
dic_steps2['m'] = m_steps2
dic_steps1['n'] = n_steps1
dic_steps2['n'] = n_steps2
dic_steps1['u'] = u_steps1
dic_steps2['u'] = u_steps2


# Create restraint definitions
rest = [rec_trans_force, rec_orient_force, rec_rmsd_force, lig_trans_force, lig_orient_force, lig_rmsd_force]

# Create boxsize definitions
boxsize = [boxsize_x, boxsize_y, boxsize_z, box_z_center, boxsize_ligand]

# Create ion definitions
ion_def = [cation, anion, ion_conc]

if stage == 'equil':
    print('Setting up '+str(system))
    # Create aligned initial complex
    build.build_equil(system, rec_chain, lig_chain, water_model, boxsize, neut, ion_def)
    # Prepare simulation files
    setup.sim_equil(system, rest, boxsize, rec_chain, temperature, eq_steps, rstfreq, dcdfreq, xstfreq, outpr, outen, clvfr, cutoff, gamma, tstep, ffield)
elif stage == 'smd':
    print('Setting up '+str(system))
    # Prepare simulation files
    setup.sim_smd(system, rest, boxsize, rec_chain, rec_restr, lig_chain, lig_restr, temperature, smd_steps, pmf_dist, rstfreq, dcdfreq, xstfreq, outpr, outen, clvfr, cutoff, gamma, tstep, ffield)
elif stage == 'fe':
    print('Setting up '+str(system))
    # Prepare simulation files
    for j in range(0, len(components)):
      comp = components[j]
      if (comp != 'r' and comp != 'c'):
        steps1 = dic_steps1[comp]
        steps2 = dic_steps2[comp]
        setup.sim_fe(comp, system, rest, water_model, boxsize, neut, ion_def, rec_chain, lig_chain, lig_restr, temperature, steps1, steps2, pmf_dist, rest_wgt, num_sim, rstfreq, dcdfreq, xstfreq, outpr, outen, clvfr, cutoff, gamma, tstep, ffield)
      elif (comp == 'r'):
        steps1 = dic_steps1[comp]
        steps2 = dic_steps2[comp]
        setup.sim_rec(comp, system, rest, water_model, boxsize, neut, ion_def, rec_chain, rec_restr, temperature, steps1, steps2, rest_wgt, num_sim, rstfreq, dcdfreq, xstfreq, outpr, outen, clvfr, cutoff, gamma, tstep, ffield)
      elif (comp == 'c'):
        steps1 = dic_steps1[comp]
        steps2 = dic_steps2[comp]
        setup.sim_lig(comp, system, rest, water_model, boxsize_ligand, neut, ion_def, lig_chain, lig_restr, temperature, steps1, steps2, rest_wgt, num_sim, rstfreq, dcdfreq, xstfreq, outpr, outen, clvfr, cutoff, gamma, tstep, ffield)
elif stage == 'analysis':
  # Free energies MBAR and analytical calculations
  analysis.fe_values(blocks, components, temperature, system, rest_wgt, rest, pmf_dist)
  os.chdir('../../')

