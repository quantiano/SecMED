import types
from cryptography.fernet import Fernet
import json
from pymongo import MongoClient
import pymongo
import findDoc
import JSONCrypto
import os
NoneType = type(None)
def deletePatient(key,patientdb):
        while(True):
            pid = input("Enter patient id: ")
            if pid == "exit": 
                exit()
            elif pid == "back":
                break

            if pid[2] != patientdb[7]:
                print("You don't have permission to access section {}".format(pid[2]))
            #find the document
            wanteddoc = findDoc.findDoc(key,pid,patientdb)
            if type(wanteddoc) != NoneType:
                #decrypt the document
                decdoc = JSONCrypto.decryptjson(key,wanteddoc)
                
                decdoc_sorted = json.dumps(decdoc, indent = 6)
                print(decdoc_sorted)

                while(True): #keep asking for the confirmation
                    ans = input("Do you want to delete this document? (y/n/exit): ")
                    if ans =='y':
                        client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
                        mydb = client['SecMED'] #connect to db
                        mycol = mydb[patientdb]
                        mycol.delete_one(wanteddoc)
                        
                        #delete local document
                        f = open('./section{}-patient/{}_{}.json'.format(patientdb[7],pid,decdoc["name"]), 'w') #delete local file
                        f.close()
                        os.remove(f.name)
                        print("{}'s document has been deleted".format(pid))
                        break
                    elif ans =='n':
                        break
                    elif ans == "exit":
                        exit()
                    else:
                        print("Invalid input, please try again")
            else:
                print("Invalid patient's ID")

