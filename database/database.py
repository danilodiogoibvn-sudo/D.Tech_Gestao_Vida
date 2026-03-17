import streamlit as st
import psycopg2
import os

# =========================================================
# CONEXÃO COM O NEON (PostgreSQL)
# =========================================================
@st.cache_resource(show_spinner=False)
def get_connection():
    """Conecta ao Neon e garante que a conexão está ativa"""
    try:
        # Puxa a URL que você colou lá nos Settings > Secrets
        DATABASE_URL = st.secrets["connections"]["neon"]["url"]
        
        conn = psycopg2.connect(DATABASE_URL)
        # O autocommit=True salva os dados na mesma hora
        conn.autocommit = True 
        return conn
    except Exception as e:
        st.error(f"Erro crítico de conexão: {e}")
        return None

def get_db_cursor():
    """Função auxiliar para sempre pegar um cursor novo e validar a conexão"""
    conn = get_connection()
    if conn is None:
        return None, None
    try:
        # Testa se a conexão ainda está viva
        cur = conn.cursor()
        cur.execute("SELECT 1") 
        return conn, cur
    except (psycopg2.InterfaceError, psycopg2.OperationalError):
        # Se a conexão caiu, limpa o cache e tenta de novo uma vez
        st.cache_resource.clear()
        conn = get_connection()
        return conn, conn.cursor()

# =========================================================
# CRIAÇÃO DAS TABELAS (O ESQUELETO DO APP NO NEON)
# =========================================================
def criar_tabelas():
    """Roda toda vez que o app inicia para garantir que as tabelas existam"""
    conn = get_connection()
    if conn is None:
        return
        
    cursor = conn.cursor()

    try:
        # 1. Tabela de Compras (Aba Casa)
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

        # 2. Tabela de Metas
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

        # 3. Tabela de Hábitos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitos (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                frequencia TEXT NOT NULL,
                ofensiva INTEGER DEFAULT 0,
                ultima_vez DATE
            )
        """)

        # 4. Tabela Financeira
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
        print(f"Erro ao criar tabelas no Neon: {e}")
    finally:
        cursor.close()
        # Não fechamos a conn aqui pois ela é gerenciada pelo cache_resource
