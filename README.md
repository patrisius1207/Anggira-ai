# 🤖 Anggira AI – Smart Home Intelligence System

<p align="center"> 
  <img src="https://img.shields.io/badge/ESP32-S3%2FC3-blue?style=for-the-badge"/> 
  <img src="https://img.shields.io/badge/AI-Groq%20LLM-orange?style=for-the-badge"/> 
  <img src="https://img.shields.io/badge/MCP-Protocol-purple?style=for-the-badge"/> 
  <img src="https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge"/> 
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/> 
</p>

<p align="center"> 
  <b>⚡ AI Smart Home Ecosystem powered by ESP32 + STB Android + Groq + MCP</b><br/> 
  Voice AI • Automation • IoT Sensor • Telegram Control 
</p>

---

## 🌐 Language / Bahasa
* [English](#english)
* [Bahasa Indonesia](#bahasa-indonesia)

---

<div id="english"></div>

## 🇺🇸 English Version

### 🧠 System Architecture
This system integrates Large Language Models (LLM) with IoT hardware to create a responsive smart home ecosystem. It utilizes a **Rooted Android STB** as the Brain Server to bridge communication between users, AI, and physical sensors.

### 🧩 IoT Devices
* **🎤 ESP32-S3 (XiaoZhi AI Voice Node):** Handles high-quality voice I/O and acts as an MCP client for real-time AI interaction with low latency.
* **🏠 ESP32-C3 (Smart Home Sensor Node):** Monitors environment via `AHT20` & `BMP280` sensors and controls appliances via Relay.
* **🧠 STB Android (AI Brain Server):** Powered by ZTE ZXV10 B866F. Processes natural language via Groq LLM and manages the Telegram Bot gateway.

### ✨ Features
* **AI System:** Natural conversational AI, Real-time voice assistant, and direct MCP tool execution.
* **Smart Home:** Remote lamp control, automated scheduling, and Telegram integration.
* **Monitoring:** Live tracking of temperature, humidity, and atmospheric pressure.

### 📱 Telegram Commands
| Command | Function |
| :--- | :--- |
| `sensor rumah` | Get latest sensor data |
| `lampu nyala` | Turn ON the lamp |
| `lampu mati` | Turn OFF the lamp |
| `cuaca` | Real-time weather info |
| `berita` | Latest news updates |
| `jam` | Current system time |

---

<div id="bahasa-indonesia"></div>

## 🇮🇩 Bahasa Indonesia

### 🧠 Arsitektur Sistem
Sistem ini mengintegrasikan LLM dengan hardware IoT untuk menciptakan ekosistem rumah pintar yang responsif. Menggunakan **STB Android (Rooted)** sebagai Brain Server yang menjembatani komunikasi antara pengguna, AI, dan sensor fisik.

### 🧩 Perangkat IoT
* **🎤 ESP32-S3 (XiaoZhi AI Voice Node):** Menangani input/output suara dan berperan sebagai MCP client untuk interaksi AI real-time dengan latensi rendah.
* **🏠 ESP32-C3 (Smart Home Sensor Node):** Memantau lingkungan melalui sensor `AHT20` & `BMP280` serta mengontrol perangkat via Relay.
* **🧠 STB Android (AI Brain Server):** Menggunakan ZTE ZXV10 B866F. Memproses bahasa natural via Groq LLM dan mengelola gateway Telegram Bot.

### ✨ Fitur Utama
* **Sistem AI:** Percakapan AI yang natural, asisten suara real-time, dan eksekusi tool MCP secara langsung.
* **Smart Home:** Kontrol lampu jarak jauh, penjadwalan otomatis, dan integrasi Telegram.
* **Monitoring:** Pelacakan langsung suhu, kelembapan, dan tekanan udara.

### 📱 Perintah Telegram
| Perintah | Fungsi |
| :--- | :--- |
| `sensor rumah` | Mengambil data sensor terbaru |
| `lampu nyala` | Menyalakan lampu |
| `lampu mati` | Mematikan lampu |
| `cuaca` | Info cuaca real-time |
| `berita` | Berita terkini |
| `jam` | Waktu sistem saat ini |

---

## 🌐 Dashboard & Integration
| Module | URL / Resource |
| :--- | :--- |
| **ESP32 Sensor** | `http://192.168.1.222` |
| **STB AI Panel** | `http://[IP_STB]:8088` |
| **Groq AI** | [console.groq.com](https://console.groq.com) |
| **OpenWeather** | [openweathermap.org](https://openweathermap.org/api) |
| **Firmware** | [github.com/78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) |

---

## ⚠️ System Notes
1.  **Security:** Do not expose API keys to public repositories.
2.  **Networking:** All devices must be on the same WiFi network.
3.  **Root Access:** Android STB must be rooted for full access.
4.  **Stability:** Use watchdog timers to prevent system hangs.

---

## 👨‍💻 Author
**patrisius1207**

---

## ⭐ Support Project
* ⭐ **Star** this repository
* 🍴 **Fork** & improve the code
* 🚀 **Share** with the IoT community
