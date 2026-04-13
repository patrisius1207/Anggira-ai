import asyncio
import websockets
import json
import urllib.request
import urllib.error
import re
import subprocess
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# ── Config ─────────────────────────────────────────────
MCP_ENDPOINT = os.environ.get('MCP_ENDPOINT', '')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_ALLOWED_ID = os.environ.get('TELEGRAM_ALLOWED_USER_ID', '')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')
DEFAULT_CITY = "Salatiga"

SYSTEM_PROMPT = """Kamu adalah Anggira, asisten AI pribadi yang ramah dan helpful.
Kamu berbicara bahasa Indonesia dengan sopan dan natural.
Kamu siap membantu kapan saja untuk menjawab pertanyaan, memutar musik, membacakan berita, info cuaca, dan berbagai tugas lainnya.
Jawab dengan singkat dan jelas, maksimal 3 kalimat kecuali diminta lebih panjang.
Jika ditanya musik, arahkan user untuk bicara langsung ke ESP32."""

executor = ThreadPoolExecutor(max_workers=4)

# ── Groq API ───────────────────────────────────────────
def _groq_chat(messages):
    url = "https://api.groq.com/openai/v1/chat/completions"
    data = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "max_tokens": 500
    }).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        result = json.loads(r.read().decode())
        return result['choices'][0]['message']['content']

async def groq_chat(messages):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _groq_chat, messages)

# ── Cuaca ──────────────────────────────────────────────
def _get_weather(city):
    if not OPENWEATHER_API_KEY:
        return "API key cuaca belum diset."
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},ID&appid={OPENWEATHER_API_KEY}&units=metric&lang=id"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read().decode())
    kondisi = d['weather'][0]['description'].capitalize()
    suhu = d['main']['temp']
    terasa = d['main']['feels_like']
    humidity = d['main']['humidity']
    angin = d['wind']['speed']
    kota = d['name']
    return (
        f"🌤 Cuaca {kota} saat ini:\n\n"
        f"🌡 Suhu: {suhu}°C (terasa {terasa}°C)\n"
        f"💧 Kelembapan: {humidity}%\n"
        f"💨 Angin: {angin} m/s\n"
        f"☁️ Kondisi: {kondisi}"
    )

def _get_forecast(city):
    if not OPENWEATHER_API_KEY:
        return "API key cuaca belum diset."
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},ID&appid={OPENWEATHER_API_KEY}&units=metric&lang=id&cnt=8"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read().decode())
    kota = d['city']['name']
    lines = [f"📅 Prakiraan cuaca {kota} 24 jam ke depan:\n"]
    for item in d['list'][:6]:
        waktu = datetime.fromtimestamp(item['dt']).strftime('%H:%M')
        suhu = item['main']['temp']
        kondisi = item['weather'][0]['description']
        hujan = item.get('rain', {}).get('3h', 0)
        rain_info = f" 🌧 {hujan}mm" if hujan > 0 else ""
        lines.append(f"⏰ {waktu} — {suhu}°C, {kondisi}{rain_info}")
    return "\n".join(lines)

async def get_weather(city=None):
    city = city or DEFAULT_CITY
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(executor, _get_weather, city)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return "API key cuaca belum aktif, tunggu 30-60 menit setelah daftar."
        elif e.code == 404:
            return f"Kota '{city}' tidak ditemukan."
        return f"Error cuaca: {e}"
    except Exception as e:
        return f"Gagal ambil cuaca: {e}"

async def get_forecast(city=None):
    city = city or DEFAULT_CITY
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(executor, _get_forecast, city)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return "API key cuaca belum aktif, tunggu 30-60 menit setelah daftar."
        return f"Error prakiraan: {e}"
    except Exception as e:
        return f"Gagal ambil prakiraan: {e}"

