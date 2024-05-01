from gpiozero import DigitalInputDevice, LED, Button
import threading
import adafruit_dht
import board
import time

from monitor_lumina import MonitorLumina
from monitor_temperatura_umiditate import MonitorTemperaturaUmiditate
from monitor_miscare_radar import MonitorMiscareRadar
from monitor_vibratii import MonitorVibratii
from monitor_sunet import MonitorSunet

import utilitare as ut

#constane
TIMP_VIBRATII_INCEPUT = 300 #in medie, un om se pune in pat cam in 5 minute

#definirea moulelor cu senzori
led = LED(13)
buton = Button(26)
modul_microfon = DigitalInputDevice(23)
modul_miscare    = DigitalInputDevice(21)
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
        print("Iesire din program.")
        led.close()
        buton.close()
        modul_microfon.close()
        modul_miscare.close()
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


#pornirea programului
start = time.perf_counter()

ut.mod_consum_energie(buton, led)
modul_vibratii.wait_for_active(TIMP_VIBRATII_INCEPUT)

#pornirea firelor de executie
thread_lumina = threading.Thread(target=monitor_lumina.monitorizeaza_lumina)
thread_lumina.start()

thread_miscare_radar = threading.Thread(target=monitor_miscare_radar.monitorizeaza_miscare)
thread_miscare_radar.start()

thread_sunet = threading.Thread(target=monitor_sunet.monitorizeaza_sunet)
thread_sunet.start()

thread_temperatura_umiditate = threading.Thread(target=monitor_temp.monitorizeaza_temperatura_umiditate)
thread_temperatura_umiditate.start()

thread_vibratie = threading.Thread(target=monitor_vibratii.monitorizeaza_vibratie)
thread_vibratie.start()

#setarea starilor
time.sleep(30)
monitor_lumina.stare.set()
monitor_miscare_radar.grad_miscare = 1 #doar pentru test
monitor_sunet.stare.set()
monitor_temp.stare.set()

#asteptare finalizare fire de executie
thread_lumina.join()
thread_miscare_radar.join()
thread_sunet.join()
thread_temperatura_umiditate.join()
thread_vibratie.join()

# print(f'Medie temperatura finala {medie_temp_final}, medie umiditate finala {medie_umid_final}')
# print (f'Timp lumina {secunde_luminozitate}.')

finish = time.perf_counter()
print(f'Terminat in {round(finish-start,4)} secunde.')

inchide_module()
