from database.database import get_db_cursor

def adicionar_meta(titulo, categoria, data_limite):
    conn, cursor = get_db_cursor()
    if not cursor: return False
    try:
        cursor.execute("""
            INSERT INTO metas (titulo, categoria, data_limite, progresso, status)
            VALUES (%s, %s, %s, 0, 'ativa')
        """, (titulo, categoria, data_limite))
        return True
    except Exception as e:
        print(f"Erro ao adicionar meta: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def listar_metas():
    conn, cursor = get_db_cursor()
    if not cursor: return []
    try:
        cursor.execute("SELECT id, titulo, categoria, data_limite, progresso, status FROM metas ORDER BY status ASC, data_limite ASC")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar metas: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def atualizar_progresso(id_meta, progresso_atual, incremento):
    novo_progresso = min(progresso_atual + incremento, 100)
    status = 'concluída' if novo_progresso == 100 else 'ativa'
    
    conn, cursor = get_db_cursor()
    if not cursor: return False
    try:
        cursor.execute("UPDATE metas SET progresso = %s, status = %s WHERE id = %s", (novo_progresso, status, id_meta))
        return True
    except Exception as e:
        print(f"Erro ao atualizar progresso: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def excluir_meta(id_meta):
    conn, cursor = get_db_cursor()
    if not cursor: return False
    try:
        cursor.execute("DELETE FROM metas WHERE id = %s", (id_meta,))
        return True
    except Exception as e:
        print(f"Erro ao excluir meta: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
