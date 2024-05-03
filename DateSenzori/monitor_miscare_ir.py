from gpiozero import DigitalInputDevice
import time
import threading

class MonitorMiscareIR:
    def __init__(self, stare, modul_miscare_ir: DigitalInputDevice):
        if not isinstance(modul_miscare_ir, DigitalInputDevice):
            raise TypeError("Parametrul 'modul_miscare_ir' trebuie sa fie obiect de tipul DigitalInputDevice!")

        self.modul_miscare_ir = modul_miscare_ir
        self.modul_miscare_ir_activat = 0
        self.stare = stare


    def monitorizeaza_miscare_ir(self):
        
        #time.sleep(300)
        print("Monitorizare miscare prin PIR.")

        while not self.modul_miscare_ir.value and not self.stare.is_set():
            if self.modul_miscare_ir.value :
                self.modul_miscare_ir_activat = 1
                print("PIR activ.")
            time.sleep(2)

        print("Monitorzare PIR incheiata.")


if __name__ == "__main__":
    start = time.perf_counter()
    modul_miscare_ir = DigitalInputDevice(25)
    stare_miscare_ir = threading.Event()
    monitor_miscare_ir = MonitorMiscareIR(stare_miscare_ir, modul_miscare_ir)

    monitor_miscare_ir.monitorizeaza_miscare_ir()
    monitor_miscare_ir.stare.set()
    print("Iesire din program")
    modul_miscare_ir.close()
    finish = time.perf_counter()
    print(monitor_miscare_ir.modul_miscare_ir_activat)
    print(f'Terminat in {round(finish-start,4)} secunde.')