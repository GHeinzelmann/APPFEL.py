# APPFEL.py

The Automated Protein-Protein Free Energy tooL (APPFEL.py) is a python tool designed to calculate the affinity of a receptor-ligand complex made of two polypeptide chains. It takes advantage of the collective variables module from the simulation software NAMD, which can apply a sophisticated set of harmonic restraints to multiple groups of atoms. 

APPFEL can perform absolute binding free energy (ABFE) calculations starting only from the pdb structure of the complex, with all the needed steps to build and simulate the systems being performed in a fully automated way. 
  
![](doc/Fig-tut.jpg)


# Getting started

To use APPFEL.py, download the files from this repository, which already contain an example of a protein-protein system. In order to perform all the steps in the calculation, the following programs must be installed and in your path:

NAMD 2.14 (NAnoscale Molecular Dynamics)[1] - https://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=NAMD  

VMD (Visual Molecular Dynamics) [2] - https://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=VMD

MUSTANG v3.2.3 (MUltiple (protein) STructural AligNment alGorithm) [3] - http://lcb.infotech.monash.edu.au/mustang/

AmberTools20 or later [4] - http://ambermd.org/AmberTools.php

The folder APPFEL/strucures contains the initial structure of the complex, which will be the starting point of the calculations. The APPFEL/build\_files and APPFEL/namd\_files folders contain the CHARMM36 topology and parameters needed to build and simulate the systems. Additional force-field options, such as AMBER, will be added to APPFEL workflow in the near future. 

Even though Ambertools is not needed for parameter generation at the moment, the python3 version from AMBER's miniconda contains all the necessary modules to run APPFEL, such as *numpy* and *scipy*. So installing Ambertools might be simpler when compared to downloading, installing and adding each module to the python path. 

# Running a sample calculation

In this tutorial we will perform a sample calculation on a well-known protein-protein system, which will be carried out inside the ./APPFEL/ folder from the APPFEL distribution. The whole procedure requires no manual steps and is divided in four stages: equilibration, steered molecular dynamics (SMD), running the free energy windows, and analyzing them to obtain the desired binding free energy.  

## Equilibration

The equilibration step starts from the initial complex pdb structure, first gradually heating the system, and then performing a simulation with no restraints applied to the ligand. To run this step, inside the ./APPFEL/ folder type:

python APPFEL.py -i input.in -s equil

APPFEL is compatible with python 3.8 versions. If you have another version, or you find that this command gives an error (such as the absence of one or more modules), you can use the python version included in the Ambertools20 distribution:

$AMBERHOME/miniconda/bin/python APPFEL.py -i input.in -s equil

This command will create an ./equil/ folder, with another folder inside for the particular complex chosen for the calculations. In order to run the simulations locally, there is an example bash script called *run-eq.bash* inside the equil/\<complex-name\> folder. The users can also create their own PBS script to run the simulations in a queue system such as TORQUE, which will depend on their server particular definitions. 

# Acknowledgments

Germano Heinzelmann thanks FAPESC and CNPq for the research grants.


# References

1. J. C. Phillips, D. J. Hardy, J. D. C. Maia, J. E. Stone, J. V. Ribeiro, et al. (2020)
“Scalable molecular dynamics on CPU and GPU architectures with NAMD.”
Journal of Chemical Physics, 153, 044130.

2. W. Humphrey, A. Dalke and K. Schulten. (1996)  "VMD - Visual Molecular Dynamics", Journal of Molecular Graphics, 14, 33-38.

3. A. S. Konagurthu, J. Whisstock, P. J. Stuckey, and A. M. Lesk. (2006) “MUSTANG: A multiple structural alignment algorithm”. Proteins, 64, 559-574.

4. D.A. Case, K. Belfon, I.Y. Ben-Shalom, S.R. Brozell, D.S. Cerutti, T.E. Cheatham, III, V.W.D. Cruzeiro, T.A. Darden, R.E. Duke, G. Giambasu, M.K. Gilson, H. Gohlke, A.W. Goetz, R. Harris, S. Izadi, S.A. Izmailov, K. Kasavajhala, A. Kovalenko, R. Krasny, T. Kurtzman, T.S. Lee, S. LeGrand, P. Li, C. Lin, J. Liu, T. Luchko, R. Luo, V. Man, K.M. Merz, Y. Miao, O. Mikhailovskii, G. Monard, H. Nguyen, A. Onufriev, F.Pan, S. Pantano, R. Qi, D.R. Roe, A. Roitberg, C. Sagui, S. Schott-Verdugo, J. Shen, C. Simmerling, N.R.Skrynnikov, J. Smith, J. Swails, R.C. Walker, J. Wang, L. Wilson, R.M. Wolf, X. Wu, Y. Xiong, Y. Xue, D.M. York and P.A. Kollman (2020), AMBER 2020, University of California, San Francisco.



