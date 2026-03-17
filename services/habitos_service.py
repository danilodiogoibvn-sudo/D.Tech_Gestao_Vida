from database.database import get_connection
from datetime import date

def adicionar_habito(nome, frequencia):
    conn = get_connection()
    if conn is None: return False
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO habitos (nome, frequencia, ofensiva, ultima_vez)
            VALUES (%s, %s, 0, NULL)
        """, (nome, frequencia))
        return True
    except Exception as e:
        print(f"Erro ao adicionar hábito: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def listar_habitos():
    conn = get_connection()
    if conn is None: return []
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM habitos ORDER BY id DESC")
        dados = cursor.fetchall()
        return dados
    except Exception as e:
        print(f"Erro ao listar hábitos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def fazer_checkin(id_habito, ofensiva_atual):
    hoje = date.today().isoformat()
    nova_ofensiva = ofensiva_atual + 1
    
    conn = get_connection()
    if conn is None: return False
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE habitos 
            SET ofensiva = %s, ultima_vez = %s
            WHERE id = %s
        """, (nova_ofensiva, hoje, id_habito))
        return True
    except Exception as e:
        print(f"Erro ao fazer checkin: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def excluir_habito(id_habito):
    conn = get_connection()
    if conn is None: return False
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM habitos WHERE id = %s", (id_habito,))
        return True
    except Exception as e:
        print(f"Erro ao excluir hábito: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
