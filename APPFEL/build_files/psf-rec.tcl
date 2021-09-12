

package require psfgen
topology top_all36_prot.rtf
topology toppar_water_ions.str

#pdbaliases
pdbalias residue TIP TIP3
pdbalias residue HOH TIP3
pdbalias residue WAT TIP3
pdbalias residue SOL TIP3
pdbalias residue HID HSE
pdbalias residue Cl- ClA
pdbalias residue K+ POT
pdbalias residue POP POPE
pdbalias residue LIP POPE
pdbalias residue DMP DMPC

pdbalias atom ILE CD1 CD
pdbalias atom ILE HD11 HD1
pdbalias atom ILE HD12 HD2
pdbalias atom ILE HD13 HD3

pdbalias atom TIP3 O OH2
pdbalias atom TIP3 HT1 H1
pdbalias atom TIP3 HT2 H2
pdbalias atom TIP3 OW OH2
pdbalias atom TIP3 HW1 H1
pdbalias atom TIP3 HW2 H2
pdbalias atom CLA Cl- CLA
pdbalias atom POT K+ POT


pdbalias atom FOR H HN
pdbalias atom GLY H HN
pdbalias atom LEU H HN
pdbalias atom VAL H HN
pdbalias atom TRP H HN
pdbalias atom ETA HF H51
pdbalias atom ETA HE H52
pdbalias atom ETA HA2 H11
pdbalias atom ETA HA1 H12
pdbalias atom ETA H  HN1
pdbalias atom ETA HE1 HO1
pdbalias atom ETA CE C5
pdbalias atom ETA CA C1
pdbalias atom ETA OE OH1


pdbalias residue HIS HSD
pdbalias residue HSC HSD
pdbalias atom THR OXT O


segment A {pdb prot.pdb}
coordpdb prot.pdb A

writepdb vac.pdb
writepsf vac.psf

exit
