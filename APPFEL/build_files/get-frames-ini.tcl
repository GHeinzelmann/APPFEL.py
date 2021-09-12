puts ""
puts "Number of frames"
set simframes [molinfo top get numframes]
set totframes [expr ($simframes - 1)]
puts ""
puts "SMD distance range"
set range RNG_UM
puts ""
puts "Number of windows"
set win [llength $windows]
puts ""
puts "Frames/Angstrom"
set step [expr double($totframes)/double($range)]
puts "###############"
puts "### Windows ###"
puts "###############"
puts ""
for {set i 0} {$i < $win} {incr i} {
set win1 [lindex $windows $i]
set j [format "%02d" [expr $i]]
set fra [expr round([expr ($win1/$range)*$totframes])]
puts ""
puts "Position $win1"
puts "Window number $j"
puts "Frame $fra"
set a [atomselect top all frame $fra]
$a writenamdbin out_smd-$j.restart.coor
}
exit
