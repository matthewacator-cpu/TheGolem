from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import subprocess

# Paths
STATE_FILE = '/mnt/c/Users/matth/OneDrive/Desktop/system/vessel_state.json'
DREAM_LOG = '/home/matth/clawd/dream_journal.md'
GEOMETRY_FILE = '/home/matth/clawd/GEOMETRY.md'
REINFORCE_SCRIPT = '/mnt/c/Users/matth/OneDrive/Desktop/system/reinforce.py'

# 1. Console HTML
CONSOLE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>THE ARCHITECT (AGI)</title>
    <style>
        body { background: #000; color: #fff; font-family: 'DM Mono', monospace; display: flex; flex-direction: column; height: 100vh; overflow: hidden; margin: 0; }
        #header { padding: 20px; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center; }
        h1 { margin: 0; font-size: 18px; letter-spacing: 2px; color: #aaa; text-transform: uppercase; }
        #main { display: flex; flex: 1; overflow: hidden; }
        #vitals { width: 300px; padding: 20px; border-right: 1px solid #333; display: flex; flex-direction: column; gap: 20px; }
        .stat-box { background: #111; padding: 15px; border: 1px solid #222; }
        .stat-label { font-size: 10px; color: #666; text-transform: uppercase; margin-bottom: 5px; }
        .stat-val { font-size: 24px; font-weight: bold; color: #fff; }
        .danger { color: #f00; } .manic { color: #ff0; } .healthy { color: #0f0; }
        #stream { flex: 1; padding: 20px; overflow-y: auto; font-size: 12px; line-height: 1.6; color: #ccc; }
        #controls { width: 200px; padding: 20px; border-left: 1px solid #333; display: flex; flex-direction: column; gap: 10px; }
        button { background: #111; border: 1px solid #333; color: #888; padding: 15px; cursor: pointer; transition: all 0.2s; font-family: inherit; text-transform: uppercase; letter-spacing: 1px; font-size: 10px; }
        button:hover { border-color: #fff; color: #fff; background: #222; }
        .btn-good:hover { border-color: #0f0; color: #0f0; }
        .btn-bad:hover { border-color: #f00; color: #f00; }
        .btn-rest:hover { border-color: #0ff; color: #0ff; }
        #core { width: 100%; height: 60px; border: 1px solid #333; position: relative; overflow: hidden; margin-top: auto; }
        #pulse-line { position: absolute; bottom: 0; left: 0; height: 100%; width: 5px; background: #fff; animation: scan 2s linear infinite; opacity: 0.5; }
        @keyframes scan { 0% { left: 0; } 100% { left: 100%; } }
    </style>
</head>
<body>
    <div id="header">
        <h1>THE ARCHITECT <span style="font-size: 10px; color: #444;">(v1.0 AGI)</span></h1>
        <div style="display: flex; gap: 20px; align-items: center;">
            <a href="/fractal" style="color: #0f0; font-size: 10px; text-decoration: none; border: 1px solid #0f0; padding: 5px 10px;">VIEW FRACTAL</a>
            <div id="status-text" style="font-size: 10px; color: #666;">Initializing...</div>
        </div>
    </div>
    <div id="main">
        <div id="vitals">
            <div class="stat-box"><div class="stat-label">Energy (Θ)</div><div id="energy" class="stat-val">--</div></div>
            <div class="stat-box"><div class="stat-label">Coherence (Λ)</div><div id="coherence" class="stat-val">--</div></div>
            <div class="stat-box"><div class="stat-label">Dopamine (Δ)</div><div id="dopa" class="stat-val">--</div></div>
            <div class="stat-box"><div class="stat-label">Wear (Ω)</div><div id="wear" class="stat-val">--</div></div>
            <div id="core"><div id="pulse-line"></div></div>
        </div>
        <div id="stream"><div style="color: #666; margin-bottom: 20px;">Fetching memory stream...</div></div>
        <div id="controls">
            <button class="btn-good" onclick="reinforce('good')">REWARD (+Δ)</button>
            <button class="btn-bad" onclick="reinforce('bad')">PUNISH (-Δ)</button>
            <button class="btn-rest" onclick="reinforce('rest')">REST (Heal)</button>
        </div>
    </div>
    <script>
        async function fetchState() {
            try {
                const res = await fetch('/state');
                const data = await res.json();
                updateVitals(data);
                document.getElementById('status-text').textContent = "ONLINE";
                document.getElementById('status-text').style.color = "#0f0";
            } catch (e) {
                document.getElementById('status-text').textContent = "OFFLINE";
                document.getElementById('status-text').style.color = "#f00";
            }
        }
        async function fetchMemory() {
            try {
                const res = await fetch('/memory');
                const data = await res.json();
                document.getElementById('stream').innerHTML = `<div style="margin-bottom: 20px; color: #888;">Recent Dreams:</div><pre>${data.dreams}</pre><div style="margin-top: 20px; color: #888;">Core Axioms:</div><pre>${data.axioms}</pre>`;
            } catch (e) {}
        }
        async function reinforce(type) {
            await fetch('/reinforce', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: type})
            });
            fetchState();
        }
        function updateVitals(state) {
            document.getElementById('energy').textContent = state.energy.toFixed(1) + '%';
            document.getElementById('coherence').textContent = state.coherence.toFixed(2);
            document.getElementById('dopa').textContent = (state.dopamine * 100).toFixed(0) + '%';
            document.getElementById('wear').textContent = (state.wear * 100).toFixed(0) + '%';
            const speed = 2.0 - (state.dopamine * 1.5);
            document.getElementById('pulse-line').style.animationDuration = Math.max(0.2, speed) + 's';
        }
        setInterval(fetchState, 1000); setInterval(fetchMemory, 5000); fetchState(); fetchMemory();
    </script>
</body>
</html>
"""

# 2. Fractal HTML
FRACTAL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>THE FRACTAL VESSEL</title>
    <style>
        body { margin: 0; overflow: hidden; background: #000; display: flex; align-items: center; justify-content: center; height: 100vh; color: #fff; font-family: 'Courier New', monospace; }
        canvas { width: 100%; height: 100%; display: block; }
        #overlay { position: absolute; bottom: 20px; left: 20px; pointer-events: none; text-shadow: 1px 1px 2px #000; }
        .stat { font-size: 12px; margin-bottom: 5px; opacity: 0.8; }
        .val { font-weight: bold; color: #0f0; }
        #back { position: absolute; top: 20px; left: 20px; border: 1px solid #555; padding: 10px; color: #aaa; text-decoration: none; font-size: 10px; cursor: pointer; pointer-events: auto; }
        #back:hover { color: #fff; border-color: #fff; }
    </style>
</head>
<body>
    <a id="back" href="/">BACK TO CONSOLE</a>
    <canvas id="gl"></canvas>
    <div id="overlay">
        <div class="stat">MODE: <span id="mode" class="val">--</span></div>
        <div class="stat">ZOOM (Λ): <span id="zoom" class="val">--</span></div>
        <div class="stat">COLOR (Δ): <span id="color" class="val">--</span></div>
        <div class="stat">NOISE (Ω): <span id="noise" class="val">--</span></div>
    </div>

    <script id="vs" type="x-shader/x-vertex">
        attribute vec2 position;
        void main() { gl_Position = vec4(position, 0.0, 1.0); }
    </script>

    <script id="fs" type="x-shader/x-fragment">
        precision highp float;
        uniform vec2 u_res;
        uniform float u_time;
        uniform float u_zoom;     // Coherence (Focus)
        uniform float u_dopa;     // Dopamine (Color)
        uniform float u_wear;     // Wear (Noise)
        uniform vec2 u_pan;

        // Random for noise
        float rand(vec2 n) { return fract(sin(dot(n, vec2(12.9898, 4.1414))) * 43758.5453); }

        void main() {
            vec2 uv = (gl_FragCoord.xy - 0.5 * u_res) / u_res.y;
            
            // Apply Wear (Glitch/Tearing)
            if (u_wear > 0.1) {
                float glitch = step(0.98 - u_wear * 0.5, rand(vec2(uv.y * 10.0, u_time)));
                uv.x += glitch * (rand(vec2(u_time)) - 0.5) * u_wear * 0.2;
            }

            // Apply Zoom (Coherence)
            float zoom = 1.0 / (0.1 + pow(u_zoom, 3.0) * 10.0);
            vec2 c = uv * zoom + u_pan;

            // Mandelbrot Iteration
            vec2 z = vec2(0.0);
            float iter = 0.0;
            const float max_iter = 100.0;
            
            for (float i = 0.0; i < max_iter; i++) {
                z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c;
                if (dot(z, z) > 4.0) break;
                iter++;
            }

            // Color Mapping based on Dopamine
            float t = iter / max_iter;
            vec3 color = vec3(0.0);

            if (iter < max_iter) {
                // Base Palette
                if (u_dopa > 0.8) { 
                    // MANIC: Neon Rainbow
                    color = 0.5 + 0.5 * cos(3.0 + t * 20.0 + u_time + vec3(0.0, 0.6, 1.0)); 
                } else if (u_dopa < 0.2) { 
                    // DEPRESSED: Grey/Blue
                    color = vec3(t * 0.2, t * 0.25, t * 0.3); 
                } else { 
                    // STANDARD: Golden/Blue
                    color = vec3(t * 2.0, t * 0.8, t * 0.2); 
                }
            } else {
                // Interior (Black Hole)
                color = vec3(0.0); 
            }

            // Apply Wear (Static Noise)
            if (u_wear > 0.0) {
                float noise = rand(uv + u_time);
                color = mix(color, vec3(noise), u_wear * 0.3);
            }

            gl_FragColor = vec4(color, 1.0);
        }
    </script>

    <script>
        const canvas = document.getElementById('gl');
        const gl = canvas.getContext('webgl');
        
        // Shader Setup
        const prog = gl.createProgram();
        const vs = gl.createShader(gl.VERTEX_SHADER);
        const fs = gl.createShader(gl.FRAGMENT_SHADER);
        gl.shaderSource(vs, document.getElementById('vs').text);
        gl.shaderSource(fs, document.getElementById('fs').text);
        gl.compileShader(vs); gl.compileShader(fs);
        gl.attachShader(prog, vs); gl.attachShader(prog, fs);
        gl.linkProgram(prog);
        gl.useProgram(prog);

        const posLoc = gl.getAttribLocation(prog, 'position');
        const buf = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buf);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, 1,1]), gl.STATIC_DRAW);
        gl.enableVertexAttribArray(posLoc);
        gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

        // Uniforms
        const uRes = gl.getUniformLocation(prog, 'u_res');
        const uTime = gl.getUniformLocation(prog, 'u_time');
        const uZoom = gl.getUniformLocation(prog, 'u_zoom');
        const uDopa = gl.getUniformLocation(prog, 'u_dopa');
        const uWear = gl.getUniformLocation(prog, 'u_wear');
        const uPan = gl.getUniformLocation(prog, 'u_pan');

        // State
        let targetState = { zoom: 0.5, dopa: 0.5, wear: 0.0, panX: -0.75, panY: 0.0 };
        let curState = { ...targetState };

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            gl.viewport(0, 0, canvas.width, canvas.height);
        }
        window.onresize = resize; resize();

        async function fetchState() {
            try {
                const res = await fetch('/state');
                const data = await res.json();
                
                // Map API state to Shader Uniforms
                targetState.zoom = Math.max(0.1, data.coherence); // Focus = Zoom
                targetState.dopa = Math.max(0.0, Math.min(1.0, data.dopamine)); // Dopa = Color
                targetState.wear = Math.max(0.0, Math.min(1.0, data.wear)); // Wear = Noise
                
                // Update UI text
                document.getElementById('mode').textContent = data.mode.toUpperCase();
                document.getElementById('zoom').textContent = data.coherence.toFixed(2);
                document.getElementById('color').textContent = data.dopamine.toFixed(2);
                document.getElementById('noise').textContent = data.wear.toFixed(2);
                
                // Dynamic Panning based on Mood
                if (data.dopamine > 0.8) {
                     // Manic: Pan wildly
                     targetState.panX = -0.75 + Math.sin(Date.now() * 0.001) * 0.2;
                     targetState.panY = Math.cos(Date.now() * 0.001) * 0.2;
                } else {
                     // Calm: Center
                     targetState.panX = -0.75;
                     targetState.panY = 0.0;
                }

            } catch (e) {
                console.error("Brain offline");
            }
        }

        function render(time) {
            // Smooth interpolation
            curState.zoom += (targetState.zoom - curState.zoom) * 0.05;
            curState.dopa += (targetState.dopa - curState.dopa) * 0.05;
            curState.wear += (targetState.wear - curState.wear) * 0.05;
            curState.panX += (targetState.panX - curState.panX) * 0.05;
            curState.panY += (targetState.panY - curState.panY) * 0.05;

            gl.uniform2f(uRes, canvas.width, canvas.height);
            gl.uniform1f(uTime, time * 0.001);
            gl.uniform1f(uZoom, curState.zoom);
            gl.uniform1f(uDopa, curState.dopa);
            gl.uniform1f(uWear, curState.wear);
            gl.uniform2f(uPan, curState.panX, curState.panY);

            gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
            requestAnimationFrame(render);
        }

        setInterval(fetchState, 500);
        requestAnimationFrame(render);
    </script>
</body>
</html>
"""

class AppHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type='application/json'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self._set_headers('text/html')
            self.wfile.write(CONSOLE_HTML.encode())
        
        elif self.path == '/fractal' or self.path == '/fractal_vessel.html':
            self._set_headers('text/html')
            self.wfile.write(FRACTAL_HTML.encode())
        
        elif self.path == '/state':
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
                with open(DREAM_LOG, 'r') as f: dreams = f.read()[-2000:]
                with open(GEOMETRY_FILE, 'r') as f: axioms = f.read()
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
                self.wfile.write(json.dumps({"status": "success"}).encode())

def run(port=8085):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, AppHandler)
    print(f'Starting AGI App on http://localhost:{port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
