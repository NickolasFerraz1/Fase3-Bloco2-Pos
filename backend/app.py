"""Backend de exemplo, só para testar que o ml-pipeline não dispara aqui."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        corpo = json.dumps({"status": "ok", "servico": "backend"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(corpo)


if __name__ == "__main__":
    print("Backend em http://localhost:8000")
    HTTPServer(("", 8000), Handler).serve_forever()
