
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from fpdf import FPDF

st.title("Relatório de Monitoramento de Crédito")

# Upload de arquivo Excel
uploaded_file = st.file_uploader("Envie um arquivo Excel", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("Arquivo carregado com sucesso!")

    # Mostrar DataFrame
    st.subheader("Pré-visualização dos dados")
    st.dataframe(df)

    # KPIs simples
    if "valor_credito" in df.columns:
        total = df["valor_credito"].sum()
        media = df["valor_credito"].mean()
        st.metric("Total de Crédito", f"R$ {total:,.2f}")
        st.metric("Média de Crédito", f"R$ {media:,.2f}")

        # Gráfico
        st.subheader("Distribuição de Crédito")
        fig = px.histogram(df, x="valor_credito", nbins=20)
        st.plotly_chart(fig)

    # Geração de PDF
    if st.button("Gerar PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Relatório de Crédito", ln=True, align='C')
        pdf.ln(10)

        for index, row in df.iterrows():
            linha = " | ".join(f"{col}: {row[col]}" for col in df.columns)
            pdf.multi_cell(0, 10, linha)

        buffer = BytesIO()
        pdf.output(buffer)
        st.download_button(
            label="📄 Baixar relatório PDF",
            data=buffer.getvalue(),
            file_name="relatorio_credito.pdf",
            mime="application/pdf"
        )
