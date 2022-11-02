import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64, hashlib, random, timeit, pymongo, datetime, json, math
from random import choice
def XOR (a, b):
    if a != b:
        return 1
    else:
        return 0

def Sign(CT_byte,certid,id_MD):
    #start = timeit.default_timer()
    #hash the CT
    CT_MD = hashlib.sha256(CT_byte).hexdigest()
    CT_MD_byte = str.encode(CT_MD)
    #import pubkey
    f = open('{}_RSA_pubkey.pem'.format(certid),'r')

    pubkey = RSA.import_key(f.read())
    CT_RSA_Pubkey = PKCS1_OAEP.new(pubkey)
    #encrypt MD with RSA -> Get DS
    #print("1: ",CT_MD_byte)
    #print("OriMD: ",CT_MD_byte)
    DS_byte = CT_RSA_Pubkey.encrypt(CT_MD_byte)
    #print("DSByte:",DS_byte)
    
    #print("Length DS Byte: ",len(DS_byte))
    DS = DS_byte.decode('ISO-8859-1')
    print("DS: ",DS)
    # for i in range(len(DS)):
    #     print("DS index: ",DS[i])
    # #print("Len DS: ",len(DS))
    # DS_byte1 = str.encode(DS)
    # f = open('{}_RSA_privkey.pem'.format(certid),'r')
    # privkey = RSA.import_key(f.read())
    # CT_RSA_Privkey = PKCS1_OAEP.new(privkey)
    # #encrypt MD with RSA -> Get DS
    # MD2 = CT_RSA_Privkey.decrypt(DS_byte1)
    # #print("3: ",DS_byte1)
    # #DS1 = DS_byte1.decode('ISO-8859-1')
    # print("MD2:",MD2)


    #start = timeit.default_timer()
    #encoded_bytes = DS.encode(encoding='utf-8')
    #Convert DS to binary string
    #print("encodedbytes: ",encoded_bytes)
    DS_Binary = ''.join([bin(b)[2:] for b in DS_byte])
    #print("DS Binary: ",DS_Binary)
    #print("Len DS Bi: ",len(DS_Binary))

    # DS_split = ' '.join([DS_Binary[i:i+8] for i in range(0, len(DS_Binary), 8)])
    # ascii_string = "".join([chr(int(binary, 2)) for binary in DS_split.split(" ")])
    # print("DS1: ",ascii_string)

    #print("DS: ",int(DS_Binary,2))
    lenDSBinary = len(DS_Binary)
    
    #generate R value

    R = ''.join(choice('01') for _ in range(lenDSBinary))
    # XOR DS_Binary with R value
    
    DS_XOR_R_Binary = ""
    for i in range(len(DS_Binary)):
        temp1 = XOR(DS_Binary[i],R[i])
        DS_XOR_R_Binary += str(temp1)
    #print(DS_XOR_R_Binary)
    binary_int = int(DS_XOR_R_Binary, 2)
    # Getting the byte number
    byte_number = binary_int.bit_length() + 7 // 8
    # Getting an array of bytes
    binary_array = binary_int.to_bytes(byte_number, "big")
    #print("BA: ",binary_array)
    
    # Converting the array into ASCII text
    DS_XOR_R_text = binary_array.decode('ISO-8859-1')
    # print(len(DS_XOR_R_text))
    # binary_array_enc = CT_RSA_Pubkey.encrypt(DS_XOR_R_text)
    # print("BA: ",binary_array_enc)
    #print(DS_XOR_R_text)
    #Define constant R
    constR = "111011101110011010000100101111000101000100100101111001010000110010010000110110001111000110010001101111010100010010101110000101000101110100001001011010111100001001110111011101110101111011111011111110010010101010010001101010001000000011001001001111000100100100001001000111011001111001111110100101011111011001101101100110111100111100011100011100011010000010101010011010000011100001011011110011010010001010000010111001010001110011010010000000001001101100010001110111111101100111100000010110000101000011010110010001111000001010011001001001100001101101000101101010010010001101111111011001111111010000011010011101001100001010011111101100011010111101001001100001001100011000001011100010011111010110110100010111011100001100111000101000110110100010111100100111011001101000010100111010100010010011111010110010000111111001010001111111011001110110000001000100010011101010110011001001111011000101001111110111111110010110000111010110000100011001101001000000001101011100110100000000101110001001100000111100111000101110010011001100110110001110001110101100000111000011011010101001111010001110011110110000001101101010100111101000111001111011000"
    constR += constR
    #Get R1
    
    R1_Binary = ""
    for i in range(len(R)):
        temp1 = XOR(R[i],constR[i])
        R1_Binary += str(temp1)
    #print("R1: ",R1_Binary)
    #print(len(R1_Binary))
    #Transform binary to text
    binary_int = int(R1_Binary, 2)
    # Getting the byte number
    byte_number = binary_int.bit_length() + 7 // 8
    # Getting an array of bytes
    binary_array = binary_int.to_bytes(byte_number, "big")
    R1_text = binary_array.decode('ISO-8859-1')
    #print("R1: ",R1_text)
    #stop = timeit.default_timer()
    #print('DSXORR & R1 Time: ', stop - start)

    #-------Audit Log part---------
    client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
    mydb = client['EncryptedMTR']
    mycol = mydb['AuditLog']
    
    #get private key from local, convert to string for storing on database
    f = open('{}_RSA_privkey.pem'.format(certid),'r')
    privkey = RSA.import_key(f.read())
    privkey_byte = privkey.exportKey("PEM")
    privkey_string = privkey_byte.decode('ISO-8859-1')
    
    curtimedate = str(datetime.datetime.now())
    update = {'certid': '{}'.format(certid), 'PrivKey': '{}'.format(privkey_string), 'DS*R': '{}'.format(DS_XOR_R_Binary), 'R1': '{}'.format(R1_Binary)}
    existedLog = mycol.find_one({'MD_id': id_MD})
    #stop = timeit.default_timer()
    #print('Signing Time: ', stop - start)
    # if  type(existedLog) != type(None):  #If the audit log of file is existed then update the log
    #     existedLog[curtimedate] = update
    #     mycol.delete_one({'MD_id': id_MD})
    #     mycol.insert_one(existedLog)
    #     #existedLog[curtimedate] = update
    # else: #There is no audit log for this document
    #     log = {'MD_id': '{}'.format(id_MD), '{}'.format(curtimedate): update}
    #     mycol.insert_one(log)
    return DS_XOR_R_Binary, R1_Binary