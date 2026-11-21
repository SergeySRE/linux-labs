#!/usr/bin/env bash
# LAB 04 — безопасная проверка состояния учебных портов и HTTP.
# Ничего не запускает, не выключает и не изменяет.

printf '\n=== Прослушиваемые TCP-порты 8000 и 8081 ===\n'
ss -lnt | grep -E '(:8000|:8081)[[:space:]]' || echo 'На 8000/8081 нет TCP listeners'

printf '\n=== Прямой запрос к Python backend (127.0.0.1:8000) ===\n'
curl --max-time 5 -sS -o /dev/null -w 'HTTP status: %{http_code}\n' \
  http://127.0.0.1:8000/ || echo 'Нет успешного подключения к backend'

printf '\n=== Запрос через Nginx proxy (127.0.0.1:8081) ===\n'
curl --max-time 5 -sS -o /dev/null -w 'HTTP status: %{http_code}\n' \
  http://127.0.0.1:8081/ || echo 'Нет успешного подключения к reverse proxy'

printf '\nПодсказка: HTTP 502 — ответ от прокси, который не смог корректно обратиться к upstream.\n'
printf 'Сравни результаты, затем сам выбери следующую команду диагностики.\n'
