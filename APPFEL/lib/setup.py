#!/usr/bin/env python2
import datetime as dt
import glob as glob
import os as os
import re as re
import shutil as shutil
import signal as signal
import subprocess as sp
import sys as sys
from lib import scripts as scripts
from lib import build as build

def sim_equil(system, rest, boxsize, rec_chain, temperature, eq_steps, rstfreq, dcdfreq, xstfreq, outpr, outen, clvfr, cutoff, gamma, tstep, ffield):


    # Create simulation directory
    if os.path.exists('namd_files'):
      shutil.rmtree('./namd_files')
    try:
      shutil.copytree('../namd_files', './namd_files')
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)
    for dname, dirs, files in os.walk('./namd_files'):
      for fname in files:
        fpath = os.path.join(dname, fname)
        with open(fpath) as f:
          s = f.read()
          s = s.replace('TEMP', '%5.2f' %temperature).replace('EQUIL_STEPS', '%8.0f' %eq_steps).replace('CUTOFF', cutoff).replace('GAMMA', gamma).replace('TM_STEP', tstep).replace('REST_FREQ', rstfreq).replace('DCD_FREQ', dcdfreq).replace('XST_FREQ', xstfreq).replace('OUT_ENER', outen).replace('OUT_PRES', outpr).replace('XX', '%5.0f' %boxsize[0]).replace('YY', '%5.0f' %boxsize[1]).replace('ZZ', '%5.0f' %boxsize[2]).replace('ZCT', '%5.1f' %boxsize[3])
        with open(fpath, "w") as f:
          f.write(s)
    if not os.path.exists(system):
      os.makedirs(system)
    os.chdir(system)
    # Copy namd input files
    shutil.copy('../build_files/ionized.pdb', './')
    shutil.copy('../build_files/ionized.psf', './')
    shutil.copy('../namd_files/colv-eq.inp', 'colvar.inp')
    shutil.copy('../namd_files/conf_heat', 'conf_heat')
    shutil.copy('../namd_files/conf_equil', 'conf_equil')
    shutil.copy('../namd_files/par_all36_lipid.prm', './')
    shutil.copy('../namd_files/par_all36_prot.prm', './')
    shutil.copy('../namd_files/toppar_water_ions.str', './')
    shutil.copy('../namd_files/run-eq.bash', './')
    with open("../build_files/setup-eq.tcl", "rt") as fin:
      with open("setup.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('REC_CHAIN', rec_chain))
    sp.call('vmd -dispdev text -e setup.tcl', shell=True)
    # Read position of center of mass of protein and change colvar file
    cmass_file = 'cmass.txt'
    f = open(cmass_file, 'r')
    for line in f:
       splitdata = line.split()
       cx = splitdata[0]
       cy = splitdata[1]
       cz = splitdata[2]
    fin = open("colvar.inp", "rt")
    data = fin.read()
    data = data.replace('xxxx', cx).replace('yyyy', cy).replace('zzzz', cz).replace('COLVAR_FREQ', clvfr).replace('REC_TR_FC', '%5.2f' %rest[0]).replace('REC_OR_FC', '%5.2f' %rest[1]) 
    fin.close()
    fin = open("colvar.inp", "wt")
    fin.write(data)
    fin.close()
    os.chdir('../')


def sim_smd(system, rest, boxsize, rec_chain, rec_restr, lig_chain, lig_restr, temperature, smd_steps, pmf_dist, rstfreq, dcdfreq, xstfreq, outpr, outen, clvfr, cutoff, gamma, tstep, ffield):


    # Create SMD directory
    if not os.path.exists('smd'):
      os.makedirs('smd')
    os.chdir('smd')
    if not os.path.exists('build_files'):
      try:
        shutil.copytree('../build_files', './build_files')
      # Directories are the same
      except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
      # Any error saying that the directory doesn't exist
      except OSError as e:
        print('Directory not copied. Error: %s' % e)
    # Create simulation directory
    if os.path.exists('namd_files'):
      shutil.rmtree('./namd_files')
    try:
      shutil.copytree('../namd_files', './namd_files')
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)
    for dname, dirs, files in os.walk('./namd_files'):
      for fname in files:
        fpath = os.path.join(dname, fname)
        with open(fpath) as f:
          s = f.read()
          s = s.replace('TEMP', '%5.2f' %temperature).replace('SMD_STEPS', '%8.0f' %smd_steps).replace('CUTOFF', cutoff).replace('GAMMA', gamma).replace('TM_STEP', tstep).replace('REST_FREQ', rstfreq).replace('DCD_FREQ', dcdfreq).replace('XST_FREQ', xstfreq).replace('OUT_ENER', outen).replace('OUT_PRES', outpr).replace('XX', '%5.0f' %boxsize[0]).replace('YY', '%5.0f' %boxsize[1]).replace('ZZ', '%5.0f' %boxsize[2]).replace('ZCT', '%5.1f' %boxsize[3])
        with open(fpath, "w") as f:
          f.write(s)
    if not os.path.exists(system):
      os.makedirs(system)
    os.chdir(system)
    # Copy namd input files
    shutil.copy('../../equil/'+system+'/ionized.pdb', './')
    shutil.copy('../../equil/'+system+'/ionized.psf', './')
    shutil.copy('../../equil/'+system+'/cmass.txt', './')
    for filename in glob.glob(os.path.join('../../equil/'+system+'/', 'out_equil.restart.*')):
      shutil.copy(filename, './')
    shutil.copy('../namd_files/conf_smd', './')
    shutil.copy('../namd_files/par_all36_lipid.prm', './')
    shutil.copy('../namd_files/par_all36_prot.prm', './')
    shutil.copy('../namd_files/toppar_water_ions.str', './')
    shutil.copy('../namd_files/colv-smd.inp', './colvar.inp')
    shutil.copy('../namd_files/run-smd.bash', './')
    with open("../build_files/setup-smd.tcl", "rt") as fin:
      with open("setup.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('REC_CHAIN', rec_chain).replace('LIG_CHAIN', lig_chain).replace('LIG_RESTR', lig_restr).replace('REC_RESTR', rec_restr))
    sp.call('vmd -dispdev text -e setup.tcl', shell=True)
    # Read definitions and change protein/ligand and change colvar file
    bulk_dist = pmf_dist[-1]
    final_dist = bulk_dist+4.00
    cmass_file = 'cmass.txt'
    f = open(cmass_file, 'r')
    for line in f:
       splitdata = line.split()
       cx = splitdata[0]
       cy = splitdata[1]
       cz = splitdata[2]
    cmlig_file = 'cmlig.txt'
    f = open(cmlig_file, 'r')
    for line in f:
       splitdata = line.split()
       lx = splitdata[0]
       ly = splitdata[1]
       lzt = splitdata[2]
    lx = float(lx)
    ly = float(ly)
    lz = float(lzt)-4.00
    fin = open("colvar.inp", "rt")
    data = fin.read()
    data = data.replace('SMD_STEPS', '%8.0f' %smd_steps).replace('xxxx', cx).replace('yyyy', cy).replace('zzzz', cz).replace('llxx', '%8.6f' %lx).replace('llyy', '%8.6f' %ly).replace('llzz', '%8.6f' %lz).replace('COLVAR_FREQ', clvfr).replace('REC_TR_FC', '%5.2f' %rest[0]).replace('REC_OR_FC', '%5.2f' %rest[1]).replace('REC_RM_FC', '%5.2f' %rest[2]).replace('LIG_TR_FC', '%5.2f' %rest[3]).replace('LIG_OR_FC', '%5.2f' %rest[4]).replace('LIG_RM_FC', '%5.2f' %rest[5]).replace('FINAL_DIS', '%4.1f' %final_dist) 
    fin.close()
    fin = open("colvar.inp", "wt")
    fin.write(data)
    fin.close()
    os.chdir('../')


def sim_fe(comp, system, rest, water_model, boxsize, ion_def, rec_chain, lig_chain, lig_restr, temperature, steps1, steps2, pmf_dist, rest_wgt, num_sim, rstfreq, dcdfreq, xstfreq, outpr, outen, clvfr, cutoff, gamma, tstep, ffield):


    # Create free energy directory
    if not os.path.exists('fe'):
      os.makedirs('fe')
    os.chdir('fe')
    if not os.path.exists('build_files'):
      try:
        shutil.copytree('../build_files', './build_files')
      # Directories are the same
      except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
      # Any error saying that the directory doesn't exist
      except OSError as e:
        print('Directory not copied. Error: %s' % e)
    # Create simulation directory
    if os.path.exists('namd_files'):
      shutil.rmtree('./namd_files')
    try:
      shutil.copytree('../namd_files', './namd_files')
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)
    for dname, dirs, files in os.walk('./namd_files'):
      for fname in files:
        fpath = os.path.join(dname, fname)
        with open(fpath) as f:
          s = f.read()
          s = s.replace('TEMP', '%5.2f' %temperature).replace('CUTOFF', cutoff).replace('GAMMA', gamma).replace('TM_STEP', tstep).replace('REST_FREQ', rstfreq).replace('DCD_FREQ', dcdfreq).replace('XST_FREQ', xstfreq).replace('OUT_ENER', outen).replace('OUT_PRES', outpr).replace('XX', '%5.0f' %boxsize[0]).replace('YY', '%5.0f' %boxsize[1]).replace('ZZ', '%5.0f' %boxsize[2]).replace('ZCT', '%5.1f' %boxsize[3])
        with open(fpath, "w") as f:
          f.write(s)
    if not os.path.exists(system):
      os.makedirs(system)
    os.chdir(system)
    runrng = len(rest_wgt) - 1    
    runumb = len(pmf_dist) - 1    
    shutil.copy('../namd_files/run-all.bash', './')
    with open('run-all.bash') as f:
      s = f.read()
      s = s.replace('RANGE', '%2.0f' %runrng).replace('RUMB', '%2.0f' %runumb)
    with open('run-all.bash', "w") as f:
      f.write(s)
    shutil.copy('../namd_files/run-express.bash', './')
    with open('run-express.bash') as f:
      s = f.read()
      s = s.replace('RANGE', '%2.0f' %runrng).replace('RUMB', '%2.0f' %runumb)
    with open('run-express.bash', "w") as f:
      f.write(s)
    if not os.path.exists("input_files"):
      os.makedirs("input_files")
    os.chdir("input_files")
    # Copy namd input files
    shutil.copy('../../../equil/'+system+'/ionized.pdb', './')
    shutil.copy('../../../equil/'+system+'/ionized.psf', './')
    shutil.copy('../../../equil/'+system+'/cmass.txt', './')
    shutil.copy('../../../smd/'+system+'/atoms.pdb', './')
    shutil.copy('../../../smd/'+system+'/refumb0.pdb', './')
    shutil.copy('../../../smd/'+system+'/cmlig.txt', './')
    for filename in glob.glob(os.path.join('../../../equil/'+system+'/', 'out_equil.restart.*')):
      shutil.copy(filename, './')
    for filename in glob.glob(os.path.join('../../../smd/'+system+'/', 'out_smd.*')):
      shutil.copy(filename, './')
    for filename in glob.glob(os.path.join('../../namd_files/', 'colv*.inp')):
      shutil.copy(filename, './')
    for filename in glob.glob(os.path.join('../../namd_files/', 'conf*')):
      shutil.copy(filename, './')
    shutil.copy('../../namd_files/par_all36_lipid.prm', './')
    shutil.copy('../../namd_files/par_all36_prot.prm', './')
    shutil.copy('../../namd_files/toppar_water_ions.str', './')
    shutil.copy("../../build_files/get-frames-ini.tcl", './')
    # Read definitions and change protein/ligand and change colvar file
    cmass_file = 'cmass.txt'
    f = open(cmass_file, 'r')
    for line in f:
       splitdata = line.split()
       cx = splitdata[0]
       cy = splitdata[1]
       cz = splitdata[2]
    cmlig_file = 'cmlig.txt'
    f = open(cmlig_file, 'r')
    for line in f:
       splitdata = line.split()
       lx = splitdata[0]
       ly = splitdata[1]
       lzt = splitdata[2]
    lx = float(lx)
    ly = float(ly)
    lz = float(lzt)-4.00
    bulk_dist = pmf_dist[-1]
    if (comp == 'u'):
      get_frames = open('get-frames.tcl', 'wt')
      get_frames.write('mol new ionized.psf\n')
      get_frames.write('mol addfile out_equil.restart.coor molid 0 waitfor all\n')
      get_frames.write('mol addfile out_smd.dcd molid 0 waitfor all\n')
      get_frames.write('puts \"\"\n')
      get_frames.write('puts \"Umbrella windows\"\n')
      get_frames.write('set windows { ')
      for listitem in pmf_dist:
          get_frames.write('%4.2f ' % listitem)
      get_frames.write('}\n')
      get_frames.close()
      with open("get-frames-ini.tcl", "rt") as fin:
        with open("get-frames.tcl", "a") as fout:
          for line in fin:
            fout.write(line.replace('RNG_UM', '%4.2f' %bulk_dist))
      get_frames.close()
      sp.call('vmd -dispdev text -e get-frames.tcl', shell=True)
      print('\n')
      os.chdir('../')
      for k in range(0, len(pmf_dist)):
        umb_dist = float(pmf_dist[k]+4.00)
        win = k
        print('PMF window %s%02d - distance %4.2f - Force constant %4.2f' %(comp, int(win), float(pmf_dist[k]), float(rest[3])))
        if not os.path.exists('%s%02d' %(comp, int(win))):
          os.makedirs('%s%02d' %(comp, int(win)))
        os.chdir('%s%02d' %(comp, int(win)))
        shutil.copy("../input_files/conf_ue", './')
        shutil.copy("../input_files/colv-u.inp", './')
        shutil.copy("../input_files/out_smd-%02d.restart.coor" %int(win), './')
        shutil.copy("../input_files/out_smd.restart.xsc", './')
        shutil.copy("../input_files/refumb0.pdb", './')
        shutil.copy("../input_files/atoms.pdb", './')
        shutil.copy("../input_files/ionized.pdb", './')
        shutil.copy("../input_files/ionized.psf", './')
        shutil.copy('../input_files/par_all36_lipid.prm', './')
        shutil.copy('../input_files/par_all36_prot.prm', './')
        shutil.copy('../input_files/toppar_water_ions.str', './')
        conf_min = open('./conf_run-00', 'wt')
        conf_min.write('######################################################\n')
        conf_min.write('## INPUT AND OUTPUT FILES                           ##\n')
        conf_min.write('######################################################\n')
        conf_min.write('set input       run-00\n')
        conf_min.write('set input_pr    smd-%02d\n' %(int(win)))
        conf_min.close()
        fin = open("./colv-u.inp", "rt")
        data = fin.read()
        data = data.replace('xxxx', cx).replace('yyyy', cy).replace('zzzz', cz).replace('llxx', '%8.6f' %lx).replace('llyy', '%8.6f' %ly).replace('llzz', '%8.6f' %lz).replace('COLVAR_FREQ', clvfr).replace('REC_TR_FC', '%5.2f' %rest[0]).replace('REC_OR_FC', '%5.2f' %rest[1]).replace('REC_RM_FC', '%5.2f' %rest[2]).replace('LIG_TR_FC', '%5.2f' %rest[3]).replace('LIG_OR_FC', '%5.2f' %rest[4]).replace('LIG_RM_FC', '%5.2f' %rest[5]).replace('PMF_CENT', '%4.2f' %umb_dist) 
        fin.close()
        fout = open("colvar.inp", "wt")
        fout.write(data)
        fout.close()
        with open("conf_ue", "rt") as fin:
          with open('./conf_run-00', 'a') as fout:
            for line in fin:
              fout.write(line.replace('MIN_STEPS', '%s' %steps1))
        conf_min.close()
        for i in range(1, num_sim):
          pr=i-1
          shutil.copy("../input_files/conf_up", './')
          conf_run = open('./conf_run-%02d' %(int(i)), 'wt')
          conf_run.write('######################################################\n')
          conf_run.write('## INPUT AND OUTPUT FILES                           ##\n')
          conf_run.write('######################################################\n')
          conf_run.write('set input       run-%02d\n' %(int(i)))
          conf_run.write('set input_pr    run-%02d\n' %(int(pr)))
          conf_run.close()
          with open("conf_up", "rt") as fin:
            with open('./conf_run-%02d' %(int(i)), 'a') as fout:
              for line in fin:
                fout.write(line.replace('PROD_STEPS', '%s' %steps2))
          conf_run.close()
        os.chdir('../')    
      os.chdir('../../')
    elif (comp == 'n'):   
      os.chdir('../')
      rel_dist = float(bulk_dist+4.00)
      for k in range(0, len(rest_wgt)):
        weight = rest_wgt[k]
        win = k
        if not os.path.exists('%s%02d' %(comp, int(win))):
          os.makedirs('%s%02d' %(comp, int(win)))
        os.chdir('%s%02d' %(comp, int(win)))
        shutil.copy("../input_files/conf_rest", './')
        shutil.copy("../input_files/colv-%s.inp" %comp, './')
        for filename in glob.glob(os.path.join('../input_files/', 'out_smd.restart.*')):
          shutil.copy(filename, './')
        shutil.copy("../input_files/refumb0.pdb", './')
        shutil.copy("../input_files/atoms.pdb", './')
        shutil.copy("../input_files/ionized.pdb", './')
        shutil.copy("../input_files/ionized.psf", './')
        shutil.copy('../input_files/par_all36_lipid.prm', './')
        shutil.copy('../input_files/par_all36_prot.prm', './')
        shutil.copy('../input_files/toppar_water_ions.str', './')
        conf_min = open('./conf_rest-00', 'wt')
        conf_min.write('######################################################\n')
        conf_min.write('## INPUT AND OUTPUT FILES                           ##\n')
        conf_min.write('######################################################\n')
        conf_min.write('set input       rest-00\n')
        conf_min.write('set input_pr    smd\n')
        conf_min.close()
        fin = open("./colv-%s.inp" %comp, "rt")
        data = fin.read()
        fca1=float(rest[2]*weight)/100
        fca2=float(rest[5]*weight)/100
        data = data.replace('xxxx', cx).replace('yyyy', cy).replace('zzzz', cz).replace('llxx', '%8.6f' %lx).replace('llyy', '%8.6f' %ly).replace('llzz', '%8.6f' %lz).replace('COLVAR_FREQ', clvfr).replace('REC_TR_FC', '%5.2f' %rest[0]).replace('REC_OR_FC', '%5.2f' %rest[1]).replace('REC_RM_FC', '%5.2f' %fca1).replace('LIG_TR_FC', '%5.2f' %rest[3]).replace('LIG_OR_FC', '%5.2f' %rest[4]).replace('LIG_RM_FC', '%5.2f' %fca2).replace('PMF_CENT', '%4.2f' %rel_dist)  
        print('Merged restraints window %s%02d - Force constants %4.2f (Rec-rmsd), %4.2f (Lig-rmsd)' %(comp, int(win), fca1, fca2))
        fin.close()
        fout = open("colvar.inp", "wt")
        fout.write(data)
        fout.close()
        with open("conf_rest", "rt") as fin:
          with open('./conf_rest-00', 'a') as fout:
            for line in fin:
              fout.write(line.replace('PROD_STEPS', '%s' %steps1))
        conf_min.close()
        for i in range(1, num_sim):
          pr=i-1
          conf_run = open('./conf_rest-%02d' %(int(i)), 'wt')
          conf_run.write('######################################################\n')
          conf_run.write('## INPUT AND OUTPUT FILES                           ##\n')
          conf_run.write('######################################################\n')
          conf_run.write('set input       rest-%02d\n' %(int(i)))
          conf_run.write('set input_pr    rest-%02d\n' %(int(pr)))
          conf_run.close()
          with open("conf_rest", "rt") as fin:
            with open('./conf_rest-%02d' %(int(i)), 'a') as fout:
              for line in fin:
                fout.write(line.replace('PROD_STEPS', '%s' %steps2))
          conf_run.close()
        os.chdir('../')    
      os.chdir('../../')    
    elif (comp == 'a' or comp == 'l' or comp == 't' or comp == 'm'):
      os.chdir('../')
      for k in range(0, len(rest_wgt)):
        weight = rest_wgt[k]
        win = k
        if not os.path.exists('%s%02d' %(comp, int(win))):
          os.makedirs('%s%02d' %(comp, int(win)))
        os.chdir('%s%02d' %(comp, int(win)))
        shutil.copy("../input_files/conf_rest", './')
        shutil.copy("../input_files/colv-%s.inp" %comp, './')
        for filename in glob.glob(os.path.join('../input_files/', 'out_equil.restart.*')):
          shutil.copy(filename, './')
        shutil.copy("../input_files/refumb0.pdb", './')
        shutil.copy("../input_files/atoms.pdb", './')
        shutil.copy("../input_files/ionized.pdb", './')
        shutil.copy("../input_files/ionized.psf", './')
        shutil.copy('../input_files/par_all36_lipid.prm', './')
        shutil.copy('../input_files/par_all36_prot.prm', './')
        shutil.copy('../input_files/toppar_water_ions.str', './')
        conf_min = open('./conf_rest-00', 'wt')
        conf_min.write('######################################################\n')
        conf_min.write('## INPUT AND OUTPUT FILES                           ##\n')
        conf_min.write('######################################################\n')
        conf_min.write('set input       rest-00\n')
        conf_min.write('set input_pr    equil\n')
        conf_min.close()
        fin = open("./colv-%s.inp" %comp, "rt")
        data = fin.read()
        if (comp == 'a'):
          fca=float(rest[2]*weight)/100
          data = data.replace('COLVAR_FREQ', clvfr).replace('REC_RM_FC', '%5.2f' %fca) 
          print('Receptor RMSD restraints window %s%02d - Force constant %4.2f ' %(comp, int(win), fca))
        elif (comp == 'l'):
          fca=float(rest[5]*weight)/100
          data = data.replace('COLVAR_FREQ', clvfr).replace('REC_RM_FC', '%5.2f' %rest[2]).replace('LIG_RM_FC', '%5.2f' %fca) 
          print('Ligand RMSD restraints window %s%02d - Force constant %4.2f ' %(comp, int(win), fca))
        elif (comp == 't'):
          fca1=float(rest[3]*weight)/100
          fca2=float(rest[4]*weight)/100
          data = data.replace('xxxx', cx).replace('yyyy', cy).replace('zzzz', cz).replace('llxx', '%8.6f' %lx).replace('llyy', '%8.6f' %ly).replace('llzz', '%8.6f' %lz).replace('COLVAR_FREQ', clvfr).replace('REC_TR_FC', '%5.2f' %rest[0]).replace('REC_OR_FC', '%5.2f' %rest[1]).replace('REC_RM_FC', '%5.2f' %rest[2]).replace('LIG_TR_FC', '%5.2f' %fca1).replace('LIG_OR_FC', '%5.2f' %fca2).replace('LIG_RM_FC', '%5.2f' %rest[5]) 
          print('Ligand translational/rotational restraints window %s%02d - Force constants %4.2f (tr), %4.2f (rot)' %(comp, int(win), fca1, fca2))
        elif (comp == 'm'):
          fca1=float(rest[2]*weight)/100
          fca2=float(rest[3]*weight)/100
          fca3=float(rest[4]*weight)/100
          fca4=float(rest[5]*weight)/100
          data = data.replace('xxxx', cx).replace('yyyy', cy).replace('zzzz', cz).replace('llxx', '%8.6f' %lx).replace('llyy', '%8.6f' %ly).replace('llzz', '%8.6f' %lz).replace('COLVAR_FREQ', clvfr).replace('REC_TR_FC', '%5.2f' %rest[0]).replace('REC_OR_FC', '%5.2f' %rest[1]).replace('REC_RM_FC', '%5.2f' %fca1).replace('LIG_TR_FC', '%5.2f' %fca2).replace('LIG_OR_FC', '%5.2f' %fca3).replace('LIG_RM_FC', '%5.2f' %fca4) 
          print('Merged restraints window %s%02d - Force constants %4.2f (Rec-rmsd), %4.2f (Lig-tr), %4.2f (Lig-rot), %4.2f (Lig-rmsd)' %(comp, int(win), fca1, fca2, fca3, fca4))
        fin.close()
        fout = open("colvar.inp", "wt")
        fout.write(data)
        fout.close()
        with open("conf_rest", "rt") as fin:
          with open('./conf_rest-00', 'a') as fout:
            for line in fin:
              fout.write(line.replace('PROD_STEPS', '%s' %steps1))
        conf_min.close()
        for i in range(1, num_sim):
          pr=i-1
          conf_run = open('./conf_rest-%02d' %(int(i)), 'wt')
          conf_run.write('######################################################\n')
          conf_run.write('## INPUT AND OUTPUT FILES                           ##\n')
          conf_run.write('######################################################\n')
          conf_run.write('set input       rest-%02d\n' %(int(i)))
          conf_run.write('set input_pr    rest-%02d\n' %(int(pr)))
          conf_run.close()
          with open("conf_rest", "rt") as fin:
            with open('./conf_rest-%02d' %(int(i)), 'a') as fout:
              for line in fin:
                fout.write(line.replace('PROD_STEPS', '%s' %steps2))
          conf_run.close()
        os.chdir('../')    
      os.chdir('../../')    