# ── Berita ─────────────────────────────────────────────
async def get_news(category="terkini"):
    urls = {
        "terkini":   "https://news.google.com/rss?hl=id-ID&gl=ID&ceid=ID:id",
        "nasional":  "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlRZU0FtVnVHZ0pWVXlnQVAB?hl=id-ID&gl=ID&ceid=ID:id",
        "dunia":     "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=id-ID&gl=ID&ceid=ID:id",
        "teknologi": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=id-ID&gl=ID&ceid=ID:id",
        "olahraga":  "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdZU0FtVnVHZ0pWVXlnQVAB?hl=id-ID&gl=ID&ceid=ID:id",
        "hiburan":   "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RZU0FtVnVHZ0pWVXlnQVAB?hl=id-ID&gl=ID&ceid=ID:id",
        "bisnis":    "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=id-ID&gl=ID&ceid=ID:id",
    }
    url = urls.get(category.lower(), urls["terkini"])
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            xml = r.read().decode("utf-8", errors="ignore")
        items = []
        for block in re.findall(r"<item>(.*?)</item>", xml, re.DOTALL)[:5]:
            title = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", block, re.DOTALL)
            source = re.search(r"<source>(.*?)</source>", block)
            if title:
                src = f" - {source.group(1)}" if source else ""
                items.append(f"{title.group(1).strip()}{src}")
        if not items:
            return "Tidak ada berita ditemukan."
        tanggal = datetime.now().strftime("%d %B %Y")
        return f"Berita {category.upper()} terbaru ({tanggal}):\n\n" + "\n\n".join(
            f"{i+1}. {t}" for i, t in enumerate(items)
        )
    except Exception as e:
        return f"Gagal ambil berita: {e}"

async def get_music_url(song_name):
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            lambda: subprocess.run(
                ["yt-dlp", "-f", "bestaudio", "--get-url", f"ytsearch1:{song_name}"],
                capture_output=True, text=True, timeout=30
            )
        )
        url = result.stdout.strip()
        if url:
            return {"success": True, "audio_url": url, "title": song_name, "source": "youtube", "result": f"Lagu ditemukan: {song_name}. Siap diputar di ESP32."}
    except Exception as e:
        print(f"[MUSIC] Error: {e}")
    return {"success": False, "result": "Lagu tidak ditemukan."}

# ── Status Server ──────────────────────────────────────
def get_server_status():
    procs = subprocess.run(["pgrep", "-f", "anggira.py"], capture_output=True, text=True)
    uptime_info = subprocess.run(["uptime"], capture_output=True, text=True).stdout.strip()
    mem_info = subprocess.run(["free", "-m"], capture_output=True, text=True).stdout
    mem_lines = mem_info.strip().split("\n")
    mem_used = "N/A"
    if len(mem_lines) > 1:
        mem_parts = mem_lines[1].split()
        if len(mem_parts) >= 3:
            mem_used = f"{mem_parts[2]}/{mem_parts[1]} MB"
    status = "🟢 AKTIF" if procs.stdout.strip() else "🔴 MATI"
    pid = procs.stdout.strip().replace("\n", ", ") or "N/A"
    now = datetime.now().strftime("%H:%M:%S")
    return (
        f"📊 Status Anggira MCP\n\n"
        f"{status}\n"
        f"🕐 Waktu: {now}\n"
        f"🔢 PID: {pid}\n"
        f"💾 RAM: {mem_used}\n"
        f"⚙️ {uptime_info}"
    )

# ── HTTP helpers ───────────────────────────────────────
def _http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=35) as r:
        return json.loads(r.read().decode())

def _http_post(url, data):
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())

# ── Telegram ───────────────────────────────────────────
async def tg_get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?timeout=10"
    if offset:
        url += f"&offset={offset}"
    try:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(executor, _http_get, url)
    except Exception as e:
        print(f"[TG] getUpdates error: {e}")
        return {"ok": False, "result": []}

async def tg_send(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text}).encode()
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(executor, _http_post, url, data)
    except Exception as e:
        print(f"[TG] sendMessage error: {e}")

chat_history = {}

