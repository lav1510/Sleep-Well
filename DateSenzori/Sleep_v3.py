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
from monitor_miscare_ir import MonitorMiscareIR
from status_somn import StatusSomn

import utilitare as ut

#constane
TIMP_PIR = 300
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
monitor_miscare_ir = MonitorMiscareIR(modul_miscare_ir)
status_somn = StatusSomn()

##################################################################################################################

#pornirea programului
start = time.perf_counter()

for _ in range(2):
        #starea treaz in afara patului
        ut.mod_consum_energie(buton, led)
        modul_vibratii.wait_for_active(TIMP_VIBRATII_INCEPUT)

        #starea treaz in pat
        stare_actuala = 1 #stare initiala : treaz in pat


        #definirea firelor de executie
        thread_lumina = threading.Thread(target=monitor_lumina.monitorizeaza_lumina)
        thread_sunet = threading.Thread(target=monitor_sunet.monitorizeaza_sunet)
        thread_temperatura_umiditate = threading.Thread(target=monitor_temp.monitorizeaza_temperatura_umiditate)

        thread_pir = threading.Thread(target=monitor_miscare_ir.monitorizeaza_miscare_ir)
        thread_miscare_radar = threading.Thread(target=monitor_miscare_radar.monitorizeaza_miscare)
        thread_vibratie = threading.Thread(target=monitor_vibratii.monitorizeaza_vibratie)


        #pornirea firelor de executie 
        thread_lumina.start()
        thread_sunet.start()
        thread_temperatura_umiditate.start()
        thread_miscare_radar.start()
        thread_vibratie.start()
        thread_pir.start()


        #cat timp persoana nu este treaza in afara patului( starea 0 )
        flagtest=1
        while flagtest != 0 :

                stare_actuala = status_somn.testeaza_starea(stare_anterioara = stare_actuala, miscare_pir = monitor_miscare_ir.modul_miscare_ir_activat, grad_miscare = monitor_miscare_radar.grad_miscare, grad_vibratii = monitor_vibratii.grad_vibratie)
                print(stare_actuala)

                #sansa sa se intoarca in pat in 5 min
                if stare_actuala == 0:
                        monitor_miscare_ir.modul_miscare_ir.wait_for_active(TIMP_PIR)
                        if monitor_miscare_ir.modul_miscare_ir.value :
                                stare_actuala = 1

                flagtest = 0
        else:
                #odihna s-a terminat
                #setarea starilor
                monitor_lumina.stare.set()
                monitor_sunet.stare.set()
                monitor_temp.stare.set()

                #asteptare finalizare fire de executie cu fortarea terminarii dupa 5 secunde
                thread_lumina.join(5)
                thread_sunet.join(5)
                thread_temperatura_umiditate.join(5)
                thread_vibratie.join(5)
                thread_miscare_radar.join(5)
                thread_pir.join(5)

                #inserarea datelor in baza de date
                ore_lumina = monitor_lumina.secunde_luminozitate // 3600
                ore_sunet = monitor_sunet.secunde_zgomot // 3600
                ut.insereaza_baza_date(umiditate_medie = monitor_temp.medie_umid_final, temp_medie = monitor_temp.medie_temp_final,  ore_somn_profund = status_somn.ore_somn_adanc, ore_somn_usor = status_somn.ore_somn_usor, lumina = ore_lumina, sunet = ore_sunet, ora_trezire = status_somn.ora_trezire, ora_culcare = status_somn.ora_culcare)

                #resetarea starilor claselor
                monitor_lumina.stare.clear()
                monitor_sunet.stare.clear()
                monitor_temp.stare.clear()

                #reset
                monitor_lumina.secunde_luminozitate = 0
                monitor_sunet.secunde_zgomot = 0
                monitor_miscare_ir.modul_miscare_ir_activat = 0
                monitor_vibratii.grad_vibratie = 0
                monitor_miscare_radar.grad_miscare = 0

#try, catch aici
finish = time.perf_counter()
print(f'Terminat in {round(finish-start,4)} secunde.')

inchide_module()
