# modules/analises/analises.py
import streamlit as st
import numpy as np
import statistics
from datetime import datetime
from database import inserir_analise

# ---------------------- FUNÇÕES DE CÁLCULO E SALVAMENTO DE ANALISES ----------------------

def salvar_analise_com_triplicata(usuario, nome_amostra, parametro, triplicata):
    media = round(np.mean(triplicata), 2)
    desvio = round(statistics.stdev(triplicata), 2) if len(set(triplicata)) > 1 else 0.0
    coef_var = round((desvio / media) * 100, 2) if media != 0 else 0.0
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    inserir_analise(
        usuario_id=usuario['id'],
        nome_amostra=nome_amostra,
        parametro=parametro,
        triplicata=triplicata,
        media=media,
        desvio=desvio,
        coef_var=coef_var,
        data=data
    )

    st.success(f"Análise de {parametro.lower()} registrada com sucesso!")
    st.metric("Média", f"{media}%")
    st.metric("Desvio Padrão", f"{desvio}%")
    st.metric("Coef. de Variação", f"{coef_var}%")

    return media, desvio, coef_var
