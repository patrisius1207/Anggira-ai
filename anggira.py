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

# ================= CONFIG =================
MCP_ENDPOINT = os.environ.get('MCP_ENDPOINT', '')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY') or "ISI_API_KEY_KAMU"
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')
ESP32_URL = "http://192.168.1.222"
DEFAULT_CITY = "Salatiga"

SYSTEM_PROMPT = """Kamu adalah Anggira, asisten AI pribadi yang ramah.
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
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    })

    with urllib.request.urlopen(req, timeout=20) as r:
        result = json.loads(r.read().decode())
        return result['choices'][0]['message']['content']

async def groq_chat(messages):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _groq_chat, messages)

# ================= ESP32 =================
def esp32_get(path):
    try:
        return urllib.request.urlopen(f"{ESP32_URL}{path}").read().decode()
    except Exception as e:
        return f"ESP32 error: {e}"

async def lamp_on():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, esp32_get, "/on")

async def lamp_off():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, esp32_get, "/off")

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

# ================= TELEGRAM =================
def _http_get(url):
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read().decode())

def _http_post(url, data):
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

async def tg_send(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text}).encode()

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, _http_post, url, data)

async def telegram_loop():
    if not TELEGRAM_BOT_TOKEN:
        print("[TG] Disabled")
        return

    print("[TG] Aktif")
    offset = None

    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?timeout=10"
            if offset:
                url += f"&offset={offset}"

            data = await asyncio.get_event_loop().run_in_executor(executor, _http_get, url)

            for update in data.get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "")

                if not text:
                    continue

                text_lower = text.lower()
                print("[TG]", text)

                if text == "/start":
                    await tg_send(chat_id, "Halo! Anggira siap 🤖")
                    continue

                # ===== LAMPU =====
                if "lampu" in text_lower or "teras" in text_lower:
                    if any(k in text_lower for k in ["nyala", "hidup", "on"]):
                        await tg_send(chat_id, "Menyalakan lampu...")
                        await lamp_on()
                        await tg_send(chat_id, "Lampu teras ON 💡")
                        continue

                    elif any(k in text_lower for k in ["mati", "off"]):
                        await tg_send(chat_id, "Mematikan lampu...")
                        await lamp_off()
                        await tg_send(chat_id, "Lampu teras OFF 🌙")
                        continue

                # ===== AI =====
                await tg_send(chat_id, "🤔...")
                reply = await groq_chat([{"role": "user", "content": text}])
                await tg_send(chat_id, reply)

        except Exception as e:
            print("[TG ERROR]", e)
            await asyncio.sleep(5)

# ================= MCP (XIOZHI) =================
async def handle_mcp():
    print("Connecting to XiaoZhi MCP...")

    async with websockets.connect(MCP_ENDPOINT) as ws:
        print("✅ Connected to XiaoZhi!")

        async for message in ws:
            try:
                data = json.loads(message)
                method = data.get("method", "")
                msg_id = data.get("id")

                print("[MCP]", method)

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
                                {"name": "time"}
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
                    else:
                        result = "Tool tidak dikenal"

                    await ws.send(json.dumps({
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "content": [{"type": "text", "text": result}]
                        }
                    }))

            except Exception as e:
                print("[MCP ERROR]", e)

async def mcp_loop():
    while True:
        try:
            if MCP_ENDPOINT:
                await handle_mcp()
            else:
                await asyncio.sleep(5)
        except Exception as e:
            print("[MCP DISCONNECT]", e)
            await asyncio.sleep(5)

# ================= MAIN =================
async def main():
    print("🚀 Anggira FULL ONLINE (FINAL)")

    await asyncio.gather(
        telegram_loop(),
        mcp_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())
