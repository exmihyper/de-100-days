#!/bin/bash

# ============================================================
# Скрипт бэкапа: архивирует папку source, хранит 7 последних копий
# ============================================================

# Пути
SOURCE_DIR="$HOME/de-100-days/week-08-linux-bash/day-50/source"
BACKUP_DIR="$HOME/de-100-days/week-08-linux-bash/day-50/backups"
LOG_FILE="$HOME/de-100-days/week-08-linux-bash/day-50/logs/backup.log"

# Текущая дата и время для имени файла
# date +%Y-%m-%d_%H-%M-%S — формат: 2026-11-05_18-30-00
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_NAME="backup_${TIMESTAMP}.tar.gz"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"

# Функция логирования
log() {
    # Дата + сообщение -> в файл и в консоль
    echo "[$(date +%Y-%m-%d_%H:%M:%S)] $1" | tee -a "$LOG_FILE"
}

log "=== НАЧАЛО БЭКАПА ==="

# Проверка, что исходная папка существует
if [ ! -d "$SOURCE_DIR" ]; then
    log "ОШИБКА: папка $SOURCE_DIR не найдена"
    exit 1
fi

# Создание архива
log "Создаю архив $BACKUP_NAME"
# tar -czf: c = create, z = gzip, f = file
# -C: перейти в папку перед архивацией
if tar -czf "$BACKUP_PATH" -C "$SOURCE_DIR" .; then
    # $? — код возврата предыдущей команды (0 = успех)
    SIZE=$(du -h "$BACKUP_PATH" | cut -f1)
    log "Архив создан успешно. Размер: $SIZE"
else
    log "ОШИБКА: не удалось создать архив"
    exit 1
fi

# Очистка старых бэкапов (оставляем только 7 последних)
log "Проверяю старые бэкапы..."
BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/backup_*.tar.gz 2>/dev/null | wc -l)
log "Всего бэкапов: $BACKUP_COUNT"

if [ "$BACKUP_COUNT" -gt 7 ]; then
    # Находим все бэкапы, сортируем по времени, берём все кроме 7 последних
    # head -n -7 — взять все строки, КРОМЕ последних 7
    TO_DELETE=$(ls -1t "$BACKUP_DIR"/backup_*.tar.gz | head -n -7)
    
    for old_file in $TO_DELETE; do
        rm "$old_file"
        log "Удалён старый бэкап: $(basename $old_file)"
    done
fi

log "=== БЭКАП ЗАВЕРШЁН ==="
log ""