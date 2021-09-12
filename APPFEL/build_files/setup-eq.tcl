mol load psf ionized.psf pdb ionized.pdb

set all [atomselect top all]
$all set occupancy 0
$all set beta 0
$all writepdb refumb0.pdb

set all [atomselect top all]
$all set occupancy 0
$all set beta 0
set pr [atomselect top "segname A and backbone"]
$pr set occupancy 1.0
$all writepdb atoms.pdb
set r [measure center $pr weight mass]
set filename "cmass.txt"
set fileId [open $filename "w"]
puts -nonewline $fileId $r
close $fileId

exit
