## 📍 Radar de Entrega — Dashboard e pipeline ETL

Projeto autoral focado em monitoramento e análise da performance logística no e-commerce brasileiro a partir do dataset público da Olist. O pipeline ETL implementado garante qualidade, validação e visualização geográfica dos dados para facilitar a tomada de decisão.

---

### 🔍 Análise Exploratória Inicial

Utilizamos o `ydata-profiling` para gerar perfis automáticos de cada CSV, identificando:
- Dados ausentes, duplicatas e anomalias
- Distribuições regionais e tendências iniciais
- Compreensão da estrutura e variáveis para embasar regras de validação

Esses perfis foram fundamentais para entender a estrutura dos dados e guiar a definição das regras de validação aplicadas posteriormente.



### 🛠️ Tecnologias e Bibliotecas

| Finalidade           | Ferramenta/Biblioteca     |
|----------------------|---------------------------|
| Manipulação de dados  | `Pandas`                  |
| Validação dos Dados   | `Pydantic`                |
| Testes                | `Pytest`                  |
| Registro de logs      | `Loguru`                  |
| Visualização/KPIs     | `Streamlit`               |
| Documentação          | `MkDocs`                  |



### 📋 Modelagem e Regras de Validação

As regras de validação foram implementadas com `Pydantic`, por meio de três classes principais:  `Customer`, `Order` e `OrderItem`, que representam as estruturas dos respectivos arquivos CSV.

⚠️ As regras foram definidas com base na análise exploratória dos dados (via ydata-profiling) e hipóteses lógicas, já que o projeto é autoral e sem especificações oficiais de negócio.


### 📌 Objetivos do Pipeline

 Extrair dados públicos de forma confiável (CSVs oficiais da Olist)

- ✅ Validar e garantir a qualidade dos dados com regras estruturadas
- ✅ Transformar dados para análises precisas e insights relevantes
- ✅ Registrar logs detalhados para monitoramento e debug
- ✅ Disponibilizar visualizações interativas e KPIs via dashboard
- ✅ Documentar todo o projeto e facilitar sua manutenção e extensão

---
### 🐳 Subindo o PostgreSQL com Docker + PgAdmin

### Pré-requisitos

- [Docker](https://www.docker.com/)
- O projeto já inclui um `docker-compose.yml` com os serviços do banco PostgreSQL e do PgAdmin configurados.


### Clone este repositório:

```bash
git clone https://github.com/seu_usuario/seu_repositorio.git
```
```
cd seu_repositorio
```
```
docker-compose up -d
```

----
### 📚 Fonte dos Dados

Kaggle: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
