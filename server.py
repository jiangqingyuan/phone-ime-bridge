#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from pathlib import Path
import subprocess

HOST = "0.0.0.0"
PORT = 8765
WEB_DIR = Path(__file__).parent / "web"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = WEB_DIR / "index.html"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(path.read_bytes())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        text = parse_qs(body).get("text", [""])[0]

        if text:
            subprocess.run(["wtype", text], check=False)

        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

if __name__ == "__main__":
    print(f"Phone IME Bridge running on http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), Handler).serve_forever()
