# Sleep-Well
O aplicatie din sfera IoT care isi propune sa **monitorizeze orele de odihna** si sa afle **calitatea somnului** unei persoane.

# Link-ul repository-ului
Codul sursă poate fi accesat la adresa: https://github.com/lav1510/Sleep-Well. 

# Cerinte
* Proiectul este destinat sa fie rulat exclusiv pe o placuta de dezvoltare **Raspberry Pi 5**.
* Versiunea de Python folosita este **Python 3.11**.
* **Conectarea fizica a modulelor** folosite la pinii de intrare iesire (GPIO) conform figurii de mai jos.
* Conectarea la internet a placutei fie prin cablul Ethernet fie prin Wifi.
* Instalarea Visual Studio Code pe placuta.
* Instalarea biblioteciilor folosite

# Pasii de instalare
Inainte de rularea aplicatiei se deschide un nou terminal din desktopul placutei si se ruleaza comenzile de mai jos:


Actualizarea programelor
```
sudo apt-get update
sudo apt-get upgrade

```

Instalare Python 3.11
```
sudo apt-get install python3.11
sudo apt-get install python3-pip
```
Instalarea bibliotecilor folosite
```
pip3 install gpiozero
pip3 install adafruit-circuitpython-dht --break-system-packages
sudo apt-get install libgpiod2
pip3 install pandas
pip3 install dash
pip3 install pymongo
```

# Pasii de rulare
*Se deschide folderul _Sleep_ in editorul de text Visual Studio Code
*In terminalul _bash_ deschis din editorul de text și se executa
```
cd DateSenzori
python3 modul_principal.py
```
Astfel se porneste programul pentru monitorizare si determinare a calitatii somnului, acesta va astepta dupa apasarea butonului.

*Pentru a deschide aplicatia web dintr-un terminal separat bash:
```
cd Aplicatie
python3 aplicatie.py
```

După rulare va aparea un link. Linkul va fi accesat prin apasarea tastei CTR si click pe acesta.


Aplicatia web poate fi accesata si de pe o sursa externa, instaland doar bibliotecile pandas, dash si mongo si executand fisierul aplicatie.py, ca in figura de mai jos.
Fisierele din directorul DateSenzori nu pot fi executate extern.

![runaplicatie](https://github.com/lav1510/Sleep-Well/assets/101553716/1c4307d6-dc0e-475b-861a-35c536bdf50f)



# Structura
Exista 4 directoare prezente in acest repository. 
**Directorul DateSenzori** este directorul principal. Acesta contine fisierele responsabile pentru citirea senzorilor, prelucrarea informatiilor si inserare in baza de date.


**Fisierul _modul_principal.py_** este cel mai important fisier, acesta importa celelalte fisiere pentru a indeplinii functionalitate proiectului.


Directorul Aplicatie contine fisierul _aplicatie.py_ care este sursa aplicatiei web unde se pot vizualiza local informatiile din baza de date.

# Despre proiect
## Colectarea si prelucrarea datelor
Tot proiectul se desfasoara pe o placuta de dezvoltare **Raspberry Pi 5**.

Conectarea se face astfel:
* senzorul de sunet are conectată ieșirea la GPIO24;
* senzorul de mișcare PIR are ieșirea la GPIO25;
* senzorul de vibrații are ieșirea la GPIO12;
* senzorul de mișcare Doppler are ieșirea la GPIO21;
* senzorul de lumină conectat la GPIO27;
* senzorul de temperatură și umiditate DHT22 are ieșirea la GPIO4;
* ieșirea butonului la GPIO26;
* intrarea LED-ului verde la GPIO13.
  
![DesignCircuit](https://github.com/lav1510/Sleep-Well/assets/101553716/e3a8d53f-0ece-4f7c-82a4-f789377c10a9)


Datele sunt colectate si prelucrate in timp real intr-un program Python, folosindu-se Threads( fire de executie).
Pentru functionarea codului, s-a folosit **schema logica**:

![ordinograma](https://github.com/lav1510/Sleep-Well/assets/101553716/5ce649d6-7c63-4d47-95f2-90b7d753d292)

## Stocarea datelor
Datele sunt salvate in baza de date online **MongoDB**.

Diagrama ER a bazei de date:
![DiagramaER drawio](https://github.com/lav1510/Sleep-Well/assets/101553716/203b3a4e-0d78-41ca-af83-19ee8c844ad2)


## Afisarea informatiilor
Se folosesc platformele **Plotly** si **Dash** pentru a creea o aplicatie interactiva. Bilbioteca **Pandas** e folosita pentru a prelucra datele.

![aplicatie](https://github.com/lav1510/Sleep-Well/assets/101553716/534d51cf-b9ba-4987-bbb7-4b739b4d177a)


