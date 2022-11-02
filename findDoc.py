from cryptography.fernet import Fernet
from pymongo import MongoClient
import pymongo
import hashlib, cpabe, json, timeit
def findDoc(id):
    client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
    mydb = client['EncryptedMTR']
    mycol = mydb['patient']
    #start = timeit.default_timer()
    id_byte = str.encode(id)
    #generate MAC from patient id
    id_MD = hashlib.sha256(id_byte).hexdigest()
    #print(id_MD)
    try:
        document = mycol.find_one({'MD_id': id_MD}) #find the wanted document by MD_id
        #print(document)
    except(pymongo.errors.ServerSelectionTimeoutError):
        print("Connection timeout")
        exit()
    #print(document)
    #start = timeit.default_timer()
    enc_SK = document["enc_SK"]
    CT_byte = str.encode(document["CT"])
    #print(type(enc_SK))
    #print(enc_SK)
    #store the enc_Symkey to local storage
    enc_SK = str.encode(enc_SK, encoding="ISO-8859-1")
    #print("Byte SK: ",enc_SK)
    # enc_SK.decode("ISO-8859-1")
    # print(enc_SK)
    with open('./SymkeyCloud/{}_key.txt.cpabe'.format(id),'wb') as file:
        file.write(enc_SK)
    #Decrypt the enc_Symkey
    cpabe.decrypt("./SymkeyCloud/{}_key.txt.cpabe".format(id))
    with open('./SymkeyCloud/{}_key.txt'.format(id),'r') as file:
        Symkey = file.read()
    fernet = Fernet(Symkey)
    PT_byte= fernet.decrypt(CT_byte)
    PT = PT_byte.decode("ISO-8859-1")
    #stop = timeit.default_timer()
    #print('Dec: ', stop - start)
    PT_json = json.loads(PT)
    PT_sorted = json.dumps(PT_json, indent = 3)
    #stop = timeit.default_timer()
    #print('Dec Time: ', stop - start)
    print(PT_sorted)
    # print(Symkey)
    #print(PT_json)
    #print(type(PT_json))
    return PT_json,id_MD

def findDocTime():
    client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
    mydb = client['EncryptedMTR']
    mycol = mydb['patient']
    for i in range(1,51):
        j = str(i)
        if len(j) == 1:
            j = "0"+ j
        id = "p000{}".format(j)
        #print(id)
        runtimexbar = 0 
        for j in range(5):
            start = timeit.default_timer()
            id_byte = str.encode(id)
            #generate MAC from patient id
            id_MD = hashlib.sha256(id_byte).hexdigest()
            #print(id_MD)
            try:
                document = mycol.find_one({'MD_id': id_MD}) #find the wanted document by MD_id
                #print(document)
            except(pymongo.errors.ServerSelectionTimeoutError):
                print("Connection timeout")
                exit()
            #print(document)
            #start = timeit.default_timer()
            enc_SK = document["enc_SK"]
            CT_byte = str.encode(document["CT"])
            #print(type(enc_SK))
            #print(enc_SK)
            #store the enc_Symkey to local storage
            enc_SK = str.encode(enc_SK, encoding="ISO-8859-1")
            #print("Byte SK: ",enc_SK)
            # enc_SK.decode("ISO-8859-1")
            # print(enc_SK)
            with open('{}1_key.txt.cpabe'.format(id),'wb') as file:
                file.write(enc_SK)
            #Decrypt the enc_Symkey
            cpabe.decrypt("{}1".format(id))
            with open('{}1_key.txt'.format(id),'r') as file:
                Symkey = file.read()
            fernet = Fernet(Symkey)
            PT_byte= fernet.decrypt(CT_byte)
            PT = PT_byte.decode("ISO-8859-1")
            stop = timeit.default_timer()
            runtime = stop -start
            runtimexbar += runtime
        runtimexbar = runtimexbar / 5
        print('DecTime({}): '.format(i), runtimexbar)
        #print(PT)
    PT_json = json.loads(PT)
    PT_sorted = json.dumps(PT_json, indent = 3)
    #stop = timeit.default_timer()
    #print('Dec Time: ', stop - start)
    #print(PT_sorted)
    # print(Symkey)
    #print(PT_json)
    #print(type(PT_json))
    return PT_json

findDoc("p0009")
