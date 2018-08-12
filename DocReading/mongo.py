# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 21:22:13 2018

@author: Ken
"""

#%%
import pymongo
#must install dnspython 

client = pymongo.MongoClient('mongodb+srv://ken_test:Password1@kentest-82ly3.gcp.mongodb.net/test?retryWrites=true')

db = client.test

#creates a database called 'contdatabase'
mydb = client['contdatabase']
#create a collection called 'documents'
mycol = mydb['documents']

#mydict = { "name": "John", "address": "Highway 37" }
#inserts a record into 'documents' collection
#x = mycol.insert_one(mydict)
#%%
mylist = [
  { "_id": 1, "name": "John", "address": "Highway 37"},
  { "_id": 2, "name": "Peter", "address": "Lowstreet 27"},
  { "_id": 3, "name": "Amy", "address": "Apple st 652"},
  { "_id": 4, "name": "Hannah", "address": "Mountain 21"},
  { "_id": 5, "name": "Michael", "address": "Valley 345"},
  { "_id": 6, "name": "Sandy", "address": "Ocean blvd 2"},
  { "_id": 7, "name": "Betty", "address": "Green Grass 1"},
  { "_id": 8, "name": "Richard", "address": "Sky st 331"},
  { "_id": 9, "name": "Susan", "address": "One way 98"},
  { "_id": 10, "name": "Vicky", "address": "Yellow Garden 2"},
  { "_id": 11, "name": "Ben", "address": "Park Lane 38"},
  { "_id": 12, "name": "William", "address": "Central st 954"},
  { "_id": 13, "name": "Chuck", "address": "Main Road 989"},
  { "_id": 14, "name": "Viola", "address": "Sideway 1633"}
]

#inserts many records into 'documents' collection
#each with id as specified
x = mycol.insert_many(mylist)

#returns all documents in the 'documents' collections
for x in mycol.find():
  print(x)

#Return only the names and addresses, not the _ids:
for x in mycol.find({},{ "_id": 0, "container": 1, "shippedon": 1 }):
  print(x)
#You get an error if you specify both 0 and 1 values in the same object (except if one of the fields is the _id field):
  
#for query
myquery = { "address": "Park Lane 38" }
mydoc = mycol.find(myquery)
for x in mydoc:
  print(x)
  
#advanced query
#Find documents where the address starts with the letter "S" or higher:
myquery = { "address": { "$gt": "S" } }
mydoc = mycol.find(myquery)
for x in mydoc:
  print(x)

#filter with regex
myquery = { "container": { "$regex": "SZ" }, "date": {"$regex": "11"} }
mydoc = mycol.find(myquery)
for x in mydoc:
  print(x)
  
#for nested array
myquery = { "products.name": {"$regex": "P"} }
mydoc = mycol.find(myquery)
for x in mydoc:
  print(x)  


#sort the results
mydoc = mycol.find().sort("name")
for x in mydoc:
  print(x)

#delete
myquery = { "address": "Mountain 21" }
mycol.delete_one(myquery)

#delete many
myquery = { "address": {"$regex": "^S"} }
x = mycol.delete_many(myquery)
print(x.deleted_count, " documents deleted.")

#delete all
x = mycol.delete_many({})
print(x.deleted_count, " documents deleted.")

#drop collection
mycol.drop()

#update 
myquery = { "address": "Valley 345" }
newvalues = { "$set": { "address": "Canyon 123" } }
mycol.update_one(myquery, newvalues)

#update many
myquery = { "address": { "$regex": "^S" } }
newvalues = { "$set": { "name": "Minnie" } }
x = mycol.update_many(myquery, newvalues)
print(x.modified_count, "documents updated.")

