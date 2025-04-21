import streamlit as st
import pandas as pd
from database import conn, converter_excel, converter_pdf
from io import BytesIO

def painel_admin():
    st.title("🔐 Painel do Administrador")
    st.subheader("📊 Visualização Geral de Todas as Análises")

    df = pd.read_sql_query("SELECT * FROM analises ORDER BY data DESC", conn)

    if df.empty:
        st.info("Nenhuma análise registrada no sistema.")
        return

    st.dataframe(df, use_container_width=True)

    # 🔍 Filtro por nome de amostra
    st.subheader("🔍 Buscar por Nome da Amostra")
    busca = st.text_input("Digite parte do nome da amostra", key="busca_admin")
    if busca:
        df_filtrado = df[df['nome_amostra'].str.contains(busca, case=False)]
        st.dataframe(df_filtrado, use_container_width=True)

    # 📥 Exportações
    st.subheader("📁 Exportar Todos os Dados")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Baixar Excel",
            data=converter_excel(df),
            file_name="analises_geral_admin.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col2:
        st.download_button(
            label="📥 Baixar PDF",
            data=converter_pdf(df),
            file_name="analises_geral_admin.pdf",
            mime="application/pdf"
        )

    # 📊 Resumo estatístico
    st.subheader("📊 Resumo Estatístico por Tipo de Análise")
    resumo = df.groupby("parametro")["media"].agg(['count', 'mean', 'std']).reset_index()
    resumo.columns = ["Análise", "Total", "Média Geral", "Desvio Padrão"]
    st.dataframe(resumo, use_container_width=True)