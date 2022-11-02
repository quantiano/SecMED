from cryptography.fernet import Fernet
import hmac, hashlib
import json
import hashlib
from pymongo import MongoClient
import pymongo
import JSONCrypto

def getalldoc(key,db):

    client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
    mydb = client['Hospital']
    mycol = mydb[db]
    #Get id from database
    for doc in mycol.find(): #find the wanted document by comparing MD
        
        decdoc = JSONCrypto.decryptjson(key,doc)
        if not decdoc:  #if decryptjson returned False then terminate this function
            return False
        id_byte = str.encode(decdoc["id"])
        hmac1 = hmac.new(key, id_byte, digestmod=hashlib.sha256)
        #Create MD from hmac1
        md1 = hmac1.hexdigest()
        decdoc_sorted = json.dumps(decdoc,indent = 6)
        #print("MD: ",md1)
        #if(decdoc_sorted['password'] != ''):
        #    decdoc['password'] = ''
        print("{}'s document: \n{}".format(decdoc["name"],decdoc_sorted))
        
    return True
