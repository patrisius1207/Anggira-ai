# 🤖 Anggira AI Assistant

Asisten AI pribadi berbahasa Indonesia yang jalan di **STB Android yang sudah di-root** (ZTE ZXV10 B866F Telkomsel).

## ✨ Fitur

- 🤖 **Chat AI** — powered by Groq LLM (Llama 3.3 70B)
- 📰 **Berita** — Google News Indonesia (terkini, teknologi, olahraga, dll)
- 🌤 **Cuaca** — OpenWeatherMap (suhu, kelembapan, angin, prakiraan)
- 🕐 **Waktu** — info jam dan tanggal
- 🎵 **Musik** — streaming YouTube via ESP32 XiaoZhi
- 📱 **Telegram Bot** — kontrol semua fitur dari HP
- 🌐 **Dashboard Web** — setting via browser (port 8088)
- 🔄 **Auto Restart** — watchdog otomatis restart kalau mati
- 🔐 **SSH Remote** — akses STB dari PC via SSH port 8022

## 📋 Perintah Telegram

| Perintah | Fungsi |
|---|---|
| `/start` | Info dan daftar perintah |
| `/status` | Cek status server |
| `/restart` | Restart server |
| `/clear` | Hapus riwayat chat |
| `cuaca` | Cuaca default (Salatiga) |
| `cuaca Jakarta` | Cuaca kota tertentu |
| `prakiraan cuaca` | Prakiraan 24 jam |
| `berita hari ini` | Berita terkini |
| `berita teknologi` | Berita teknologi |
| `jam berapa sekarang` | Info waktu |
| *(teks bebas)* | Chat dengan AI |

## 🛠 Hardware

- **STB:** ZTE ZXV10 B866F 
- **Chipset:** Amlogic S905Y4 ARM 32-bit
- **RAM:** 2GB
- **OS:** Android TV 11 (rooted)
- **Konsumsi:** ~5-8 watt
- **ESP32:** ESP32-S3 dengan firmware XiaoZhi

## 🚀 Instalasi di STB

### 1. Install Termux
Download dari F-Droid: https://f-droid.org/packages/com.termux/

### 2. Install Dependencies
```bash
pkg update && pkg upgrade -y
pkg install python git openssh -y
pip install websockets yt-dlp
```

### 3. Clone & Setup
```bash
git clone https://github.com/patrisius1207/Anggira-ai.git
cd Anggira-ai
```

### 4. Set Environment
```bash
echo 'export MCP_ENDPOINT="wss://api.xiaozhi.me/mcp/?token=TOKEN"' >> ~/.bashrc
echo 'export TELEGRAM_BOT_TOKEN="TOKEN_BOT"' >> ~/.bashrc
echo 'export GROQ_API_KEY="gsk_..."' >> ~/.bashrc
echo 'export OPENWEATHER_API_KEY="..."' >> ~/.bashrc
source ~/.bashrc
```

### 5. Jalankan
```bash
sshd
python -u anggira.py > ~/anggira.log 2>&1 &
python -u dashboard.py > ~/dashboard.log 2>&1 &
bash watchdog.sh &
```

### 6. Autostart (install Termux:Boot dari F-Droid)
```bash
mkdir -p ~/.termux/boot
cp start_stb.sh ~/.termux/boot/start_server.sh
chmod +x ~/.termux/boot/start_server.sh
```

## 🌐 Dashboard Web

Akses dari browser di jaringan yang sama:
http://IP_STB:8088

## 🔑 API Keys yang Dibutuhkan

| API | Link Daftar | Gratis |
|---|---|---|
| Groq LLM | https://console.groq.com | ✅ |
| OpenWeatherMap | https://openweathermap.org/api | ✅ |
| Telegram Bot | @BotFather di Telegram | ✅ |
| XiaoZhi MCP | https://xiaozhi.me | ✅ |

## 📁 Struktur File

- `anggira.py` — Server utama (MCP + Telegram + AI)
- `dashboard.py` — Web dashboard (port 8088)
- `watchdog.sh` — Auto restart script
- `start_stb.sh` — Autostart script untuk Termux:Boot

## ⚠️ Catatan

- Tidak butuh pydantic/mcp library — cocok ARM 32-bit
- SSH port 8022 (bukan 22)
- Dashboard port 8088
- Token dan API key jangan di-commit ke GitHub!
