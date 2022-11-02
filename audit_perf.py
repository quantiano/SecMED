import base64
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64, hashlib, random, timeit, pymongo, datetime, json, math
from random import choice
import binascii
from base64 import b64decode,b64encode
from ast import literal_eval
from sympy import dsolve
client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
#client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client['EncryptedMTR']
Data_owner_list = []
mycol_audit = mydb['AuditLogPerf']
mycol_patient = mydb['patientperf160']
item_details = mycol_audit.find()
templist = []
thislist = []
patient_list = []
runtime_list = []

prevLeastRuntime = 0
for i in range (0,81):
    if i < 10:
        temp = "p000" + str(i)
        patient_list.append(temp)
    elif (i < 100) and (i >= 10):
        temp = "p00" + str(i)
        patient_list.append(temp)
    elif (i <1000 ) and (i >= 100):
        temp = "p0" + str(i)
        patient_list.append(temp)
#print(patient_list)

array_request = [1,5,10,20,40,80]
for k in array_request:
    for k1 in range(10):
        runtime_total = 0
        for j in range (0,k): 
            patient = patient_list[j]
            #print(patient)
            patient= str.encode(patient)
            #print(patient)
            hash_patient = hashlib.sha256(patient).hexdigest()
            #print(hash_patient)
            document_audit = mycol_audit.find_one({'MD_id': hash_patient})
            #document_audit = mycol_audit.find_one({'MD_id': "a4d5e07e23b14fef41dbb972621cf67d2fc47e6614f6c61bc0b598ac474343c5"})
            times = 0
            timestamp = ''
            for i in document_audit:
                if (i[0:2] == "20"):
                    
                    #print(No)
                    timestamp = timestamp+i
                    #print(timestamp)
                    R1 = document_audit[timestamp]['R1']
                    R1 = literal_eval(R1)
                    #print("R1 =", R1)
                    constR = [27, 40, 6, 9, 68, 107, 123, 49, 22, 31, 127, 79, 85, 34, 71, 26, 0, 115, 121, 110, 74, 5, 36, 63, 73, 76, 39, 112, 111, 53, 70, 4, 65, 48, 126, 117, 52, 109, 67, 35, 95, 72, 94, 86, 50, 10, 118, 105, 90, 33, 102, 88, 113, 32, 61, 92, 122, 29, 16, 28, 119, 1, 114, 83, 98, 18, 77, 62, 45, 80, 38, 8, 42, 99, 13, 69, 96, 17, 20, 91, 25, 106, 19, 30, 47, 15, 3, 37, 56, 41, 46, 124, 87, 75, 89, 120, 100, 81, 97, 11, 60, 21, 104, 59, 93, 43, 66, 55, 78, 101, 64, 82, 12, 116, 7, 44, 23, 14, 58, 2, 51, 24, 108, 103, 57, 84, 54, 125]
                    
                    #---reverse
                    start = timeit.default_timer()
                    R = []
                    for i in range(128):
                        j = 0
                        while constR[j] != i:
                            #print(constR[j])
                            j+=1
                        #print("index:",j)
                        R.append(R1[j])
                    stop = timeit.default_timer()
                    runtime_R_constR = stop-start
                    #print("testR: ",testR)
                    #print("R = ",R)
                    DS_R = document_audit[timestamp]['DS*R']
                    #print(DS_R)
                    start = timeit.default_timer()
                    DS = ""
                    for i in range(128):
                        j = 0
                        while R[j] != i:
                            #print(constR[j])
                            j+=1
                        #print("index:",j)
                        DS+=DS_R[j]
                    stop = timeit.default_timer()
                    runtime_DSR_R = stop-start
                    #print("testR: ",testR)
                    #print("DS = ",DS)

                    # get private key
                    audit_priv = document_audit[timestamp]['PrivKey']
                    #print('audit_priv =', audit_priv)
                    
                    certid = document_audit[timestamp]['certid']
                    #print('certid =',certid)
                    #print(certid)
                    with open('./RSAKeyCloud/{}_RSA_privkey.pem'.format(certid),'w') as file:
                        file.write(audit_priv)
                    f = open('./RSAKeyCloud/{}_RSA_privkey.pem'.format(certid),'r')
                    privkey = RSA.import_key(f.read())
                    CT_RSA_Privkey = PKCS1_OAEP.new(privkey)
                    #encrypt MD with RSA -> Get DS
                    DS_byte = str.encode(DS, encoding = 'ISO-8859-1')
                    #print(len(DS_byte))
                    #encrypt MD with RSA -> Get DS
                    MD = CT_RSA_Privkey.decrypt(DS_byte)
                    MD = MD.decode('ISO-8859-1')
                    #print("MD from reversing=",MD)
                    #---------------------------------------------------------------------
                    # patientid = 'p0000'
                    # patientid= str.encode(patientid)
                    # hash_patientid = hashlib.sha256(patientid).hexdigest()
                    # #print("hash patient ID=", hash_patientid)
                    # document_patient = mycol_patient.find_one({'MD_id': hash_patient})
                    # patient_CT = document_patient['CT']
                    patient_CT = document_audit[timestamp]['CT']
                    patient_CT_byte = str.encode(patient_CT)
                    hash_patient_CT = hashlib.sha256(patient_CT_byte).hexdigest()
                    #print("hash patient CT= ",hash_patient_CT)
                    #----------------------------------------------------------------------
                    # if (MD == hash_patient_CT):
                    #     print("true")
                    # else:
                    #     print("false")
                    timestamp = ''
                    runtime_shuffle = runtime_R_constR + runtime_DSR_R
                    runtime_total = runtime_total + runtime_shuffle
                    runtime_list.append(runtime_total)
    runtime_list.sort()
    for i1 in range(len(runtime_list)):
        if runtime_list[i1] > prevLeastRuntime:
            #print('EncTime({}): '.format(i), runtime_list[i1])
            print('Time({})(ms): '.format(k), runtime_list[i1]*1000)
            prevLeastRuntime = runtime_list[i1]
            break