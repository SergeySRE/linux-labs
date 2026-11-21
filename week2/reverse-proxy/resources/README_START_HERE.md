# Lab: Nginx Reverse Proxy → Python backend → 502 → восстановление

Этот пакет создан для учебной VM Ubuntu и репозитория `~/linux-labs`.
Все файлы учебные, без секретов. **Сначала прочитай этот README.**

## Что внутри

| Файл | Когда нужен |
|---|---|
| `01_nginx_reverse_proxy_basic.conf` | Задание 1. Настройка Nginx на 127.0.0.1:8081 |
| `02_python_backend_health.py` | Задание 3. Расширенный backend: `/health` и `/headers` |
| `03_nginx_reverse_proxy_with_headers.conf` | Задание 4. Передача заголовков в backend |
| `04_check_reverse_proxy_lab.sh` | Проверка 8000/8081 на разных этапах |
| `05_incident_report_template.md` | Отчёт об учебной неисправности в GitHub |
| `06_linux_commands_cheatsheet.md` | Шпаргалка по командам |

## Перенос с Windows в Ubuntu

1. Распакуй ZIP на диске, который виден из обеих ОС.
2. В Ubuntu через файловый менеджер скопируй **все файлы** в каталог:
   `~/linux-labs/week2/reverse-proxy/resources/`
3. Если папки нет, создай её:
   `mkdir -p ~/linux-labs/week2/reverse-proxy/resources`
4. Все дальнейшие команды выполняй **в терминале Ubuntu**.

Имя и путь диска не надо угадывать. Используй графический файловый менеджер для переноса.

## Задание 1 — Nginx на новом порту 8081

Текущий сайт на порту 80 не трогаем. Не копируй файлы в `sites-enabled` напрямую.

Сначала открой два терминала. В первом запусти существующий учебный backend:

```bash
cd ~/linux-labs/week2/reverse-proxy
python3 -m http.server 8000 --bind 127.0.0.1
```

В **другом** терминале проверь свободный порт 8081 и перейди к ресурсам:

```bash
sudo ss -lntp | grep ':8081 '
cd ~/linux-labs/week2/reverse-proxy/resources
sudo cp 01_nginx_reverse_proxy_basic.conf /etc/nginx/sites-available/reverse-proxy-lab
```

Создай ссылку **только если её ещё нет**:

```bash
sudo ln -s /etc/nginx/sites-available/reverse-proxy-lab /etc/nginx/sites-enabled/reverse-proxy-lab
```

Если появляется `File exists`, убедись через `ls -l`, что ссылка уже указывает на нужный файл; повторять создание не нужно.

Проверка перед применением обязательна:

```bash
sudo nginx -t
sudo systemctl reload nginx
curl -i http://127.0.0.1:8081/
```

Ожидается HTTP 200 и HTML из backend.

## Задание 2 — учебный инцидент 502 Bad Gateway

В терминале, где работает `python3 -m http.server`, нажми `Ctrl+C`.
**Не останавливай Nginx.**

Запроси сайт через proxy:

```bash
curl -i http://127.0.0.1:8081/
```

Пока не меняй конфигурацию. Сформулируй свои гипотезы: почему Nginx жив, но страница не открылась?
Собери факты командами диагностики из `06_linux_commands_cheatsheet.md`.
Потом восстанови backend исходной командой, повтори HTTP-запрос и зафиксируй результат.

## Задание 3 — backend с маршрутами /health и /headers

Сначала останови старый `http.server` через `Ctrl+C`, иначе порт 8000 будет занят.

```bash
cd ~/linux-labs/week2/reverse-proxy/resources
python3 02_python_backend_health.py
```

В другом терминале:

```bash
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8081/health
curl -i http://127.0.0.1:8081/headers
```

Сравни прямой запрос к backend и запрос через proxy.

## Задание 4 — расширенные заголовки proxy

**Не активируй одновременно** `01_...conf` и `03_...conf`: у них один и тот же порт.
Замени содержимое ранее активированного файла:

```bash
cd ~/linux-labs/week2/reverse-proxy/resources
sudo cp 03_nginx_reverse_proxy_with_headers.conf /etc/nginx/sites-available/reverse-proxy-lab
sudo nginx -t
sudo systemctl reload nginx
curl -i http://127.0.0.1:8081/headers
```

Посмотри, какие заголовки стал получать backend. Их можно увидеть в JSON.

## Задание 5 — отчёт в Git

Создай файл `incident-502-report.md` на основе `05_incident_report_template.md`.
Заполни своими наблюдениями. Не копируй секретные ключи, пароли или токены.
Проверь `git status` и только после проверки сделай отдельный учебный коммит.

## Проверка без изменения системы

```bash
cd ~/linux-labs/week2/reverse-proxy/resources
bash 04_check_reverse_proxy_lab.sh
```

## Безопасность и уборка

- Python-server запущен только на `127.0.0.1`; не открывай его наружу.
- Nginx для лабораторной также слушает только `127.0.0.1:8081`.
- Текущая конфигурация Nginx на порту 80 остаётся нетронутой.
- Если захочешь убрать лабу: удали **только** символьную ссылку `/etc/nginx/sites-enabled/reverse-proxy-lab`, затем `sudo nginx -t` и `sudo systemctl reload nginx`.
- Конфигурационные файлы в `sites-available` можно оставить для дальнейших опытов.

## Чего ждать от преподавателя

Не выполняй все задания сразу. Начни с задания 1, пришли `curl` и вывод `nginx -t`. Потом по одному перейдём к инциденту и расширенным проверкам.
