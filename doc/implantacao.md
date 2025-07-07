# Instruções para Implantação do Sistema TCC UFF: Chatbot de Atendimento

Este documento apresenta um passo a passo para implantar o sistema completo do TCC UFF: Chatbot de Atendimento, incluindo o banco de dados, API, WebApp e Chatbot em um único servidor. Futuramente, este documento pode ser refatorado para detalhar a implantação em infraestrutura distribuída.

**Documentação complementar:**
- [Arquitetura do Projeto](./arquitetura-projeto.md)
- [Estrutura do Banco de Dados](./database.md)
- [Estrutura da API](./api.md)
- [Funcionamento do Chatbot](./chatbot.md)

## 1. Pré-requisitos

Antes de iniciar a implantação, certifique-se de que o ambiente possui os seguintes requisitos:

- Todos os Hosts
  - **Sistema Operacional:** Ubuntu 20.04 LTS
  - **Acesso à internet**
  - Pelo menos 1.5GB de memória RAM
  - Pelo menos 5GB de espaço livre em disco
  - Processador com pelo menos dois núcleos de 1.2Ghz

## 2. Instruções Iniciais 

1. Atualize o sistema operacional

```sh
sudo apt update && sudo apt upgrade -y
```

2. Instale o `git`

```sh
sudo apt install -y git
```

1. Instale o Python3 e o respectivo pip

```sh
sudo apt install -y python3 python3-pip python3-venv
```

4. Clone o repositório deste projeto e aponte

```sh
git clone https://github.com/MarcosCezarMc/chatbot-tcc-saude.git
```

5. Ajuste o `.env` para configurar as variáveis de ambiente

```sh
cd chatbot-tcc-saude
cp doc/dot-env-base .env
nano .env
apt install dos2unix
dos2unix .env
```

```
> ℹ️ Mantenha as credenciais usadas em documentação segura!
```

### 3. Implantação do Banco de Dados

1. Instale o MongoDB Community Server e o Mongo Shell

```sh
wget -qO - https://www.mongodb.org/static/pgp/server-8.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
sudo apt update
sudo apt install -y mongodb-org mongodb-mongosh
```

2. Inicie o serviço do MongoDB e verifique se está rodando normalmente

```sh
sudo systemctl start mongod
sudo systemctl enable mongod
sudo systemctl status mongod
```

3. Crie um usuário root no MongoDb

    * Acesse o `mongosh`
        > ```sh
        > mongosh
        > ```

    * No shell, crie o usuário root com credenciais adequadas:

       >  ```javascript
       >  use admin
       > db.createUser({
       >    user: "root",
       >    pwd: "SUA_SENHA_FORTE_AQUI",
       >    roles: [ { role: "root", db: "admin" } ]
       > })
       > ```

       > ℹ️ Mantenha as credenciais do usuário **root** documentadas em lugar seguro!

    * Saia do shell:

        > ```javascript
        > exit
        > ```

4. Edite o arquivo de configuração do MongoDB para ativar autenticação:

    * Use o `nano` para abrir o arquivo de configuração do MongoDb
   
        > ```sh
        > sudo nano /etc/mongod.conf
        > ```

    * Procure pela seção `security:` e adicione (ou descomente):
  
        > ```yaml
        > security:
        >   authorization: enabled
        > ```

    * Salve e feche o arquivo. Reinicie o serviço:
  
        > ```sh
        > sudo systemctl restart mongod
        > ```

    * Use o `mongosh` com a nova credencial de **root**: 
  
        > ```sh
        > mongosh -u root -p --authenticationDatabase admin
        > ```

5. Carregue as variáveis de ambiente do `.env` para a sessão atual:
   
    > ```sh
    > set -a
    > source .env
    > set +a
    > ```

6. Execute o script de criação do banco de dados com autenticação root:

    > ```sh
    > mongosh -u root -p --authenticationDatabase admin ./database/create-database.js
    > ```

### 4. Implantação da API em Produção

1. Instale as dependências da API (Python):

    ```sh
    pip install -r ./api/requirements.txt
    ```

