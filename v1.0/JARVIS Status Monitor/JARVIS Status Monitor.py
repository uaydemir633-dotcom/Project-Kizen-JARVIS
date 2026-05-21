# JARVIS Status Monitor.py
import time
import threading
import socket

# Portlar - FARKLI PORT KULLAN
CORE_HEARTBEAT_PORT = 5050    # Core'un heartbeat portu
CORE_STATUS_PORT = 5051       # Core'un status portu  
MONITOR_PORT = 5053           # MONITOR için FARKLI PORT (5052 yerine 5053)

# Modül durumları
module_status = {
    "CORE": {"status": "OFFLINE", "last_update": 0},
    "VISION": {"status": "OFFLINE", "last_update": 0},
    "VOICE": {"status": "OFFLINE", "last_update": 0},
    "AI": {"status": "OFFLINE", "last_update": 0},
    "CONTROL": {"status": "OFFLINE", "last_update": 0}
}

def get_core_status():
    """Core'dan status al"""
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect(('127.0.0.1', CORE_STATUS_PORT))
        data = sock.recv(1024).decode()
        sock.close()
        return data
    except:
        return None

def send_heartbeat(mod):
    """Core'a heartbeat gönder"""
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect(('127.0.0.1', CORE_HEARTBEAT_PORT))
        sock.sendall(mod.encode())
        sock.close()
        return True
    except:
        return False

def monitor_server():
    """Status Monitor için server - FARKLI PORT"""
    try:
        sock = socket.socket()
        sock.bind(('127.0.0.1', MONITOR_PORT))
        sock.listen()
        print(f"✅ Monitor server: port {MONITOR_PORT}")
        
        while True:
            conn, _ = sock.accept()
            # Status'u JSON olarak gönder
            status_json = {
                "CORE": module_status["CORE"]["status"],
                "VISION": module_status["VISION"]["status"],
                "VOICE": module_status["VOICE"]["status"],
                "AI": module_status["AI"]["status"],
                "CONTROL": module_status["CONTROL"]["status"],
                "timestamp": time.time()
            }
            import json
            conn.sendall(json.dumps(status_json).encode())
            conn.close()
    except Exception as e:
        print(f"❌ Monitor server hatası: {e}")

def update_status():
    """Core'dan status güncelle"""
    while True:
        core_data = get_core_status()
        if core_data:
            parts = core_data.split("|")
            for part in parts:
                if ":" in part:
                    mod, state = part.split(":", 1)
                    if mod in module_status:
                        if mod == "VISION":
                            # Vision kodu varsa ONLINE
                            if "S1_" in state or "S0_" in state:
                                module_status[mod]["status"] = "ONLINE"
                                module_status[mod]["last_update"] = time.time()
                            else:
                                module_status[mod]["status"] = "OFFLINE"
                        else:
                            module_status[mod]["status"] = state
                            module_status[mod]["last_update"] = time.time()
        
        # Monitor'den de heartbeat gönder
        send_heartbeat("MONITOR")
        
        time.sleep(0.5)

def show_two_lines():
    """2 satır göster"""
    print("\033[2A", end="")
    print("JARVIS Status Monitor" + " " * 60)
    
    line = "STATUS:"
    for mod in ["CORE", "VISION", "VOICE", "AI", "CONTROL"]:
        state = module_status[mod]["status"]
        line += f" {mod}:{state}"
    
    print(line + " " * 40)

def main():
    print("\n\n")
    
    # Server'ı başlat
    threading.Thread(target=monitor_server, daemon=True).start()
    time.sleep(0.1)
    threading.Thread(target=update_status, daemon=True).start()
    
    # Core'a bağlanmayı dene
    print("🔌 Core'a bağlanılıyor...")
    
    time.sleep(1)  # Bağlantı için bekle
    
    # İlk gösterim
    last_status = {mod: module_status[mod]["status"] for mod in module_status}
    show_two_lines()
    
    while True:
        current_status = {mod: module_status[mod]["status"] for mod in module_status}
        
        if current_status != last_status:
            show_two_lines()
            last_status = current_status.copy()
        
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDurduruldu")