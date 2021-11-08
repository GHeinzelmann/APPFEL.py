#!/usr/bin/env python2
import glob as glob
import os as os
import re as re
import shutil as shutil
import signal as signal
import subprocess as sp
import sys as sys
import math
import numpy as np 
from lib.pymbar import MBAR # multistate Bennett acceptance ratio
from lib.pymbar import timeseries # timeseries analysis

def fe_values(blocks, components, temperature, system, rest_wgt, rest, pmf_dist):


    # Set initial values to zero
    fe_a = fe_l = fe_t = fe_u = fe_c = fe_r = fe_b = fe_n = fe_m = 0
    fb_a = fb_l = fb_t = fb_u = fb_c = fb_r = fb_b = fb_n = fb_m = 0
    sd_a = sd_l = sd_t = sd_u = sd_c = sd_r = sd_b = sd_n = sd_m = 0

    # Acquire simulation data
    os.chdir('fe')
    os.chdir(system)
    for i in range(0, len(components)):
      comp = components[i]
      if comp != 'u':
        for j in range(0, len(rest_wgt)):
          data = []
          win = j
          os.chdir('%s%02d' %(comp, int(win)))
          if (comp == 't' or comp == 'm' or comp == 'n') and win == 0:
            # Calculate analytical release of ligand
            k_tr = rest[3]
            k_qu = rest[4]
            fe_b = fe_int(k_tr, k_qu, temperature)
          # Separate in blocks
          with open("out_rest-01.colvars.traj", "r") as fin:
            for line in fin:
              if not '#' in line:
                data.append(line)
          for k in range(0, blocks):
            fout = open('block%02d.dat' % (k+1), "w")
            for t in range(k*int(round(len(data)//blocks)), (k+1)*int(round(len(data)//blocks))):
              fout.write(data[t])
            fout.close()
          os.chdir('../')
      else:
        for j in range(0, len(pmf_dist)):
          data = []
          win = j
          os.chdir('%s%02d' %(comp, int(win)))
          # Separate in blocks
          with open("out_run-01.colvars.traj", "r") as fin:
            for line in fin:
              if not '#' in line:
                data.append(line)
          for k in range(0, blocks):
            fout = open('block%02d.dat' % (k+1), "w")
            for t in range(k*int(round(len(data)//blocks)), (k+1)*int(round(len(data)//blocks))):
              fout.write(data[t])
            fout.close()
          os.chdir('../')
    os.chdir('../../')

    # Get free energies for the whole run    
    for i in range(0, len(components)):
      comp = components[i]
      if comp != 'u':
        rest_file = 'out_rest-01.colvars.traj'
        mode = 'all'
        fe_mbar(mode, comp, system, rest_file, temperature)
      else:
        rest_file = 'out_run-01.colvars.traj'
        mode = 'all'
        fe_mbar(mode, comp, system, rest_file, temperature)

    # Get free energies for the blocks   
    for i in range(0, len(components)):
      comp = components[i]
      for k in range(0, blocks):
        mode = 'b%02d' % (k+1)
        rest_file = 'block%02d.dat' % (k+1)
        fe_mbar(mode, comp, system, rest_file, temperature)

    sys.stdout = sys.__stdout__

    # Calculate final results
    os.chdir('fe')
    os.chdir(system)
    # Get MBAR free energy averages
    for i in range(0, len(components)):
      comp = components[i]
      with open('./data/mbar-'+comp+'-all.dat', "r") as f_in:
        lines = (line.rstrip() for line in f_in)
        lines = list(line for line in lines if line)
        data = lines[-1]
        splitdata = data.split()
        if comp == 'c':
          fe_c = -1.00*float(splitdata[1])
        elif comp == 'a':
          fe_a = float(splitdata[1])
        elif comp == 't':
          fe_t = float(splitdata[1])
        elif comp == 'l':
          fe_l = float(splitdata[1])
        elif comp == 'm':
          fe_m = float(splitdata[1])
        elif comp == 'r':
          fe_r = -1.00*float(splitdata[1])
        elif comp == 'n':
          fe_n = -1.00*float(splitdata[1])
        elif comp == 'u':
          fe_u = float(splitdata[1])

    # Get errors
    for i in range(0, len(components)):
      comp = components[i]
      b_data = [] 
      for k in range(0, blocks):
        with open('./data/mbar-'+comp+'-b%02d.dat' %(k+1), "r") as f_in:
          lines = (line.rstrip() for line in f_in)
          lines = list(line for line in lines if line)
          data = lines[-1]
          splitdata = data.split()
          b_data.append(float(splitdata[1]))
        if comp == 'c':
          sd_c = np.std(b_data)
        elif comp == 'a':
          sd_a = np.std(b_data)
        elif comp == 't':
          sd_t = np.std(b_data)
        elif comp == 'l':
          sd_l = np.std(b_data)
        elif comp == 'm':
          sd_m = np.std(b_data)
        elif comp == 'n':
          sd_n = np.std(b_data)
        elif comp == 'r':
          sd_r = np.std(b_data)
        elif comp == 'u':
          sd_u = np.std(b_data)

    # Create Results folder
    if not os.path.exists('Results'):
      os.makedirs('Results')

    # Get MBAR free energy averages for the blocks
    for k in range(0, blocks):
      for i in range(0, len(components)):
        comp = components[i]
        with open('./data/mbar-'+comp+'-b%02d.dat' %(k+1), "r") as f_in:
          lines = (line.rstrip() for line in f_in)
          lines = list(line for line in lines if line)
          data = lines[-1]
          splitdata = data.split()
          if comp == 'c':
            fb_c = -1.00*float(splitdata[1])
          elif comp == 'a':
            fb_a = float(splitdata[1])
          elif comp == 't':
            fb_t = float(splitdata[1])
          elif comp == 'l':
            fb_l = float(splitdata[1])
          elif comp == 'm':
            fb_m = float(splitdata[1])
          elif comp == 'r':
            fb_r = -1.00*float(splitdata[1])
          elif comp == 'n':
            fb_n = -1.00*float(splitdata[1])
          elif comp == 'u':
            fb_u = float(splitdata[1])

      fb_b = fe_b
      blck = fb_a + fb_l + fb_t + fb_u + fb_b + fb_c + fb_r
      blckm = fb_m + fb_u + fb_b + fb_n

      # Write results for the blocks
      resfile = open('./Results/Res-b%02d.dat' %(k+1), 'w')
      resfile.write('\n----------------------------------------------\n')
      resfile.write('All components')
      resfile.write('\n----------------------------------------------\n\n')
      resfile.write('%-21s %-10s\n\n' % ('Component', 'Free Energy'))
      resfile.write('%-20s %8.2f\n' % ('Attach Receptor CF', fb_a))
      resfile.write('%-20s %8.2f\n' % ('Attach ligand CF', fb_l))
      resfile.write('%-20s %8.2f\n' % ('Attach ligand TR', fb_t))
      resfile.write('%-20s %8.2f\n' % ('Ligand Pulling', fb_u))
      resfile.write('%-20s %8.2f\n' % ('Release Ligand TR',fb_b))
      resfile.write('%-20s %8.2f\n' % ('Release Ligand CF', fb_c))
      resfile.write('%-20s %8.2f\n\n' % ('Release Receptor CF', fb_r))
      resfile.write('%-20s %8.2f\n' % ('Binding free energy', blck))
      resfile.write('\n----------------------------------------------\n\n')
      # Merged results
      if os.path.exists('./m00/') or os.path.exists('./n00/'):
        fb_rel = fb_b + fb_n
        resfile.write('\n----------------------------------------------\n')
        resfile.write('Merged components (express)')
        resfile.write('\n----------------------------------------------\n\n')
        resfile.write('%-21s %-10s\n\n' % ('Component', 'Free Energy'))
        resfile.write('%-20s %8.2f\n' % ('Attach all', fb_m))
        resfile.write('%-20s %8.2f\n' % ('Ligand Pulling', fb_u))
        resfile.write('%-20s %8.2f\n\n' % ('Release all', fb_rel))
        resfile.write('%-20s %8.2f\n' % ('Binding free energy', blckm))
        resfile.write('\n----------------------------------------------\n\n')
      resfile.write('Energies in kcal/mol\n')
      resfile.close()

    # Write final results
    fe_tot = fe_a + fe_l + fe_t + fe_u + fe_b + fe_c + fe_r
    fe_merged = fe_m + fe_u + fe_b + fe_n
    sd_tot = math.sqrt(sd_a**2 + sd_l**2 + sd_t**2 + sd_u**2 + sd_b**2 + sd_c**2 + sd_r**2)
    sd_merged = math.sqrt(sd_m**2 + sd_u**2 + sd_n**2 + sd_b**2)

    resfile = open('./Results/Results.dat', 'w')
    resfile.write('\n----------------------------------------------\n')
    resfile.write('All components')
    resfile.write('\n----------------------------------------------\n\n')
    resfile.write('%-21s %-10s %-4s\n\n' % ('Component', 'Free Energy', '(Error)'))
    resfile.write('%-20s %8.2f (%3.2f)\n' % ('Attach receptor CF', fe_a, sd_a))
    resfile.write('%-20s %8.2f (%3.2f)\n' % ('Attach ligand CF', fe_l, sd_l))
    resfile.write('%-20s %8.2f (%3.2f)\n' % ('Attach ligand TR', fe_t, sd_t))
    resfile.write('%-20s %8.2f (%3.2f)\n' % ('PMF free energy', fe_u, sd_u))
    resfile.write('%-20s %8.2f \n' % ('Release Ligand TR',fe_b))
    resfile.write('%-20s %8.2f (%3.2f)\n' % ('Release Ligand CF', fe_c, sd_c))
    resfile.write('%-20s %8.2f (%3.2f)\n\n' % ('Release Receptor CF', fe_r, sd_r))
    resfile.write('%-20s %8.2f (%3.2f)\n' % ('Binding free energy', fe_tot, sd_tot))
    resfile.write('\n----------------------------------------------\n\n')
    # Merged results
    if os.path.exists('./m00/') or os.path.exists('./n00/'):
      fe_rel = fe_b + fe_n
      resfile.write('\n----------------------------------------------\n')
      resfile.write('Merged components (express)')
      resfile.write('\n----------------------------------------------\n\n')
      resfile.write('%-21s %-10s %-4s\n\n' % ('Component', 'Free Energy', '(Error)'))
      resfile.write('%-20s %8.2f (%3.2f)\n' % ('Attach all', fe_m, sd_m))
      resfile.write('%-20s %8.2f (%3.2f)\n' % ('Ligand Pulling', fe_u, sd_u))
      resfile.write('%-20s %8.2f (%3.2f)\n\n' % ('Release all', fe_rel, sd_n))
      resfile.write('%-20s %8.2f (%3.2f)\n' % ('Binding free energy', fe_merged, sd_merged))
      resfile.write('\n----------------------------------------------\n\n')
    resfile.write('Energies in kcal/mol\n')
    resfile.close()


def fe_mbar(mode, comp, system, rest_file, temperature):

    kB = 1.381e-23 * 6.022e23 / (4.184 * 1000.0) # Boltzmann constant in kJ/mol/K
    beta = 1/(kB * temperature) # beta
    N_max = 20000 # Max frames for any simulation window, you should check this if you did some long runs


    ### Change to pose directory
    os.chdir('fe')
    os.chdir(system)
    if not os.path.exists('data'):
      os.makedirs('data')

    # Define log file
    sys.stdout = open('./data/mbar-'+comp+'-'+mode+'.log', 'w')

    ### Determine Number of windows
    K = 0
    filename = './'+comp+'%02.0f/%s' % (K, rest_file)
    while os.path.isfile(filename):
      K = K+1
      filename = './'+comp+'%02.0f/%s' % (K, rest_file)

    R = 1

    print  ("K= %5.0f  R= %5.0f" % ( K, R ))

    ### Calculate Statistical Inefficiency (g)
    def calcg(data):
      sum = 0
      randnum = ("%05.0f" % (int(100000*np.random.random())))
      datafn = '/dev/shm/series.'+randnum+'.dat'
      acffn = '/dev/shm/acf.'+randnum+'.dat'
      cppfn = '/dev/shm/pt-acf.'+randnum+'.in'
      np.savetxt(datafn,data)
      cpptin = open(cppfn, 'w')
      cpptin.write("readdata "+datafn+" name "+randnum+"\nautocorr "+randnum+" out "+acffn+" noheader\n")
      cpptin.close()

      FNULL = open(os.devnull, 'w')
      sp.call(['cpptraj','-i',cppfn], stdout=FNULL, stderr=sp.STDOUT)

      with open(acffn, 'r') as acf:
        for line in acf:
          col = line.split()
          t = float(col[0]) - 1.0
      T = t

      with open(acffn, 'r') as acf:
        for line in acf:
          col = line.split()
          t = float(col[0]) - 1.0
          v = float(col[1])
          if t == 0:
            continue
          if v < 0.0:
            break
          sum += ( 1 - (t/T) )*(v)

      sp.call(['rm',datafn,acffn,cppfn])

      return 1+(2*sum)

    ### Allocate storage for simulation data
    N = np.zeros([K], np.int32)                       # N_k[k] is the number of snapshots to be used from umbrella simulation k
    Neff = np.zeros([K], np.int32)
    Nind = np.zeros([K], np.int32)
    Nprg = np.zeros([K], np.int32)
    rty = ['d']*R                                     # restraint type (distance or angle)
    rfc = np.zeros([K,R], np.float64)                 # restraint force constant
    rfc1 = np.zeros([K,R], np.float64)                 # restraint force constant
    rfc2 = np.zeros([K,R], np.float64)                 # restraint force constant
    rfc3 = np.zeros([K,R], np.float64)                 # restraint force constant
    rfc4 = np.zeros([K,R], np.float64)                 # restraint force constant
    fcmax = np.zeros([R], np.float64)                 # full force constant value used during umbrella portion of work 
    req = np.zeros([K,R], np.float64)                 # restraint target value
    req1 = np.zeros([K,R], np.float64)                 # restraint target value
    req2 = np.zeros([K,R], np.float64)                 # restraint target value
    req3 = np.zeros([K,R], np.float64)                 # restraint target value
    req4 = np.zeros([K,R], np.float64)                 # restraint target value
    val = np.zeros([N_max,K,R], np.float64)           # value of the restrained variable at each frame n
    val1 = np.zeros([N_max,K,R], np.float64)           # value of the restrained variable at each frame n
    val2 = np.zeros([N_max,K,R], np.float64)           # value of the restrained variable at each frame n
    val3 = np.zeros([N_max,K,R], np.float64)           # value of the restrained variable at each frame n
    val4 = np.zeros([N_max,K,R], np.float64)           # value of the restrained variable at each frame n
    g = np.zeros([K], np.float64)
    u=np.zeros([N_max], np.float64)

    ### Read the simulation data
    r=0
    for k in range(K):
      # Read Equilibrium Value and Force Constant
      if comp == 't' or comp == 'm':
        with open('./'+comp+'%02.0f/colvar.inp' % k, 'r') as f:
          for line in f:
             if 'posit2' in line:
               for line in f:
                 cols = line.split()
                 if len(cols) != 0 and (cols[0] == "centers"):
                   req[k,r] = float(cols[1])
                 if len(cols) != 0 and (cols[0] == "forceConstant"):
                   rfc[k,r] = float(cols[1])/2
                   break
        with open('./'+comp+'%02.0f/colvar.inp' % k, 'r') as f:
          for line in f:
             if 'posit3' in line:
               for line in f:
                 cols = line.split()
                 if len(cols) != 0 and (cols[0] == "centers"):
                   req1[k,r] = float(cols[1])
                 if len(cols) != 0 and (cols[0] == "forceConstant"):
                   rfc1[k,r] = float(cols[1])/2
                   break
        with open('./'+comp+'%02.0f/colvar.inp' % k, 'r') as f:
          for line in f:
             if 'orient2' in line:
               for line in f:
                 cols = line.split()
                 if len(cols) != 0 and (cols[0] == "centers"):
                   str = cols[1][1:-1]
                   req2[k,r] = float(str)
                 if len(cols) != 0 and (cols[0] == "forceConstant"):
                   rfc2[k,r] = float(cols[1])/2
                   break
        if comp == 'm':       
          with open('./'+comp+'%02.0f/colvar.inp' % k, 'r') as f:
            for line in f:
               if 'rmsd1' in line:
                 for line in f:
                   cols = line.split()
                   if len(cols) != 0 and (cols[0] == "centers"):
                     req3[k,r] = float(cols[1])
                   if len(cols) != 0 and (cols[0] == "forceConstant"):
                     rfc3[k,r] = float(cols[1])/2
                     break
          with open('./'+comp+'%02.0f/colvar.inp' % k, 'r') as f:
            for line in f:
               if 'rmsd2' in line:
                 for line in f:
                   cols = line.split()
                   if len(cols) != 0 and (cols[0] == "centers"):
                     req4[k,r] = float(cols[1])
                   if len(cols) != 0 and (cols[0] == "forceConstant"):
                     rfc4[k,r] = float(cols[1])/2
                     break
      elif comp == 'c' or comp == 'l':
        with open('./'+comp+'%02.0f/colvar.inp' % k, 'r') as f:
          for line in f:
             if 'rmsd2' in line:
               for line in f:
                 cols = line.split()
                 if len(cols) != 0 and (cols[0] == "centers"):
                   req[k,r] = float(cols[1])
                 if len(cols) != 0 and (cols[0] == "forceConstant"):
                   rfc[k,r] = float(cols[1])/2
                   break
      elif comp == 'a' or comp == 'r' or comp == 'n':
        with open('./'+comp+'%02.0f/colvar.inp' % k, 'r') as f:
          for line in f:
             if 'rmsd1' in line:
               for line in f:
                 cols = line.split()
                 if len(cols) != 0 and (cols[0] == "centers"):
                   req[k,r] = float(cols[1])
                 if len(cols) != 0 and (cols[0] == "forceConstant"):
                   rfc[k,r] = float(cols[1])/2
                   break
        if comp == 'n':       
          with open('./'+comp+'%02.0f/colvar.inp' % k, 'r') as f:
            for line in f:
               if 'rmsd2' in line:
                 for line in f:
                   cols = line.split()
                   if len(cols) != 0 and (cols[0] == "centers"):
                     req1[k,r] = float(cols[1])
                   if len(cols) != 0 and (cols[0] == "forceConstant"):
                     rfc1[k,r] = float(cols[1])/2
                     break
      elif comp == 'u':
        with open('./'+comp+'%02.0f/colvar.inp' % k, 'r') as f:
          for line in f:
             if 'posit3' in line:
               for line in f:
                 cols = line.split()
                 if len(cols) != 0 and (cols[0] == "centers"):
                   req[k,r] = float(cols[1])
                 if len(cols) != 0 and (cols[0] == "forceConstant"):
                   rfc[k,r] = float(cols[1])/2
                   break
      else:
        sys.exit("not sure about restraint type!")

      # Read in Values for restrained variables for each simulation
      filename = './'+comp+'%02.0f/%s' % (k, rest_file)
      infile = open(filename, 'r')
      restdat = infile.readlines()     # slice off first 20 lines  readlines()[20:]
      infile.close()
      # Parse Data
      n = 0
      s = 0
      for line in restdat:
        s += 1
        if line[0] != '#' and line[0] != '@' and s > 00:
          cols = line.split()
          if comp == 't':
            val[n,k,r] = float(cols[10])
            val1[n,k,r] = float(cols[11])
            val2[n,k,r] = math.acos(float(cols[2]))
          elif comp == 'm':
            val[n,k,r] = float(cols[12])
            val1[n,k,r] = float(cols[13])
            val2[n,k,r] = math.acos(float(cols[4]))
            val3[n,k,r] = float(cols[1])
            val4[n,k,r] = float(cols[2])
          elif comp == 'n':
            val[n,k,r] = float(cols[1])
            val1[n,k,r] = float(cols[2])
          elif comp == 'u':
            val[n,k,r] = float(cols[2])
          else:
            val[n,k,r] = float(cols[1])
          n += 1
      N[k] = n


      # Calculate Reduced Potential 
      if comp == 't':
        if rfc[k,0] == 0:
          tmp=np.ones([R],np.float64)*0.001
          u[0:N[k]] = np.sum(beta*tmp[0:R]*((val[0:N[k],k,0:R])**2), axis=1)
        else:
          u[0:N[k]] = np.sum(beta*rfc2[k,0:R]*((val2[0:N[k],k,0:R])**2), axis=1)+np.sum(beta*rfc1[k,0:R]*((val1[0:N[k],k,0:R]-req1[k,0:R])**2), axis=1)+np.sum(beta*rfc[k,0:R]*((val[0:N[k],k,0:R]-req[k,0:R])**2), axis=1)
      else:
        if rfc[k,0] == 0:
          tmp=np.ones([R],np.float64)*0.001
          u[0:N[k]] = np.sum(beta*tmp[0:R]*((val[0:N[k],k,0:R]-req[k,0:R])**2), axis=1)
        else:
          u[0:N[k]] = np.sum(beta*rfc[k,0:R]*((val[0:N[k],k,0:R]-req[k,0:R])**2), axis=1)


      if mode == 'sub':
        g[k] = calcg(u[0:N[k]])
        subs = timeseries.subsampleCorrelatedData(np.zeros([N[k]]),g=g[k])
        Nind[k] = len(subs)
        Neff[k] = Nind[k]
      else:
        g[k] = 1.00
        Neff[k] = N[k]
        Nind[k] = N[k]

      print  ("Processed Window %5.0f.  N= %12.0f.  g= %10.3f   Neff= %12.0f" % ( k, N[k], g[k], Neff[k] ))

    Upot = np.zeros([K,K,np.max(Neff)], np.float64)

    # Calculate Restraint Energy
    for k in range(K):
    #  subs = timeseries.subsampleCorrelatedData(np.zeros([N[k]]),g=g[k])
      for l in range(K):
        if comp == 't':
          Upot[k,l,0:Neff[k]] = np.sum(beta*rfc2[l,0:R]*((val2[0:Neff[k],k,0:R])**2), axis=1)+np.sum(beta*rfc1[l,0:R]*((val1[0:Neff[k],k,0:R]-req1[l,0:R])**2), axis=1)+np.sum(beta*rfc[l,0:R]*((val[0:Neff[k],k,0:R]-req[l,0:R])**2), axis=1)
        elif comp == 'm':
          Upot[k,l,0:Neff[k]] = np.sum(beta*rfc2[l,0:R]*((val2[0:Neff[k],k,0:R])**2), axis=1)+np.sum(beta*rfc1[l,0:R]*((val1[0:Neff[k],k,0:R]-req1[l,0:R])**2), axis=1)+np.sum(beta*rfc[l,0:R]*((val[0:Neff[k],k,0:R]-req[l,0:R])**2), axis=1)+np.sum(beta*rfc3[l,0:R]*((val3[0:Neff[k],k,0:R]-req3[l,0:R])**2), axis=1)+np.sum(beta*rfc4[l,0:R]*((val4[0:Neff[k],k,0:R]-req4[l,0:R])**2), axis=1)
        elif comp == 'n':
          Upot[k,l,0:Neff[k]] = np.sum(beta*rfc1[l,0:R]*((val1[0:Neff[k],k,0:R]-req1[l,0:R])**2), axis=1)+np.sum(beta*rfc[l,0:R]*((val[0:Neff[k],k,0:R]-req[l,0:R])**2), axis=1)
        else:
          Upot[k,l,0:Neff[k]] = np.sum(beta*rfc[l,0:R]*((val[0:Neff[k],k,0:R]-req[l,0:R])**2), axis=1)

    val=[]
    val1=[]
    val2=[]
    val3=[]
    val4=[]

    print  ("Running MBAR... ") 
    mbar = MBAR(Upot, Neff, initialize='BAR')

    print  ("Calculate Free Energy Differences Between States")
    [Deltaf, dDeltaf] = mbar.getFreeEnergyDifferences()

    min = np.argmin(Deltaf[0])

    # Write to file
    print  ("Free Energy Differences (in units of kcal/mol)")
    print  ("%9s %8s %8s %12s %12s" % ('bin', 'f', 'df', 'deq', 'dfc'))
    datfile = open('./data/mbar-'+comp+'-'+mode+'.dat', 'w')
    # Sort restraint and umbrella windows in crescent order
    nwsu = np.argsort(req, axis=0)
    nwsr = np.argsort(rfc, axis=0)
    if comp != 'u': # Attach/release
      for k in range(K):
        print ("%10.5f %10.5f %10.5f %12.7f %12.7f" % ( rfc[nwsr[k],0]/rfc[-1,0], Deltaf[0,nwsr[k]]/beta, dDeltaf[0,nwsr[k]]/beta, req[nwsr[k],0], rfc[nwsr[k],0] ))
        datfile.write ( "%10.5f %10.5f %10.5f %12.7f %12.7f\n" % ( rfc[nwsr[k],0]/rfc[-1,0], Deltaf[0,nwsr[k]]/beta, dDeltaf[0,nwsr[k]]/beta, req[nwsr[k],0], rfc[nwsr[k],0] ) )
    else: # Umbrella/Translation
      for k in range(K):
        print ("%10.5f %10.5f %10.5f %12.7f %12.7f" % ( req[nwsu[k],0], Deltaf[0,nwsu[k]]/beta, dDeltaf[0,nwsu[k]]/beta, req[nwsu[k],0], rfc[nwsu[k],0] ))
        datfile.write ( "%10.5f %10.5f %10.5f %12.7f %12.7f\n" % ( req[nwsu[k],0], Deltaf[0,nwsu[k]]/beta, dDeltaf[0,nwsu[k]]/beta, req[nwsu[k],0], rfc[nwsu[k],0] ) )
    datfile.close()
    print ("\n\n")
    
    os.chdir('../../')

def fe_int(k_tr, k_qu, temperature):

    R = 1.987204118e-3 # kcal/mol-K, a.k.a. boltzman constant
    beta = 1/(temperature*R)

    tr_int = (2*np.pi/(beta*k_tr))**(1.5)
    qu_int = (8*np.pi/(beta*k_qu))**(1.5)
    return R*temperature*np.log((1/(8.0*np.pi*np.pi))*(1.0/1661.0)*tr_int*qu_int) 



