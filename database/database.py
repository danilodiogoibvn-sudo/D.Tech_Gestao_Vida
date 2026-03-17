import os
import sqlite3
import streamlit as st

# =========================================================
# O ESCUDO DE VELOCIDADE (Evita travamentos no Streamlit)
# =========================================================
class CachedSQLiteConnection:
    def __init__(self, conn):
        self._conn = conn

    def cursor(self, *args, **kwargs):
        return self._conn.cursor(*args, **kwargs)

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        pass  # A mágica da velocidade: não fecha a conexão, reaproveita!

    def __getattr__(self, name):
        return getattr(self._conn, name)

# =========================================================
# CONEXÃO BLINDADA
# =========================================================
@st.cache_resource(show_spinner=False)
def _get_connection_persistente():
    caminho_db = "database/gestao_vida.db"
    
    # Garante que a pasta 'database' exista antes de criar o arquivo
    pasta = os.path.dirname(caminho_db)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
        
    # check_same_thread=False evita que o app trave ao clicar rápido
    conn = sqlite3.connect(caminho_db, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def get_connection():
    """Use esta função nos seus services (casa_service, etc)"""
    conn = _get_connection_persistente()
    return CachedSQLiteConnection(conn)

# =========================================================
# CRIAÇÃO DAS TABELAS (O ESQUELETO DO APP)
# =========================================================
def criar_tabelas():
    """Roda toda vez que o app.py inicia para garantir que as tabelas existam"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Tabela da ABA CASA (Compras)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL,
                data_compra DATE,
                status TEXT DEFAULT 'pendente'
            )
        """)

        # 2. Tabela da ABA METAS (Objetivos de vida)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                data_limite DATE,
                progresso INTEGER DEFAULT 0,
                status TEXT DEFAULT 'ativa'
            )
        """)

        # 3. Tabela da ABA HÁBITOS (O tracker diário)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                frequencia TEXT NOT NULL,
                ofensiva INTEGER DEFAULT 0,
                ultima_vez DATE
            )
        """)

        # 4. Tabela da ABA FINANCEIRO (Suas finanças pessoais)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financeiro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                data_lancamento DATE,
                status TEXT DEFAULT 'realizado'
            )
        """)

        conn.commit()
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        cursor.close()