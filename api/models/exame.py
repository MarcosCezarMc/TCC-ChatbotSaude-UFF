from api.models.db import get_exames_collection
from bson.objectid import ObjectId

def create_exame(exame):
    exames = get_exames_collection()
    return str(exames.insert_one(exame).inserted_id)

def read_exame(exame_id):
    try:
        exame_id = str(exame_id)
        object_id = ObjectId(exame_id)
    except Exception as e:
        return None
    exames = get_exames_collection()
    return exames.find_one({'_id': object_id})

def read_exames():
    exames = get_exames_collection()
    return list(exames.find())

def read_exames(paciente_id):
    exames = get_exames_collection()
    try:
        object_id = ObjectId(paciente_id)
        query = {'paciente_id': object_id}
    except Exception:
        return None
    return list(exames.find(query))

def update_exame(exame):
    exames = get_exames_collection()
    return exames.update_one({'_id': ObjectId(exame.get("_id"))}, {'$set': exame})

def delete_exame(exame_id):
    exames = get_exames_collection()
    return exames.delete_one({'_id': ObjectId(exame_id)})
