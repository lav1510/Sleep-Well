# Sleep-Well
O aplicatie din sfera Iot care isi propune sa **monitorizeze orele de odihna** si sa afle **calitatea somnului** unei persoane.

## Colectarea si prelucrarea datelor
Tot proiectul se desfasoara pe o placuta de dezvoltare **Raspberry Pi 5**.
![DesignCircuit](https://github.com/lav1510/Sleep-Well/assets/101553716/e3a8d53f-0ece-4f7c-82a4-f789377c10a9)


Datele sunt colectate si prelucrate in timp real intr-un program Python, folosindu-se Threads( fire de executie).

Se doreste ca in viitor sa se organizeze codul sursa in clase si pachete.

Pentru functionarea codului, s-a folosit **schema logica**:

![Schema_Logica drawio](https://github.com/lav1510/Sleep-Well/assets/101553716/d761cf23-4172-4875-a495-dd4a940caa59)

## Stocarea datelor
Datele sunt salvate intr-un server **mySQL**.

Diagrama ER a bazei de date:
![DiagramaER drawio](https://github.com/lav1510/Sleep-Well/assets/101553716/203b3a4e-0d78-41ca-af83-19ee8c844ad2)


## Afisarea informatiilor
Se folosesc platformele **Plotly** si **Dash** pentru a creea o aplicatie interactiva. Bilbioteca **Pandas** e folosita pentru a prelucra datele.
Pentru dezvoltarea aplicatiei, pana sa se colecteze datele pentru setul propriu de date, se foloseste setul de date disponibil la adresa: 
https://www.kaggle.com/datasets/equilibriumm/sleep-efficiency/data


Se doreste ca aplicatia sa arate asa:
![DesignAplicatie](https://github.com/lav1510/Sleep-Well/assets/101553716/28a85e13-0689-479c-850c-8ba1348c8da9)


