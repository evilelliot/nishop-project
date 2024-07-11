import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mi-secreto-es-queteamomucho1998'
    SESSION_TYPE = 'filesystem'
