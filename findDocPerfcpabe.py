from cryptography.fernet import Fernet
from pymongo import MongoClient
import pymongo
import hashlib, cpabe, json, timeit, subprocess


def findDocTime():
    client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
    mydb = client['EncryptedMTR']
    mycol = mydb['patientcpabe']
    prevLeastRuntime = 0
    for i in range(1000,10001,1000):
        j = str(i)
        while(len(j) < 5):
            j = "0"+ j
        id = "p{}".format(j)
        #runtimexbar = 0 
        runtime_list = []
        totalbrowsetime = 0
        for k in range(10):
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
            stop = timeit.default_timer()
            totalbrowsetime = stop-start

            #print(document)
            start = timeit.default_timer()
            #CT = document["CT"]
            CT_byte = str.encode(document["CT"],encoding="ISO-8859-1")

            # with open('./patientCloud/{}.txt.cpabe'.format(id),'wb') as file:
            #     file.write(CT_byte)
            cpabe.decrypt("./patientCloud/enc_{}.txt.cpabe".format(id))
            # with open('./patientCrypto/{}.txt'.format(id),'r') as file:
            #     PT = file.read()
            #fernet = Fernet(Symkey)
            #PT_byte= fernet.decrypt(CT_byte)
            #PT = PT_byte.decode("ISO-8859-1")
            #print(PT)
            stop = timeit.default_timer()
            runtime = stop -start + totalbrowsetime
            runtime_list.append(runtime)
            #runtimexbar += runtime
        runtime_list.sort()
        for i1 in range(len(runtime_list)):
                if runtime_list[i1] > prevLeastRuntime:
                    print('DecTime({})(ms): '.format(i), runtime_list[i1]*1000)
                    prevLeastRuntime = runtime_list[i1]
                    break
        # runtimexbar = runtimexbar / 5
        # print('DecTime({}): '.format(i), runtimexbar)
            #print(PT)
    #PT_json = json.loads(PT)
    #PT_sorted = json.dumps(PT_json, indent = 3)
    #stop = timeit.default_timer()
    #print('Dec Time: ', stop - start)
    #print(PT_sorted)
    # print(Symkey)
    #print(PT_json)
    #print(type(PT_json))
    #return PT_json

findDocTime()
