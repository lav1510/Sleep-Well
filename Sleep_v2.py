from gpiozero import MotionSensor, DigitalInputDevice
from statistics import mean
import threading
import adafruit_dht
import board
import time

#definirea variabilelor
modul_miscare_ir_activat = 0
medie_temp_final = None
medie_umid_final = None

#definirea moulelor cu senzori
modul_microfon = DigitalInputDevice(23)
modul_miscare_ir = MotionSensor(25)
modul_vibratii = DigitalInputDevice(12)
modul_lumina = DigitalInputDevice(27)
modul_temperatura_umiditate = adafruit_dht.DHT22(board.D4)

def arata_timp():
        timp = time.localtime()
        ora = timp.tm_hour
        minute = timp.tm_min
        secunde = timp.tm_sec
        print("Timp {:02d}:{:02d}:{:02d}.".format(ora, minute, secunde))

def citeste_sunet():
        arata_timp()
        print("sunet!")
        
def citeste_miscare_pir():
        print("Se asteapta miscare PIR.")
        modul_miscare_ir.wait_for_active()
        print("PIR a detectat miscare!")
        modul_miscare_ir_activat = 1

def citeste_presiune():
        arata_timp()
        print("presiune!")

def citeste_lumina():
        arata_timp()
        print("lumina!")
        
def citeste_temperatura_umiditate():
       flag_citire = 0
       while not flag_citire:
            try:
                temperatura = modul_temperatura_umiditate.temperature
                umiditate = modul_temperatura_umiditate.humidity
                flag_citire = 1
                return (temperatura, umiditate)
                
            except RuntimeError as error:
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                modul_temperatura_umiditate.exit()
                raise error

            time.sleep(2.0)

def monitorizeaza_temperatura_umiditate(stare):
        print("Monitorizare temperatura si umiditate.")
        
        multime_temp = set()
        multime_umid = set()

        while not stare.is_set():
                (temperatura, umiditate) = citeste_temperatura_umiditate()
                print( "Temperatura: {:.1f} C    Umditate: {}% ".format( temperatura, umiditate))
                
                multime_temp.add(temperatura)
                multime_umid.add(umiditate)
                
                #se asteapta 10 minute = 600 secunde
                time.sleep(6)

        print("S-a finalizat monitorizarea temperaturii si umiditatii.")

        global medie_temp_final
        global medie_umid_final  

        medie_temp_final = mean(multime_temp)
        medie_umid_final = mean(multime_umid)


def inchide_module():
        print("Iesire din program")
        modul_microfon.close()
        modul_miscare_ir.close()
        modul_vibratii.close()
        modul_lumina.close()
        modul_temperatura_umiditate.exit()
        

time.sleep(20)
stare = threading.Event()
start = time.perf_counter()

thread_dht = threading.Thread(target=monitorizeaza_temperatura_umiditate, args=(stare,))
thread_dht.start()
time.sleep(30)
stare.set()
thread_dht.join()
print(f'Medie temperatura finala {medie_temp_final}, medie umiditate finala {medie_umid_final}')

finish = time.perf_counter()
print(f'Terminat in {round(finish-start,4)} secunde.')
inchide_module()
