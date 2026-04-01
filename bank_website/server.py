#!/usr/bin/env python3
"""Simple HTTP server to serve the dummy bank website."""

import os
import http.server
import socketserver

PORT = 9000


class BankHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve files from the bank_website directory."""
    
    def __init__(self, *args, **kwargs):
        # Set the directory to serve files from
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)
    
    def end_headers(self):
        # Add headers to prevent caching during development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()


def run_server():
    """Start the HTTP server."""
    with socketserver.TCPServer(("", PORT), BankHTTPRequestHandler) as httpd:
        print(f"🏦 SentinAL Dummy Bank server running at http://localhost:{PORT}")
        print(f"📂 Serving files from: {os.path.dirname(os.path.abspath(__file__))}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped")


if __name__ == "__main__":
    run_server()
