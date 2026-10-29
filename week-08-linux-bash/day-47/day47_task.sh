#!/bin/bash


read -p "Как тебя зовут? " name
read -p "Сколько тебе лет? " age


if [ "$age" -lt 18 ]; then
    echo "Доступ запрещён"
elif [ "$age" -lt 64 ]; then
    echo "Доступ разрешён"
elif [ "$age" -ge 64 ]; then
    echo "Льготный доступ"
fi

echo "Проверка завершена"