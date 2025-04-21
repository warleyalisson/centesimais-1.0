import streamlit as st
import numpy as np
import statistics
from datetime import datetime
from database import inserir_analise

# ---------------------- ANÁLISE DE CINZAS ----------------------
def analise_cinzas(usuario):
    st.subheader("🧪 Análise de Cinzas - Método AOAC")
    nome_amostra = st.text_input("Nome da Amostra", key="cinzas_nome_amostra")

    st.markdown("### Coleta de Dados para Triplicata")
    triplicata = []

    for i in range(1, 4):
        st.markdown(f"**🔁 Medida {i}**")
        peso_cadinho = st.number_input(f"Peso do cadinho vazio (g) [{i}]", key=f"cinzas_cadinho_vazio_{i}", step=0.0001)
        peso_amostra = st.number_input(f"Peso do cadinho + amostra seca (g) [{i}]", key=f"cinzas_cadinho_amostra_{i}", step=0.0001)
        peso_cinzas = st.number_input(f"Peso do cadinho + cinzas (g) [{i}]", key=f"cinzas_cadinho_cinza_{i}", step=0.0001)

        peso_amostra_liquida = peso_amostra - peso_cadinho
        peso_cinzas_liquido = peso_cinzas - peso_cadinho

        cinzas = (peso_cinzas_liquido / peso_amostra_liquida) * 100 if peso_amostra_liquida > 0 else 0
        triplicata.append(round(cinzas, 2))

        st.markdown(f"🔹 Cinzas estimadas ({i}): `{round(cinzas, 2)} %`")

    if st.button("Calcular e Salvar Análise de Cinzas", key="btn_salvar_cinzas"):
        media = round(np.mean(triplicata), 2)
        desvio = round(statistics.stdev(triplicata), 2) if len(set(triplicata)) > 1 else 0.0
        coef_var = round((desvio / media) * 100, 2) if media != 0 else 0.0
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        inserir_analise(usuario['id'], nome_amostra, "Cinzas", triplicata, media, desvio, coef_var, data)

        st.success("✅ Análise de cinzas registrada com sucesso!")
        st.metric("Média", f"{media}%")
        st.metric("Desvio Padrão", f"{desvio}%")
        st.metric("Coef. de Variação", f"{coef_var}%")