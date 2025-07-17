# import pandas as pd
import plotly.express as px
import streamlit as st

# from utils.conexao import engine
from utils.queries import carregar_query

# from sqlalchemy import text


st.set_page_config(page_title="Radar de Entrega", layout="wide")
st.title("📦 Radar de Entrega - Performance Logística")

# Filtro de estado
estado_selecionado = st.sidebar.selectbox(
    "Selecione um Estado",
    options=[
        "Todos",
        "AC",
        "AL",
        "AM",
        "AP",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MG",
        "MS",
        "MT",
        "PA",
        "PB",
        "PE",
        "PI",
        "PR",
        "RJ",
        "RN",
        "RO",
        "RR",
        "RS",
        "SC",
        "SE",
        "SP",
        "TO",
    ],
    index=0,
)

# Carregar métrica com filtro
df_atraso = carregar_query(
    "relatorios/atraso_medio_dias.sql", estado=estado_selecionado
)
atraso_medio = (
    df_atraso["atraso_medio_dias"].iloc[0] if not df_atraso.empty else 0
)

df_entregas = carregar_query(
    "relatorios/percentual_entrega_prazo.sql", estado=estado_selecionado
)
entregas_no_prazo = (
    df_entregas["entregas_no_prazo_pct"].iloc[0]
    if not df_entregas.empty
    else 0
)

df_tempo = carregar_query(
    "relatorios/tempo_medio_entrega.sql", estado=estado_selecionado
)
tempo_medio = (
    df_tempo["tempo_medio_entrega_dias"].iloc[0] if not df_tempo.empty else 0
)

# Mostrar na página
st.header("Visão Geral")

col1, col2, col3 = st.columns(3)
col1.metric("Atraso Médio (dias)", f"{atraso_medio:.2f}")
col2.metric("Entregas no Prazo (%)", f"{entregas_no_prazo:.2f}%")
col3.metric("Tempo Médio de Entrega (dias)", f"{tempo_medio:.2f}")

st.header("📊 Comparações por Estado")

# Carregar dados atraso médio
df_atraso_estado = carregar_query(
    "relatorios/atraso_medio_estado.sql", estado=estado_selecionado
)
fig_atraso = px.bar(
    df_atraso_estado,
    x="customer_state",
    y="atraso_medio_dias",
    labels={
        "customer_state": "Estado",
        "atraso_medio_dias": "Atraso Médio (dias)",
    },
    title="Atraso Médio por Estado",
    color="atraso_medio_dias",
    color_continuous_scale="reds",
)
st.plotly_chart(fig_atraso, use_container_width=True)

# Carregar dados frete médio
df_frete_estado = carregar_query(
    "relatorios/frete_medio_estado.sql", estado=estado_selecionado
)
fig_frete = px.bar(
    df_frete_estado,
    x="customer_state",
    y="frete_medio",
    labels={"customer_state": "Estado", "frete_medio": "Frete Médio (R$)"},
    title="Frete Médio por Estado",
    color="frete_medio",
    color_continuous_scale="blues",
)
st.plotly_chart(fig_frete, use_container_width=True)
