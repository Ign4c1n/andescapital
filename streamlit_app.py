
import base64
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

try:
    import yfinance as yf
except Exception:
    yf = None


# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Andes Capital | Radar Bursátil",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).parent
LOGO_PATH = ROOT / "assets" / "andes_capital_logo.png"

DEFAULT_ASSETS = [
    {"ticker": "SQM-B.SN", "name": "SQM-B", "company": "Soc. Química y Minera de Chile"},
    {"ticker": "COPEC.SN", "name": "COPEC", "company": "Empresas Copec S.A."},
    {"ticker": "FALABELLA.SN", "name": "FALABELLA", "company": "Falabella S.A."},
    {"ticker": "CENCOSUD.SN", "name": "CENCOSUD", "company": "Cencosud S.A."},
    {"ticker": "CHILE.SN", "name": "CHILE", "company": "Banco de Chile"},
    {"ticker": "BSANTANDER.SN", "name": "BSANTANDER", "company": "Banco Santander Chile"},
    {"ticker": "BCI.SN", "name": "BCI", "company": "Banco de Crédito e Inversiones"},
    {"ticker": "ITAUCL.SN", "name": "ITAUCL", "company": "Itaú Chile"},
    {"ticker": "ENELCHILE.SN", "name": "ENELCHILE", "company": "Enel Chile S.A."},
    {"ticker": "ENELAM.SN", "name": "ENELAM", "company": "Enel Américas S.A."},
    {"ticker": "COLBUN.SN", "name": "COLBUN", "company": "Colbún S.A."},
    {"ticker": "ENGIE.SN", "name": "ENGIE", "company": "Engie Energía Chile S.A."},
    {"ticker": "CMPC.SN", "name": "CMPC", "company": "Empresas CMPC S.A."},
    {"ticker": "CAP.SN", "name": "CAP", "company": "CAP S.A."},
    {"ticker": "VAPORES.SN", "name": "VAPORES", "company": "Compañía Sud Americana de Vapores"},
    {"ticker": "SONDA.SN", "name": "SONDA", "company": "Sonda S.A."},
    {"ticker": "ENTEL.SN", "name": "ENTEL", "company": "Empresa Nacional de Telecomunicaciones"},
    {"ticker": "ANDINA-B.SN", "name": "ANDINA-B", "company": "Embotelladora Andina S.A."},
    {"ticker": "CCU.SN", "name": "CCU", "company": "Compañía Cervecerías Unidas"},
    {"ticker": "CONCHATORO.SN", "name": "CONCHATORO", "company": "Viña Concha y Toro S.A."},
    {"ticker": "ILC.SN", "name": "ILC", "company": "Inversiones La Construcción S.A."},
    {"ticker": "MALLPLAZA.SN", "name": "MALLPLAZA", "company": "Plaza S.A."},
    {"ticker": "PARAUCO.SN", "name": "PARAUCO", "company": "Parque Arauco S.A."},
    {"ticker": "CENCOSHOPP.SN", "name": "CENCOSHOPP", "company": "Cencosud Shopping S.A."},
    {"ticker": "RIPLEY.SN", "name": "RIPLEY", "company": "Ripley Corp S.A."},
    {"ticker": "SMU.SN", "name": "SMU", "company": "SMU S.A."},
    {"ticker": "SALFACORP.SN", "name": "SALFACORP", "company": "Salfacorp S.A."},
    {"ticker": "SECURITY.SN", "name": "SECURITY", "company": "Grupo Security S.A."},
    {"ticker": "LTM.SN", "name": "LTM", "company": "LATAM Airlines Group S.A."},
]

MARKET_INDEXES = [
    {"ticker": "^GSPC", "name": "S&P 500"},
    {"ticker": "^DJI", "name": "DOW JONES"},
    {"ticker": "^IXIC", "name": "NASDAQ"},
    {"ticker": "CLP=X", "name": "USD/CLP"},
    {"ticker": "HG=F", "name": "Cobre"},
    {"ticker": "BZ=F", "name": "Brent"},
    {"ticker": "GC=F", "name": "Oro"},
]


# =========================================================
# CSS / BRAND
# =========================================================

def logo_base64() -> str:
    if LOGO_PATH.exists():
        return "data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode("utf-8")
    return ""


LOGO_DATA = logo_base64()

