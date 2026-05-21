import socket, speech_recognition as sr, os, sys, threading, time
from colorama import Fore, Style, init

init(autoreset=True)

os.system('chcp 65001 > nul')
sys.stdout.reconfigure(encoding='utf-8')

CORE_ADDR = ('127.0.0.1', 5050)
WAKE_WORD = "jarvis"

class JarvisVoice:
    def get_mics(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.YELLOW}╔{'═'*43}╗")
        print(f"{Fore.YELLOW}║      🎙️  JARVIS SES DENETİM PANELİ         ║")
        print(f"{Fore.YELLOW}╚{'═'*43}╝")
        mics = sr.Microphone.list_microphone_names()
        f_hd, f_buds = None, None
        for i, name in enumerate(mics):
            n = name.lower()
            if "high definition" in n: f_hd = i
            if "buds fe" in n: f_buds = i
        
        print(f"\n  {Fore.CYAN}[1] {Fore.WHITE}SİSTEM MİKROFONU")
        print(f"  {Fore.CYAN}[2] {Fore.WHITE}GALAXY BUDS FE")
        print(f"\n{Fore.YELLOW}{'─'*45}")
        
        secim = input(f"{Fore.GREEN}Seçiminiz (1/2): ")
        return f_buds if secim == "2" and f_buds is not None else (f_hd if f_hd is not None else 1)

    def listen(self, idx):
        r = sr.Recognizer()
        try:
            with sr.Microphone(device_index=idx) as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print(f"\n{Fore.GREEN}● {Fore.WHITE}Dinleniyor... (Jarvis diyerek konuşun)")
                while True:
                    try:
                        audio = r.listen(source, phrase_time_limit=4)
                        text = r.recognize_google(audio, language='tr-TR').lower()
                        if WAKE_WORD in text:
                            print(f"{Fore.YELLOW}➜ Algılandı: {Fore.WHITE}{text}")
                            msg = text.replace(WAKE_WORD, "").strip()
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                                s.connect(CORE_ADDR)
                                s.sendall(f"VOICE:{msg}".encode('utf-8'))
                    except: pass
        except Exception as e: print(f"Hata: {e}")

if __name__ == "__main__":
    jv = JarvisVoice()
    idx = jv.get_mics()
    jv.listen(idx)