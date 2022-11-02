
from multiprocessing.sharedctypes import Value
from cryptography.fernet import Fernet
import json
import JSONCrypto
import pymongo, time
import keygenerator
def insertpatient():
    # connect to MongoDB
    client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
    mydb = client['EncryptedMTR']
    mycol = mydb['patient']
    """
    doc_count = mycol.count_documents({})
    patient_id_num = str(doc_count)
    while len(patient_id_num) < 4:
        patient_id_num = "0" + patient_id_num
    patient_id = "p" + patient_id_num
    print(patient_id)

    entername()
    doc = {"id":"{}".format(patient_id),
        "name":"{}".format(name),
        "National ID":"{}".format(NationalID),
        "Address of residence":"{}".format(address),
        "Phonenum":"{}".format(Phonenum),
        "Email":"{}".format(email),
        "Name of family member":"{}".format(fam_name),
        "Contact of family member":"{}".format(fam_contact),
        "dob":"{}".format(dob),
        "nationality":"{}".format(nationality),
        "height": "{}".format(height),
        "weight":"{}".format(weight),
        "bloodtype":"{}".format(bloodtype),
        "Insurance Provider":"{}".format(insurance_prov),
        "Insurance ID":"{}".format(insurance_ID),
        "Responsible Physician":"{}".format(doctor),
        "Health-related behavior":"{}".format(health_relate),
        "Past medical records":"{}".format(Past_med),
        "Family history":"{}".format(fam_hist),
        "Allergies":"{}".format(allergies),
        "Data of addmission":"{}".format(datead),
        "Vaccination":"{}".format(vaccinelistJson),
        "Room":"{}".format(room)
        }
    """
    certid = "DO0000"
    with open('./Patients/p0009.json','r') as file:
        doc = file.read()
    doc = json.loads(doc)
    doc_string = json.dumps(doc)
        
    doc_encrypted = JSONCrypto.encryptjson(doc_string,certid)

    # id = mycol.insert_one(doc_encrypted)
    # print("The document has been saved (id: {}).".format(id.inserted_id))
#     confirm = input("Do you want to insert the encrypted document? (y/n): ")
#     if confirm == "y":
#         id = mycol.insert_one(doc_encrypted)
#         print("The document has been saved (id: {}).".format(id.inserted_id))
#         #insertpatient() #go back to the top
#     #elif confirm == "n":
#     #    insertpatient() #go back to the top
#     elif confirm == "n":
#         exit()
#     else:
#         print("Invalid command, please try again")

# def entername():
#     global name
#     name = input("Enter name: ")
#     if name == "exit":
#         exit()
#     elif name == "back":
#         return "back"
#     enterNationalID()
        
# def enterNationalID():
#     global NationalID
#     NationalID = input("Enter National ID: ")
#     if NationalID == "exit":
#         exit()
#     elif NationalID == "back":
#         entername()
#     enterAddress()

# def enterAddress():
#     global address
#     address = input("Address of residence: ")
#     if address == "exit":
#         exit()
#     elif address == "back":
#         enterAddress()
#     enterPhonenum()

# def enterPhonenum():
#     global Phonenum
#     Phonenum = input("Enter phone number: ")
#     if Phonenum == "exit":
#         exit()
#     elif Phonenum == "back":
#         enterPhonenum()
#     enterEmail()

# def enterEmail():
#     global email
#     email = input("Email: ")
#     if email == "exit":
#         exit()
#     elif email == "back":
#         enterEmail()
#     enterFamname()

# def enterFamname():
#     global fam_name
#     fam_name = input("Name of family member: ")
#     if fam_name == "exit":
#         exit()
#     elif fam_name == "back":
#         enterEmail()
#     enterFamnum()

# def enterFamnum():
#     global fam_contact
#     fam_contact = input("Contact of family member: ")
#     if fam_contact == "exit":
#         exit()
#     elif fam_contact == "back":
#         enterFamname()
#     enterdob()

