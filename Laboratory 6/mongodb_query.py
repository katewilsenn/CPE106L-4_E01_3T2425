from pymongo import MongoClient
import pprint
import re

## Connect to the client and database
client = MongoClient("mongodb://localhost:27017/")
db = client["local"]

## Access the customers collection (table) 
customers_collection = db["customers"]
print(customers_collection)

## Print the first document (entry)
# doc1 = customers_collection.find_one()
# print(doc1)

## Print all documents (entries)
# for all_doc in customers_collection.find():
#   print(all_doc)

## Print the first and last name from each document
# for rec in customers_collection.find({},{"_id": 0,"LastName": 1, "FirstName": 1}):
#   print(rec)

## Find last names starting in 'G'
rgx = re.compile('^G.*?$', re.IGNORECASE)
cursor = customers_collection.find({"LastName": rgx})
num_docs = 0

## Count and print queried documents
for document in cursor:
  num_docs += 1
  pprint.pprint(document)
  print()

print("# of documents found: " + str(num_docs))
client.close()
