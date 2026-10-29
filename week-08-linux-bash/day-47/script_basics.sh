#!/bin/bash


echo "Привет из Bash!"

name="Студент"
age=47


echo "Привет, $name! День $age."

read -p "Как тебя зовут? " username
echo "Привет, $username!"

read -p "Твой возраст: " userage
echo "Тебе $userage лет."


if [ "$userage" -ge 18 ]; then
    echo "Ты совершеннолетний"
else
    echo "Ты несовершеннолетний"
fi



for i in 1 2 3 4 5; do
    echo "Число: $i"
done

for i in {1..5}; do
    echo "Итерация $i"
done

count=1
while [ $count -le 3 ]; do
    echo "Счётчик: $count"
    ((count++))
done