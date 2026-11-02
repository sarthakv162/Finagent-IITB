#!/usr/bin/env python3
"""Serve the local dummy bank website on loopback only."""

import http.server
import os
import socketserver

HOST = "127.0.0.1"
PORT = 9000


class BankHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Serve static files from this directory without browser caching."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()


def run_server() -> None:
    """Start the dummy website on the local machine only."""
    with socketserver.TCPServer((HOST, PORT), BankHTTPRequestHandler) as server:
        print(f"FinAgent dummy bank running at http://{HOST}:{PORT}")
        print("Press Ctrl+C to stop the server.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nDummy bank server stopped.")


if __name__ == "__main__":
    run_server()