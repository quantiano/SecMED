import base64
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64, hashlib, random, timeit, pymongo, datetime, json, math
from random import choice


client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
#client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client['EncryptedMTR']
Data_owner_list = []
mycol_audit = mydb['AuditLog']
mycol_patient = mydb['patient']
item_details = mycol_audit.find()
templist = []
thislist = []
no =0
def XOR (a, b):
    if a != b:
        return 1
    else:
        return 0

document_audit = mycol_audit.find_one({'MD_id': "a4d5e07e23b14fef41dbb972621cf67d2fc47e6614f6c61bc0b598ac474343c5"})
timestamp = ''
for i in document_audit:
    if (i[0:2] == "20"):
        timestamp = timestamp+i
print(timestamp)