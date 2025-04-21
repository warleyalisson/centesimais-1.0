# anotacoes.py (local: raiz/analises/anotacoes.py)
import streamlit as st
from datetime import datetime
from database import salvar_anotacao, atualizar_anotacao, deletar_anotacao, buscar_anotacoes_usuario


def modulo_anotacoes(usuario):
    st.subheader("📒 Minhas Anotações")

    # Formulário para nova anotação
    with st.expander("➕ Nova Anotação"):
        titulo = st.text_input("Título da anotação", key="nova_titulo")
        conteudo = st.text_area("Conteúdo", key="nova_conteudo")
        if st.button("Salvar anotação", key="btn_salvar_anotacao"):
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            salvar_anotacao(usuario['id'], titulo, conteudo, data)
            st.success("Anotação salva com sucesso!")
            st.experimental_rerun()

    # Exibir anotações existentes
    anotacoes = buscar_anotacoes_usuario(usuario['id'])
    if anotacoes:
        for anotacao in anotacoes:
            id_, titulo, conteudo, data = anotacao
            with st.expander(f"📜 {titulo} ({data})"):
                st.write(conteudo)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Editar", key=f"editar_{id_}"):
                        novo_conteudo = st.text_area("Editar conteúdo", value=conteudo, key=f"edit_{id_}")
                        if st.button("Salvar edição", key=f"salvar_edit_{id_}"):
                            atualizar_anotacao(id_, novo_conteudo)
                            st.success("Anotação atualizada com sucesso!")
                            st.experimental_rerun()
                with col2:
                    if st.button("Excluir", key=f"excluir_{id_}"):
                        deletar_anotacao(id_)
                        st.warning("Anotação excluída!")
                        st.experimental_rerun()
