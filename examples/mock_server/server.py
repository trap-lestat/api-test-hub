from __future__ import annotations

from http.server import HTTPServer

from api_test_hub.utils.mock_server import MockHandler


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = HTTPServer((host, port), MockHandler)
    print(f"Mock server running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
