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

def build_equil(system, rec_chain, lig_chain, water_model, boxsize, ion_def):


    # Create equilibrium directory
    if not os.path.exists('equil'):
      os.makedirs('equil')
    os.chdir('equil')
    if not os.path.exists('build_files'):
      try:
        shutil.copytree('../build_files', './build_files')
      # Directories are the same
      except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
      # Any error saying that the directory doesn't exist
      except OSError as e:
        print('Directory not copied. Error: %s' % e)
    os.chdir('build_files')
    shutil.copy('../../structures/%s.pdb' %(system), './')



    # Get box dimensions and ion concentration
    minx = (boxsize[0]/2)*(-1)
    miny = (boxsize[1]/2)*(-1)
    minz = (boxsize[2]/2)*(-1)
    maxx = (boxsize[0]/2)
    maxy = (boxsize[1]/2)
    maxz = (boxsize[2]/2)
    ion_conc = ion_def[2]

    # Replace names in initial files and VMD scripts
    with open("align-ini.tcl", "rt") as fin:
      with open("align.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('REC_CHAIN', rec_chain).replace('SYS_NAME', system).replace('LIG_CHAIN', lig_chain))
    with open("split-ini.tcl", "rt") as fin:
      with open("split.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('REC_CHAIN', rec_chain).replace('SYS_NAME', system).replace('LIG_CHAIN', lig_chain))
    with open("solvate-ini.tcl", "rt") as fin:
      with open("solvate.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('XMIN','%3.1f' %minx).replace('YMIN','%3.1f' %miny).replace('ZMIN','%3.1f' %minz).replace('XMAX','%3.1f' %maxx).replace('YMAX','%3.1f' %maxy).replace('ZMAX','%3.1f' %maxz))
    with open("ionize-ini.tcl", "rt") as fin:
      with open("ionize.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('ION_CONC','%3.2f' %ion_conc).replace('CATION','%s' %ion_def[0]).replace('ANION','%s' %ion_def[1]))
    sp.call('vmd -dispdev text -e split.tcl', shell=True)
    sp.call('mustang-3.2.3 -p ./ -i reference.pdb prot-ini.pdb -o prot-aligned -r ON', shell=True)
    with open('prot-aligned.pdb', 'r') as oldfile, open('prot-aligned-clean.pdb', 'w') as newfile:
        for line in oldfile:
            splitdata = line.split()
            if len(splitdata) > 4:
              if splitdata[4] != 'A':
                newfile.write(line)
    sp.call('vmd -dispdev text -e align.tcl', shell=True)
    sp.call('vmd -dispdev text -e psf.tcl', shell=True)
    sp.call('vmd -dispdev text -e solvate.tcl', shell=True)
    sp.call('vmd -dispdev text -e ionize.tcl', shell=True)

    os.chdir('../')


def build_receptor(system, rec_chain, rec_restr, water_model, boxsize, ion_def):


    # Get box dimensions and ion concentration
    minx = (boxsize[0]/2)*(-1)
    miny = (boxsize[1]/2)*(-1)
    minz = (boxsize[2]/2)*(-1)
    maxx = (boxsize[0]/2)
    maxy = (boxsize[1]/2)
    maxz = (boxsize[2]/2)
    ion_conc = ion_def[2]

    # Replace names in initial files and VMD scripts
    with open("split-rec.tcl", "rt") as fin:
      with open("split.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('REC_CHAIN', rec_chain).replace('SYS_NAME', 'atoms-eq2'))
    with open("solvate-ini.tcl", "rt") as fin:
      with open("solvate.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('XMIN','%3.1f' %minx).replace('YMIN','%3.1f' %miny).replace('ZMIN','%3.1f' %minz).replace('XMAX','%3.1f' %maxx).replace('YMAX','%3.1f' %maxy).replace('ZMAX','%3.1f' %maxz))
    with open("ionize-ini.tcl", "rt") as fin:
      with open("ionize.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('ION_CONC','%3.2f' %ion_conc).replace('CATION','%s' %ion_def[0]).replace('ANION','%s' %ion_def[1]))
    sp.call('vmd -dispdev text -e split.tcl', shell=True)
    sp.call('vmd -dispdev text -e psf-rec.tcl', shell=True)
    sp.call('vmd -dispdev text -e solvate.tcl', shell=True)
    sp.call('vmd -dispdev text -e ionize.tcl', shell=True)
    with open("../../../build_files/setup-rec.tcl", "rt") as fin:
      with open("setup.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('REC_RESTR', rec_restr))
    sp.call('vmd -dispdev text -e setup.tcl', shell=True)

def build_ligand(system, lig_chain, lig_restr, water_model, boxsize_ligand, ion_def):


    # Get box dimensions and ion concentration
    minb = (boxsize_ligand/2)*(-1)
    maxb = (boxsize_ligand/2)
    ion_conc = ion_def[2]

    # Replace names in initial files and VMD scripts
    with open("split-lig.tcl", "rt") as fin:
      with open("split.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('LIG_CHAIN', lig_chain).replace('SYS_NAME', 'atoms-eq2'))
    with open("solvate-ini.tcl", "rt") as fin:
      with open("solvate.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('XMIN','%3.1f' %minb).replace('YMIN','%3.1f' %minb).replace('ZMIN','%3.1f' %minb).replace('XMAX','%3.1f' %maxb).replace('YMAX','%3.1f' %maxb).replace('ZMAX','%3.1f' %maxb))
    with open("ionize-ini.tcl", "rt") as fin:
      with open("ionize.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('ION_CONC','%3.2f' %ion_conc).replace('CATION','%s' %ion_def[0]).replace('ANION','%s' %ion_def[1]))
    sp.call('vmd -dispdev text -e split.tcl', shell=True)
    sp.call('vmd -dispdev text -e psf-lig.tcl', shell=True)
    sp.call('vmd -dispdev text -e solvate.tcl', shell=True)
    sp.call('vmd -dispdev text -e ionize.tcl', shell=True)
    with open("../../../build_files/setup-lig.tcl", "rt") as fin:
      with open("setup.tcl", "wt") as fout:
        for line in fin:
          fout.write(line.replace('LIG_RESTR', lig_restr))
    sp.call('vmd -dispdev text -e setup.tcl', shell=True)

