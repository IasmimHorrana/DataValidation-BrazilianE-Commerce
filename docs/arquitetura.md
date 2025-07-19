# Arquitetura do Pipeline ETL - Radar de Entregas

Este pipeline ETL processa os dados do Olist, realizando a extração, transformação e carga para análise da performance logística das entregas.

O fluxo principal é dividido em três etapas:

1. **Extract:** leitura dos arquivos CSV originais com os dados dos clientes, pedidos e itens dos pedidos.
2. **Transform:** limpeza, validação e preparação dos dados para análise.
3. **Load:** gravação dos dados transformados no banco PostgreSQL, incluindo dados válidos e inválidos.


## Fluxo do Pipeline

- Arquivos CSV (raw)
↓
- Extração
↓
- Transformação
↓
- Gravação CSVs transformados
↓
- Carga no PostgreSQL
↓
- Base pronta para análise e dashboards

