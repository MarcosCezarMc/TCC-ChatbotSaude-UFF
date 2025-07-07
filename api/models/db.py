from flask import current_app, g
from pymongo import MongoClient


def get_db():
    if 'db' not in g:
        g.client = MongoClient(current_app.config['MONGO_URI'])
        g.db = g.client[current_app.config['MONGO_DBNAME']]
    return g.db

def get_pacientes_collection():
    db = get_db()
    return db['pacientes']

def get_exames_collection():
    db = get_db()
    return db['exames']

def get_usuarios_collection():
    db = get_db()
    return db['usuarios']

def get_chaves_servico_collection():
    db = get_db()
    return db['chaves_servico']
