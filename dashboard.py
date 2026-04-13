import http.server
import json
import os
import subprocess
from urllib.parse import urlparse, parse_qs

CONFIG_FILE = os.path.expanduser("~/.anggira_config.json")

DEFAULT_CONFIG = {
    "mcp_endpoint": os.environ.get("MCP_ENDPOINT", ""),
    "telegram_token": os.environ.get("TELEGRAM_BOT_TOKEN", ""),
    "telegram_allowed_id": os.environ.get("TELEGRAM_ALLOWED_USER_ID", ""),
    "groq_api_key": os.environ.get("GROQ_API_KEY", ""),
    "openweather_api_key": os.environ.get("OPENWEATHER_API_KEY", ""),
    "default_city": "Salatiga",
    "ai_name": "Anggira",
    "ai_language": "Indonesia",
    "ai_personality": "ramah",
    "system_prompt": "Kamu adalah Anggira, asisten AI pribadi yang ramah dan helpful. Kamu berbicara bahasa Indonesia dengan sopan dan natural. Jawab dengan singkat dan jelas, maksimal 3 kalimat kecuali diminta lebih panjang.",
    "tts_voice": "perempuan",
    "tts_speed": "1.0"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
            for k, v in DEFAULT_CONFIG.items():
                if k not in cfg:
                    cfg[k] = v
            return cfg
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
    # Update bashrc
    lines_to_add = {
        "MCP_ENDPOINT": cfg.get("mcp_endpoint", ""),
        "TELEGRAM_BOT_TOKEN": cfg.get("telegram_token", ""),
        "TELEGRAM_ALLOWED_USER_ID": cfg.get("telegram_allowed_id", ""),
        "GROQ_API_KEY": cfg.get("groq_api_key", ""),
        "OPENWEATHER_API_KEY": cfg.get("openweather_api_key", ""),
    }
    bashrc = os.path.expanduser("~/.bashrc")
    with open(bashrc, "r") as f:
        lines = f.readlines()
    new_lines = []
    updated = set()
    for line in lines:
        skip = False
        for key in lines_to_add:
            if line.startswith(f"export {key}="):
                skip = True
                break
        if not skip:
            new_lines.append(line)
    for key, val in lines_to_add.items():
        if val:
            new_lines.append(f'export {key}="{val}"\n')
    with open(bashrc, "w") as f:
        f.writelines(new_lines)

def get_server_status():
    procs = subprocess.run(["pgrep", "-f", "anggira.py"], capture_output=True, text=True)
    running = bool(procs.stdout.strip())
    pid = procs.stdout.strip().replace("\n", ", ") or "N/A"
    mem = subprocess.run(["free", "-m"], capture_output=True, text=True).stdout
    mem_lines = mem.strip().split("\n")
    mem_used = mem_total = "N/A"
    if len(mem_lines) > 1:
        parts = mem_lines[1].split()
        if len(parts) >= 3:
            mem_total = parts[1]
            mem_used = parts[2]
    uptime = subprocess.run(["uptime", "-p"], capture_output=True, text=True).stdout.strip()
    return {"running": running, "pid": pid, "mem_used": mem_used, "mem_total": mem_total, "uptime": uptime}

HTML = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Anggira Dashboard</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; }
.header { background: linear-gradient(135deg, #1e3a5f, #0f172a); padding: 20px 30px; border-bottom: 1px solid #1e40af; display: flex; align-items: center; gap: 15px; }
.header h1 { font-size: 24px; color: #60a5fa; }
.header .subtitle { font-size: 13px; color: #94a3b8; }
.robot { font-size: 36px; }
.container { max-width: 900px; margin: 0 auto; padding: 25px 20px; }
.status-bar { display: flex; gap: 12px; margin-bottom: 25px; flex-wrap: wrap; }
.status-card { background: #1e293b; border-radius: 10px; padding: 15px 20px; flex: 1; min-width: 140px; border: 1px solid #334155; }
.status-card .label { font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
.status-card .value { font-size: 18px; font-weight: bold; }
.status-card .value.green { color: #22c55e; }
.status-card .value.red { color: #ef4444; }
.status-card .value.blue { color: #60a5fa; }
.tabs { display: flex; gap: 5px; margin-bottom: 20px; flex-wrap: wrap; }
.tab { padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; border: 1px solid #334155; background: #1e293b; color: #94a3b8; transition: all 0.2s; }
.tab.active { background: #1d4ed8; color: white; border-color: #1d4ed8; }
.tab:hover:not(.active) { background: #334155; color: #e2e8f0; }
.panel { display: none; }
.panel.active { display: block; }
.card { background: #1e293b; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #334155; }
.card h3 { font-size: 15px; color: #60a5fa; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; }
.form-group { margin-bottom: 15px; }
.form-group label { display: block; font-size: 13px; color: #94a3b8; margin-bottom: 6px; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px 14px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; color: #e2e8f0; font-size: 14px; outline: none; transition: border-color 0.2s; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { border-color: #1d4ed8; }
.form-group textarea { min-height: 100px; resize: vertical; font-family: inherit; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
.btn { padding: 10px 22px; border-radius: 8px; border: none; cursor: pointer; font-size: 14px; font-weight: 600; transition: all 0.2s; }
.btn-primary { background: #1d4ed8; color: white; }
.btn-primary:hover { background: #2563eb; }
.btn-success { background: #16a34a; color: white; }
.btn-success:hover { background: #15803d; }
.btn-danger { background: #dc2626; color: white; }
.btn-danger:hover { background: #b91c1c; }
.btn-warning { background: #d97706; color: white; }
.btn-warning:hover { background: #b45309; }
.btn-group { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
.alert { padding: 12px 16px; border-radius: 8px; margin-bottom: 15px; font-size: 14px; display: none; }
.alert.success { background: #064e3b; color: #34d399; border: 1px solid #065f46; }
.alert.error { background: #450a0a; color: #f87171; border: 1px solid #7f1d1d; }
.log-box { background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 15px; font-family: monospace; font-size: 12px; color: #94a3b8; height: 300px; overflow-y: auto; white-space: pre-wrap; word-break: break-all; }
.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }
.badge.green { background: #064e3b; color: #22c55e; }
.badge.red { background: #450a0a; color: #ef4444; }
.divider { border: none; border-top: 1px solid #334155; margin: 15px 0; }
@media (max-width: 600px) { .form-row { grid-template-columns: 1fr; } .status-bar { flex-direction: column; } }
</style>
</head>
<body>
<div class="header">
  <div class="robot">🤖</div>
  <div>
    <h1>Anggira Dashboard</h1>
    <div class="subtitle">STB Control Panel — Anggira AI Assistant</div>
  </div>
</div>
<div class="container">
  <div class="status-bar" id="statusBar">
    <div class="status-card"><div class="label">Server</div><div class="value" id="srvStatus">...</div></div>
    <div class="status-card"><div class="label">PID</div><div class="value blue" id="srvPid">...</div></div>
    <div class="status-card"><div class="label">RAM Dipakai</div><div class="value blue" id="srvMem">...</div></div>
    <div class="status-card"><div class="label">Uptime</div><div class="value blue" id="srvUptime">...</div></div>
  </div>

  <div class="tabs">
    <div class="tab active" onclick="showTab('server')">⚙️ Server</div>
    <div class="tab" onclick="showTab('ai')">🤖 AI</div>
    <div class="tab" onclick="showTab('api')">🔑 API Keys</div>
    <div class="tab" onclick="showTab('cuaca')">🌤 Cuaca</div>
    <div class="tab" onclick="showTab('log')">📋 Log</div>
  </div>

  <div id="alert" class="alert"></div>

  <!-- SERVER TAB -->
  <div id="tab-server" class="panel active">
    <div class="card">
      <h3>⚙️ Kontrol Server</h3>
      <div class="btn-group">
        <button class="btn btn-success" onclick="serverAction('start')">▶ Start</button>
        <button class="btn btn-danger" onclick="serverAction('stop')">⏹ Stop</button>
        <button class="btn btn-warning" onclick="serverAction('restart')">🔄 Restart</button>
        <button class="btn btn-primary" onclick="loadStatus()">🔃 Refresh Status</button>
      </div>
    </div>
    <div class="card">
      <h3>📡 MCP Endpoint</h3>
      <div class="form-group">
        <label>WebSocket MCP URL</label>
        <input type="text" id="mcp_endpoint" placeholder="wss://api.xiaozhi.me/mcp/?token=...">
      </div>
      <div class="form-group">
        <label>Telegram Bot Token</label>
        <input type="text" id="telegram_token" placeholder="1234567890:AAxxxx...">
      </div>
      <div class="form-group">
        <label>Telegram Allowed User ID (kosongkan = semua bisa akses)</label>
        <input type="text" id="telegram_allowed_id" placeholder="123456789">
      </div>
      <button class="btn btn-primary" onclick="saveConfig()">💾 Simpan</button>
    </div>
  </div>

  <!-- AI TAB -->
  <div id="tab-ai" class="panel">
    <div class="card">
      <h3>🤖 Kepribadian AI</h3>
      <div class="form-row">
        <div class="form-group">
          <label>Nama AI</label>
          <input type="text" id="ai_name" placeholder="Anggira">
        </div>
        <div class="form-group">
          <label>Bahasa Utama</label>
          <select id="ai_language">
            <option value="Indonesia">Indonesia</option>
            <option value="English">English</option>
            <option value="Jawa">Jawa</option>
          </select>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Kepribadian</label>
          <select id="ai_personality">
            <option value="ramah">Ramah & Santai</option>
            <option value="formal">Formal & Profesional</option>
            <option value="lucu">Lucu & Humoris</option>
            <option value="tegas">Tegas & To The Point</option>
          </select>
        </div>
        <div class="form-group">
          <label>Model AI</label>
          <select id="ai_model">
            <option value="llama-3.3-70b-versatile">Llama 3.3 70B (Terbaik)</option>
            <option value="llama-3.1-8b-instant">Llama 3.1 8B (Cepat)</option>
            <option value="gemma2-9b-it">Gemma 2 9B</option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label>System Prompt (instruksi AI)</label>
        <textarea id="system_prompt" rows="5"></textarea>
      </div>
      <button class="btn btn-primary" onclick="saveConfig()">💾 Simpan</button>
    </div>
  </div>

  <!-- API TAB -->
  <div id="tab-api" class="panel">
    <div class="card">
      <h3>🔑 API Keys</h3>
      <div class="form-group">
        <label>Groq API Key</label>
        <input type="password" id="groq_api_key" placeholder="gsk_...">
      </div>
      <div class="form-group">
        <label>OpenWeatherMap API Key</label>
        <input type="password" id="openweather_api_key" placeholder="a1b2c3...">
      </div>
      <button class="btn btn-primary" onclick="saveConfig()">💾 Simpan</button>
    </div>
  </div>

  <!-- CUACA TAB -->
  <div id="tab-cuaca" class="panel">
    <div class="card">
      <h3>🌤 Pengaturan Cuaca</h3>
      <div class="form-group">
        <label>Kota Default</label>
        <input type="text" id="default_city" placeholder="Salatiga">
      </div>
      <button class="btn btn-primary" onclick="saveConfig()">💾 Simpan</button>
      <hr class="divider">
      <h3>🌡 Test Cuaca Sekarang</h3>
      <div class="form-group">
        <label>Cek cuaca kota:</label>
        <input type="text" id="test_city" placeholder="Salatiga">
      </div>
      <button class="btn btn-success" onclick="testWeather()">🔍 Cek Cuaca</button>
      <div id="weather_result" style="margin-top:15px; color:#94a3b8; font-size:14px; white-space:pre-line;"></div>
    </div>
  </div>

  <!-- LOG TAB -->
  <div id="tab-log" class="panel">
    <div class="card">
      <h3>📋 Log Server</h3>
      <div class="btn-group" style="margin-bottom:10px;">
        <button class="btn btn-primary" onclick="loadLog()">🔃 Refresh Log</button>
        <button class="btn btn-danger" onclick="clearLog()">🗑 Clear Log</button>
      </div>
      <div class="log-box" id="logBox">Klik Refresh Log untuk melihat log...</div>
    </div>
  </div>
</div>

<script>
function showTab(name) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  event.target.classList.add('active');
  document.getElementById('tab-' + name).classList.add('active');
  if (name === 'log') loadLog();
}

function showAlert(msg, type) {
  const el = document.getElementById('alert');
  el.textContent = msg;
  el.className = 'alert ' + type;
  el.style.display = 'block';
  setTimeout(() => el.style.display = 'none', 4000);
}

async function loadStatus() {
  const r = await fetch('/api/status');
  const d = await r.json();
  document.getElementById('srvStatus').innerHTML = d.running
    ? '<span class="badge green">🟢 AKTIF</span>'
    : '<span class="badge red">🔴 MATI</span>';
  document.getElementById('srvPid').textContent = d.pid;
  document.getElementById('srvMem').textContent = d.mem_used + ' / ' + d.mem_total + ' MB';
  document.getElementById('srvUptime').textContent = d.uptime;
}

async function loadConfig() {
  const r = await fetch('/api/config');
  const d = await r.json();
  for (const [k, v] of Object.entries(d)) {
    const el = document.getElementById(k);
    if (el) el.value = v;
  }
}

async function saveConfig() {
  const fields = ['mcp_endpoint','telegram_token','telegram_allowed_id','groq_api_key',
                  'openweather_api_key','default_city','ai_name','ai_language',
                  'ai_personality','system_prompt'];
  const cfg = {};
  for (const f of fields) {
    const el = document.getElementById(f);
    if (el) cfg[f] = el.value;
  }
  const r = await fetch('/api/config', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(cfg)});
  const d = await r.json();
  if (d.ok) showAlert('✅ Pengaturan disimpan! Restart server untuk menerapkan perubahan.', 'success');
  else showAlert('❌ Gagal menyimpan: ' + d.error, 'error');
}

async function serverAction(action) {
  const r = await fetch('/api/server/' + action, {method:'POST'});
  const d = await r.json();
  if (d.ok) {
    showAlert('✅ ' + d.message, 'success');
    setTimeout(loadStatus, 2000);
  } else {
    showAlert('❌ ' + d.error, 'error');
  }
}

async function loadLog() {
  const r = await fetch('/api/log');
  const d = await r.json();
  const box = document.getElementById('logBox');
  box.textContent = d.log || '(log kosong)';
  box.scrollTop = box.scrollHeight;
}

async function clearLog() {
  await fetch('/api/log/clear', {method:'POST'});
  document.getElementById('logBox').textContent = '(log dibersihkan)';
}

async function testWeather() {
  const city = document.getElementById('test_city').value || 'Salatiga';
  document.getElementById('weather_result').textContent = 'Mengambil cuaca...';
  const r = await fetch('/api/weather?city=' + encodeURIComponent(city));
  const d = await r.json();
  document.getElementById('weather_result').textContent = d.result || d.error;
}

// Init
loadStatus();
loadConfig();
setInterval(loadStatus, 30000);
</script>
</body>
</html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html):
        body = html.encode()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(length)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == '/':
            self.send_html(HTML)
        elif path == '/api/status':
            self.send_json(get_server_status())
        elif path == '/api/config':
            self.send_json(load_config())
        elif path == '/api/log':
            log_file = os.path.expanduser('~/anggira.log')
            if os.path.exists(log_file):
                with open(log_file) as f:
                    lines = f.readlines()
                log = ''.join(lines[-100:])
            else:
                log = '(log tidak ditemukan)'
            self.send_json({'log': log})
        elif path == '/api/weather':
            city = qs.get('city', ['Salatiga'])[0]
            try:
                cfg = load_config()
                key = cfg.get('openweather_api_key', '')
                if not key:
                    self.send_json({'error': 'API key cuaca belum diset'})
                    return
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city},ID&appid={key}&units=metric&lang=id"
                import urllib.request
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=10) as r:
                    d = json.loads(r.read().decode())
                result = (
                    f"🌤 Cuaca {d['name']} saat ini:\n"
                    f"🌡 Suhu: {d['main']['temp']}°C (terasa {d['main']['feels_like']}°C)\n"
                    f"💧 Kelembapan: {d['main']['humidity']}%\n"
                    f"💨 Angin: {d['wind']['speed']} m/s\n"
                    f"☁️ Kondisi: {d['weather'][0]['description'].capitalize()}"
                )
                self.send_json({'result': result})
            except Exception as e:
                self.send_json({'error': str(e)})
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        path = self.path

        if path == '/api/config':
            try:
                body = self.read_body()
                cfg = json.loads(body)
                save_config(cfg)
                self.send_json({'ok': True})
            except Exception as e:
                self.send_json({'ok': False, 'error': str(e)})

        elif path == '/api/server/start':
            procs = subprocess.run(["pgrep", "-f", "anggira.py"], capture_output=True, text=True)
            if procs.stdout.strip():
                self.send_json({'ok': False, 'error': 'Server sudah jalan'})
            else:
                subprocess.Popen(
                    ["/data/data/com.termux/files/usr/bin/python", "-u",
                     "/data/data/com.termux/files/home/anggira.py"],
                    stdout=open(os.path.expanduser("~/anggira.log"), "a"),
                    stderr=subprocess.STDOUT
                )
                self.send_json({'ok': True, 'message': 'Server Anggira distart!'})

        elif path == '/api/server/stop':
            subprocess.run(["pkill", "-f", "anggira.py"])
            self.send_json({'ok': True, 'message': 'Server Anggira distop!'})

        elif path == '/api/server/restart':
            subprocess.run(["pkill", "-f", "anggira.py"])
            import time
            time.sleep(2)
            subprocess.Popen(
                ["/data/data/com.termux/files/usr/bin/python", "-u",
                 "/data/data/com.termux/files/home/anggira.py"],
                stdout=open(os.path.expanduser("~/anggira.log"), "a"),
                stderr=subprocess.STDOUT
            )
            self.send_json({'ok': True, 'message': 'Server Anggira direstart!'})

        elif path == '/api/log/clear':
            with open(os.path.expanduser("~/anggira.log"), "w") as f:
                f.write("")
            self.send_json({'ok': True})

        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    PORT = 8088
    server = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"🌐 Anggira Dashboard jalan di http://0.0.0.0:{PORT}")
    print(f"   Akses dari PC: http://192.168.1.3:{PORT}")
    server.serve_forever()
