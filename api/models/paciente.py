from api.models.db import get_pacientes_collection
from bson.objectid import ObjectId

def create_paciente(patient):
    pacientes = get_pacientes_collection()
    return str(pacientes.insert_one(patient).inserted_id)

def read_paciente(paciente_id):
    try:
        paciente_id = str(paciente_id)
        object_id = ObjectId(paciente_id)
    except Exception as e:
        return None
    pacientes = get_pacientes_collection()
    return pacientes.find_one({'_id': object_id})

def read_paciente_by_cpf(cpf):
    pacientes = get_pacientes_collection()
    return pacientes.find_one({'cpf': cpf})

def read_pacientes():
    pacientes = get_pacientes_collection()
    return list(pacientes.find())

def update_paciente(paciente):
    pacientes = get_pacientes_collection()
    return pacientes.update_one({'_id': ObjectId(paciente.get("_id"))}, {'$set': paciente})

def delete_paciente(paciente_id):
    pacientes = get_pacientes_collection()
    return pacientes.delete_one({'_id': ObjectId(paciente_id)})

