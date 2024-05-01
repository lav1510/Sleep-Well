from datetime import datetime 
import time

import configurare_mongo

###################################################################################################################

def adauga_element_lista_fixa(lista, element):
        if len(lista) > 5:
               lista.pop(0)
        lista.append(element)

###################################################################################################################

def medie_ignora_none(data):
    data = [x for x in data if x is not None]
    return sum(data) / len(data) if data else 0
###################################################################################################################

def joc_led(led):
        for _ in range (5):
                led.on()
                time.sleep(0.1)
                led.off()
                time.sleep(0.1)

###################################################################################################################

def mod_consum_energie(buton, led):
        print("Asteptare apasare buton...")
        while buton.is_pressed:
                time.sleep(1)
        else:
                joc_led(led)

###################################################################################################################

PRAG_MINIM_UMIDITATE = 40
PRAG_MAXIM_UMIDITATE = 50

PRAG_MINIM_TEMPERATURA = 15.5
PRAG_MAXIM_TEMPERATURA = 20

PRAG_MINIM_SOMN_ADANC = 4

PRAG_MINIM_SOMN_TOTAL = 8

PRAG_MAXIM_LUMINA_SUNET = 0

def calitate_somn(umiditate = 0, temperatura = 0,  ore_somn_adanc = 0, ore_somn_total = 0, ore_lumina = 0, ore_sunet = 0):
    
    #Ponderi calitate: umiditate 10%, temperatura 10%, lumina 10%, sunet 15%, durata somn adanc 30%, durata somn total 25%.

    puncte_umiditate = 10 if umiditate >= PRAG_MINIM_UMIDITATE and umiditate <= PRAG_MAXIM_UMIDITATE else 0.
    puncte_temperatura = 10 if temperatura >= PRAG_MINIM_TEMPERATURA and temperatura <= PRAG_MAXIM_TEMPERATURA else 0.
    puncte_ore_somn_adanc =  30 if ore_somn_adanc >= PRAG_MINIM_SOMN_ADANC else 0
    puncte_ore_somn_total =  25 if ore_somn_total >= PRAG_MINIM_SOMN_TOTAL else 0

    puncte_lumina = 10 if ore_lumina <= PRAG_MAXIM_LUMINA_SUNET else 0
    puncte_sunet = 15 if ore_sunet <= PRAG_MAXIM_LUMINA_SUNET else 0

    return int(puncte_umiditate + puncte_temperatura + puncte_ore_somn_adanc + puncte_ore_somn_total + puncte_lumina + puncte_sunet)

###################################################################################################################
stare = { 'treaz': 0 , 'treaz_in_pat': 1, 'somn_usor': 2, 'somn_profund': 3}

miscare = { 'miscare_putina': 0 , 'miscare_medie': 1, 'miscare_multa': 2}
vibratii = { 'vibraii_inexistene': 0 , 'vibratii_rare': 1, ' vibratii_dese': 2}

def testeaza_starea(stare_anterioara = 0, buton = 0, miscare_pir = 0, grad_miscare = 0, grad_vibratii = 0):

        global ora_culcare 
        global ora_trezire

        ora_culcare = None
        ora_trezire = None
        
        stare_somn = stare_anterioara

        match stare_anterioara:
                #treaz
                case 0:
                        stare_somn = stare['treaz_in_pat'] if buton and grad_vibratii != vibratii['vibraii_inexistene'] else stare_anterioara
                #treaz_in_pat
                case 1:
                        if grad_miscare == miscare['miscare_putina'] and grad_vibratii == vibratii['vibraii_inexistene'] and miscare_pir:
                                stare_somn = stare['treaz']
                        elif grad_miscare != miscare['miscare_multa'] or grad_vibratii != vibratii['vibratii_dese']:
                                stare_somn = stare['somn_usor']
                                ora_culcare = datetime.now().replace(second = 0, microsecond = 0)
                #somn_usor
                case 2:
                        if grad_miscare == miscare['miscare_putina'] and grad_vibratii == vibratii['vibraii_inexistene']:
                                stare_somn = stare['somn_profund']
                        elif grad_miscare == miscare['miscare_multa'] or grad_vibratii == vibratii['vibratii_dese']:
                                stare_somn = stare['treaz_in_pat']
                                ora_trezire = datetime.now().replace(second = 0, microsecond = 0)
                #somn_profund
                case 3:
                        stare_somn = stare['somn_usor'] if grad_miscare != miscare['miscare_putina'] else stare_anterioara

                case _:
                        #stare invalida
                        stare_somn = -1

        return stare_somn

###################################################################################################################
def insereaza_baza_date(umiditate_medie, temp_medie,  ore_somn_profund, ore_somn_usor, lumina, sunet, ora_trezire, ora_culcare):
        
        ore_somn_complet = ore_somn_profund + ore_somn_usor
        calitatea_somnului = calitate_somn(umiditate = umiditate_medie, temperatura = temp_medie,  ore_somn_adanc = ore_somn_profund, ore_somn_total = ore_somn_complet, ore_lumina = lumina, ore_sunet = sunet)

        print(f'Calitate somn : {calitatea_somnului}.')
        un_somn = {
        "umiditate_medie" : umiditate_medie,
        "temp_medie" : temp_medie,
        "ore_somn_profund" : ore_somn_profund,
        "ore_somn_complet" : ore_somn_complet,
        "lumina" : lumina,
        "sunet" : sunet,
        "ora_trezire" : ora_trezire,
        "ora_culcare" : ora_culcare,
        "calitatea_somnului" : calitatea_somnului
        }


        try:
                configurare_mongo.baza_date.insert_one(un_somn)
                print("Data inserted successfully!")
        except Exception as e:
                print("Error:", e)

###################################################################################################################

if __name__ == "__main__":
        print(f'Calitate somn : {calitate_somn(umiditate = 50, temperatura = 16,  ore_somn_adanc = 4, ore_somn_total = 8, ore_lumina = 1)}.')
        print(f'Stare: {testeaza_starea(stare_anterioara = 1, buton = 0, miscare_pir = 0, grad_miscare = 1, grad_vibratii = 0)}.')
        print(ora_culcare, ora_trezire)

        insereaza_baza_date(umiditate_medie = 50, temp_medie = 16.3,  ore_somn_profund = 8, ore_somn_usor = 4, lumina = 1, sunet = 0, ora_trezire = ora_culcare, ora_culcare = ora_culcare)
        