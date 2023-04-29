import requests, json, os
from flask import Blueprint, request
from azure.storage.blob import BlobClient, generate_blob_sas, BlobSasPermissions, BlobServiceClient
from datetime import datetime, timedelta





api = Blueprint('api', __name__)


myheader= {"Ocp-Apim-Subscription-Key": "5cb74fcedeb14edd8eee96bc0634288b", "Content-Type": "application/json"}

def CreateContainer(container_name):
   

    blob_service_client = BlobServiceClient.from_connection_string(conn_str=os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
   
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

blob = get_blob_sas(os.getenv('ACCOUNT_NAME'),os.getenv('ACCOUNT_KEY'), os.getenv('CONTAINER_NAME'), os.getenv('BLOB_NAME'))
requestTranscription('https://'+ os.getenv('ACCOUNT_NAME') +'.blob.core.windows.net/' +os.getenv('CONTAINER_NAME')+ '/' + os.getenv('BLOB_NAME') + '?' + blob)


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
    

       
@api.route('/api', methods=['GET','POST'])
def bigGirlPanties():
    container_name=request.json["container_name"]
    filename=request.json["filename"]
    blob = get_blob_sas(os.getenv('ACCOUNT_NAME'),os.getenv('ACCOUNT_KEY'), container_name, filename)
    transcriptionId = requestTranscription('https://'+ os.getenv('ACCOUNT_NAME') +'.blob.core.windows.net/' + container_name + '/' + filename + '?' + blob)
    transcriptionStatus = getStatus(transcriptionId)
    if transcriptionStatus == False:
        print('ERROR')
        return print('ERROR, FAIL')
    else:
        realDeal = getResults(transcriptionId)
        print(realDeal)
    deleteTranscription(transcriptionId)
    return realDeal

@api.route('/sasurl', methods=['GET', 'POST'])
def sasUrl():
    print('sasUrl')
    # container_name=request.json["container_name"]
    # filename=request.json["filename"]
    # CreateContainer(container_name)
    # blob = get_blob_sas(os.getenv('ACCOUNT_NAME'),os.getenv('ACCOUNT_KEY'), container_name, filename)
    return 'hello'
    



