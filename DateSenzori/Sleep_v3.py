from gpiozero import DigitalInputDevice
import threading
import adafruit_dht
import board
import time

from monitor_lumina import MonitorLumina
from monitor_temperatura_umiditate import MonitorTemperaturaUmiditate
from monitor_miscare_radar import MonitorMiscareRadar
from monitor_vibratii import MonitorVibratii
from monitor_sunet import MonitorSunet


#definirea moulelor cu senzori
modul_microfon = DigitalInputDevice(23)
modul_miscare    = DigitalInputDevice(24)
modul_miscare_ir = DigitalInputDevice(25)
modul_vibratii = DigitalInputDevice(12)
modul_lumina = DigitalInputDevice(27)
modul_temperatura_umiditate = adafruit_dht.DHT22(board.D4)
       
        
def citeste_miscare_pir():
        print("Se asteapta miscare PIR.")
        modul_miscare_ir.wait_for_active()
        print("PIR a detectat miscare!")
        modul_miscare_ir_activat = 1
              

def inchide_module():
        print("Iesire din program")
        modul_microfon.close()
        modul_miscare_ir.close()
        modul_vibratii.close()
        modul_lumina.close()
        modul_temperatura_umiditate.exit()

#definirea variabielor stare si grade
stare_temp = threading.Event()
stare_lumina = threading.Event()
stare_sunet = threading.Event()
stare_sunet = threading.Event()

grad_vibratie = 0
grad_miscare = 0

#instantiera claselor
monitor_lumina = MonitorLumina(stare_lumina, modul_lumina)
monitor_miscare_radar = MonitorMiscareRadar(grad_miscare, modul_miscare)
monitor_sunet = MonitorSunet(stare_sunet, modul_microfon)
monitor_temp = MonitorTemperaturaUmiditate(stare_temp, modul_temperatura_umiditate)
monitor_vibratii = MonitorVibratii(grad_vibratie, modul_vibratii)

#pornirea firelor de executie
start = time.perf_counter()

# thread_lumina = threading.Thread(target=monitor_lumina.monitorizeaza_lumina)
# thread_lumina.start()

# thread_miscare = threading.Thread(target=monitor_miscare_radar.monitorizeaza_miscare)
# thread_miscare.start()


# #setarea starilor
# time.sleep(30)
# stare_temp.set()
# stare_lumina.set()

# #asteptare finalizare fire de executie
# thread_dht.join()
# # thread_lux.join()

# print(f'Medie temperatura finala {medie_temp_final}, medie umiditate finala {medie_umid_final}')
# print (f'Timp lumina {secunde_luminozitate}.')

finish = time.perf_counter()
print(f'Terminat in {round(finish-start,4)} secunde.')

inchide_module()
