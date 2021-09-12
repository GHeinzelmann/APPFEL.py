mol load pdb SYS_NAME.pdb
set a [atomselect top "segname A"]
$a writepdb prot.pdb
exit
