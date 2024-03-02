from pymongo import MongoClient

mongo_host = 'localhost'
mongo_port = 27017
mongo_username = 'bbot-db'
mongo_password = 'RosMuBWcxefcYLks'

# Create a connection to MongoDB
client = MongoClient(mongo_host, mongo_port, username=mongo_username, password=mongo_password)

# Access a specific database+
db = client['Techboys']

# Access a specific collection in the database
# collection = db['BBOT']

# # Insert a document into the collection
data = {"key": "value"}

db.get_collection('BBOT').insert_one(data)

# Find documents in the collection
query = {"key": "value",
         "ordered": True}
result = db.get_collection('BBOT').find(query)
# result = collection.find(query)

for document in result:
    print(document)
