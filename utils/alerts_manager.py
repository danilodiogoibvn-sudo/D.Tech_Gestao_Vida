import pandas as pd
from datetime import date
from services.casa_service import listar_compras
from services.metas_service import listar_metas
from services.habitos_service import listar_habitos

def verificar_alertas():
    alertas = []
    hoje = date.today()

    # 1. Alertas de Compras da Casa
    compras = listar_compras()
    if compras:
        df_c = pd.DataFrame(compras, columns=["ID", "Item", "Categoria", "Preco", "Data", "Status"])
        pendentes = df_c[df_c["Status"] == "pendente"]
        if not pendentes.empty:
            alertas.append(f"🛒 Você tem **{len(pendentes)} item(ns)** pendente(s) na lista de compras para a casa.")

    # 2. Alertas de Metas
    metas = listar_metas()
    if metas:
        df_m = pd.DataFrame(metas, columns=["ID", "Titulo", "Categoria", "Data", "Progresso", "Status"])
        df_m["Data"] = pd.to_datetime(df_m["Data"]).dt.date
        ativas = df_m[df_m["Status"] == "ativa"]
        
        for _, row in ativas.iterrows():
            dias_restantes = (row["Data"] - hoje).days
            if 0 <= dias_restantes <= 7:
                alertas.append(f"🎯 Atenção: A meta **'{row['Titulo']}'** vence em {dias_restantes} dia(s)!")
            elif dias_restantes < 0:
                alertas.append(f"🚨 A meta **'{row['Titulo']}'** está atrasada!")

    # 3. Alertas de Hábitos (Risco de perder a ofensiva)
    habitos = listar_habitos()
    if habitos:
        df_h = pd.DataFrame(habitos, columns=["ID", "Nome", "Frequencia", "Ofensiva", "Ultima_vez"])
        for _, row in df_h.iterrows():
            if row["Ofensiva"] > 0 and row["Ultima_vez"]:
                ultima = pd.to_datetime(row["Ultima_vez"]).date()
                dias_sem_fazer = (hoje - ultima).days
                
                if dias_sem_fazer == 1:
                    alertas.append(f"🔥 Não quebre o ritmo! Faça o check-in de **'{row['Nome']}'** hoje para manter sua ofensiva de {row['Ofensiva']} dias.")
                elif dias_sem_fazer > 1:
                    alertas.append(f"🧊 Você perdeu a ofensiva do hábito **'{row['Nome']}'**. Volte aos treinos hoje!")

    return alertas