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

## 🧠 System Architecture
Sistem ini mengintegrasikan kecerdasan buatan (LLM) dengan perangkat keras IoT untuk menciptakan ekosistem rumah pintar yang responsif. Menggunakan **STB Android** sebagai otak pusat (Brain Server) yang menjembatani komunikasi antara pengguna, AI, dan sensor fisik.

---

## 🧩 IoT Devices

### 🎤 ESP32-S3 (XiaoZhi AI Voice Node)
**Voice Assistant • Real-time AI • MCP Client**
* **Voice I/O:** Input dan output suara berkualitas tinggi.
* **AI Integration:** Bertindak sebagai client untuk asisten AI via protokol MCP.
* **Performance:** Eksekusi perintah dengan latensi rendah.
* **Feedback:** Sistem umpan balik audio untuk interaksi yang lebih hidup.

### 🏠 ESP32-C3 (Smart Home Sensor Node)
**Environment Monitoring • Automation Controller**
* **Sensors:** Menggunakan `AHT20` (Suhu & Kelembapan) dan `BMP280` (Tekanan Udara).
* **Control:** Dilengkapi Relay untuk kendali lampu/perangkat listrik.
* **Automation:** Sistem penjadwalan otomatis (scheduling) internal.
* **Connectivity:** Berjalan sebagai REST API server lokal.

### 🧠 STB Android (AI Brain Server)
**Core Intelligence Hub**
* **Hardware:** ZTE ZXV10 B866F (Rooted).
* **Processing:** Pemrosesan bahasa alami menggunakan Groq LLM.
* **Control:** Berfungsi sebagai pusat kendali Telegram Bot dan gateway MCP server.
* **Interface:** Dilengkapi dengan sistem dashboard web.

---

## ✨ Features

* **🤖 AI System:** Chat Bahasa Indonesia yang natural, Voice assistant real-time, dan eksekusi tool MCP secara langsung.
* **🏠 Smart Home:** Kontrol lampu (ON/OFF), penjadwalan otomatis, dan kendali jarak jauh via Telegram.
* **📊 Monitoring:** Pelacakan suhu, kelembapan, tekanan udara, serta status perangkat secara live.

---

## 📱 Telegram Commands

| Command | Function |
| :--- | :--- |
| `sensor rumah` | Mengambil data sensor terbaru |
| `lampu nyala` | Menyalakan lampu |
| `lampu mati` | Mematikan lampu |
| `cuaca` | Informasi cuaca terkini |
| `berita` | Berita terbaru |
| `jam` | Waktu sistem saat ini |

---

## 🌐 Dashboard System

| Module | URL |
| :--- | :--- |
| **ESP32 Sensor** | `http://192.168.1.222` |
| **STB AI Panel** | `http://[IP_STB]:8088` |

---

## 🔗 Ecosystem Integration

* **Groq AI:** [console.groq.com](https://console.groq.com)
* **OpenWeather:** [openweathermap.org](https://openweathermap.org/api)
* **Telegram Bot:** [t.me/BotFather](https://t.me/BotFather)
* **XiaoZhi MCP:** [xiaozhi.me](https://xiaozhi.me)
* **Firmware:** [github.com/78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32)

---

## ⚠️ System Notes

1.  **Security:** Jangan mengekspos API key ke publik (GitHub).
2.  **Networking:** Semua perangkat harus berada dalam satu jaringan WiFi.
3.  **Root Access:** STB Android wajib di-root untuk akses penuh.
4.  **Stability:** Gunakan sistem watchdog untuk menjaga stabilitas perangkat.

---

## 👨‍💻 Author
patrisius1207 


---

## ⭐ Support Project
* ⭐ **Star** repository ini
* 🍴 **Fork** & improve kode
* 🚀 **Share** ke komunitas IoT
