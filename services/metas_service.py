from database.database import get_connection

def adicionar_meta(titulo, categoria, data_limite):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO metas (titulo, categoria, data_limite, progresso, status)
        VALUES (?, ?, ?, 0, 'ativa')
    """, (titulo, categoria, data_limite))
    conn.commit()

def listar_metas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM metas ORDER BY status ASC, data_limite ASC")
    dados = cursor.fetchall()
    return dados

def atualizar_progresso(id_meta, progresso_atual, incremento):
    novo_progresso = progresso_atual + incremento
    if novo_progresso > 100:
        novo_progresso = 100
    
    status = 'concluída' if novo_progresso == 100 else 'ativa'
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE metas
        SET progresso = ?, status = ?
        WHERE id = ?
    """, (novo_progresso, status, id_meta))
    conn.commit()

def excluir_meta(id_meta):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM metas WHERE id = ?", (id_meta,))
    conn.commit()