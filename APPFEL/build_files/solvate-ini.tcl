package require solvate
solvate vac.psf vac.pdb -o solvate -b 1.5 -minmax {{XMIN YMIN ZMIN} {XMAX YMAX ZMAX}}
exit
