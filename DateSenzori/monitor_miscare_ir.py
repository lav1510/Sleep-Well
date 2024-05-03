from gpiozero import DigitalInputDevice
import time
import threading


class MonitorMiscareIR:
    def __init__(self, stare: int,  modul_miscare_ir: DigitalInputDevice):
        if not isinstance(stare, int):
            raise TypeError("Parametrul 'stare' trebuie sa fie obiect de tipul int!")

        if not isinstance(modul_miscare_ir, DigitalInputDevice):
            raise TypeError("Parametrul 'modul_miscare_ir' trebuie sa fie obiect de tipul DigitalInputDevice!")

        self.modul_miscare_ir = modul_miscare_ir
        self.stare = stare
        self.modul_miscare_ir_activat = 0


    def monitorizeaza_miscare_ir(self):
        print("Monitorizare miscare prin PIR.")

        #relevant doar cand starea actuala este 1 (treaz in pat)
        while self.stare == 1 and not self.modul_miscare_ir_activat:        
            if self.modul_miscare_ir.value :
                self.modul_miscare_ir_activat = 1
                print("PIR activ.")
                break
            time.sleep(1)

        print("Monitorzare PIR incheiata.")


if __name__ == "__main__":
    start = time.perf_counter()
    modul_miscare_ir = DigitalInputDevice(25)
    stare_miscare_ir = 1
    monitor_miscare_ir = MonitorMiscareIR(stare_miscare_ir, modul_miscare_ir)

    thread_pir = threading.Thread(target=monitor_miscare_ir.monitorizeaza_miscare_ir)
    thread_pir.start()
    # time.sleep(10)
    # monitor_miscare_ir.stare = 2
    thread_pir.join()

    print("Iesire din program")
    modul_miscare_ir.close()
    finish = time.perf_counter()
    print(monitor_miscare_ir.modul_miscare_ir_activat)
    print(f'Terminat in {round(finish-start,4)} secunde.')