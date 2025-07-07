# Estrutura da API

A API foi implementada com Python e framework Flask, que é uma biblioteca minimalista e flexível para construção de aplicações web e APIs RESTful. O Flask permite criar rotas, tratar requisições HTTP e organizar o código de forma simples.

O padrão de arquitetura de software usada na implementação é o [MVC](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller), pois ele separa claramente as responsabilidades do sistema: Models (acesso e manipulação dos dados), Views (formatação e serialização das respostas) e Controllers (lógica de negócio e manipulação das requisições).

Os `endpoints` implementados seguem o padrão arquitetural de software [REST](https://pt.wikipedia.org/wiki/REST), pois ele define princípios claros para construção de APIs, como uso de métodos HTTP padronizados (GET, POST, PUT, PATCH, DELETE), recursos identificados por URLs e comunicação sem estado.

Assim, as demais seções deste documento descrevem um recurso da API e os respectivos `endpoints` que podem ser usados pelas outras componentes deste sistema.

## Autenticação

- **URL base:** `/`

### Autenticar Usuário ou Serviço
- **Endpoint:** `POST /login`
- **Descrição:** Autentica usuário ou serviço e retorna um token JWT.
- **Body:**
  - Para usuário:
    ```json
    {
      "username": "usuario",
      "password": "senha"
    }
    ```
  - Para serviço:
    ```json
    {
      "service": "nome_servico",
      "key": "chave"
    }
    ```
- **Retorno:**
  - Sucesso: `200 OK`
    ```json
    { "token": "<jwt_token>" }
    ```
  - Erro:
    - `400` Dados inválidos
      - Verifique se o body não está mal formatado, com os campos corretos ou se realmente existe.
      - Se o login é para usuário, então tenha certeza de que o body contém `username` e `senha`.
      - Caso contrário, então verifique se o body contém `service` e a `key`.
    - `401` Credenciais inválidas
      - Para usuários, verifique se a senha e o nome do usuário estão corretos.
      - Para serviços, verifique se o nome e a respectiva chave estão corretos. Não esqueça o `.env`.
- **Observações:**
  - O token JWT deve ser enviado no header `Authorization: Bearer <token>` para acessar os demais endpoints.

### Validar Token
- **Endpoint:** `GET /validate-token`
- **Descrição:** Retorna 200 caso o token esteja válido e não expirado.
- **Retorno:**
  - Sucesso: `200 OK` `{ "msg": "Token válido" }`

## Paciente

- **Recurso:** Paciente
- **URL base:** `/pacientes`

### Criar paciente
- **Endpoint:** `POST /pacientes`
- **Autenticação:** JWT obrigatória
- **Body:**
  ```json
  {
    "nome": "chave e string obrigatórias. O valor não pode ser nulo",
    "cpf": "chave e string obrigatórias. O valor não pode ser nulo",
    "telefone": "chave e string obrigatórias. O valor não poder ser nulo.",
    "email": "chave e string opcionais",
    "data_nascimento": "chave e string opcionais",
    "rua": "chave e string opcionais",
    "numero": "chave e string opcionais",
    "bairro": "chave e string opcionais",
    "cidade": "chave e string opcionais",
    "estado": "chave e string opcionais",
    "cep": "chave e string opcionais",
    "complemento": "chave e string opcionais"
  }
  ```
- **Retorno:**
  - Sucesso: `201 Created` `{ "id": "<id_paciente>" }`
  - Erro: 
    - `400` Dados inválidos
      - Verifique se o body realmente existe;
      - Verifique se todos os campos obrigatórios existem e se não são nulos;
      - Verifique se o body não está mal formatado. 
    - `409` Paciente já cadastrado
      - O sistema verificou que o paciente que está tentando cadastro já existe;
      - Veja se o `cpf` está realmente correto, caso sim, então verifique o cadastro existente do paciente.

### Listar pacientes
- **Endpoint:** `GET /pacientes`
- **Autenticação:** JWT obrigatória
- **Retorno:**
  - Sucesso: `200 OK` com uma lista Json contento objetos que descrevem cada paciente.

### Buscar paciente por ID
- **Endpoint:** `GET /pacientes/id/<paciente_id>`
- **Autenticação:** JWT obrigatória
- **Retorno:**
  - Sucesso: `200 OK` com um objeto paciente
  - Erro: `404` paciente não encontrado. Verifique se o ID passado na URL está correto.

### Buscar paciente por CPF
- **Endpoint:** `GET /pacientes/cpf/<cpf>`
- **Autenticação:** JWT obrigatória
- **Retorno:**
  - Sucesso: `200 OK` com um objeto paciente
  - Erro: `404` paciente não encontrado. Verifique se o CPF passado na URL está correto.

### Atualizar dados do paciente (parcial)
- **Endpoint:** `PATCH /pacientes/id/<paciente_id>`
- **Autenticação:** JWT obrigatória
- **Body:** 
  ```json
  {
    "nome": "chave e string opcionais. O valor não pode ser nulo",
    "telefone": "chave e string opcionais. O valor não pode ser nulo",
    "email": "chave e string opcionais",
    "data_nascimento": "chave e string opcionais",
    "rua": "chave e string opcionais",
    "numero": "chave e string opcionais",
    "bairro": "chave e string opcionais",
    "cidade": "chave e string opcionais",
    "estado": "chave e string opcionais",
    "cep": "chave e string opcionais",
    "complemento": "chave e string opcionais"
  }
  ```

- **Retorno:**
  - Sucesso: `200 OK` `{ "msg": "Dados do paciente atualizados com sucesso" }`
  - Erro: 
    - `400` Dados inválidos
      - Verifique se o body realmente existe;
      - Se tem algum nome ou telefone, então eles não podem ser nulos;
      - Verifique se o body não está mal formatado. 
    - `404` Paciente não encontrado. Verifique se o ID na URL realmente está correto.

### Agendar contato para paciente
- **Endpoint:** `PUT /pacientes/id/<paciente_id>/agendar-contato`
- **Autenticação:** JWT obrigatória
- **Body:**
  ```json
  { "agendar_para": "YYYY-MM-DDTHH:MM:SS" }
  ```
- **Retorno:**
  - Sucesso: `200 OK` `{ "msg": "Agendado com sucesso" }`
  - Erro: 
    - `400` Dados inválidos
      - O campo `"agendar_para"` tem que existir, ser não nulo e tem que ser compatível com o padrão ISODate.
      - Verifique se o body não está mal formatado e se existe mesmo.
    - `404` Paciente não encontrado. Verifique se o ID do paciente na URL realmente está correto.

### Remover paciente
- **Endpoint:** `DELETE /pacientes/id/<paciente_id>`
- **Autenticação:** JWT obrigatória
- **Retorno:**
  - Sucesso: `204 No Content` `{ "msg": "Paciente removido" }`
  - Erro: 
    - `400` Paciente possui exames associados. Precisa obter o ID de todos os exames do paciente e deleta-los antes.
    - `404` Paciente não encontrado. Verifique se o ID na URL realmente está correto.

---

## Exame

- **Recurso:** Exame
- **URL base:** `/exames`

### Criar exame
- **Endpoint:** `POST /exames`
- **Autenticação:** JWT obrigatória
- **Body:**
  ```json
  {
    "paciente_id": "chave e string obrigatórias",
    "tipo": "chave e string obrigatórias. Não pode ser nulo",
    "data": "chave e string obrigatórias. Não pode ser nulo e deve estar no formato ISODate YYYY-MM-DDTHH:MM:SS",
    "local_unidade": "chave e string obrigatórias. Não pode ser nulo",
    "local_sala": "chave e string opcionais",
    "medico_nome": "chave e string opcionais",
    "medico_crm": "chave e string opcionais",
    "orientacao": "chave e string opcionais"
  }
  ```
- **Retorno:**
  - Sucesso: `201 Created` `{ "id": "<id_exame>" }`
  - Erro:
    -  `400` Campo obrigatório não fornecido ou inválido
       -  Verifique se o body não está mal formatado e se existe mesmo;
       -  Verifique se as informações obrigatórias existem mesmo e se elas não são nulas;
       -  Verifique se a data está com o formato compatível com ISODate `YYYY-MM-DDTHH:MM:SS`.
    -  `404` Paciente não encontrado. Verifique se o campo com o ID do paciente realmente existe, se não é nulo e se está correto.

### Buscar exame por ID
- **Endpoint:** `GET /exames/id/<exame_id>`
- **Autenticação:** JWT obrigatória
- **Retorno:**
  - Sucesso: `200 OK` Objeto exame
  - Erro: `404` Exame não encontrado. Verifique se o ID do exame está correto na URL.

### Listar exames de um paciente
- **Endpoint:** `GET /exames/paciente/id/<paciente_id>`
- **Autenticação:** JWT obrigatória
- **Retorno:**
  - Sucesso: `200 OK` Lista de exames
  - Erro: `404` Paciente não encontrado ou nenhum exame encontrado.

### Atualizar dados do exame (parcial)
- **Endpoint:** `PATCH /exames/id/<exame_id>`
- **Autenticação:** JWT obrigatória
- **Body:**
  ```json
  {
    "tipo": "chave e string opcionais. Não pode ser nulo.",
    "data": "chave e string opcionais. Não pode ser nulo e tem que ser compatível com ISODate YYYY-MM-DDTHH:MM:SS",
    "orientacao": "chave e string opcionais",
    "local_unidade": "chave e string opcionais. Não pode ser nulo.",
    "local_sala": "chave e string opcionais",
    "medico_nome": "chave e string opcionais",
    "medico_crm": "chave e string opcionais",
  }
  ```
- **Retorno:**
  - Sucesso: `200 OK` `{ "msg": "Dados do exame atualizados com sucesso" }`
  - Erro:
    -  `400` Dados inválidos
       -  Verifique se o body não está mal formado ou se existe mesmo;
       -  Verifique se o `tipo`, `local_unidade` e `data` não são nulos caso existam;
       -  Verifique se a `data` está em um formato compatível com ISODate caso exista.
    -  `404` Exame não encontrado. Verifique o ID do exame na URL.

### Agendar notificação para exame
- **Endpoint:** `PUT /exames/id/<exame_id>/agendar-notificacao`
- **Autenticação:** JWT obrigatória
- **Body:**
  ```json
  { "agendar_para": "chave e string obrigatórias. Não pode ser nulo e deve ser compatível com ISODate YYYY-MM-DDTHH:MM:SS" }
  ```
- **Retorno:**
  - Sucesso: `200 OK` `{ "msg": "Agendado com sucesso" }`
  - Erro: 
    - `400` Dados inválidos. Verifique se o campo `agendar_para` existe e está em formato compatível com ISODate.
    - `404` Exame não encontrado. Verifique se o ID do exame está correto na URL.

### Remover exame
- **Endpoint:** `DELETE /exames/id/<exame_id>`
- **Autenticação:** JWT obrigatória
- **Retorno:**
  - Sucesso: `200 OK` `{ "msg": "Exame deletado com sucesso" }`
  - Erro: `404` Exame não encontrado. Verifique se o ID do exame está correto na URL.