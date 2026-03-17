import streamlit as st
import psycopg2

# =========================================================
# CONEXÃO COM O NEON (PostgreSQL)
# =========================================================
@st.cache_resource(show_spinner=False)
def get_connection():
    try:
        DATABASE_URL = st.secrets["connections"]["neon"]["url"]
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        return conn
    except Exception as e:
        st.error(f"Erro crítico de conexão: {e}")
        return None


def get_db_cursor():
    conn = get_connection()
    if conn is None:
        return None, None

    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        return conn, cur

    except (psycopg2.InterfaceError, psycopg2.OperationalError):
        # Recria conexão se morrer
        st.cache_resource.clear()
        conn = get_connection()
        if conn:
            return conn, conn.cursor()
        return None, None


# =========================================================
# CRIAÇÃO DAS TABELAS
# =========================================================
def criar_tabelas():
    conn, cursor = get_db_cursor()
    if not cursor:
        return

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compras (
                id SERIAL PRIMARY KEY,
                item TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL,
                data_compra DATE,
                status TEXT DEFAULT 'pendente'
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metas (
                id SERIAL PRIMARY KEY,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                data_limite DATE,
                progresso INTEGER DEFAULT 0,
                status TEXT DEFAULT 'ativa'
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitos (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                frequencia TEXT NOT NULL,
                ofensiva INTEGER DEFAULT 0,
                ultima_vez DATE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financeiro (
                id SERIAL PRIMARY KEY,
                tipo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                data_lancamento DATE,
                status TEXT DEFAULT 'realizado'
            )
        """)

    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")

    finally:
        cursor.close()
