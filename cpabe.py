import subprocess
#enc the symkey with policy dataowner or medicalstaff
#id = "p0000"
def encrypt_key(id):
    p = subprocess.call(["cpabe-enc","-k", "pub_key", "./Symkeys/{}_key.txt".format(id), "dataowner"])
def encrypt_text(id):
    p = subprocess.call(["cpabe-enc","-k", "pub_key", "./testpatientCPABE/{}.txt".format(id), "dataowner"])
#dec the symkey with dataowner's private key
# def decrypt_key(id):
#     p = subprocess.call(["cpabe-dec", "pub_key", "DO00000_priv_key", "./Symkeys/{}_key.txt.cpabe".format(id)])
def decrypt(file):
    p = subprocess.call(["cpabe-dec", "-k","pub_key", "./cpabe_keys/DO00000_priv_key", "{}".format(file)])
def keygen(id,policy):
    p = subprocess.call(["cpabe-keygen", "-o","./cpabe_keys/{}_priv_key".format(id),"pub_key","cpabe-0.11/master_key", policy])
#p = subprocess.call(["mv", "{}_key.txt.cpabe".format(id), "{}_key.txt".format(id)])
decrypt("./patientCloud/p01000.txt.cpabe")
#encrypt_text("p00010")
# policyarray = ["dataowner","medicalstaff","a","b","c","d","e","f","g","h"]
# inputpolicy = ""
# for i in range(10):
#     policy = policyarray[i]+" "
#     inputpolicy += policy
#     keygen("DO000{}".format(i),"inputpolicy")
#     #print(inputpolicy)
#keygen("DO00000","dataowner")
#decrypt("./SymkeyCloud/p0000_key.txt.cpabe")