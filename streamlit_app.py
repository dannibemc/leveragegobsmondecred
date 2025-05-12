import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import io

# Configuração da página
st.set_page_config(
    page_title="Dashboard Monitoramento de Crédito",
    layout="wide",
    page_icon="📊"
)

# Funções auxiliares
def calcular_metricas(df):
    if df.empty:
        return 0, 0, 0
    volume_total = df["Exposição Atual (R$)"].sum()
    atrasos = df[df["Dias de Atraso"] > 30]["Exposição Atual (R$)"].sum()
    inadimplencia = (atrasos / volume_total) * 100 if volume_total > 0 else 0
    concentracao = (df["Exposição Atual (R$)"].max() / volume_total) * 100 if volume_total > 0 else 0
    return volume_total, inadimplencia, concentracao

def download_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# Simula carregamento de dados
@st.cache_data

def carregar_dados():
    np.random.seed(42)
    n = 20
    setores = ['Agro', 'Indústria', 'Comércio', 'Serviços', 'Financeiro']
    ratings = ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'C']
    df = pd.DataFrame({
        "Razão Social": [f"Empresa {i+1}" for i in range(n)],
        "CNPJ": [f"00.000.{i:03d}/0001-00" for i in range(n)],
        "Setor": np.random.choice(setores, n),
        "Rating Inicial": np.random.choice(ratings, n),
        "Rating Atual": np.random.choice(ratings, n),
        "Limite de Crédito (R$)": np.random.randint(100_000, 1_000_000, n),
        "Exposição Atual (R$)": np.random.randint(50_000, 900_000, n),
        "% Utilização": np.random.uniform(10, 120, n),
        "Dias de Atraso": np.random.choice([0, 15, 30, 60, 90, 120], n),
        "Score Serasa": np.random.randint(300, 1000, n),
        "Protestos": np.random.choice([0, 1], n, p=[0.7, 0.3]),
        "PEFIN": np.random.choice([0, 1], n, p=[0.6, 0.4]),
        "REFIN": np.random.choice([0, 1], n, p=[0.8, 0.2]),
    })
    return df

# Interface
st.title("📊 Dashboard de Monitoramento de Crédito")

df = carregar_dados()
volume_total, inadimplencia, concentracao = calcular_metricas(df)

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Volume Total (R$)", f"{volume_total:,.2f}".replace(",", "."))
col2.metric("Inadimplência (%)", f"{inadimplencia:.2f}%")
col3.metric("Concentração Máxima (%)", f"{concentracao:.2f}%")

# Abas
aba1, aba2, aba3 = st.tabs(["📈 Visão Geral", "🏢 Devedores", "📤 Exportar"])

with aba1:
    st.subheader("Distribuição por Setor")
    fig1 = px.histogram(df, x="Setor", y="Exposição Atual (R$)", color="Setor", text_auto=True)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Score Serasa")
    fig2 = px.histogram(df, x="Score Serasa", nbins=20, title="Distribuição de Score Serasa")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Top 10 Devedores por Exposição")
    top_devedores = df.nlargest(10, "Exposição Atual (R$)")
    fig3 = px.bar(top_devedores, x="Razão Social", y="Exposição Atual (R$)", color="Score Serasa")
    st.plotly_chart(fig3, use_container_width=True)

with aba2:
    st.subheader("Base de Devedores")
    st.dataframe(df, use_container_width=True)

with aba3:
    st.subheader("Exportar Dados")
    excel_data = download_excel(df)
    st.download_button(
        label="📥 Baixar Excel",
        data=excel_data,
        file_name="dados_credito.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
