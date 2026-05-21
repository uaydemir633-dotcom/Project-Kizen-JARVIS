import socket, threading, datetime
from colorama import Fore, Style, init

init(autoreset=True)

CORE_IP = '127.0.0.1'
CORE_PORT = 5050 

class JarvisCore:
    def log(self, module, message, color=Fore.CYAN):
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.WHITE}[{time_str}] {color}[{module}] {Style.BRIGHT}{message}")

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024).decode('utf-8').strip()
            if ":" in data:
                mod, content = data.split(":", 1)
                if "VOICE" in mod.upper():
                    self.shared_data = content
                    self.log("VOICE", f"Girdi alındı: {content}", Fore.YELLOW)
                if "AI" in mod.upper() and "GET" in content:
                    if self.shared_data:
                        client_socket.sendall(self.shared_data.encode('utf-8'))
                        self.log("CORE", "Veri AI modülüne aktarıldı.", Fore.GREEN)
                        self.shared_data = ""
            client_socket.close()
        except: pass

    def start_server(self):
        self.shared_data = ""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((CORE_IP, CORE_PORT))
        server.listen(5)
        
        print(f"\n{Fore.MAGENTA}{'='*50}")
        print(f"{Fore.MAGENTA}   🚀 JARVIS MERKEZİ ÇEKİRDEK (CORE) AKTİF")
        print(f"{Fore.MAGENTA}{'='*50}\n")
        
        while True:
            client, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

if __name__ == "__main__":
    JarvisCore().start_server()