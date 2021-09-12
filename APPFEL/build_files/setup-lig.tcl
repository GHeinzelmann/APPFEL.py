mol load pdb atoms-eq2.pdb
mol load pdb ionized.pdb

set all [atomselect 1 all]
$all set beta 0.0
$all set occupancy 0.0
$all writepdb refumb0.pdb
set a [atomselect 0 "beta 2.00"]
set resid [$a get resid]
set name [$a get name]
set j 0
foreach i $resid {
set atom [atomselect 1 "segname B and resid [lindex $resid $j] and name [lindex $name $j]"]
$atom set beta 2.0
incr j
}
$all writepdb atoms.pdb

exit
