import streamlit as st
from datetime import datetime
from database import salvar_anotacao, buscar_anotacoes_usuario, atualizar_anotacao, deletar_anotacao

def modulo_anotacoes(usuario):
    st.subheader("📜 Minhas Anotações")

    # Formulário para nova anotação
    with st.expander("➕ Nova anotacão"):
        titulo = st.text_input("Título da anotação", key="nova_titulo")
        conteudo = st.text_area("Conteúdo", key="nova_conteudo")
        if st.button("Salvar anotacão", key="btn_salvar_anotacao"):
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            salvar_anotacao(usuario['id'], titulo, conteudo, data)
            st.success("Anotação salva com sucesso!")
            st.experimental_rerun()

    # Exibir anotações existentes
    anotacoes = buscar_anotacoes_usuario(usuario['id'])
    if anotacoes:
        for id_, titulo, conteudo, data in anotacoes:
            with st.expander(f"📝 {titulo} ({data})"):
                st.write(conteudo)

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("✏️ Editar", key=f"edit_btn_{id_}"):
                        novo_conteudo = st.text_area("Editar conteúdo", value=conteudo, key=f"edit_txt_{id_}")
                        if st.button("Salvar edição", key=f"save_edit_{id_}"):
                            atualizar_anotacao(id_, novo_conteudo)
                            st.success("Anotação atualizada com sucesso!")
                            st.experimental_rerun()

                with col2:
                    if st.button("🗑️ Excluir", key=f"del_btn_{id_}"):
                        deletar_anotacao(id_)
                        st.warning("Anotação excluída!")
                        st.experimental_rerun()
