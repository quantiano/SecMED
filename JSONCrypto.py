
from cryptography.fernet import Fernet
import json
import hashlib, rsa
import SigningPhase
import os, subprocess, cpabe, keygenerator, timeit
def encryptjson(data_string,certid):
    start = timeit.default_timer()
    #--------Begin Encryption Phase----------
    #convert string to JSON
    
    data_json = json.loads(data_string)
    #store name in name variable
    id = data_json["id"]
    #convert string to byte for encryption
    data_byte = str.encode(data_string)
    # convert pname to byte format
    id_byte = str.encode(id)
    #generate Symkey
    symkey = keygenerator.symkeygenerator(id)
    # with open('{}_key.txt'.format(id),'wb') as file:
    #     file.write(symkey)
    # this encrypts the data read from your json and stores it in 'encrypted'
    #start = timeit.default_timer()
    CT_byte= Fernet(symkey).encrypt(data_byte)
    
    #hash patient id
    id_MD = hashlib.sha256(id_byte).hexdigest()
    # convert bytes to string
    CT = CT_byte.decode("ISO-8859-1")
    #stop = timeit.default_timer()
    #print('Enc Time: ', stop - start)
    #encrypt SymKey with CP-ABE PubKey
    cpabe.encrypt_key(id)
    
    #rename encrypted symkey file to be able to read the file
    p = subprocess.call(["mv", "./Symkeys/{}_key.txt.cpabe".format(id), "./Symkeys/{}_key.txt".format(id)])
    
    #read the encrypted SymKey
    with open('./Symkeys/{}_key.txt'.format(id),'rb') as file:
        enc_Symkey = file.read()

    #convert byte to string for storing in the DB
    enc_Symkey = enc_Symkey.decode("ISO-8859-1")

    #rename the symkey file
    p = subprocess.call(["mv", "./Symkeys/{}_key.txt".format(id), "./Symkeys/{}_key.txt.cpabe".format(id)])

    #Decrypt the local Symkey
    cpabe.decrypt("./Symkeys/{}_key.txt.cpabe".format(id))

    #-----Begin Signing Phase------
    DS_XOR_R, R1 = SigningPhase.Sign(CT_byte,CT,certid, id_MD)
    
    # Form a JSON document for storing on cloud
    doc = {'MD_id': '{}'.format(id_MD), 'CT': '{}'.format(CT), 'enc_SK': '{}'.format(enc_Symkey),
    'DS*R': '{}'.format(DS_XOR_R), 'R1': '{}'.format(R1)}
    stop = timeit.default_timer()
    print('Enc Time: ', stop - start)
    #print(doc['enc_SK'])
    return doc

# def decryptjson(key,doc):
#     #start = timeit.default_timer()
#     #store the stored ciphertext in CT
#     try:
#         CT = doc['CT']
#     except(TypeError):
#         print("Cannot find the document")
#         return False
#     #store the original MAC to origmac

#     #convert string to byte
#     CTbytes = str.encode(CT)
#     #decrypt the ciphertext
    
#     with open('dataOwner.key','rb') as file:
#         check_key = file.read()

#     fernet = Fernet(check_key)
#     decdoc = fernet.decrypt(CTbytes)
#     #convert the decrypted byte to string
#     decdoc = decdoc.decode("utf-8")
    
#     #convert string to json format
#     decdoc = json.loads(decdoc)
    
#     #stop = timeit.default_timer()
#     #print('Dec Time: ', stop - start)
#     return decdoc
#test code

# with open('/home/nontawat/SecMED/Patients/p0000_Intira Preecha.json','r') as file:
#         pdoc = file.read()
# #pdoc_string = json.dumps(pdoc)
# #print(type(pdoc_string))
# encryptjson(pdoc)