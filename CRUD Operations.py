import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017")

mydb=client.TelephoneDirectory
details=mydb.TelephoneDetails

#inserting Data into Database
records=[
        {
        'Name':'Raj',
        'STD code':9144,
        'Number':2343435,
        'Place':'Trichy'
        },{
        '_id':1,
        'Name':'Raj',
        'STD code':9144,
        'Number':2343435,
        'Place':'Trichy'
        },{
        '_id':2,
        'Name':'Ram',
        'STD code':9145,
        'Number':2343035,
        'Place':'Anna nagar'
        },{
        '_id':3,
        'Name':'Ajay',
        'STD code':9146,
        'Number':2343437,
        'Place':'T Nagar'       
        }
        ]
details.insert_many(records)

# Query to find all the records in database
for records in details.find():
        print(records)

# Query to update one records in database
details.update_one({"_id":1},{"$set":{"Place":"Chennai"}})

# Query to delete record in database
details.delete_one({"Place":"Trichy"})

print("New Records")
for records in details.find():
        print(records)