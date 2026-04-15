# 🤖 Anggira AI – Smart Home Assistant ESP32 + XiaoZhi MCP

<p align="center">
  <img src="https://img.shields.io/badge/ESP32-IoT-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Python-Async-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/AI-Groq%20LLM-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Production-brightgreen?style=for-the-badge"/>
</p>

<p align="center">
  <b>Smart Home System berbasis AI (Groq + MCP + ESP32 + STB Android)</b><br/>
  Voice AI • Telegram Control • Sensor Rumah • Automation
</p>

---

## 🎬 Demo

<p align="center">
  <img src="https://user-images.githubusercontent.com/placeholder/dashboard.png" width="80%"/>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/placeholder/telegram.gif" width="60%"/>
</p>

---

## 🧠 Arsitektur Sistem


📱 Telegram / Voice Input
│
▼
🤖 Anggira AI (STB Android)
Groq LLM + MCP Server + Python
│
┌────────┴────────┐
▼ ▼
ESP32-S3 ESP32-C3
(XiaoZhi AI) (Sensor Rumah)
│ │
Voice AI Sensor + Servo Lampu


---

## 🧩 Komponen Sistem

### 🔹 ESP32-C3 – Smart Sensor Node
- 🌡 AHT20 → suhu & kelembapan  
- 🌬 BMP280 → tekanan udara  
- 💡 Servo → saklar lampu  
- 🌐 Web dashboard monitoring  
- ⏰ Jadwal otomatis lampu  

---

### 🔹 ESP32-S3 – XiaoZhi Voice AI
- 🎤 Voice assistant real-time  
- 🔗 MCP client ke Anggira AI  
- 🎵 Audio & voice interaction  

📦 Firmware:
👉 https://github.com/78/xiaozhi-esp32

---

### 🔹 STB Android – AI Core
- 📦 Device: ZTE ZXV10 B866F (Rooted)  
- 🧠 Menjalankan:
  - Groq LLM AI
  - Telegram Bot
  - MCP Server
  - Web Dashboard

---

## ✨ Fitur Utama

### 🤖 AI Assistant
- Chat AI Bahasa Indonesia
- Voice AI (XiaoZhi)
- MCP integration

### 🏠 Smart Home
- Lampu ON/OFF
- Jadwal otomatis
- Kontrol jarak jauh

### 📊 Monitoring
- 🌡 Suhu
- 💧 Kelembapan
- 🌬 Tekanan udara
- 💡 Status lampu

### 🌐 Dual Dashboard
- ESP32 Dashboard → sensor rumah
- STB Dashboard → AI system

### 📱 Telegram Bot
- Kontrol perangkat
- Ambil sensor rumah
- Chat AI langsung

---

## 📋 Telegram Commands

| Command | Fungsi |
|--------|--------|
| `/start` | Start bot |
| `sensor rumah` | Data sensor |
| `lampu nyala` | ON lampu |
| `lampu mati` | OFF lampu |
| `cuaca` | Info cuaca |
| `berita` | News |
| `jam` | Waktu |
| bebas | Chat AI |

---

## 🌐 API ESP32-C3

### 📊 Sensor Rumah

GET /sensor_rumah
```json
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
⏰ Jadwal Lampu
GET /set?on=18:00&off=06:00

🚀 Instalasi (STB / Termux)
1. Install Dependencies
pkg update && pkg upgrade -y
pkg install python git openssh -y
pip install websockets
2. Clone Repo
git clone https://github.com/patrisius1207/Anggira-ai.git
cd Anggira-ai
3. Environment Variables
export MCP_ENDPOINT="wss://api.xiaozhi.me/mcp/?token=TOKEN"
export TELEGRAM_BOT_TOKEN="TOKEN"
export GROQ_API_KEY="gsk_..."
export OPENWEATHER_API_KEY="..."
4. Run System
python anggira.py
🌐 Dashboard Access
System	URL
ESP32 Sensor	http://192.168.1.222

STB AI Dashboard	http://IP_STB:8088
📁 Project Structure
Anggira-ai/
├── anggira.py        # AI + Telegram + MCP Core
├── dashboard.py      # Web Dashboard STB
├── watchdog.sh       # Auto restart system
├── start_stb.sh      # Boot automation
🔐 API Services
Service	Link
Groq LLM	https://console.groq.com

OpenWeather	https://openweathermap.org/api

Telegram Bot	@BotFather
XiaoZhi MCP	https://xiaozhi.me
⚠️ Notes
Optimized untuk ARM 32-bit (STB Android)
Jangan upload API key ke GitHub
Semua device harus dalam 1 jaringan WiFi
Gunakan watchdog untuk stabilitas
🛣 Roadmap
 Kontrol AC / IR Remote
 Voice offline mode
 AI CCTV detection
 Notifikasi otomatis Telegram
 Smart energy monitoring
👨‍💻 Author

Patrisius Wogananda

⭐ Support Project

Jika project ini membantu:

⭐ Star repo ini
🍴 Fork & improve
🚀 Share ke komunitas IoT

💡 "Smart home bukan hanya otomatis, tapi harus bisa memahami penggunanya."
