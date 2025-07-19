Este projeto utiliza **Poetry** para gerenciar dependências e **Docker Compose** para subir o banco de dados PostgreSQL com interface do **PgAdmin** via navegador.

### ✅ Pré-requisitos

Antes de começar, instale o seguinte em sua máquina:

- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

---

### Passo a passo de instalação:

#### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```
#### 2. Instale as dependências com o Poetry
```
poetry install
```
#### 3. Ative o ambiente virtual do Poetry
```
poetry shell
```

### 🐳 Suba o banco de dados com Docker Compose
O projeto já inclui um arquivo docker-compose.yml. Ele vai subir:

- Uma instância PostgreSQL
- O PgAdmin acessível via navegador

#### Execute
```
docker-compose up -d
```
#### Acesse o PgAdmin em
```
http://localhost:5050
```
#### Login PgAdmin
```
E-mail: pgadmin4@pgadmin.org
Senha: postgres
```

Ao entrar no PgAdmin pela primeira vez, ele vai pedir para adicionar um novo servidor. Aqui vão os dados que você deve preencher:

#### Aba "General"
- Name: olist_db (ou qualquer nome que você queira dar ao servidor)

#### Aba "Connection"
- Host name/address: db
(esse é o nome do serviço do container Docker, não é localhost)

- Port: 5432
- Username: postgres
- Password: postgres

☑️ Marque a opção "Save Password" se quiser evitar digitar sempre.

