import streamlit as st
import bcrypt
import sqlite3
from database import conn, cursor, criar_tabelas
from config import TIPOS_USUARIO

# ---------------------- FUNÇÕES DE USUÁRIO ----------------------

def cadastrar_usuario():
    st.subheader("📋 Cadastro de Novo Usuário")
    with st.form("form_cadastro"):
        nome = st.text_input("Nome completo", key="cadastro_nome")
        email = st.text_input("Email", key="cadastro_email")
        senha = st.text_input("Senha", type="password", key="cadastro_senha")
        tipo = st.selectbox("Tipo de usuário", TIPOS_USUARIO, key="cadastro_tipo")
        cadastrar = st.form_submit_button("Cadastrar")

    if cadastrar:
        if nome and email and senha:
            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
            try:
                cursor.execute("""
                    INSERT INTO usuarios (nome, email, senha, tipo) 
                    VALUES (?, ?, ?, ?)
                """, (nome, email, senha_hash, tipo))
                conn.commit()
                st.success("Usuário cadastrado com sucesso!")
            except sqlite3.IntegrityError:
                st.error("Este e-mail já está cadastrado.")
        else:
            st.warning("Por favor, preencha todos os campos.")


def login():
    st.subheader("🔐 Login")
    with st.form("form_login"):
        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")
        entrar = st.form_submit_button("Entrar")

    if entrar:
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(senha.encode(), user[3]):
            st.session_state['usuario'] = {
                "id": user[0],
                "nome": user[1],
                "email": user[2],
                "tipo": user[4]
            }
            st.success("Login realizado com sucesso!")
            st.experimental_rerun()
        else:
            st.error("Email ou senha incorretos.")


def logout():
    if st.sidebar.button("🚪 Sair", key="botao_sair"):
        st.session_state.clear()
        st.success("Sessão encerrada.")
        st.experimental_rerun()
