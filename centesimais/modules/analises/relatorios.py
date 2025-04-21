# relatorios.py (local: /analises/relatorios.py)

import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO
from database import buscar_analises_usuario

# ---------------------- RELATÓRIOS ----------------------
def modulo_relatorios(usuario):
    st.subheader("📄 Relatórios de Análises")
    aba = st.radio("Escolha uma opção:", ["Exportar Todas", "Exportar por Tipo"], key="relatorio_opcao")

    if aba == "Exportar Todas":
        exportar_todas(usuario)
    elif aba == "Exportar por Tipo":
        exportar_por_parametro(usuario)


def exportar_todas(usuario):
    dados = buscar_analises_usuario(usuario['id'])
    df = pd.DataFrame(dados, columns=["ID", "Usuario", "Amostra", "Parametro", "V1", "V2", "V3", "Média", "DP", "CV", "Data"])

    if df.empty:
        st.info("Nenhuma análise disponível.")
        return

    st.download_button("📥 Baixar Excel", data=converter_excel(df), file_name="analises_completas.xlsx")
    st.download_button("📥 Baixar PDF", data=converter_pdf(df), file_name="analises_completas.pdf")


def exportar_por_parametro(usuario):
    dados = buscar_analises_usuario(usuario['id'])
    df = pd.DataFrame(dados, columns=["ID", "Usuario", "Amostra", "Parametro", "V1", "V2", "V3", "Média", "DP", "CV", "Data"])
    parametros = df['Parametro'].unique()

    if len(parametros) == 0:
        st.info("Nenhum parâmetro encontrado.")
        return

    selecao = st.selectbox("Escolha o parâmetro para exportar:", parametros)
    df_filtrado = df[df['Parametro'] == selecao]

    st.download_button("📥 Baixar Excel", data=converter_excel(df_filtrado), file_name=f"relatorio_{selecao}.xlsx")
    st.download_button("📥 Baixar PDF", data=converter_pdf(df_filtrado), file_name=f"relatorio_{selecao}.pdf")


def converter_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()


def converter_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Relatório de Análises", ln=True, align='C')
    pdf.ln(5)

    for _, row in df.iterrows():
        texto = f"{row['Amostra']} | {row['Parametro']} | Média: {row['Média']}%"
        pdf.cell(200, 6, txt=texto, ln=True)

    return pdf.output(dest='S').encode('latin-1')
