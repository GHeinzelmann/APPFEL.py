mol load pdb SYS_NAME.pdb
set all [atomselect top "protein and (chain REC_CHAIN or chain LIG_CHAIN)"]
$all writepdb complex.pdb
set a [atomselect top "chain REC_CHAIN"]
$a writepdb prot-ini.pdb
set b [atomselect top "chain LIG_CHAIN"]
$b writepdb lig-ini.pdb
exit
