import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Andes Capital | Radar Bursátil",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ROOT = Path(__file__).parent

def b64(path):
    p = ROOT / path
    if not p.exists():
        return ""
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode("utf-8")

html = (ROOT / "index.html").read_text(encoding="utf-8")
css = (ROOT / "styles.css").read_text(encoding="utf-8")
js = (ROOT / "app.js").read_text(encoding="utf-8")

# Inline everything for Streamlit Cloud
html = html.replace('<link rel="stylesheet" href="styles.css"/>', f"<style>{css}</style>")
html = html.replace('<script src="app.js"></script>', f"<script>{js}</script>")
html = html.replace('src="assets/andes_capital_logo.png"', f'src="{b64("assets/andes_capital_logo.png")}"')
html = html.replace("url('assets/andes_hero_mountain.png')", f"url('{b64('assets/andes_hero_mountain.png')}')")
html = html.replace("url('assets/ad_mountain_1.png')", f"url('{b64('assets/ad_mountain_1.png')}')")
html = html.replace("url('assets/ad_mountain_2.png')", f"url('{b64('assets/ad_mountain_2.png')}')")

st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}
.block-container {padding:0 !important; max-width:100% !important;}
iframe {display:block;}
</style>
""", unsafe_allow_html=True)

components.html(html, height=980, scrolling=True)
