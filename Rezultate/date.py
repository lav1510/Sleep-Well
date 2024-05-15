import pandas as pd

#citirea datelor, sursa: https://www.kaggle.com/datasets/equilibriumm/sleep-efficiency?resource=download
df = pd.read_csv("Sleep_Efficiency.csv")

#filtrarea datelor
df = df[df['Gender'] == 'Female']
df = df[(df['Age'] <= 28) & (df['Age'] >= 20)]
df = df[['Bedtime', 'Sleep duration',
       'Sleep efficiency']]

#statistica
marime = len(df)
medie_durata = round(df['Sleep duration'].mean(), 2)
medie_calitate = round(df['Sleep efficiency'].mean(), 2)
print(f'în medie, din {marime} înregistrări din 2021, colectate pentru femei cu vârsta între 20 si 28 de ani,\n numarul orelor dormite este {medie_durata}, iar calitatea este {medie_calitate}%.')