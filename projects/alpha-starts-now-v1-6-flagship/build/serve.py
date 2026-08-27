import http.server
import socketserver
import os
import sys

PORT = 8089
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

if __name__ == '__main__':
    with ThreadingServer(('0.0.0.0', PORT), NoCacheHTTPRequestHandler) as httpd:
        print(f"Serving Alpha Starts Now Flagship from {DIRECTORY} on port {PORT} with No-Cache headers...")
        httpd.serve_forever()
