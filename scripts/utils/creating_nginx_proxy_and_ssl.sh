#!/bin/bash

# Автоматическое создание конфигурации nginx обратного proxy
# Создание SSL сертификата для веб сервера nginx для указанного домена
# Проверка создания конфига и доступности сайта
# Использование sudo creating_nginx_proxy_and_ssl.sh имя_домена адрес проксирования порт почтовый_адрес_для_certbot

set -uo pipefail

UID=$(id -u)
UTILS=(nginx certbot python3-certbot-nginx)
DOMAIN=$1
NGINX_AVAILABLE=/etc/nginx/sites-available/
NGINX_ENABLED=/etc/nginx/sites-enabled/
PROXY_ADDRESS=$2
PROXY_PORT=$3
EMAIL=$4

# Проверка прав суперпользователя
if [[ "$UID" -ne 0 ]]; then
    echo "Скрипт выполнен без прав суперпользователя"
    echo "Правильное использование скрипта: sudo creating_nginx_proxy_and_ssl.sh имя_домена адрес_проксирования порт почтовый_адрес_для_certbot"
    exit 1
fi

if [[ $# -ne 4 ]]; then
    echo "Неверное количество аргументов команды"
    echo "Правильное использование скрипта: sudo creating_nginx_proxy_and_ssl.sh имя_домена адрес_проксирования порт почтовый_адрес_для_certbot"
    exit 2
fi

if [[ ! $DOMAIN =~ ^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    echo "Домен ${DOMAIN} указан не верно"
    echo "Правильный формат: exemple.ru/example.com"
    exit 2
fi

for util in ${UTILS[@]}; do
    if ! dpkg -s $util &>/dev/null; then
        echo "Пакета ${util} не существует, начинаю установку"
        apt install $util -y
        ERR_CODE=$?
        if [[ "$ERR_CODE" -ne 0 ]]; then
            echo  "Не удалось установить ${util} по причине: $ERR_CODE"
            exit 1
        fi
    fi
done

cat <<EOF > "${NGINX_AVAILABLE}${DOMAIN}"
server {
    listen 80;
    listen [::]:80;

    server_name "${DOMAIN}";

    location / {
        proxy_pass http://${PROXY_ADDRESS}:${PROXY_PORT};

        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ERR_CODE=$?

if [[ $ERR_CODE -ne 0 ]]; then
    echo "Не удалось создать конфигурационный файл в ${NGINX_AVAILABLE}"
    echo "Причина: ${ERR_CODE}"
    exit 3
fi

ln -s "${NGINX_AVAILABLE}${DOMAIN}" "${NGINX_ENABLED}${DOMAIN}"

ERR_CODE=$?

if [[ $ERR_CODE -ne 0 ]]; then
    echo "Не удалось создать симлинк на конфигурационный файл в ${NGINX_ENABLED}"
    echo "Причина: ${ERR_CODE}"
    exit 3
fi

certbot certonly \
  --non-interactive \
  --agree-tos \
  --email "${EMAIL}" \
  --no-eff-email \
  --nginx \
  --domains "${DOMAIN}" &>/dev/null

ERR_CODE=$?

if [[ $ERR_CODE -ne 0 ]]; then
    echo "Не удалось создать SSL сертификат для ${DOMAIN}"
    echo "Причина: ${ERR_CODE}"
    exit 3
fi

ls /etc/letsencrypt/ssl-dhparams.pem

ERR_CODE=$?

if [[ $ERR_CODE -ne 0 ]]; then
    openssl dhparam -out /etc/letsencrypt/ssl-dhparams.pem 2048 &>/dev/null
    ERR_CODE=$?
    if [[ $ERR_CODE -ne 0 ]]; then
        echo "Не удалось создать /etc/letsencrypt/ssl-dhparams.pem"
        echo "Причина: ${ERR_CODE}"
        exit 3
    fi
fi

cat <<EOF > "${NGINX_AVAILABLE}${DOMAIN}"
server {
    listen 443 ssl;
    listen [::]:443 ssl;

    server_name "${DOMAIN}";

    ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://"${PROXY_ADDRESS}":"${PROXY_PORT}";

        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

nginx -t &>/dev/null

ERR_CODE=$?

if [[ $ERR_CODE -ne 0 ]]; then
    echo "Невозможно применить изменения для веб сервера, так как конфигурация не проходит проверку"
    echo "Причина: ${ERR_CODE}"
    exit 3
fi

systemctl reload nginx &>/dev/null
ERR_CODE=$?
NGINX_STATUS=$(systemctl is-active nginx)

if [ "${NGINX_STATUS}" != "active" ]; then
    echo "Не удалось перезапустить nginx"
    echo "Причина: ${ERR_CODE}"
    exit 3
fi

curl -s -o /dev/null -w "status=%{http_code}" "https://${DOMAIN}"