from pymongo import MongoClient
from pymongo.server_api import ServerApi

import configurare_mongo_privat

#conexiune la server
client = MongoClient(configurare_mongo_privat.CONNECTION_STRING, server_api=ServerApi('1'))

# #confirmare conexiune
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

baza_date = client['Sleep']['SleepProject']