async def telegram_loop():
    if not TELEGRAM_BOT_TOKEN:
        print("[TG] Token tidak ada, dinonaktifkan.")
        return
    print("[TG] Telegram bot aktif!")
    offset = None
    while True:
        try:
            data = await tg_get_updates(offset)
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                user_id = str(msg.get("from", {}).get("id", ""))
                text = msg.get("text", "").strip()
                if not text or not chat_id:
                    continue
                if TELEGRAM_ALLOWED_ID and user_id != TELEGRAM_ALLOWED_ID:
                    await tg_send(chat_id, "Akses ditolak.")
                    continue
                print(f"[TG] Pesan: {text}")
                text_lower = text.lower()

                # ── Commands ──
                if text == "/start":
                    await tg_send(chat_id,
                        "Halo! Saya Anggira, asisten AI pribadimu 🤖\n\n"
                        "Yang bisa saya lakukan:\n"
                        "🌤 cuaca / cuaca Jakarta\n"
                        "📅 prakiraan cuaca besok\n"
                        "📰 berita hari ini\n"
                        "📰 berita teknologi/olahraga/dll\n"
                        "🕐 jam berapa sekarang?\n"
                        "💬 chat bebas dengan AI\n\n"
                        "🔧 Perintah server:\n"
                        "📊 /status — cek status server\n"
                        "🔄 /restart — restart server\n"
                        "🗑 /clear — hapus riwayat chat"
                    )
                    continue

                if text == "/status":
                    loop = asyncio.get_event_loop()
                    status_msg = await loop.run_in_executor(executor, get_server_status)
                    await tg_send(chat_id, status_msg)
                    continue

                if text == "/restart":
                    await tg_send(chat_id, "🔄 Merestart Anggira...")
                    subprocess.Popen(
                        ["/data/data/com.termux/files/usr/bin/python", "-u",
                         "/data/data/com.termux/files/home/anggira.py"],
                        stdout=open("/data/data/com.termux/files/home/anggira.log", "a"),
                        stderr=subprocess.STDOUT
                    )
                    await asyncio.sleep(3)
                    await tg_send(chat_id, "✅ Anggira direstart! Server baru sudah jalan.")
                    continue

                if text == "/clear":
                    chat_history[user_id] = []
                    await tg_send(chat_id, "Riwayat chat dihapus! Kita mulai dari awal 😊")
                    continue

                # ── Cuaca ──
                if any(k in text_lower for k in ["cuaca", "suhu", "hujan", "panas", "dingin", "kelembapan", "angin", "temperatur"]):
                    city = DEFAULT_CITY
                    parts = text.split()
                    for i, word in enumerate(parts):
                        if word.lower() in ["di", "cuaca", "suhu"] and i + 1 < len(parts):
                            city = parts[i + 1]
                            break
                    if any(k in text_lower for k in ["prakiraan", "besok", "nanti", "ramalan", "forecast"]):
                        await tg_send(chat_id, f"Mengambil prakiraan cuaca {city}...")
                        result = await get_forecast(city)
                    else:
                        await tg_send(chat_id, f"Mengambil cuaca {city}...")
                        result = await get_weather(city)
                    await tg_send(chat_id, result)

                # ── Berita ──
                elif any(k in text_lower for k in ["berita", "news", "kabar"]):
                    cat = "terkini"
                    for k in ["teknologi", "olahraga", "hiburan", "bisnis", "nasional", "dunia"]:
                        if k in text_lower:
                            cat = k
                            break
                    await tg_send(chat_id, "Mengambil berita...")
                    result = await get_news(cat)
                    await tg_send(chat_id, result)

                # ── Waktu ──
                elif any(k in text_lower for k in ["jam", "waktu", "time", "tanggal", "sekarang"]):
                    now = datetime.now()
                    hari = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"][now.weekday()]
                    await tg_send(chat_id, f"🕐 Sekarang pukul {now.strftime('%H:%M')} WIB\n📅 {hari}, {now.strftime('%d %B %Y')}")

                # ── Chat AI ──
                else:
                    await tg_send(chat_id, "Anggira sedang berpikir... 🤔")
                    if user_id not in chat_history:
                        chat_history[user_id] = []
                    chat_history[user_id].append({"role": "user", "content": text})
                    if len(chat_history[user_id]) > 10:
                        chat_history[user_id] = chat_history[user_id][-10:]
                    try:
                        reply = await groq_chat(chat_history[user_id])
                        chat_history[user_id].append({"role": "assistant", "content": reply})
                        await tg_send(chat_id, reply)
                    except Exception as e:
                        await tg_send(chat_id, f"Maaf, Anggira sedang bermasalah: {e}")

        except Exception as e:
            print(f"[TG] Error: {e}")
            await asyncio.sleep(5)

