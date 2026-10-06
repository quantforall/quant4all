import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, time, date
from zoneinfo import ZoneInfo
import base64
import os

# -----------------------
# Logo
# -----------------------
def get_base64_of_bin_file(filename):
    with open(filename, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_of_bin_file("Logo.jpg") if os.path.exists("Logo.jpg") else ""

# -----------------------
# Page config
# -----------------------
st.set_page_config(
    page_title="Quant4all | Let's compare",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto",
)

# -----------------------
# Global CSS — Modern Dark-Accent Design
# -----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Tokens (marca Quant4all) ── */
:root {
    --q-navy: #0A1428;
    --q-navy-2: #14264A;
    --q-orange: #F7931E;
    --q-orange-text: #B45309;      /* naranja legible sobre blanco (4.8:1) */
    --q-orange-soft: #FFF4E6;
    --q-bg: #F5F7FB;
    --q-surface: #FFFFFF;
    --q-surface-2: #F8FAFC;
    --q-border: #E2E8F0;
    --q-border-soft: #EEF2F7;
    --q-text: #0F172A;
    --q-text-2: #334155;
    --q-muted: #64748B;            /* 4.7:1 sobre blanco */
    --q-pos: #15803D;
    --q-pos-soft: #DCFCE7;
    --q-neg: #B91C1C;
    --q-neg-soft: #FEE2E2;
    --q-radius: 14px;
    --q-radius-sm: 10px;
    --q-shadow-1: 0 1px 2px rgba(15,23,42,0.04), 0 1px 3px rgba(15,23,42,0.06);
    --q-shadow-2: 0 4px 12px rgba(15,23,42,0.08), 0 2px 4px rgba(15,23,42,0.04);
}

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: var(--q-bg); }
[data-testid="stHeader"] { background: rgba(245,247,251,0.85); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }

.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 1400px;
}

:focus-visible { outline: 2px solid var(--q-orange) !important; outline-offset: 2px; }

