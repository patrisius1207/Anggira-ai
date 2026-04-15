import asyncio
import websockets
import json
import base64
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor
import urllib.request

PORT = 8000
executor = ThreadPoolExecutor(max_workers=4)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

SYSTEM_PROMPT = """Kamu adalah Anggira, asisten AI Indonesia yang ramah.
Jawab singkat, jelas, natural. Maksimal 2 kalimat.
"""

# =========================
# 🔥 GROQ CHAT
# =========================
def _groq_chat(text):
    url = "https://api.groq.com/openai/v1/chat/completions"

    data = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    }).encode()

    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    })

    with urllib.request.urlopen(req, timeout=20) as r:
        result = json.loads(r.read().decode())
        return result["choices"][0]["message"]["content"]


async def groq_chat(text):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _groq_chat, text)


# =========================
# 🎤 STT (WHISPER CPP)
# =========================
def stt_whisper():
    try:
        result = subprocess.run(
            [
                "./main",
                "-m", "models/ggml-base.bin",
                "-f", "input.raw",
                "-nt"
            ],
            cwd="whisper.cpp",
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"(STT error: {e})"


# =========================
# 🔊 TTS (dummy PCM)
# =========================
def tts_dummy(text):
    # nanti bisa ganti Piper / Coqui
    print(f"[TTS] {text}")
    return b'\x00\x00' * 8000


# =========================
# 🎧 HANDLE ESP32
# =========================
async def handle_esp32(ws):
    print("📡 ESP32 connected")

    async for message in ws:
        try:
            data = json.loads(message)
            method = data.get("method", "")

            if method == "device.audio":

                audio_b64 = data["params"]["audio"]
                audio_bytes = base64.b64decode(audio_b64)

                print(f"[AUDIO IN] {len(audio_bytes)} bytes")

                # simpan file
                with open("input.raw", "ab") as f:
                    f.write(audio_bytes)

                # =================
                # STT
                # =================
                text = stt_whisper()

                if not text:
                    text = "halo anggira"

                print(f"[STT] {text}")

                # =================
                # AI
                # =================
                reply = await groq_chat(text)
                print(f"[AI] {reply}")

                # =================
                # TTS
                # =================
                audio_out = tts_dummy(reply)

                audio_b64_out = base64.b64encode(audio_out).decode()

                # =================
                # SEND BACK
                # =================
                await ws.send(json.dumps({
                    "jsonrpc": "2.0",
                    "method": "device.audio",
                    "params": {
                        "audio": audio_b64_out
                    }
                }))

        except Exception as e:
            print(f"[ERROR] {e}")


# =========================
# 🚀 START SERVER
# =========================
async def main():
    print(f"🚀 MCP Server running on port {PORT}")
    async with websockets.serve(handle_esp32, "0.0.0.0", PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())

