from pymongo import MongoClient # type: ignore
from pymongo.server_api import ServerApi # type: ignore

import configurare_mongo_privat

#conexiune la server
client = MongoClient(configurare_mongo_privat.CONNECTION_STRING, server_api=ServerApi('1'))

# #confirmare conexiune
try:
    client.admin.command('ping')
    print("Conectat cu succes la MongoDB!")
except Exception as e:
    print(e)

baza_date = client['Sleep']['SleepProject']

