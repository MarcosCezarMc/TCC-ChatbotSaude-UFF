import logging
from flask import request, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required
from api.models.paciente import create_paciente, read_paciente_by_cpf, read_pacientes, read_paciente, update_paciente, delete_paciente
from api.views.paciente_view import serialize_paciente

def paciente_routes(app):
    @app.route('/pacientes', methods=['POST'])
    @jwt_required()
    def add_patient():
        client_ip = request.remote_addr
        logging.info(f"Requisição de adicionar paciente feita por: {client_ip}. Checando se existe body")
        data = request.get_json(silent=True)
        if not data:
            logging.info(f"[{client_ip}] Dados não fornecidos na requisição de criar paciente. Retornando erro 400")
            return jsonify({'error': 'Dados inválidos'}), 400
        
        logging.info(f"[{client_ip}] Checando se o body contém as informações obrigatórias para criar o paciente")
        must_have = ['nome', 'cpf', 'telefone']
        for field in must_have:
            if field not in data:
                logging.info(f"[{client_ip}] Campo obrigatório '{field}' não fornecido. Retornando erro 400")
                return jsonify({'error': f'Campo obrigatório {field} não fornecido'}), 400
            if data.get(field) is None:
                logging.info(f"[{client_ip}] Campo obrigatório '{field}' não pode ser None. Retornando erro 400")
                return jsonify({'error': f'Campo obrigatório {field} não pode ser null'}), 400
        
        logging.info(f"[{client_ip}] Checando se o paciente com CPF {str(data.get('cpf'))} já existe no banco de dados")
        if read_paciente_by_cpf(str(data.get('cpf'))):
            logging.info(f"[{client_ip}] Paciente com CPF {str(data.get('cpf'))} já existe. Retornando erro 409")
            return jsonify({'error': 'Paciente já cadastrado'}), 409

        logging.info(f"[{client_ip}] Criando o paciente dentro do sistema")
        patient = {
            'nome': str(data.get('nome')),
            'cpf': str(data.get('cpf')),
            'telefone': str(data.get('telefone')),
            'email': str(data.get('email')) if data.get('email') else None,
            'data_nascimento': str(data.get('data_nascimento')) if data.get('data_nascimento') else None,
            'endereco': {
                'rua': str(data.get('rua')) if data.get('rua') else None,
                'numero': str(data.get('numero')) if data.get('numero') else None,
                'bairro': str(data.get('bairro')) if data.get('bairro') else None,
                'cidade': str(data.get('cidade')) if data.get('cidade') else None,
                'estado': str(data.get('estado')) if data.get('estado') else None,
                'cep': str(data.get('cep')) if data.get('cep') else None,
                'complemento': str(data.get('complemento')) if data.get('complemento') else None
            },
            "confirmacao": None,
            "exames": None,
            "proxima_interacao": None,
            "ultima_interacao": None,
            "canal_contato": "Telegram"
        }
        patient_id = create_paciente(patient)

        logging.info(f"[{client_ip}] Paciente criado com sucesso. ID: {patient_id}")
        return jsonify({'id': patient_id}), 201

    @app.route('/pacientes', methods=['GET'])
    @jwt_required()
    def list_pacientes():
        client_ip = request.remote_addr
        logging.info(f"Requisição de listar pacientes feita por: {client_ip}. Obtendo lista de pacientes")
        pacientes = read_pacientes()
        logging.info(f"[{client_ip}] Retornando {len(pacientes)} pacientes encontrados")
        return jsonify([serialize_paciente(p) for p in pacientes]), 200

    @app.route('/pacientes/id/<paciente_id>', methods=['GET'])
    @jwt_required()
    def get_paciente_by_id(paciente_id):
        client_ip = request.remote_addr
        logging.info(f"Requisição de obter paciente por ID feita por: {client_ip}. Checando se ID {paciente_id} existe")
        paciente = read_paciente(paciente_id)
        if paciente:
            logging.info(f"[{client_ip}] Retornando 200 com os dados do paciente")
            return jsonify(serialize_paciente(paciente)), 200
        else:
            logging.info(f"[{client_ip}] Paciente não encontrado. Retornando erro 404")
            return jsonify({'error': 'Paciente não encontrado'}), 404
    
    @app.route('/pacientes/cpf/<paciente_cpf>', methods=['GET'])
    @jwt_required()
    def get_paciente_by_cpf(paciente_cpf):
        client_ip = request.remote_addr
        logging.info(f"Requisição de obter paciente por CPF feita por: {client_ip}. Checando se CPF {paciente_cpf} existe")
        paciente = read_paciente_by_cpf(paciente_cpf)

        if paciente:
            logging.info(f"[{client_ip}] Retornando 200 com os dados do paciente")
            return jsonify(serialize_paciente(paciente))
        else:
            logging.info(f"[{client_ip}] Paciente não encontrado. Retornando erro 404")
            return jsonify({'error': 'Paciente não encontrado'}), 404

    @app.route('/pacientes/id/<paciente_id>', methods=['PATCH'])
    @jwt_required()
    def update_paciente_by_id(paciente_id):
        client_ip = request.remote_addr
        logging.info(f"Requisição de atualizar os dados básicos de paciente feita por: {client_ip}. Checando se ID {paciente_id} existe")
        paciente = read_paciente(paciente_id)
        if not paciente:
            logging.info(f"[{client_ip}] Paciente não encontrado. Retornando erro 404")
            return jsonify({'error': 'Paciente não encontrado'}), 404
        paciente = { "_id": paciente.get('_id') }
        
        logging.info(f"[{client_ip}] Checando se existe body")
        data = request.get_json(silent=True)
        if not data:
            logging.info(f"[{client_ip}] Dados não fornecidos na requisição de atualizar paciente. Retornando erro 400")
            return jsonify({'error': 'Dados inválidos'}), 400
        
        logging.info(f"[{client_ip}] Checando os dados básicos para atualizar o paciente")
        if 'nome' in data:
            if data.get('nome') is None:
                logging.info(f"[{client_ip}] Nome não pode ser None. Retornando erro 400")
                return jsonify({'error': 'Nome não pode ser null'}), 400
            paciente['nome'] = str(data.get('nome'))
        if 'telefone' in data: 
            if data.get('telefone') is None:
                logging.info(f"[{client_ip}] Telefone não pode ser None. Retornando erro 400")
                return jsonify({'error': 'Telefone não pode ser null'}), 400
            paciente['telefone'] = str(data.get('telefone'))
        if 'email' in data: paciente['email'] = str(data.get('email')) if data.get('email') else None
        if 'data_nascimento' in data: paciente['data_nascimento'] = str(data.get('data_nascimento')) if data.get('data_nascimento') else None

        logging.info(f"[{client_ip}] Checando os dados de endereço para atualizar o paciente")
        if 'rua' in data: paciente['endereco.rua'] = str(data.get('rua')) if data.get('rua') else None
        if 'numero' in data: paciente['endereco.numero'] = str(data.get('numero')) if data.get('numero') else None
        if 'bairro' in data: paciente['endereco.bairro'] = str(data.get('bairro')) if data.get('bairro') else None
        if 'cidade' in data: paciente['endereco.cidade'] = str(data.get('cidade')) if data.get('cidade') else None
        if 'estado' in data: paciente['endereco.estado'] = str(data.get('estado')) if data.get('estado') else None
        if 'cep' in data: paciente['endereco.cep'] = str(data.get('cep')) if data.get('cep') else None
        if 'complemento' in data: paciente['endereco.complemento'] = str(data.get('complemento')) if data.get('complemento') else None

        if len(paciente.keys()) > 1:
            logging.info(f"[{client_ip}] Atualizando os dados do paciente com ID {paciente_id}")
            update_paciente(paciente)

            logging.info(f"[{client_ip}] Dados do paciente com ID {paciente_id} atualizados com sucesso. Retornando 200")
            return jsonify({'msg': 'Dados do paciente atualizados com sucesso'}), 200
        else:
            logging.info(f"[{client_ip}] Nenhum dado fornecido para atualizar o paciente com ID {paciente_id}. Retornando erro 400")
            return jsonify({'error': 'Nenhum dado fornecido para atualizar o paciente'}), 400     

    @app.route('/pacientes/id/<paciente_id>/agendar-contato', methods=['PUT'])
    @jwt_required()
    def agendar_contato(paciente_id):
        client_ip = request.remote_addr
        logging.info(f"Requisição de agendar contato feita por: {client_ip}. Checando se ID {paciente_id} existe")
        paciente = read_paciente(paciente_id)
        if not paciente:
            logging.info(f"[{client_ip}] Paciente não encontrado. Retornando erro 404")
            return jsonify({'error': 'Paciente não encontrado'}), 404
        
        logging.info(f"[{client_ip}] Checando se existe body na requisição de agendamento")
        data = request.get_json(silent=True)
        if not data:
            logging.info(f"[{client_ip}] Dados inválidos para agendamento. Retornando erro 400")
            return jsonify({'error': 'Dados inválidos para agendamento'}), 400
        
        logging.info(f"[{client_ip}] Checando se existe o campo de agendar_para no body")
        if 'agendar_para' in data:
            logging.info(f"[{client_ip}] Checando se o campo de agendar_para está no formato correto")
            try:
                proxima_interacao = datetime.fromisoformat(data.get('agendar_para'))
            except Exception:
                logging.info(f"[{client_ip}] Formato de data inválido para proxima_interacao: {str(data.get('agendar_para'))}. Retornando erro 400")
                return jsonify({'error': 'O formato de agendar_para tem que ser compatível com ISODate'}), 400
            paciente = { "_id": paciente.get('_id'), "proxima_interacao": proxima_interacao }

            logging.info(f"[{client_ip}] Agendando a proxima interação para: {proxima_interacao}")
            update_paciente(paciente)

            logging.info(f"[{client_ip}] Proxima interação agendada com sucesso. Retornando 200")
            return jsonify({'msg': 'Agendado com sucesso'}), 200
        else:
            logging.info(f"[{client_ip}] Campo de agendamento 'agendar_para' não fornecido. Retornando erro 400")
            return jsonify({'error': 'Campo de agendamento agendar_para não fornecido'}), 400
        
    @app.route('/pacientes/id/<paciente_id>', methods=['DELETE'])
    @jwt_required()
    def delete_paciente_by_id(paciente_id):
        client_ip = request.remote_addr
        logging.info(f"Requisição de remover paciente feita por: {client_ip}. Checando se o paciente existe")
        paciente = read_paciente(paciente_id)
        if not paciente:
            logging.info(f"[{client_ip}] Paciente não encontrado. Retornando erro 404")
            return jsonify({'error': 'Paciente não encontrado'}), 404
        
        logging.info(f"[{client_ip}] Checando se o paciente tem exames associados")
        exames = paciente.get('exames') or []
        if len(exames) > 0:
            logging.info(f"[{client_ip}] Paciente com ID {paciente_id} tem exames associados. Retornando erro 400")
            return jsonify({'error': 'Paciente não pode ser removido, pois possui exames associados'}), 400

        logging.info(f"[{client_ip}] Removendo paciente com ID {paciente_id} do sistema")
        delete_paciente(paciente_id)
        logging.info(f"[{client_ip}] Paciente com ID {paciente_id} removido com sucesso. Retornando 204")
        return jsonify({'msg': 'Paciente removido'}), 204
