from database.database import get_connection

# ==========================
# ADICIONAR COMPRA
# ==========================
def adicionar_compra(item, categoria, preco, data):
    conn = get_connection()
    if conn is None: return False
    cursor = conn.cursor()
    
    try:
        # Trocado ? por %s
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

# ==========================
# LISTAR COMPRAS
# ==========================
def listar_compras():
    conn = get_connection()
    if conn is None: return []
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM compras")
        dados = cursor.fetchall()
        return dados
    except Exception as e:
        print(f"Erro ao listar compras: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# ==========================
# MARCAR COMO COMPRADO
# ==========================
def marcar_comprado(id):
    conn = get_connection()
    if conn is None: return False
    cursor = conn.cursor()
    
    try:
        # Trocado ? por %s
        cursor.execute("""
            UPDATE compras
            SET status = 'comprado'
            WHERE id = %s
        """, (id,))
        return True
    except Exception as e:
        print(f"Erro ao marcar comprado: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# ==========================
# EXCLUIR ITEM
# ==========================
def excluir_compra(id):
    conn = get_connection()
    if conn is None: return False
    cursor = conn.cursor()
    
    try:
        # Trocado ? por %s
        cursor.execute("""
            DELETE FROM compras
            WHERE id = %s
        """, (id,))
        return True
    except Exception as e:
        print(f"Erro ao excluir compra: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
