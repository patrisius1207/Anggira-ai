# 🤖 Anggira AI – Smart Home Intelligence System

![ESP32](https://img.shields.io/badge/ESP32--S3%2FC3-blue?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Groq%20LLM-orange?style=for-the-badge)
![MCP](https://img.shields.io/badge/MCP-Protocol-purple?style=for-the-badge)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**⚡ AI Smart Home Ecosystem powered by ESP32 + STB Android + Groq + MCP**  
Voice AI • Music Streaming • Automation • IoT Sensor • Telegram Control

---

## 🌐 Language / Bahasa

- [English](#-english-version)
- [Bahasa Indonesia](#-bahasa-indonesia)

---

## 🇺🇸 English Version

### 🧠 System Architecture

This system integrates Large Language Models (LLM) with IoT hardware to create a responsive smart home ecosystem. It utilizes a **Rooted Android STB** as the Brain Server to bridge communication between users, AI, and physical sensors.

### 🧩 IoT Devices

- **🎤 ESP32-S3 (XiaoZhi AI Voice Node):** Handles high-quality voice I/O and acts as an MCP client for real-time AI interaction with low latency. Supports MP3 music streaming with real-time lyric display.
- **🏠 ESP32-C3 (Smart Home Sensor Node):** Monitors environment via `AHT20` & `BMP280` sensors and controls appliances via Relay.
- **🧠 STB Android (AI Brain Server):** Powered by ZTE ZXV10 B866F. Runs Termux + Python stack. Processes natural language via Groq LLM, manages the Telegram Bot gateway, and serves the music streaming backend.

### ✨ Features

- **AI System:** Natural conversational AI, Real-time voice assistant, and direct MCP tool execution.
- **🎵 Music Streaming:** Voice-activated music playback on ESP32. YouTube audio search via `yt-dlp`, real-time MP3 transcoding via FFmpeg, synchronized LRC lyric display on ESP32 screen.
- **Smart Home:** Remote lamp control, automated scheduling, and Telegram integration.
- **Monitoring:** Live tracking of temperature, humidity, and atmospheric pressure.

### 🎵 Music System Architecture

```
User Voice → ESP32-S3 → XiaoZhi MCP → anggira.py (STB)
                                            ↓
                                    stream_server.py (Flask :8080)
                                            ↓
                                    yt-dlp → YouTube Audio URL
                                            ↓
                                    FFmpeg → MP3 Stream → ESP32
                                            ↓
                                    lrclib.net → LRC Lyrics → ESP32 Display
```

**Music Server Endpoints:**

| Endpoint | Description |
|---|---|
| `GET /stream_pcm?song=&artist=` | Search song, returns audio & lyric URLs |
| `GET /play?url=` | Stream MP3 audio via FFmpeg |
| `GET /lyrics?song=&artist=` | Serve synced LRC lyrics |
| `GET /health` | Server health check |

### 📱 Telegram Commands

| Command | Function |
|---|---|
| `sensor rumah` | Get latest sensor data |
| `lampu nyala` | Turn ON the lamp |
| `lampu mati` | Turn OFF the lamp |
| `cuaca` | Real-time weather info |
| `berita` | Latest news updates |
| `jam` | Current system time |
| `putar lagu <title>` | Play music on ESP32 |

---

## 🇮🇩 Bahasa Indonesia

### 🧠 Arsitektur Sistem

Sistem ini mengintegrasikan LLM dengan hardware IoT untuk menciptakan ekosistem rumah pintar yang responsif. Menggunakan **STB Android (Rooted)** sebagai Brain Server yang menjembatani komunikasi antara pengguna, AI, dan sensor fisik.

### 🧩 Perangkat IoT

- **🎤 ESP32-S3 (XiaoZhi AI Voice Node):** Menangani input/output suara dan berperan sebagai MCP client untuk interaksi AI real-time dengan latensi rendah. Mendukung streaming musik MP3 dengan tampilan lirik sinkron.
- **🏠 ESP32-C3 (Smart Home Sensor Node):** Memantau lingkungan melalui sensor `AHT20` & `BMP280` serta mengontrol perangkat via Relay.
- **🧠 STB Android (AI Brain Server):** Menggunakan ZTE ZXV10 B866F. Menjalankan Termux + Python stack. Memproses bahasa natural via Groq LLM, mengelola gateway Telegram Bot, dan menyajikan backend streaming musik.

### ✨ Fitur Utama

- **Sistem AI:** Percakapan AI yang natural, asisten suara real-time, dan eksekusi tool MCP secara langsung.
- **🎵 Streaming Musik:** Pemutaran musik via perintah suara di ESP32. Pencarian audio YouTube via `yt-dlp`, transcoding MP3 real-time via FFmpeg, tampilan lirik LRC sinkron di layar ESP32.
- **Smart Home:** Kontrol lampu jarak jauh, penjadwalan otomatis, dan integrasi Telegram.
- **Monitoring:** Pelacakan langsung suhu, kelembapan, dan tekanan udara.

### 🎵 Arsitektur Sistem Musik

```
Perintah Suara → ESP32-S3 → XiaoZhi MCP → anggira.py (STB)
                                                ↓
                                        stream_server.py (Flask :8080)
                                                ↓
                                        yt-dlp → URL Audio YouTube
                                                ↓
                                        FFmpeg → Stream MP3 → ESP32
                                                ↓
                                        lrclib.net → Lirik LRC → Layar ESP32
```

**Endpoint Music Server:**

| Endpoint | Keterangan |
|---|---|
| `GET /stream_pcm?song=&artist=` | Cari lagu, kembalikan URL audio & lirik |
| `GET /play?url=` | Stream audio MP3 via FFmpeg |
| `GET /lyrics?song=&artist=` | Sajikan lirik LRC sinkron |
| `GET /health` | Cek status server |

**Contoh perintah suara:**
> *"Anggira, putar lagu Tanah Airku"*  
> *"Putar lagu Coldplay - The Scientist"*  
> *"Hentikan musik"*

### 📱 Perintah Telegram

| Perintah | Fungsi |
|---|---|
| `sensor rumah` | Mengambil data sensor terbaru |
| `lampu nyala` | Menyalakan lampu |
| `lampu mati` | Mematikan lampu |
| `cuaca` | Info cuaca real-time |
| `berita` | Berita terkini |
| `jam` | Waktu sistem saat ini |
| `putar lagu <judul>` | Putar musik di ESP32 |

---

## 🌐 Dashboard & Integration

| Module | URL / Resource |
|---|---|
| **ESP32 Sensor** | `http://192.168.1.222` |
| **Music Server** | `http://[IP_STB]:8080` |
| **STB AI Panel** | `http://[IP_STB]:8088` |
| **Groq AI** | [console.groq.com](https://console.groq.com) |
| **OpenWeather** | [openweathermap.org](https://openweathermap.org/api) |
| **Firmware** | [github.com/78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Voice AI Node | ESP32-S3, XiaoZhi firmware |
| Brain Server | Android STB (Rooted), Termux |
| AI Engine | Groq LLM (llama-3.3-70b-versatile) |
| Protocol | MCP (Model Context Protocol) over WebSocket |
| Music Backend | Python Flask, yt-dlp, FFmpeg |
| Lyrics | lrclib.net (free, no API key) |
| Messaging | Telegram Bot API |
| Weather | OpenWeatherMap API |
| Sensor | AHT20, BMP280 via ESP32-C3 |

---

## ⚠️ System Notes

1. **Security:** Do not expose API keys to public repositories.
2. **Networking:** All devices must be on the same WiFi network. Disable AP Isolation on router.
3. **Root Access:** Android STB must be rooted for Termux full access.
4. **Stability:** Launcher watchdog (`launcher.sh`) auto-restarts crashed services.
5. **Music:** STB must have `ffmpeg` installed via Termux (`pkg install ffmpeg`) and `yt-dlp` via pip.

---

## 👨‍💻 Author

**patrisius1207**

---

## ⭐ Support Project

- ⭐ **Star** this repository
- 🍴 **Fork** & improve the code
- 🚀 **Share** with the IoT community
