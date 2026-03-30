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
    echo -e ""
}