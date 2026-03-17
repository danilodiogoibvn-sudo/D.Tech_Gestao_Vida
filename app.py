import sys
import os
import streamlit as st
import pandas as pd

# Adiciona o diretório atual ao path do Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importações do nosso ecossistema
from database.database import criar_tabelas
from utils.alerts_manager import verificar_alertas
from components.cards import metric_card, icon_svg

# Importações dos serviços para puxar os números totais
from services.casa_service import listar_compras
from services.metas_service import listar_metas
from services.habitos_service import listar_habitos

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="D-Tech | Gestão de Vida",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# INICIALIZAÇÃO
# ==========================================
# Garante que as tabelas existam
criar_tabelas()

# Menu lateral com a logo
with st.sidebar:
    try:
        st.image("assets/logo.png", width=150)
    except:
        st.markdown("## D.Tech")
    st.markdown("---")
    st.markdown("Use o menu acima para navegar.")

# ==========================================
# HEADER
# ==========================================
st.title("🏠 D-Tech | Gestão de Vida")
st.markdown("<span style='color: #A0AEC0;'>Seu painel de controle pessoal. Organização, metas e rotina em um só lugar.</span>", unsafe_allow_html=True)
st.divider()

# ==========================================
# CÁLCULO DOS RESUMOS (KPIs)
# ==========================================
# Compras
compras = listar_compras()
df_compras = pd.DataFrame(compras, columns=["ID", "Item", "Cat", "Preco", "Data", "Status"]) if compras else pd.DataFrame()
compras_pendentes = len(df_compras[df_compras["Status"] == "pendente"]) if not df_compras.empty else 0

# Metas
metas = listar_metas()
df_metas = pd.DataFrame(metas, columns=["ID", "Titulo", "Cat", "Data", "Progresso", "Status"]) if metas else pd.DataFrame()
metas_ativas = len(df_metas[df_metas["Status"] == "ativa"]) if not df_metas.empty else 0
metas_concluidas = len(df_metas[df_metas["Status"] == "concluída"]) if not df_metas.empty else 0

# Hábitos
habitos = listar_habitos()
df_habitos = pd.DataFrame(habitos, columns=["ID", "Nome", "Freq", "Ofensiva", "Ultima"]) if habitos else pd.DataFrame()
maior_ofensiva = df_habitos["Ofensiva"].max() if not df_habitos.empty else 0

# ==========================================
# DASHBOARD VISUAL (CARDS PREMIUM)
# ==========================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Compras Pendentes", f"{compras_pendentes}", "Para a Casa", "gray", icon_svg("out"))
with col2:
    metric_card("Metas Ativas", f"{metas_ativas}", "Em andamento", "red" if metas_ativas > 0 else "gray", icon_svg("trend"))
with col3:
    metric_card("Vitórias", f"{metas_concluidas}", "Metas concluídas", "green", icon_svg("up"))
with col4:
    metric_card("Melhor Ofensiva", f"{maior_ofensiva} dias 🔥", "Nos Hábitos", "red" if maior_ofensiva > 0 else "gray", icon_svg("in"))

st.write("")

# ==========================================
# ALERTAS INTELIGENTES
# ==========================================
alertas = verificar_alertas()

if alertas:
    st.subheader("🔔 Seus Alertas de Hoje")
    for alerta in alertas:
        # Pinta de vermelho se for aviso de atraso, senão pinta de laranja/azul
        if "🚨" in alerta or "🧊" in alerta:
            st.error(alerta)
        elif "🔥" in alerta or "🎯" in alerta:
            st.warning(alerta)
        else:
            st.info(alerta)
else:
    st.success("Tudo tranquilo por aqui! Nenhuma pendência urgente ou meta atrasada. 🎉")