def sim_rec(comp, system, rest, water_model, boxsize, ion_def, rec_chain, rec_restr, temperature, steps1, steps2, rest_wgt, num_sim, rstfreq, dcdfreq, xstfreq, outpr, outen, clvfr, cutoff, gamma, tstep, ffield):
     
    # Create free energy directory
    if not os.path.exists('fe'):
      os.makedirs('fe')
    os.chdir('fe')
    if not os.path.exists('build_files'):
      try:
        shutil.copytree('../build_files', './build_files')
      # Directories are the same
      except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
      # Any error saying that the directory doesn't exist
      except OSError as e:
        print('Directory not copied. Error: %s' % e)
    # Create simulation directory
    if os.path.exists('namd_files'):
      shutil.rmtree('./namd_files')
    try:
      shutil.copytree('../namd_files', './namd_files')
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)
    for dname, dirs, files in os.walk('./namd_files'):
      for fname in files:
        fpath = os.path.join(dname, fname)
        with open(fpath) as f:
          s = f.read()
          s = s.replace('TEMP', '%5.2f' %temperature).replace('CUTOFF', cutoff).replace('GAMMA', gamma).replace('TM_STEP', tstep).replace('REST_FREQ', rstfreq).replace('DCD_FREQ', dcdfreq).replace('XST_FREQ', xstfreq).replace('OUT_ENER', outen).replace('OUT_PRES', outpr).replace('XX', '%5.0f' %boxsize[0]).replace('YY', '%5.0f' %boxsize[1]).replace('ZZ', '%5.0f' %boxsize[2]).replace('ZCT', '%5.1f' %boxsize[3])
        with open(fpath, "w") as f:
          f.write(s)
    if not os.path.exists(system):
      os.makedirs(system)
    os.chdir(system)
    if not os.path.exists("input_files"):
      os.makedirs("input_files")
    os.chdir("input_files")
    # Copy namd input files
    shutil.copy('../../../smd/'+system+'/atoms.pdb', './')
    for filename in glob.glob(os.path.join('../../namd_files/', 'colv*.inp')):
      shutil.copy(filename, './')
    for filename in glob.glob(os.path.join('../../namd_files/', 'conf*')):
      shutil.copy(filename, './')
    shutil.copy('../../namd_files/par_all36_lipid.prm', './')
    shutil.copy('../../namd_files/par_all36_prot.prm', './')
    shutil.copy('../../namd_files/toppar_water_ions.str', './')
    os.chdir('../')
    
    for k in range(0, len(rest_wgt)):
      weight = rest_wgt[k]
      win = k
      if int(k) == 0:
        if not os.path.exists('%s%02d' %(comp, int(win))):
          os.makedirs('%s%02d' %(comp, int(win)))
        os.chdir('%s%02d' %(comp, int(win)))
        shutil.copy("../input_files/conf_rest", './')
        shutil.copy("../input_files/conf_heat", './')
        shutil.copy("../input_files/colv-%s.inp" %comp, './')
        shutil.copy("../input_files/atoms.pdb", './atoms-eq2.pdb')
        shutil.copy('../input_files/par_all36_lipid.prm', './')
        shutil.copy('../input_files/par_all36_prot.prm', './')
        shutil.copy('../input_files/toppar_water_ions.str', './')
        for filename in glob.glob(os.path.join('../../../build_files/', '*.tcl')):
          shutil.copy(filename, './')
        for filename in glob.glob(os.path.join('../../../build_files/', 'top*')):
          shutil.copy(filename, './')
        build.build_receptor(system, rec_chain, rec_restr, water_model, boxsize, ion_def)
        shutil.copy('../input_files/toppar_water_ions.str', './')
        conf_min = open('./conf_rest-00', 'wt')
        conf_min.write('######################################################\n')
        conf_min.write('## INPUT AND OUTPUT FILES                           ##\n')
        conf_min.write('######################################################\n')
        conf_min.write('set input       rest-00\n')
        conf_min.write('set input_pr    heat\n')
        conf_min.close()
        fin = open("./colv-%s.inp" %comp, "rt")
        data = fin.read()
        fca=float(rest[2]*weight)/100
        data = data.replace('COLVAR_FREQ', clvfr).replace('REC_RM_FC', '%5.2f' %fca) 
        print('Receptor RMSD restraints window %s%02d - Force constant %4.2f ' %(comp, int(win), fca))
        fin.close()
        fout = open("colvar.inp", "wt")
        fout.write(data)
        fout.close()
        with open("conf_rest", "rt") as fin:
          with open('./conf_rest-00', 'a') as fout:
            for line in fin:
              fout.write(line.replace('PROD_STEPS', '%s' %steps1))
        conf_min.close()
        for i in range(1, num_sim):
          pr=i-1
          conf_run = open('./conf_rest-%02d' %(int(i)), 'wt')
          conf_run.write('######################################################\n')
          conf_run.write('## INPUT AND OUTPUT FILES                           ##\n')
          conf_run.write('######################################################\n')
          conf_run.write('set input       rest-%02d\n' %(int(i)))
          conf_run.write('set input_pr    rest-%02d\n' %(int(pr)))
          conf_run.close()
          with open("conf_rest", "rt") as fin:
            with open('./conf_rest-%02d' %(int(i)), 'a') as fout:
              for line in fin:
                fout.write(line.replace('PROD_STEPS', '%s' %steps2))
          conf_run.close()
        os.chdir('../')    
      else:
        if not os.path.exists('%s%02d' %(comp, int(win))):
          os.makedirs('%s%02d' %(comp, int(win)))
        os.chdir('%s%02d' %(comp, int(win)))
        for filename in glob.glob(os.path.join('../r00/', 'par*')):
          shutil.copy(filename, './')
        for filename in glob.glob(os.path.join('../r00/', 'conf*')):
          shutil.copy(filename, './')
        for filename in glob.glob(os.path.join('../r00/', 'top*')):
          shutil.copy(filename, './')
        for filename in glob.glob(os.path.join('../r00/', '*.pdb')):
          shutil.copy(filename, './')
        shutil.copy('../r00/ionized.psf', './')
        shutil.copy('../r00/colv-r.inp', './')
        conf_min = open('./conf_rest-00', 'wt')
        conf_min.write('######################################################\n')
        conf_min.write('## INPUT AND OUTPUT FILES                           ##\n')
        conf_min.write('######################################################\n')
        conf_min.write('set input       rest-00\n')
        conf_min.write('set input_pr    heat\n')
        conf_min.close()
        fin = open("./colv-%s.inp" %comp, "rt")
        data = fin.read()
        fca=float(rest[2]*weight)/100
        data = data.replace('COLVAR_FREQ', clvfr).replace('REC_RM_FC', '%5.2f' %fca) 
        print('Receptor RMSD restraints window %s%02d - Force constant %4.2f ' %(comp, int(win), fca))
        fin.close()
        fout = open("colvar.inp", "wt")
        fout.write(data)
        fout.close()
        with open("conf_rest", "rt") as fin:
          with open('./conf_rest-00', 'a') as fout:
            for line in fin:
              fout.write(line.replace('PROD_STEPS', '%s' %steps1))
        conf_min.close()
        for i in range(1, num_sim):
          pr=i-1
          conf_run = open('./conf_rest-%02d' %(int(i)), 'wt')
          conf_run.write('######################################################\n')
          conf_run.write('## INPUT AND OUTPUT FILES                           ##\n')
          conf_run.write('######################################################\n')
          conf_run.write('set input       rest-%02d\n' %(int(i)))
          conf_run.write('set input_pr    rest-%02d\n' %(int(pr)))
          conf_run.close()
          with open("conf_rest", "rt") as fin:
            with open('./conf_rest-%02d' %(int(i)), 'a') as fout:
              for line in fin:
                fout.write(line.replace('PROD_STEPS', '%s' %steps2))
          conf_run.close()
        os.chdir('../')    
    os.chdir('../../')    


