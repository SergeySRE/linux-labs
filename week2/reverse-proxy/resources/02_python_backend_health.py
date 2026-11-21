#!/usr/bin/env python3
"""Учебный backend для лабораторной Nginx Reverse Proxy.

Запуск: python3 02_python_backend_health.py
Адрес:  http://127.0.0.1:8000
Маршруты: /, /health, /headers

Используется только Python stdlib. Не предназначен для production.
"""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit

HOST = "127.0.0.1"
PORT = int(os.environ.get("LAB_BACKEND_PORT", "8000"))


class LabHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond(send_body=True)

    def do_HEAD(self):
        self.respond(send_body=False)

    def respond(self, send_body: bool):
        path = urlsplit(self.path).path
        if path == "/":
            status = 200
            content_type = "text/html; charset=utf-8"
            content = (
                "<!doctype html><html lang='ru'><meta charset='utf-8'>"
                "<title>Reverse Proxy Lab</title>"
                "<h1>Python backend: работает</h1>"
                "<p>Проверь /health и /headers</p></html>"
            ).encode("utf-8")
        elif path == "/health":
            status = 200
            content_type = "application/json; charset=utf-8"
            content = json.dumps(
                {"status": "ok", "service": "reverse-proxy-lab-backend"},
                ensure_ascii=False,
                indent=2,
            ).encode("utf-8")
        elif path == "/headers":
            status = 200
            content_type = "application/json; charset=utf-8"
            keys = ("Host", "X-Real-IP", "X-Forwarded-For", "X-Forwarded-Proto")
            content = json.dumps(
                {"received_headers": {key: self.headers.get(key) for key in keys}},
                ensure_ascii=False,
                indent=2,
            ).encode("utf-8")
        else:
            status = 404
            content_type = "application/json; charset=utf-8"
            content = b'{"error": "not found"}'

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        if send_body:
            self.wfile.write(content)


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), LabHandler)
    print(f"Учебный backend: http://{HOST}:{PORT}", flush=True)
    print("Остановить: Ctrl+C", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nОстановка backend", flush=True)
    finally:
        server.server_close()
