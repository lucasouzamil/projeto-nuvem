
# API de Cotação do Dólar

**Autor**: [Lucas Lima](https://github.com/lucasouzamil)
[Site da documentação](https://lucasouzamil.github.io/projeto-nuvem/)

## Descrição do Projeto

Este projeto é uma API RESTful desenvolvida para realizar o registro e autenticação de usuários, além de fornecer a cotação atual do dólar em reais. A API foi construída com FastAPI e utiliza JWT para autenticação, garantindo segurança no acesso ao endpoint de consulta. A consulta de cotação do dólar é realizada via web scraping da página [Dólar Hoje](https://dolarhoje.com/), enquanto o gerenciamento de usuários e suas informações é feito utilizando o banco de dados MySQL, executado em um container Docker para facilitar a portabilidade e consistência do ambiente.

Vídeo de demonstração [aqui](https://youtu.be/AdvA5T4O6kY).

### Funcionalidades

- Registro de novos usuários com criação de token JWT
- Autenticação de usuários com retorno de token JWT
- Consulta da cotação do dólar, acessível apenas para usuários autenticados

### Pré-requisitos

- [Docker](https://www.docker.com/) instalado na máquina.

## Passos para execução

### 1. Crie um arquivo  `compose.yaml`

No diretório de sua preferência, crie um arquivo chamado `compose.yaml` com o seguinte conteúdo (você também pode baixa-lo na raiz deste repositório):

```yaml
services:

  db:
    image: mysql:9.1.0
    environment:
      MYSQL_ROOT_PASSWORD: ${ROOT_PASSWORD:-projeto}
      MYSQL_DATABASE: ${DATABASE_NAME:-projeto}
      MYSQL_USER: ${USER:-projeto}
      MYSQL_PASSWORD: ${PASSWORD:-projeto}
    ports:
      - "3306:3306"

  api:
    image: lucasouzamil/projeto-api-consulta-dolar:v1.0
    environment:
      # Informações da conectividade com o DB
      - USER=${USER:-projeto}
      - PASSWORD=${PASSWORD:-projeto}
      - SERVER=db
      - PORT=3306
      - DATABASE_NAME=${DATABASE_NAME:-projeto}
      # Informações da JWT
      - SECRET_KEY=${SECRET_KEY:-key_super_secreta}
      - ALGORITHM=${ALGORITHM:-HS256}
      - ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES:-30}
    ports:
      - "8000:8000"
    depends_on:
      - db
    restart: always
```

### 2. Configurar variáveis personalizadas (opcional):

Para usar variáveis personalizadas, crie um arquivo `.env` no mesmo diretório do `compose.yaml` (você também pode baixar o arquivo `.env.example` na raiz do repositório e renomea-lo). Adicione nele as variáveis com os valores desejados, por exemplo:

```bash
#Informações da conectividade com o DataBase
ROOT_PASSWORD=SenhaSuperSecretaRoot

USER=NomeDeUsuarioDoDataBase
PASSWORD=SenhaSuperSecretaUsuario
DATABASE_NAME=NomeDoDatabase

# Informações da JWT
SECRET_KEY=KeySuperSecretaDeCryptografia
ACCESS_TOKEN_EXPIRE_MINUTES=30 #minutos
```

Isso permite que você altere as configurações sem modificar o compose.yaml.

### 3. Iniciar os serviços com o Docker Compose:

No terminal, navegue até o diretório onde está o compose.yaml e execute o comando:

```bash
docker compose up -d
```

### 4. Acessar a aplicação:

Com os serviços ativos, acesse a aplicação em `http://localhost:8000`. A documentação interativa da API estará disponível em [`http://localhost:8000/docs`](http://localhost:8000/docs).

**OBS:** Para requisições que utilizam autenticação JWT, utilize outras formas de consulta, como o [Postman](https://www.postman.com/).

## Documentação da API

### Endpoints

1. **POST /registrar**

   Registra um novo usuário e retorna um token JWT.

    - **Request**: JSON
      ```json
      {
        "nome": "Disciplina Cloud",
        "email": "cloud@insper.edu.br",
        "senha": "cloud0"
      }
      ```

   - **Response**: JSON
     ```json
     {
       "jwt": "<JWT gerado>"
     }
     ```

2. **POST /login**

   Autentica o usuário e retorna um token JWT.

   - **Request**: JSON
     ```json
     {
       "email": "cloud@insper.edu.br",
       "senha": "cloud0"
     }
     ```

   - **Response**: JSON
     ```json
     {
       "jwt": "<JWT gerado>"
     }
     ```

3. **GET /consultar**

   Retorna a cotação atual do dólar em reais. Requer autenticação via JWT.

   - **Header**:
     ```
     Authorization: Bearer <JWT>
     ```

   - **Response**: JSON
     ```json
     {
       "Dólar agora (R$)": "<Cotação atual>"
     }
     ```

## Demonstração

### Screenshot dos Endpoints Testados

#### 1. **POST /registrar**

![Screenshot POST /registrar](./docs/img/teste-registrar.png)

#### 2. **POST /login**

![Screenshot POST /login](./docs/img/teste-login.png)

#### 3. **GET /consultar**

![Screenshot *GET /consulta](./docs/img/teste-consultar.png)

### Vídeo de Execução

Link para o vídeo de execução: [Vídeo de Demonstração](https://youtu.be/AdvA5T4O6kY)

## Link do Docker Hub

A imagem deste projeto está disponível no Docker Hub:

[Imagem Docker do Projeto](https://hub.docker.com/r/lucasouzamil/projeto-api-consulta-dolar)