## Radar de Entrega - Performance Logística

Este projeto tem como objetivo monitorar e analisar a performance logística do e-commerce brasileiro com base nos dados públicos da Olist. Ele foi construído com foco em qualidade de dados, validação, rastreabilidade e visualização interativa.

### 📌 Visão Geral do Projeto

O projeto segue um pipeline completo de dados, do bruto à análise final:

1. Importação dos arquivos CSV (disponíveis publicamente pela Olist)
2. Análise exploratória inicial com ydata-profiling para entender:

- Distribuição dos dados
- Campos ausentes e duplicados
- Regras possíveis de consistência e validação

### ✅ Validação com Pydantic

Com base na análise exploratória, foram definidas regras específicas para garantir a qualidade dos dados. Três modelos principais foram implementados:

- Customer – valida cidade, estado e estrutura de ID do cliente
- Order – valida status, timestamps e datas consistentes
- OrderItem – valida IDs, preços, frete e prazos de envio

As validações são aplicadas durante o processamento para garantir consistência e rastrear problemas de dados desde o início.

### 🔧 Transformações e Testes

Após a validação, os dados passam por transformações com **Pandas**, ajustando formatos e criando novas colunas úteis para a análise logística.
Essas transformações foram testadas com **Pytest** para garantir que regras críticas fossem mantidas mesmo com atualizações futuras.

### 🧠 Logging e Rastreamento
O projeto implementa logging com Loguru, gerando arquivos separados para cada etapa do fluxo:

- Log detalhado para extração
- Log específico por dataset na transformação
- Mensagens de erro amigáveis e rastreáveis

### 🐳 Armazenamento e Deploy

Para facilitar o uso em diferentes ambientes, os dados transformados são carregados em um banco PostgreSQL via Docker, com conexão gerenciada por SQLAlchemy.

### 📊 Dashboards Interativos
As análises finais são apresentadas em um dashboard Streamlit, com KPIs logísticos, comparações regionais e mapa interativo.