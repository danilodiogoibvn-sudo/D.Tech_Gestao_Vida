from database.database import get_connection
from datetime import date

def adicionar_habito(nome, frequencia):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO habitos (nome, frequencia, ofensiva, ultima_vez)
        VALUES (?, ?, 0, NULL)
    """, (nome, frequencia))
    conn.commit()

def listar_habitos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habitos ORDER BY id DESC")
    dados = cursor.fetchall()
    return dados

def fazer_checkin(id_habito, ofensiva_atual):
    hoje = date.today().isoformat()
    nova_ofensiva = ofensiva_atual + 1
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE habitos 
        SET ofensiva = ?, ultima_vez = ?
        WHERE id = ?
    """, (nova_ofensiva, hoje, id_habito))
    conn.commit()

def excluir_habito(id_habito):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habitos WHERE id = ?", (id_habito,))
    conn.commit()