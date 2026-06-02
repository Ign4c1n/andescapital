import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

st.set_page_config(
    page_title="Andes Capital | Radar Bursátil",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

root = Path(__file__).parent
html = (root / "index.html").read_text(encoding="utf-8")
css = (root / "styles.css").read_text(encoding="utf-8")
js = (root / "app.js").read_text(encoding="utf-8")
logo_path = root / "assets" / "andes_capital_logo.png"

logo_data = ""
if logo_path.exists():
    logo_data = "data:image/png;base64," + base64.b64encode(logo_path.read_bytes()).decode("utf-8")

# Inline assets so Streamlit Cloud can render the same design without static routing issues.
html = html.replace('<link rel="stylesheet" href="styles.css"/>', f"<style>{css}</style>")
html = html.replace('<script src="app.js"></script>', f"<script>{js}</script>")
html = html.replace('src="assets/andes_capital_logo.png"', f'src="{logo_data}"')

# Remove external font dependency gracefully; Inter will be used if available.
html = html.replace('<link rel="preconnect" href="https://fonts.googleapis.com">', '')
html = html.replace('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>', '')
html = html.replace('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">', '')

st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}
.block-container {padding:0 !important; max-width:100% !important;}
iframe {display:block;}
</style>
""", unsafe_allow_html=True)

components.html(html, height=1080, scrolling=True)
