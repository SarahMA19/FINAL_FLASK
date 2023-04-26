import requests, json, os
from azure.storage.blob import BlobClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta




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
    # print(json.dumps(myobject))
    myheader= {"Ocp-Apim-Subscription-Key": "5cb74fcedeb14edd8eee96bc0634288b", "Content-Type": "application/json"}

    res = requests.post("https://cognativeaudio.cognitiveservices.azure.com/speechtotext/v3.1/transcriptions", json=myobject, headers=myheader)
    # print(res)
    if res.ok:
        data = res.json()
        # print(data)
       
account_name = "audiofilesproject" 
account_key = "22pd8D9ByK9cQCb2Na+4e35K2WemzEoLPu917yKgCUnpEhllm8cdvx6TMvbkYQNQUYErJROUPGzL+AStZyMRZA=="
container_name = "test2"
blob_name = "ENG_M.wav" 


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



    