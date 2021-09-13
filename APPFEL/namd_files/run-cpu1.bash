x=0
while [  $x -lt 10 ]; do
cd l0$x
namd2 +p6 conf_rest-00 > conf_rest-00.log
sleep 10
namd2 +p6 conf_rest-01 > conf_rest-01.log
cd ../
cd a0$x
namd2 +p6 conf_rest-00 > conf_rest-00.log
sleep 10
namd2 +p6 conf_rest-01 > conf_rest-01.log
cd ../
let x=x+1
done

if [ $x -ge 10 ]; then
while [  $x -lt 16 ]; do
cd l$x
namd2 +p6 conf_rest-00 > conf_rest-00.log
sleep 10
namd2 +p6 conf_rest-01 > conf_rest-01.log
cd ../
cd a$x
namd2 +p6 conf_rest-00 > conf_rest-00.log
sleep 10
namd2 +p6 conf_rest-01 > conf_rest-01.log
cd ../
let x=x+1
done
fi

