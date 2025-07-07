# TCC UFF: Chatbot para Atendimento

Chatbot de Telegram didático para atendimento a pacientes com as seguintes componentes:

1. Banco de dados para simular uma base de informações de pacientes.
2. Front-end com autenticação para administrar os pacientes que estão no banco de dados;
3. API para fazer ligação entre o front-end e o banco de dados de pacientes;
4. Chatbot de Telegram para simular didaticamente a ideia proposta no TCC.

<div align="center">
  <img src="doc/diagrama-arquitetura.png" alt="Diagrama da Arquitetura deste projeto." width="500"/>
  <br/>
  <span>Diagrama da Arquitetura deste projeto.</span>
</div>

Para demais detalhes da arquitetura do projeto e justificativa do uso do ferramental escolhido, veja a documentação: [Arquitetura do Projeto](doc/arquitetura-projeto.md).

## Pré-requisitos para Desenvolvimento

- Windows 11 ou Windows 10
- [Visual Studio Code (última versão)](https://code.visualstudio.com/)
- [Python (3.12+)](https://www.python.org/downloads/)
- [Git (última versão)](https://git-scm.com/downloads)
- [MongoDB Community Server 8.0.10](https://www.mongodb.com/try/download/community)
- [Mongo Shell 2.5.2](https://www.mongodb.com/try/download/shell)
- [MongoDB Compass 1.46.2](https://www.mongodb.com/try/download/compass)

## Preparação do Ambiente de Desenvolvimento

1. Instale as ferramentas da seção anterior nas versões corretas;
2. Abra o PowerShell na sua pasta de repositórios git;
3. Clone este repositório e coloque seu terminal na raiz deste projeto:
   
   ```powershell
   git clone git@github-marcoscezarmc:MarcosCezarMc/chatbot-tcc-saude.git
   cd chatbot-tcc-saude/
   ```

4. Use a ferramenta `pip` que vêm com o Python para instalar as dependências das componentes do back-end:

   ```powershell
   pip install -r api/requirements.txt
   pip install -r chatbot/requirements.txt
   ```

5. Crie o arquivo `.env` na raiz deste projeto para configurar as variáveis de ambiente usadas a partir do arquivo exemplo:

   ```powershell
   copy doc\dot-env-base .env
   ```

   > ⚠️ Atenção: não altere os valores das variáveis de ambiente se você está organizando seu ambiente para desenvolvimento básico somente. Exceto nos casos excepcionais em que pode haver algum conflito de endereços ou portas no seu sistema operacional.

6. Carregue as variáveis de ambiente no PowerShell que você está usando no momento:

   ```powershell
   Get-Content .env | ForEach-Object { if ($_ -match '^(.*?)=(.*)$') { [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2]) } }
   ```

7. Crie o banco de dados através do mongosh:

   ```powershell
   mongosh database/create-database.js
   ```

   > ⚠️ Atenção: a instalação padrão do MongoDb vem com a autenticação desabilitada.
   > Mas se a sua instalação tem autenticação, então use o seguinte comando:
   >
   > ```powershell
   > mongosh -u <root-user> -p <password> --authenticationDatabase admin create-database.js
   > ```

   > ⚠️ Atenção2: O script de criação do banco de dados armazena um usuário administrador padrão para autenticação no
   > WebApp baseado na configuração do `.env`. É fortemente recomendado mudar essas credenciais em sistemas expostos.

8. Execute a API em modo de desenvolvimento sem debug:

   ```powershell
   python -m api.main
   ```

   > ℹ️ Com os valores padrões do `.env`, a API vai ser hospedada em: `http://localhost:5000/`.
   > O debug do Flask está desabilitado para não encher o terminal com informações exaustivas.
   > O `logging` no terminal da API deve ser o suficiente para fins de debug.

9. Abra um novo terminal de PowerShell e ligue o WebApp:

   ```powershell
   cd webapp
   python -m http.server 3000
   ```

   > ℹ️ Acesse o WebApp com qualquer browser moderno usando o seguinte link: `http://localhost:3000/`. 
   > Por padrão, a etapa de criação do banco de dados faz um usuário com as credenciais `admin/tcc-uff` baseado no que foi extraído do `.env`. 

   > ⚠️ Atenção: para o WebApp funcionar corretamente, a API deve estar ligada. 
   > Se você alterou os valores do `.env` antes de ligar a API, então ajuste o código em `webapp/scripts/config.js` para usar a URL correta.

   > ⚠️ Atenção2: a API utiliza os valores no `.env` para registrar no CORS o endereço que está servindo o WebApp.
   > Se antes de ligar a API você mudou algum valor das variáveis de ambiente relacionadas ao WebApp, então ajuste o comando acima para ligar o WebApp na URL correta.

10.  TODO: executar o chatbot

11.  Seu ambiente de desenvolvimento está finalizado. Antes de construir qualquer funcionalidade do sistema:
   
     * Finalize a leitura desse README.md;
     * Finalize a leitura dos demais documentos na seção de [Documentação Importante](#documentação-importante);
     * Faça o melhor para siga a padronização local de todas as componentes, como estilo de código, estilo de logging, estrutura de pastas, padrões de nomenclatura e etc.
     * No desenvolvimento da API depois de construir ou atualizar um endpoint novo, revise a respectiva documentação no começo do `main.py` e na pasta `/doc/`;
     * Para qualquer alteração na estrutura do banco de dados, revise a respectiva documentação no `/doc/`;
     * Depois de qualquer implementação de funcionalidade no Chatbot, revise a respectiva documentação no `/doc/`.
     * Para qualquer arquivo que somente é necessário no seu próprio ambiente de desenvolvimento, como o `.env`, então coloque-o no `.gitignore`.


## Estrutura deste Repositório

### Esquema de Branchs e Versionamento

Como este projeto é um protótipo didático para demonstração da proposta de solução computacional do TCC, todo o versionamento do projeto é controlado através dos commits no git na branch `main`. Utilize sempre o último commit para desenvolver e implantar em qualquer ambiente computacional.

* Link do repositório: https://github.com/MarcosCezarMc/chatbot-tcc-saude 

### Estrutura de pastas 

```
chatbot-tcc-saude/
│
├── api/         # Código da API backend que interage com o banco de dados
├── chatbot/     # Código do chatbot Telegram
├── database/    # Scripts de banco de dados
├── doc/         # Documentação do projeto e .env exemplo 
├── webapp/      # Código do WebApp
│                # Outros arquivos na raiz: README.md, .gitignore, etc
```

## Documentação Importante

* [Arquitetura do projeto](./doc/arquitetura-projeto)
* [Estrutura do banco de dados](./doc/database.md)
* [Estrutura da API](./doc/api.md)
* [Funcionamento do Chatbot](./doc/chatbot.md)
* [Instruções para implantação](./doc/implantacao.md)
* [Implantação do projeto para o TCC](./doc/implantacao-apresentacao.md)
* Todas as implementações devem ter uma documentação básica de como executar no topo do arquivo principal




