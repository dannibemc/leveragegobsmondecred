
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

def validar_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj) != 14:
        return False
    if cnpj in (c * 14 for c in "0123456789"):
        return False
    def calcular_digito(cnpj, pesos):
        soma = sum(int(d) * p for d, p in zip(cnpj, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1
    digito1 = calcular_digito(cnpj[:12], pesos1)
    digito2 = calcular_digito(cnpj[:12] + digito1, pesos2)
    return cnpj[-2:] == digito1 + digito2

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

if "dados" not in st.session_state:
    st.session_state.dados = carregar_dados()

# Formulário para adicionar novos registros
with st.expander("➕ Adicionar Novo Devedor"):
    with st.form("form_novo_devedor"):
        razao_social = st.text_input("Razão Social")
        cnpj = st.text_input("CNPJ")
        setor = st.selectbox("Setor", ['Agro', 'Indústria', 'Comércio', 'Serviços', 'Financeiro'])
        rating_inicial = st.selectbox("Rating Inicial", ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'C'])
        rating_atual = st.selectbox("Rating Atual", ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'C'])
        limite = st.number_input("Limite de Crédito (R$)", min_value=0)
        exposicao = st.number_input("Exposição Atual (R$)", min_value=0)
        utilizacao = st.number_input("% Utilização", min_value=0.0, max_value=200.0)
        atraso = st.number_input("Dias de Atraso", min_value=0)
        score = st.slider("Score Serasa", 300, 1000, 600)
        protesto = st.checkbox("Possui Protestos")
        pefin = st.checkbox("Possui PEFIN")
        refin = st.checkbox("Possui REFIN")
        enviar = st.form_submit_button("Adicionar")
        if enviar:
            if not validar_cnpj(cnpj):
                st.error("CNPJ inválido. Verifique e tente novamente.")
            else:
                novo = pd.DataFrame([{
                    "Razão Social": razao_social,
                    "CNPJ": cnpj,
                    "Setor": setor,
                    "Rating Inicial": rating_inicial,
                    "Rating Atual": rating_atual,
                    "Limite de Crédito (R$)": limite,
                    "Exposição Atual (R$)": exposicao,
                    "% Utilização": utilizacao,
                    "Dias de Atraso": atraso,
                    "Score Serasa": score,
                    "Protestos": int(protesto),
                    "PEFIN": int(pefin),
                    "REFIN": int(refin),
                }])
                st.session_state.dados = pd.concat([st.session_state.dados, novo], ignore_index=True)
                st.success("Devedor adicionado com sucesso!")

# Exibição dos dados
df = st.session_state.dados
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