# def enterdob():
#     global dob
#     dob = input("Date of birth: ")
#     if dob == "exit":
#         exit()
#     elif dob == "back":
#         enterFamnum()
#     enterNationality()

# def enterNationality():
#     global nationality
#     nationality = input("Nationality: ")
#     if nationality == "exit":
#         exit()
#     elif nationality == "back":
#         enterdob()
#     enterHeight()

# def enterHeight():
#     global height
#     height = input("Height: ")
#     if height == "exit":
#         exit()
#     elif height == "back":
#         enterNationality()
#     enterWeight()

# def enterWeight():
#     global weight
#     weight = input("Weight: ")
#     if weight == "exit":
#         exit()
#     elif weight == "back":
#         enterHeight()
#     enterBloodtype()

# def enterBloodtype():
#     global bloodtype
#     bloodtype = input("Bloodtype: ")
#     if bloodtype == "exit":
#         exit()
#     elif bloodtype == "back":
#         enterWeight()
#     enterInsprovider()

# def enterInsprovider():
#     global insurance_prov
#     insurance_prov = input("Insurance provider: ")
#     if insurance_prov == "exit":
#         exit()
#     elif insurance_prov == "back":
#         enterBloodtype()
#     enterInsID()

# def enterInsID():
#     global insurance_ID
#     insurance_ID = input("Insurance ID : ")
#     if insurance_ID == "exit":
#         exit()
#     elif insurance_ID == "back":
#         enterInsprovider()
#     enterdoctor()

# def enterdoctor():
#     global doctor
#     doctor = input("Responsible physician : ")
#     if doctor == "exit":
#         exit()
#     elif doctor == "back":
#         enterInsID()
#     enterHealth_related_behavior()

# def enterHealth_related_behavior():
#     global health_relate
#     health_relate = input("Health-related behavior : ")
#     if health_relate == "exit":
#         exit()
#     elif health_relate == "back":
#         enterdoctor()
#     enterPastMedRecord()
        
# def enterPastMedRecord():
#     global Past_med
#     Past_med = input("Past medical records: ")
#     if Past_med == "exit":
#         exit()
#     elif Past_med == "back":
#         enterHealth_related_behavior()
#     enterFamHistory()

# def enterFamHistory():
#     global fam_hist
#     fam_hist = input("Family history: ")
#     if fam_hist == "exit":
#         exit()
#     elif fam_hist == "back":
#         enterPastMedRecord()
#     enterAllergy()

# def enterAllergy():
#     global allergies
#     allergies = input("Allergies: ")
#     if allergies == "exit":
#         exit()
#     elif allergies == "back":
#         enterFamHistory()
#     enterDateofAdmission()   

# def enterDateofAdmission():
#     global datead
#     datead = input("Date of admission: ")
#     if datead == 'exit':
#         exit()
#     elif datead == 'back':
#         enterAllergy()
#     entervaccine()

# def entervaccine():
#     global vaccinelistJson
#     vaccinelist = []
#     while(True):
#         try:
#             vaccineNum = int(input("Enter number of received vaccine: "))
#             break
#         except(ValueError):
#             print("Invalid type of input")
#     if vaccineNum == 'exit':
#         exit()
#     elif vaccineNum == 'back':
#         enterAllergy()
#     for i in range(vaccineNum):
#         vaccinename = input("Enter vaccine name ({}): ".format(i+1))
#         vaccinelist.append("Received vaccine({})".format(i+1))
#         vaccinelist.append(vaccinename)
#     vaccinelistJson = {vaccinelist[i]: vaccinelist[i + 1] for i in range(0, len(vaccinelist), 2)}
#     enterRoom()

# def enterRoom():
#     global room
#     room = input("Room: ")
#     if room == 'exit':
#         exit()
#     elif room == 'back':
#         entervaccine()

insertpatient()