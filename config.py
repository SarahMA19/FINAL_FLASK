import os

basedir = os.path.abspath(os.path.dirname(__name__))

class Config():
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    API_KEY=os.environ.get('API_KEY')
    SERVICE_REGION=os.environ.get('SERVICE_REGION')
    ENDPOINT=os.environ.get('ENDPOINT')
    ACCOUNT_NAME  = os.environ.get('ACCOUNT_NAME')
    ACCOUNT_KEY = os.environ.get('ACCOUNT_KEY')
    CONTAINER_NAME = os.environ.get('CONTAINER_NAME')
    BLOB_NAME =os.environ.get('BLOB_NAME') 
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
   
    
