import json

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from utils.queries import carregar_query

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

st.header("Visão Geral")

col1, col2, col3 = st.columns(3)
col1.metric("Atraso Médio (dias)", f"{atraso_medio:.2f}")
col2.metric("Entregas no Prazo (%)", f"{entregas_no_prazo:.2f}%")
col3.metric("Tempo Médio de Entrega (dias)", f"{tempo_medio:.2f}")

st.markdown("### 📊 Comparações por Estado")

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

st.markdown("### 📦 Proporções de Pedidos e Entregas")

col1, col2 = st.columns(2)

with col1:
    pedidos_df = carregar_query(
        "relatorios/percentual_pedidos_estado.sql", estado=estado_selecionado
    )
    total_pedidos = pedidos_df["total_pedidos"].sum()
    pedidos_df["percentual"] = (
        pedidos_df["total_pedidos"] / total_pedidos
    ) * 100

    fig_pedidos = px.bar(
        pedidos_df,
        x="estado",
        y="percentual",
        text=pedidos_df["percentual"].round(1).astype(str) + "%",
        title="Percentual de Pedidos por Estado (%)",
        labels={"estado": "Estado", "percentual": "% de Pedidos"},
        height=400,
    )
    fig_pedidos.update_traces(marker_color="royalblue")
    fig_pedidos.update_layout(yaxis_title="% de Pedidos", xaxis_title="Estado")
    st.plotly_chart(fig_pedidos, use_container_width=True)

with col2:
    entregas_df = carregar_query(
        "relatorios/entregas_no_prazo_donut.sql", estado=estado_selecionado
    )

    fig_donut = px.pie(
        entregas_df,
        names="status_entrega",
        values="total",
        hole=0.5,
        title="Percentual de Entregas no Prazo (%)",
        color_discrete_map={"No Prazo": "green", "Fora do Prazo": "red"},
    )
    st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("### 🚨 Top 5 Estados com Mais Atrasos")

top_atrasos_df = carregar_query(
    "relatorios/top5_estados_atraso.sql", estado=estado_selecionado
)

fig_top_atrasos = px.bar(
    top_atrasos_df,
    x="estado",
    y="atraso_medio_dias",
    text=top_atrasos_df["atraso_medio_dias"].astype(str) + " dias",
    title="Top 5 Estados com Maior Atraso Médio",
    labels={"estado": "Estado", "atraso_medio_dias": "Atraso Médio (dias)"},
    color="atraso_medio_dias",
    color_continuous_scale="reds",
)

fig_top_atrasos.update_traces(textposition="outside")

# Ajuste leve no eixo Y para não cortar texto no topo
fig_top_atrasos.update_yaxes(
    range=[0, top_atrasos_df["atraso_medio_dias"].max() * 1.1]
)

fig_top_atrasos.update_layout(
    yaxis_title="Atraso Médio (dias)", xaxis_title="Estado", height=400
)

st.plotly_chart(fig_top_atrasos, use_container_width=True)

st.markdown("## 🗺️ Mapa de Atrasos por Estado")


# Carregar GeoJSON do Brasil
@st.cache_data
def load_geojson():
    url = (
        "https://raw.githubusercontent.com/giuliano-macedo/"
        "geodata-br-states/refs/heads/main/geojson/br_states.json"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao carregar dados geográficos: {e}")
        return None
    except json.JSONDecodeError:
        st.error("Erro ao decodificar os dados geográficos.")
        return None


geojson = load_geojson()

# ---- DADOS DO PROJETO ----
df_atraso_estado = carregar_query(
    "relatorios/mapa_percentual_atrasos.sql", estado=estado_selecionado
)

if geojson and not df_atraso_estado.empty:
    all_states = [feature["id"] for feature in geojson["features"]]
    df_all_states = pd.DataFrame(all_states, columns=["customer_state"])

    # Renomear coluna no df_atraso_estado
    # para "customer_state" para casar com df_all_states
    df_atraso_estado = df_atraso_estado.rename(
        columns={
            "estado": "customer_state",
            "percentual_atrasos": "pct_atraso",
        }
    )

    # Merge com chave correta
    df_mapa = pd.merge(
        df_all_states, df_atraso_estado, on="customer_state", how="left"
    )

    # Categorias para faixa percentual de atraso
    bins = [0, 5, 10, 15, 20, 25, 100]
    labels = [
        "Até 5%",
        "5% a 10%",
        "10% a 15%",
        "15% a 20%",
        "20% a 25%",
        "Acima de 25%",
    ]
    df_mapa["faixa_pct_atraso"] = pd.cut(
        df_mapa["pct_atraso"], bins=bins, labels=labels, right=False
    )
    df_mapa["faixa_pct_atraso"] = df_mapa[
        "faixa_pct_atraso"
    ].cat.add_categories(["Sem Informação"])
    df_mapa["faixa_pct_atraso"].fillna("Sem Informação", inplace=True)

    fig_mapa = px.choropleth(
        df_mapa,
        geojson=geojson,
        locations="customer_state",
        featureidkey="id",
        color="faixa_pct_atraso",
        color_discrete_map={
            "Sem Informação": "lightgrey",
            "Até 5%": "#d4f0f0",
            "5% a 10%": "#a0d6d6",
            "10% a 15%": "#72b7b7",
            "15% a 20%": "#469999",
            "20% a 25%": "#1e7c7c",
            "Acima de 25%": "#005f5f",
        },
        scope="south america",
        labels={
            "customer_state": "Estado",
            "faixa_pct_atraso": "% Pedidos com Atraso",
        },
        title="Percentual de Pedidos com Atraso por Estado (%)",
    )
    fig_mapa.update_layout(height=700)
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_mapa, use_container_width=True)
else:
    st.warning(
        "O mapa não pôde ser exibido porque o GeoJSON "
        "não foi carregado ou dados estão vazios."
    )