/* ── Hero ── */
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(120deg, var(--q-navy) 0%, var(--q-navy-2) 100%);
    border-radius: 18px;
    padding: 1.6rem 2rem 1.5rem 2rem;
    margin-bottom: 1.25rem;
    box-shadow: var(--q-shadow-2);
}
.hero::after {
    content: "";
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
    background-size: 28px 28px;
    mask-image: linear-gradient(90deg, transparent 35%, #000 100%);
    -webkit-mask-image: linear-gradient(90deg, transparent 35%, #000 100%);
    pointer-events: none;
}
.hero-eyebrow {
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--q-orange); margin-bottom: 0.45rem;
}
.hero-title {
    font-size: 2rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.15;
    letter-spacing: -0.02em;
}
.hero-sub { color: var(--q-orange); }
.hero-desc { color: #CBD5E1; font-size: 0.95rem; margin-top: 0.45rem; max-width: 62ch; line-height: 1.5; }

/* ── Tabs: control segmentado ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 4px;
    background: #E9EEF5;
    padding: 4px;
    border-radius: 12px;
    width: fit-content;
    max-width: 100%;
    overflow-x: auto;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    height: auto;
    padding: 0.5rem 1rem;
    border-radius: 9px;
    color: var(--q-text-2);
    font-weight: 600;
    background: transparent;
    transition: background-color 0.15s ease, color 0.15s ease, box-shadow 0.15s ease;
}
[data-testid="stTabs"] [data-baseweb="tab"] p { font-size: 0.9rem; font-weight: 600; }
[data-testid="stTabs"] [data-baseweb="tab"]:hover { color: var(--q-navy); background: rgba(255,255,255,0.6); }
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
    background: var(--q-surface);
    color: var(--q-navy);
    box-shadow: var(--q-shadow-1);
}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] [data-testid="stIconMaterial"] { color: var(--q-orange); }
[data-testid="stTabs"] [data-baseweb="tab-highlight"],
[data-testid="stTabs"] [data-baseweb="tab-border"] { display: none; }

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--q-text);
    letter-spacing: -0.01em;
    margin: 1.75rem 0 0.9rem 0;
}
.section-header .sh-icon {
    display: inline-flex; align-items: center; justify-content: center;
    width: 32px; height: 32px; border-radius: 9px;
    background: var(--q-orange-soft); color: var(--q-orange-text);
    flex-shrink: 0;
}
.section-header::after {
    content: ""; flex: 1; height: 1px; background: var(--q-border); margin-left: 0.4rem;
}

/* ── Divider ── */
.q-divider {
    border: none;
    border-top: 1px solid var(--q-border);
    margin: 1rem 0;
}

/* ── Contenedores con borde de Streamlit (st.container(border=True)) ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--q-surface);
    border-color: var(--q-border) !important;
    border-radius: var(--q-radius) !important;
    box-shadow: var(--q-shadow-1);
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
}
.kpi-card {
    position: relative;
    background: var(--q-surface);
    border: 1px solid var(--q-border);
    border-radius: var(--q-radius);
    padding: 1rem 1.25rem;
    text-align: center;
    box-shadow: var(--q-shadow-1);
    transition: box-shadow 0.2s ease;
    overflow: hidden;
}
.kpi-card::before {
    content: ""; position: absolute; left: 0; right: 0; top: 0; height: 3px;
    background: linear-gradient(90deg, var(--q-orange), #FDBA74);
}
.kpi-card:hover { box-shadow: var(--q-shadow-2); }
.kpi-card .kpi-label {
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--q-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.35rem;
}
.kpi-card .kpi-value {
    font-size: 1.75rem;
    font-weight: 800;
    line-height: 1.1;
    color: var(--q-text);
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.02em;
}
.kpi-card .kpi-foot { font-size: 0.75rem; color: var(--q-muted); margin-top: 0.4rem; }
.kpi-card .kpi-foot.live { color: var(--q-pos); font-weight: 600; }
.live-dot {
    display: inline-block; width: 7px; height: 7px; border-radius: 50%;
    background: var(--q-pos); margin-right: 5px; vertical-align: 1px;
    box-shadow: 0 0 0 3px rgba(21,128,61,0.18);
}

/* ── Tables ── */
.table-wrap {
    background: var(--q-surface);
    border: 1px solid var(--q-border);
    border-radius: var(--q-radius);
    overflow: hidden;
    box-shadow: var(--q-shadow-1);
    align-self: flex-start;
    width: 100%;
}
.table-common {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    font-family: 'Inter', sans-serif;
    font-variant-numeric: tabular-nums;
}
.table-common thead th {
    background: var(--q-surface-2);
    padding: 8px 4px;
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--q-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    text-align: center;
    border-bottom: 1px solid var(--q-border);
    white-space: nowrap;
}
.table-common tbody td {
    padding: 6px 4px;
    text-align: center;
    vertical-align: middle;
    border-bottom: 1px solid var(--q-border-soft);
    font-size: 0.8rem;
    color: var(--q-text-2);
    white-space: nowrap;
}
.table-common tbody tr { height: 54px; transition: background-color 0.15s ease; }
.table-common tbody tr:last-child td { border-bottom: none; }
.table-common tbody tr:hover td { background: #FBFCFE; }

/* Numbers inside cells */
.num {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--q-text);
    white-space: nowrap;
    display: inline-block;
    font-variant-numeric: tabular-nums;
}
.tw-date {
    font-size: 0.64rem;
    color: var(--q-muted);
    display: block;
    margin-top: 1px;
    white-space: nowrap;
}

/* Column widths — summary */
.summary-table { table-layout: auto; }
.summary-table th:first-child, .summary-table td:first-child { text-align: left; padding-left: 14px; }

/* Column widths — top/worst */
.tw-tabular { table-layout: auto; }
.tw-tabular th:first-child, .tw-tabular td:first-child { text-align: left; padding-left: 14px; }

/* Table title */
.table-title {
    display: flex; align-items: center; gap: 0.45rem;
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--q-text);
    padding: 10px 14px 9px 14px;
    background: var(--q-surface);
    border-bottom: 1px solid var(--q-border);
}
.table-title svg { color: var(--q-orange-text); }

/* ── Position sizing ── */
.sizing-table { table-layout: auto; min-width: 640px; }
.sizing-table th, .sizing-table td { padding-left: 12px !important; padding-right: 12px !important; }
.sizing-table th:first-child, .sizing-table td:first-child { text-align: left; padding-left: 18px !important; }
.sizing-table tbody tr { height: 58px; }
.sys-name { font-weight: 700; color: var(--q-text); font-size: 0.9rem; }
.chip {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 3px 10px; border-radius: 999px;
    font-size: 0.76rem; font-weight: 600; line-height: 1.4;
    white-space: nowrap;
}
.chip-market { background: #EEF2F7; color: var(--q-text-2); font-weight: 700; letter-spacing: 0.03em; }
.chip-long { background: var(--q-pos-soft); color: var(--q-pos); }
.chip-short { background: var(--q-neg-soft); color: var(--q-neg); }
.chip-micro { background: var(--q-orange-soft); color: var(--q-orange-text); border: 1px solid #FED7AA; }
.chip-nano { background: #EEF2FF; color: #3730A3; border: 1px solid #C7D2FE; }
.chip-shares { background: #FEF9C3; color: #854D0E; border: 1px solid #FDE68A; }
.chip-off { background: #F1F5F9; color: var(--q-muted); }
.chip b { font-weight: 800; font-variant-numeric: tabular-nums; }
.pos-cell { display: inline-flex; gap: 6px; flex-wrap: wrap; justify-content: center; }
.sizing-foot {
    display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;
    margin-top: 0.85rem; padding: 0.75rem 1rem;
    background: var(--q-surface); border: 1px solid var(--q-border);
    border-radius: var(--q-radius-sm); color: var(--q-text-2); font-size: 0.85rem;
}
.sizing-foot b { color: var(--q-text); font-variant-numeric: tabular-nums; }

/* ── Chart card wrapper ── */
.chart-card {
    background: var(--q-surface);
    border: 1px solid var(--q-border);
    border-radius: var(--q-radius);
    padding: 0.5rem 0.75rem 0.25rem 0.75rem;
    box-shadow: var(--q-shadow-1);
    margin-bottom: 0.25rem;
}
[data-testid="stPlotlyChart"] {
    background: var(--q-surface);
    border: 1px solid var(--q-border);
    border-radius: var(--q-radius);
    padding: 0.4rem 0.6rem;
    box-shadow: var(--q-shadow-1);
}

/* ── Monthly heat table ── */
.monthly-heat-wrap { width: 88%; margin: 0 auto; }
.monthly-heat {
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
    table-layout: fixed;
    font-size: 0.88rem;
    border: 1px solid var(--q-border);
    border-radius: 12px;
    overflow: hidden;
    font-family: 'Inter', sans-serif;
    font-variant-numeric: tabular-nums;
    background: var(--q-surface);
    box-shadow: var(--q-shadow-1);
}
.monthly-heat th, .monthly-heat td {
    border-right: 1px solid var(--q-border-soft);
    border-bottom: 1px solid var(--q-border-soft);
    padding: 6px 4px;
    text-align: center;
    vertical-align: middle;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.monthly-heat thead th {
    background: var(--q-surface-2);
    font-weight: 700;
    font-size: 0.74rem;
    color: var(--q-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.monthly-heat tfoot td { background: var(--q-surface-2); font-weight: 700; }
.monthly-heat td.year-col, .monthly-heat th.year-col { width: 7%; font-weight: 700; color: var(--q-text-2); }
.monthly-heat th.mon-col, .monthly-heat td.mon-col { width: 6.5%; }
.monthly-heat th.ytd-col, .monthly-heat td.ytd-col { width: 7.5%; font-weight: 800; }
.monthly-heat .cell { color: var(--q-text); font-weight: 600; font-size: 0.82rem; }
.monthly-heat .na { color: #94A3B8; font-weight: 500; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    min-width: 18rem;
    background: linear-gradient(180deg, var(--q-navy) 0%, #0D1A33 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] .stMarkdown p {
    font-size: 0.72rem; font-weight: 700; color: #94A3B8;
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;
}
[data-testid="stSidebar"] label { color: #CBD5E1 !important; }
[data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] .stTextInput label { color: #CBD5E1 !important; }
[data-testid="stSidebar"] [data-testid="stCheckbox"] label > div:last-child,
[data-testid="stSidebar"] [data-testid="stCheckbox"] label p {
    color: #E2E8F0 !important; text-transform: none; letter-spacing: 0; font-size: 0.85rem; font-weight: 500;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.10); }
[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stSliderTickBarMin"],
[data-testid="stSidebar"] [data-testid="stSliderTickBarMax"] { color: #CBD5E1; }

/* ── Stats card ── */
.stats-card {
    background: var(--q-surface);
    border: 1px solid var(--q-border);
    border-radius: var(--q-radius);
    padding: 1rem 1.25rem;
    box-shadow: var(--q-shadow-1);
    text-align: center;
    margin-top: 0.5rem;
}
.stats-card .stats-title {
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--q-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.75rem;
}
.stats-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid var(--q-border-soft);
    font-size: 0.88rem;
    font-variant-numeric: tabular-nums;
}
.stats-row:last-child { border-bottom: none; }
.stats-row .stat-label { color: var(--q-muted); }
.stats-row .stat-val { font-weight: 700; color: var(--q-text); }

/* ── Threshold counter cards ── */
.count-card {
    border-radius: var(--q-radius);
    padding: 1rem 0.5rem;
    text-align: center;
    margin-top: 0.5rem;
    font-variant-numeric: tabular-nums;
}
.count-card .count-label { font-size: 0.82rem; font-weight: 700; margin-bottom: 4px; }
.count-card .count-val { font-size: 2.8rem; font-weight: 800; line-height: 1; }
.count-card.positive { background: var(--q-pos-soft); border: 1px solid #86efac; }
.count-card.positive .count-label { color: var(--q-pos); }
.count-card.positive .count-val { color: #166534; }
.count-card.negative { background: var(--q-orange-soft); border: 1px solid #FDBA74; }
.count-card.negative .count-label { color: var(--q-orange-text); }
.count-card.negative .count-val { color: #9A3412; }

/* ── Radio / controls pill ── */
div[data-testid="stHorizontalBlock"] .stRadio > label { font-size: 0.8rem; }

/* ── Newsletter button ── */
.newsletter-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: var(--q-orange);
    color: var(--q-navy) !important;
    text-decoration: none !important;
    padding: 0.6rem 1.4rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    cursor: pointer;
    transition: box-shadow 0.2s ease, transform 0.2s ease, background-color 0.2s ease;
    box-shadow: 0 4px 14px rgba(247,147,30,0.35);
}
.newsletter-btn:hover {
    background: #FFA53D;
    box-shadow: 0 6px 20px rgba(247,147,30,0.5);
    transform: translateY(-1px);
}

/* ── Sidebar logo ── */
.sidebar-logo { text-align: center; margin-bottom: 1.2rem; }
.sidebar-logo img { width: 72px; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.35); }
.sidebar-brand {
    text-align: center; color: #FFFFFF; font-weight: 800; font-size: 1.15rem;
    letter-spacing: -0.01em; margin: 0.25rem 0 1rem 0;
}
.sidebar-brand span { color: var(--q-orange); }
.sidebar-brand small {
    display: block; color: #94A3B8; font-size: 0.68rem; font-weight: 600;
    letter-spacing: 0.14em; text-transform: uppercase; margin-top: 2px;
}

/* ── Quitar líneas negras del number_input ── */
[data-testid="stNumberInput"] > div { border-top: none !important; border-bottom: none !important; }
[data-testid="stNumberInput"] input { border-top: none !important; border-bottom: none !important; }

/* Captions */
[data-testid="stCaptionContainer"] { color: var(--q-muted); }

/* hide default streamlit header/footer noise */
#MainMenu, footer { visibility: hidden; }

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { transition: none !important; animation: none !important; }
}

/* ===================================================== */
/* ============== RESPONSIVE / MÓVIL ==================== */
/* ===================================================== */
@media (max-width: 820px) {

    /* Padding lateral compacto */
    .block-container {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-top: 2.5rem !important;
    }

    /* Apilar TODAS las columnas en vertical */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 0.6rem !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    /* Hero y títulos más pequeños */
    .hero { padding: 1.2rem 1.25rem; border-radius: 14px; }
    .hero-title { font-size: 1.45rem; }
    .hero-desc { font-size: 0.85rem; }
    .section-header { font-size: 1.02rem; margin: 1.25rem 0 0.75rem 0; }

    /* Tabs: ocupan todo el ancho y hacen scroll */
    [data-testid="stTabs"] [data-baseweb="tab-list"] { width: 100%; }
    [data-testid="stTabs"] [data-baseweb="tab"] { padding: 0.45rem 0.7rem; }

    /* KPI cards: número algo menor */
    .kpi-card .kpi-value { font-size: 1.45rem; }
    .kpi-card { padding: 0.75rem 1rem; }

    /* Tablas anchas (Top/Worst, Performance) → scroll horizontal */
    .table-wrap { overflow-x: auto !important; -webkit-overflow-scrolling: touch; }

    /* Heatmap mensual: ancho completo + scroll, sin aplastar celdas */
    .monthly-heat-wrap { width: 100% !important; overflow-x: auto; -webkit-overflow-scrolling: touch; }
    .monthly-heat { min-width: 620px; }

    /* Counter cards (días +/-) un poco menores */
    .count-card .count-val { font-size: 2.2rem; }

    /* Stats card margen superior para separarla del gráfico apilado */
    .stats-card { margin-top: 1rem; }
}

/* Pantallas muy pequeñas (teléfonos estrechos) */
@media (max-width: 480px) {
    .hero-title { font-size: 1.25rem; }
    .num { font-size: 0.78rem; }
    .table-common tbody td { font-size: 0.74rem; }
    .kpi-card .kpi-value { font-size: 1.25rem; }
}
</style>
""", unsafe_allow_html=True)


# -----------------------
# Iconos (Lucide, SVG en línea)
# -----------------------
_ICON_PATHS = {
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
    "trending-up": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "trending-down": '<polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/>',
    "bar-chart": '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "pie-chart": '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/>',
    "calculator": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8"/><path d="M16 14v4"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/>',
    "arrow-up-right": '<path d="M7 17 17 7"/><path d="M7 7h10v10"/>',
    "arrow-down-right": '<path d="m7 7 10 10"/><path d="M17 7v10H7"/>',
    "layers": '<path d="m12 2 10 5-10 5L2 7l10-5z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
}


def icon(name: str, size: int = 18, stroke: float = 2) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'fill="none" stroke="currentColor" stroke-width="{stroke}" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{_ICON_PATHS[name]}</svg>')


def section_header(title: str, icon_name: str) -> None:
    st.markdown(
        f"<div class='section-header'><span class='sh-icon'>{icon(icon_name)}</span>{title}</div>",
        unsafe_allow_html=True,
    )


# -----------------------
# Sidebar
# -----------------------
with st.sidebar:
    if logo_base64:
        st.markdown(f"""
        <div class='sidebar-logo'>
            <img src='data:image/jpg;base64,{logo_base64}'>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='sidebar-brand'>Quant<span>4</span>all<small>Systematic Trading</small></div>
    <div style='text-align:center; margin-bottom:1.5rem;'>
        <a href='https://quant4all.substack.com/' target='_blank' rel='noopener' class='newsletter-btn'>
            {icon("mail", 16, 2.2)} Subscribe free
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("**Initial Capital ($)**")
    initial_capital = st.number_input(
        "", min_value=1000, value=25000, step=500, label_visibility="collapsed"
    )

    st.markdown("**Begin | End**")
    dates_container = st.container()
    range_slider_container = st.container()

    st.markdown("")

    col_assets, col_systems = st.columns(2)
    with col_assets:
        st.markdown("**Tickers (Yahoo)**")
        tickers = []
        for i in range(4):
            v = st.text_input(
                "", value="", placeholder=f"Ticker {i+1}", label_visibility="collapsed"
            )
            if v.strip():
                tickers.append(v.strip())
        show_benchmark = st.checkbox("Use benchmark", value=True)
        benchmark = st.text_input("Benchmark", value="^GSPC", label_visibility="collapsed")

    with col_systems:
        st.markdown("**Quant4all Systems**")
        system_choices = ["", "ROCStar", "All Stars", "TAA"]
        systems = []
        default_selection = ["All Stars", "ROCStar", "", ""]
        for i in range(4):
            choice = st.selectbox(
                f"sys{i}",
                system_choices,
                index=system_choices.index(default_selection[i]),
                label_visibility="collapsed",
            )
            if choice:
                systems.append(choice)


# -----------------------
# Helpers
# -----------------------
PALETTE = ["#6366f1", "#e11d48", "#0891b2", "#d97706", "#16a34a", "#8b5cf6"]
BENCH_COLOR = "#9ca3af"


@st.cache_data(show_spinner=False)
def download_prices(ticker: str) -> pd.Series:
    df = yf.download(
        ticker, start="1900-01-01", end=pd.Timestamp.today().normalize(),
        interval="1d", auto_adjust=True, progress=False,
    )
    if df.empty or "Close" not in df.columns:
        return pd.Series(dtype=float)
    close = df["Close"].squeeze().dropna()
    close.index = pd.to_datetime(close.index)
    close.name = ticker.upper()
    return close


def compute_equity_and_dd_from_close(close: pd.Series, initial_capital: float) -> pd.DataFrame:
    df = pd.DataFrame(index=close.index)
    df["close"] = close.astype(float)
    df["ret"] = df["close"].pct_change().fillna(0.0)
    df["equity"] = float(initial_capital) * (1 + df["ret"]).cumprod()
    df["peak"] = df["equity"].cummax()
    df["dd"] = df["equity"] / df["peak"] - 1.0
    return df


def compute_equity_and_dd_from_returns(ret: pd.Series, initial_capital: float) -> pd.DataFrame:
    df = pd.DataFrame(index=ret.index)
    df["ret"] = ret.astype(float).fillna(0.0)
    df["equity"] = float(initial_capital) * (1 + df["ret"]).cumprod()
    df["peak"] = df["equity"].cummax()
    df["dd"] = df["equity"] / df["peak"] - 1.0
    return df


def cagr_from_equity(df: pd.DataFrame) -> float:
    if df.empty or len(df) < 2:
        return np.nan
    total_ret = df["equity"].iloc[-1] / df["equity"].iloc[0]
    years = (df.index[-1] - df.index[0]).days / 365.25
    if years <= 0:
        return np.nan
    return total_ret ** (1 / years) - 1


def ann_vol_from_equity(df: pd.DataFrame) -> float:
    if df is None or df.empty or "ret" not in df.columns:
        return np.nan
    s = pd.Series(df["ret"]).dropna()
    if len(s) < 2:
        return np.nan
    return float(s.std(ddof=1) * np.sqrt(252) * 100.0)


SYSTEM_FILES = {
    "ROCStar":   "data/ROCStar.csv",
    "All Stars": "data/AllStars.csv",
    "Big Three": "data/BigThree.csv",
    "TAA":       "data/TAA.csv",
}


@st.cache_data(show_spinner=False)
def load_system_returns(system_name: str) -> pd.Series:
    path = SYSTEM_FILES.get(system_name)
    if not path or not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el fichero para {system_name}: {path or '—'}")
    # Con ";" explícito: el autodetector confunde la coma decimal ("-0,85") con el separador
    with open(path, encoding="utf-8-sig") as f:
        first_line = f.readline()
    raw = pd.read_csv(
        path, header=None, engine="python", sep=";" if ";" in first_line else None,
        encoding="utf-8-sig", comment="#", skip_blank_lines=True, dtype=str,
        na_values=["", "NA", "NaN", "nan", None],
    )
    if raw.shape[1] < 2:
        s = raw.iloc[:, 0].dropna().astype(str)
        parts = s.str.split(r"[;,|\s]\s*", n=1, expand=True)
        if parts.shape[1] < 2:
            raise ValueError("CSV inválido: necesito 2 columnas (fecha y retorno).")
        raw = parts
    raw = raw.iloc[:, :2].copy()
    raw.columns = ["date", "ret"]
    raw["date"] = raw["date"].astype(str).str.strip()
    idx = pd.to_datetime(raw["date"], dayfirst=True, errors="coerce")
    if idx.isna().all():
        raise ValueError("No se han podido parsear las fechas.")
    idx = pd.to_datetime(idx.dt.date)
    ret_txt = raw["ret"].astype(str).str.replace("%", "", regex=False).str.strip()
    ret_txt = ret_txt.str.replace(",", ".", regex=False)
    ret = pd.to_numeric(ret_txt, errors="coerce")
    if ret.isna().all():
        raise ValueError("No se han podido parsear los retornos.")
    ret = ret / 100.0
    s = pd.Series(ret.values, index=idx).sort_index()
    s = s.groupby(s.index).mean()
    s.name = system_name
    return s


# -----------------------
# Plotting helpers
# -----------------------
PLOTLY_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", size=13, color="#334155"),
    hoverlabel=dict(bgcolor="#0A1428", bordercolor="#0A1428", font=dict(color="white", family="Inter, sans-serif")),
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=0, r=0, t=40, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(showgrid=False, zeroline=False, showline=True,
               linecolor="#E2E8F0", tickfont=dict(size=11, color="#64748B")),
    yaxis=dict(showgrid=True, gridcolor="#EEF2F7", zeroline=False,
               showline=False, tickfont=dict(size=11, color="#64748B"), side="right"),
)


def _apply_layout(fig, title="", height=360):
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text=title, font=dict(size=14, color="#111827")), height=height)
    return fig


def plot_equity(dict_equities, df_bench=None, bench_label=None, show_bench=True,
                unit="$", scale="Lin", series_color=None):
    fig = go.Figure()
    use_log = (unit == "$" and scale == "Log")
    for i, (label, df) in enumerate(dict_equities.items()):
        if df.empty:
            continue
        y = df["equity"] if unit == "$" else (df["equity"] / df["equity"].iloc[0] - 1.0) * 100.0
        color = (series_color or {}).get(label, PALETTE[i % len(PALETTE)])
        fig.add_trace(go.Scatter(
            x=df.index, y=y, mode="lines", name=label,
            line=dict(color=color, width=2.5),
            hovertemplate=f"<b>{label}</b><br>%{{x|%d %b %Y}}<br>{'$%{y:,.0f}' if unit == '$' else '%{y:.2f}%'}<extra></extra>",
        ))
    if show_bench and df_bench is not None and not df_bench.empty:
        yb = df_bench["equity"] if unit == "$" else (df_bench["equity"] / df_bench["equity"].iloc[0] - 1.0) * 100.0
        fig.add_trace(go.Scatter(
            x=df_bench.index, y=yb, mode="lines", name=bench_label,
            line=dict(color=BENCH_COLOR, width=2, dash="dot"),
            hovertemplate=f"<b>{bench_label}</b><br>%{{x|%d %b %Y}}<br>{'$%{y:,.0f}' if unit == '$' else '%{y:.2f}%'}<extra></extra>",
        ))
    _apply_layout(fig, "Equity Curve" + (" (%)" if unit == "%" else ""), height=360)
    fig.update_yaxes(
        side="right",
        type="log" if use_log else "linear",
        ticksuffix=" %" if unit == "%" else "",
        tickformat=".1f" if unit == "%" else ("$,.0f" if not use_log else ""),
    )
    return fig


def plot_dd(dict_equities, df_bench=None, bench_label=None, show_bench=True, series_color=None):
    fig = go.Figure()
    for i, (label, df) in enumerate(dict_equities.items()):
        if df.empty:
            continue
        color = (series_color or {}).get(label, PALETTE[i % len(PALETTE)])
        # Convert hex to rgba for transparent fill
        if color.startswith("#"):
            h = color.lstrip("#")
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            fill_color = f"rgba({r},{g},{b},0.10)"
        else:
            fill_color = color
        fig.add_trace(go.Scatter(
            x=df.index, y=df["dd"] * 100, mode="lines", name=label,
            line=dict(color=color, width=2),
            fill="tozeroy",
            fillcolor=fill_color,
            hovertemplate=f"<b>{label}</b><br>%{{x|%d %b %Y}}<br>%{{y:.2f}}%<extra></extra>",
        ))
    if show_bench and df_bench is not None and not df_bench.empty:
        fig.add_trace(go.Scatter(
            x=df_bench.index, y=df_bench["dd"] * 100, mode="lines", name=bench_label,
            line=dict(color=BENCH_COLOR, width=2, dash="dot"),
            hovertemplate=f"<b>{bench_label}</b><br>%{{x|%d %b %Y}}<br>%{{y:.2f}}%<extra></extra>",
        ))
    _apply_layout(fig, "Drawdown (%)", height=280)
    fig.update_yaxes(ticksuffix=" %", side="right")
    return fig


def render_summary_table(rows):
    html = [f'<div class="table-wrap"><div class="table-title">{icon("target", 16)} Key Metrics</div>']
    html.append('<table class="table-common summary-table"><thead><tr>')
    for h in ["Asset", "Return", "CAGR", "Max DD", "Vol"]:
        html.append(f"<th>{h}</th>")
    html.append("</tr></thead><tbody>")
    for r in rows:
        tr = "<tr>"
        tr += f"<td>{r['Serie']}</td>"
        if np.isnan(r["Total Return"]):
            tr += "<td>—</td><td>—</td><td>—</td><td>—</td>"
        else:
            ret_color = "#16a34a" if r["Total Return"] >= 1 else "#dc2626"
            cagr_color = "#16a34a" if r["CAGR"] >= 0 else "#dc2626"
            dd_color = "#dc2626"
            tr += f"<td><span class='num' style='color:{ret_color}'>{r['Total Return']:.1f}x</span></td>"
            tr += f"<td><span class='num' style='color:{cagr_color}'>{r['CAGR']:.1f}%</span></td>"
            tr += f"<td><span class='num' style='color:{dd_color}'>{r['Max DD']:.1f}%</span></td>"
            tr += f"<td><span class='num'>{r['Vol']:.1f}%</span></td>"
        tr += "</tr>"
        html.append(tr)
    html.append("</tbody></table></div>")
    return "\n".join(html)


def render_top_table(title: str, icon_name: str, table_dict: dict, series_color: dict):
    html = [f'<div class="table-wrap"><div class="table-title">{icon(icon_name, 16)} {title}</div>']
    html.append('<table class="table-common tw-tabular"><thead><tr>')
    html.append("<th>Asset</th>")
    for k in range(1, 6):
        html.append(f"<th># {k}</th>")
    html.append("</tr></thead><tbody>")
    for label, items in table_dict.items():
        color = series_color.get(label, "#111827")
        row = f"<tr><td><span style='color:{color}; font-weight:700'>{label}</span></td>"
        for d, r in items:
            if pd.isna(r) or d is None:
                row += "<td><span class='na' style='color:#d1d5db'>—</span></td>"
            else:
                sign = "+" if r >= 0 else ""
                num_color = "#16a34a" if r >= 0 else "#dc2626"
                row += (
                    "<td>"
                    f"<span class='num' style='color:{num_color}'>{sign}{r*100:.1f}%</span>"
                    f"<span class='tw-date'>{d:%d/%m/%y}</span>"
                    "</td>"
                )
        row += "</tr>"
        html.append(row)
    html.append("</tbody></table></div>")
    return "\n".join(html)


def compute_top_bottom(series: pd.Series, k=5):
    if series is None or series.empty:
        return [], []
    s = series.dropna()
    if s.empty:
        return [], []
    top = s.sort_values(ascending=False).head(k)
    bottom = s.sort_values(ascending=True).head(k)
    return (
        list(zip(top.index.to_pydatetime(), top.values)),
        list(zip(bottom.index.to_pydatetime(), bottom.values)),
    )


def daily_returns_from_close(close: pd.Series) -> pd.Series:
    if close.empty:
        return pd.Series(dtype=float, name=close.name)
    rets = close.pct_change().dropna()
    rets.name = close.name
    return rets


def corr_heatmap_figure(corr_df, labels_order, bench_color, series_color):
    z = corr_df.values
    labels = labels_order
    colorscale = [
        [0.0, "#16a34a"],
        [0.5, "#ffffff"],
        [1.0, "#dc2626"],
    ]
    base_heatmap = go.Heatmap(
        z=z, x=labels, y=labels, zmin=-1, zmax=1,
        colorscale=colorscale, showscale=True,
        colorbar=dict(title="ρ", thickness=14, len=0.8, tickfont=dict(size=11)),
    )
    diag = np.full_like(z, np.nan, dtype=float)
    np.fill_diagonal(diag, 1.0)
    diag_heatmap = go.Heatmap(
        z=diag, x=labels, y=labels, zmin=0, zmax=1,
        colorscale=[[0, "#e5e7eb"], [1, "#e5e7eb"]],
        showscale=False, hoverinfo="skip", opacity=1.0,
    )
    fig = go.Figure(data=[base_heatmap, diag_heatmap])
    for i, yi in enumerate(labels):
        for j, xj in enumerate(labels):
            val = z[i][j]
            if pd.notna(val):
                fig.add_annotation(
                    x=xj, y=yi, text=f"{val:.2f}", showarrow=False,
                    font=dict(size=13, color="white" if abs(val) > 0.5 else "#111827"),
                )
    fig.update_xaxes(side="top", showticklabels=False)
    fig.update_yaxes(autorange="reversed", showticklabels=False)
    for lab in labels:
        fig.add_annotation(
            x=lab, xref="x", y=1.05, yref="paper", text=f"<b>{lab}</b>",
            showarrow=False, font=dict(color=series_color.get(lab, "#111827"), size=13),
            yanchor="bottom",
        )
        fig.add_annotation(
            x=-0.02, xref="paper", y=lab, yref="y", text=f"<b>{lab}</b>",
            showarrow=False, font=dict(color=series_color.get(lab, "#111827"), size=13),
            xanchor="right", yanchor="middle",
        )
    fig.update_layout(
        height=480,
        margin=dict(l=110, r=20, t=70, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, sans-serif"),
    )
    return fig


# -----------------------
# Data load
# -----------------------
dict_closes = {}
for t in tickers:
    s = download_prices(t)
    if not s.empty:
        dict_closes[t.upper()] = s

dict_system_rets = {}
errors = []
for sys in systems:
    try:
        sret = load_system_returns(sys)
        if not sret.empty:
            dict_system_rets[sys] = sret
    except Exception as e:
        errors.append(f"⚠️ {sys}: {e}")

close_bench = None
if show_benchmark and benchmark.strip():
    s = download_prices(benchmark.strip())
    close_bench = s if not s.empty else None

if errors:
    with st.sidebar:
        for msg in errors:
            st.warning(msg)

if not dict_closes and not dict_system_rets and close_bench is None:
    st.info("Introduce al menos un **ticker** o un **sistema** válido.")
    st.stop()

# -----------------------
# Equity series (full history, pre-slice)
# -----------------------
equity_from_assets = {
    label: compute_equity_and_dd_from_close(close, 25000)
    for label, close in dict_closes.items()
}
equity_from_systems = {
    label: compute_equity_and_dd_from_returns(rets, 25000)
    for label, rets in dict_system_rets.items()
}

# -----------------------
# Common date range (benchmark excluded from intersection)
# -----------------------
series_ranges = (
    [(df.index.min(), df.index.max()) for df in equity_from_assets.values() if not df.empty]
    + [(df.index.min(), df.index.max()) for df in equity_from_systems.values() if not df.empty]
)

if not series_ranges:
    st.error("No hay datos válidos para las series seleccionadas.")
    st.stop()

global_start = max(s for s, _ in series_ranges)
global_end   = min(e for _, e in series_ranges)

if global_end < global_start:
    st.error("No hay **rango temporal común** entre los activos/sistemas seleccionados.")
    st.stop()

# -----------------------
# Sidebar date pickers + slider (state management)
# -----------------------
if "start_valid" not in st.session_state:
    st.session_state["start_valid"] = global_start.date()
if "end_valid" not in st.session_state:
    st.session_state["end_valid"] = global_end.date()
if "start_input" not in st.session_state:
    st.session_state["start_input"] = st.session_state["start_valid"]
if "end_input" not in st.session_state:
    st.session_state["end_input"] = st.session_state["end_valid"]
if "date_slider" not in st.session_state:
    st.session_state["date_slider"] = (global_start, global_end)


def _clamp_to_global(d0: datetime, d1: datetime):
    a, b = (d0, d1) if d0 <= d1 else (d1, d0)
    return max(a, global_start), min(b, global_end)


def on_slider_change():
    s, e = st.session_state["date_slider"]
    s, e = _clamp_to_global(s, e)
    st.session_state["start_input"] = s.date()
    st.session_state["end_input"] = e.date()
    st.session_state["start_valid"] = s.date()
    st.session_state["end_valid"] = e.date()
    st.session_state["date_slider"] = (s, e)


def on_dates_change():
    raw_si = st.session_state.get("start_input")
    raw_ei = st.session_state.get("end_input")
    si = raw_si if isinstance(raw_si, date) else st.session_state.get("start_valid")
    ei = raw_ei if isinstance(raw_ei, date) else st.session_state.get("end_valid")
    sdt, edt = _clamp_to_global(datetime.combine(si, time.min), datetime.combine(ei, time.min))
    st.session_state["date_slider"] = (sdt, edt)
    st.session_state["start_valid"] = sdt.date()
    st.session_state["end_valid"] = edt.date()
    st.session_state["start_input"] = sdt.date()
    st.session_state["end_input"] = edt.date()


# Clamp stored state to current global range
raw_si = st.session_state.get("start_input")
raw_ei = st.session_state.get("end_input")
si = raw_si if isinstance(raw_si, date) else st.session_state["start_valid"]
ei = raw_ei if isinstance(raw_ei, date) else st.session_state["end_valid"]
si = max(si, global_start.date())
ei = min(ei, global_end.date())
if si > ei:
    si, ei = global_start.date(), global_end.date()
st.session_state["start_valid"] = si
st.session_state["end_valid"] = ei
st.session_state["start_input"] = si
st.session_state["end_input"] = ei
st.session_state["date_slider"] = (datetime.combine(si, time.min), datetime.combine(ei, time.min))

with st.sidebar:
    with dates_container:
        col_start, col_end = st.columns(2)
        with col_start:
            st.date_input(
                "", key="start_input",
                min_value=global_start.date(), max_value=global_end.date(),
                label_visibility="collapsed", format="DD/MM/YYYY",
                on_change=on_dates_change,
            )
        with col_end:
            st.date_input(
                "", key="end_input",
                min_value=global_start.date(), max_value=global_end.date(),
                label_visibility="collapsed", format="DD/MM/YYYY",
                on_change=on_dates_change,
            )
    with range_slider_container:
        st.slider(
            "",
            min_value=datetime.combine(global_start.date(), time.min),
            max_value=datetime.combine(global_end.date(), time.min),
            key="date_slider",
            on_change=on_slider_change,
            format="DD/MM/YYYY",
        )

# -----------------------
# Slice by selected dates + recompute equity
# -----------------------
current_start, current_end = st.session_state["date_slider"]

dict_equities: dict[str, pd.DataFrame] = {}

for label, close in dict_closes.items():
    c = close.loc[current_start:current_end]
    if not c.empty:
        dict_equities[label] = compute_equity_and_dd_from_close(c, float(initial_capital))

for label, rets in dict_system_rets.items():
    r = rets.loc[current_start:current_end]
    if not r.empty:
        dict_equities[label] = compute_equity_and_dd_from_returns(r, float(initial_capital))

df_bench = None
if show_benchmark and close_bench is not None:
    cb = close_bench.loc[current_start:current_end]
    if not cb.empty:
        df_bench = compute_equity_and_dd_from_close(cb, float(initial_capital))

# -----------------------
# Consistent colors
# -----------------------
SERIES_COLOR: dict[str, str] = {}
for i, label in enumerate(dict_equities.keys()):
    SERIES_COLOR[label] = PALETTE[i % len(PALETTE)]
if show_benchmark and df_bench is not None and not df_bench.empty:
    SERIES_COLOR[benchmark.upper()] = BENCH_COLOR

# -----------------------
# Daily returns map (for correlation, histograms, Top5)
# Order: Benchmark → Systems → Tickers
# -----------------------
daily_map: dict[str, pd.Series] = {}
if show_benchmark and close_bench is not None:
    bd = daily_returns_from_close(close_bench.loc[current_start:current_end])
    if not bd.empty:
        daily_map[benchmark.upper()] = bd
for sys in systems:
    if sys in dict_system_rets:
        r = dict_system_rets[sys].loc[current_start:current_end]
        if not r.empty:
            daily_map[sys] = r
for t in tickers:
    key = t.upper()
    if key in dict_closes:
        r = daily_returns_from_close(dict_closes[key].loc[current_start:current_end])
        if not r.empty:
            daily_map[key] = r


# ======================================================
# ==================  MAIN LAYOUT  =====================
# ======================================================

# ---- Hero (outside tabs) ----
st.markdown("""
<div class='hero'>
  <div class='hero-eyebrow'>Quant4all · Systematic Trading</div>
  <div class='hero-title'>Let's compare <span class='hero-sub'>by Quant4all</span></div>
  <div class='hero-desc'>Compara sistemas y activos, simula carteras y calcula el tamaño de posición
  de los sistemas de corto plazo.</div>
</div>
""", unsafe_allow_html=True)



# ---- Master label order: Systems → Tickers → Benchmark ----
ordered_labels = []
for sys in systems:
    if sys in dict_equities or sys in daily_map:
        ordered_labels.append(sys)
for t in tickers:
    up = t.upper()
    if up in dict_equities or up in daily_map:
        ordered_labels.append(up)
if show_benchmark and df_bench is not None and not df_bench.empty:
    ordered_labels.append(benchmark.upper())

# ---- Performance Summary rows ----
summary_rows = []
for label in ordered_labels:
    df = df_bench if label == benchmark.upper() else dict_equities.get(label)
    color = SERIES_COLOR.get(label, "#111827")
    if df is None or df.empty:
        summary_rows.append({
            "Serie": f"<span style='color:{color}; font-weight:700'>{label}</span>",
            "Total Return": float("nan"), "CAGR": float("nan"),
            "Max DD": float("nan"), "Vol": float("nan"),
        })
    else:
        summary_rows.append({
            "Serie": f"<span style='color:{color}; font-weight:700'>{label}</span>",
            "Total Return": df["equity"].iloc[-1] / df["equity"].iloc[0],
            "CAGR": cagr_from_equity(df) * 100,
            "Max DD": df["dd"].min() * 100,
            "Vol": ann_vol_from_equity(df),
        })

# ---- Top/Worst ----
def _five_dashes():
    return [(None, np.nan)] * 5


top_dict, worst_dict = {}, {}
for label in ordered_labels:
    s = daily_map.get(label)
    if s is None or s.dropna().empty:
        top_dict[label] = _five_dashes()
        worst_dict[label] = _five_dashes()
    else:
        t5, b5 = compute_top_bottom(s, k=5)
        top_dict[label] = t5 + [(None, np.nan)] * (5 - len(t5))
        worst_dict[label] = b5 + [(None, np.nan)] * (5 - len(b5))

# ---- Monthly heat bg helper (shared by both tabs) ----
def bg_color(v: float) -> str:
    if pd.isna(v):
        return ""
    lim = 20.0
    x = max(-lim, min(lim, float(v)))
    if x >= 0:
        alpha = x / lim
        r1, g1, b1 = 220, 252, 231
        r2, g2, b2 = 22, 163, 74
    else:
        alpha = -x / lim
        r1, g1, b1 = 254, 226, 226
        r2, g2, b2 = 220, 38, 38
    r = int(r1 + (r2 - r1) * alpha)
    g = int(g1 + (g2 - g1) * alpha)
    b = int(b1 + (b2 - b1) * alpha)
    return f"background-color: rgb({r},{g},{b});"


# =============================================
# Position sizing — sistemas de corto plazo (réplica del CBT de AmiBroker)
# =============================================
NANO_PV = 0.5          # $ por punto de 1 e-nano (1/10 de un e-micro de 5 $/punto)
NANOS_PER_MICRO = 10

# Mismo orden y parámetros que "ZZ - MultiStategies - Futures - Nano Compound.afl".
#   tipo 1: Max(1, Min(floor(vol), round(lev)))
#   tipo 2: Max(round(vol), floor(lev)); 0 = no opera
#   tipo 3: floor(lev); 0 = no opera
#   tipo 4: Max(1, round(lev))
#   tipo 5: GLD (acciones) = floor(% equity / precio), % = Max(60, Min(100, 150 / Carver))
# con vol = VolPct % equity / riesgo $ de 1 contrato  y  lev = LevSys x equity / nocional de 1 contrato
SHORT_TERM_SYSTEMS = [
    dict(name="RSI2",        market="SPX", side="Largo", tipo=1, vol_pct=2.0, risk="carver", lev=lambda L: L),
    dict(name="BoW",         market="SPX", side="Largo", tipo=4, vol_pct=0.0, risk=None,     lev=lambda L: L),
    dict(name="EoM",         market="SPX", side="Largo", tipo=1, vol_pct=2.0, risk="carver", lev=lambda L: L),
    dict(name="7DL",         market="SPX", side="Largo", tipo=1, vol_pct=2.0, risk="atr10",  lev=lambda L: L),
    dict(name="Oversold",    market="RUT", side="Largo", tipo=1, vol_pct=2.0, risk="carver", lev=lambda L: L),
    dict(name="BlackMonday", market="RUT", side="Corto", tipo=3, vol_pct=0.0, risk=None,     lev=lambda L: max(2.0, L + 0.5)),
    dict(name="ADST",        market="RUT", side="Corto", tipo=2, vol_pct=1.2, risk="carver", lev=lambda L: min(1.0, L - 0.5)),
    dict(name="GLD",         market="GLD", side="Largo", tipo=5, vol_pct=0.0, risk="carver", lev=lambda L: 0.0),
]
SIZING_TICKERS = {"SPX": "^GSPC", "RUT": "^RUT", "GLD": "GLD"}
MICRO_SYMBOL = {"SPX": "MES", "RUT": "M2K"}
NANO_SYMBOL = {"SPX": "NES", "RUT": "N2K"}


def ami_round(x: float) -> int:
    """round() de AmiBroker: los .5 se redondean hacia arriba (Python usa redondeo bancario)."""
    return int(np.floor(x + 0.5))


@st.cache_data(ttl=300, show_spinner=False)
def download_ohlc_sizing(ticker: str, as_of: date) -> pd.DataFrame:
    """OHLC diario hasta as_of (incluido). Para hoy, la vela en curso trae el último precio disponible."""
    start = pd.Timestamp(as_of) - pd.DateOffset(years=4)
    end = pd.Timestamp(as_of) + pd.Timedelta(days=1)          # yfinance: end no incluido
    df = yf.download(ticker, start=start, end=end, interval="1d", auto_adjust=False, progress=False)
    if df.empty:
        return pd.DataFrame()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[["Open", "High", "Low", "Close"]].dropna()
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df[df.index <= pd.Timestamp(as_of)]


def sizing_market_stats(df: pd.DataFrame) -> dict:
    """Cierre, Carver (sqrt(EMA(dif^2, 36))) y ATR(10) de Wilder del último día de la serie."""
    c, h, l = df["Close"], df["High"], df["Low"]
    carver = np.sqrt((c.diff() ** 2).ewm(span=36, adjust=False).mean())
    prev_c = c.shift(1)
    tr = pd.concat([h - l, (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    atr10 = tr.ewm(alpha=1 / 10, adjust=False).mean()
    return {
        "date": df.index[-1],
        "close": float(c.iloc[-1]),
        "carver": float(carver.iloc[-1]),
        "atr10": float(atr10.iloc[-1]),
    }


def size_short_term_system(sys_cfg: dict, stats: dict, equity: float, leverage: float) -> dict:
    """Nº de e-nanos (o acciones de GLD) que daría el CBT para una entrada con esta equity."""
    tipo = sys_cfg["tipo"]
    price = stats["close"]

    if tipo == 5:
        pct = max(60.0, min(100.0, 150.0 / stats["carver"]))
        n = int(np.floor(0.01 * pct * equity / price))
        return {"n": n, "notional": n * price, "pct": pct}

    notional_1 = price * NANO_PV
    levc = sys_cfg["lev"](leverage) * equity / notional_1
    volc = 0.0
    if sys_cfg["vol_pct"] > 0:
        volc = 0.01 * sys_cfg["vol_pct"] * equity / (stats[sys_cfg["risk"]] * NANO_PV)

    if tipo == 1:
        n = max(1, min(int(np.floor(volc)), ami_round(levc)))
    elif tipo == 2:
        n = max(ami_round(volc), int(np.floor(levc)))
    elif tipo == 3:
        n = int(np.floor(levc))
    else:
        n = max(1, ami_round(levc))

    n = max(n, 0)
    return {"n": n, "notional": n * notional_1}


def split_micro_nano(n: int) -> tuple:
    return n // NANOS_PER_MICRO, n % NANOS_PER_MICRO


# =============================================
# TABS
# =============================================
tab_compare, tab_simulator, tab_sizing = st.tabs(
    [":material/insights: Comparador", ":material/account_balance_wallet: Simulador de Cartera",
     ":material/calculate: Calculadora de Posición"]
)


# =============================================
# TAB 1 — Comparador
# =============================================
with tab_compare:

    # Section 1 — Performance Summary
    section_header("Performance Summary", "award")

    c1, c2, c3 = st.columns([0.30, 0.35, 0.35], gap="small")
    with c1:
        if summary_rows:
            st.markdown(render_summary_table(summary_rows), unsafe_allow_html=True)
        else:
            st.info("Sin datos en el rango seleccionado.")
    with c2:
        st.markdown(render_top_table("Top Daily Returns", "trending-up", top_dict, SERIES_COLOR), unsafe_allow_html=True)
    with c3:
        st.markdown(render_top_table("Worst Daily Returns", "trending-down", worst_dict, SERIES_COLOR), unsafe_allow_html=True)

    st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)

    # Section 2 — Equity & Drawdown
    c_title, c_ctrl = st.columns([0.75, 0.25])
    with c_title:
        section_header("Equity & Drawdown", "trending-up")
    with c_ctrl:
        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        col_u, col_s = st.columns(2)
        with col_u:
            unit_choice = st.radio("", options=["$", "%"], index=0, horizontal=True, label_visibility="collapsed")
        with col_s:
            scale_choice = st.radio("", options=["Lin", "Log"], index=0, horizontal=True, label_visibility="collapsed")

    equity_fig = plot_equity(
        dict_equities, df_bench, benchmark.upper() if show_benchmark else None,
        show_bench=show_benchmark, unit=unit_choice, scale=scale_choice,
        series_color=SERIES_COLOR,
    )
    st.plotly_chart(equity_fig, use_container_width=True, config={"displayModeBar": False})

    dd_fig = plot_dd(
        dict_equities, df_bench, benchmark.upper() if show_benchmark else None,
        show_bench=show_benchmark, series_color=SERIES_COLOR,
    )
    st.plotly_chart(dd_fig, use_container_width=True, config={"displayModeBar": False})

    legend_items = [
        f"<span style='display:inline-flex; align-items:center; gap:5px; margin-right:14px;'>"
        f"<span style='width:18px; height:4px; border-radius:2px; background:{SERIES_COLOR.get(lab, '#111827')}; display:inline-block;'></span>"
        f"<span style='font-size:0.85rem; font-weight:600; color:#374151;'>{lab}</span>"
        f"</span>"
        for lab in ordered_labels
    ]
    st.markdown(
        "<div style='text-align:center; margin-top:-0.5rem; margin-bottom:1rem;'>"
        + "".join(legend_items) + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)

    # Section 3 — Distribution of Daily Returns
    section_header("Distribution of Daily Returns", "bar-chart")

    labels_all = (
        [t.upper() for t in tickers if t.upper() in daily_map]
        + [s for s in systems if s in daily_map]
        + ([benchmark.upper()] if show_benchmark and benchmark.upper() in daily_map else [])
    )

    if not labels_all:
        st.info("No hay series disponibles para el periodo seleccionado.")
    else:
        _, sel_col, _ = st.columns([0.425, 0.15, 0.425])
        with sel_col:
            selected_label = st.selectbox("Serie", labels_all, index=0, label_visibility="collapsed")

        vals = daily_map[selected_label].dropna() * 100.0
        if vals.empty:
            st.info("No hay datos de retornos diarios para la serie seleccionada.")
        else:
            mu = float(vals.mean())
            sigma = float(vals.std(ddof=1)) if len(vals) > 1 else 0.0
            skew_val = float(vals.skew()) if len(vals) > 2 else 0.0
            kurt_val = float(vals.kurtosis()) if len(vals) > 3 else 0.0

            col_plot, col_side = st.columns([0.75, 0.25], gap="large")

            hist_fig = go.Figure()
            series_col = SERIES_COLOR.get(selected_label, "#6366f1")
            hist_fig.add_trace(go.Histogram(
                x=vals, nbinsx=100, name=selected_label,
                marker=dict(color=series_col, line=dict(color="white", width=0.3)),
                opacity=0.9,
                hovertemplate="%{x:.2f}%<extra></extra>",
            ))
            for k, opac in zip((3, 2, 1), (0.08, 0.13, 0.20)):
                x0, x1 = mu - k * sigma, mu + k * sigma
                if np.isfinite(x0) and np.isfinite(x1):
                    hist_fig.add_vrect(x0=x0, x1=x1, fillcolor="#9ca3af", opacity=opac, line_width=0)
            hist_fig.add_vline(x=mu, line=dict(color="#111827", width=2))
            for k in (1, 2, 3):
                for xk in (mu + k * sigma, mu - k * sigma):
                    hist_fig.add_vline(x=xk, line=dict(color="#6b7280", width=1, dash="dash"))
            hist_fig.add_annotation(x=mu, y=1.06, xref="x", yref="paper", text="μ",
                                     showarrow=False, font=dict(size=12, color="#111827"))
            for k, lbl in zip((1, 2, 3), ("±1σ", "±2σ", "±3σ")):
                for sign, prefix in ((1, "+"), (-1, "-")):
                    hist_fig.add_annotation(
                        x=mu + sign * k * sigma, y=1.06, xref="x", yref="paper",
                        text=f"{prefix}{lbl}", showarrow=False, font=dict(size=10, color="#6b7280"),
                    )
            _apply_layout(hist_fig, "", height=460)
            hist_fig.update_layout(
                xaxis_title="Daily Return (%)",
                yaxis=dict(title="Frequency", side="left", showgrid=True,
                           gridcolor="#f3f4f6", tickfont=dict(size=11)),
                bargap=0.02, showlegend=False,
            )

            with col_plot:
                st.plotly_chart(hist_fig, use_container_width=True, config={"displayModeBar": False})

            with col_side:
                st.markdown(f"""
                <div class='stats-card'>
                    <div class='stats-title'>Statistics</div>
                    <div class='stats-row'>
                        <span class='stat-label'>Mean (μ)</span>
                        <span class='stat-val'>{mu:+.3f}%</span>
                    </div>
                    <div class='stats-row'>
                        <span class='stat-label'>Std Dev (σ)</span>
                        <span class='stat-val'>{sigma:.3f}%</span>
                    </div>
                    <div class='stats-row'>
                        <span class='stat-label'>Skewness</span>
                        <span class='stat-val'>{skew_val:+.3f}</span>
                    </div>
                    <div class='stats-row'>
                        <span class='stat-label'>Kurtosis</span>
                        <span class='stat-val'>{kurt_val:+.3f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

                _, th_col, _ = st.columns([0.15, 0.7, 0.15])
                with th_col:
                    st.markdown("<div style='text-align:center; font-size:0.82rem; font-weight:700; color:#6b7280; text-transform:uppercase; letter-spacing:.05em; margin-bottom:4px;'>Threshold (%)</div>", unsafe_allow_html=True)
                    threshold_pct = st.number_input(
                        "", min_value=0.0, max_value=100.0, value=5.0,
                        step=0.5, format="%.1f", label_visibility="collapsed",
                    )

                thr = float(threshold_pct)
                pos_days = int((vals >= +thr).sum())
                neg_days = int((vals <= -thr).sum())

                st.markdown("<div style='text-align:center; font-size:0.82rem; font-weight:700; color:#6b7280; text-transform:uppercase; letter-spacing:.05em; margin-bottom:6px; margin-top:1rem;'>Days beyond threshold</div>", unsafe_allow_html=True)

                k1, k2 = st.columns(2)
                with k1:
                    st.markdown(f"""
                    <div class='count-card positive'>
                        <div class='count-label'>≥ +{thr:.1f}%</div>
                        <div class='count-val'>{pos_days}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with k2:
                    st.markdown(f"""
                    <div class='count-card negative'>
                        <div class='count-label'>≤ -{thr:.1f}%</div>
                        <div class='count-val'>{neg_days}</div>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)

    # Section 5 — Distribution of Monthly Returns
    section_header("Distribution of Monthly Returns", "calendar")

    st.markdown("""
    <style>
    .monthly-heat-wrap { width: 90%; margin: 0 auto; }
    .monthly-heat {
        border-collapse: collapse; width: 100%; table-layout: fixed;
        font-size: 0.88rem; font-family: 'Inter', sans-serif;
    }
    .monthly-heat th, .monthly-heat td {
        border: 1px solid #e5e7eb;
        padding: 6px 4px; text-align: center; vertical-align: middle;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .monthly-heat thead th {
        background: #f9fafb; font-weight: 700; font-size: 0.76rem;
        color: #6b7280; text-transform: uppercase; letter-spacing: 0.04em;
    }
    .monthly-heat tfoot td { background: #f9fafb; font-weight: 700; color: #374151; }
    .monthly-heat td.year-col, .monthly-heat th.year-col { width: 6.5%; font-weight: 700; color: #374151; }
    .monthly-heat th.mon-col, .monthly-heat td.mon-col { width: 6.5%; }
    .monthly-heat th.ytd-col, .monthly-heat td.ytd-col { width: 7%; font-weight: 800; }
    .monthly-heat .cell { color: #111827; font-weight: 600; }
    .monthly-heat .na { color: #9ca3af; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

    available_labels = []
    label_to_series = {}
    if show_benchmark and close_bench is not None and not close_bench.empty:
        available_labels.append(benchmark.upper())
        label_to_series[benchmark.upper()] = close_bench
    for sys, rets in dict_system_rets.items():
        if not rets.empty:
            available_labels.append(sys)
            label_to_series[sys] = rets
    for t, s in dict_closes.items():
        if not s.empty:
            available_labels.append(t.upper())
            label_to_series[t.upper()] = s

    if not available_labels:
        st.info("Añade al menos un ticker, sistema o benchmark.")
    else:
        _, sel_col2, _ = st.columns([0.425, 0.15, 0.425])
        with sel_col2:
            monthly_label = st.selectbox("Serie mensual", available_labels, index=0, label_visibility="collapsed")

        ser = label_to_series[monthly_label].loc[current_start:current_end]
        if ser.empty:
            st.info("No hay datos en el rango seleccionado para esta serie.")
        else:
            if monthly_label in dict_system_rets:
                m_ret = ser.resample("ME").apply(lambda x: (1 + x).prod() - 1) * 100
            else:
                m_close = ser.resample("ME").last()
                m_ret = m_close.pct_change() * 100

            df_m = m_ret.to_frame("ret").dropna(how="all")
            df_m["Year"] = df_m.index.year
            df_m["Month"] = df_m.index.month
            pivot = df_m.pivot(index="Year", columns="Month", values="ret").sort_index()
            yret = ((1.0 + pivot / 100.0).prod(axis=1) - 1.0) * 100.0
            avg_row = pivot.mean(axis=0)
            avg_y = yret.mean()

            months_abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

            html = ["<div class='monthly-heat-wrap'><table class='monthly-heat'>"]
            html.append("<thead><tr><th class='year-col'>Year</th>")
            for m in months_abbr:
                html.append(f"<th class='mon-col'>{m}</th>")
            html.append("<th class='ytd-col'>Yr%</th></tr></thead><tbody>")
            for yr in pivot.index:
                html.append(f"<tr><td class='year-col'>{yr}</td>")
                for m_idx in range(1, 13):
                    v = pivot.loc[yr].get(m_idx, np.nan)
                    if pd.isna(v):
                        html.append("<td class='mon-col na'>—</td>")
                    else:
                        html.append(f"<td class='mon-col' style='{bg_color(v)}'>"
                                    f"<span class='cell'>{v:+.1f}%</span></td>")
                vy = yret.get(yr, np.nan)
                if pd.isna(vy):
                    html.append("<td class='ytd-col na'>—</td>")
                else:
                    html.append(f"<td class='ytd-col' style='{bg_color(vy)}'>"
                                f"<span class='cell'>{vy:+.1f}%</span></td>")
                html.append("</tr>")
            html.append("</tbody><tfoot><tr><td class='year-col'>Avg</td>")
            for m_idx in range(1, 13):
                v = avg_row.get(m_idx, np.nan)
                if pd.isna(v):
                    html.append("<td class='mon-col na'>—</td>")
                else:
                    html.append(f"<td class='mon-col' style='{bg_color(v)}'>"
                                f"<span class='cell'>{v:+.1f}%</span></td>")
            if pd.isna(avg_y):
                html.append("<td class='ytd-col na'>—</td>")
            else:
                html.append(f"<td class='ytd-col' style='{bg_color(avg_y)}'>"
                            f"<span class='cell'>{avg_y:+.1f}%</span></td>")
            html.append("</tr></tfoot></table></div>")
            st.markdown("".join(html), unsafe_allow_html=True)


# =============================================
# TAB 2 — Simulador de Cartera
# =============================================
with tab_simulator:

    # Series disponibles: sistemas + tickers (sin benchmark, sin cash)
    sim_series_keys = [s for s in systems if s in dict_system_rets] + \
                      [t.upper() for t in tickers if t.upper() in dict_closes]

    if not sim_series_keys:
        st.info("Añade al menos un **ticker** o **sistema** en la barra lateral para usar el simulador.")
    else:
        # ---- Construir retornos diarios de cada serie ----
        @st.cache_data(show_spinner=False)
        def get_daily_returns(series_key: str, start, end) -> pd.Series:
            if series_key in dict_system_rets:
                d = dict_system_rets[series_key].loc[start:end]
            else:
                close = dict_closes[series_key].loc[start:end]
                d = daily_returns_from_close(close)
            d.name = series_key
            return d.dropna()

        daily_series = {}
        for key in sim_series_keys:
            ds = get_daily_returns(key, current_start, current_end)
            if not ds.empty:
                daily_series[key] = ds

        if not daily_series:
            st.info("No hay datos en el rango seleccionado para simular.")
        else:
            # Alinear todas las series al índice común
            df_daily = pd.concat(daily_series.values(), axis=1).dropna()
            df_daily.columns = list(daily_series.keys())

            n_series = len(df_daily.columns)
            series_list = list(df_daily.columns)

            # ---- Controles: pesos + rebalanceo + cash ----
            section_header("Pesos de la cartera", "pie-chart")

            # Pesos por defecto: distribución equitativa entre series (sin cash), suma = 100
            base_w = 100 // n_series
            remainder_w = 100 - base_w * n_series
            default_weights = {key: base_w + (remainder_w if i == 0 else 0)
                               for i, key in enumerate(series_list)}

            # Lista de elementos a renderizar: activos + Cash (cada uno con su propia celda)
            slider_items = [(k, SERIES_COLOR.get(k, PALETTE[i % len(PALETTE)]))
                            for i, k in enumerate(series_list)]
            slider_items.append(("Cash", "#9ca3af"))

            raw_weights = {}
            w_cash_pct = 0
            cols_per_row = 4  # máximo de sliders por fila

            for row_start in range(0, len(slider_items), cols_per_row):
                row_items = slider_items[row_start:row_start + cols_per_row]
                cols = st.columns(len(row_items))
                for col, (key, color) in zip(cols, row_items):
                    with col:
                        st.markdown(
                            f"<div style='color:{color}; font-weight:700; font-size:0.85rem; margin-bottom:2px;'>{key}</div>",
                            unsafe_allow_html=True,
                        )
                        if key == "Cash":
                            w_cash_pct = st.slider(
                                "w_cash", 0, 100, 0, step=1,
                                label_visibility="collapsed", key="sim_w_cash",
                            )
                        else:
                            raw_weights[key] = st.slider(
                                f"w_{key}", 0, 100, default_weights[key], step=1,
                                label_visibility="collapsed", key=f"sim_w_{key}",
                            )

            total_w = sum(raw_weights.values()) + w_cash_pct

            # Barra visual de pesos
            if total_w > 0:
                bar_segs = ""
                for i, (key, w) in enumerate(raw_weights.items()):
                    if w > 0:
                        color = SERIES_COLOR.get(key, PALETTE[i % len(PALETTE)])
                        pct = w / total_w * 100
                        bar_segs += f"<div style='width:{pct:.1f}%; background:{color}; height:100%;'></div>"
                if w_cash_pct > 0:
                    pct = w_cash_pct / total_w * 100
                    bar_segs += f"<div style='width:{pct:.1f}%; background:#9ca3af; height:100%;'></div>"
                st.markdown(f"""
                <div style='display:flex; height:10px; border-radius:5px; overflow:hidden;
                            gap:2px; margin:0.5rem 0 0.25rem 0;'>{bar_segs}</div>
                """, unsafe_allow_html=True)

            # Indicador suma
            sum_color = "#16a34a" if total_w == 100 else "#dc2626"
            st.markdown(
                f"<div style='font-size:0.82rem; font-weight:700; color:{sum_color}; margin-bottom:0.5rem;'>"
                f"Suma de pesos: {total_w}% {'✓' if total_w == 100 else '— deben sumar 100%'}</div>",
                unsafe_allow_html=True,
            )

            # ---- Rebalanceo + Cash rate ----
            ctrl1, ctrl2, _ = st.columns([0.25, 0.25, 0.5])
            with ctrl1:
                rebal_options = {"Mensual": 1, "Trimestral": 3, "Semestral": 6, "Anual": 12, "Sin rebalanceo": 0}
                rebal_label = st.selectbox("Rebalanceo", list(rebal_options.keys()), index=3)
                rebal_months = rebal_options[rebal_label]
            with ctrl2:
                cash_rate_annual = st.number_input("Cash rate (% anual)", min_value=0.0, max_value=10.0,
                                                    value=2.0, step=0.25, format="%.2f")

            if total_w != 100:
                st.warning("Ajusta los pesos para que sumen exactamente 100%.")
            else:
                # ---- Simulación (diaria) ----
                weights = {k: v / 100.0 for k, v in raw_weights.items()}
                w_cash = w_cash_pct / 100.0
                cash_rate_d = (1 + cash_rate_annual / 100) ** (1 / 252) - 1

                # Fechas de rebalanceo: último día hábil de cada N meses.
                # El usuario sigue eligiendo la frecuencia en meses; el motor corre en diario.
                rebal_dates = set()
                if rebal_months > 0:
                    month_ends = df_daily.groupby(df_daily.index.to_period("M")).apply(
                        lambda g: g.index[-1]
                    )
                    rebal_dates = set(month_ends.iloc[rebal_months - 1::rebal_months])

                current_w = {k: weights[k] for k in series_list}
                current_w_cash = w_cash

                equity = float(initial_capital)
                equity_curve = [equity]
                daily_rets_port = []
                dates_sim = [df_daily.index[0] - pd.tseries.offsets.BDay(1)]

                for dt, row in df_daily.iterrows():
                    r_port = sum(current_w[k] * row[k] for k in series_list) + current_w_cash * cash_rate_d
                    equity *= (1 + r_port)
                    equity_curve.append(equity)
                    daily_rets_port.append(r_port)
                    dates_sim.append(dt)

                    # 1) Derivar pesos según la rentabilidad de cada componente
                    #    (buy & hold: el peso crece/decrece con su retorno relativo)
                    factor = 1 + r_port
                    if abs(factor) > 1e-9:
                        for k in series_list:
                            current_w[k] *= (1 + row[k]) / factor
                        current_w_cash *= (1 + cash_rate_d) / factor

                    # 2) Resetear a pesos objetivo en los puntos de rebalanceo
                    #    (rebal_months == 0 → nunca resetea → buy & hold puro)
                    if dt in rebal_dates:
                        current_w = {k: weights[k] for k in series_list}
                        current_w_cash = w_cash

                # ---- Series de la cartera ----
                ret_sim = pd.Series(daily_rets_port, index=df_daily.index, name="ret")
                eq_sim = pd.Series(equity_curve[1:], index=df_daily.index, name="equity")

                # Métricas (convenciones del resto de la app: CAGR calendario, vol √252 ddof=1)
                n_years = (df_daily.index[-1] - df_daily.index[0]).days / 365.25
                total_ret = equity / float(initial_capital)
                cagr_sim = total_ret ** (1 / n_years) - 1 if n_years > 0 else np.nan
                vol_sim = float(ret_sim.std(ddof=1) * np.sqrt(252)) if len(ret_sim) > 1 else np.nan
                sharpe_sim = cagr_sim / vol_sim if vol_sim and vol_sim > 0 else np.nan

                cum = np.array(equity_curve)
                roll_max = np.maximum.accumulate(cum)
                dd_curve_sim = (cum - roll_max) / roll_max * 100
                max_dd_sim = float(dd_curve_sim.min())

                # VaR histórico diario: percentil empírico de los retornos de la cartera.
                # Sin supuesto de normalidad, así que recoge las colas reales de la serie.
                var95_sim = float(np.percentile(ret_sim, 5)) if len(ret_sim) > 1 else np.nan
                var99_sim = float(np.percentile(ret_sim, 1)) if len(ret_sim) > 1 else np.nan

                # Retornos mensuales de la cartera (agregación para la tabla y la vista mensual)
                monthly_rets_sim = ret_sim.resample("ME").apply(lambda x: (1 + x).prod() - 1)

                # Rentabilidades anuales
                annual_sim = eq_sim.resample("YE").last().pct_change().dropna()
                annual_sim.index = annual_sim.index.year

                # ---- KPI cards ----
                st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)
                section_header("Resultados", "bar-chart")

                # Periodo realmente simulado (intersección común de todas las series)
                sim_ini = df_daily.index[0]
                sim_fin = df_daily.index[-1]
                st.caption(
                    f"📅 Periodo común simulado: **{sim_ini:%d %b %Y} → {sim_fin:%d %b %Y}** "
                    f"({len(df_daily)} sesiones · {n_series} activo(s)). "
                    f"Si una serie empieza más tarde, la simulación se recorta al solape de todas."
                )

                kc1, kc2, kc3, kc4 = st.columns(4)
                def _kpi(col, label, value, color="#111827"):
                    col.markdown(f"""
                    <div class='kpi-card'>
                        <div class='kpi-label'>{label}</div>
                        <div class='kpi-value' style='color:{color};'>{value}</div>
                    </div>
                    """, unsafe_allow_html=True)

                _kpi(kc1, "CAGR", f"{cagr_sim*100:.2f}%", "#16a34a" if cagr_sim > 0 else "#dc2626")
                _kpi(kc2, "Volatilidad", f"{vol_sim*100:.2f}%")
                _kpi(kc3, "Sharpe", f"{sharpe_sim:.2f}", "#16a34a" if sharpe_sim > 1 else "#d97706" if sharpe_sim > 0 else "#dc2626")
                _kpi(kc4, "Max Drawdown", f"{max_dd_sim:.2f}%", "#dc2626")

                # ---- VaR (segunda fila, dos tarjetas) ----
                st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
                # 4 columnas (no 2) para que las tarjetas midan igual que la fila de arriba;
                # las dos de la derecha se quedan vacías a propósito.
                vc1, vc2, _vc3, _vc4 = st.columns(4)
                _kpi(vc1, "VaR 95% (diario)", f"{var95_sim*100:.2f}%", "#dc2626")
                _kpi(vc2, "VaR 99% (diario)", f"{var99_sim*100:.2f}%", "#dc2626")
                st.caption(
                    "VaR histórico sobre los retornos diarios de la cartera simulada: pérdida diaria "
                    "que solo se supera el 5% / 1% de las sesiones del periodo seleccionado."
                )

                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

                # ---- Gráficos ----
                sim_tab1, sim_tab2, sim_tab3 = st.tabs([":material/show_chart: Equity", ":material/trending_down: Drawdown", ":material/calendar_month: Rentabilidad anual"])

                with sim_tab1:
                    fig_eq = go.Figure()
                    fig_eq.add_trace(go.Scatter(
                        x=dates_sim, y=equity_curve, mode="lines", name="Cartera",
                        line=dict(color="#6366f1", width=2.5),
                        fill="tozeroy", fillcolor="rgba(99,102,241,0.07)",
                        hovertemplate="%{x|%b %Y}<br>$%{y:,.0f}<extra></extra>",
                    ))
                    _apply_layout(fig_eq, "Equity Curve", height=380)
                    fig_eq.update_yaxes(tickformat="$,.0f", side="right")
                    st.plotly_chart(fig_eq, use_container_width=True, config={"displayModeBar": False})

                with sim_tab2:
                    fig_dd2 = go.Figure()
                    fig_dd2.add_trace(go.Scatter(
                        x=dates_sim, y=dd_curve_sim, mode="lines", name="Drawdown",
                        line=dict(color="#e11d48", width=2),
                        fill="tozeroy", fillcolor="rgba(225,29,72,0.08)",
                        hovertemplate="%{x|%b %Y}<br>%{y:.2f}%<extra></extra>",
                    ))
                    _apply_layout(fig_dd2, "Drawdown (%)", height=380)
                    fig_dd2.update_yaxes(ticksuffix=" %", side="right")
                    st.plotly_chart(fig_dd2, use_container_width=True, config={"displayModeBar": False})

                with sim_tab3:
                    bar_colors = ["#16a34a" if v >= 0 else "#dc2626" for v in annual_sim.values]
                    fig_bar = go.Figure()
                    fig_bar.add_trace(go.Bar(
                        x=annual_sim.index.astype(str),
                        y=(annual_sim * 100).round(2),
                        marker_color=bar_colors,
                        hovertemplate="%{x}<br>%{y:.2f}%<extra></extra>",
                    ))
                    _apply_layout(fig_bar, "Annual Returns (%)", height=380)
                    fig_bar.update_layout(bargap=0.3)
                    fig_bar.update_yaxes(ticksuffix=" %", side="right")
                    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

                # ---- Correlation Matrix ----
                st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)
                section_header("Correlation Matrix", "grid")
                if len(daily_map) >= 2:
                    ddf = pd.concat(list(daily_map.values()), axis=1)
                    ddf.columns = list(daily_map.keys())
                    ddf = ddf.dropna(how="all")
                    corr_df = ddf.corr(method="pearson", min_periods=3)
                    ordered_corr = list(daily_map.keys())
                    corr_df = corr_df.reindex(index=ordered_corr, columns=ordered_corr)
                    st.plotly_chart(
                        corr_heatmap_figure(corr_df, ordered_corr, BENCH_COLOR, SERIES_COLOR),
                        use_container_width=True, config={"displayModeBar": False},
                    )
                else:
                    st.info("Añade al menos **dos** series con datos en el periodo para ver la correlación.")

                # ---- Tabla mensual de la cartera ----
                st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)
                section_header("Monthly Returns — Cartera", "calendar")

                df_mport = pd.DataFrame({"ret": monthly_rets_sim * 100.0}, index=monthly_rets_sim.index)
                df_mport["Year"] = df_mport.index.year
                df_mport["Month"] = df_mport.index.month
                pivot_p = df_mport.pivot(index="Year", columns="Month", values="ret").sort_index()
                yret_p = ((1.0 + pivot_p / 100.0).prod(axis=1) - 1.0) * 100.0
                avg_row_p = pivot_p.mean(axis=0)
                avg_y_p = yret_p.mean()

                months_abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

                html_p = ["<div class='monthly-heat-wrap'><table class='monthly-heat'>"]
                html_p.append("<thead><tr><th class='year-col'>Year</th>")
                for m in months_abbr:
                    html_p.append(f"<th class='mon-col'>{m}</th>")
                html_p.append("<th class='ytd-col'>Yr%</th></tr></thead><tbody>")
                for yr in pivot_p.index:
                    html_p.append(f"<tr><td class='year-col'>{yr}</td>")
                    for m_idx in range(1, 13):
                        v = pivot_p.loc[yr].get(m_idx, np.nan)
                        if pd.isna(v):
                            html_p.append("<td class='mon-col na'>—</td>")
                        else:
                            html_p.append(f"<td class='mon-col' style='{bg_color(v)}'>"
                                          f"<span class='cell'>{v:+.1f}%</span></td>")
                    vy = yret_p.get(yr, np.nan)
                    if pd.isna(vy):
                        html_p.append("<td class='ytd-col na'>—</td>")
                    else:
                        html_p.append(f"<td class='ytd-col' style='{bg_color(vy)}'>"
                                      f"<span class='cell'>{vy:+.1f}%</span></td>")
                    html_p.append("</tr>")
                html_p.append("</tbody><tfoot><tr><td class='year-col'>Avg</td>")
                for m_idx in range(1, 13):
                    v = avg_row_p.get(m_idx, np.nan)
                    if pd.isna(v):
                        html_p.append("<td class='mon-col na'>—</td>")
                    else:
                        html_p.append(f"<td class='mon-col' style='{bg_color(v)}'>"
                                      f"<span class='cell'>{v:+.1f}%</span></td>")
                if pd.isna(avg_y_p):
                    html_p.append("<td class='ytd-col na'>—</td>")
                else:
                    html_p.append(f"<td class='ytd-col' style='{bg_color(avg_y_p)}'>"
                                  f"<span class='cell'>{avg_y_p:+.1f}%</span></td>")
                html_p.append("</tr></tfoot></table></div>")
                st.markdown("".join(html_p), unsafe_allow_html=True)

                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
                st.caption(
                    "Simulación basada en retornos históricos. "
                    "El rebalanceo se aplica al final de cada periodo. "
                    "El cash se remunera al tipo anual configurado. "
                    "Resultados pasados no garantizan rentabilidades futuras."
                )


# =============================================
# TAB 3 — Calculadora de Posición (sistemas de corto plazo)
# =============================================
with tab_sizing:

    section_header("Tamaño de posición — Sistemas de corto plazo", "calculator")

    today_ny = datetime.now(ZoneInfo("America/New_York")).date()

    sz_controls = st.container(border=True)
    c_cap, c_lev, c_date = sz_controls.columns([0.30, 0.40, 0.30], gap="large")
    with c_cap:
        sz_capital = st.number_input(
            "Capital ($)", min_value=1000, value=10000, step=1000, key="sz_capital",
        )
    with c_lev:
        sz_leverage = st.select_slider(
            "Apalancamiento",
            options=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0],
            value=1.25,
            key="sz_leverage",
            help="Para RSI2, BoW, EoM, 7DL y Oversold se usa tal cual. "
                 "ADST usa Min(1, apalanc. − 0,5) y BlackMonday Max(2, apalanc. + 0,5).",
        )
    with c_date:
        sz_date = st.date_input(
            "Fecha", value=today_ny, min_value=date(2006, 1, 1), max_value=today_ny,
            format="DD/MM/YYYY", key="sz_date",
            help="Cierre de esa fecha (o de la última sesión anterior si fue festivo). "
                 "Para hoy se usa el último valor disponible.",
        )

    with st.spinner("Descargando precios…"):
        sz_stats, sz_errors = {}, []
        for mkt, yticker in SIZING_TICKERS.items():
            try:
                df_mkt = download_ohlc_sizing(yticker, sz_date)
            except Exception:
                df_mkt = pd.DataFrame()
            if len(df_mkt) < 60:
                sz_errors.append(f"No hay datos suficientes de {yticker} para esa fecha.")
            else:
                sz_stats[mkt] = sizing_market_stats(df_mkt)

    for msg in sz_errors:
        st.warning(msg)

    if sz_stats:
        # ---- KPIs: precios usados ----
        now_ny = datetime.now(ZoneInfo("America/New_York"))
        session_open = now_ny.time() < time(16, 15)
        mkt_labels = {"SPX": "S&P 500", "RUT": "Russell 2000", "GLD": "GLD"}
        kpi_html = ["<div class='kpi-grid'>"]
        for mkt, label in mkt_labels.items():
            if mkt in sz_stats:
                s = sz_stats[mkt]
                if s["date"].date() == today_ny and session_open:
                    foot = (f"<div class='kpi-foot live'><span class='live-dot'></span>"
                            f"Último · {now_ny:%d/%m/%Y %H:%M} NY</div>")
                else:
                    foot = f"<div class='kpi-foot'>Cierre · {s['date']:%d/%m/%Y}</div>"
                kpi_html.append(
                    f"<div class='kpi-card'><div class='kpi-label'>{label}</div>"
                    f"<div class='kpi-value'>{s['close']:,.2f}</div>{foot}</div>"
                )
        kpi_html.append("</div>")
        st.markdown("".join(kpi_html), unsafe_allow_html=True)

        # ---- Tabla de tamaños ----
        rows_html = []
        total_notional = 0.0
        for cfg in SHORT_TERM_SYSTEMS:
            stats = sz_stats.get(cfg["market"])
            if stats is None:
                continue
            r = size_short_term_system(cfg, stats, float(sz_capital), float(sz_leverage))
            n = r["n"]
            total_notional += r["notional"]
            if cfg["side"] == "Largo":
                side_chip = f"<span class='chip chip-long'>{icon('arrow-up-right', 14, 2.5)}Largo</span>"
            else:
                side_chip = f"<span class='chip chip-short'>{icon('arrow-down-right', 14, 2.5)}Corto</span>"

            if n == 0:
                chips = ["<span class='chip chip-off'>No opera</span>"]
            elif cfg["tipo"] == 5:
                chips = [f"<span class='chip chip-shares'><b>{r['pct']:.0f} %</b> - <b>{n:,}</b> acciones GLD</span>"]
            else:
                micros, nanos = split_micro_nano(n)
                chips = []
                if micros:
                    chips.append(f"<span class='chip chip-micro'><b>{micros}</b> e-micro "
                                 f"{MICRO_SYMBOL[cfg['market']]}</span>")
                if nanos:
                    chips.append(f"<span class='chip chip-nano'><b>{nanos}</b> e-nano "
                                 f"{NANO_SYMBOL[cfg['market']]}</span>")
            position = "<div class='pos-cell'>" + "".join(chips) + "</div>"

            rows_html.append(
                "<tr>"
                f"<td><span class='sys-name'>{cfg['name']}</span></td>"
                f"<td><span class='chip chip-market'>{cfg['market']}</span></td>"
                f"<td>{side_chip}</td>"
                f"<td>{position}</td>"
                f"<td><span class='num'>{r['notional']:,.0f} $</span></td>"
                f"<td><span class='num'>{r['notional'] / sz_capital:.2f}x</span></td>"
                "</tr>"
            )

        table_html = (
            "<div class='table-wrap' style='overflow-x:auto'><table class='table-common sizing-table'><thead><tr>"
            "<th>Sistema</th><th>Mercado</th><th>Dirección</th><th>Comprar / vender</th>"
            "<th>Nocional</th><th>Apalanc. efectivo</th>"
            "</tr></thead><tbody>" + "".join(rows_html) + "</tbody></table></div>"
        )
        st.markdown(table_html, unsafe_allow_html=True)

        st.markdown(
            f"<div class='sizing-foot'>{icon('layers', 16)}<span>Si los {len(rows_html)} sistemas estuvieran "
            f"en posición a la vez, el nocional bruto sería <b>{total_notional:,.0f} $</b> "
            f"(<b>{total_notional / sz_capital:.2f}x</b> el capital).</span></div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        st.caption(
            "Herramienta informativa: no constituye recomendación de inversión. "
            "Verifica el tamaño con tu bróker antes de operar."
        )
