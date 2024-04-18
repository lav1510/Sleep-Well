from gpiozero import MotionSensor, DigitalInputDevice, LED, Button
import adafruit_dht
import board
import time

#definirea moulelor cu senzori
led = LED(13)
buton = Button(26)
modul_microfon = DigitalInputDevice(23)
modul_miscare_ir = MotionSensor(25)
modul_miscare = MotionSensor(21)
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
        
def citeste_miscare_ir():
        arata_timp()
        print("miscare!")

def citeste_miscare():
        arata_timp()
        print("miscare Radar!")

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

def inchide_module():
        print("Iesire din program")
        modul_microfon.close()
        modul_miscare_ir.close()
        modul_vibratii.close()
        modul_lumina.close()
        modul_miscare.close()
        led.close()
        button.close()
        modul_temperatura_umiditate.exit()
        
(temperatura, umiditate) = citeste_temperatura_umiditate()
print( "Temperatura: {:.1f} C    Umditate: {}% ".format( temperatura, umiditate))
for _ in range(10):
        if not modul_microfon.value : citeste_sunet()
        if modul_miscare_ir.value : citeste_miscare_ir()
        if modul_miscare.value : citeste_miscare()
        if modul_vibratii.value : citeste_presiune()
        if not modul_lumina.value : citeste_lumina()
        if buton.is_pressed: 
                for _ in range (5):
                        led.on()
                        time.sleep(0.1)
                        led.off()
                        time.sleep(0.1)
                        
        time.sleep(10)

inchide_module()
