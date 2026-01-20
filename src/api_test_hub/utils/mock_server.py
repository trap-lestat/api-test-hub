from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Tuple


class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/hello":
            payload = {"message": "hello", "user": {"id": 7}}
            self._send_json(200, payload)
            return
        if self.path.startswith("/users/"):
            user_id = self.path.split("/users/", 1)[1]
            self._send_json(200, {"id": int(user_id), "name": "lei"})
            return
        self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path == "/submit":
            raw = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode(
                "utf-8"
            )
            try:
                payload = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                payload = {"raw": raw}
            self._send_json(201, {"received": payload})
            return
        self._send_json(404, {"error": "not found"})

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send_json(self, status: int, data: Dict[str, Any]) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def start_mock_server(host: str = "127.0.0.1", port: int = 0) -> Tuple[str, HTTPServer]:
    server = HTTPServer((host, port), MockHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://{host}:{server.server_port}"
    return base_url, server


def stop_mock_server(server: HTTPServer) -> None:
    server.shutdown()
    server.server_close()
