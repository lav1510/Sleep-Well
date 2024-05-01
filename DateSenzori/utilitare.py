
def adauga_element_lista_fixa(lista, element):
        if len(lista) > 5:
               lista.pop(0)
        lista.append(element)

###################################################################################################################

def medie_ignora_none(data):
    data = [x for x in data if x is not None]
    return sum(data) / len(data) if data else 0

###################################################################################################################

PRAG_MINIM_UMIDITATE = 40
PRAG_MAXIM_UMIDITATE = 50

PRAG_MINIM_TEMPERATURA = 15.5
PRAG_MAXIM_TEMPERATURA = 20

PRAG_MINIM_SOMN_ADANC = 4

PRAG_MINIM_SOMN_TOTAL = 8

PRAG_MAXIM_LUMINA_SUNET = 0

def calitate_somn(umiditate, temperatura,  ore_somn_adanc, ore_somn_total, ore_lumina, ore_sunet):
    
    #Ponderi calitate: umiditate 10%, temperatura 10%, lumina 10%, sunet 15%, durata somn adanc 30%, durata somn total 25%.

    puncte_umiditate = 10 if umiditate >= PRAG_MINIM_UMIDITATE and umiditate <= PRAG_MAXIM_UMIDITATE else 0.
    puncte_temperatura = 10 if temperatura >= PRAG_MINIM_TEMPERATURA and temperatura <= PRAG_MAXIM_TEMPERATURA else 0.
    puncte_ore_somn_adanc =  30 if ore_somn_adanc >= PRAG_MINIM_SOMN_ADANC else 0
    puncte_ore_somn_total =  25 if ore_somn_total >= PRAG_MINIM_SOMN_TOTAL else 0

    puncte_lumina = 10 if ore_lumina <= PRAG_MAXIM_LUMINA_SUNET else 0
    puncte_sunet = 15 if ore_sunet <= PRAG_MAXIM_LUMINA_SUNET else 0

    return int(puncte_umiditate + puncte_temperatura + puncte_ore_somn_adanc + puncte_ore_somn_total + puncte_lumina + puncte_sunet)

if __name__ == "__main__":
        umiditate = 50
        temperatura = 16
        lumina = 1
        sunet = 0
        somn_adanc = 4
        somn_total = 8
        
        print(f'Calitate somn : {calitate_somn(umiditate, temperatura, somn_adanc, somn_total, lumina, sunet)}.')