st.markdown(
    """
<style>
:root {
  --navy-950:#001127;
  --navy-900:#001833;
  --navy-850:#001f43;
  --navy-800:#062b57;
  --panel:rgba(8,43,85,.70);
  --panel-2:rgba(9,47,93,.78);
  --line:rgba(151,184,230,.16);
  --line-2:rgba(151,184,230,.25);
  --white:#f7fbff;
  --muted:#b8c6dc;
  --muted-2:#8293b2;
  --red:#d82835;
  --red-2:#9d1b27;
  --green:#2bd981;
  --yellow:#ffd34f;
  --blue:#4d8dff;
}

html, body, [class*="css"] {
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.stApp {
  background:
    radial-gradient(circle at 72% 4%, rgba(95,146,225,.20), transparent 27%),
    radial-gradient(circle at 18% 48%, rgba(0,80,158,.26), transparent 29%),
    linear-gradient(180deg,#00142c 0%, #001c3c 45%, #001124 100%);
  color: var(--white);
}

#MainMenu, header, footer { visibility:hidden; }
.block-container {
  padding-top: 1.2rem !important;
  padding-bottom: 2rem !important;
  max-width: 100% !important;
}

.andes-topbar {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:1.6rem;
  padding:0.3rem 1.1rem 1.1rem 1.1rem;
  border-bottom:1px solid var(--line);
  margin-bottom:1.0rem;
}

.andes-logo {
  width:148px;
  height:auto;
  display:block;
}

.andes-top-right {
  display:flex;
  align-items:center;
  gap:1rem;
  color:var(--muted);
  font-size:.86rem;
}

.status-pill {
  border:1px solid var(--line-2);
  background:rgba(255,255,255,.04);
  color:#dce8ff;
  border-radius:999px;
  padding:.55rem .85rem;
  font-weight:700;
}

.disclaimer-pill {
  border:1px solid rgba(216,40,53,.45);
  background:rgba(216,40,53,.11);
  color:#ffd9dd;
  border-radius:999px;
  padding:.55rem .85rem;
  font-weight:800;
}

.nav-row {
  display:flex;
  gap:.65rem;
  padding:.1rem 1.1rem 1.0rem 1.1rem;
}

div[data-testid="stButton"] > button {
  border-radius:8px;
  border:1px solid rgba(151,184,230,.20);
  background:rgba(9,47,93,.62);
  color:#edf5ff;
  font-weight:800;
  padding:.68rem 1rem;
}

div[data-testid="stButton"] > button:hover {
  border-color:rgba(216,40,53,.75);
  color:white;
  background:rgba(216,40,53,.22);
}

.andes-hero {
  min-height:310px;
  border:1px solid var(--line);
  border-radius:18px;
  padding:2.6rem 2.4rem;
  background:
    linear-gradient(105deg, rgba(0,29,61,.98), rgba(0,29,61,.86), rgba(216,40,53,.10)),
    radial-gradient(circle at 82% 10%, rgba(255,255,255,.15), transparent 28%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 20px 60px rgba(0,0,0,.16);
}

.andes-hero h1 {
  font-size:3.4rem;
  line-height:1.04;
  letter-spacing:-.045em;
  margin:0;
  color:white;
  font-weight:850;
}

.red-line {
  width:64px;
  height:4px;
  background:var(--red);
  margin:1.35rem 0 1.0rem 0;
}

.andes-hero p {
  color:#d9e4f4;
  font-size:1.03rem;
  line-height:1.58;
  max-width:720px;
  margin:0;
}

.timestamp {
  margin-top:2.2rem!important;
  color:#aebdd4!important;
  font-size:.86rem!important;
}

.kpi-card {
  min-height:124px;
  background:linear-gradient(180deg,rgba(12,53,101,.72),rgba(8,40,80,.64));
  border:1px solid var(--line);
  border-radius:12px;
  padding:1.1rem 1.25rem;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.04);
}

.kpi-label {
  color:#d9e4f5;
  font-size:.72rem;
  text-transform:uppercase;
  letter-spacing:.08em;
  font-weight:850;
}

.kpi-value {
  color:white;
  font-size:2.0rem;
  line-height:1.15;
  font-weight:850;
  margin-top:.28rem;
}

.kpi-note {
  color:#8fb4ef;
  font-size:.82rem;
  margin-top:.35rem;
  font-weight:700;
}

.panel {
  background:linear-gradient(180deg,rgba(9,46,91,.78),rgba(7,35,70,.70));
  border:1px solid var(--line);
  border-radius:12px;
  padding:1.25rem;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 20px 60px rgba(0,0,0,.16);
}

.panel h2, .panel h3 {
  color:white;
  margin-top:0;
}

.small-red-line {
  width:42px;
  height:3px;
  background:var(--red);
  margin:.65rem 0 1.3rem 0;
}

.signal {
  display:inline-flex;
  align-items:center;
  justify-content:center;
  min-width:86px;
  height:30px;
  border-radius:5px;
  font-weight:900;
  font-size:.75rem;
  letter-spacing:.02em;
}

.signal.alza {
  background:rgba(43,217,129,.18);
  border:1px solid rgba(43,217,129,.60);
  color:#dfffea;
}

.signal.vigilar {
  background:rgba(255,211,79,.16);
  border:1px solid rgba(255,211,79,.55);
  color:#fff4c5;
}

.signal.riesgo {
  background:rgba(216,40,53,.22);
  border:1px solid rgba(216,40,53,.70);
  color:#ffd5d9;
}

.signal.sin-datos {
  background:rgba(151,184,230,.10);
  border:1px solid rgba(151,184,230,.25);
  color:#d3ddef;
}

.metric-positive { color:var(--green); font-weight:800; }
.metric-negative { color:#ff5969; font-weight:800; }
.metric-neutral { color:var(--yellow); font-weight:800; }

.dataframe-container {
  border-radius:12px;
  overflow:hidden;
  border:1px solid var(--line);
}

.warning-box {
  border:1px solid rgba(255,211,79,.35);
  background:rgba(255,211,79,.08);
  color:#fff2bf;
  padding:1rem 1.15rem;
  border-radius:12px;
  line-height:1.5;
}

.info-box {
  border:1px solid rgba(91,141,255,.35);
  background:rgba(91,141,255,.08);
  color:#dfeaff;
  padding:1rem 1.15rem;
  border-radius:12px;
  line-height:1.5;
}

hr {
  border-color:rgba(255,255,255,.10);
}

div[data-testid="stMetric"] {
  background:rgba(255,255,255,.04);
  border:1px solid var(--line);
  border-radius:12px;
  padding:1rem;
}

div[data-testid="stMetricValue"] { color:white; }
div[data-testid="stMetricLabel"] { color:#d9e4f5; }

.semaforo-card {
  min-height:96px;
  background:rgba(255,255,255,.04);
  border:1px solid var(--line);
  border-radius:12px;
  padding:1rem;
}
.semaforo-title {
  font-weight:900;
  font-size:1.05rem;
  color:white;
}
.semaforo-desc {
  color:#d7e2f3;
  font-size:.88rem;
  line-height:1.45;
  margin-top:.35rem;
}


.detail-card {
  background:rgba(255,255,255,.045);
  border:1px solid var(--line);
  border-radius:12px;
  padding:1.05rem 1.15rem;
  margin:.75rem 0;
}
.detail-card h3 {
  margin:.15rem 0 .45rem 0;
  color:white;
}
.detail-grid {
  display:grid;
  grid-template-columns:repeat(4, minmax(0,1fr));
  gap:.75rem;
  margin:.8rem 0 1rem 0;
}
.detail-metric {
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.08);
  border-radius:10px;
  padding:.8rem;
}
.detail-metric span {
  display:block;
  color:#9fb0ca;
  font-size:.72rem;
  text-transform:uppercase;
  letter-spacing:.08em;
  font-weight:850;
}
.detail-metric strong {
  display:block;
  color:white;
  font-size:1.08rem;
  margin-top:.25rem;
}
.reason-box {
  border:1px solid rgba(91,141,255,.32);
  background:rgba(91,141,255,.08);
  color:#dfeaff;
  padding:.95rem 1rem;
  border-radius:10px;
  line-height:1.5;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# DATA
# =========================================================

@st.cache_data(ttl=900, show_spinner=False)
def download_price_history(ticker: str, period: str = "1y") -> pd.DataFrame:
    """Descarga datos reales desde Yahoo Finance vía yfinance."""
    if yf is None:
        return pd.DataFrame()

    try:
        data = yf.download(
            ticker,
            period=period,
            interval="1d",
            auto_adjust=True,
            progress=False,
            threads=False,
        )
        if data is None or data.empty:
            return pd.DataFrame()

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns]

        data = data.dropna(how="all")
        needed = ["Open", "High", "Low", "Close"]
        if not all(col in data.columns for col in needed):
            return pd.DataFrame()

        data.index = pd.to_datetime(data.index)
        return data
    except Exception:
        return pd.DataFrame()


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    out = df.copy()
    out["SMA20"] = out["Close"].rolling(20).mean()
    out["SMA50"] = out["Close"].rolling(50).mean()
    out["SMA200"] = out["Close"].rolling(200).mean()

    delta = out["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    out["RSI14"] = 100 - (100 / (1 + rs))

    out["Retorno 20D"] = out["Close"].pct_change(20)
    out["Retorno 60D"] = out["Close"].pct_change(60)
    out["Volatilidad 20D"] = out["Close"].pct_change().rolling(20).std() * np.sqrt(252)
    return out


def classify_signal(row: pd.Series) -> tuple[str, str, str]:
    if row is None or row.empty or pd.isna(row.get("Close")):
        return "SIN DATOS", "sin-datos", "No fue posible obtener datos suficientes para este activo."

    score = 0
    reasons = []

    if pd.notna(row.get("SMA20")) and pd.notna(row.get("SMA50")):
        if row["SMA20"] > row["SMA50"]:
            score += 1
            reasons.append("tendencia corta favorable")
        else:
            score -= 1
            reasons.append("tendencia corta débil")

    if pd.notna(row.get("SMA50")) and pd.notna(row.get("SMA200")):
        if row["SMA50"] > row["SMA200"]:
            score += 1
            reasons.append("mediano plazo favorable")
        else:
            score -= 1
            reasons.append("mediano plazo débil")

    rsi = row.get("RSI14")
    if pd.notna(rsi):
        if 45 <= rsi <= 65:
            score += 1
            reasons.append("RSI en zona sana")
        elif rsi > 72:
            score -= 1
            reasons.append("RSI alto / posible sobrecompra")
        elif rsi < 35:
            reasons.append("RSI castigado / posible rebote, con cautela")

    ret20 = row.get("Retorno 20D")
    if pd.notna(ret20):
        if ret20 > 0.03:
            score += 1
            reasons.append("momentum 20D positivo")
        elif ret20 < -0.05:
            score -= 1
            reasons.append("momentum 20D negativo")

    vol = row.get("Volatilidad 20D")
    if pd.notna(vol) and vol > 0.45:
        score -= 1
        reasons.append("volatilidad elevada")

    if score >= 3:
        return "ALZA", "alza", "🟢 Favorable: merece revisión prioritaria, pero no implica compra automática. " + " · ".join(reasons)
    if score <= -2:
        return "RIESGO", "riesgo", "🔴 Riesgo: presenta debilidad o volatilidad relevante; revisar con cautela. " + " · ".join(reasons)
    return "VIGILAR", "vigilar", "🟡 Vigilar: señal mixta; conviene esperar confirmación. " + " · ".join(reasons)

def semaforo_text(signal: str) -> str:
    if signal == "ALZA":
        return "🟢 Favorable"
    if signal == "RIESGO":
        return "🔴 Riesgo"
    if signal == "VIGILAR":
        return "🟡 Vigilar"
    return "⚪ Sin datos"


def fmt_money(value: float) -> str:
    if pd.isna(value):
        return "—"
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(value: float) -> str:
    if pd.isna(value):
        return "—"
    return f"{value*100:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_num(value: float) -> str:
    if pd.isna(value):
        return "—"
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@st.cache_data(ttl=900, show_spinner=False)
def build_asset_table(asset_list: list[dict], period: str) -> pd.DataFrame:
    rows = []

    for item in asset_list:
        ticker = item["ticker"]
        raw = download_price_history(ticker, period=period)
        df = add_indicators(raw)

        if df.empty or len(df) < 5:
            signal, css, reason = "SIN DATOS", "sin-datos", "Sin datos suficientes desde la fuente."
            rows.append({
                "Activo": item["name"],
                "Ticker": ticker,
                "Empresa": item["company"],
                "Precio": np.nan,
                "Retorno 20D": np.nan,
                "Retorno 60D": np.nan,
                "RSI 14": np.nan,
                "Volatilidad 20D": np.nan,
                "Señal": signal,
                "Clase": css,
                "Lectura": reason,
                "Última fecha": "—",
            })
            continue

        last = df.iloc[-1]
        signal, css, reason = classify_signal(last)
        rows.append({
            "Activo": item["name"],
            "Ticker": ticker,
            "Empresa": item["company"],
            "Precio": float(last.get("Close", np.nan)),
            "Retorno 20D": float(last.get("Retorno 20D", np.nan)) if pd.notna(last.get("Retorno 20D")) else np.nan,
            "Retorno 60D": float(last.get("Retorno 60D", np.nan)) if pd.notna(last.get("Retorno 60D")) else np.nan,
            "RSI 14": float(last.get("RSI14", np.nan)) if pd.notna(last.get("RSI14")) else np.nan,
            "Volatilidad 20D": float(last.get("Volatilidad 20D", np.nan)) if pd.notna(last.get("Volatilidad 20D")) else np.nan,
            "Señal": signal,
            "Clase": css,
            "Lectura": reason,
            "Última fecha": df.index[-1].strftime("%d-%m-%Y"),
        })

    return pd.DataFrame(rows)


def make_chart(df: pd.DataFrame, title: str) -> go.Figure:
    fig = go.Figure()

    if df.empty:
        fig.update_layout(
            template="plotly_dark",
            title="Sin datos disponibles",
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.03)",
        )
        return fig

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Precio",
        increasing_line_color="#2bd981",
        decreasing_line_color="#ff4759",
    ))

    for col, name in [("SMA20", "MA 20"), ("SMA50", "MA 50"), ("SMA200", "MA 200")]:
        if col in df.columns and df[col].notna().any():
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df[col],
                mode="lines",
                name=name,
                line=dict(width=1.6),
            ))

    fig.update_layout(
        title=title,
        template="plotly_dark",
        height=470,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.035)",
        margin=dict(l=10, r=10, t=45, b=10),
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", y=1.04, x=0),
    )

    return fig


def signal_badge(signal: str, css: str) -> str:
    return f'<span class="signal {css}">{signal}</span>'


def style_return(value: float) -> str:
    if pd.isna(value):
        return '<span class="metric-neutral">—</span>'
    klass = "metric-positive" if value >= 0 else "metric-negative"
    sign = "+" if value >= 0 else ""
    return f'<span class="{klass}">{sign}{fmt_pct(value)}</span>'


def render_table_html(df: pd.DataFrame) -> None:
    """Tabla estable del radar usando componentes nativos de Streamlit."""
    required_cols = [
        "Activo", "Ticker", "Empresa", "Precio", "Retorno 20D",
        "RSI 14", "Volatilidad 20D", "Señal", "Lectura"
    ]

    if df.empty:
        st.info("No hay activos para mostrar.")
        return

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error("El radar no pudo construir la tabla porque faltan columnas: " + ", ".join(missing_cols))
        st.dataframe(df, use_container_width=True, hide_index=True)
        return

    view = df.copy()
    view["Semáforo"] = view["Señal"].apply(semaforo_text)
    view["Activo"] = view["Activo"].astype(str) + " · " + view["Ticker"].astype(str)
    view["Precio"] = view["Precio"].apply(fmt_money)
    view["20D"] = view["Retorno 20D"].apply(fmt_pct)
    view["60D"] = view["Retorno 60D"].apply(fmt_pct)
    view["RSI"] = view["RSI 14"].apply(fmt_num)
    view["Volatilidad"] = view["Volatilidad 20D"].apply(fmt_pct)
    view["Interpretación"] = view["Lectura"]

    view = view[[
        "Semáforo",
        "Activo",
        "Empresa",
        "Precio",
        "20D",
        "60D",
        "RSI",
        "Volatilidad",
        "Interpretación",
    ]]

    st.dataframe(
        view,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Semáforo": st.column_config.TextColumn("Semáforo", width="small"),
            "Activo": st.column_config.TextColumn("Activo", width="medium"),
            "Empresa": st.column_config.TextColumn("Empresa", width="medium"),
            "Precio": st.column_config.TextColumn("Precio", width="small"),
            "20D": st.column_config.TextColumn("20D", width="small"),
            "60D": st.column_config.TextColumn("60D", width="small"),
            "RSI": st.column_config.TextColumn("RSI", width="small"),
            "Volatilidad": st.column_config.TextColumn("Volatilidad", width="small"),
            "Interpretación": st.column_config.TextColumn("Interpretación", width="large"),
        },
    )


# =========================================================
# STATE / NAVIGATION
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Radar"

if "selected_ticker" not in st.session_state:
    st.session_state.selected_ticker = "SQM-B.SN"

if "selected_signal_filter" not in st.session_state:
    st.session_state.selected_signal_filter = None

if "selected_company_detail" not in st.session_state:
    st.session_state.selected_company_detail = None


def set_page(page: str):
    st.session_state.page = page
    st.rerun()
    st.rerun()


def set_ticker(ticker: str):
    st.session_state.selected_ticker = ticker


# =========================================================
# HEADER
# =========================================================

st.markdown(
    f"""
<div class="andes-topbar">
  <div>
    <img class="andes-logo" src="{LOGO_DATA}">
  </div>
  <div class="andes-top-right">
    <span class="status-pill">Datos reales vía Yahoo Finance / yfinance</span>
    <span class="disclaimer-pill">Herramienta exploratoria · No es recomendación de inversión</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

nav_cols = st.columns([1, 1.35, 1, 1, 1, 1.4, 2.2])
with nav_cols[0]:
    if st.button("Radar", use_container_width=True):
        set_page("Radar")
with nav_cols[1]:
    if st.button("Radar de activos", use_container_width=True):
        set_page("Radar de activos")
with nav_cols[2]:
    if st.button("Señales", use_container_width=True):
        set_page("Señales")
with nav_cols[3]:
    if st.button("Portafolio", use_container_width=True):
        set_page("Portafolio")
with nav_cols[4]:
    if st.button("Mercado", use_container_width=True):
        set_page("Mercado")
with nav_cols[5]:
    if st.button("Actualizar datos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

period = nav_cols[6].selectbox(
    "Horizonte",
    ["3mo", "6mo", "1y", "2y", "5y"],
    index=2,
    label_visibility="collapsed",
)


# =========================================================
# DATA LOAD
# =========================================================

with st.spinner("Cargando datos reales de mercado..."):
    asset_df = build_asset_table(DEFAULT_ASSETS, period=period)




def signal_label(signal: str) -> str:
    labels = {
        "ALZA": "🟢 Favorable",
        "VIGILAR": "🟡 Vigilar",
        "RIESGO": "🔴 Riesgo",
        "SIN DATOS": "⚪ Sin datos",
    }
    return labels.get(signal, "⚪ Sin datos")


def set_signal_filter(signal: str):
    st.session_state.selected_signal_filter = signal
    st.session_state.selected_company_detail = None
    st.rerun()


def set_company_detail(ticker: str):
    st.session_state.selected_company_detail = ticker
    st.rerun()


def render_company_detail(row: pd.Series):
    ticker = row["Ticker"]
    signal = row["Señal"]
    css = row.get("Clase", "sin-datos")
    chart_df = add_indicators(download_price_history(ticker, period=period))

    st.markdown(
        f"""
<div class="detail-card">
  <h3>{signal_label(signal)} · {row['Activo']}</h3>
  <div style="color:#aebdd4; font-size:.9rem;">{row['Empresa']} · {ticker}</div>
  <div class="detail-grid">
    <div class="detail-metric"><span>Precio</span><strong>{fmt_money(row['Precio'])}</strong></div>
    <div class="detail-metric"><span>Retorno 20D</span><strong>{fmt_pct(row['Retorno 20D'])}</strong></div>
    <div class="detail-metric"><span>RSI 14</span><strong>{fmt_num(row['RSI 14'])}</strong></div>
    <div class="detail-metric"><span>Volatilidad 20D</span><strong>{fmt_pct(row['Volatilidad 20D'])}</strong></div>
  </div>
  <div class="reason-box"><b>¿Por qué está en esta condición?</b><br>{row['Lectura']}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if not chart_df.empty:
        st.plotly_chart(make_chart(chart_df, f"{ticker} · soporte visual de la condición"), use_container_width=True)
    else:
        st.info("No hay datos suficientes para graficar este activo.")


def render_interactive_semaforo(df: pd.DataFrame):
    if df.empty or "Señal" not in df.columns:
        st.info("No hay información suficiente para construir el semáforo interactivo.")
        return

    st.markdown("### Semáforo interactivo")
    st.caption("Pincha una condición para ver las empresas clasificadas ahí. Luego pincha una empresa para ver la explicación.")

    counts = {
        "ALZA": int((df["Señal"] == "ALZA").sum()),
        "VIGILAR": int((df["Señal"] == "VIGILAR").sum()),
        "RIESGO": int((df["Señal"] == "RIESGO").sum()),
        "SIN DATOS": int((df["Señal"] == "SIN DATOS").sum()),
    }

    c1, c2, c3, c4 = st.columns(4)
    button_map = [
        (c1, "ALZA", f"🟢 Favorable ({counts['ALZA']})"),
        (c2, "VIGILAR", f"🟡 Vigilar ({counts['VIGILAR']})"),
        (c3, "RIESGO", f"🔴 Riesgo ({counts['RIESGO']})"),
        (c4, "SIN DATOS", f"⚪ Sin datos ({counts['SIN DATOS']})"),
    ]

    for col, signal, label in button_map:
        with col:
            if st.button(label, use_container_width=True, key=f"filter_{signal}"):
                set_signal_filter(signal)

    selected = st.session_state.selected_signal_filter

    if not selected:
        st.markdown(
            """
<div class="info-box">
Selecciona un color del semáforo para desplegar las empresas clasificadas en esa condición.
</div>
""",
            unsafe_allow_html=True,
        )
        return

    subset = df[df["Señal"] == selected].copy()

    st.markdown(f"#### {signal_label(selected)}")
    if subset.empty:
        st.info("No hay empresas en esta condición.")
        return

    company_cols = st.columns(3)
    for i, (_, row) in enumerate(subset.iterrows()):
        with company_cols[i % 3]:
            label = f"{row['Activo']} · {fmt_pct(row['Retorno 20D'])}"
            if st.button(label, use_container_width=True, key=f"company_{selected}_{row['Ticker']}"):
                set_company_detail(row["Ticker"])

    chosen = st.session_state.selected_company_detail
    if chosen:
        detail_rows = df[df["Ticker"] == chosen]
        if not detail_rows.empty:
            render_company_detail(detail_rows.iloc[0])


def render_semaforo_summary(df: pd.DataFrame) -> None:
    if df.empty or "Señal" not in df.columns:
        return

    alza = int((df["Señal"] == "ALZA").sum())
    vigilar = int((df["Señal"] == "VIGILAR").sum())
    riesgo = int((df["Señal"] == "RIESGO").sum())
    sin_datos = int((df["Señal"] == "SIN DATOS").sum())

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "🟢 Favorable", alza, "Tendencia/momentum más constructivo. Revisar con prioridad, no comprar automáticamente."),
        (c2, "🟡 Vigilar", vigilar, "Lectura mixta. Esperar confirmación o revisar más antecedentes."),
        (c3, "🔴 Riesgo", riesgo, "Debilidad, presión bajista o volatilidad relevante. Actuar con cautela."),
        (c4, "⚪ Sin datos", sin_datos, "Yahoo Finance no entregó información suficiente para calcular el radar."),
    ]
    for col, title, value, desc in cards:
        with col:
            st.markdown(
                f"""
<div class="semaforo-card">
  <div class="semaforo-title">{title}: {value}</div>
  <div class="semaforo-desc">{desc}</div>
</div>
""",
                unsafe_allow_html=True,
            )


# =========================================================
# PAGES
# =========================================================

def page_radar():
    left, right = st.columns([1.1, 1.55], gap="large")

    with left:
        st.markdown(
            f"""
<div class="andes-hero">
  <h1>Radar Bursátil<br>Andes Capital</h1>
  <div class="red-line"></div>
  <p>
    Esta plataforma es una herramienta exploratoria de información bursátil.
    Su objetivo es ordenar datos, tendencias y niveles de riesgo para apoyar el análisis.
    No constituye asesoría financiera, recomendación personalizada ni una señal segura de compra o venta.
  </p>
  <p class="timestamp">Actualizado: {datetime.now().strftime("%d-%m-%Y %H:%M")} CLT</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with right:
        k1, k2, k3, k4 = st.columns(4)
        total = len(asset_df)
        alza = int((asset_df["Señal"] == "ALZA").sum()) if not asset_df.empty else 0
        vigilar = int((asset_df["Señal"] == "VIGILAR").sum()) if not asset_df.empty else 0
        riesgo = int((asset_df["Señal"] == "RIESGO").sum()) if not asset_df.empty else 0

        for col, label, value, note in [
            (k1, "Activos analizados", total, "Radar actual"),
            (k2, "Señales de alza", alza, "Tendencia favorable"),
            (k3, "En vigilancia", vigilar, "Esperar confirmación"),
            (k4, "Riesgo", riesgo, "Presión o debilidad"),
        ]:
            with col:
                st.markdown(
                    f"""
<div class="kpi-card">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  <div class="kpi-note">{note}</div>
</div>
""",
                    unsafe_allow_html=True,
                )

        st.markdown("")

        selected = st.selectbox(
            "Activo principal para gráfico",
            options=[item["ticker"] for item in DEFAULT_ASSETS],
            index=0,
            format_func=lambda t: next((x["name"] for x in DEFAULT_ASSETS if x["ticker"] == t), t),
        )
        st.session_state.selected_ticker = selected

        chart_df = add_indicators(download_price_history(selected, period=period))
        st.plotly_chart(
            make_chart(chart_df, f"{selected} · Precio, medias móviles y tendencia"),
            use_container_width=True,
        )

    c1, c2 = st.columns([1.5, 0.75], gap="large")

    with c1:
        st.markdown('<div class="panel"><h2>Radar de activos Andes Capital</h2><div class="small-red-line"></div>', unsafe_allow_html=True)
        render_table_html(asset_df.head(7))
        if st.button("Ver radar de activos completo", use_container_width=True):
            set_page("Radar de activos")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(
            """
<div class="panel">
  <h2>Análisis del día</h2>
  <div class="small-red-line"></div>
  <h3>Lectura preliminar del mercado</h3>
  <p style="color:#d7e2f3; line-height:1.55;">
    El radar cruza tendencia, momentum, RSI y volatilidad. Una señal de alza no equivale a recomendación;
    solo indica que, bajo estos criterios técnicos, el activo merece revisión.
  </p>
  <div class="info-box">
    Antes de decidir, revisar fundamentos, liquidez, noticias, horizonte, costos y perfil de riesgo.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    market_preview()


def market_preview():
    st.markdown("")
    st.markdown('<div class="panel"><h2>Resumen de mercado</h2><div class="small-red-line"></div>', unsafe_allow_html=True)
    rows = []
    for item in MARKET_INDEXES:
        df = add_indicators(download_price_history(item["ticker"], period="3mo"))
        if df.empty:
            rows.append({"Mercado": item["name"], "Último": "—", "20D": "—", "Señal": "SIN DATOS"})
            continue
        last = df.iloc[-1]
        signal, _, _ = classify_signal(last)
        rows.append({
            "Mercado": item["name"],
            "Último": fmt_money(last["Close"]),
            "20D": fmt_pct(last.get("Retorno 20D")),
            "Señal": signal,
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def page_radar_activos():
    st.markdown('<div class="panel"><h2>Radar de activos</h2><div class="small-red-line"></div>', unsafe_allow_html=True)
    st.caption("Sección activa: Radar de activos")
    st.markdown(
        """
<div class="warning-box">
Este radar ordena información de mercado y genera una lectura técnica preliminar.
No es una recomendación de inversión ni garantiza resultados futuros.
</div>
""",
        unsafe_allow_html=True,
    )

    render_semaforo_summary(asset_df)
    st.markdown("")
    render_interactive_semaforo(asset_df)
    st.markdown("")
    search = st.text_input("Buscar activo", placeholder="Ej: SQM, COPEC, CHILE, CENCOSUD...")
    filtered = asset_df.copy()
    if search:
        q = search.strip().lower()
        filtered = filtered[
            filtered["Activo"].str.lower().str.contains(q)
            | filtered["Ticker"].str.lower().str.contains(q)
            | filtered["Empresa"].str.lower().str.contains(q)
        ]

    order_choice = st.radio(
        "Ordenar por",
        ["Señal", "Retorno 20D", "RSI 14", "Volatilidad 20D"],
        horizontal=True,
    )

    if order_choice == "Señal":
        signal_order = {"ALZA": 0, "VIGILAR": 1, "RIESGO": 2, "SIN DATOS": 3}
        filtered = filtered.assign(_order=filtered["Señal"].map(signal_order)).sort_values("_order").drop(columns="_order")
    else:
        filtered = filtered.sort_values(order_choice, ascending=False, na_position="last")

    render_table_html(filtered)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="panel"><h2>Análisis por activo</h2><div class="small-red-line"></div>', unsafe_allow_html=True)
    ticker = st.selectbox(
        "Selecciona un activo",
        options=[item["ticker"] for item in DEFAULT_ASSETS],
        index=0,
        format_func=lambda t: f"{next((x['name'] for x in DEFAULT_ASSETS if x['ticker'] == t), t)} · {t}",
    )
    chart_df = add_indicators(download_price_history(ticker, period=period))
    st.plotly_chart(make_chart(chart_df, f"{ticker} · Análisis técnico"), use_container_width=True)

    if not chart_df.empty:
        last = chart_df.iloc[-1]
        signal, css, reason = classify_signal(last)
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Precio", fmt_money(last["Close"]))
        m2.metric("Retorno 20D", fmt_pct(last.get("Retorno 20D")))
        m3.metric("RSI 14", fmt_num(last.get("RSI14")))
        m4.metric("Volatilidad", fmt_pct(last.get("Volatilidad 20D")))
        m5.markdown(f"<br>{signal_badge(signal, css)}", unsafe_allow_html=True)
        st.markdown(f'<div class="info-box"><b>Lectura:</b> {reason}</div>', unsafe_allow_html=True)
    else:
        st.warning("No se pudieron obtener datos para este activo.")
    st.markdown("</div>", unsafe_allow_html=True)


def page_senales():
    st.markdown('<div class="panel"><h2>Señales</h2><div class="small-red-line"></div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="warning-box">
Las señales son filtros técnicos automáticos. Sirven para priorizar revisión, no para indicar compra o venta segura.
</div>
""",
        unsafe_allow_html=True,
    )

    tabs = st.tabs(["ALZA", "VIGILAR", "RIESGO", "SIN DATOS"])
    for tab, signal in zip(tabs, ["ALZA", "VIGILAR", "RIESGO", "SIN DATOS"]):
        with tab:
            render_table_html(asset_df[asset_df["Señal"] == signal])

    st.markdown("</div>", unsafe_allow_html=True)


def page_portafolio():
    st.markdown('<div class="panel"><h2>Portafolio</h2><div class="small-red-line"></div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="info-box">
Módulo inicial para simular una cartera. Puedes ingresar posiciones y la app calculará valorización con precios reales disponibles.
</div>
""",
        unsafe_allow_html=True,
    )

    st.caption("Ejemplo: ingresa cantidades por activo. No considera comisiones, impuestos, dividendos ni tipo de cambio contable.")
    quantities = {}
    cols = st.columns(2)
    for i, item in enumerate(DEFAULT_ASSETS[:8]):
        with cols[i % 2]:
            quantities[item["ticker"]] = st.number_input(
                f"{item['name']} · cantidad",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key=f"qty_{item['ticker']}",
            )

    rows = []
    for item in DEFAULT_ASSETS[:8]:
        qty = quantities[item["ticker"]]
        price_row = asset_df[asset_df["Ticker"] == item["ticker"]]
        price = np.nan if price_row.empty else price_row.iloc[0]["Precio"]
        value = qty * price if pd.notna(price) else np.nan
        rows.append({
            "Activo": item["name"],
            "Ticker": item["ticker"],
            "Cantidad": qty,
            "Precio": fmt_money(price),
            "Valor estimado": fmt_money(value),
        })

    portfolio_df = pd.DataFrame(rows)
    st.dataframe(portfolio_df, use_container_width=True, hide_index=True)

    total_value = 0.0
    for item in DEFAULT_ASSETS[:8]:
        qty = quantities[item["ticker"]]
        price_row = asset_df[asset_df["Ticker"] == item["ticker"]]
        if not price_row.empty and pd.notna(price_row.iloc[0]["Precio"]):
            total_value += qty * price_row.iloc[0]["Precio"]

    st.metric("Valor total estimado", fmt_money(total_value))
    st.markdown("</div>", unsafe_allow_html=True)


def page_mercado():
    st.markdown('<div class="panel"><h2>Mercado</h2><div class="small-red-line"></div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="warning-box">
Resumen de mercado con instrumentos disponibles en Yahoo Finance. Algunas series chilenas pueden no estar disponibles o venir con rezago.
</div>
""",
        unsafe_allow_html=True,
    )

    rows = []
    for item in MARKET_INDEXES:
        df = add_indicators(download_price_history(item["ticker"], period=period))
        if df.empty:
            rows.append({
                "Mercado": item["name"],
                "Ticker": item["ticker"],
                "Último": "—",
                "20D": "—",
                "60D": "—",
                "RSI": "—",
                "Señal": "SIN DATOS",
            })
            continue

        last = df.iloc[-1]
        signal, _, reason = classify_signal(last)
        rows.append({
            "Mercado": item["name"],
            "Ticker": item["ticker"],
            "Último": fmt_money(last["Close"]),
            "20D": fmt_pct(last.get("Retorno 20D")),
            "60D": fmt_pct(last.get("Retorno 60D")),
            "RSI": fmt_num(last.get("RSI14")),
            "Señal": signal,
            "Lectura": reason,
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    selected_market = st.selectbox(
        "Ver gráfico de mercado",
        options=[item["ticker"] for item in MARKET_INDEXES],
        format_func=lambda t: f"{next((x['name'] for x in MARKET_INDEXES if x['ticker'] == t), t)} · {t}",
    )
    chart_df = add_indicators(download_price_history(selected_market, period=period))
    st.plotly_chart(make_chart(chart_df, f"{selected_market} · Mercado"), use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# ROUTER
# =========================================================

page = st.session_state.page

if page == "Radar":
    page_radar()
elif page == "Radar de activos":
    page_radar_activos()
elif page == "Señales":
    page_senales()
elif page == "Portafolio":
    page_portafolio()
elif page == "Mercado":
    page_mercado()
else:
    page_radar()
