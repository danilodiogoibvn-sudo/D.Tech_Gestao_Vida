import streamlit as st
import psycopg2
import os

# =========================================================
# CONEXÃO COM O NEON (PostgreSQL)
# =========================================================
@st.cache_resource(show_spinner=False)
def get_connection():
    """Conecta ao Neon usando a URL configurada nos Secrets do Streamlit"""
    try:
        # Puxa a URL que você colou lá nos Settings > Secrets
        DATABASE_URL = st.secrets["connections"]["neon"]["url"]
        
        conn = psycopg2.connect(DATABASE_URL)
        # O autocommit=True salva os dados na mesma hora, 
        # dispensando a necessidade de dar conn.commit() toda vez.
        conn.autocommit = True 
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar no banco Neon: {e}")
        return None

# =========================================================
# CRIAÇÃO DAS TABELAS (O ESQUELETO DO APP)
# =========================================================
def criar_tabelas():
    """Roda toda vez que o app inicia para garantir que as tabelas existam no Neon"""
    conn = get_connection()
    if conn is None:
        return
        
    cursor = conn.cursor()

    try:
        # 1. Tabela da ABA CASA (Compras)
        # NOTA: AUTOINCREMENT agora é SERIAL
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

        # 2. Tabela da ABA METAS (Objetivos de vida)
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

        # 3. Tabela da ABA HÁBITOS (O tracker diário)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitos (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                frequencia TEXT NOT NULL,
                ofensiva INTEGER DEFAULT 0,
                ultima_vez DATE
            )
        """)

        # 4. Tabela da ABA FINANCEIRO (Suas finanças pessoais)
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
