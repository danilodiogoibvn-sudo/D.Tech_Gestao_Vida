from database.database import get_connection

def adicionar_meta(titulo, categoria, data_limite):
    conn = get_connection()
    if conn is None: return False
    cursor = conn.cursor()
    
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
    conn = get_connection()
    if conn is None: return []
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM metas ORDER BY status ASC, data_limite ASC")
        dados = cursor.fetchall()
        return dados
    except Exception as e:
        print(f"Erro ao listar metas: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def atualizar_progresso(id_meta, progresso_atual, incremento):
    novo_progresso = progresso_atual + incremento
    if novo_progresso > 100:
        novo_progresso = 100
    
    status = 'concluída' if novo_progresso == 100 else 'ativa'
    
    conn = get_connection()
    if conn is None: return False
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE metas
            SET progresso = %s, status = %s
            WHERE id = %s
        """, (novo_progresso, status, id_meta))
        return True
    except Exception as e:
        print(f"Erro ao atualizar progresso: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def excluir_meta(id_meta):
    conn = get_connection()
    if conn is None: return False
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM metas WHERE id = %s", (id_meta,))
        return True
    except Exception as e:
        print(f"Erro ao excluir meta: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
