# День 50: Скрипт бэкапа и Cron

## Структура проекта
```
day-50/
├── source/       # что бэкапим
├── backups/      # куда складываем архивы
├── logs/         # лог-файл
└── backup.sh     # скрипт
```

## Ключевые команды
```bash
# Архивация
tar -czf archive.tar.gz -C source .

# Дата для имени файла
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

# Уникальность в одну секунду
TIMESTAMP="${TIMESTAMP}_$$"   # $$ = PID скрипта

# Размер архива
du -h archive.tar.gz | cut -f1

# Ротация: оставить 7 последних
ls -1t backups/backup_*.tar.gz | head -n -7 | xargs rm
```

## Логирование
```bash
log() {
    echo "[$(date +%Y-%m-%d_%H:%M:%S)] $1" | tee -a "$LOG_FILE"
}
```

## Cron
```bash
crontab -e
# 0 3 * * * $HOME/de-100-days/week-08-linux-bash/day-50/backup.sh
```

## Важный урок
`ls -1t` сортирует по времени с точностью до минуты. Если все файлы созданы в одну минуту — сортировка не работает. Нужна уникальность в имени: добавляй PID (`$$`) или миллисекунды.