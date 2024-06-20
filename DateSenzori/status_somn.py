from datetime import datetime 
import time
 
class StatusSomn():

    def __init__(self):
        self.ora_culcare = None
        self.ora_trezire = None
        self.secunde_somn_adanc = 0
        self.secunde_somn_usor = 0
        self.start_usor = 0
        self.start_profund = 0

    def testeaza_starea(self, stare_anterioara = 0, buton = 0, miscare_pir = 0, grad_miscare = 0, grad_vibratii = 0):

        stare = { 'treaz': 0 , 'treaz_in_pat': 1, 'somn_usor': 2, 'somn_profund': 3}
        miscare = { 'miscare_putina': 0 , 'miscare_medie': 1, 'miscare_multa': 2}
        vibratii = { 'vibraii_inexistene': 0 , 'vibratii_rare': 1, ' vibratii_dese': 2}

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
                                self.start_usor = time.perf_counter()
                                self.ora_culcare = datetime.now().replace(second = 0, microsecond = 0)
                #somn_usor
                case 2:
                        if grad_miscare == miscare['miscare_putina'] and grad_vibratii == vibratii['vibraii_inexistene']:
                                stare_somn = stare['somn_profund']
                                self.secunde_somn_usor += time.perf_counter() - self.start_usor
                                self.start_profund = time.perf_counter()
                        elif grad_miscare == miscare['miscare_multa'] or grad_vibratii == vibratii['vibratii_dese']:
                                stare_somn = stare['treaz_in_pat']
                                self.secunde_somn_usor += time.perf_counter() - self.start_usor
                                self.ora_trezire = datetime.now().replace(second = 0, microsecond = 0)
                #somn_profund
                case 3:
                        if grad_miscare != miscare['miscare_putina']:
                                stare_somn = stare['somn_usor'] 
                                self.secunde_somn_adanc += time.perf_counter() - self.start_profund
                                self.start_usor = time.perf_counter()
                        else:
                                stare_somn = stare_anterioara
                        
                case _:
                        #stare invalida
                        stare_somn = -1

        return stare_somn


if __name__ == "__main__":
        st = StatusSomn()
        print(f'Stare: {st.testeaza_starea(stare_anterioara = 2, buton = 0, miscare_pir = 0, grad_miscare = 0, grad_vibratii = 0)}.')
        print(st.ora_culcare, st.ora_trezire)
