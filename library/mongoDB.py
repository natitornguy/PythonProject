import pymongo

def connectDB():
    client = getClient()
    db = client.get_database("workbox")
    return db

def getClient():
    client =   pymongo.MongoClient("mongodb+srv://natitornguy:Natitorn1547@cluster0.y0ywg.mongodb.net/<dbname>?retryWrites=true&w=majority")
    return client