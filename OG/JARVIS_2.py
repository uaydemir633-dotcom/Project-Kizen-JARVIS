"""
JARVIS OG — Crash-Proof Edition (English)
Opens even without audio/microphone.
"""
import socket, threading, time, io, datetime, os, sys
import psutil
from groq import Groq
from gtts import gTTS
from colorama import Fore, Style, init

init(autoreset=True)

# ─── OPTIONAL: pygame (audio) ─────────────────────────────
try:
    import pygame
    pygame.mixer.init()
    AUDIO_OK = True
except Exception:
    AUDIO_OK = False
    print(f"{Fore.YELLOW}[WARN] No audio — silent mode{Style.RESET_ALL}")

# ─── OPTIONAL: microphone ─────────────────────────────────
try:
    import speech_recognition as sr
    MIC_OK = True
except Exception:
    MIC_OK = False
    print(f"{Fore.YELLOW}[WARN] No microphone — voice commands disabled{Style.RESET_ALL}")

# ─── SETTINGS ─────────────────────────────────────────────
API_KEY   = "HERE_YOUR_GROQ_API_KEY"
CORE_ADDR = ('127.0.0.1', 6060)
WAKE_WORD = "jarvis"

shared_data = ""
shared_lock = threading.Lock()

# ─── CORE SERVER ──────────────────────────────────────────
def handle_client(client_socket):
    global shared_data
    try:
        data = client_socket.recv(1024).decode('utf-8').strip()
        if ":" in data:
            mod, content = data.split(":", 1)
            if "VOICE" in mod.upper():
                with shared_lock:
                    shared_data = content
                print(f"{Fore.YELLOW}[CORE] Input: {content}{Style.RESET_ALL}")
            if "AI" in mod.upper() and "GET" in content:
                with shared_lock:
                    msg = shared_data
                    shared_data = ""
                client_socket.sendall(msg.encode('utf-8'))
    except:
        pass
    finally:
        client_socket.close()

def core_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(CORE_ADDR)
        server.listen(5)
        print(f"{Fore.GREEN}[CORE] Server active → {CORE_ADDR[1]}{Style.RESET_ALL}")
        while True:
            client, _ = server.accept()
            threading.Thread(target=handle_client, args=(client,), daemon=True).start()
    except Exception as e:
        print(f"{Fore.RED}[CORE] Error: {e}{Style.RESET_ALL}")

# ─── VOICE RECOGNITION (optional) ─────────────────────────
def voice_listener():
    if not MIC_OK:
        return
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print(f"{Fore.CYAN}[VOICE] Microphone ready.{Style.RESET_ALL}")
            while True:
                try:
                    audio = r.listen(source, phrase_time_limit=5)
                    text = r.recognize_google(audio, language='en-US').lower()
                    if WAKE_WORD in text:
                        msg = text.replace(WAKE_WORD, "").strip()
                        if msg:
                            print(f"{Fore.YELLOW}[VOICE] {msg}{Style.RESET_ALL}")
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                                s.connect(CORE_ADDR)
                                s.sendall(f"VOICE:{msg}".encode('utf-8'))
                except:
                    pass
    except Exception as e:
        print(f"{Fore.RED}[VOICE] {e}{Style.RESET_ALL}")

# ─── VOICE OUTPUT (optional) ──────────────────────────────
def speak(text):
    print(f"{Fore.GREEN}[JARVIS] {text}{Style.RESET_ALL}")
    if not AUDIO_OK:
        return
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(f"{Fore.RED}[VOICE] TTS: {e}{Style.RESET_ALL}")

def get_system_info():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    return f"CPU {cpu}%, RAM {ram}%."

def ask_jarvis(prompt):
    p = prompt.lower()
    if any(x in p for x in ["what time", "time is it"]):
        return f"It's {datetime.datetime.now().strftime('%H:%M')}."
    if any(x in p for x in ["cpu", "processor", "ram", "memory"]):
        return get_system_info()
    if API_KEY.startswith("HERE_"):
        return "API key not set. Edit API_KEY in JARVIS_2.py."
    try:
        client = Groq(api_key=API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Jarvis. Answer briefly and clearly."},
                {"role": "user", "content": prompt}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)[:80]}"

def ai_loop():
    last_msg = ""
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(CORE_ADDR)
                s.sendall(b"AI:GET_MSG")
                msg = s.recv(1024).decode('utf-8').strip()
                if msg and msg != last_msg and not msg.startswith("Jarvis"):
                    cevap = ask_jarvis(msg)
                    if cevap:
                        speak(cevap)
                        last_msg = msg
        except:
            pass
        time.sleep(0.5)

# ─── MAIN ─────────────────────────────────────────────────
if __name__ == "__main__":
    os.system('chcp 65001 > nul' if os.name == 'nt' else '')
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}")
    print("   ██████╗  ██████╗ ")
    print("  ██╔═══██╗██╔════╝ ")
    print("  ██║   ██║██║  ███╗")
    print("  ██║   ██║██║   ██║")
    print("  ╚██████╔╝╚██████╔╝")
    print("   ╚═════╝  ╚═════╝ ")
    print(f"{Style.RESET_ALL}{Fore.CYAN}  ─── OG EDITION ───{Style.RESET_ALL}")
    print(f"  Audio: {'✅' if AUDIO_OK else '⚠️  silent'}  |  Mic: {'✅' if MIC_OK else '⚠️  none'}\n")

    threading.Thread(target=core_server,   daemon=True).start()
    time.sleep(0.5)
    threading.Thread(target=voice_listener, daemon=True).start()
    threading.Thread(target=ai_loop,        daemon=True).start()

    speak("Systems online.")

    while True:
        try:
            txt = input(f"{Fore.BLUE}User > {Fore.WHITE}")
            if txt.strip():
                cevap = ask_jarvis(txt)
                if cevap:
                    speak(cevap)
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[JARVIS] Shutting down.{Style.RESET_ALL}")
            break
        except EOFError:
            break