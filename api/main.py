"""
API do sistema TCC UFF: Chatbot Atendimento

Fornece endpoints para autenticação de usuários, assim como os de operações CRUD para pacientes e exames.

Como usar:
- Instale as dependências listadas em requirements.txt
- Configure as variáveis de ambiente na raiz do projeto com o .env
- Se estiver testando localmente, então ligue a API direto da raiz do projeto:
  python -m api.main
- Se estiver em produção, então veja a documentação de implantação para iniciar a API corretamente.

Endpoints principais:
- /login: autenticação de usuário e serviço (retorna token JWT)
- /pacientes: gerenciar pacientes
- /exames: gerenciar exames
- Todos os endpoints estão documentados em doc/api.md
"""

import os
import api.utils as utils
from flask import Flask
from flask_cors import CORS
from api.controllers.auth_controller import auth_routes
from api.controllers.paciente_controller import paciente_routes
from api.controllers.exame_controller import exame_routes
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = utils.get_must_have_env_variable('API_SECRET_KEY')
app.config['JWT_ALGORITHM'] = 'HS256'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('API_USER_TOKEN_EXPIRATION', '3600'))
app.config['JWT_SERVICE_TOKEN_EXPIRES'] = int(os.getenv('API_SERVICE_TOKEN_EXPIRATION', '604800'))
DB_HOST = utils.get_must_have_env_variable('DB_HOST')
DB_PORT = utils.get_must_have_env_variable('DB_PORT')
DB_NAME = utils.get_must_have_env_variable('DB_NAME')
DB_API_USER = utils.get_must_have_env_variable('DB_API_USER')
DB_API_PASS = utils.get_must_have_env_variable('DB_API_PASS')
app.config['MONGO_URI'] = f"mongodb://{DB_API_USER}:{DB_API_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['MONGO_DBNAME'] = DB_NAME

# Configuração CORS dinâmica baseada em variáveis de ambiente
WEBAPP_HOST = utils.get_must_have_env_variable('WEBAPP_HOST')
WEBAPP_PORT = utils.get_must_have_env_variable('WEBAPP_PORT')
WEBAPP_PROTOCOL = utils.get_must_have_env_variable('WEBAPP_PROTOCOL')
CORS_ORIGINS = [
    f'{WEBAPP_PROTOCOL}://{WEBAPP_HOST}:{WEBAPP_PORT}',
]
CORS_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
CORS(app, origins=CORS_ORIGINS, methods=CORS_METHODS, allow_headers=CORS_ALLOW_HEADERS)

JWTManager(app)

utils.setup_logging()
auth_routes(app)
paciente_routes(app)
exame_routes(app)

if __name__ == '__main__':
    api_port = utils.get_must_have_env_variable('API_PORT')
    app.run(debug = False, port = api_port)