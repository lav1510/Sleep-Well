from gpiozero import DigitalInputDevice
import time
import threading

class MonitorMiscareIR:
    def __init__(self, modul_miscare_ir: DigitalInputDevice):
        if not isinstance(modul_miscare_ir, DigitalInputDevice):
            raise TypeError("Parametrul 'modul_miscare_ir' trebuie sa fie obiect de tipul DigitalInputDevice!")

        self.modul_miscare_ir = modul_miscare_ir
        self.modul_miscare_ir_activat = 0


    def monitorizeaza_miscare_ir(self):
        print("Monitorizare miscare prin PIR.")

        self.modul_miscare_ir.wait_for_active()
        if self.modul_miscare_ir.value :
            self.modul_miscare_ir_activat = 1
            print("PIR activ.")

        print("Monitorzare PIR incheiata.")


if __name__ == "__main__":
    start = time.perf_counter()
    modul_miscare_ir = DigitalInputDevice(25)
    monitor_miscare_ir = MonitorMiscareIR(modul_miscare_ir)

    monitor_miscare_ir.monitorizeaza_miscare_ir()

    print("Iesire din program")
    modul_miscare_ir.close()
    finish = time.perf_counter()
    print(monitor_miscare_ir.modul_miscare_ir_activat)
    print(f'Terminat in {round(finish-start,4)} secunde.')