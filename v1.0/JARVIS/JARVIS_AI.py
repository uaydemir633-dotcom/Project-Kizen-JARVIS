import socket, threading, time, io, psutil, speedtest, datetime, os
from groq import Groq
from gtts import gTTS
import pygame
from colorama import Fore, Style, init

init(autoreset=True)

API_KEY = "HERE_YOUR_API_KEY"
CORE_ADDR = ('127.0.0.1', 5050)

pygame.mixer.init()

def get_system_info():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    return f"İşlemci %{cpu}, RAM %{ram} kullanımda."

def get_internet_speed():
    try:
        print(f"{Fore.YELLOW}🌐 Hız testi yapılıyor...")
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        return f"İndirme: {download:.1f}, Yükleme: {upload:.1f} Mbps."
    except: return "Hız ölçümü başarısız."

def speak(text):
    try:
        print(f"\n{Fore.GREEN}🤖 JARVIS > {Fore.WHITE}{text}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(CORE_ADDR)
                s.sendall(f"VOICE:Jarvis Cevabı: {text}".encode('utf-8'))
        except: pass
        tts = gTTS(text=text, lang='tr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy(): time.sleep(0.1)
    except Exception as e: print(f"{Fore.RED}Ses hatası: {e}")

def ask_jarvis(prompt):
    p_low = prompt.lower()
    if any(x in p_low for x in ["saat kaç", "saat kac"]):
        return f"Şu an saat {datetime.datetime.now().strftime('%H:%M')}."
    if any(x in p_low for x in ["cpu", "işlemci", "ram", "bellek"]):
        return get_system_info()
    if "internet" in p_low: return get_internet_speed()
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
    except Exception as e: return f"Hata: {str(e)[:30]}"

def core_dinle():
    last_msg = ""
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(CORE_ADDR)
                s.sendall(b"AI:GET_MSG")
                msg = s.recv(1024).decode('utf-8').strip()
                if msg and msg != last_msg:
                    if not msg.startswith("Jarvis Cevabı:"):
                        cevap = ask_jarvis(msg)
                        if cevap:
                            speak(cevap)
                            last_msg = msg
        except: pass
        time.sleep(0.5)

def startup_animation():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{Fore.CYAN}SİSTEM PROTOKOLLERİ BAŞLATILIYOR...")
    print(f"{Fore.MAGENTA}  {'='*46}")
    print(f"  {Fore.WHITE}SİSTEM DURUMU: {Fore.GREEN}Çevrimiçi")
    print(f"{Fore.MAGENTA}  {'='*46}\n")

if __name__ == "__main__":
    startup_animation()
    threading.Thread(target=core_dinle, daemon=True).start()
    speak("Sistemler çevrimiçi. Dinliyorum.")
    while True:
        txt = input(f"{Fore.BLUE}Kullanıcı > {Fore.WHITE}")
        if txt.strip():
            cevap = ask_jarvis(txt)
            if cevap: speak(cevap)