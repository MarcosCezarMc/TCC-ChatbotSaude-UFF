from api.models.db import get_chaves_servico_collection

def read_service_key(service):
    chaves_servico = get_chaves_servico_collection()
    return chaves_servico.find_one({'servico': service})
