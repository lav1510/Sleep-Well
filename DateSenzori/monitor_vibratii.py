from gpiozero import DigitalInputDevice
import time
import threading

import utilitare as ut

TIMER_VIBRATII_SOMN_PROFUND = 1200
VARIABILA_VIBRATII_SOMN_USOR = 180
VARIABILA_VIBRATII_TREAZ_IN_PAT = 600

class MonitorVibratii():
        def __init__(self, grad_vibratie:int, modul_vibratii: DigitalInputDevice):
            if grad_vibratie not in {0, 1, 2}:
                raise ValueError("Gradul de vibratii poate lua valori doar {0, 1, 2}.")

            if not isinstance(modul_vibratii, DigitalInputDevice):
                raise TypeError("Parametrul 'modul_vibratii' trebuie sa fie obiect de tipul DigitalInputDevice!")

            self.grad_vibratie = grad_vibratie
            self.modul_vibratii = modul_vibratii

        def monitorizeaza_vibratie(self):
            print("Monitorizare nivel vibratie saltea.")
            #value = 1 vibratie

            timpi_intre_vibratii = [None] * 5

            grad_curent = self.grad_vibratie

            while grad_curent == self.grad_vibratie:        
                #in medie un om adoarme in 20 minute = 1200 secunde
                self.modul_vibratii.wait_for_active(TIMER_VIBRATII_SOMN_PROFUND)
                if self.modul_vibratii.value:
                       start = time.perf_counter()

                       self.modul_vibratii.wait_for_active(TIMER_VIBRATII_SOMN_PROFUND)
                       if self.modul_vibratii.value:
                              timp = time.perf_counter() - start
                              ut.adauga_element_lista_fixa(timpi_intre_vibratii, round(timp, 2))

                              #determinare grad
                              medie_timpi = ut.medie_ignora_none(timpi_intre_vibratii)
                              if medie_timpi  > VARIABILA_VIBRATII_TREAZ_IN_PAT:
                                     grad_curent = 2
                              elif  medie_timpi <  VARIABILA_VIBRATII_SOMN_USOR: 
                                     grad_curent = 1
                       else:
                              grad_curent = 0
                else:    
                        #persoana se afla in somn profund sau a parasit patul
                        grad_curent = 0
                #se asteapta 5 secunde
                time.sleep(5)

            print("S-a schimbat gradul de vibratii.")
            self.grad_vibratie = grad_curent


if __name__ == "__main__":
    start = time.perf_counter()
    grad_vibratie = 0
    modul_vibratii = DigitalInputDevice(12)
    monitor_vibratii = MonitorVibratii(grad_vibratie, modul_vibratii)

    thread_vibratie = threading.Thread(target=monitor_vibratii.monitorizeaza_vibratie)
    thread_vibratie.start()
    thread_vibratie.join()

    print("Iesire din program")
    modul_vibratii.close()
    finish = time.perf_counter()
    print(monitor_vibratii.grad_vibratie)
    print(f'Terminat in {round(finish-start,4)} secunde.')
        
 