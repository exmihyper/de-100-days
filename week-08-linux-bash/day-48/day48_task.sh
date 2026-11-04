#!/bin/bash

grep -c "ERROR" app.log

awk -F',' 'NR>1 {sum += $4} END {print "Сумма зарплат:", sum}' employees.txt

awk -F',' 'NR>1 && $3=="IT" {sum += $4; count++} END {print "Средняя IT:", sum/count}' employees.txt

tail -n +2 employees.txt | awk -F',' '{print $3}' | sort | uniq