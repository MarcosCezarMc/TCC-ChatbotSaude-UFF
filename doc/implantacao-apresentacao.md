# Documentação de Implantação para Apresentação

## Ambiente de Produção

- **Servidor:** VM Locaweb (mantido até agosto/2025)
- **SO:** Ubuntu 20.04 LTS
- **Recursos:** 1GB RAM, 35GB SSD, 2 vCPU (Intel Xeon Silver 4316 @ 2.3GHz)
- **Hypervisor:** Xen (performance próxima ao nativo)
- **Rede:** Download ~4MB/s
- **Acesso SSH:** `ssh root@191.252.181.201` (tem que registrar chave ssh)
- **Domínio público:** [https://vps59369.publiccloud.com.br](https://vps59369.publiccloud.com.br) (IP: 191.252.181.201)
- **Todas as componentes (MongoDB, API, WebApp, Chatbot) estão hospedadas nesta mesma VM.**

## Credenciais Importantes

- **MongoDB root:**
  - Usuário: `root`
  - Senha: `Q8r2v6Lp`
- **Usuário da API:**
  - Usuário: `api_user`
  - Senha: `w7Q2p9Xb`
- **JWT Secret (API):**
  - `2b7e4f8c1a9d6e3f5c0b4a7d9e2f6c1b`
- **WebApp:**
  - Usuário: `admin`
  - Senha: `diamanteluxuoso`
- **Chave do Chatbot:**
  - `8f2c1e7a4b9d6c3f5e0a2d4b7c1f8e3a`

## Link de Acesso

- **WebApp:** [https://vps59369.publiccloud.com.br](https://vps59369.publiccloud.com.br)

## Observações Relevantes

- A hospedagem foi contratada em 09/06/2025 e está paga até 09/08/2025
- O acesso ao WebApp é feito via HTTPS, com certificado SSL gerado pelo Certbot/Let's Encrypt.
- O Nginx faz o proxy reverso e serve o WebApp diretamente da pasta do repositório.
- O MongoDB está configurado com autenticação e acesso restrito à VM.
- Todas as variáveis sensíveis estão documentadas e protegidas.
- O acesso SSH é restrito à chave principal cadastrada.
- O banco de dados está criptografado

> Para dúvidas técnicas ou reimplantações, consulte a documentação detalhada em `doc/implantacao.md`.
