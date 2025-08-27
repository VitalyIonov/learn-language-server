#!/usr/bin/env bash
set -euo pipefail

WEBROOT_VOL="learn-language_certbot-www"
LETSENCRYPT_VOL="learn-language_letsencrypt"
NGINX_CONTAINER="learn-language-nginx-1"

# 1) Продлить сертификаты (certbot сам продлит, если <30 дней до истечения)
docker run --rm \
  -v "${WEBROOT_VOL}:/var/www/certbot" \
  -v "${LETSENCRYPT_VOL}:/etc/letsencrypt" \
  certbot/certbot \
  renew --webroot -w /var/www/certbot --quiet

# 2) Перезагрузить Nginx, чтобы подхватил новые файлы
docker exec "${NGINX_CONTAINER}" nginx -s reload