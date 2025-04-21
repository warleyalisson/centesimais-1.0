# modules/analises/fibras.py
import streamlit as st
from datetime import datetime
import numpy as np
import statistics
from database import inserir_analise

def analise_fibras(usuario):
    st.subheader("🧪 Análise de Fibras Totais - AOAC 985.29 (Digestão Enzimática)")

    nome_amostra = st.text_input("Nome da Amostra", key="fibras_nome_amostra")
    st.markdown("### Coleta de Dados para Triplicata")

    triplicata = []
    for i in range(1, 4):
        st.markdown(f"**🔁 Medida {i}**")
        peso_residuo = st.number_input(f"Peso do resíduo (g) [{i}]", key=f"fibra_residuo_{i}", step=0.0001)
        correcao_proteina = st.number_input(f"Correção de proteína (g) [{i}]", key=f"fibra_proteina_{i}", step=0.0001)
        correcao_cinzas = st.number_input(f"Correção de cinzas (g) [{i}]", key=f"fibra_cinzas_{i}", step=0.0001)
        peso_amostra = st.number_input(f"Peso da amostra (g) [{i}]", key=f"fibra_amostra_{i}", step=0.0001)

        fibra_total = ((peso_residuo - correcao_proteina - correcao_cinzas) / peso_amostra) * 100 if peso_amostra > 0 else 0
        triplicata.append(round(fibra_total, 2))

        st.markdown(f"🔹 Fibras estimadas ({i}): `{round(fibra_total, 2)} %`")

    if st.button("Calcular e Salvar Análise de Fibras", key="btn_salvar_fibras"):
        media = round(np.mean(triplicata), 2)
        desvio = round(statistics.stdev(triplicata), 2) if len(set(triplicata)) > 1 else 0.0
        coef_var = round((desvio / media) * 100, 2) if media != 0 else 0.0
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        inserir_analise(usuario['id'], nome_amostra, "Fibras Totais",
                        triplicata, media, desvio, coef_var, data)

        st.success("✅ Análise de fibras registrada com sucesso!")
        st.metric("Média", f"{media}%")
        st.metric("Desvio Padrão", f"{desvio}%")
        st.metric("Coef. de Variação", f"{coef_var}%")