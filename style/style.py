import streamlit as st

def load_styles():

    st.markdown("""
    <style>

    /* ========================================
       FUNDO GERAL
    ======================================== */

    .stApp {
        background-color: #0E1117;
        color: white;
        font-family: "Source Sans 3", sans-serif;
    }

    /* ========================================
       SIDEBAR
    ======================================== */

    section[data-testid="stSidebar"] {
        background-color: #0B0F14;
        border-right: 1px solid #1F2937;
    }

    section[data-testid="stSidebar"] * {
        color: #A0AEC0;
    }

    section[data-testid="stSidebar"] a:hover {
        color: #00D1FF;
    }

    /* ========================================
       TÍTULOS
    ======================================== */

    h1, h2, h3 {
        color: #00D1FF;
        font-weight: 600;
    }

    /* ========================================
       TEXTO SECUNDÁRIO
    ======================================== */

    p, span {
        color: #A0AEC0;
    }

    /* ========================================
       CARDS KPI
    ======================================== */

    div[data-testid="stMetric"] {

        background-color: #161B22;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);

    }

    /* ========================================
       BOTÕES
    ======================================== */

    .stButton>button {

        background-color: #00D1FF;
        color: black;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
        font-weight: 600;

    }

    .stButton>button:hover {

        background-color: #00A6CC;
        color: white;

    }

    /* ========================================
       ALERTAS
    ======================================== */

    .stAlert {

        border-radius: 10px;

    }

    /* ========================================
       INPUTS
    ======================================== */

    input, textarea {

        background-color: #161B22 !important;
        color: white !important;
        border: 1px solid #1F2937 !important;
        border-radius: 6px !important;

    }

    /* ========================================
       TABELAS
    ======================================== */

    .stDataFrame {

        background-color: #161B22;

    }

    </style>
    """, unsafe_allow_html=True)