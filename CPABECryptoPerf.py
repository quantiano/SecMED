
from cryptography.fernet import Fernet
import json
import hashlib, rsa
import SigningPhasePerf
import os, subprocess, cpabe, keygenerator, timeit
def encryptjson(pid,certid):
    start = timeit.default_timer()
    #--------Begin Encryption Phase----------

    id_byte = str.encode(pid)
    #generate Symkey
    # this encrypts the data read from your json and stores it in 'encrypted'
    #start = timeit.default_timer()
    
    cpabe.encrypt_text(pid)
    #p = subprocess.call(["dataowner", "or", "medicalstaff"])
    #hash patient id
    id_MD = hashlib.sha256(id_byte).hexdigest()
    # convert bytes to string
    #CT = CT_byte.decode("ISO-8859-1")
    #stop = timeit.default_timer()
    #print('Enc Time: ', stop - start)
    #encrypt SymKey with CP-ABE PubKey
    #cpabe.encrypt(id)
    
    #rename encrypted json file to be able to read the file
    p = subprocess.call(["mv", "./testpatientCPABE/{}.txt.cpabe".format(pid), "./testpatientCPABE/enc_{}.txt".format(pid)])
    #read the encrypted json file
    with open('./testpatientCPABE/enc_{}.txt'.format(pid),'rb') as file:
        CT_byte = file.read()
    #-----Begin Signing Phase------
    #CT_byte = str.encode(CT, encoding="ISO-8859-1")
    #convert byte to string for storing in the DB
    CT = CT_byte.decode("ISO-8859-1")
    DS_R, R1, runtimeSigning = SigningPhasePerf.Sign(CT_byte,CT,certid, id_MD)

    # Form a JSON document for storing on cloud
    doc = {'MD_id': '{}'.format(id_MD), 'CT': '{}'.format(CT),
    'DS*R': '{}'.format(DS_R), 'R1': '{}'.format(R1)}
    stop = timeit.default_timer()
    runtime = stop - start
    #print(doc['CT'])
    return doc, runtime