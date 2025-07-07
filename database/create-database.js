// Script para criação do banco de dados no MongoDB.
//
// 1. Para que serve:
//  - Este script cria o banco de dados com um administrador padrão para a API.
//  - O objetivo é preparar o banco para uso inicial pelo sistema.
//  - Além disso, este script também cria um usuário para autenticação no WebApp com credenciais registradas
//    no arquivo `.env`. Veja o README.md para mais detalhes.
//
// 2. Como se usa:
//  - Carregue as variáveis de ambiente dispostas no arquivo `.env` e execute este script
//  com um usuário root do MongoDB (veja README.md ou documento de implantação).

//  - Execute este script no mongosh, por exemplo:
//  mongosh -u <root-user> -p <password> --authenticationDatabase admin create-database.js 

print("Iniciando a criação do banco de dados");
print("Carregando variáveis de ambiente");
const dbName = process.env.DB_NAME;
if (!dbName) {
    print("[ERRO] A variável de ambiente DB_NAME não foi encontrada. Certifique-se que as variáveis de ambiente estão carregadas no terminal.");
    quit(1);
}

const apiUser = process.env.DB_API_USER;
const apiPass = process.env.DB_API_PASS;
if (!apiUser || !apiPass) {
    print("[ERRO] Variáveis de ambiente DB_API_USER e/ou DB_API_PASS não encontradas. Certifique-se que as variáveis de ambiente estão carregadas no terminal.");
    quit(1);
}

const chatBotServiceName = "chatbot"
const chatBotEncryptedServiceKey = process.env.CHATBOT_ENCRYPTED_SERVICE_KEY;
if (!chatBotEncryptedServiceKey) {
    print("[ERRO] Variável de ambiente CHATBOT_ENCRYPTED_SERVICE_KEY não encontrada. Certifique-se que as variáveis de ambiente estão carregadas no terminal.");
    quit(1);
}

const defaultAdmin = process.env.WEBAPP_USER
if (!defaultAdmin) {
    print("[ERRO] Variável de ambiente WEBAPP_USER não encontrada. Certifique-se que as variáveis de ambiente estão carregadas no terminal.");
    quit(1);
}
const defaultAdminEncryptedPass = process.env.WEBAPP_ENCRYPTED_PASS;
if (!defaultAdminEncryptedPass) {
    print("[ERRO] Variável de ambiente DB_API_ENCRYPTED_PASS não encontrada. Certifique-se que as variáveis de ambiente estão carregadas no terminal.");
    quit(1);
}   

print(`Criando/acessando banco de dados '${dbName}'`);
const db = db.getSiblingDB(dbName);

print(`Criando usuário de API '${apiUser}'`);
try {
    db.createUser({
        user: apiUser,
        pwd: apiPass,
        roles: [{ role: "readWrite", db: dbName }]
    });
    print(`Usuário '${apiUser}' criado com sucesso`);
} catch (e) {
    if (e.codeName === 'DuplicateKey' || (e.errmsg && e.errmsg.indexOf('already exists') !== -1)) {
        print(`Usuário '${apiUser}' já existe no banco`);
    } else {
        print(`Erro ao criar usuário: ${e}`);
        throw e;
    }
}

print(`Criando coleção de pacientes e exames`);
collections = ["pacientes", "exames"];
collections.forEach(function(collection) {
    if (!db.getCollectionNames().includes(collection)) {
        db.createCollection(collection);
        print(`Coleção '${collection}' criada com sucesso`);
    }
    else print(`Coleção '${collection}' já existe no banco`);
});

print(`Criando coleção de usuários`);
if(!db.getCollectionNames().includes("usuarios")) {
    db.createCollection("usuarios");
    print(`Coleção 'usuarios' criada com sucesso`);
    print(`Inserindo um usuário administrador padrão na coleção usuarios`);
    db.usuarios.insertOne({
        username: defaultAdmin,
        password: defaultAdminEncryptedPass,
    });
    print(`Usuário administrador '${defaultAdmin}' inserido na coleção 'usuarios'`);
} else print(`Coleção 'usuarios' já existe no banco`);

print(`Criando coleção de chaves de serviço`);
if(!db.getCollectionNames().includes("chaves_servico")) {
    db.createCollection("chaves_servico");
    print(`Coleção 'chaves_servico' criada com sucesso`);
    print(`Inserindo chave de serviço padrão na coleção chaves_servico`);
    db.chaves_servico.insertOne({
        servico: chatBotServiceName,
        chave: chatBotEncryptedServiceKey
    });
    print(`Chave de serviço inserida na coleção 'chaves_servico'`);
}

print(`Banco de dados '${dbName}' pronto para uso`);