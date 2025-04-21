import sqlite3
from config import DB_PATH

# ---------------------- CONEXÃO COM O BANCO DE DADOS ----------------------
conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
cursor = conn.cursor()

# ---------------------- CRIAÇÃO DAS TABELAS SE NECESSÁRIO ----------------------
def criar_tabelas():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'usuario'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            nome_amostra TEXT,
            parametro TEXT,
            valor1 REAL,
            valor2 REAL,
            valor3 REAL,
            media REAL,
            desvio_padrao REAL,
            coef_var REAL,
            data TEXT,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anotacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            titulo TEXT,
            conteudo TEXT,
            data TEXT,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')

    conn.commit()

# ---------------------- FUNÇÕES AUXILIARES PARA ANÁLISES ----------------------
def inserir_analise(usuario_id, nome_amostra, parametro, triplicata, media, desvio, coef_var, data):
    cursor.execute('''
        INSERT INTO analises (
            usuario_id, nome_amostra, parametro,
            valor1, valor2, valor3,
            media, desvio_padrao, coef_var, data
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (usuario_id, nome_amostra, parametro, *triplicata, media, desvio, coef_var, data))
    conn.commit()

def deletar_analise(analise_id, usuario_id):
    cursor.execute(
        "DELETE FROM analises WHERE id = ? AND usuario_id = ?",
        (analise_id, usuario_id)
    )
    conn.commit()

def atualizar_media_analise(novo_valor, analise_id, usuario_id):
    cursor.execute(
        "UPDATE analises SET media = ? WHERE id = ? AND usuario_id = ?",
        (novo_valor, analise_id, usuario_id)
    )
    conn.commit()

def buscar_analises_usuario(usuario_id, filtro_param=None):
    if filtro_param and filtro_param != "Todos":
        return cursor.execute(
            "SELECT * FROM analises WHERE usuario_id = ? AND parametro = ?",
            (usuario_id, filtro_param)
        ).fetchall()
    return cursor.execute(
        "SELECT * FROM analises WHERE usuario_id = ?",
        (usuario_id,)
    ).fetchall()

def buscar_parametros_disponiveis(usuario_id):
    return cursor.execute(
        "SELECT DISTINCT parametro FROM analises WHERE usuario_id = ?",
        (usuario_id,)
    ).fetchall()

# ---------------------- FUNÇÕES AUXILIARES PARA ANOTAÇÕES ----------------------
def buscar_anotacoes_usuario(usuario_id):
    return cursor.execute(
        "SELECT id, titulo, conteudo, data FROM anotacoes WHERE usuario_id = ? ORDER BY data DESC",
        (usuario_id,)
    ).fetchall()

def salvar_anotacao(usuario_id, titulo, conteudo, data):
    cursor.execute(
        "INSERT INTO anotacoes (usuario_id, titulo, conteudo, data) VALUES (?, ?, ?, ?)",
        (usuario_id, titulo, conteudo, data)
    )
    conn.commit()

def atualizar_anotacao(anotacao_id, novo_conteudo):
    cursor.execute(
        "UPDATE anotacoes SET conteudo = ? WHERE id = ?",
        (novo_conteudo, anotacao_id)
    )
    conn.commit()

def deletar_anotacao(anotacao_id):
    cursor.execute("DELETE FROM anotacoes WHERE id = ?", (anotacao_id,))
    conn.commit()

# ---------------------- EXECUÇÃO INICIAL DAS TABELAS ----------------------
criar_tabelas()
