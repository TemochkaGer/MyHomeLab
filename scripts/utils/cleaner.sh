#!/bin/bash

# Программа проверки и чистки системе на Linux (Ubuntu) с Docker, apt, systemd 
# Выполнять от суперпользователя
# Для планировщика crontab
# Запуск планировщика sudo crontab -e
# 0 0 * * * /путь к скрипту/cleaner.sh
# Путь для сохранения лога

set -uo pipefail

USE_SPACE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//') # Получаем значение типа int занятого пространства на корневом разделе в процентах
PATH_TO_LOG=/var/log/cleaner.log

# Проверка существования утилит на хосте
for cmd in journalctl apt-get docker; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') Компонент системы $cmd не найден" | tee -a "${PATH_TO_LOG}"
        echo "$(date '+%Y-%m-%d %H:%M:%S') Продолжить чистку системы невозможно" | tee -a "${PATH_TO_LOG}"
        exit 2
    fi
done

# Проверка правильности формата переменной USE_SPACE
if [[ ! "$USE_SPACE" =~ ^[0-9]+$ ]]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') Не удалось получить корректное значение $USE_SPACE" | tee -a "${PATH_TO_LOG}"
    exit 3
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') Занятое пространство на корневом разделе: ${USE_SPACE}%" | tee -a "${PATH_TO_LOG}"

if (( USE_SPACE > 80 )); then # Сравниваем полученное значение с эталонным

    echo "$(date '+%Y-%m-%d %H:%M:%S') Корневой раздел превышает пороговое значение 80% на $(( USE_SPACE-80 ))%" | tee -a "${PATH_TO_LOG}"
    echo "$(date '+%Y-%m-%d %H:%M:%S') Начинаю процесс чистки корневого раздела" | tee -a "${PATH_TO_LOG}"
    echo "$(date '+%Y-%m-%d %H:%M:%S') Начинаю процесс чистки логов, кэша apt" | tee -a "${PATH_TO_LOG}"
    journalctl --vacuum-time=7d # Очистка системых логов с остатком за последние 7 дней
    ERR_CODE=$? # Сохраняем exit code последней выполенной команды

    if [ $ERR_CODE -eq 0 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') Системные журналы почищены успешно" | tee -a "${PATH_TO_LOG}"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') Не удалось почистить системные журналы. Код ошибки: ${ERR_CODE}" | tee -a "${PATH_TO_LOG}"
        exit 1
    fi
    
    echo "$(date '+%Y-%m-%d %H:%M:%S') Начинаю процесс чистки кэша apt" | tee -a "${PATH_TO_LOG}"
    apt-get clean # Систка кэша apt
    ERR_CODE=$?

    if [ $ERR_CODE -eq 0 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') Кэш apt почищен успешно" | tee -a "${PATH_TO_LOG}"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') Не удалось почистить кэш apt. Код ошибки: ${ERR_CODE}" | tee -a "${PATH_TO_LOG}"
        exit 1
    fi

    apt-get autoremove --purge -y # Удаление старых ядер
    ERR_CODE=$?

    if [ $ERR_CODE -eq 0 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') Старые ядра почищены успешно" | tee -a "${PATH_TO_LOG}"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') Не удалось почистить старые ядра. Код ошибки: ${ERR_CODE}" | tee -a "${PATH_TO_LOG}"
        exit 1
    fi

    echo "$(date '+%Y-%m-%d %H:%M:%S') Начинаю очистку Docker" | tee -a "${PATH_TO_LOG}"
    docker system prune -f # Удаление кэша сборок контейнеров Docker
    ERR_CODE=$?

    if [ $ERR_CODE -eq 0 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') Docker почищен успешно" | tee -a "${PATH_TO_LOG}"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') Не удалось почистить Docker. Код ошибки: ${ERR_CODE}" | tee -a "${PATH_TO_LOG}"
        exit 1
    fi

    exit 0

else
    echo "$(date '+%Y-%m-%d %H:%M:%S') Запас порога для корневого раздела: $(( 80-USE_SPACE ))%" | tee -a "${PATH_TO_LOG}"
    exit 0
fi