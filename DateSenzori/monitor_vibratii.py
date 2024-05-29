from gpiozero import DigitalInputDevice
import time
import threading

import utilitare as ut

TIMER_VIBRATII_SOMN_PROFUND = 900
LIMITA_VIBRATII_SOMN_USOR = 180

class MonitorVibratii():
        def __init__(self, stare: threading.Event, modul_vibratii: DigitalInputDevice, grad_vibratie = 0):
            if grad_vibratie not in {0, 1, 2}:
                raise ValueError("Gradul de vibratii poate lua valori doar {0, 1, 2}.")

            if not isinstance(stare, threading.Event):
                raise TypeError("Parametrul 'stare' trebuie sa fie obiect de tipul threading.Event!")

            if not isinstance(modul_vibratii, DigitalInputDevice):
                raise TypeError("Parametrul 'modul_vibratii' trebuie sa fie obiect de tipul DigitalInputDevice!")

            self.grad_vibratie = grad_vibratie
            self.modul_vibratii = modul_vibratii
            self.stare = stare

        def monitorizeaza_vibratie(self):
            print("Monitorizare nivel vibratie saltea.")
            #value = 1 vibratie
            timpi_intre_vibratii = [None] * 5
            grad_curent = self.grad_vibratie

            while not self.stare.is_set(): 
                while grad_curent == self.grad_vibratie and not self.stare.is_set():        
                    #in medie un om adoarme in 15 minute = 900 secunde
                    self.modul_vibratii.wait_for_active(TIMER_VIBRATII_SOMN_PROFUND)
                    if self.modul_vibratii.value:
                        start = time.perf_counter()

                        self.modul_vibratii.wait_for_active(TIMER_VIBRATII_SOMN_PROFUND)
                        if self.modul_vibratii.value:
                                timp = time.perf_counter() - start
                                ut.adauga_element_lista_fixa(timpi_intre_vibratii, round(timp, 2))

                                #determinare grad
                                medie_timpi = ut.medie_ignora_none(timpi_intre_vibratii)
                                if medie_timpi  >  LIMITA_VIBRATII_SOMN_USOR:
                                    grad_curent = 1
                                else: 
                                    grad_curent = 2
                        else:
                                grad_curent = 0
                    else:    
                            #persoana se afla in somn profund sau a parasit patul
                            grad_curent = 0
                    #se asteapta 5 secunde
                    time.sleep(5)

                print("S-a schimbat gradul de vibratii.")
                self.grad_vibratie = grad_curent
            
            print(f'S-a finalizat monitorizarea vibratiilor. ')


if __name__ == "__main__":
    start = time.perf_counter()
    modul_vibratii = DigitalInputDevice(12)
    stare_vibratii = threading.Event()
    monitor_vibratii = MonitorVibratii(stare_vibratii, modul_vibratii)

    thread_vibratie = threading.Thread(target=monitor_vibratii.monitorizeaza_vibratie)
    thread_vibratie.start()
    time.sleep(5)
    monitor_vibratii.stare.set()
    thread_vibratie.join()

    print("Iesire din program")
    modul_vibratii.close()
    finish = time.perf_counter()
    print(monitor_vibratii.grad_vibratie)
    print(f'Terminat in {round(finish-start,4)} secunde.')
        
 