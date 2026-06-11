#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from pathlib import Path
import subprocess
import time
import json

HOST = "0.0.0.0"
PORT = 8765
WEB_DIR = Path(__file__).parent / "web"


def get_focused_window():
    try:
        r = subprocess.run(
            ["niri", "msg", "--json", "windows"],
            text=True,
            capture_output=True,
            check=True,
        )
        for win in json.loads(r.stdout):
            if win.get("is_focused"):
                return {
                    "app_id": (win.get("app_id") or "").lower(),
                    "title": (win.get("title") or "").lower(),
                }
    except Exception as e:
        print("get focused window failed:", e)

    return {"app_id": "", "title": ""}


def detect_mode():
    win = get_focused_window()
    app_id = win["app_id"]
    title = win["title"]

    print("focused:", app_id, "|", title)

    if any(x in app_id for x in ["wechat", "weixin", "qq"]) or any(
        x in title for x in ["微信", "qq"]
    ):
        return "im"

    return "normal"


def get_clipboard() -> str:
    r = subprocess.run(
        ["wl-paste"],
        text=True,
        capture_output=True,
        check=False,
    )
    return r.stdout if r.returncode == 0 else ""


def set_clipboard(text: str):
    subprocess.run(
        ["wl-copy"],
        input=text,
        text=True,
        check=False,
    )


def paste_with_wtype():
    subprocess.run(
        ["wtype", "-M", "ctrl", "-k", "v", "-m", "ctrl"],
        check=False,
    )


def paste_with_crossmacro():
    subprocess.run(
        ["crossmacro", "run", "--step", "tap ctrl+v"],
        check=False,
    )


def send_by_clipboard(text: str, paste_func):
    old = get_clipboard()

    set_clipboard(text)
    paste_func()
    set_clipboard(old)


def send_text(text: str):
    mode = detect_mode()

    if mode == "im":
        send_by_clipboard(text, paste_with_crossmacro)
    else:
        send_by_clipboard(text, paste_with_wtype)


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
            send_text(text)

        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    print(f"Phone IME Bridge running on http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), Handler).serve_forever()
