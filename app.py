# ------------------ BLOCO 1: CONFIGURAÇÃO INICIAL ------------------
import streamlit as st
from config import APP_TITLE, LAYOUT_MODE

# Esta linha deve estar no topo, antes de qualquer outra chamada do Streamlit
st.set_page_config(page_title=APP_TITLE, layout=LAYOUT_MODE)

# ------------------ BLOCO 2: IMPORTAÇÕES DOS MÓDULOS ------------------
from modules.usuarios.usuarios import login, cadastrar_usuario, logout, verificar_usuario_logado, get_usuario_logado
from modules.admin.painel_admin import painel_admin
from modules.analises.menu_analises import menu_analises
from modules.anotacoes.modulo_anotacoes import modulo_anotacoes
from modules.relatorios.modulo_relatorios import modulo_relatorios
from modules.analises.analises_finalizadas import analises_finalizadas

# ------------------ BLOCO 3: NAVEGAÇÃO PRINCIPAL ------------------
def tela_autenticacao():
    if not verificar_usuario_logado():
        opcao = st.radio("🔐 Acesso", ["Entrar", "Cadastrar"], horizontal=True)
        if opcao == "Entrar":
            login()
        else:
            cadastrar_usuario()
    else:
        usuario = get_usuario_logado()
        st.sidebar.success(f"👤 Logado como: {usuario['nome']} ({usuario['tipo']})")

        if st.sidebar.button("🚪 Sair"):
            logout()
            st.experimental_rerun()

        if usuario["tipo"] == "admin":
            painel_admin()
        else:
            menu_usuario(usuario)

# ------------------ BLOCO 4: MENU DO USUÁRIO COMUM ------------------
def menu_usuario(usuario):
    st.sidebar.header("📋 Menu do Usuário")
    opcao = st.sidebar.radio(
        "Escolha uma opção:",
        ["Nova Análise", "Minhas Análises", "Anotações", "Relatórios"]
    )

    if opcao == "Nova Análise":
        menu_analises(usuario)
    elif opcao == "Minhas Análises":
        analises_finalizadas(usuario)
    elif opcao == "Anotações":
        modulo_anotacoes(usuario)
    elif opcao == "Relatórios":
        modulo_relatorios(usuario)

# ------------------ BLOCO 5: EXECUÇÃO PRINCIPAL ------------------
if __name__ == "__main__":
    tela_autenticacao()
