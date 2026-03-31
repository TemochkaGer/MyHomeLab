#!/bin/bash

#============================================
# Название: deploy.sh
# Описание: Автоматический деплой HomeLab web-stack
# Автор: Я
# Версия: 1.0
#============================================

#--------------------------------------------
# Настройки и переменные
#--------------------------------------------

# Выход при любой ошибке и выход при использовании необъявленных переменных
set -eu

# Цвета для красивого вывода
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[1;34m'
readonly NC='\033[0m' # No Color

# Пути
readonly SCRIPT_DIR="$(cd "$(9dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_DIR="${MNT}/homelab/projects/web-stack"
readonly LOG_DIR="${MNT}/homelab/logs"
readonly LOG_FILE="${LOG_DIR}/deploy-$(date +%Y%m%d-%H%M%S).log"

#--------------------------------------------
# Функции
#--------------------------------------------

# Логирование с временной меткой
log() {
    local message="$1"
    local timestamp
    timestap=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${GREEN}[${timestamp}]${NC} ${message}"
    echo "[${timestamp}] INFO: ${message}" >> "${LOG_FILE}"
    exit 1
}

warn() {
    local message="$1"
    local timestamp
    timestap=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${GREEN}[${timestamp}]${NC} ${message}"
    echo "[${timestamp}] WARNING: ${message}" >> "${LOG_FILE}"
    exit 1
}

error() {
    local message="$1"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${RED}[${timestamp}] ERROR:${NC} ${message}"
    echo "[${timestamp}] ERROR: ${message}" >> "${LOG_FILE}"
    exit 1
}

# Проверка наличия команды
check_command() {
    local cmd="$1"
    if ! command -v "${cmd}" &> /dev/null; then
        error "Команда '${cmd}' не найдена. Установисте ее перед запуском."
    fi
}

# --------------------------------------------
# Основная логика
#--------------------------------------------

main() {
    log "Начало деплоя HomeLab web-stack"

    # Проверка зависимостей
    log "Проверка зависимостей..."
    check_command "docker"
    check_command "docker compose"
    check_command "git"
    log "Все зависимости найдены"

    # Переход в директорию проекта
    if [[ ! -d "${PROJECT_DIR}" ]]; then
        error "Директория проекта не найдена: ${PROJECT_DIR}"
    fi
    cd "${PROJECT_DIR}"
    log "Рабочая директория: ${pwd}"

    # Остановка старых контейнеров
    log "Остановка старых контейнеров"
    docker compose down --remove-orphans

    # Сборка образов
    log "Сборка образов"
    docker compose build api

    # Запуск сервисов
    log "Запуск сервисов"
    docker compose up -d

    log "Ожидание запуска"
    sleep 15

    # Проверка здоровья
    log "Проверка здоровья"

    if curl -s -o /dev/null -w "%{http_code}" http://localhost:9090/nginx-health | grep -q "200"; then
        log "Nginx здоров"
    else
        warn "Nginx может быть не здоров"
    fi

    if curl -s -o /dev/null -w "%{http_code}" http://localhost:9090/health | grep -q "200"; then
        log "API здоров"
    else
        warn "API может быть не здоров"
    fi

    # Очистка
    log "Очистка лищних образов"
    docker image prune -f

    # Итог
    log "Статус контейнеров"
    docker compose ps
}

main "$@"