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

item_1 = {
  "_id" : "U1IT00001",
  "item_name" : "Blender",
  "max_discount" : "10%",
  "batch_number" : "RR450020FRG",
  "price" : 340,
  "category" : "kitchen appliance"
}

item_2 = {
  "_id" : "U1IT00002",
  "item_name" : "Egg",
  "category" : "food",
  "quantity" : 12,
  "price" : 36,
  "item_description" : "brown country eggs"
}

try:
    baza_date.insert_many([item_1, item_2])
    print("Data inserted successfully!")
except Exception as e:
    print("Error:", e)