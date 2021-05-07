import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
starlight = client['starlight']
records = starlight['records']

records.delete_many()
