import streamlit as st
import pandas as pd
from database import buscar_analises_usuario, buscar_parametros_disponiveis
from modules.relatorios.utils import converter_excel, converter_pdf
from io import BytesIO


def modulo_relatorios(usuario):
    st.subheader("📄 Relatórios de Análises")
    aba = st.radio("Escolha uma opção:", ["Exportar Todas as Análises", "Exportar por Tipo de Análise"], key="opcao_relatorio")

    if aba == "Exportar Todas as Análises":
        exportar_geral(usuario)
    elif aba == "Exportar por Tipo de Análise":
        exportar_por_parametro(usuario)


def exportar_geral(usuario):
    registros = buscar_analises_usuario(usuario['id'])
    if not registros:
        st.info("Nenhuma análise cadastrada.")
        return

    df = pd.DataFrame(registros, columns=["ID", "UsuarioID", "Amostra", "Parâmetro", "V1", "V2", "V3", "Média", "DP", "CV", "Data"])

    st.download_button("📅 Baixar Excel", data=converter_excel(df), file_name="analises_geral.xlsx")
    st.download_button("📅 Baixar PDF", data=converter_pdf(df), file_name="analises_geral.pdf")


def exportar_por_parametro(usuario):
    parametros = buscar_parametros_disponiveis(usuario['id'])
    if not parametros:
        st.info("Nenhum tipo de análise disponível.")
        return

    nomes_parametros = [p[0] for p in parametros]
    escolha = st.selectbox("Selecione o parâmetro:", nomes_parametros)

    registros = buscar_analises_usuario(usuario['id'], filtro_param=escolha)
    df = pd.DataFrame(registros, columns=["ID", "UsuarioID", "Amostra", "Parâmetro", "V1", "V2", "V3", "Média", "DP", "CV", "Data"])

    st.download_button("Baixar Excel", data=converter_excel(df), file_name=f"analise_{escolha}.xlsx")
    st.download_button("Baixar PDF", data=converter_pdf(df), file_name=f"analise_{escolha}.pdf")
