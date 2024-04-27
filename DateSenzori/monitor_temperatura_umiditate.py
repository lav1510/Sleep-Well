import threading
import adafruit_dht
from statistics import mean
import board
import time

class MonitorTemperaturaUmiditate():
    def __init__(self, stare: threading.Event,  modul_temperatura_umiditate: adafruit_dht.DHT22):
        if not isinstance(stare, threading.Event):
            raise TypeError("Parametrul 'stare' trebuie sa fie obiect de tipul threading.Event!")

        if not isinstance(modul_temperatura_umiditate, adafruit_dht.DHT22):
            raise TypeError("Parametrul 'modul_temperatura_umiditate' trebuie sa fie obiect de tipul DigitalInputDevice!")

        self.modul_temperatura_umiditate = modul_temperatura_umiditate
        self.stare = stare
        self.medie_temp_final = 0
        self.medie_umid_final = 0


    def citeste_temperatura_umiditate(self):
       flag_citire = 0
       while not flag_citire:
            try:
                temperatura = self.modul_temperatura_umiditate.temperature
                umiditate = self.modul_temperatura_umiditate.humidity
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

    def monitorizeaza_temperatura_umiditate(self):
        print("Monitorizare temperatura si umiditate.")
        
        multime_temp = set()
        multime_umid = set()

        while not self.stare.is_set():
                (temperatura, umiditate) = self.citeste_temperatura_umiditate()
                #print( "Temperatura: {:.1f} C    Umditate: {}% ".format( temperatura, umiditate))
                
                multime_temp.add(temperatura)
                multime_umid.add(umiditate)
                
                #se asteapta 10 minute = 600 secunde
                time.sleep(6)

        print("S-a finalizat monitorizarea temperaturii si umiditatii.")

        self.medie_temp_final = mean(multime_temp)
        self.medie_umid_final = mean(multime_umid)

if __name__ == "__main__":
    start = time.perf_counter()
    modul_temperatura_umiditate = adafruit_dht.DHT22(board.D4)
    stare_temp = threading.Event()
    monitor_temp = MonitorTemperaturaUmiditate(stare_temp, modul_temperatura_umiditate)

    thread_dht = threading.Thread(target=monitor_temp.monitorizeaza_temperatura_umiditate)
    thread_dht.start()
    time.sleep(10)
    monitor_temp.stare.set()
    thread_dht.join()

    print("Iesire din program")
    modul_temperatura_umiditate.exit()
    finish = time.perf_counter()
    print(f'Terminat in {round(finish-start,4)} secunde.')
    print(f'Medie temperatura finala {monitor_temp.medie_temp_final}, medie umiditate finala {monitor_temp.medie_umid_final}')
