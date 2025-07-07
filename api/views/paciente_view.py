def serialize_paciente(paciente):
    endereco = paciente.get('endereco') or None
    rua = numero = bairro = cidade = estado = cep = complemento = None
    if endereco:
        rua = endereco.get('rua') or None
        numero = endereco.get('numero') or None
        bairro = endereco.get('bairro') or None   
        cidade = endereco.get('cidade') or None
        estado = endereco.get('estado') or None   
        cep = endereco.get('cep') or None
        complemento = endereco.get('complemento') or None

    confirmacao = paciente.get('confirmacao') or None
    confirmacao_nome = confirmacao_cpf = confirmacao_telefone = confirmacao_email = confirmacao_data_nascimento = confirmacao_endereco = confirmacao_quem = confirmacao_data = None 
    confirmacao_rua = confirmacao_numero = confirmacao_bairro = confirmacao_cidade = confirmacao_estado = confirmacao_cep = confirmacao_complemento = None
    if confirmacao:
        confirmacao_nome = confirmacao.get('nome') or None
        confirmacao_cpf = confirmacao.get('cpf') or None
        confirmacao_telefone = confirmacao.get('telefone') or None
        confirmacao_email = confirmacao.get('email') or None
        confirmacao_data_nascimento = confirmacao.get('data_nascimento') or None
        confirmacao_endereco = confirmacao.get('endereco') or None
        if confirmacao_endereco:
            confirmacao_rua = confirmacao_endereco.get('rua') or None
            confirmacao_numero = confirmacao_endereco.get('numero') or None
            confirmacao_bairro = confirmacao_endereco.get('bairro') or None
            confirmacao_cidade = confirmacao_endereco.get('cidade') or None
            confirmacao_estado = confirmacao_endereco.get('estado') or None
            confirmacao_cep = confirmacao_endereco.get('cep') or None
            confirmacao_complemento = confirmacao_endereco.get('complemento') or None
        confirmacao_quem = confirmacao.get('quem_confirmou') or None
        confirmacao_data = confirmacao.get('data_confirmacao') or None
        
    exames = paciente.get('exames') or []
    exames = [str(exame) for exame in exames]
    proxima_interacao = str(paciente.get('proxima_interacao')) if paciente.get('proxima_interacao') else None
    ultima_interacao = str(paciente.get('ultima_interacao')) if paciente.get('ultima_interacao') else None
    canal_contato = paciente.get('canal_contato') or None

    return {
        'id': str(paciente.get('_id')),
        'nome': str(paciente.get('nome')),
        'confirmacao_nome': str(confirmacao_nome) if confirmacao_nome else None,
        'cpf': paciente.get('cpf'),
        'confirmacao_cpf': confirmacao_cpf,
        'telefone': paciente.get('telefone') if paciente.get('telefone') else None,
        'confirmacao_telefone': confirmacao_telefone,
        'email': paciente.get('email') if paciente.get('email') else None,
        'confirmacao_email': confirmacao_email,
        'data_nascimento': paciente.get('data_nascimento') if paciente.get('data_nascimento') else None,
        'confirmacao_data_nascimento': confirmacao_data_nascimento,
        'rua': rua,
        'rua_confirmacao': confirmacao_rua,
        'numero': numero,
        'numero_confirmacao': confirmacao_numero,
        'bairro': bairro,
        'bairro_confirmacao': confirmacao_bairro,
        'cidade': cidade,
        'cidade_confirmacao': confirmacao_cidade,
        'estado': estado,
        'estado_confirmacao': confirmacao_estado,
        'cep': cep,
        'cep_confirmacao': confirmacao_cep,
        'complemento': complemento,
        'complemento_confirmacao': confirmacao_complemento,
        'quem_confirmou': confirmacao_quem,
        'data_confirmacao': confirmacao_data,
        'exames': exames,
        'proxima_interacao': proxima_interacao,
        'ultima_interacao': ultima_interacao,
        'canal_contato': canal_contato
    }
