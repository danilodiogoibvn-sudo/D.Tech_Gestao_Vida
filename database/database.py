@st.cache_resource(show_spinner=False)
def get_connection():
    """Conecta ao Neon e garante que a conexão está ativa"""
    try:
        DATABASE_URL = st.secrets["connections"]["neon"]["url"]
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        return conn
    except Exception as e:
        st.error(f"Erro crítico de conexão: {e}")
        return None

def get_db_cursor():
    """Função auxiliar para sempre pegar um cursor novo e validar a conexão"""
    conn = get_connection()
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
