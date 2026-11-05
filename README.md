# 🏛️ Project Kizen JARVIS (OG)

![Status](https://img.shields.io/badge/status-ARCHIVED-lightgrey.svg)
![Version](https://img.shields.io/badge/version-2.0--OG-orange.svg)
![Python](https://img.shields.io/badge/Python-100%25-3776AB.svg?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> **"A modular AI ecosystem. Building the future, version by version."**

---

## ⚠️ ARCHIVED — Original JARVIS

This is the **original Kizen JARVIS** — the first attempt at a modular
AI assistant. It pioneered the socket-based multi-module architecture
that would later inform the entire Kizen ecosystem.

**Status:** Archived on 2026-11-05.
**Replaced by:** [Project-Kizen-Client](https://github.com/uaydemir633-dotcom/Project-Kizen-Client)
— a modern desktop AI client built with CustomTkinter.

---

## 📖 History

JARVIS was conceived as a **microservice-like AI assistant** running on
Windows/Linux, where each module (CORE, AI, VOICE, MONITOR) operated
independently and communicated over local TCP/IP sockets.
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ JARVIS_AI │────▶│ JARVIS_CORE │◀────│ JARVIS_Voice │
│ (port 5050) │ │ (port 5050) │ │ (port 5050) │
└──────────────┘ └──────────────┘ └──────────────┘
▲
│
┌────────┴────────┐
│ Status Monitor │
│ (port 5053) │
└─────────────────┘

### What Worked
- ✅ Modular socket architecture concept
- ✅ Ghost boot animation (terminal)
- ✅ Groq/Gemini LLM integration
- ✅ System diagnostics (CPU, RAM, speedtest)
- ✅ Wake-word detection ("Jarvis")

### What Didn't (Why We Archived It)
- ❌ Port conflicts (5050 vs 6060 between `JARVIS_AI` and `JARVIS_2`)
- ❌ Two duplicate AI files (`JARVIS_AI.py` and `JARVIS_2.py`)
- ❌ Status Monitor never showed real status (missing core heartbeat)
- ❌ `speech_recognition` + `gTTS` fragile on Windows
- ❌ Polling every 500ms inefficient (socket open/close loop)

These lessons shaped every decision in the Kizen-Client rewrite.

---

## 🗂️ File Manifest

| File | Purpose | Status |
|------|---------|--------|
| `JARVIS_CORE.py` | Central message broker (port 5050) | Legacy |
| `JARVIS_AI.py` | AI engine + TTS (connects to 5050) | Legacy |
| `JARVIS_Voice.py` | Speech recognition + wake word | Legacy |
| `JARVIS Status Monitor.py` | Dashboard (port 5053) | Broken |
| `JARVIS_2.py` | All-in-one rewrite (port 6060) | Legacy |
| `JARVIS_2_0_OPTIMIZED.py` | Ghost boot animation | Legacy |

**Note:** These files are preserved as-is for historical reference.
They are not maintained, not tested, and may not run on modern systems.

---

## 🧩 Architecture Notes

JARVIS used a **message-broker pattern** where:

- **CORE** held shared state (`shared_data` string) and relayed messages
- **AI** polled CORE every 500ms for new prompts
- **VOICE** sent recognized speech to CORE as `VOICE:<text>`
- **MONITOR** tried to read status from a port that was never opened

The two AI files (`JARVIS_AI.py` and `JARVIS_2.py`) represent two
competing designs:
- `JARVIS_AI.py` → talks to an external `JARVIS_CORE.py` (port 5050)
- `JARVIS_2.py` → self-contained, runs its own core (port 6060)

Neither design was completed to production quality.

---

## 🎬 Ghost Boot Animation

`JARVIS_2_0_OPTIMIZED.py` contained a 15-second terminal Matrix/Ghost
animation that:
- Auto-detected terminal size
- Rendered ASCII "JARVIS" with a materialization effect
- Exploded into a white ring at t=12s
- Then `subprocess.Popen`-ed `JARVIS_2.py` and exited

This was the most polished part of the project and survives as a
standalone demo.

---

## 🔗 Kizen Ecosystem (Active Projects)

- [Project-Kizen-Client](https://github.com/uaydemir633-dotcom/Project-Kizen-Client) — AI desktop client
- [Project-Kizen-Optimizer](https://github.com/uaydemir633-dotcom/Project-Kizen-Optimizer) — Windows maintenance
- [Kizen-Auto-Updater](https://github.com/uaydemir633-dotcom/Kizen-Auto-Updater) — Update engine
- [Project-Kizen-Command-Center](https://github.com/uaydemir633-dotcom/Project-Kizen-Command-Center) — Web dashboard
- [Project-Kizen-Notes](https://github.com/uaydemir633-dotcom/Project-Kizen-Notes) — Local notes app

---

## 🚫 Why It's Archived

JARVIS taught us three hard lessons:

1. **Duplicate code kills projects.** Two AI files doing the same thing
   meant neither got polished.
2. **Port discipline matters.** Two core designs (5050 vs 6060) meant
   modules couldn't find each other.
3. **Voice is fragile.** `speech_recognition` + `gTTS` + Windows
   microphone APIs = endless debugging.

The Kizen-Client was born directly from these failures.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Respect the history. JARVIS was Kizen's first step. 🚀*
*— 2026-11-05*
