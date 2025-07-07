import logging
from flask import request, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required
from api.models.paciente import read_paciente, update_paciente
from api.models.exame import create_exame, read_exames, read_exame, update_exame, delete_exame
from api.views.exame_view import serialize_exame
from datetime import timedelta
from bson.objectid import ObjectId

# CRUD endpoints para exame

def exame_routes(app):
    @app.route('/exames', methods=['POST'])
    @jwt_required()
    def add_exam():
        client_ip = request.remote_addr
        logging.info(f"Requisição de adicionar exame feita por: {client_ip}. Checando se existe body")
        data = request.get_json(silent=True)
        if not data:
            logging.info(f"[{client_ip}] Dados não fornecidos na requisição de criar exame. Retornando erro 400")
            return jsonify({'error': 'Dados inválidos'}), 400

        logging.info(f"[{client_ip}] Checando se o body contém as informações obrigatórias para criar o exame")
        must_have = ['paciente_id', 'tipo', 'data', 'local_unidade']
        for field in must_have:
            if field not in data:
                logging.info(f"[{client_ip}] Campo obrigatório '{field}' não fornecido. Retornando erro 400")
                return jsonify({'error': f'Campo obrigatório {field} não fornecido'}), 400
            if field is None:
                logging.info(f"[{client_ip}] Campo obrigatório '{field}' não pode ser nulo. Retornando erro 400")
                return jsonify({'error': f'Campo obrigatório {field} não pode ser nulo'}), 400
            
        logging.info(f"[{client_ip}] Checando se o campo 'paciente_id' está correto")
        paciente_id = data.get('paciente_id')
        paciente = read_paciente(paciente_id)
        if not paciente:
            logging.info(f"[{client_ip}] Paciente com ID {paciente_id} não encontrado. Retornando erro 404")
            return jsonify({'error': 'Paciente não encontrado'}), 404
            
        logging.info(f"[{client_ip}] Checando se o campo 'data' está no formato correto")
        try:
            data_iso = datetime.fromisoformat(data.get('data'))
        except ValueError:
            logging.info(f"[{client_ip}] Formato de data inválido. Retornando erro 400")
            return jsonify({'error': 'Formato de data inválido, use YYYY-MM-DDTHH:MM:SS'}), 400

        logging.info(f"[{client_ip}] Criando o exame dentro do sistema")
        exame = {
            'paciente_id': ObjectId(data.get('paciente_id')),
            'tipo': str(data.get('tipo')),
            'data': data_iso,
            'local': {
                'unidade': str(data.get('local_unidade')),
                'sala': data.get('local_sala') if data.get('local_sala') else None
            },
            'medico_responsavel': {
                'nome': data.get('medico_nome') if data.get('medico_nome') else None,
                'crm': data.get('medico_crm') if data.get('medico_crm') else None,
            },
            'orientacoes': data.get('orientacao') if data.get('orientacao') else None,
            'status': "A confirmar",
            'ultima_notificacao': None,
            'proxima_notificacao': data_iso - timedelta(hours=24)
        }
        exame_id = create_exame(exame)

        logging.info(f"[{client_ip}] Inserindo o exame no documento do paciente")
        paciente['exames'] = paciente.get('exames') or []
        paciente['exames'].append(ObjectId(exame_id))
        update_paciente(paciente)

        logging.info(f"[{client_ip}] Exame criado com sucesso. ID: {exame_id}")
        return jsonify({'id': exame_id}), 201

    @app.route('/exames/id/<exame_id>', methods=['GET'])
    @jwt_required()
    def get_exame_by_id(exame_id):
        client_ip = request.remote_addr
        logging.info(f"Requisição de listar exame por ID feita por: {client_ip}. Checando se exame ID {exame_id} existe")
        exame = read_exame(exame_id)
        if not exame:
            logging.info(f"[{client_ip}] Exame com ID {exame_id} não encontrado. Retornando erro 404")
            return jsonify({'error': 'Exame não encontrado'}), 404

        logging.info(f"[{client_ip}] Exame encontrado. Retornando dados do exame")
        return jsonify(serialize_exame(exame)), 200
    
    @app.route('/exames/paciente/id/<paciente_id>', methods=['GET'])
    @jwt_required()
    def get_exames_by_paciente_id(paciente_id):
        client_ip = request.remote_addr
        logging.info(f"Requisição de listar exames por paciente feita por: {client_ip}. Checando se paciente ID {paciente_id} existe")
        paciente = read_paciente(paciente_id)
        if not paciente:
            logging.info(f"[{client_ip}] Paciente com ID {paciente_id} não encontrado. Retornando erro 404")
            return jsonify({'error': 'Paciente não encontrado'}), 404

        logging.info(f"[{client_ip}] Buscando exames associados ao paciente {paciente_id}")
        exames = read_exames(paciente_id) or []
        if len(exames) > 0:
            logging.info(f"[{client_ip}] Retornando {len(exames)} exames encontrados para o paciente {paciente_id}")
            return jsonify([serialize_exame(e) for e in exames]), 200
        else:
            logging.info(f"[{client_ip}] Nenhum exame encontrado para o paciente {paciente_id}. Retornando 404")
            return jsonify({'error': 'Nenhum exame encontrado para este paciente'}), 404

    @app.route('/exames/id/<exame_id>', methods=['PATCH'])
    @jwt_required()
    def update_exame_by_id(exame_id):
        client_ip = request.remote_addr
        logging.info(f"Requisição de atualizar exame feita por: {client_ip}. Checando se existe body")
        data = request.get_json(silent=True)
        if not data:
            logging.info(f"[{client_ip}] Dados não fornecidos na requisição de atualizar exame. Retornando erro 400")
            return jsonify({'error': 'Dados inválidos'}), 400

        logging.info(f"[{client_ip}] Checando se o exame ID {exame_id} existe")
        exame = read_exame(exame_id)
        if not exame:
            logging.info(f"[{client_ip}] Exame com ID {exame_id} não encontrado. Retornando erro 404")
            return jsonify({'error': 'Exame não encontrado'}), 404
        exame = { "_id": exame.get('_id') }
        
        logging.info(f"[{client_ip}] Checando os dados básicos para atualização do exame")
        if 'tipo' in data:
            if data.get('tipo') is None:
                logging.info(f"[{client_ip}] Tipo de exame não pode ser um dado nulo. Retornando erro 400")
                return jsonify({'error': 'Tipo de exame não pode ser um dado nulo'}), 400
            exame['tipo'] = str(data.get('tipo'))
        if 'data' in data:
            try:
                data_iso = datetime.fromisoformat(data.get('data'))
                exame['data'] = data_iso
            except ValueError:
                logging.info(f"[{client_ip}] Formato de data inválido. Retornando erro 400")
                return jsonify({'error': 'Formato de data inválido, use YYYY-MM-DDTHH:MM:SS'}), 400
        if 'orientacao' in data: exame['orientacoes'] = str(data.get('orientacao')) if data.get('orientacao') else None

        logging.info(f"[{client_ip}] Checando os dados de local para atualização do exame")
        if 'local_unidade' in data: 
            if data.get('local_unidade') is None:
                logging.info(f"[{client_ip}] Unidade do local não pode ser um dado nulo. Retornando erro 400")
                return jsonify({'error': 'Unidade do local não pode ser um dado nulo'}), 400
            exame['local.unidade'] = str(exame.get('local_unidade'))
        if 'local_sala' in data: exame['local.sala'] = str(data.get('local_sala')) if data.get('local_sala') else None

        logging.info(f"[{client_ip}] Checando os dados do médico responsável para atualização do exame")
        if 'medico_nome' in data: exame['medico_responsavel.nome'] = str(data.get('medico_nome')) if data.get('medico_nome') else None
        if 'medico_crm' in data: exame['medico_responsavel.crm'] = str(data.get('medico_crm')) if data.get('medico_crm') else None

        logging.info(f"[{client_ip}] Atualizando o exame com os dados fornecidos")
        update_exame(exame)

        if len(exame.keys()) > 1:
            logging.info(f"[{client_ip}] Atualizando os dados do exame com ID {exame_id}")
            update_exame(exame)

            logging.info(f"[{client_ip}] Dados do exame com ID {exame_id} atualizados com sucesso. Retornando 200")
            return jsonify({'msg': 'Dados do exame atualizados com sucesso'}), 200
        else:
            logging.info(f"[{client_ip}] Nenhum dado fornecido para atualizar o exame com ID {exame_id}. Retornando erro 400")
            return jsonify({'error': 'Nenhum dado fornecido para atualizar o exame'}), 400     
        
    @app.route('/exames/id/<exame_id>/agendar-notificacao', methods=['PUT'])
    @jwt_required()
    def agendar_notificacao(exame_id):
        client_ip = request.remote_addr
        logging.info(f"Requisição de agendar notificacao feita por: {client_ip}. Checando se ID {exame_id} existe")
        exame = read_exame(exame_id)
        if not exame:
            logging.info(f"[{client_ip}] Exame não encontrado. Retornando erro 404")
            return jsonify({'error': 'Exame não encontrado'}), 404
        
        logging.info(f"[{client_ip}] Checando se existe body na requisição de agendamento")
        data = request.get_json(silent=True)
        if not data:
            logging.info(f"[{client_ip}] Dados inválidos para agendamento. Retornando erro 400")
            return jsonify({'error': 'Dados inválidos para agendamento'}), 400
        
        logging.info(f"[{client_ip}] Checando se existe o campo de agendar_para no body")
        if 'agendar_para' in data:
            logging.info(f"[{client_ip}] Checando se o campo de agendar_para está no formato correto")
            try:
                proxima_notificacao = datetime.fromisoformat(data.get('agendar_para'))
            except Exception:
                logging.info(f"[{client_ip}] Formato de data inválido para proxima_notificacao: {str(data.get('agendar_para'))}. Retornando erro 400")
                return jsonify({'error': 'O formato de agendar_para tem que ser compatível com ISODate'}), 400
            exame = { "_id": exame.get('_id'), "proxima_interacao": proxima_notificacao }

            logging.info(f"[{client_ip}] Agendando a proxima notificação para: {proxima_notificacao}")
            update_exame(exame)

            logging.info(f"[{client_ip}] Proxima notificação agendada com sucesso. Retornando 200")
            return jsonify({'msg': 'Agendado com sucesso'}), 200
        else:
            logging.info(f"[{client_ip}] Campo de agendamento 'agendar_para' não fornecido. Retornando erro 400")
            return jsonify({'error': 'Campo de agendamento agendar_para não fornecido'}), 400
        
    @app.route('/exames/id/<exame_id>', methods=['DELETE'])
    @jwt_required()
    def delete_exame_by_id(exame_id):
        client_ip = request.remote_addr
        logging.info(f"Requisição de deletar exame feita por: {client_ip}. Checando se o exame ID {exame_id} existe")
        exame = read_exame(exame_id)
        if not exame:
            logging.info(f"[{client_ip}] Exame com ID {exame_id} não encontrado. Retornando erro 404")
            return jsonify({'error': 'Exame não encontrado'}), 404
        
        logging.info(f"[{client_ip}] Removendo o exame com ID {exame_id} do documento do paciente")
        paciente = read_paciente(exame.get('paciente_id'))
        paciente = { 
            "_id": paciente.get('_id'),
            "exames": [ex for ex in paciente.get('exames') if str(ex) != str(exame_id)]
        }
        update_paciente(paciente)

        logging.info(f"[{client_ip}] Deletando o exame com ID {exame_id}")
        delete_exame(exame_id)
        logging.info(f"[{client_ip}] Exame com ID {exame_id} deletado com sucesso. Retornando 200")
        return jsonify({'msg': 'Exame deletado com sucesso'}), 200



