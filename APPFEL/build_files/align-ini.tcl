mol load pdb prot-aligned-clean.pdb
mol load pdb complex.pdb
set sel1 [atomselect 0 "backbone"]
set sel2 [atomselect 1 "chain REC_CHAIN and backbone"]
set all [atomselect 1 all]
$all move [measure fit $sel2 $sel1]
$all moveby [vecinvert [measure center $all weight mass]]
set a [atomselect 1 "chain REC_CHAIN"]
set b [atomselect 1 "chain LIG_CHAIN"]
set all [atomselect 1 all]
$a writepdb prot.pdb
$b writepdb lig.pdb
$all writepdb complex.pdb
exit