def sim_lig(comp, system, rest, water_model, boxsize_ligand, ion_def, lig_chain, lig_restr, temperature, steps1, steps2, rest_wgt, num_sim, rstfreq, dcdfreq, xstfreq, outpr, outen, clvfr, cutoff, gamma, tstep, ffield):
     
    # Create free energy directory
    if not os.path.exists('fe'):
      os.makedirs('fe')
    os.chdir('fe')
    if not os.path.exists('build_files'):
      try:
        shutil.copytree('../build_files', './build_files')
      # Directories are the same
      except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
      # Any error saying that the directory doesn't exist
      except OSError as e:
        print('Directory not copied. Error: %s' % e)
    # Create simulation directory
    if os.path.exists('namd_files'):
      shutil.rmtree('./namd_files')
    try:
      shutil.copytree('../namd_files', './namd_files')
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)
    for dname, dirs, files in os.walk('./namd_files'):
      for fname in files:
        fpath = os.path.join(dname, fname)
        with open(fpath) as f:
          s = f.read()
          s = s.replace('TEMP', '%5.2f' %temperature).replace('CUTOFF', cutoff).replace('GAMMA', gamma).replace('TM_STEP', tstep).replace('REST_FREQ', rstfreq).replace('DCD_FREQ', dcdfreq).replace('XST_FREQ', xstfreq).replace('OUT_ENER', outen).replace('OUT_PRES', outpr).replace('XX', '%5.0f' %boxsize_ligand).replace('YY', '%5.0f' %boxsize_ligand).replace('ZZ', '%5.0f' %boxsize_ligand).replace('ZCT', '0.0')
        with open(fpath, "w") as f:
          f.write(s)
    if not os.path.exists(system):
      os.makedirs(system)
    os.chdir(system)
    if not os.path.exists("input_files"):
      os.makedirs("input_files")
    os.chdir("input_files")
    # Copy namd input files
    shutil.copy('../../../smd/'+system+'/atoms.pdb', './')
    for filename in glob.glob(os.path.join('../../namd_files/', 'colv*.inp')):
      shutil.copy(filename, './')
    for filename in glob.glob(os.path.join('../../namd_files/', 'conf*')):
      shutil.copy(filename, './')
    shutil.copy('../../namd_files/par_all36_lipid.prm', './')
    shutil.copy('../../namd_files/par_all36_prot.prm', './')
    shutil.copy('../../namd_files/toppar_water_ions.str', './')
    os.chdir('../')
    
    for k in range(0, len(rest_wgt)):
      weight = rest_wgt[k]
      win = k
      if int(k) == 0:
        if not os.path.exists('%s%02d' %(comp, int(win))):
          os.makedirs('%s%02d' %(comp, int(win)))
        os.chdir('%s%02d' %(comp, int(win)))
        shutil.copy("../input_files/conf_rest", './')
        shutil.copy("../input_files/conf_heat", './')
        shutil.copy("../input_files/colv-%s.inp" %comp, './')
        shutil.copy("../input_files/atoms.pdb", './atoms-eq2.pdb')
        shutil.copy('../input_files/par_all36_lipid.prm', './')
        shutil.copy('../input_files/par_all36_prot.prm', './')
        shutil.copy('../input_files/toppar_water_ions.str', './')
        for filename in glob.glob(os.path.join('../../../build_files/', '*.tcl')):
          shutil.copy(filename, './')
        for filename in glob.glob(os.path.join('../../../build_files/', 'top*')):
          shutil.copy(filename, './')
        build.build_ligand(system, lig_chain, lig_restr, water_model, boxsize_ligand, ion_def)
        shutil.copy('../input_files/toppar_water_ions.str', './')
        conf_min = open('./conf_rest-00', 'wt')
        conf_min.write('######################################################\n')
        conf_min.write('## INPUT AND OUTPUT FILES                           ##\n')
        conf_min.write('######################################################\n')
        conf_min.write('set input       rest-00\n')
        conf_min.write('set input_pr    heat\n')
        conf_min.close()
        fin = open("./colv-%s.inp" %comp, "rt")
        data = fin.read()
        fca=float(rest[5]*weight)/100
        data = data.replace('COLVAR_FREQ', clvfr).replace('LIG_RM_FC', '%5.2f' %fca) 
        print('Ligand RMSD restraints window %s%02d - Force constant %4.2f ' %(comp, int(win), fca))
        fin.close()
        fout = open("colvar.inp", "wt")
        fout.write(data)
        fout.close()
        with open("conf_rest", "rt") as fin:
          with open('./conf_rest-00', 'a') as fout:
            for line in fin:
              fout.write(line.replace('PROD_STEPS', '%s' %steps1))
        conf_min.close()
        for i in range(1, num_sim):
          pr=i-1
          conf_run = open('./conf_rest-%02d' %(int(i)), 'wt')
          conf_run.write('######################################################\n')
          conf_run.write('## INPUT AND OUTPUT FILES                           ##\n')
          conf_run.write('######################################################\n')
          conf_run.write('set input       rest-%02d\n' %(int(i)))
          conf_run.write('set input_pr    rest-%02d\n' %(int(pr)))
          conf_run.close()
          with open("conf_rest", "rt") as fin:
            with open('./conf_rest-%02d' %(int(i)), 'a') as fout:
              for line in fin:
                fout.write(line.replace('PROD_STEPS', '%s' %steps2))
          conf_run.close()
        os.chdir('../')    
      else:
        if not os.path.exists('%s%02d' %(comp, int(win))):
          os.makedirs('%s%02d' %(comp, int(win)))
        os.chdir('%s%02d' %(comp, int(win)))
        for filename in glob.glob(os.path.join('../c00/', 'par*')):
          shutil.copy(filename, './')
        for filename in glob.glob(os.path.join('../c00/', 'conf*')):
          shutil.copy(filename, './')
        for filename in glob.glob(os.path.join('../c00/', 'top*')):
          shutil.copy(filename, './')
        for filename in glob.glob(os.path.join('../c00/', '*.pdb')):
          shutil.copy(filename, './')
        shutil.copy('../c00/ionized.psf', './')
        shutil.copy('../c00/colv-c.inp', './')
        conf_min = open('./conf_rest-00', 'wt')
        conf_min.write('######################################################\n')
        conf_min.write('## INPUT AND OUTPUT FILES                           ##\n')
        conf_min.write('######################################################\n')
        conf_min.write('set input       rest-00\n')
        conf_min.write('set input_pr    heat\n')
        conf_min.close()
        fin = open("./colv-%s.inp" %comp, "rt")
        data = fin.read()
        fca=float(rest[5]*weight)/100
        data = data.replace('COLVAR_FREQ', clvfr).replace('LIG_RM_FC', '%5.2f' %fca) 
        print('Ligand RMSD restraints window %s%02d - Force constant %4.2f ' %(comp, int(win), fca))
        fin.close()
        fout = open("colvar.inp", "wt")
        fout.write(data)
        fout.close()
        with open("conf_rest", "rt") as fin:
          with open('./conf_rest-00', 'a') as fout:
            for line in fin:
              fout.write(line.replace('PROD_STEPS', '%s' %steps1))
        conf_min.close()
        for i in range(1, num_sim):
          pr=i-1
          conf_run = open('./conf_rest-%02d' %(int(i)), 'wt')
          conf_run.write('######################################################\n')
          conf_run.write('## INPUT AND OUTPUT FILES                           ##\n')
          conf_run.write('######################################################\n')
          conf_run.write('set input       rest-%02d\n' %(int(i)))
          conf_run.write('set input_pr    rest-%02d\n' %(int(pr)))
          conf_run.close()
          with open("conf_rest", "rt") as fin:
            with open('./conf_rest-%02d' %(int(i)), 'a') as fout:
              for line in fin:
                fout.write(line.replace('PROD_STEPS', '%s' %steps2))
          conf_run.close()
        os.chdir('../')    
    os.chdir('../../')    

