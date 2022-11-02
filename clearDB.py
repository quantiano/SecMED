
import pymongo

client = pymongo.MongoClient("mongodb+srv://Nontawat:iS1sKbQnyLO6CWDE@section1.oexkw.mongodb.net/section1?retryWrites=true&w=majority")
mydb = client['EncryptedMTR']
mycol = mydb['patientcpabe']
mycol.delete_many({})

# mycol = mydb['AuditLogPerf']
# mycol.delete_many({})