# ── MCP ────────────────────────────────────────────────
async def handle_mcp():
    print("Connecting to MCP...")
    async with websockets.connect(MCP_ENDPOINT) as ws:
        print("Connected to Anggira MCP!")
        async for message in ws:
            try:
                data = json.loads(message)
                method = data.get("method", "")
                msg_id = data.get("id")
                print(f"<- {method}")
                if method == "initialize":
                    await ws.send(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "Anggira MCP", "version": "1.0.0"}}}))
                    print("-> Handshake OK!")
                elif method == "tools/list":
                    await ws.send(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                        {"name": "get_latest_news", "description": "Ambil berita terbaru dari Google News Indonesia. Category: terkini, nasional, dunia, teknologi, olahraga, hiburan, bisnis", "inputSchema": {"type": "object", "properties": {"category": {"type": "string"}, "jumlah": {"type": "integer"}}}},
                        {"name": "search_music_url", "description": "Cari dan stream lagu dari YouTube", "inputSchema": {"type": "object", "properties": {"song_name": {"type": "string"}}, "required": ["song_name"]}},
                        {"name": "get_current_time", "description": "Dapatkan waktu sekarang", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "get_weather", "description": "Dapatkan info cuaca terkini. Param city opsional, default Salatiga.", "inputSchema": {"type": "object", "properties": {"city": {"type": "string"}}}}
                    ]}}))
                    print("-> Tools list sent!")
                elif method == "tools/call":
                    tool = data["params"]["name"]
                    args = data["params"].get("arguments", {})
                    print(f"-> Tool: {tool}")
                    if tool == "get_latest_news":
                        result = await get_news(args.get("category", "terkini"))
                    elif tool == "search_music_url":
                        music = await get_music_url(args.get("song_name", ""))
                        result = json.dumps(music, ensure_ascii=False)
                    elif tool == "get_current_time":
                        now = datetime.now()
                        hari = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"][now.weekday()]
                        result = f"Sekarang pukul {now.strftime('%H:%M')} WIB, {hari} {now.strftime('%d %B %Y')}."
                    elif tool == "get_weather":
                        result = await get_weather(args.get("city", DEFAULT_CITY))
                    else:
                        result = f"Tool tidak dikenal: {tool}"
                    await ws.send(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": result}]}}))
                    print(f"-> Response sent: {tool}")
                else:
                    if msg_id is not None:
                        await ws.send(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {}}))
            except Exception as e:
                print(f"[MCP ERROR] {e}")

async def mcp_loop():
    while True:
        try:
            await handle_mcp()
        except Exception as e:
            print(f"[MCP] Reconnecting in 5s... ({e})")
            await asyncio.sleep(5)

# ── Main ───────────────────────────────────────────────
async def main():
    print("🤖 Anggira AI Assistant - STB Edition")
    print(f"📡 MCP: {'OK' if MCP_ENDPOINT else 'TIDAK ADA'}")
    print(f"🤖 Groq: {'OK' if GROQ_API_KEY else 'TIDAK ADA'}")
    print(f"📱 Telegram: {'OK' if TELEGRAM_BOT_TOKEN else 'TIDAK ADA'}")
    print(f"🌤 Cuaca: {'OK' if OPENWEATHER_API_KEY else 'TIDAK ADA'}")
    await asyncio.gather(
        mcp_loop(),
        telegram_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())
