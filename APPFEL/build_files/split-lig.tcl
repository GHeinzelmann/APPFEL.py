mol load pdb SYS_NAME.pdb
set a [atomselect top "segname B"]
$a writepdb lig.pdb
exit
