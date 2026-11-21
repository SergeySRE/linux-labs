# Команды для лабораторной Reverse Proxy

| Команда | Для чего |
|---|---|
| `sudo nginx -t` | Проверить конфигурацию Nginx |
| `sudo systemctl reload nginx` | Перечитать конфигурацию работающего Nginx |
| `systemctl status nginx` | Статус systemd-службы |
| `sudo ss -lntp` | Прослушиваемые TCP-порты и их процессы |
| `curl -i http://127.0.0.1:8000/` | Прямой HTTP-запрос к backend |
| `curl -i http://127.0.0.1:8081/` | Запрос к backend через Nginx |
| `sudo tail -n 30 /var/log/nginx/reverse_proxy_lab_error.log` | Последние ошибки учебного reverse proxy |
| `sudo tail -n 30 /var/log/nginx/reverse_proxy_lab_access.log` | Последние запросы к proxy |
| `sudo journalctl -u nginx -n 30` | События systemd-службы Nginx |
| `git status` | Состояние файлов в Git |

Важно: ошибки обращения к upstream часто записываются в error.log Nginx, а не обязательно в journalctl.
