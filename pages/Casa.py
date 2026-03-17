import streamlit as st
import pandas as pd
from datetime import date

# Importando os serviços
from services.casa_service import adicionar_compra, listar_compras, marcar_comprado, excluir_compra

# Importando o visual D.Tech (O mesmo que usamos no app corporativo)
from components.cards import metric_card, icon_svg

st.title("🏠 Compras da Casa")
st.markdown("<span style='color: #A0AEC0;'>Gerencie o que falta comprar para a casa, desde a reforma até a decoração.</span>", unsafe_allow_html=True)
st.divider()

# ==================================
# 1) KPIs - O VISUAL PREMIUM
# ==================================
dados = listar_compras()
df = pd.DataFrame(dados, columns=["ID", "Item", "Categoria", "Preço", "Data", "Status"]) if dados else pd.DataFrame()

# Cálculos rápidos
total_itens = len(df)
itens_pendentes = len(df[df["Status"] == "pendente"]) if not df.empty else 0
valor_pendente = df[df["Status"] == "pendente"]["Preço"].sum() if not df.empty else 0.0

col1, col2, col3 = st.columns(3)
with col1:
    metric_card("Total Planejado", f"{total_itens} itens", "Na sua lista de desejos", "gray", icon_svg("trend"))
with col2:
    metric_card("Falta Comprar", f"{itens_pendentes} itens", "Pendentes", "red" if itens_pendentes > 0 else "green", icon_svg("out"))
with col3:
    metric_card("Investimento Pendente", f"R$ {valor_pendente:,.2f}", "Previsão de gasto", "red", icon_svg("wallet"))

st.write("")

# ==================================
# 2) FORMULÁRIO DE CADASTRO
# ==================================
with st.expander("➕ Adicionar Novo Item", expanded=False):
    with st.form("form_compra", clear_on_submit=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        
        with c1:
            item = st.text_input("O que precisa comprar?")
        with c2:
            categoria = st.selectbox("Categoria", ["Móveis", "Eletrodoméstico", "Cozinha", "Decoração", "Reforma", "Outros"])
        with c3:
            preco = st.number_input("Preço Médio (R$)", min_value=0.0, step=50.0)

        data = st.date_input("Até quando quer comprar?")
        salvar = st.form_submit_button("💾 Salvar na Lista", type="primary")

        if salvar and item:
            adicionar_compra(item, categoria, preco, data)
            st.success(f"'{item}' adicionado com sucesso!")
            st.rerun()

st.divider()

# ==================================
# 3) LISTA DE COMPRAS INTERATIVA
# ==================================
st.subheader("📋 Sua Lista")

if not df.empty:
    # Separa os pendentes dos comprados
    df_pendentes = df[df["Status"] == "pendente"].sort_values(by="Data")
    df_comprados = df[df["Status"] == "comprado"]

    if not df_pendentes.empty:
        st.markdown("#### ⏳ Pendentes")
        for i, row in df_pendentes.iterrows():
            # Cria um "cardzinho" para cada item usando colunas
            with st.container():
                c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
                c1.markdown(f"**{row['Item']}** <br> <span style='font-size:12px; color:#A0AEC0;'>{row['Categoria']}</span>", unsafe_allow_html=True)
                c2.markdown(f"**R$ {row['Preço']:,.2f}**")
                c3.markdown(f"📅 {pd.to_datetime(row['Data']).strftime('%d/%m/%Y')}")
                
                with c4:
                    # Botões lado a lado
                    b1, b2 = st.columns(2)
                    if b1.button("✅", key=f"comprar_{row['ID']}", help="Marcar como comprado"):
                        marcar_comprado(row['ID'])
                        st.rerun()
                    if b2.button("🗑️", key=f"del_{row['ID']}", help="Excluir item"):
                        excluir_compra(row['ID'])
                        st.rerun()
                st.markdown("<hr style='margin: 0; opacity: 0.2;'>", unsafe_allow_html=True)

    if not df_comprados.empty:
        st.write("")
        st.markdown("#### 🎉 Já Comprados")
        for i, row in df_comprados.iterrows():
            st.markdown(f"<span style='text-decoration: line-through; color: #A0AEC0;'>{row['Item']} - R$ {row['Preço']:,.2f}</span>", unsafe_allow_html=True)
            
else:
    st.info("Sua casa está completa! Nenhuma compra cadastrada.")