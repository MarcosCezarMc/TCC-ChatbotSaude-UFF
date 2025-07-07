import bcrypt
import logging
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask import request, jsonify
from api.models.usuario import read_user
from api.models.chaves_servico import read_service_key

def auth_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        client_ip = request.remote_addr
        logging.info(f"Requisição de login recebida do client: {client_ip}. Checando se existe body")
        data = request.get_json(silent=True)
        if not data:
            logging.info(f"[{client_ip}] Dados não fornecidos na requisição de login. Retornando erro 400")
            return jsonify({'error': 'Dados inválidos'}), 400

        logging.info(f"[{client_ip}] Checando se o body da requisição de login contém username e password")
        if 'username' in data and 'password' in data:
            logging.info(f"[{client_ip}] Tentando encontrar usuário: {data.get('username')}")
            user = read_user(data.get('username'))
            if not user:
                logging.info(f"[{client_ip}] Usuário {data.get('username')} não encontrado. Retornando erro 401")
                return jsonify({'error': 'Credenciais inválidas'}), 401
            
            logging.info(f"[{client_ip}] Checando senha para usuário: {data.get('username')}")
            if bcrypt.checkpw(data.get('password').encode('utf-8'), user.get('password').encode('utf-8')):
                logging.info(f"[{client_ip}] Usuário {data.get('username')} autenticado com sucesso. Criando token JWT")
                access_token = create_access_token(identity=str(user.get('_id')))

                logging.info(f"[{client_ip}] Retornando Token JWT e status 200")
                return jsonify({'token': access_token}), 200
            else:
                logging.info(f"[{client_ip}] Senha incorreta para usuário {data.get('username')}. Retornando erro 401")
                return jsonify({'error': 'Credenciais inválidas'}), 401
        
        logging.info(f"[{client_ip}] Checando se o body da requisição de login contém service e key")
        if 'service' in data and 'key' in data:
            logging.info(f"[{client_ip}] Tentando encontrar serviço: {data.get('service')}")
            service_key = read_service_key(data.get('service'))
            if not service_key:
                logging.info(f"[{client_ip}] Serviço {data.get('service')} não encontrado. Retornando erro 401")
                return jsonify({'error': 'Credenciais inválidas'}), 401
            
            logging.info(f"[{client_ip}] Checando chave para serviço: {data.get('service')}")
            if bcrypt.checkpw(data.get('key').encode('utf-8'), service_key.get("chave").encode('utf-8')):
                logging.info(f"[{client_ip}] Serviço {data.get('service')} autenticado com sucesso. Criando token JWT")
                access_token = create_access_token(
                    identity = data.get('service'),
                    additional_claims = {"service": True},
                    expires_delta = app.config['JWT_SERVICE_TOKEN_EXPIRES']
                )

                logging.info(f"[{client_ip}] Retornando Token JWT e status 200")
                return jsonify({'token': access_token})
            else:
                logging.info(f"[{client_ip}] Chave incorreta para serviço {data.get('service')}. Retornando erro 401")
                return jsonify({'error': 'Credenciais inválidas'}), 401

        logging.info(f"[{client_ip}] Body de login incompleto. Retornando erro 401")
        return jsonify({'error': 'Dados inválidos'}), 400

    @app.route('/validate-token', methods=['GET'])
    @jwt_required()
    def validate_token():
        return jsonify({'message': 'Token válido'}), 200


