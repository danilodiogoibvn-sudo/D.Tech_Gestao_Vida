import streamlit as st

def icon_svg(name: str) -> str:
    """Retorna o código SVG do ícone solicitado."""
    icons = {
        "wallet": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"/></svg>""",
        "in": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"></polyline></svg>""",
        "out": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>""",
        "trend": """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline></svg>"""
    }
    return icons.get(name, "")

def metric_card(title: str, value: str, subtitle: str, color_theme: str = "green", icon: str = ""):
    """Desenha o card premium no estilo D.Tech."""
    # Define as cores baseadas no tema escolhido
    if color_theme == "green":
        border_color = "rgba(0, 204, 150, 0.3)"
        bg_color = "rgba(0, 204, 150, 0.05)"
        text_color = "#00CC96"
    elif color_theme == "red":
        border_color = "rgba(255, 75, 75, 0.3)"
        bg_color = "rgba(255, 75, 75, 0.05)"
        text_color = "#FF4B4B"
    elif color_theme == "gray":
        border_color = "rgba(160, 174, 192, 0.3)"
        bg_color = "rgba(160, 174, 192, 0.05)"
        text_color = "#A0AEC0"
    else: # Padrão / Ciano
        border_color = "rgba(0, 209, 255, 0.3)"
        bg_color = "rgba(0, 209, 255, 0.05)"
        text_color = "#00D1FF"

    html = f"""
    <div style="
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 18px;
        background-color: {bg_color};
        margin-bottom: 12px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="color: #A0AEC0; font-size: 14px; font-weight: 600;">{title}</span>
            <span style="color: {text_color}; opacity: 0.8;">{icon}</span>
        </div>
        <div style="font-size: 26px; font-weight: 800; color: #FFFFFF; margin-bottom: 4px;">
            {value}
        </div>
        <div style="font-size: 13px; color: #A0AEC0; opacity: 0.8;">
            {subtitle}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)