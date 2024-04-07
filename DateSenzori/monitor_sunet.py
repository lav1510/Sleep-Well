from gpiozero import DigitalInputDevice
import time
import threading

class MonitorSunet:
    def __init__(self, stare: threading.Event, modul_microfon: DigitalInputDevice):
        if not isinstance(stare, threading.Event):
            raise TypeError("Parametrul 'stare' rebuie sa fie obiect de tipul threading.Event!")

        if not isinstance(modul_microfon, DigitalInputDevice):
            raise TypeError("Parametrul 'modul_microfon' rebuie sa fie obiect de tipul DigitalInputDevice!")

        self.secunde_zgomot = 0.0
        self.stare = stare
        self.modul_microfon = modul_microfon
        #variabila pentru a sti ca s=0 in diagrama stari
        self.fara_zgomot = True


    def monitorizeaza_sunet(self):
        print("Monitorizarea nivelului de zgomot din camera.")
        #value = 1 liniste, value = 0 zgomot
        start = 0.0
        secunde_zgomot = 0.0
        toggle = False
        sunet_anterior = 1

        timpi_intre_zgomote = [None] * 5

        while not self.stare.is_set():        
                if(not modul_microfon.value and sunet_anterior == 1):
                        start = time.perf_counter()
                        sunet_anterior = 0
                        fara_zgomot = 0
                        toggle = 1
                        continue

                if( (modul_microfon.value) and sunet_anterior == 0):        
                        secunde_zgomot += time.perf_counter() - start
                        sunet_anterior = 1
                        print("Liniste dupa zgomot.")
                elif (modul_microfon.value) and start > 600:
                        fara_zgomot = 1
                        
                #se asteapta 5 secunde_zgomot
                time.sleep(5)

        if(not toggle):  
                secunde_zgomot += time.perf_counter() - start
        print(f'Numar total de secunde zgomot {secunde_zgomot}')
        print("S-a finalizat monitorizarea nivelului de zgomot din camera.")




if __name__ == "__main__":
    start = time.perf_counter()
    modul_microfon = DigitalInputDevice(23)
    stare_sunet = threading.Event()
    monitor_sunet = MonitorSunet(stare_sunet, modul_microfon)

    thread_sunet = threading.Thread(target=monitor_sunet.monitorizeaza_sunet)
    thread_sunet.start()
    time.sleep(30)
    monitor_sunet.stare.set()
    thread_sunet.join()

    print("Iesire din program")
    modul_microfon.close()
    finish = time.perf_counter()
    print(f'Terminat in {round(finish-start,4)} secunde.')
        
 