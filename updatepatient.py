
from cryptography.fernet import Fernet
import pymongo
import json
import os
import findDoc,SigningPhase
import JSONCrypto


def updatePatient(pid,certid):
    client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
    db = client['EncryptedMTR']
    patientcol = db['patient']

    wanteddoc,id_MD = findDoc.findDoc(pid)
    if wanteddoc == "":
        print("The wanted document is not found, please try again")
        exit()
    #print(type(wanteddoc))
    while(True):
        #print(wanteddoc.id)
        edit_attr = input("Enter attribute you want to edit: ".format(pid))
        if edit_attr in wanteddoc:
            while(True):
                new_val = input("Enter the new value of {}: ".format(edit_attr))
                if new_val == "exit":
                    exit()
                elif new_val=="back":
                    break
                else:
                    #apply new value to the selected attribute
                    #origName = wanteddoc["name"] 
                    wanteddoc[edit_attr] = new_val

                    #covert the edited document to string
                    edited_wanteddoc_string = json.dumps(wanteddoc)
                    #edited_wanteddoc_string_sorted = json.dumps(wanteddoc, indent = 6)

                    #reindent the edited document
                    edited_wanteddoc_sorted = json.dumps(wanteddoc, indent = 6)

                    #print the results
                    print("Edited {}'s document: \n{}".format(pid,edited_wanteddoc_sorted))
                    #print("Encrypted edited {}'s document: \n{}".format(pid,encrypted_edited_wanteddoc_sorted))

                    #update to the database
                    while(True): #If user input the unexpected command then ask again
                        confirm = input("Do you want to apply change? (y/n/exit): ")
                        if confirm == "y":
                            try:
                                #encrypt the edited document
                                encrypted_edited_wanteddoc = JSONCrypto.encryptjson(edited_wanteddoc_string,certid)
                                patientcol.delete_one(wanteddoc)
                                patientcol.insert_one(encrypted_edited_wanteddoc)
                                # #delete original local file name
                                # f = open('./section{}-patient/{}_{}.json'.format(patientdb[7],pid,origName), 'w') #delete local file
                                # f.close()
                                # os.remove(f.name)
                                # with open('./section{}-patient/{}_{}.json'.format(patientdb[7],pid,wanteddoc["name"]),'w') as file:
                                #     file.write(edited_wanteddoc_string_sorted)
                                
                                print("The document has been saved to {}".format(patientcol.name))
                                
                            except(pymongo.http.ServerError):
                                print("Cannot save the document")
                            break
                        elif confirm == "n":
                            break
                        elif confirm == "exit":
                            exit()
                        else:
                            print("Invalid command, please try again")
                    if confirm in ("y","n"):
                        break
        elif edit_attr=="back":
            break
        elif edit_attr == "exit":
            exit()
        elif edit_attr not in wanteddoc:
            print("Invalid attribute, please try again")

#testing the code
updatePatient("p0000", "MS0000")