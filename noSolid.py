from abc import ABC, abstractmethod

# =================================================================
# 1. ANTARMUKA RAKSASA (Melanggar I - Interface Segregation)
# =================================================================
class SmartDevice(ABC):
    """
    Antarmuka (kontrak) yang memaksa SEMUA perangkat pintar
    memiliki fungsi-fungsi di bawah ini.
    """
    @abstractmethod
    def turn_on(self): pass
    
    @abstractmethod
    def turn_off(self): pass
    
    @abstractmethod
    def play_music(self): pass
    
    @abstractmethod
    def set_temperature(self, temp): pass


# =================================================================
# 2. IMPLEMENTASI KELAS ANAK (Melanggar L - Liskov Substitution)
# =================================================================
class SmartSpeaker(SmartDevice):
    def turn_on(self):
        print("Speaker menyala.")
        
    def turn_off(self):
        print("Speaker mati.")
        
    def play_music(self):
        print("Memutar lagu di Spotify...")
        
    def set_temperature(self, temp):
        # ERROR: Speaker tidak bisa mendinginkan ruangan!
        raise Exception("Error: Speaker tidak punya fitur pengatur suhu!")


class SmartAC(SmartDevice):
    def turn_on(self):
        print("AC menyala.")
        
    def turn_off(self):
        print("AC mati.")
        
    def play_music(self):
        # ERROR: AC tidak punya speaker untuk memutar lagu!
        raise Exception("Error: AC tidak bisa memutar musik!")
        
    def set_temperature(self, temp):
        print(f"Suhu AC diatur ke {temp}°C.")


# =================================================================
# 3. KONTROLER UTAMA (Melanggar S, O, dan D)
# =================================================================
class SmartHomeController:
    def __init__(self):
        # Melanggar D: Bergantung langsung pada kelas konkret (hardcoded)
        self.speaker = SmartSpeaker()
        self.ac = SmartAC()
        
    # Melanggar S: Fungsi ini mengurus logika kontrol DITAMBAH logging manual
    # Melanggar O: Kalau besok beli SmartTV, harus tambah if-elif lagi
    def control_device(self, device_type, action, value=None):
        print(f"[LOG SERVER] Memulai perintah: '{action}' pada '{device_type}'")
        
        if device_type == "speaker":
            if action == "on":
                self.speaker.turn_on()
            elif action == "off":
                self.speaker.turn_off()
            elif action == "music":
                self.speaker.play_music()
        elif device_type == "ac":
            if action == "on":
                self.ac.turn_on()
            elif action == "off":
                self.ac.turn_off()
            elif action == "temp":
                self.ac.set_temperature(value)
        else:
            print("Perangkat tidak dikenali.")

        print(f"[LOG SERVER] Perintah selesai.\n")

# --- CARA MENGGUNAKANNYA ---
controller = SmartHomeController()

# Berjalan lancar
controller.control_device("speaker", "music")
controller.control_device("ac", "temp", 18)

# Bencana terjadi di sini (Liskov Violation)
try:
    print("Mencoba mengatur suhu lewat speaker:")
    controller.speaker.set_temperature(20) 
except Exception as e:
    print(e)