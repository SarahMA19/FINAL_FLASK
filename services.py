import requests, json, os 
from azure.storage.blob import BlobClient, generate_blob_sas, BlobSasPermissions, BlobServiceClient
from datetime import datetime, timedelta
AZURE_STORAGE_CONNECTION_STRING='DefaultEndpointsProtocol=https;AccountName=audiofilesproject;AccountKey=DgVvagiFy7KRV6/KtSRgzVWEHG6Dry2KHTWX01/OLDrD/x/JuzjH631eFMNPIzqUWtvOkFCJbWcU+AStrPqvRw==;EndpointSuffix=core.windows.net'
myheader= {"Ocp-Apim-Subscription-Key": "5cb74fcedeb14edd8eee96bc0634288b", "Content-Type": "application/json"}
def CreateContainer(container_name):
   

    blob_service_client = BlobServiceClient.from_connection_string(conn_str=AZURE_STORAGE_CONNECTION_STRING) 
   
    try:
        container_client = blob_service_client.get_container_client(container=container_name)
        container_client.get_container_properties()
    except Exception as e:
        # print(e)
        # print("Creating container...")
        container_client = blob_service_client.create_container(container_name)
    return container_client


def upload_audio(container_name, filepath, filename):
    container_client = CreateContainer(container_name)
    with open(file=os.path.join(filepath, filename), mode="rb") as data:
        try:
             container_client.upload_blob(filepath, filename)
        except Exception as e:
            f = 10
            # print(e)
            # print("Ignoring duplicate filenames") # ignore duplicate filenames
   
    #todo: save name in db & update status - transcription table
    #return transcription record ID
    return 10
            
    

def requestTranscription(file):
    myobject ={
    'contentUrls':[file],
    'locale': 'en-US',
    'displayName': 'My Translation',
    'model': None,
    'properties': {
        'wordLevelTimestampsEnabled': True,
        'languageIdentification': {
            'candidateLocales': [
                'en-US',
                'de-DE',
                'es-ES'
            ]
        }
    }
    }
    myheader= {"Ocp-Apim-Subscription-Key": "5cb74fcedeb14edd8eee96bc0634288b", "Content-Type": "application/json"}

    res = requests.post("https://cognativeaudio.cognitiveservices.azure.com/speechtotext/v3.1/transcriptions", json=myobject, headers=myheader)
    # print(res)
    if res.ok:
        data = res.json()
        # print(data["self"])
        return data["self"]
     

    


       

def get_blob_sas(account_name,account_key, container_name, blob_name):
    sas_blob = generate_blob_sas(account_name=account_name, 
                                container_name=container_name,
                                blob_name=blob_name,
                                account_key=account_key,
                                permission=BlobSasPermissions(read=True),
                                expiry=datetime.utcnow() + timedelta(hours=24))
    return sas_blob

blob = get_blob_sas(account_name,account_key, container_name, blob_name)
requestTranscription('https://'+ account_name +'.blob.core.windows.net/' + container_name + '/' + blob_name + '?' + blob)


def getStatus(transcriptionId):
    while True:
        res = requests.get(transcriptionId, headers=myheader)
        if res.ok:
            data = res.json()
            # print(data['status'])
            if data['status'] == 'Succeeded':
                return True
           
                


def getResults(transcriptionId):
    res = requests.get(transcriptionId + "/files", headers=myheader)
    if res.ok:
        data = res.json()
        # print(data)
        words = requests.get(data['values'][0]['links']['contentUrl'], headers=myheader)
        if words.ok:
            data=words.json()
            return data['combinedRecognizedPhrases'][0]['lexical']
        

def deleteTranscription(transcriptionId):
    res = requests.delete(transcriptionId, headers=myheader)
    if res.status_code >= 400:
        print('FAILED')
    

       






def bigGirlPanties(container_name, filepath, filename):
    db_row = upload_audio(container_name, filepath, filename)
    blob = get_blob_sas(account_name,account_key, container_name, blob_name)
    transcriptionId = requestTranscription('https://'+ account_name +'.blob.core.windows.net/' + container_name + '/' + blob_name + '?' + blob)
    transcriptionStatus = getStatus(transcriptionId)
    if transcriptionStatus == False:
        print('ERROR')
        return print('ERROR, FAIL')
    else:
        realDeal = getResults(transcriptionId)
        print(realDeal)
    deleteTranscription(transcriptionId)

bigGirlPanties("test2", "/Users/sarahmartin/Desktop", "ENG_M.wav")




# person = {
#     "name": "Sarah",
#     'age' : 1234,
#     'role': 'Mom'
# }

        #Python
# for key, value in person.items():
#print(key, ':', value)

#for calue in person.values()
    #print(value)

        #Javascript
# for (let key in person) {
#     console.log(key, person[key])
# }

# const values = Object.values(person);
# for (let value of values) {
#     console.log(value)
# }