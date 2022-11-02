import json
with open('./Patient160/p0000.json','r') as file:
    doc = file.read()
doc = json.loads(doc)
for i in range(1,161):
    j = str(i)
    while(len(j) < 4):
        j = "0"+ j
    # while(len(certid) < 5):
    #     certid = "0" + certid
    # certid = "DO" + certid
    # print(certid)
    #print(j)
    id = "p"+j
    doc["id"] = "p{}".format(j)
    #print(doc['id'])

    doc_string = json.dumps(doc)
    with open('./Patient160/{}.json'.format(id),'w') as file:
        file.write(doc_string)
