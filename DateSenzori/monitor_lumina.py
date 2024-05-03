from gpiozero import DigitalInputDevice
import time
import threading

class MonitorLumina():
    def __init__(self, stare: threading.Event,  modul_lumina: DigitalInputDevice):
        if not isinstance(stare, threading.Event):
            raise TypeError("Parametrul 'stare' trebuie sa fie obiect de tipul threading.Event!")

        if not isinstance(modul_lumina, DigitalInputDevice):
            raise TypeError("Parametrul 'modul_lumina' trebuie sa fie obiect de tipul DigitalInputDevice!")

        self.modul_lumina = modul_lumina
        self.stare = stare
        self.secunde_luminozitate = 0


    def monitorizeaza_lumina(self):
        print("Monitorizare nivel luminozitate camera.")
        #value = 0 lumina, value = 1 intuneric
        secunde = 0.0
        toggle = 0
        lumina_anterior = 1

        while not self.stare.is_set():        
            if(self.modul_lumina.value and lumina_anterior == 0):
                    secunde += time.perf_counter() - start
                    toggle = 1
                    lumina_anterior = 1
                    print("Intuneric.")
                    continue
                    
            if( (not self.modul_lumina.value) and lumina_anterior == 1):
                    start = time.perf_counter()
                    lumina_anterior = 0      

            #se asteapta 30 secunde
            time.sleep(1)

        if(not toggle):
                secunde += time.perf_counter() - start

        print("S-a finalizat monitorizarea nivelului de luminozitate din camera.")
        
        self.secunde_luminozitate = round(secunde,4)
        print(f'Numar total de secunde lumina {self.secunde_luminozitate }')



if __name__ == "__main__":
    start = time.perf_counter()
    modul_lumina = DigitalInputDevice(27)
    stare_lumina = threading.Event()
    monitor_lumina = MonitorLumina(stare_lumina, modul_lumina)

    thread_lumina = threading.Thread(target=monitor_lumina.monitorizeaza_lumina)
    thread_lumina.start()
    time.sleep(10)
    monitor_lumina.stare.set()
    thread_lumina.join()

    print("Iesire din program")
    modul_lumina.close()
    finish = time.perf_counter()
    print(monitor_lumina.secunde_luminozitate)
    print(f'Terminat in {round(finish-start,4)} secunde.')