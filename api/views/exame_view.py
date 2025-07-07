def serialize_exame(exame):
    local = exame.get('local')
    local_unidade = local.get('unidade')
    local_sala = local.get('sala') or None
    
    medico = exame.get('medico_responsavel')
    medico_nome = medico_crm = None
    if medico:
        medico_nome = medico.get('nome')
        medico_crm = medico.get('crm')
    
    orientacao = exame.get('orientacoes') or None
    ultima_notificacao = str(exame.get('ultima_notificacao')) if exame.get('ultima_notificacao') else None
    proxima_notificacao = str(exame.get('proxima_notificacao')) if exame.get('proxima_notificacao') else None

    return {
        'id': str(exame.get('_id')),
        'paciente_id': str(exame.get('paciente_id')),
        'tipo': exame.get('tipo'),
        'data': str(exame.get('data')),
        'local_unidade': local_unidade,
        'local_sala': local_sala,
        'medico_nome': medico_nome,
        'medico_crm': medico_crm,
        'orientacao': orientacao,
        'status': exame.get('status'),
        'ultima_notificacao': ultima_notificacao,
        'proxima_notificacao': proxima_notificacao
    }