2. Crie um serviço systemd para iniciar a API automaticamente ao ligar o servidor:

    * Execute o seguinte comando

        > ```sh
        > sudo nano /etc/systemd/system/tcc-api.service
        > ```

    * Adicione o conteúdo abaixo (ajuste caminhos conforme necessário):
    
        ```ini
        [Unit]
        Description=API SISTEMA TCC UFF
        After=network.target

        [Service]
        User=root
        WorkingDirectory=/root/chatbot-tcc-saude
        EnvironmentFile=/root/chatbot-tcc-saude/.env
        ExecStart=/usr/bin/gunicorn -w 2 -b 0.0.0.0:5000 api.main:app
        Restart=always

        [Install]
        WantedBy=multi-user.target
        ```
    
    > ℹ️ Caso não utilize root, substitua a variável `User` pelo seu usuário.    
    > Os caminhos em `WorkingDirectory` e `EnvironmentFile` devem apontar para o repositório clonado.
    > O comando `ExecStart` vai executar a API com **dois workers** por padrão. Altere este número para a quantidade de workers ser igual ao número de núcleos da CPU do host. Além disso, o comando usa a porta `5000` por padrão, portanto, altere caso necessário mantendo em conformidade com o `.env`.

    * Ative e inicie o serviço:
    
        ```sh
        sudo systemctl daemon-reload
        sudo systemctl enable tcc-api
        sudo systemctl start tcc-api
        sudo systemctl status tcc-api
        ```
    
    * Para ver os últimos logs gerados pelo serviço da API use:

        ```sh
        journalctl -u tcc-api -n 50
        ```

    * Em tempo real:

        ```sh
        journalctl -u tcc-api -f
        ```

### 5. Implantação do WebApp em Produção

1. Instale o Nginx:

    ```sh
    sudo apt install -y nginx
    ```

2. Altere o arquivo de configuração do WebApp para apontar para o endereço da API:

    ```sh
    nano ./webapp/scripts/config.js
    ```
    > ℹ️ Modificar o `baseURL` para `https://seu-dominio.com.br/api`. 

3. Mova o diretório do WebApp para um local acessível pelo Nginx:

    * Crie um diretório apropriado para hospedar o WebApp:

        ```sh
        sudo mkdir -p /var/www/webapp
        sudo cp -r ~/chatbot-tcc-saude/webapp/* /var/www/webapp/
        sudo chown -R www-data:www-data /var/www/webapp
        sudo chmod -R 755 /var/www/webapp
        ```

    * Abra o arquivo de configuração do `nginx`

        ```sh
        sudo nano /etc/nginx/sites-available/webapp-tcc
        ```

    * Adicione o conteúdo abaixo **(ajuste caminhos e domínio)**:

        ```nginx
        server {
            listen 80;
            listen [::]:80;
            server_name seu-dominio.com.br;

            root /var/www/webapp;
            index index.html;

            location / {
                try_files $uri $uri/ /index.html;
            }
        }
        ```

    > ℹ️ Substitua `seu-dominio.com.br` pelo domínio real do WebApp.
    > Ajuste o caminho do WebApp caso tenha usado outro diretório.

    * Ative a configuração e reinicie o Nginx:

        ```sh
        sudo ln -s /etc/nginx/sites-available/webapp-tcc /etc/nginx/sites-enabled/
        sudo nginx -t
        sudo systemctl reload nginx
        ```

4. Instale o Certbot e obtenha um certificado SSL:

    ```sh
    sudo apt install -y certbot python3-certbot-nginx
    sudo certbot --nginx
    ```

    ```
    > ℹ️ Siga as instruções do Certbot para registrar o domínio e gerar o certificado SSL.
    > Diga `2` (Sim) na etapa que pede para redirecionar o tráfego HTTP 
    > Teste o Webapp entrando no link do seu domínio!
    ```

### 6. Proxy Reverso para a API via Nginx

1. Abra o arquivo de configuração do Nginx do WebApp:

    ```sh
    sudo nano /etc/nginx/sites-available/webapp-tcc
    ```

2. Dentro do bloco do seu domínio, adicione o seguinte bloco para proxy reverso:

    ```nginx
    location /api/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    ```

    > ℹ️ Isso faz com que todas as requisições para `/api` sejam encaminhadas para a API rodando localmente na porta `5000`. Se o serviço da API foi configurada para executar em outra porta, ajuste conforme necessário.

4. Recarregue o Nginx:

    ```sh
    sudo nginx -t
    sudo systemctl reload nginx
    ```

### 6. Implantação do Chatbot em Produção

*TODO*






