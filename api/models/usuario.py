from api.models.db import get_usuarios_collection

def read_user(username):
    usuarios = get_usuarios_collection()
    return usuarios.find_one({'username': username})
