mol new ionized.psf 
mol addfile out_equil.restart.coor molid 0

set all [atomselect top all]
$all set beta 0.0
$all set occupancy 0.0
$all writepdb refumb0.pdb
set prot [atomselect top "segname A and backbone"]
$prot set occupancy 1.0
set pm [atomselect top REC_RESTR]
$pm set beta 1.0
set ac [atomselect top "segname B and backbone"]
$ac set occupancy 2.0
set am [atomselect top LIG_RESTR]
$am set beta 2.0
$all writepdb atoms.pdb
set r [measure center $ac weight mass]
set filename "cmlig.txt"
set fileId [open $filename "w"]
puts -nonewline $fileId $r
close $fileId

exit
