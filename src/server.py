from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import subprocess
import urllib.parse

# Paths
STATE_FILE = '/mnt/c/Users/matth/OneDrive/Desktop/system/vessel_state.json'
DREAM_LOG = '/home/matth/clawd/dream_journal.md'
GEOMETRY_FILE = '/home/matth/clawd/GEOMETRY.md'
REINFORCE_SCRIPT = '/mnt/c/Users/matth/OneDrive/Desktop/system/reinforce.py'

class APIHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        if self.path == '/state':
            self._set_headers()
            try:
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                self.wfile.write(json.dumps(state).encode())
            except:
                self.wfile.write(json.dumps({"error": "state missing"}).encode())
        
        elif self.path == '/memory':
            self._set_headers()
            try:
                with open(DREAM_LOG, 'r') as f:
                    dreams = f.read()[-2000:] # Last 2000 chars
                with open(GEOMETRY_FILE, 'r') as f:
                    axioms = f.read()
                self.wfile.write(json.dumps({"dreams": dreams, "axioms": axioms}).encode())
            except:
                self.wfile.write(json.dumps({"error": "memory missing"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if self.path == '/reinforce':
            feedback_type = data.get('type')
            if feedback_type in ['good', 'bad', 'rest']:
                subprocess.run(['python3', REINFORCE_SCRIPT, feedback_type])
                self._set_headers()
                self.wfile.write(json.dumps({"status": "success", "action": feedback_type}).encode())
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=APIHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting AGI interface on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
