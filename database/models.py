from database.database import get_connection

def criar_tabelas():

    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # COMPRAS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS compras (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        categoria TEXT,
        preco REAL,
        data_compra DATE,
        status TEXT
    )
    """)

    # =========================
    # METAS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metas (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meta TEXT,
        categoria TEXT,
        prazo DATE,
        progresso INTEGER,
        status TEXT
    )
    """)

    # =========================
    # HABITOS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habitos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habito TEXT,
        data DATE,
        feito INTEGER
    )
    """)

    # =========================
    # FINANCEIRO
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financeiro (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT,
        tipo TEXT,
        valor REAL,
        data DATE
    )
    """)

    conn.commit()
    conn.close()