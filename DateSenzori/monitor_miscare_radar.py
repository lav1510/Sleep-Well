from gpiozero import DigitalInputDevice
import time
import threading
from statistics import mean

import utilitare as ut

TIMER_MISCARE_SOMN_PROFUND = 600
VARIABILA_MISCARE_SOMN_USOR = 300
VARIABILA_MISCARE_TREAZ_IN_PAT = 600

class MonitorMiscareRadar:
    def __init__(self, stare: threading.Event, modul_miscare: DigitalInputDevice, grad_miscare = 0):
        if grad_miscare not in {0, 1, 2}:
            raise ValueError("Grad miscare poate lua valori doar {0, 1, 2}.")

        if not isinstance(stare, threading.Event):
            raise TypeError("Parametrul 'stare' trebuie sa fie obiect de tipul threading.Event!")

        if not isinstance(modul_miscare, DigitalInputDevice):
            raise TypeError("Parametrul 'modul_miscare' trebuie sa fie obiect de tipul DigitalInputDevice!")

        self.grad_miscare = grad_miscare
        self.stare = stare
        self.modul_miscare = modul_miscare

    def monitorizeaza_miscare(self):
        print("Monitorizare nivel miscare in pat.")
        #value = 1 miscare

        grad_curent = self.grad_miscare

        timpi_intre_miscari = [None] * 5

        while not self.stare.is_set():  
            while grad_curent == self.grad_miscare and not self.stare.is_set():        
                    #in medie un om adoarme in 10 minute = 600 secunde
                    self.modul_miscare.wait_for_active(TIMER_MISCARE_SOMN_PROFUND)
                    if self.modul_miscare.value:
                        start = time.perf_counter()

                        self.modul_miscare.wait_for_active(TIMER_MISCARE_SOMN_PROFUND)
                        if self.modul_miscare.value:
                                timp = time.perf_counter() - start
                                ut.adauga_element_lista_fixa(timpi_intre_miscari, round(timp, 2))

                                #determinare grad
                                medie_timpi = ut.medie_ignora_none(timpi_intre_miscari)
                                if medie_timpi  > VARIABILA_MISCARE_TREAZ_IN_PAT:
                                        grad_curent = 2
                                elif  medie_timpi <  VARIABILA_MISCARE_SOMN_USOR: 
                                        grad_curent = 1
                        else:
                                grad_curent = 0
                    else:    
                            #persoana se afla in somn profund sau a parasit patul
                            grad_curent = 0
                    #se asteapta 5 secunde
                    time.sleep(5)

            print(f'S-a schimbat gradul de miscare. ')
            self.grad_miscare = grad_curent

        print(f'S-a finalizat monitorizarea miscari prin radar. ')




if __name__ == "__main__":

    start = time.perf_counter()
    modul_miscare = DigitalInputDevice(21)
    stare_miscare = threading.Event()
    monitor_miscare_radar = MonitorMiscareRadar(stare_miscare, modul_miscare)

    thread_miscare = threading.Thread(target=monitor_miscare_radar.monitorizeaza_miscare)
    thread_miscare.start()
    time.sleep(10)
    monitor_miscare_radar.stare.set()
    thread_miscare.join()

    print("Iesire din program")
    modul_miscare.close()
    finish = time.perf_counter()
    print(f'Grad nou {monitor_miscare_radar.grad_miscare}')
    print(f'Terminat in {round(finish-start,4)} secunde.')
        
 