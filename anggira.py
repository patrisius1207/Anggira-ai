import asyncio
import websockets
import json
import urllib.request
import urllib.error
import urllib.parse
import re
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# ================= CONFIG =================
MCP_ENDPOINT = os.environ.get('MCP_ENDPOINT', '')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY') or "ISI_API_KEY_KAMU"
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')

ESP32_URL = "http://192.168.1.222"
MUSIC_SERVER = "http://192.168.1.3:8080"
DEFAULT_CITY = "Salatiga"

SYSTEM_PROMPT = """Kamu adalah Anggira, asisten AI pribadi yang ramah.
Jika user meminta memutar lagu, WAJIB gunakan tool play_song.
Jangan gunakan search_music.
Jawab singkat, jelas, bahasa Indonesia natural."""

executor = ThreadPoolExecutor(max_workers=4)

# ================= GROQ =================
def _groq_chat(messages):
    url = "https://api.groq.com/openai/v1/chat/completions"
    data = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "temperature": 0.7,
        "max_tokens": 300
    }).encode()

    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    })

    with urllib.request.urlopen(req, timeout=20) as r:
        result = json.loads(r.read().decode())
        return result['choices'][0]['message']['content']

async def groq_chat(messages):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _groq_chat, messages)

# ================= MUSIC =================
def play_song_http(song, artist=""):
    try:
        url = f"{MUSIC_SERVER}/stream_pcm?song={urllib.parse.quote(song)}&artist={urllib.parse.quote(artist)}"
        return urllib.request.urlopen(url).read().decode()
    except Exception as e:
        return f"Music error: {e}"

async def play_song(song, artist=""):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, play_song_http, song, artist)

# ================= ESP32 (FIX ONLY HERE) =================
def esp32_get(path):
    try:
        url = f"{ESP32_URL}{path}"
        req = urllib.request.Request(url, method="GET")

        with urllib.request.urlopen(req, timeout=5) as r:
            return r.read().decode(errors="ignore")

    except urllib.error.HTTPError as e:
        return f"HTTPError {e.code}: {e.reason}"

    except urllib.error.URLError as e:
        return f"URLError: {e.reason}"

    except Exception as e:
        return f"ESP32 error: {str(e)}"

async def lamp_on():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, esp32_get, "/on")

async def lamp_off():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, esp32_get, "/off")

# ================= SENSOR =================
def esp32_sensor():
    try:
        return urllib.request.urlopen(f"{ESP32_URL}/sensor_rumah").read().decode()
    except Exception as e:
        return f"Sensor error: {e}"

async def get_sensor_rumah():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, esp32_sensor)

# ================= JADWAL =================
def esp32_get_schedule():
    try:
        return urllib.request.urlopen(f"{ESP32_URL}/jadwal").read().decode()
    except Exception as e:
        return f"Jadwal error: {e}"

def esp32_set_schedule(on, off):
    try:
        return urllib.request.urlopen(f"{ESP32_URL}/set?on={on}&off={off}").read().decode()
    except Exception as e:
        return f"Set jadwal error: {e}"

async def get_schedule():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, esp32_get_schedule)

async def set_schedule(on, off):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, esp32_set_schedule, on, off)

# ================= WEATHER =================
async def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},ID&appid={OPENWEATHER_API_KEY}&units=metric&lang=id"
        with urllib.request.urlopen(url) as r:
            d = json.loads(r.read().decode())
        return f"{city}: {d['main']['temp']}°C, {d['weather'][0]['description']}"
    except Exception as e:
        return f"Cuaca error: {e}"

# ================= NEWS =================
async def get_news():
    try:
        xml = urllib.request.urlopen("https://news.google.com/rss?hl=id-ID&gl=ID&ceid=ID:id").read().decode()
        items = re.findall(r"<title>(.*?)</title>", xml)[1:6]
        return "Berita:\n" + "\n".join(items)
    except Exception as e:
        return f"News error: {e}"

# ================= MCP =================
async def handle_mcp():
    async with websockets.connect(MCP_ENDPOINT) as ws:
        async for message in ws:
            data = json.loads(message)
            method = data.get("method", "")
            msg_id = data.get("id")

            if method == "initialize":
                await ws.send(json.dumps({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"protocolVersion": "2024-11-05"}
                }))

            elif method == "tools/list":
                await ws.send(json.dumps({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {"name": "lamp_on"},
                            {"name": "lamp_off"},
                            {"name": "news"},
                            {"name": "weather"},
                            {"name": "time"},
                            {"name": "sensor_rumah"},
                            {"name": "get_schedule"},
                            {"name": "set_schedule"},
                            {
                                "name": "play_song",
                                "description": "Putar lagu dari internet",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "song": {"type": "string"},
                                        "artist": {"type": "string"}
                                    },
                                    "required": ["song"]
                                }
                            }
                        ]
                    }
                }))

            elif method == "tools/call":
                tool = data["params"]["name"]

                if tool == "lamp_on":
                    result = await lamp_on()
                elif tool == "lamp_off":
                    result = await lamp_off()
                elif tool == "news":
                    result = await get_news()
                elif tool == "weather":
                    result = await get_weather(DEFAULT_CITY)
                elif tool == "time":
                    result = datetime.now().strftime("%H:%M")
                elif tool == "sensor_rumah":
                    result = await get_sensor_rumah()
                elif tool == "get_schedule":
                    result = await get_schedule()
                elif tool == "set_schedule":
                    args = data["params"].get("arguments", {})
                    result = await set_schedule(
                        args.get("on", "18:00"),
                        args.get("off", "06:00")
                    )
                elif tool == "play_song":
                    args = data["params"].get("arguments", {})
                    result = await play_song(
                        args.get("song", ""),
                        args.get("artist", "")
                    )
                else:
                    result = "Tool tidak dikenal"

                await ws.send(json.dumps({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [
                            {"type": "text", "text": result}
                        ]
                    }
                }))

# ================= MAIN =================
async def main():
    print("🚀 Anggira FULL + MUSIC + SENSOR + JADWAL")
    await asyncio.gather(handle_mcp())

if __name__ == "__main__":
    asyncio.run(main())