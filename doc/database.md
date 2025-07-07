# Estrutura do Banco de Dados

O banco de dados é montado através do MongoDB. Para saber detalhes de como configurá-lo para desenvolvimento, consulte o [README.md](../README.md). Para configuração em produção, veja as [Instruções para implantação](./implantacao.md)

Este projeto somente usa coleções homogêneas, portanto, este documento relaciona todas as coleções e a respectiva estrutura dos documentos de cada uma. Cada seção abaixo detalha uma coleção.

> ℹ️ Observação: todas as tipagens que estiverem entre `<>` indicam que é **obrigatório existir a respectiva chave e que o valor não pode ser nulo**.

## pacientes

Armazena os dados dos pacientes. O campo CPF **deve ser único** para cada pacientes.

```yml
{
  "_id" : <ObjectId>
  "nome" : <string>
  "cpf" : <string>
  "telefone" : <string>
  "email" : string
  "data_nascimento" : string
  "endereco" : {
    "rua" : string
    "numero" : string
    "bairro" : string
    "cidade" : string
    "estado" : string
    "cep" : string  
    "complemento" : string
  },
  "confirmacao" : {
    "nome" : string
    "cpf" : string
    "telefone" : string
    "email" : string
    "data_nascimento" : string
    "endereco" : {
      "rua" : string
      "numero" : string
      "bairro" : string
      "cidade" : string
      "estado" : string
      "cep" : string    
      "complemento" : string
    },
    "quem_confirmou": string
    "data_confirmacao": ISODate
  }
  "exames" : ObjectId[0..*],          #Array de _id dos respectivos exames
  "proxima_interacao" : "ISODate",
  "ultima_interacao" : "ISODate",
  "canal_contato" : <string>
}
```

## exames

Armazena os dados dos exames dos pacientes.

```yml
{
  "_id" : <ObjectId>,
  "paciente_id" : <ObjectId>,          #Relacionado com o _id do paciente.
  "tipo" : <string>,
  "data" : <ISODate>,
  "local" : {
    "unidade" : <string>,
    "sala" : string
  },
  "medico_responsavel" : {
    "nome" : string,
    "crm" : string
  },
  "orientacoes" : string,
  "status" : <string> (A confirmar; Confirmado),
  "ultima_notificacao" : ISODate
  "proxima_notificacao" : ISODate
}
```

## usuarios

Armazena os dados dos usuários que podem autenticar no sistema através do WebApp.

```yml
{
    "_id" : <ObjectId>,
    "username" : <string>,
    "password" : <Binary>
}
```

## chaves_servico

Armazena chaves para que as componentes possam autenticar na API deste projeto. Por exemplo, o Chatbot deve ter uma chave própria.

```yml
{
  "_id" : <ObjectId>,
  "servico" : <string>,
  "chave" : <string>
}
```