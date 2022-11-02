
from asyncio import start_server
from cryptography.fernet import Fernet
import json
import hashlib, rsa
import SigningPhasePerf
import os, subprocess, cpabe, keygenerator, timeit,time
def encryptjson(pid,certid):
    start = timeit.default_timer()
    #--------Begin Encryption Phase----------

    id_byte = str.encode(pid)
    #generate Symkey
    symkey = keygenerator.symkeygenerator(pid)
    with open('./Symkeys/{}_key.txt'.format(pid),'wb') as file:
        file.write(symkey)
    # with open('./Patient160/{}.json'.format(pid),'r') as file:
    #     doc = file.read()
    with open('./testpatient/{}.txt'.format(pid),'r') as file:
        doc = file.read()
    doc_byte = str.encode(doc, encoding="ISO-8859-1")

    #start = timeit.default_timer()
    CT_byte= Fernet(symkey).encrypt(doc_byte)
    
    #hash patient id
    #start = timeit.default_timer()
    id_MD = hashlib.sha256(id_byte).hexdigest()
    #stop = timeit.default_timer()
    #runtime1 = stop-start
    # convert bytes to string
    CT = CT_byte.decode("ISO-8859-1")
    #stop = timeit.default_timer()

    #encrypt SymKey with CP-ABE PubKey
    #print("here")
    cpabe.encrypt_key(pid)
    
    #rename encrypted symkey file to be able to read the file
    p = subprocess.call(["mv", "./Symkeys/{}_key.txt.cpabe".format(pid), "./Symkeys/{}_key.txt".format(pid)])
    
    #-----Begin Signing Phase------
    DS_R, R1, runtimexor = SigningPhasePerf.Sign(CT_byte,CT,certid, id_MD)
    #stop = time.time()
    #print("Time({}): ".format(i),stop-start)
    #read the encrypted SymKey
    with open('./Symkeys/{}_key.txt'.format(pid),'rb') as file:
        enc_Symkey = file.read()
    #convert byte to string for storing in the DB
    enc_Symkey = enc_Symkey.decode("ISO-8859-1")
    #rename the symkey file
    p = subprocess.call(["mv", "./Symkeys/{}_key.txt".format(pid), "./Symkeys/{}_key.txt.cpabe".format(pid)])
    #Decrypt the local Symkey
    cpabe.decrypt("./Symkeys/{}_key.txt.cpabe".format(pid))
    # Form a JSON document for storing on cloud
    doc = {'MD_id': '{}'.format(id_MD), 'CT': '{}'.format(CT), 'enc_SK': '{}'.format(enc_Symkey),
    'DS*R': '{}'.format(DS_R), 'R1': '{}'.format(R1)}
    stop = timeit.default_timer()
    runtime = stop - start
    #print(doc)
    return doc, runtime