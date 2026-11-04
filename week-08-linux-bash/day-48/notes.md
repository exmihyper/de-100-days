# День 48: Работа с файлами и текстом

## grep — поиск
```bash
grep "ERROR" app.log           # найти строки
grep -c "ERROR" app.log        # только количество
grep -n "login" app.log        # с номерами строк
grep -v "INFO" app.log         # инвертировать (всё кроме)
grep -i "error" app.log        # игнорировать регистр
```

## awk — обработка колонок
```bash
awk '{print $2}' app.log                       # вторая колонка
awk -F',' '{print $2, $4}' employees.txt       # CSV, 2-я и 4-я
awk -F',' 'NR>1 {sum += $4} END {print sum}' employees.txt  # сумма
awk -F',' 'NR>1 && $3=="IT" {sum+=$4; count++} END {print sum/count}' employees.txt
```

## sed — замена
```bash
sed 's/ERROR/CRITICAL/' app.log        # первое вхождение
sed 's/ERROR/CRITICAL/g' app.log       # все вхождения
sed 's/ERROR/CRITICAL/g' app.log > out.log  # в новый файл
# sed -i 's/ERROR/CRITICAL/g' app.log  # прямо в файле
```

## find — поиск файлов
```bash
find . -name "*.sh"              # все .sh файлы
find ~/de-100-days -name "*.txt"
find ~/de-100-days -mtime -2     # за последние 2 дня
```

## wc — подсчёт
```bash
wc -l app.log     # строки
wc -w app.log     # слова
```

## Конвейеры (pipe)
```bash
grep "ERROR" app.log | wc -l                              # сколько ошибок
grep "login" app.log | awk '{print $5}' | sort | uniq      # уникальные логины
tail -n +2 employees.txt | awk -F',' '{print $3}' | sort | uniq -c | sort -rn  # отделы по количеству
```

## Практика
Написал `day48_task.sh`:
- 3 ошибки в логах
- Сумма зарплат: 803000
- Средняя IT: 110750
- Уникальные отделы: Finance, HR, IT