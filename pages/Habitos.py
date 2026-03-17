import streamlit as st
import pandas as pd
from datetime import date

# Importando o motor de hábitos
from services.habitos_service import adicionar_habito, listar_habitos, fazer_checkin, excluir_habito
# Importando o visual D.Tech
from components.cards import metric_card, icon_svg

st.title("🏃 Rastreador de Hábitos")
st.markdown("<span style='color: #A0AEC0;'>Construa a sua disciplina diária. Não quebre a ofensiva! 🔥</span>", unsafe_allow_html=True)
st.divider()

# ==================================
# 1) KPIs DE HÁBITOS
# ==================================
dados = listar_habitos()
df = pd.DataFrame(dados, columns=["ID", "Nome", "Frequência", "Ofensiva", "Última Vez"]) if dados else pd.DataFrame()

total_habitos = len(df)
maior_ofensiva = df["Ofensiva"].max() if not df.empty else 0

col1, col2, col3 = st.columns(3)
with col1:
    metric_card("Hábitos Ativos", f"{total_habitos}", "Na sua rotina", "gray", icon_svg("trend"))
with col2:
    metric_card("Maior Ofensiva", f"{maior_ofensiva} dias 🔥", "O seu melhor recorde", "red" if maior_ofensiva > 0 else "gray", icon_svg("up"))
with col3:
    # Apenas ilustrativo para completar o design
    metric_card("Disciplina", "Foco 100%", "Mantenha o ritmo", "green", icon_svg("wallet"))

st.write("")

# ==================================
# 2) ADICIONAR NOVO HÁBITO
# ==================================
with st.expander("➕ Criar Novo Hábito", expanded=False):
    with st.form("form_habito", clear_on_submit=True):
        c1, c2 = st.columns([3, 1])
        
        with c1:
            nome = st.text_input("Qual hábito quer construir? (Ex: Ler 10 páginas, Treinar)")
        with c2:
            frequencia = st.selectbox("Frequência", ["Diária", "Semanal"])

        salvar = st.form_submit_button("🌱 Começar", type="primary")

        if salvar and nome:
            adicionar_habito(nome, frequencia)
            st.success("Hábito criado! O primeiro dia começa hoje.")
            st.rerun()

st.divider()

# ==================================
# 3) LISTA DE HÁBITOS & CHECK-IN
# ==================================
st.subheader("✅ Check-in Diário")

if not df.empty:
    hoje = date.today().isoformat()
    
    for i, row in df.iterrows():
        with st.container():
            c1, c2, c3 = st.columns([3, 1, 1])
            
            # Texto do Hábito
            c1.markdown(f"**{row['Nome']}** <br> <span style='font-size:12px; color:#A0AEC0;'>{row['Frequência']}</span>", unsafe_allow_html=True)
            
            # Foguinho da Ofensiva 🔥
            ofensiva = row['Ofensiva']
            cor_fogo = "#FF4B4B" if ofensiva > 0 else "#A0AEC0"
            c2.markdown(f"<div style='font-size: 20px; color: {cor_fogo}; font-weight: bold;'>🔥 {ofensiva}</div>", unsafe_allow_html=True)
            
            # Botões de Ação
            with c3:
                # Verifica se já fez check-in hoje
                ja_fez_hoje = str(row['Última Vez']) == hoje
                
                b1, b2 = st.columns(2)
                
                if ja_fez_hoje:
                    b1.button("✔️", key=f"ok_{row['ID']}", disabled=True, help="Check-in já feito hoje!")
                else:
                    if b1.button("✅", key=f"check_{row['ID']}", help="Fazer check-in"):
                        fazer_checkin(row['ID'], row['Ofensiva'])
                        st.rerun()
                        
                if b2.button("🗑️", key=f"del_{row['ID']}", help="Excluir hábito"):
                    excluir_habito(row['ID'])
                    st.rerun()
            
            st.markdown("<hr style='margin: 0; opacity: 0.2;'>", unsafe_allow_html=True)

else:
    st.info("Nenhum hábito cadastrado. Vamos criar o seu primeiro?")