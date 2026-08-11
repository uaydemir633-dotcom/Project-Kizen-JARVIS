# 🤖 Project Kizen JARVIS (v2.0)

![Python](https://img.shields.io/badge/Python-100%25-3776AB.svg?style=flat&logo=python&logoColor=white)
![Version](https://img.shields.io/badge/version-2.0-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Architecture](https://img.shields.io/badge/Architecture-Modular%20Sockets-blue.svg)

> **"A modular AI ecosystem. Building the future step by step, version by version."**

Project Kizen JARVIS is an advanced artificial intelligence assistant infrastructure running on Windows/Linux that enables concurrent and independent inter-module communication using local TCP/IP socket networking (socket/threading)[cite: 3, 5, 8].

---

## 🏗️ Architecture & Module Structure

JARVIS v2.0 transitions to a microservice-like structure where each module operates completely independently[cite: 3, 5, 8]:

* 🧠 **Core Engine:** Coordinates data flow and inter-module messaging on a local server (Ports 5050/6060)[cite: 3, 5, 8].
* 💬 **AI Engine (Groq / Gemini / LLaMA):** Processes inputs from the core, queries system parameters, and generates natural language responses.
* 🎙️ **Voice Module (SpeechRecognition & gTTS):** Listens for the "Jarvis" wake word, converts speech to text, sends data to the Core, and vocalizes output using gTTS/Pygame[cite: 6, 8].
* 📊 **Status Monitor (Port 5053):** Real-time dashboard tracking the operational status and connectivity health of all services (CORE, VISION, VOICE, AI, CONTROL)[cite: 3].
* 🎆 **Ghost Boot Animation:** Terminal-based dynamic Matrix/Ghost boot animation that initializes core services[cite: 9].

---

## 📋 Key Features

* **Modular Socket Communication:** Services operate independently, communicating seamlessly over local TCP/IP sockets[cite: 3, 5, 8].
* **Advanced LLM Integration:** Built-in support for Groq (LLaMA 3.3 70B Versatile) and Google Gemini API[cite: 4, 8].
* **Local System Diagnostics:** Real-time CPU usage, RAM stats, and integrated internet speed testing (Speedtest)[cite: 4, 8].
* **Enhanced Microphone Selector:** In-app selection between system default microphones and Bluetooth headsets (e.g., Galaxy Buds FE)[cite: 6].
* **Dynamic CLI & Animation:** Interactive startup interface featuring custom ASCII art and color-coded status logs[cite: 4, 5, 9].

---

## ⚙️ Installation & Usage

### 1. Clone the Repository
```bash
git clone [https://github.com/uaydemir633-dotcom/Proje-Kizen-JARVIS.git](https://github.com/uaydemir633-dotcom/Proje-Kizen-JARVIS.git)
cd Proje-Kizen-JARVIS
