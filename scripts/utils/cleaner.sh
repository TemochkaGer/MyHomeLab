#!/bin/bash

# Программа проверки и чистки системе на Linux (Ubuntu) с Docker, apt, systemd 
# Выполнять от суперпользователя

set -uo pipefail

USE_SPACE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//') # Получаем значение типа int занятого пространства на корневом разделе в процентах

for cmd in journalctl apt-get docker; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "Компонент системы $cmd не найден" | tee -a clear.log
        echo "Продолжить чистку системы невозможно"
        exit 2
    fi
done

if [[ ! "$USE_SPACE" =~ ^[0-9]+$ ]]; then
    echo "Не удалось получить корректное значение $USE_SPACE" | tee -a clear.log
    exit 3
fi

echo "Занятое пространство на корневом разделе: ${USE_SPACE}%" | tee -a clear.log

if (( USE_SPACE > 80 )); then # Сравниваем полученное значение с эталонным

    echo "Корневой раздел превышает пороговое значение 80% на $(( USE_SPACE-80 ))%" | tee -a clear.log
    echo "Начинаю процесс чистки корневого раздела" | tee -a clear.log
    echo "Начинаю процесс чистки логов, кэша apt" | tee -a clear.log
    journalctl --vacuum-time=7d # Очистка системых логов с остатком за последние 7 дней
    ERR_CODE=$?

    if [ $ERR_CODE -eq 0 ]; then
        echo "Системные журналы почищены успешно" | tee -a clear.log
    else
        echo "Не удалось почистить системные журналы. Код ошибки: ${ERR_CODE}" | tee -a clear.log
        exit 1
    fi
    
    echo "Начинаю процесс чистки кэша apt" | tee -a clear.log
    apt-get clean
    ERR_CODE=$?

    if [ $ERR_CODE -eq 0 ]; then
        echo "Кэш apt почищен успешно" | tee -a clear.log
    else
        echo "Не удалось почистить кэш apt. Код ошибки: ${ERR_CODE}" | tee -a clear.log
        exit 1
    fi

    apt-get autoremove --purge -y
    ERR_CODE=$?

    if [ $ERR_CODE -eq 0 ]; then
        echo "Старые ядра почищены успешно" | tee -a clear.log
    else
        echo "Не удалось почистить старые ядра. Код ошибки: ${ERR_CODE}" | tee -a clear.log
        exit 1
    fi

    echo "Начинаю очистку Docker" | tee -a clear.log
    docker system prune -f
    ERR_CODE=$?

    if [ $ERR_CODE -eq 0 ]; then
        echo "Docker почищен успешно" | tee -a clear.log
    else
        echo "Не удалось почистить Docker. Код ошибки: ${ERR_CODE}" | tee -a clear.log
        exit 1
    fi

    exit 0

else
    echo "Запас порога для корневого раздела: $(( 80-USE_SPACE ))%" | tee -a clear.log
    exit 0
fi