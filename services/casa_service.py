from database.database import get_connection


# ==========================
# ADICIONAR COMPRA
# ==========================

def adicionar_compra(item, categoria, preco, data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO compras (item, categoria, preco, data_compra, status)
        VALUES (?, ?, ?, ?, 'pendente')
    """, (item, categoria, preco, data))

    conn.commit()
    conn.close()


# ==========================
# LISTAR COMPRAS
# ==========================

def listar_compras():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM compras")

    dados = cursor.fetchall()

    conn.close()

    return dados


# ==========================
# MARCAR COMO COMPRADO
# ==========================

def marcar_comprado(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE compras
        SET status = 'comprado'
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()


# ==========================
# EXCLUIR ITEM
# ==========================

def excluir_compra(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM compras
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()