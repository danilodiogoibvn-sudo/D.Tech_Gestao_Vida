import streamlit as st
import pandas as pd

# Importando o nosso motor
from services.metas_service import adicionar_meta, listar_metas, atualizar_progresso, excluir_meta
# Importando o visual premium
from components.cards import metric_card, icon_svg

st.title("🎯 Minhas Metas")
st.markdown("<span style='color: #A0AEC0;'>Acompanhe seus objetivos pessoais, financeiros e de aprendizado.</span>", unsafe_allow_html=True)
st.divider()

# ==================================
# 1) KPIs DE METAS
# ==================================
dados = listar_metas()
df = pd.DataFrame(dados, columns=["ID", "Título", "Categoria", "Data Limite", "Progresso", "Status"]) if dados else pd.DataFrame()

ativas = len(df[df["Status"] == "ativa"]) if not df.empty else 0
concluidas = len(df[df["Status"] == "concluída"]) if not df.empty else 0

col1, col2, col3 = st.columns(3)
with col1:
    metric_card("Metas Ativas", f"{ativas}", "Em andamento", "gray", icon_svg("trend"))
with col2:
    metric_card("Metas Concluídas", f"{concluidas}", "Vitórias alcançadas", "green", icon_svg("up"))
with col3:
    tx_sucesso = (concluidas / (ativas + concluidas) * 100) if (ativas + concluidas) > 0 else 0
    metric_card("Taxa de Sucesso", f"{tx_sucesso:.0f}%", "Aproveitamento", "green" if tx_sucesso >= 50 else "red", icon_svg("in"))

st.write("")

# ==================================
# 2) FORMULÁRIO DE NOVA META
# ==================================
with st.expander("➕ Criar Novo Objetivo", expanded=False):
    with st.form("form_meta", clear_on_submit=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        
        with c1:
            titulo = st.text_input("Qual é a sua meta? (Ex: Ler 12 livros, Juntar 10k)")
        with c2:
            categoria = st.selectbox("Categoria", ["Financeira", "Aprendizado", "Saúde", "Viagem", "Pessoal"])
        with c3:
            data = st.date_input("Data Limite")

        salvar = st.form_submit_button("🚀 Iniciar Meta", type="primary")

        if salvar and titulo:
            adicionar_meta(titulo, categoria, data)
            st.success("Meta criada! Foco e disciplina! 💪")
            st.rerun()

st.divider()

# ==================================
# 3) ACOMPANHAMENTO VISUAL
# ==================================
st.subheader("📊 Progresso Atual")

if not df.empty:
    df_ativas = df[df["Status"] == "ativa"]
    df_concluidas = df[df["Status"] == "concluída"]

    if not df_ativas.empty:
        for i, row in df_ativas.iterrows():
            with st.container():
                st.markdown(f"**{row['Título']}** <span style='font-size:12px; color:#A0AEC0;'>• {row['Categoria']} • Prazo: {pd.to_datetime(row['Data Limite']).strftime('%d/%m/%Y')}</span>", unsafe_allow_html=True)
                
                # A mágica da barra de progresso visual
                st.progress(row['Progresso'] / 100.0)
                
                c1, c2, c3, c4 = st.columns([1, 1, 1, 6])
                with c1:
                    if st.button("➕ 10%", key=f"p10_{row['ID']}", help="Avançar 10%"):
                        atualizar_progresso(row['ID'], row['Progresso'], 10)
                        st.rerun()
                with c2:
                    if st.button("➕ 25%", key=f"p25_{row['ID']}", help="Avançar 25%"):
                        atualizar_progresso(row['ID'], row['Progresso'], 25)
                        st.rerun()
                with c3:
                    if st.button("🗑️", key=f"del_{row['ID']}", help="Excluir meta"):
                        excluir_meta(row['ID'])
                        st.rerun()
                with c4:
                    st.markdown(f"<div style='text-align: right; color:#00D1FF; font-weight:bold;'>{row['Progresso']}%</div>", unsafe_allow_html=True)
                
                st.write("") # Espaçamento
    
    if not df_concluidas.empty:
        st.write("---")
        st.markdown("#### 🏆 Conquistas")
        for i, row in df_concluidas.iterrows():
            st.markdown(f"✅ **{row['Título']}** <span style='color:#00CC96;'>(100% Concluída)</span>", unsafe_allow_html=True)

else:
    st.info("Nenhuma meta ativa. Que tal definir seu primeiro objetivo hoje?")