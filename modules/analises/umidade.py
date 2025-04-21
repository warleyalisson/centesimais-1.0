from datetime import datetime
import streamlit as st
import numpy as np
import statistics
from modules.database import inserir_analise


def analise_umidade(usuario):
    st.subheader("🔬 Nova Análise: Umidade (Estufa - AOAC)")
    nome_amostra = st.text_input("Nome da Amostra", key="umidade_nome")

    st.markdown("### Coleta de dados brutos para triplicata")
    triplicata = []

    for i in range(1, 4):
        st.markdown(f"**🔁 Medida {i}**")
        peso_cadinho_vazio = st.number_input(f"Peso do cadinho vazio (g) [{i}]", key=f"cad_um_{i}", step=0.0001)
        peso_cadinho_amostra = st.number_input(f"Peso do cadinho + amostra antes da estufa (g) [{i}]", key=f"cad_amu_{i}", step=0.0001)
        peso_cadinho_seco = st.number_input(f"Peso do cadinho + amostra seca (g) [{i}]", key=f"cad_sec_{i}", step=0.0001)

        peso_umida = peso_cadinho_amostra - peso_cadinho_vazio
        peso_seca = peso_cadinho_seco - peso_cadinho_vazio
        umidade = ((peso_umida - peso_seca) / peso_umida) * 100 if peso_umida > 0 else 0
        triplicata.append(round(umidade, 2))

        st.markdown(f"🔹 Umidade estimada ({i}): `{round(umidade, 2)} %`")

    if st.button("Calcular Estatísticas e Salvar Umidade", key="btn_umidade"):
        media = round(np.mean(triplicata), 2)
        desvio = round(statistics.stdev(triplicata), 2) if len(set(triplicata)) > 1 else 0.0
        coef_var = round((desvio / media) * 100, 2) if media != 0 else 0.0
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        inserir_analise(
            usuario_id=usuario['id'],
            nome_amostra=nome_amostra,
            parametro="Umidade",
            triplicata=triplicata,
            media=media,
            desvio=desvio,
            coef_var=coef_var,
            data=data
        )

        st.success("Análise de umidade registrada com sucesso!")
        st.metric("Média", f"{media}%")
        st.metric("Desvio Padrão", f"{desvio}%")
        st.metric("Coef. de Variação", f"{coef_var}%")
