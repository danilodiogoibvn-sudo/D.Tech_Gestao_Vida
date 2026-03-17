from database.database import get_db_cursor
from datetime import date

def adicionar_habito(nome, frequencia):
    conn, cursor = get_db_cursor()
    if conn is None or cursor is None:
        return False

    try:
        cursor.execute("""
            INSERT INTO habitos (nome, frequencia, ofensiva, ultima_vez)
            VALUES (%s, %s, 0, NULL)
        """, (nome, frequencia))
        return True

    except Exception as e:
        print(f"Erro ao adicionar habito: {e}")
        return False

    finally:
        cursor.close()
        conn.close()


def listar_habitos():
    conn, cursor = get_db_cursor()
    if conn is None or cursor is None:
        return []

    try:
        cursor.execute("""
            SELECT id, nome, frequencia, ofensiva, ultima_vez 
            FROM habitos 
            ORDER BY id DESC
        """)
        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao listar habitos: {e}")
        return []

    finally:
        cursor.close()
        conn.close()
