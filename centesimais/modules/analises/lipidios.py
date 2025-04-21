import streamlit as st
import numpy as np
import statistics
from datetime import datetime
from database import inserir_analise


def analise_lipidios(usuario):
    st.subheader("🧪 Análise de Lipídios - Extração Etérea (Soxhlet)")

    nome_amostra = st.text_input("Nome da Amostra", key="lipidios_nome_amostra")
    st.markdown("### Coleta de Dados para Triplicata")

    triplicata = []
    for i in range(1, 4):
        st.markdown(f"**🔁 Medida {i}**")
        peso_frasco_vazio = st.number_input(f"Peso do frasco vazio (g) [{i}]", key=f"lip_frasco_vazio_{i}", step=0.0001)
        peso_frasco_com_lip = st.number_input(f"Peso do frasco com lipídios (g) [{i}]", key=f"lip_frasco_com_lip_{i}", step=0.0001)
        peso_amostra = st.number_input(f"Peso da amostra (g) [{i}]", key=f"lip_peso_amostra_{i}", step=0.0001)

        peso_lipidios = peso_frasco_com_lip - peso_frasco_vazio
        lipidios = (peso_lipidios / peso_amostra) * 100 if peso_amostra > 0 else 0

        triplicata.append(round(lipidios, 2))
        st.markdown(f"🔹 Lipídeos estimados ({i}): `{round(lipidios, 2)} %`")

    if st.button("Calcular e Salvar Análise de Lipídeos", key="btn_salvar_lipidios"):
        media = round(np.mean(triplicata), 2)
        desvio = round(statistics.stdev(triplicata), 2) if len(set(triplicata)) > 1 else 0.0
        coef_var = round((desvio / media) * 100, 2) if media != 0 else 0.0
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        inserir_analise(usuario['id'], nome_amostra, "Lipídeos", triplicata, media, desvio, coef_var, data)

        st.success("✅ Análise de lipídeos registrada com sucesso!")
        st.metric("Média", f"{media}%")
        st.metric("Desvio Padrão", f"{desvio}%")
        st.metric("Coef. de Variação", f"{coef_var}%")
