# analises/proteinas.py

import streamlit as st
import numpy as np
import statistics
from datetime import datetime
from config import PADRAO_FATOR_KJELDAHL
from database import inserir_analise

def analise_proteinas(usuario):
    st.subheader("\U0001F9EA Análise de Proteínas - Kjeldahl (AOAC)")

    nome_amostra = st.text_input("Nome da Amostra", key="proteina_nome_amostra")
    fator_conv = st.number_input("Fator de conversão (ex: 6.25)", value=PADRAO_FATOR_KJELDAHL, step=0.01, key="fator_kjeldahl")

    st.markdown("### Coleta de Dados para Triplicata")
    triplicata = []

    for i in range(1, 4):
        st.markdown(f"**\U0001F501 Medida {i}**")
        volume_HCl = st.number_input(f"Volume de HCl (mL) [{i}]", key=f"prot_hcl_{i}", step=0.01)
        branco = st.number_input(f"Volume de branco (mL) [{i}]", key=f"prot_branco_{i}", step=0.01)
        normalidade = st.number_input(f"Normalidade do HCl (N) [{i}]", key=f"prot_n_{i}", step=0.01)
        peso_amostra = st.number_input(f"Peso da amostra (g) [{i}]", key=f"prot_peso_{i}", step=0.0001)

        if peso_amostra > 0:
            nitrogenio = ((volume_HCl - branco) * normalidade * 14.007) / (peso_amostra * 1000)
            proteinas = nitrogenio * fator_conv
        else:
            proteinas = 0.0

        triplicata.append(round(proteinas, 2))
        st.markdown(f"\U0001F539 Proteína estimada ({i}): `{round(proteinas, 2)} %`")

    if st.button("Calcular e Salvar Análise de Proteínas", key="btn_salvar_proteinas"):
        media = round(np.mean(triplicata), 2)
        desvio = round(statistics.stdev(triplicata), 2) if len(set(triplicata)) > 1 else 0.0
        coef_var = round((desvio / media) * 100, 2) if media != 0 else 0.0
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        inserir_analise(usuario['id'], nome_amostra, "Proteínas", triplicata, media, desvio, coef_var, data)

        st.success("✅ Análise de proteínas registrada com sucesso!")
        st.metric("Média", f"{media}%")
        st.metric("Desvio Padrão", f"{desvio}%")
        st.metric("Coef. de Variação", f"{coef_var}%")
