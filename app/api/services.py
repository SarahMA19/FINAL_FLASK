import requests, json, os
from flask import Blueprint, request
from azure.storage.blob import BlobClient, generate_account_sas, BlobSasPermissions, BlobServiceClient, ResourceTypes
from datetime import datetime, timedelta
from ..models import db, User, Transcription


api = Blueprint('api', __name__, url_prefix='/api')


myheader= {"Ocp-Apim-Subscription-Key": "5cb74fcedeb14edd8eee96bc0634288b", "Content-Type": "application/json"}


##### HELPER FUNCTIONS #####

def CreateContainer(container_name):
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
    try:
        container_client = blob_service_client.get_container_client(container=container_name)
        container_client.get_container_properties()
    except Exception as e:
        container_client = blob_service_client.create_container(container_name)
    return container_client

            
    
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
     

def get_blob_sas(account_name,account_key):
    sas_blob = generate_account_sas(account_name=account_name, 
                                account_key=account_key,
                                resource_types=ResourceTypes(service=True, container=True, object=True),
                                permission=BlobSasPermissions(read=True, add =True, write=True),
                                expiry=datetime.utcnow() + timedelta(minutes=15))
    return sas_blob



def getStatus(transcriptionId):
    while True:
        res = requests.get(transcriptionId, headers=myheader)
        if res.ok:
            data = res.json()
            if data['status'] == 'Succeeded':
                return True
           

def getResults(transcriptionId):
    res = requests.get(transcriptionId + "/files", headers=myheader)
    if res.ok:
        data = res.json()
        words = requests.get(data['values'][0]['links']['contentUrl'], headers=myheader)
        if words.ok:
            data=words.json()
            return data['combinedRecognizedPhrases'][0]['lexical']
                

def deleteTranscription(transcriptionId):
    res = requests.delete(transcriptionId, headers=myheader)
    if res.status_code >= 400:
        print('FAILED')
    
##### ROUTES ######
       
@api.post('/transcription')
def createTranscriptionWorkFlow():
    container_name=request.json["container_name"]
    filename=request.json["filename"]
    uid=request.json["uid"]
    duration=request.json["duration"]
    blob = get_blob_sas(os.getenv('ACCOUNT_NAME'),os.getenv('ACCOUNT_KEY'))
    transcriptionId = requestTranscription('https://'+ os.getenv('ACCOUNT_NAME') +'.blob.core.windows.net/' + container_name + '/' + filename + '?' + blob)
    transcriptionStatus = getStatus(transcriptionId)
    if transcriptionStatus == False:
        print('ERROR')
        return print('ERROR, FAIL')
    else:
        realDeal = getResults(transcriptionId)
    transcriptiondb = Transcription(user_uid=uid, body=realDeal, paid=False, filename=filename, audio_length=duration).create()   
    deleteTranscription(transcriptionId)
    return realDeal


@api.post('/sasurl')
def sasUrl():
    container_name=request.json["container_name"]
    CreateContainer(container_name)
    blob = get_blob_sas(os.getenv('ACCOUNT_NAME'),os.getenv('ACCOUNT_KEY'))
    return blob


@api.post('/users')
def create_user():
    uid = request.json.get("uid")
    name = request.json.get("displayName")
    email = request.json.get("email")
    container_name = request.json.get("container_name")
    user = User.query.filter_by(uid=uid).first()
    if user:
        return {'status': 'ok', 'message': 'Unable to create user. User already exists', 'user': user.to_dict()}
    user = User(uid=uid, name=name, email=email, container_name=container_name)
    user.create()
    return {'status': 'ok', 'user': user.to_dict()}

@api.get('/users')
def get_users():
    users = User.query.all()
    if not users:
        return {'status': 'not ok', 'message': 'Unable to get users'}
    return {'status': 'ok', 'users': [user.to_dict() for user in users]}


@api.get('/transcriptions')
def get_transcription():
    user_uid = request.args.get('uid')
    if user_uid == 'undefined':
        return "undefined"
    else:
        transcriptions = Transcription.query.filter(Transcription.user_uid==user_uid).order_by(Transcription.created_at.desc()).all()
        if not transcriptions:
            return {'status': 'not ok', 'message': 'Unable to get transcription'}
        for t in transcriptions:
            t.body = t.body[0:30]
        return {'status': 'ok', 'transcription': [transcription.to_dict() for transcription in transcriptions]}
    

@api.delete('/transcriptions/<int:id>')
def delete_transcription(id):
    transcription = Transcription.query.get(id)
    if not transcription:
        return {'status': 'not ok', 'message': 'Unable to delete transcription'}
    transcription.delete()
    return {'status': 'ok'}

@api.get('/transcriptions/<int:id>')
def get_transcription_id(id):
    transcription = Transcription.query.get(id)
    if not transcription:
        return {'status': 'not ok', 'message': 'Unable to get transcription'}
    return transcription.body











