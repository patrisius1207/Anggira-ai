🤖 Anggira AI
Smart Home Assistant • ESP32 • XiaoZhi MCP • AI Powered
<p align="center"> <img src="https://img.shields.io/badge/ESP32-IoT-blue?style=for-the-badge"/> <img src="https://img.shields.io/badge/Python-Async-green?style=for-the-badge"/> <img src="https://img.shields.io/badge/AI-Groq%20LLM-orange?style=for-the-badge"/> <img src="https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge"/> <img src="https://img.shields.io/badge/Status-Production-brightgreen?style=for-the-badge"/> </p> <p align="center"> <b>Ekosistem Smart Home berbasis AI dengan 2 ESP32 + STB Android + Voice Assistant</b> </p>
🎬 Demo
<p align="center"> <img src="https://user-images.githubusercontent.com/placeholder/dashboard.png" width="80%"/> </p> <p align="center"> <img src="https://user-images.githubusercontent.com/placeholder/telegram.gif" width="60%"/> </p>
🧠 Arsitektur Sistem
        📱 Telegram / Voice
               │
               ▼
        🤖 Anggira AI (STB)
   (Groq LLM + MCP + Python)
               │
      ┌────────┴────────┐
      ▼                 ▼
 ESP32-S3          ESP32-C3
 (XiaoZhi AI)      (Sensor Rumah)
      │                 │
 🎤 Voice AI        🌡 Sensor + Servo
🧩 Komponen Utama
🔹 ESP32-C3 — Smart Sensor Node
🌡 AHT20 → suhu & kelembapan
🌬 BMP280 → tekanan udara
💡 Servo → kontrol saklar lampu
🌐 Web dashboard real-time
⏰ Jadwal otomatis lampu
🔹 ESP32-S3 — XiaoZhi Voice AI
🎤 Voice assistant (real-time)
🔗 MCP client ke Anggira
🎵 Audio playback / streaming

📦 Firmware:
👉 https://github.com/78/xiaozhi-esp32

🔹 STB Android — AI Core System
📦 Device: ZTE ZXV10 B866F (Rooted)
🧠 Menjalankan:
AI (Groq LLM)
Telegram Bot
MCP Server
Dashboard Web
✨ Fitur
🤖 AI System
Chat AI natural (Bahasa Indonesia)
Integrasi MCP (XiaoZhi)
Multi-platform (Telegram + Voice)
🏠 Smart Home
Kontrol lampu ON/OFF
Jadwal otomatis (timer harian)
Monitoring sensor rumah
📊 Monitoring
🌡 Suhu
💧 Kelembapan
🌬 Tekanan udara
💡 Status lampu
🌐 Dual Dashboard
Dashboard	Fungsi
ESP32	Monitoring sensor
STB	Status AI & sistem
📱 Telegram Bot
Kontrol perangkat
Ambil data sensor
Chat AI langsung
📋 Command Telegram
Command	Fungsi
/start	Start bot
sensor rumah	Data sensor
lampu nyala	ON
lampu mati	OFF
cuaca	Info cuaca
berita	News
jam	Waktu
bebas	Chat AI
🌐 API Endpoint ESP32
📊 Sensor
GET /sensor_rumah
{
  "nama": "sensor rumah",
  "temperature": 27.5,
  "humidity": 60.2,
  "pressure": 1008.3,
  "lamp": "on"
}
💡 Lamp Control
GET /on
GET /off
⏰ Schedule
GET /set?on=18:00&off=06:00
🚀 Instalasi (STB via Termux)
1. Setup
pkg update && pkg upgrade -y
pkg install python git openssh -y
pip install websockets
2. Clone Repo
git clone https://github.com/patrisius1207/Anggira-ai.git
cd Anggira-ai
3. Environment
export MCP_ENDPOINT="wss://api.xiaozhi.me/mcp/?token=TOKEN"
export TELEGRAM_BOT_TOKEN="TOKEN"
export GROQ_API_KEY="gsk_..."
export OPENWEATHER_API_KEY="..."
4. Run
python anggira.py
🌐 Dashboard
Service	URL
ESP32 Sensor	http://192.168.1.222

STB Dashboard	http://IP_STB:8088
📁 Struktur Project
Anggira-ai/
├── anggira.py        # Core AI system
├── dashboard.py      # Web dashboard
├── watchdog.sh       # Auto restart
├── start_stb.sh      # Boot script
🔐 API & Integrasi
Service	Link
Groq LLM	https://console.groq.com

OpenWeather	https://openweathermap.org/api

Telegram Bot	@BotFather
XiaoZhi MCP	https://xiaozhi.me
⚠️ Notes
⚡ Optimized untuk ARM 32-bit (STB)
🔐 Jangan commit API key
📶 Semua device harus satu jaringan
🔁 Gunakan watchdog untuk stabilitas
🛣 Roadmap
 Integrasi AC / IR Remote
 Voice offline mode
 CCTV AI detection
 Notifikasi otomatis Telegram
 Smart energy monitoring
👨‍💻 Author

Patrisius Wogananda

⭐ Support

Kalau project ini membantu:

⭐ Star repository
🚀 Fork & kembangkan
🔥 Share ke komunitas
