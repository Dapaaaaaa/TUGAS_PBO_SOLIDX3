from abc import ABC, abstractmethod

# SOAL NOMOR 1

# =================================================================
# 1. ANTARMUKA RAKSASA (Melanggar I - Interface Segregation)
# =================================================================
class SmartDevice(ABC):
    pass

class nyalakan(ABC):
    @abstractmethod
    def turn_on(self): pass
    
class matikan(ABC):
    @abstractmethod
    def turn_off(self): pass
    
class musik(ABC):
    @abstractmethod
    def play_music(self): pass
    
class suhu(ABC):
    @abstractmethod
    def set_temperature(self, temp): pass

# SOAL NOMOR 2

# =================================================================
# 2. IMPLEMENTASI KELAS ANAK (Melanggar L - Liskov Substitution)
# =================================================================

class SmartDevice():
    def turn_on(self):
      raise NotImplementedError

    def turn_off(self):
      raise NotImplementedError

    def play_music(self):
      raise NotImplementedError

    def set_temperature(self, temp):
      raise NotImplementedError

class SmartSpeaker(SmartDevice):
    def play_music(self):
        raise NotImplementedError

class Subwoofer(SmartSpeaker):
    def turn_on(self):
        print("Subwoofer menyala.")

    def turn_off(self):
        print("Subwoofer mati.")

    def play_music(self):
        print("Memutar lagu di Subwoofer...")

class SmartAC(SmartDevice):
    def set_temperature(self, temp):
        raise NotImplementedError

class CentralAC(SmartAC):
    def set_temperature(self, temp):
        print(f"Suhu AC diatur ke {temp}°C.")

def mainkan_musik(speaker: SmartSpeaker):
    """Hanya terima BurungTerbang, tidak akan dapat BurungCarah."""
    print(speaker.play_music())


# SOAL NOMOR 3

from abc import ABC, abstractmethod

# =================================================================
# ABSTRAKSI (Dasar untuk OCP & DIP)
# =================================================================
class Device(ABC):
    @abstractmethod
    def turn_on(self): pass

    @abstractmethod
    def turn_off(self): pass

# =================================================================
# S - SINGLE RESPONSIBILITY PRINCIPLE
# =================================================================
class Logger:
    """Satu-satunya alasan kelas ini berubah adalah jika cara log berubah."""
    @staticmethod
    def log(message):
        print(f"[LOG] {message}")

# =================================================================
# O - OPEN/CLOSED PRINCIPLE (Implementasi Perangkat)
# =================================================================
class SmartSpeaker(Device):
    def turn_on(self): print("Speaker ON")
    def turn_off(self): print("Speaker OFF")
    def play_music(self): print("Musik diputar...")

class SmartAC(Device):
    def turn_on(self): print("AC ON")
    def turn_off(self): print("AC OFF")
    def set_temp(self, t): print(f"Suhu diatur ke {t}C")

# =================================================================
# D - DEPENDENCY INVERSION PRINCIPLE (Controller)
# =================================================================
class SmartHomeController:
    def __init__(self, devices: list[Device], logger: Logger):
        # DIP: Bergantung pada list[Device] (abstraksi), bukan kelas konkret.
        # Dependency Injection: Logger dan Devices dimasukkan dari luar.
        self.devices = devices
        self.logger = logger

    def run(self, device_index, action, *args):
        device = self.devices[device_index]
        self.logger.log(f"Perintah: {action}")

        # OCP: Menggunakan getattr agar tidak perlu if-elif (Closed for modification)
        if hasattr(device, action):
            func = getattr(device, action)
            func(*args)
        else:
            self.logger.log(f"Gagal: {action} tidak ditemukan.")

# =================================================================
# PENGGUNAAN
# =================================================================

# 1. Siapkan komponen (Dependency)
logs = Logger()
my_devices = [SmartSpeaker(), SmartAC()]

# 2. Masukkan komponen ke Controller (DIP)
app = SmartHomeController(my_devices, logs)

# 3. Eksekusi (OCP & SRP bekerja di balik layar)
app.run(0, "play_music")  # Menjalankan fungsi speaker
app.run(1, "set_temp", 20) # Menjalankan fungsi AC