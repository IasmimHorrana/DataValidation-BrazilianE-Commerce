## 📍 Radar de Entrega – Análise de Atrasos por Região

Este projeto implementa um pipeline ETL com foco em **qualidade de dados**, **validação**, **métricas** e **visualização geográfica** da performance logística no e-commerce brasileiro, utilizando esse dataset público da Olist.

---

### 🔍 Análise Exploratória Inicial

Utilizamos o `ydata-profiling` para gerar perfis automáticos de cada CSV, identificando:
- Colunas com valores ausentes
- Duplicatas
- Anomalias
- Distribuições por região

Esses perfis foram fundamentais para entender a estrutura dos dados e guiar a definição das regras de validação aplicadas posteriormente.

---

### 🎯 Objetivo

Avaliar a **performance de entrega por região** (estado e cidade), identificando gargalos logísticos através da análise de atrasos nas entregas. O projeto inclui:

---

## 🛠️ Tecnologias e Bibliotecas

| Finalidade           | Ferramenta/Biblioteca     |
|----------------------|---------------------------|
| Manipulação de dados  | `Pandas`                  |
| Validação dos Dados   | `Pydantic`                |
| Registro de logs      | `Loguru`                  |
| Cálculo de métricas   | `Time`, `Datetime`        |
| Documentação          | `MkDocs`                  |
| Visualização/KPIs     | `Streamlit`               |
| Testes                | `Pytest`                  |

---

### 📋 Modelagem e Regras de Validação

As regras de validação foram implementadas com `Pydantic`, por meio de três classes principais:  `Customer`, `Order` e `OrderItem`, que representam as estruturas dos respectivos arquivos CSV.

⚠️ As regras foram definidas com base na análise exploratória dos dados (via ydata-profiling) e hipóteses lógicas, já que o projeto é autoral e sem especificações oficiais de negócio.

---

## 📌 Objetivos do Pipeline

- ✅ Realizar **extração** dos dados públicos (CSV)
- ✅ Aplicar **validações estruturadas** para garantir qualidade
- ✅ Realizar **transformações** úteis (limpeza, formatação, enriquecimento)
- ✅ **Registrar logs** para cada etapa
- ✅ Gerar **métricas simples** de execução e qualidade
- ✅ Preparar os dados para **análises exploratórias e criação de KPIs**

---

### 📚 Fonte dos Dados

Kaggle: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
