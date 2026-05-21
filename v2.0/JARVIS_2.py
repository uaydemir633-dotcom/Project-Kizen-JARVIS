import socket, threading, time, io, datetime, os, sys
import psutil, speech_recognition as sr
from groq import Groq
from gtts import gTTS
import pygame
from colorama import Fore, init

init(autoreset=True)

# ─── AYARLAR ───────────────────────────────────────────────
API_KEY    = "HERE_YOUR_API_KEY"
CORE_ADDR  = ('127.0.0.1', 6060)
WAKE_WORD  = "jarvis"

pygame.mixer.init()
shared_data = ""
shared_lock = threading.Lock()

# ─── CORE SUNUCU ───────────────────────────────────────────
def handle_client(client_socket):
    global shared_data
    try:
        data = client_socket.recv(1024).decode('utf-8').strip()
        if ":" in data:
            mod, content = data.split(":", 1)
            mod = mod.upper()
            if "VOICE" in mod:
                with shared_lock:
                    shared_data = content
                print(f"{Fore.YELLOW}[CORE] Girdi: {content}")
            if "AI" in mod and "GET" in content:
                with shared_lock:
                    msg = shared_data
                    shared_data = ""
                client_socket.sendall(msg.encode('utf-8'))
    except:
        pass
    finally:
        client_socket.close()

def core_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(CORE_ADDR)
    server.listen(5)
    print(f"{Fore.GREEN}[CORE] Sunucu aktif → {CORE_ADDR[1]}")
    while True:
        client, _ = server.accept()
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

# ─── SES TANIMA ────────────────────────────────────────────
def voice_listener():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print(f"{Fore.CYAN}[VOICE] Mikrofon hazır.")
            while True:
                try:
                    audio = r.listen(source, phrase_time_limit=5)
                    text = r.recognize_google(audio, language='tr-TR').lower()
                    if WAKE_WORD in text:
                        msg = text.replace(WAKE_WORD, "").strip()
                        if msg:
                            print(f"{Fore.YELLOW}[VOICE] Algılandı: {msg}")
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                                s.connect(CORE_ADDR)
                                s.sendall(f"VOICE:{msg}".encode('utf-8'))
                except:
                    pass
    except Exception as e:
        print(f"{Fore.RED}[VOICE] Hata: {e}")

# ─── AI & SES ÇIKIŞI ───────────────────────────────────────
def speak(text):
    print(f"{Fore.GREEN}[JARVIS] {text}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(CORE_ADDR)
            s.sendall(f"VOICE:Jarvis Cevabı: {text}".encode('utf-8'))
    except:
        pass
    try:
        tts = gTTS(text=text, lang='tr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(f"{Fore.RED}[VOICE] TTS hatası: {e}")

def get_system_info():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    return f"İşlemci %{cpu}, RAM %{ram} kullanımda."

def ask_jarvis(prompt):
    p = prompt.lower()
    if any(x in p for x in ["saat kaç", "saat kac"]):
        return f"Şu an saat {datetime.datetime.now().strftime('%H:%M')}."
    if any(x in p for x in ["cpu", "işlemci", "ram", "bellek"]):
        return get_system_info()
    try:
        client = Groq(api_key=API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Sen Jarvis'sin. 2026 yılındasın. Asistanın. Kısa ve öz cevap ver."},
                {"role": "user", "content": prompt}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Hata: {str(e)[:50]}"

def ai_loop():
    last_msg = ""
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(CORE_ADDR)
                s.sendall(b"AI:GET_MSG")
                msg = s.recv(1024).decode('utf-8').strip()
                if msg and msg != last_msg and not msg.startswith("Jarvis Cevabı:"):
                    cevap = ask_jarvis(msg)
                    if cevap:
                        speak(cevap)
                        last_msg = msg
        except:
            pass
        time.sleep(0.5)

# ─── ANA PROGRAM ───────────────────────────────────────────
if __name__ == "__main__":
    os.system('chcp 65001 > nul' if os.name == 'nt' else '')
    threading.Thread(target=core_server,   daemon=True).start()
    time.sleep(0.5)
    threading.Thread(target=voice_listener, daemon=True).start()
    threading.Thread(target=ai_loop,        daemon=True).start()
    speak("Sistemler çevrimiçi. Dinliyorum.")
    while True:
        try:
            txt = input(f"{Fore.BLUE}Kullanıcı > {Fore.WHITE}")
            if txt.strip():
                cevap = ask_jarvis(txt)
                if cevap:
                    speak(cevap)
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[JARVIS] Kapatılıyor.")
            break