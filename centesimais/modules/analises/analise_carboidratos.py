import streamlit as st
import numpy as np
from datetime import datetime
from database import inserir_analise

# ---------------------- ANÁLISE DE CARBOIDRATOS POR DIFERENÇA ----------------------

def analise_carboidratos(usuario):
    st.subheader("\U0001F9EA Cálculo de Carboidratos por Diferença")

    nome_amostra = st.text_input("Nome da Amostra", key="carb_nome_amostra")
    st.markdown("### Inserção das Médias das Demais Análises")

    umidade = st.number_input("Umidade (%)", step=0.01, key="carb_umidade")
    cinzas = st.number_input("Cinzas (%)", step=0.01, key="carb_cinzas")
    proteinas = st.number_input("Proteínas (%)", step=0.01, key="carb_proteinas")
    lipidios = st.number_input("Lipídios (%)", step=0.01, key="carb_lipidios")
    fibras = st.number_input("Fibras Totais (%)", step=0.01, key="carb_fibras")

    if st.button("Calcular e Salvar Carboidratos", key="btn_salvar_carb"):
        soma = umidade + cinzas + proteinas + lipidios + fibras
        carboidratos = round(100 - soma, 2)
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        inserir_analise(
            usuario_id=usuario['id'],
            nome_amostra=nome_amostra,
            parametro="Carboidratos por Diferença",
            triplicata=[0, 0, 0],  # sem triplicata nesse caso
            media=carboidratos,
            desvio=0.0,
            coef_var=0.0,
            data=data
        )

        st.success("✅ Cálculo de carboidratos registrado com sucesso!")
        st.metric("Carboidratos", f"{carboidratos}%")
