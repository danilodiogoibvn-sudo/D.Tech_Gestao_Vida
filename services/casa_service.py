from database.database import get_db_cursor

def adicionar_compra(item, categoria, preco, data):
    conn, cursor = get_db_cursor()
    if not cursor: return False
    try:
        cursor.execute("""
            INSERT INTO compras (item, categoria, preco, data_compra, status)
            VALUES (%s, %s, %s, %s, 'pendente')
        """, (item, categoria, preco, data))
        return True
    except Exception as e:
        print(f"Erro ao adicionar compra: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def listar_compras():
    conn, cursor = get_db_cursor()
    if not cursor: return []
    try:
        cursor.execute("SELECT id, item, categoria, preco, data_compra, status FROM compras ORDER BY id DESC")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar compras: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def marcar_comprado(id):
    conn, cursor = get_db_cursor()
    if not cursor: return False
    try:
        cursor.execute("UPDATE compras SET status = 'comprado' WHERE id = %s", (id,))
        return True
    except Exception as e:
        print(f"Erro ao marcar comprado: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def excluir_compra(id):
    conn, cursor = get_db_cursor()
    if not cursor: return False
    try:
        cursor.execute("DELETE FROM compras WHERE id = %s", (id,))
        return True
    except Exception as e:
        print(f"Erro ao excluir compra: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
