
x=0
while [  $x -lt 10 ]; do
cd u0$x
namd2 +p6 conf_run-00 > conf_run-00.log
sleep 10
namd2 +p6 conf_run-01 > conf_run-01.log
cd ../
let x=x+1
done

if [ $x -ge 10 ]; then
while [  $x -lt 41 ]; do
cd u$x
namd2 +p6 conf_run-00 > conf_run-00.log
sleep 10
namd2 +p6 conf_run-01 > conf_run-01.log
cd ../
let x=x+1
done
fi

