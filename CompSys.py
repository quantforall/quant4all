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
.kpi-grid.kpi-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
@media (max-width: 820px) { .kpi-grid.kpi-4 { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
/* 5 columnas (Simulador: 10 tarjetas en 2 filas): tarjetas más estrechas y cifra algo menor */
.kpi-grid.kpi-5 { grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 0.75rem; }
.kpi-grid.kpi-5 .kpi-card { padding: 0.85rem 0.6rem; }
.kpi-grid.kpi-5 .kpi-value { font-size: 1.5rem; }
.kpi-grid.kpi-5 .kpi-label { font-size: 0.68rem; letter-spacing: 0.04em; }
@media (max-width: 1100px) { .kpi-grid.kpi-5 .kpi-value { font-size: 1.3rem; } }
@media (max-width: 820px) { .kpi-grid.kpi-5 { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
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

/* Aire en el borde derecho para que los números no toquen el marco */
.summary-table th:last-child, .summary-table td:last-child,
.tw-tabular th:last-child, .tw-tabular td:last-child { padding-right: 12px; }

/* Menos separación entre las tablas de mejores / peores días → más ancho útil */
[data-testid="stHorizontalBlock"]:has(.tw-tabular) { gap: 0.5rem !important; }

/* La letra de Top/Worst se ajusta al ancho de la tarjeta (con 10 series no caben a tamaño fijo) */
.table-wrap:has(.tw-tabular) { container-type: inline-size; }
.tw-tabular .num { font-size: clamp(0.66rem, 2.75cqi, 0.82rem); }
.tw-tabular td:first-child { font-size: clamp(0.68rem, 2.75cqi, 0.8rem); }
.tw-tabular .tw-date { font-size: clamp(0.56rem, 2.15cqi, 0.64rem); }
.tw-tabular td, .tw-tabular th { padding-left: 3px; padding-right: 3px; }

/* Tablas de métricas (muchas columnas): ancho completo y scroll horizontal si no caben */
.table-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
/* Columnas fijas e iguales (la primera la marca un <colgroup>): auto las repartía según el largo de la cabecera */
.metrics-table { table-layout: fixed; min-width: 980px; }
.metrics-table.narrow { min-width: 620px; }
.metrics-table thead th { white-space: normal; line-height: 1.25; vertical-align: middle; letter-spacing: 0.03em; overflow-wrap: normal; word-break: normal; hyphens: none; }
.metrics-table th, .metrics-table td { padding-left: 8px; padding-right: 8px; }
.metrics-table th:first-child, .metrics-table td:first-child { text-align: left; padding-left: 14px; }
.metrics-table th:last-child, .metrics-table td:last-child { padding-right: 14px; }
.metrics-table tbody tr { height: 46px; }
.metrics-table .na { color: #CBD5E1; }

/* ── Barra de selección actual (bajo el hero) ── */
.sel-bar { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin: -0.35rem 0 1rem 0; }
.sel-bar .sel-period { font-size: 0.8rem; font-weight: 700; color: var(--q-text-2); margin-right: 4px; }
.sel-chip {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 3px 10px; border-radius: 999px; background: var(--q-surface);
    border: 1px solid var(--q-border); font-size: 0.76rem; font-weight: 600; color: var(--q-text-2);
}
.sel-chip i { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.mobile-only { display: none; }

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

/* ── Fichas de sistemas ── */
.sys-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; align-items: stretch; margin-bottom: 1rem; }
.sys-card {
    position: relative; overflow: hidden; display: flex; flex-direction: column;
    background: var(--q-surface); border: 1px solid var(--q-border);
    border-radius: var(--q-radius); box-shadow: var(--q-shadow-1);
    padding: 1.2rem 1.35rem 1.1rem 1.35rem; margin-bottom: 1rem;
}
.sys-card::before {
    content: ""; position: absolute; left: 0; right: 0; top: 0; height: 4px;
    background: linear-gradient(90deg, var(--q-orange), #FDBA74);
}
.sys-grid .sys-card { margin-bottom: 0; }
.sys-card-title { font-size: 1.25rem; font-weight: 800; color: var(--q-navy); letter-spacing: -0.01em; line-height: 1.2; }
.sys-card-sub { font-size: 0.78rem; font-weight: 600; color: var(--q-muted); margin-top: 2px; }
.sys-card-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 0.75rem; }
.sys-bottom { margin-top: auto; }
.sys-real {
    font-size: 0.72rem; font-weight: 700; color: var(--q-pos); background: var(--q-pos-soft);
    border-radius: 999px; padding: 3px 10px; white-space: nowrap;
}
.sys-tagline { color: var(--q-text-2); font-size: 0.92rem; margin: 0.45rem 0 0.8rem 0; line-height: 1.5; }
.sys-bullets { margin: 0 0 0.9rem 0; padding-left: 1.1rem; color: var(--q-text-2); font-size: 0.85rem; line-height: 1.55; }
.sys-bullets li { margin-bottom: 0.2rem; }
.sys-specs { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.5rem; margin-bottom: 0.9rem; }
.sys-card.wide .sys-specs { grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); }
.sys-spec { background: var(--q-surface-2); border: 1px solid var(--q-border-soft); border-radius: var(--q-radius-sm); padding: 0.45rem 0.65rem; }
.sys-spec .k { font-size: 0.66rem; font-weight: 700; color: var(--q-muted); text-transform: uppercase; letter-spacing: 0.06em; }
.sys-spec .v { font-size: 0.85rem; font-weight: 700; color: var(--q-text); margin-top: 1px; }
.sys-stats { display: flex; flex-wrap: wrap; gap: 0.5rem 1.25rem; padding-top: 0.75rem; border-top: 1px solid var(--q-border-soft); font-size: 0.82rem; color: var(--q-muted); }
.sys-stats b { color: var(--q-text); font-variant-numeric: tabular-nums; }
.sys-subs { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 0.5rem; margin-bottom: 0.9rem; }
.sys-sub { border: 1px solid var(--q-border-soft); border-radius: var(--q-radius-sm); padding: 0.5rem 0.65rem; font-size: 0.8rem; color: var(--q-text-2); line-height: 1.4; }
.sys-sub b { color: var(--q-text); }
.cta-band {
    display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;
    background: linear-gradient(120deg, var(--q-navy) 0%, var(--q-navy-2) 100%);
    border-radius: var(--q-radius); padding: 1.1rem 1.4rem; margin: 0.5rem 0 1rem 0; box-shadow: var(--q-shadow-2);
}
.cta-band .cta-text { color: #E2E8F0; font-size: 0.95rem; line-height: 1.45; max-width: 62ch; }
.cta-band .cta-text b { color: #FFFFFF; }

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

    /* En móvil la barra lateral está plegada: avisar de dónde están los controles */
    .mobile-only {
        display: block; font-size: 0.8rem; color: var(--q-text-2);
        background: var(--q-orange-soft); border: 1px solid #FED7AA;
        border-radius: var(--q-radius-sm); padding: 0.55rem 0.8rem; margin-bottom: 0.9rem;
    }
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
# Estado inicial desde la URL (enlaces compartibles)
# -----------------------
SYSTEM_CHOICES = ["", "ROCStar", "All Stars", "TAA", "ST x1", "ST x1.25"]
DEFAULT_SYSTEMS = ["All Stars", "ROCStar", "TAA", "ST x1.25", ""]


def _read_url_state() -> dict:
    """Lee la selección de la URL. Solo se usa en la primera carga de la sesión: después mandan los widgets
    (si los valores por defecto cambiaran en cada rerun, Streamlit reiniciaría los widgets)."""
    qp = st.query_params
    state = {"capital": 25000, "tickers": [""] * 5, "systems": list(DEFAULT_SYSTEMS),
             "bench_on": True, "bench": "^GSPC", "start": None, "end": None}
    try:
        if "cap" in qp:
            state["capital"] = max(1000, int(float(qp["cap"])))
        if "tk" in qp:
            tks = [t.strip().upper() for t in qp["tk"].split(",") if t.strip()][:5]
            state["tickers"] = tks + [""] * (5 - len(tks))
        if "sys" in qp:
            sy = [s for s in qp["sys"].split(",") if s and s in SYSTEM_CHOICES][:5]
            state["systems"] = sy + [""] * (5 - len(sy))
        if "bench" in qp:
            state["bench"] = qp["bench"].strip().upper()
        if "b" in qp:
            state["bench_on"] = qp["b"] != "0"
        if "from" in qp:
            state["start"] = datetime.strptime(qp["from"], "%Y-%m-%d").date()
        if "to" in qp:
            state["end"] = datetime.strptime(qp["to"], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        pass
    return state


if "url_state" not in st.session_state:
    st.session_state["url_state"] = _read_url_state()
URL0 = st.session_state["url_state"]

# -----------------------
# Idioma (ES por defecto; EN con ?lang=en o con el selector de banderas)
# -----------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "en" if st.query_params.get("lang") == "en" else "es"


def tx(es: str, en: str) -> str:
    """Texto en el idioma activo."""
    return en if st.session_state.get("lang") == "en" else es


def _set_lang(lang: str) -> None:
    st.session_state["lang"] = lang


_FLAG_ES = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 750 500'%3E"
            "%3Crect width='750' height='500' fill='%23c60b1e'/%3E%3Crect width='750' height='250' y='125' "
            "fill='%23ffc400'/%3E%3C/svg%3E")
_FLAG_GB = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 30'%3E"
            "%3CclipPath id='t'%3E%3Cpath d='M30,15h30v15zv15h-30zh-30v-15zv-15h30z'/%3E%3C/clipPath%3E"
            "%3Cpath d='M0,0v30h60v-30z' fill='%23012169'/%3E"
            "%3Cpath d='M0,0L60,30M60,0L0,30' stroke='%23fff' stroke-width='6'/%3E"
            "%3Cpath d='M0,0L60,30M60,0L0,30' clip-path='url(%23t)' stroke='%23C8102E' stroke-width='4'/%3E"
            "%3Cpath d='M30,0v30M0,15h60' stroke='%23fff' stroke-width='10'/%3E"
            "%3Cpath d='M30,0v30M0,15h60' stroke='%23C8102E' stroke-width='6'/%3E%3C/svg%3E")
st.markdown(f"""
<style>
.st-key-lang_switch {{ display: flex; flex-direction: row; justify-content: flex-end; gap: 6px; margin: -1.4rem 0 0.4rem 0; }}
.st-key-lang_switch > div {{ width: auto !important; flex: 0 0 auto; }}
.st-key-lang_es button, .st-key-lang_en button {{
    min-height: 0; padding: 4px 10px 4px 8px; border-radius: 999px; font-size: 0.78rem; font-weight: 700;
}}
.st-key-lang_es button::before, .st-key-lang_en button::before {{
    content: ""; display: inline-block; width: 22px; height: 15px; margin-right: 6px; border-radius: 3px;
    background-size: cover; background-position: center; box-shadow: 0 0 0 1px rgba(15,23,42,0.15);
}}
.st-key-lang_es button::before {{ background-image: url("{_FLAG_ES}"); }}
.st-key-lang_en button::before {{ background-image: url("{_FLAG_GB}"); }}
@media (max-width: 820px) {{ .st-key-lang_switch {{ margin-top: 0; }} }}
</style>
""", unsafe_allow_html=True)

with st.container(key="lang_switch", horizontal=True, horizontal_alignment="right"):
    _active = st.session_state["lang"]
    st.button("ES", key="lang_es", type="primary" if _active == "es" else "secondary",
              on_click=_set_lang, args=("es",), help="Español")
    st.button("EN", key="lang_en", type="primary" if _active == "en" else "secondary",
              on_click=_set_lang, args=("en",), help="English")

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
            {icon("mail", 16, 2.2)} {tx("Suscríbete gratis", "Subscribe free")}
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(tx("**Capital inicial ($)**", "**Initial capital ($)**"))
    initial_capital = st.number_input(
        "", min_value=1000, value=URL0["capital"], step=500, label_visibility="collapsed"
    )

    st.markdown(tx("**Inicio | Fin**", "**Start | End**"))
    dates_container = st.container()
    range_slider_container = st.container()

    st.markdown("")

    col_assets, col_systems = st.columns(2)
    with col_assets:
        st.markdown("**Tickers (Yahoo)**")
        tickers = []
        for i in range(5):
            v = st.text_input(
                "", value=URL0["tickers"][i], placeholder=f"Ticker {i+1}", label_visibility="collapsed"
            )
            if v.strip():
                tickers.append(v.strip())
        show_benchmark = st.checkbox("Benchmark", value=URL0["bench_on"])
        benchmark = st.text_input("Benchmark", value=URL0["bench"], label_visibility="collapsed")

    with col_systems:
        st.markdown("**Quant4all**")
        systems = []
        for i in range(5):
            choice = st.selectbox(
                f"sys{i}",
                SYSTEM_CHOICES,
                index=SYSTEM_CHOICES.index(URL0["systems"][i]),
                label_visibility="collapsed",
            )
            if choice:
                systems.append(choice)
        st.caption(tx("ST = sistemas Short-term (corto plazo) · x1 / x1.25 = apalancamiento",
                      "ST = Short-term systems · x1 / x1.25 = leverage"))

    st.caption(tx("🔗 La dirección del navegador guarda esta selección: cópiala para compartir la comparación.",
                   "🔗 The browser address keeps this selection: copy it to share the comparison."))



# -----------------------
# Helpers
# -----------------------
# La primera serie (normalmente un sistema Quant4all) va en el naranja de marca; el resto, tonos bien separados
PALETTE = ["#F7931E", "#2563EB", "#0891B2", "#7C3AED", "#16A34A", "#E11D48",
           "#0F766E", "#BE185D", "#65A30D", "#78350F"]
BENCH_COLOR = "#9ca3af"
PORTFOLIO_COLOR = "#F7931E"
POS_COLOR, NEG_COLOR, MID_COLOR = "#16a34a", "#dc2626", "#d97706"
MONTHS_ES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
MONTHS_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
TRADING_DAYS = 252


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


def compute_equity_and_dd_from_returns(ret: pd.Series, initial_capital: float) -> pd.DataFrame:
    df = pd.DataFrame(index=ret.index)
    df["ret"] = ret.astype(float).fillna(0.0)
    df["equity"] = float(initial_capital) * (1 + df["ret"]).cumprod()
    # El capital inicial cuenta como primer máximo: una pérdida el primer día ya es drawdown
    df["peak"] = df["equity"].cummax().clip(lower=float(initial_capital))
    df["dd"] = df["equity"] / df["peak"] - 1.0
    return df


def compute_equity_and_dd_from_close(close: pd.Series, initial_capital: float) -> pd.DataFrame:
    return compute_equity_and_dd_from_returns(close.astype(float).pct_change(), initial_capital)


def daily_returns_from_close(close: pd.Series) -> pd.Series:
    if close.empty:
        return pd.Series(dtype=float, name=close.name)
    rets = close.pct_change().dropna()
    rets.name = close.name
    return rets


def drawdown_episodes(dd: pd.Series) -> pd.DataFrame:
    """Un episodio por cada caída desde un máximo: inicio (máximo previo), valle, recuperación y duraciones."""
    cols = ["start", "trough", "end", "depth", "days", "days_to_trough", "days_to_recover"]
    dd = dd.dropna()
    if dd.empty or dd.min() >= 0:
        return pd.DataFrame(columns=cols)
    gid = (dd >= 0).cumsum()                      # cada nuevo máximo abre un grupo
    grp = dd.groupby(gid)
    eps = pd.DataFrame({
        "start": dd.index.to_series().groupby(gid).first(),
        "trough": grp.idxmin(),
        "depth": grp.min(),
    })
    eps["end"] = eps["start"].shift(-1)           # el día del siguiente máximo = recuperación
    eps = eps[eps["depth"] < 0].copy()
    eps["days"] = (eps["end"].fillna(dd.index[-1]) - eps["start"]).dt.days
    eps["days_to_trough"] = (eps["trough"] - eps["start"]).dt.days
    eps["days_to_recover"] = (eps["end"] - eps["trough"]).dt.days
    return eps[cols].reset_index(drop=True)


def perf_metrics(df: pd.DataFrame, rf_annual=0.0, always_invested: bool = False) -> dict:
    """Métricas de una serie de equity (df con columnas ret / equity / dd).
    rf_annual: tipo anual en tanto por uno, fijo (float) o variable en el tiempo (Series)."""
    ret = df["ret"]
    if isinstance(rf_annual, pd.Series):
        rf_annual = rf_annual.reindex(ret.index).ffill().bfill().fillna(0.0)
    total = float((1 + ret).prod())
    years = (df.index[-1] - df.index[0]).days / 365.25 if len(df) > 1 else 0.0
    cagr = total ** (1 / years) - 1 if years > 0 else np.nan
    vol = float(ret.std(ddof=1) * np.sqrt(TRADING_DAYS)) if len(ret) > 1 else np.nan
    rf_d = (1 + rf_annual) ** (1 / TRADING_DAYS) - 1
    excess = ret - rf_d
    ann_excess = float(excess.mean() * TRADING_DAYS)
    downside = float(np.sqrt((np.minimum(excess, 0) ** 2).mean()) * np.sqrt(TRADING_DAYS))
    max_dd = float(df["dd"].min())
    yearly = (1 + ret).groupby(ret.index.year).prod() - 1
    eps = drawdown_episodes(df["dd"])
    return {
        "total": total,
        "cagr": cagr,
        "vol": vol,
        "sharpe": ann_excess / vol if vol > 0 else np.nan,
        "sortino": ann_excess / downside if downside > 0 else np.nan,
        "max_dd": max_dd,
        "calmar": cagr / abs(max_dd) if max_dd < 0 else np.nan,
        "worst_year": float(yearly.min()) if not yearly.empty else np.nan,
        "worst_year_label": int(yearly.idxmin()) if not yearly.empty else None,
        "max_dd_days": int(eps["days"].max()) if not eps.empty else 0,
        "in_market": 1.0 if always_invested else float((ret != 0).mean()),
    }


def relative_metrics(ret: pd.Series, bench: pd.Series) -> dict:
    """Beta, alpha anual (rf = 0), correlación y up/down capture (mensual) frente al benchmark."""
    df = pd.concat([ret.rename("r"), bench.rename("b")], axis=1, join="inner").dropna()
    if len(df) < 20:
        return dict(beta=np.nan, alpha=np.nan, corr=np.nan, up=np.nan, down=np.nan)
    r, b = df["r"], df["b"]
    var_b = b.var(ddof=1)
    beta = r.cov(b) / var_b if var_b > 0 else np.nan
    alpha = (r.mean() - beta * b.mean()) * TRADING_DAYS
    m = (1 + df).resample("ME").prod() - 1
    up_m, down_m = m["b"] > 0, m["b"] < 0
    up = m.loc[up_m, "r"].mean() / m.loc[up_m, "b"].mean() if up_m.any() else np.nan
    down = m.loc[down_m, "r"].mean() / m.loc[down_m, "b"].mean() if down_m.any() else np.nan
    return dict(beta=beta, alpha=alpha, corr=r.corr(b), up=up, down=down)


def simulate_portfolio(df_daily: pd.DataFrame, weights: dict, w_cash: float, cash_rate_d,
                       rebal_months: int, capital: float) -> pd.Series:
    """Equity diaria de la cartera. Entre rebalanceos cada componente deriva (buy & hold) con su
    rentabilidad; al cierre del último día hábil de cada N meses se vuelve a los pesos objetivo.
    cash_rate_d: retorno diario del cash, fijo (float) o por fecha (Series alineada con df_daily)."""
    rebal_dates = pd.DatetimeIndex([])
    if rebal_months > 0:
        month_ends = df_daily.index.to_series().groupby(df_daily.index.to_period("M")).last()
        rebal_dates = pd.DatetimeIndex(month_ends.iloc[rebal_months - 1::rebal_months])

    growth = 1 + df_daily
    growth["__cash__"] = 1 + cash_rate_d
    w = pd.Series({**weights, "__cash__": w_cash})[growth.columns]

    # Tramo = días entre rebalanceos; el día siguiente a un rebalanceo empieza tramo nuevo
    is_reb = df_daily.index.isin(rebal_dates)
    seg = np.concatenate([[0], np.cumsum(is_reb[:-1])])

    parts, level = [], float(capital)
    for _, g in growth.groupby(seg):
        v = g.cumprod().mul(w, axis=1).sum(axis=1) * level
        parts.append(v)
        level = float(v.iloc[-1])
    return pd.concat(parts)


@st.cache_data(ttl=6 * 3600, show_spinner=False)
def load_tbill_rate() -> pd.Series:
    """Rentabilidad anual de las letras del Tesoro a 13 semanas (^IRX), en tanto por uno."""
    s = download_prices("^IRX")
    return s / 100.0 if not s.empty else s


# Caídas relevantes del S&P 500 (cierre del máximo previo → cierre del mínimo)
CRISIS_PERIODS = [
    ("LTCM / Rusia", "LTCM / Russia", "1998-07-17", "1998-08-31"),
    ("Burbuja puntocom", "Dot-com bubble", "2000-03-24", "2002-10-09"),
    ("11-S", "9/11", "2001-09-10", "2001-09-21"),
    ("Crisis financiera", "Financial crisis", "2007-10-09", "2009-03-09"),
    ("Flash crash 2010", "2010 flash crash", "2010-04-23", "2010-07-02"),
    ("Deuda EE.UU. 2011", "2011 US debt crisis", "2011-04-29", "2011-10-03"),
    ("Corrección 2015–16", "2015–16 correction", "2015-05-21", "2016-02-11"),
    ("Volmageddon", "Volmageddon", "2018-01-26", "2018-02-08"),
    ("4º trimestre 2018", "Q4 2018", "2018-09-20", "2018-12-24"),
    ("COVID-19", "COVID-19", "2020-02-19", "2020-03-23"),
    ("Bajista 2022", "2022 bear market", "2022-01-03", "2022-10-12"),
    ("Aranceles 2025", "2025 tariffs", "2025-02-19", "2025-04-08"),
]


def period_stats(daily_ret: pd.Series, start: str, end: str):
    """(retorno, peor drawdown) de una serie de retornos diarios entre dos cierres; None si no los cubre."""
    s = daily_ret.dropna()
    t0, t1 = pd.Timestamp(start), pd.Timestamp(end)
    if s.empty or s.index[0] > t0 + pd.Timedelta(days=5) or s.index[-1] < t1:
        return None
    p = s[(s.index > t0) & (s.index <= t1)]
    if p.empty:
        return None
    eq = (1 + p).cumprod()
    return float(eq.iloc[-1] - 1), float((eq / np.maximum(eq.cummax(), 1.0) - 1).min())


@st.cache_data(show_spinner=False, max_entries=16)
def monte_carlo(rets: np.ndarray, horizon: int, n_sims: int = 1000, block: int = 21, seed: int = 42) -> dict:
    """Bootstrap por bloques de los retornos diarios (los bloques de ~1 mes conservan rachas y
    agrupación de volatilidad). Devuelve CAGR, Max DD y percentiles de la equity (base 1)."""
    rng = np.random.default_rng(seed)
    block = min(block, len(rets))
    n_blocks = -(-horizon // block)
    starts = rng.integers(0, len(rets) - block + 1, size=(n_sims, n_blocks))
    idx = (starts[:, :, None] + np.arange(block)).reshape(n_sims, -1)[:, :horizon]
    eq = np.cumprod(1 + rets[idx], axis=1)
    peak = np.maximum(np.maximum.accumulate(eq, axis=1), 1.0)
    return {
        "cagr": eq[:, -1] ** (TRADING_DAYS / horizon) - 1,
        "max_dd": (eq / peak - 1).min(axis=1),
        "bands": np.percentile(eq, [5, 25, 50, 75, 95], axis=0),
    }


def _project_simplex(v: np.ndarray) -> np.ndarray:
    """Proyección euclídea sobre {w ≥ 0, Σw = 1} (Duchi et al., 2008)."""
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, len(v) + 1) > (css - 1))[0][-1]
    return np.maximum(v - (css[rho] - 1) / (rho + 1), 0)


@st.cache_data(show_spinner=False, max_entries=16)
def optimize_weights(df_daily: pd.DataFrame) -> dict:
    """Pesos (solo largos, suman 1) para cuatro criterios, estimados con los retornos del periodo."""
    R = df_daily.values
    n = R.shape[1]
    if n == 1:
        return {k: np.ones(1) for k in ("Equiponderado", "Risk parity", "Mínima varianza", "Máximo Sharpe")}
    mu = R.mean(axis=0) * TRADING_DAYS
    cov = np.cov(R, rowvar=False) * TRADING_DAYS
    out = {"Equiponderado": np.full(n, 1 / n)}

    # Risk parity (igual contribución al riesgo): iteración de punto fijo
    w = 1 / np.sqrt(np.diag(cov))
    w /= w.sum()
    for _ in range(500):
        rc = w * (cov @ w)
        w = w * np.sqrt(rc.mean() / np.maximum(rc, 1e-18))
        w /= w.sum()
    out["Risk parity"] = w

    # Mínima varianza: descenso de gradiente proyectado (paso 1/L garantiza convergencia)
    step = 1 / (2 * np.linalg.eigvalsh(cov).max())
    w = np.full(n, 1 / n)
    for _ in range(3000):
        w = _project_simplex(w - step * 2 * cov @ w)
    out["Mínima varianza"] = w

    # Máximo Sharpe (rf = 0): búsqueda aleatoria + ascenso de gradiente proyectado
    def sharpe(x):
        v = np.sqrt(x @ cov @ x)
        return (x @ mu) / v if v > 0 else -np.inf

    rng = np.random.default_rng(0)
    cands = np.vstack([rng.dirichlet(np.ones(n), 20000), np.eye(n), np.full((1, n), 1 / n)])
    vols = np.sqrt(np.einsum("ij,jk,ik->i", cands, cov, cands))
    w = cands[np.argmax((cands @ mu) / vols)]
    best, lr = sharpe(w), 0.05
    for _ in range(2000):
        v = np.sqrt(w @ cov @ w)
        g = mu / v - (w @ mu) * (cov @ w) / v ** 3
        w_new = _project_simplex(w + lr * g / (np.linalg.norm(g) + 1e-12))
        s_new = sharpe(w_new)
        if s_new > best:
            w, best = w_new, s_new
        else:
            lr *= 0.7
            if lr < 1e-7:
                break
    out["Máximo Sharpe"] = w
    return out


def to_int_percent(weights: np.ndarray, total: int) -> list:
    """Reparte `total` puntos enteros proporcionalmente a `weights` (método del mayor resto)."""
    raw = np.asarray(weights, dtype=float)
    raw = raw / raw.sum() * total if raw.sum() > 0 else np.zeros_like(raw)
    floors = np.floor(raw).astype(int)
    for i in np.argsort(-(raw - floors))[: total - floors.sum()]:
        floors[i] += 1
    return floors.tolist()

SYSTEM_FILES = {
    "ROCStar":   "data/ROCStar.csv",
    "All Stars": "data/AllStars.csv",
    "Big Three": "data/BigThree.csv",
    "TAA":       "data/TAA.csv",
    "ST x1":    "data/Short-term_x1.csv",
    "ST x1.25": "data/Short-term_x1.25.csv",
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
    margin=dict(l=8, r=8, t=40, b=8),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(showgrid=False, zeroline=False, showline=True, automargin=True,
               linecolor="#E2E8F0", tickfont=dict(size=11, color="#64748B")),
    yaxis=dict(showgrid=True, gridcolor="#EEF2F7", zeroline=False, automargin=True,
               showline=False, tickfont=dict(size=11, color="#64748B"), side="right"),
)


def _apply_layout(fig, title="", height=360):
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text=title, font=dict(size=14, color="#111827")), height=height)
    return fig


def _hex_to_rgba(color: str, alpha: float) -> str:
    h = color.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{alpha})"


def plot_equity(eq_map, labels, series_color, bench_key=None, unit="$", scale="Lin"):
    fig = go.Figure()
    use_log = (unit == "$" and scale == "Log")
    for label in labels:
        df = eq_map[label]
        y = df["equity"] if unit == "$" else (df["equity"] / df["equity"].iloc[0] - 1.0) * 100.0
        is_bench = label == bench_key
        fig.add_trace(go.Scatter(
            x=df.index, y=y, mode="lines", name=label,
            line=dict(color=series_color[label], width=2 if is_bench else 2.5, dash="dot" if is_bench else None),
            hovertemplate=f"<b>{label}</b><br>%{{x|%d %b %Y}}<br>{'$%{y:,.0f}' if unit == '$' else '%{y:.2f}%'}<extra></extra>",
        ))
    _apply_layout(fig, tx("Curva de capital", "Equity curve") + (" (%)" if unit == "%" else ""), height=360)
    fig.update_yaxes(
        side="right",
        type="log" if use_log else "linear",
        ticksuffix=" %" if unit == "%" else "",
        tickformat=".1f" if unit == "%" else ("$,.0f" if not use_log else "$~s"),
    )
    return fig


def plot_dd(eq_map, labels, series_color, bench_key=None):
    fig = go.Figure()
    for label in labels:
        df = eq_map[label]
        color = series_color[label]
        is_bench = label == bench_key
        fig.add_trace(go.Scatter(
            x=df.index, y=df["dd"] * 100, mode="lines", name=label,
            line=dict(color=color, width=2, dash="dot" if is_bench else None),
            fill=None if is_bench else "tozeroy",
            fillcolor=None if is_bench else _hex_to_rgba(color, 0.10),
            hovertemplate=f"<b>{label}</b><br>%{{x|%d %b %Y}}<br>%{{y:.2f}}%<extra></extra>",
        ))
    _apply_layout(fig, "Drawdown (%)", height=280)
    # La leyenda ya está en la curva de capital (mismos colores): aquí sobra
    fig.update_layout(showlegend=False)
    fig.update_yaxes(ticksuffix=" %", side="right")
    return fig


# -----------------------
# Tablas HTML
# -----------------------
NA_CELL = "<td><span class='na'>—</span></td>"


def _cell(v, text_fn, color_fn=None) -> str:
    if v is None or pd.isna(v):
        return NA_CELL
    color = color_fn(v) if color_fn else None
    style = f" style='color:{color}'" if color else ""
    return f"<td><span class='num'{style}>{text_fn(v)}</span></td>"


def _sign_color(v):
    return POS_COLOR if v >= 0 else NEG_COLOR


def _ratio_color(v):
    return POS_COLOR if v >= 1 else (MID_COLOR if v > 0 else NEG_COLOR)


def series_label_html(label: str, series_color: dict) -> str:
    return f"<span style='color:{series_color.get(label, '#111827')}; font-weight:700'>{label}</span>"


def _colgroup(n_cols: int, first_pct: float) -> str:
    """Primera columna con ancho propio y el resto a partes iguales (para table-layout: fixed)."""
    rest = (100 - first_pct) / (n_cols - 1)
    return (f"<colgroup><col style='width:{first_pct}%'>"
            + f"<col style='width:{rest:.3f}%'>" * (n_cols - 1) + "</colgroup>")


def render_metrics_table(rows, title: str = "") -> str:
    """rows: lista de (label_html, dict de perf_metrics o None)."""
    heads = [tx("Serie", "Series"), tx("Retorno", "Return"), "CAGR", tx("Volatilidad", "Volatility"), "Max DD", "Sharpe", "Sortino",
             "Calmar", tx("Peor año", "Worst year"), tx("Días en DD (máx.)", "Max days in DD"), tx("En mercado", "In market")]
    html = [f'<div class="table-wrap"><div class="table-title">{icon("target", 16)} {title or tx("Métricas clave", "Key metrics")}</div>',
            '<div class="table-scroll"><table class="table-common metrics-table">' + _colgroup(len(heads), 11) + '<thead><tr>']
    html += [f"<th>{h}</th>" for h in heads]
    html.append("</tr></thead><tbody>")
    for label_html, m in rows:
        tr = f"<tr><td>{label_html}</td>"
        if m is None:
            tr += NA_CELL * (len(heads) - 1)
        else:
            tr += _cell(m["total"], lambda v: f"{v:.1f}x", lambda v: POS_COLOR if v >= 1 else NEG_COLOR)
            tr += _cell(m["cagr"], lambda v: f"{v * 100:.1f}%", _sign_color)
            tr += _cell(m["vol"], lambda v: f"{v * 100:.1f}%")
            tr += _cell(m["max_dd"], lambda v: f"{v * 100:.1f}%", lambda v: NEG_COLOR)
            tr += _cell(m["sharpe"], lambda v: f"{v:.2f}", _ratio_color)
            tr += _cell(m["sortino"], lambda v: f"{v:.2f}", _ratio_color)
            tr += _cell(m["calmar"], lambda v: f"{v:.2f}", _ratio_color)
            if pd.isna(m["worst_year"]):
                tr += NA_CELL
            else:
                tr += (f"<td><span class='num' style='color:{_sign_color(m['worst_year'])}'>"
                       f"{m['worst_year'] * 100:+.1f}%</span><span class='tw-date'>{m['worst_year_label']}</span></td>")
            tr += _cell(m["max_dd_days"], lambda v: f"{v:,.0f}")
            tr += _cell(m["in_market"], lambda v: f"{v * 100:.0f}%")
        html.append(tr + "</tr>")
    html.append("</tbody></table></div></div>")
    return "".join(html)


def render_relative_table(rows, bench_label: str) -> str:
    """rows: lista de (label_html, dict de relative_metrics)."""
    heads = [tx("Serie", "Series"), "Beta", tx("Alpha anual", "Annual alpha"), tx("Correlación", "Correlation"),
             tx("Captura alcista", "Upside capture"), tx("Captura bajista", "Downside capture")]
    html = [f'<div class="table-wrap"><div class="table-title">{icon("layers", 16)} {tx("Frente a", "Versus")} {bench_label}</div>',
            '<div class="table-scroll"><table class="table-common metrics-table narrow">'
            + _colgroup(len(heads), 15) + '<thead><tr>']
    html += [f"<th>{h}</th>" for h in heads]
    html.append("</tr></thead><tbody>")
    for label_html, m in rows:
        tr = f"<tr><td>{label_html}</td>"
        tr += _cell(m["beta"], lambda v: f"{v:.2f}")
        tr += _cell(m["alpha"], lambda v: f"{v * 100:+.1f}%", _sign_color)
        tr += _cell(m["corr"], lambda v: f"{v:.2f}")
        tr += _cell(m["up"], lambda v: f"{v * 100:.0f}%", lambda v: POS_COLOR if v >= 1 else None)
        tr += _cell(m["down"], lambda v: f"{v * 100:.0f}%", lambda v: POS_COLOR if v < 1 else NEG_COLOR)
        html.append(tr + "</tr>")
    html.append("</tbody></table></div></div>")
    return "".join(html)


def render_drawdowns_table(eps: pd.DataFrame, k: int = 5, sort_by: str = "depth") -> str:
    """Los k drawdowns más profundos (sort_by="depth") o más largos (sort_by="days", incluye el abierto)."""
    heads = ["#", tx("Inicio", "Start"), tx("Valle", "Trough"), tx("Recuperación", "Recovery"), tx("Profundidad", "Depth"),
             tx("Días de caída", "Days to trough"), tx("Días de recuperación", "Days to recover"), tx("Duración total", "Total length")]
    html = [f'<div class="table-wrap"><div class="table-title">{icon("trending-down", 16)} {tx(f"Los {k} drawdowns más largos", f"The {k} longest drawdowns") if sort_by == "days" else tx(f"Los {k} peores drawdowns", f"The {k} worst drawdowns")}</div>',
            '<div class="table-scroll"><table class="table-common metrics-table narrow">'
            + _colgroup(len(heads), 6) + '<thead><tr>']
    html += [f"<th>{h}</th>" for h in heads]
    html.append("</tr></thead><tbody>")
    top = eps.nlargest(k, "days") if sort_by == "days" else eps.nsmallest(k, "depth")
    for i, ep in enumerate(top.itertuples(), start=1):
        ongoing = pd.isna(ep.end)
        tr = f"<tr><td><span class='num'>{i}</span></td>"
        tr += f"<td>{ep.start:%d/%m/%Y}</td><td>{ep.trough:%d/%m/%Y}</td>"
        tr += (f"<td><span class='chip chip-short'>{tx('En curso', 'Ongoing')}</span></td>" if ongoing
               else f"<td>{ep.end:%d/%m/%Y}</td>")
        tr += _cell(ep.depth, lambda v: f"{v * 100:.1f}%", lambda v: NEG_COLOR)
        tr += _cell(ep.days_to_trough, lambda v: f"{v:,.0f} d")
        tr += NA_CELL if ongoing else _cell(ep.days_to_recover, lambda v: f"{v:,.0f} d")
        tr += _cell(ep.days, lambda v: f"{v:,.0f} d" + ("+" if ongoing else ""))
        html.append(tr + "</tr>")
    html.append("</tbody></table></div></div>")
    return "".join(html)


def render_crisis_table(full_daily: dict, labels: list, series_color: dict):
    """Filas = crisis; columnas = series. Retorno del periodo y, debajo, su peor drawdown.
    Devuelve (html, nº de crisis con datos)."""
    rows = []
    for name_es, name_en, start, end in CRISIS_PERIODS:
        name = tx(name_es, name_en)
        stats = {l: period_stats(full_daily[l], start, end) for l in labels}
        if all(v is None for v in stats.values()):
            continue
        d0, d1 = pd.Timestamp(start), pd.Timestamp(end)
        tr = (f"<tr><td><span class='sys-name' style='font-size:0.82rem'>{name}</span>"
              f"<span class='tw-date'>{d0:%d/%m/%y} → {d1:%d/%m/%y}</span></td>")
        for l in labels:
            v = stats[l]
            if v is None:
                tr += NA_CELL
            else:
                ret, dd = v
                tr += (f"<td><span class='num' style='color:{_sign_color(ret)}'>{ret * 100:+.1f}%</span>"
                       f"<span class='tw-date'>DD {dd * 100:.1f}%</span></td>")
        rows.append(tr + "</tr>")
    heads = [tx("Periodo", "Period")] + [series_label_html(l, series_color) for l in labels]
    html = (f'<div class="table-wrap"><div class="table-title">{icon("trending-down", 16)} '
            f'{tx("Comportamiento en las grandes caídas del S&P 500", "Behaviour in the big S&P 500 sell-offs")}</div>'
            f'<div class="table-scroll"><table class="table-common metrics-table narrow" '
            f'style="min-width:{180 + 95 * len(labels)}px">'
            + _colgroup(len(heads), 22 if len(labels) <= 4 else 16) + "<thead><tr>"
            + "".join(f"<th>{h}</th>" for h in heads) + "</tr></thead><tbody>"
            + "".join(rows) + "</tbody></table></div></div>")
    return html, len(rows)


def render_top_table(title: str, icon_name: str, table_dict: dict, series_color: dict):
    html = [f'<div class="table-wrap"><div class="table-title">{icon(icon_name, 16)} {title}</div>']
    html.append('<table class="table-common tw-tabular"><thead><tr>')
    html.append(f"<th>{tx('Serie', 'Series')}</th>")
    for k in range(1, 6):
        html.append(f"<th># {k}</th>")
    html.append("</tr></thead><tbody>")
    for label, items in table_dict.items():
        row = f"<tr><td>{series_label_html(label, series_color)}</td>"
        for d, r in items:
            if pd.isna(r) or d is None:
                row += "<td><span class='na' style='color:#d1d5db'>—</span></td>"
            else:
                sign = "+" if r >= 0 else ""
                row += (
                    "<td>"
                    f"<span class='num' style='color:{_sign_color(r)}'>{sign}{r*100:.1f}%</span>"
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


def monthly_heat_html(daily_ret: pd.Series) -> str:
    """Tabla año × mes a partir de retornos DIARIOS (el primer mes incluye desde el primer cierre)."""
    m_ret = ((1 + daily_ret.dropna()).resample("ME").prod() - 1) * 100
    df_m = m_ret.to_frame("ret")
    df_m["Year"] = df_m.index.year
    df_m["Month"] = df_m.index.month
    pivot = df_m.pivot(index="Year", columns="Month", values="ret").sort_index()
    yret = ((1.0 + pivot / 100.0).prod(axis=1) - 1.0) * 100.0
    avg_row = pivot.mean(axis=0)
    avg_y = yret.mean()

    def td(v, cls):
        if pd.isna(v):
            return f"<td class='{cls} na'>—</td>"
        return f"<td class='{cls}' style='{bg_color(v)}'><span class='cell'>{v:+.1f}%</span></td>"

    html = ["<div class='monthly-heat-wrap'><table class='monthly-heat'>",
            f"<thead><tr><th class='year-col'>{tx('Año', 'Year')}</th>"]
    html += [f"<th class='mon-col'>{m}</th>" for m in (MONTHS_EN if tx("es", "en") == "en" else MONTHS_ES)]
    html.append(f"<th class='ytd-col'>{tx('Año %', 'Year %')}</th></tr></thead><tbody>")
    for yr in pivot.index:
        html.append(f"<tr><td class='year-col'>{yr}</td>")
        html += [td(pivot.loc[yr].get(m, np.nan), "mon-col") for m in range(1, 13)]
        html.append(td(yret.get(yr, np.nan), "ytd-col") + "</tr>")
    html.append(f"</tbody><tfoot><tr><td class='year-col'>{tx('Media', 'Avg')}</td>")
    html += [td(avg_row.get(m, np.nan), "mon-col") for m in range(1, 13)]
    html.append(td(avg_y, "ytd-col") + "</tr></tfoot></table></div>")
    return "".join(html)


def corr_heatmap_figure(corr_df, labels_order, series_color):
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


def series_picker(label: str, options: list, default=None, format_func=str) -> str:
    """Selector en botones (sin key: si cambian las opciones, vuelve al valor por defecto).
    Las opciones son identificadores estables; format_func da el texto visible (idioma)."""
    default = default if default in options else options[0]
    choice = st.segmented_control(label, options, default=default, format_func=format_func,
                                  label_visibility="collapsed")
    return choice if choice in options else default


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

bench_label = benchmark.strip().upper()
# Si el benchmark coincide con un ticker introducido, se distingue para no pisar la serie
bench_key = bench_label if bench_label not in dict_closes else f"{bench_label} (bench)"
close_bench = None
if show_benchmark and bench_label:
    s = download_prices(bench_label)
    close_bench = s if not s.empty else None

if errors:
    with st.sidebar:
        for msg in errors:
            st.warning(msg)

if not dict_closes and not dict_system_rets and close_bench is None:
    st.info(tx("Introduce al menos un **ticker** o un **sistema** válido.", "Enter at least one valid **ticker** or **system**."))
    st.stop()

# -----------------------
# Common date range (benchmark excluded from intersection)
# -----------------------
series_ranges = (
    [(s.index.min(), s.index.max()) for s in dict_closes.values()]
    + [(s.index.min(), s.index.max()) for s in dict_system_rets.values()]
)

if not series_ranges:
    st.error(tx("No hay datos válidos para las series seleccionadas.", "There is no valid data for the selected series."))
    st.stop()

global_start = max(s for s, _ in series_ranges)
global_end   = min(e for _, e in series_ranges)

if global_end < global_start:
    st.error(tx("No hay **rango temporal común** entre los activos/sistemas seleccionados.",
                "The selected assets/systems have **no common date range**."))
    st.stop()

# -----------------------
# Sidebar date pickers + slider (state management)
# -----------------------
if "start_valid" not in st.session_state:
    st.session_state["start_valid"] = URL0["start"] or global_start.date()
if "end_valid" not in st.session_state:
    st.session_state["end_valid"] = URL0["end"] or global_end.date()
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

# Reflejar la selección en la URL para poder compartirla
_url_now = {
    "sys": ",".join(systems),
    "tk": ",".join(t.upper() for t in tickers),
    "bench": benchmark.strip().upper(),
    "b": "1" if show_benchmark else "0",
    "cap": str(int(initial_capital)),
    "from": f"{current_start:%Y-%m-%d}",
    "to": f"{current_end:%Y-%m-%d}",
    "lang": "en" if st.session_state["lang"] == "en" else "",
}
_url_now = {k: v for k, v in _url_now.items() if v or k == "sys"}   # sys vacío = ningún sistema
if dict(st.query_params) != _url_now:
    st.query_params.from_dict(_url_now)

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
has_bench = df_bench is not None and not df_bench.empty

# -----------------------
# Orden único en toda la app: Sistemas → Tickers → Benchmark
# -----------------------
ordered_labels = [s for s in systems if s in dict_equities]
ordered_labels += [t.upper() for t in tickers if t.upper() in dict_equities and t.upper() not in ordered_labels]
eq_map = {label: dict_equities[label] for label in ordered_labels}
if has_bench:
    ordered_labels.append(bench_key)
    eq_map[bench_key] = df_bench

SERIES_COLOR: dict[str, str] = {}
for i, label in enumerate(l for l in ordered_labels if l != bench_key):
    SERIES_COLOR[label] = PALETTE[i % len(PALETTE)]
if has_bench:
    SERIES_COLOR[bench_key] = BENCH_COLOR

# Retornos diarios (correlación, histogramas, Top 5, tabla mensual, métricas vs benchmark)
daily_map: dict[str, pd.Series] = {}
for label in ordered_labels:
    if label in dict_system_rets:
        r = dict_system_rets[label].loc[current_start:current_end].dropna()
    elif label == bench_key:
        r = daily_returns_from_close(close_bench.loc[current_start:current_end])
    else:
        r = daily_returns_from_close(dict_closes[label].loc[current_start:current_end])
    if not r.empty:
        daily_map[label] = r

# Historia completa de cada serie (stress test por crisis: no depende del rango de fechas elegido)
full_daily: dict[str, pd.Series] = {}
for label in ordered_labels:
    if label in dict_system_rets:
        full_daily[label] = dict_system_rets[label].dropna()
    elif label == bench_key:
        full_daily[label] = daily_returns_from_close(close_bench)
    else:
        full_daily[label] = daily_returns_from_close(dict_closes[label])


# ======================================================
# ==================  MAIN LAYOUT  =====================
# ======================================================

# ---- Hero (outside tabs) ----
st.markdown(f"""
<div class='hero'>
  <div class='hero-eyebrow'>Quant4all · Systematic Trading</div>
  <div class='hero-title'>Let's compare <span class='hero-sub'>by Quant4all</span></div>
  <div class='hero-desc'>{tx("Compara sistemas y activos, simula carteras y calcula el tamaño de posición "
                             "de los sistemas de corto plazo.",
                             "Compare systems and assets, simulate portfolios and size the positions "
                             "of the short-term systems.")}</div>
</div>
""", unsafe_allow_html=True)

# ---- Selección actual (visible también en móvil, donde la barra lateral está plegada) ----
sel_chips = "".join(
    f"<span class='sel-chip'><i style='background:{SERIES_COLOR[l]}'></i>{l}</span>" for l in ordered_labels
)
st.markdown(
    f"<div class='mobile-only'>☰ "
    + tx("Abre el menú lateral (arriba a la izquierda) para elegir sistemas, tickers, capital y fechas.",
         "Open the side menu (top left) to choose systems, tickers, capital and dates.")
    + "</div>"
    f"<div class='sel-bar'><span class='sel-period'>{icon('calendar', 14)} "
    f"{current_start:%d/%m/%Y} → {current_end:%d/%m/%Y}</span>{sel_chips}</div>",
    unsafe_allow_html=True,
)

# ---- Métricas por serie ----
metrics_map = {
    label: perf_metrics(eq_map[label], always_invested=label not in dict_system_rets)
    for label in ordered_labels
}

def _to_csv(df: pd.DataFrame, index: bool = True) -> bytes:
    """CSV listo para Excel: en español ';' y coma decimal; en inglés ',' y punto. BOM para los acentos."""
    sep, dec = (",", ".") if tx("es", "en") == "en" else (";", ",")
    return df.to_csv(sep=sep, decimal=dec, index=index, float_format="%.6f").encode("utf-8-sig")


def metrics_csv() -> bytes:
    rows = []
    for l in ordered_labels:
        m = metrics_map[l]
        rows.append({
            tx("Serie", "Series"): l, tx("Desde", "From"): f"{current_start:%Y-%m-%d}",
            tx("Hasta", "To"): f"{current_end:%Y-%m-%d}",
            tx("Retorno (x)", "Return (x)"): m["total"], "CAGR %": m["cagr"] * 100,
            tx("Volatilidad %", "Volatility %"): m["vol"] * 100,
            "Max DD %": m["max_dd"] * 100, "Sharpe": m["sharpe"], "Sortino": m["sortino"], "Calmar": m["calmar"],
            tx("Peor año %", "Worst year %"): m["worst_year"] * 100, tx("Peor año", "Worst year"): m["worst_year_label"],
            tx("Días en DD (máx.)", "Max days in DD"): m["max_dd_days"], tx("En mercado %", "In market %"): m["in_market"] * 100,
        })
    return _to_csv(pd.DataFrame(rows), index=False)


def curves_csv() -> bytes:
    eq = pd.concat({f"{l} · {tx('capital', 'equity')}": eq_map[l]["equity"] for l in ordered_labels}, axis=1)
    dd = pd.concat({f"{l} · drawdown %": eq_map[l]["dd"] * 100 for l in ordered_labels}, axis=1)
    out = pd.concat([eq, dd], axis=1).sort_index()
    out.index = out.index.strftime("%Y-%m-%d")
    out.index.name = tx("Fecha", "Date")
    return _to_csv(out)


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
    dict(name="BlackMonday", market="RUT", side="Corto", tipo=3, vol_pct=0.0, risk=None,     lev=lambda L: max(2.0, L + 0.25)),
    dict(name="ADST",        market="RUT", side="Corto", tipo=2, vol_pct=1.2, risk="carver", lev=lambda L: min(1.0, L - 0.25)),
    dict(name="GLD",         market="GLD", side="Largo", tipo=5, vol_pct=0.0, risk="carver", lev=lambda L: 0.0),
]
SIZING_TICKERS = {"SPX": "^GSPC", "RUT": "^RUT", "GLD": "GLD"}
MICRO_SYMBOL = {"SPX": "MES", "RUT": "M2K"}
NANO_SYMBOL = {"SPX": "NES", "RUT": "N2K"}
# Margen orientativo de 1 e-micro (editable en la app: cada bróker fija el suyo)
DEFAULT_MICRO_MARGIN = {"SPX": 2500, "RUT": 1200}


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
# Cada pestaña es un fragmento: tocar un control dentro de una pestaña solo recalcula esa pestaña
tab_compare, tab_simulator, tab_sizing, tab_systems = st.tabs(
    [":material/insights: " + tx("Comparador", "Comparator"),
     ":material/account_balance_wallet: " + tx("Simulador de Cartera", "Portfolio Simulator"),
     ":material/calculate: " + tx("Calculadora de Posición", "Position Sizing"),
     ":material/menu_book: " + tx("Sistemas", "Systems")]
)


# =============================================
# TAB 1 — Comparador
# =============================================
@st.fragment
def render_comparador():

    # Section 1 — Resumen
    section_header(tx("Resumen de rendimiento", "Performance summary"), "award")

    metric_rows = [(series_label_html(l, SERIES_COLOR), metrics_map.get(l)) for l in ordered_labels]
    st.markdown(render_metrics_table(metric_rows), unsafe_allow_html=True)
    st.caption(
        tx("Sharpe y Sortino con tipo libre de riesgo 0 % · Calmar = CAGR / |Max DD| · "
           "Días en DD (máx.) = el periodo más largo (días naturales) por debajo del máximo anterior · "
           "En mercado = % de sesiones con retorno distinto de 0 (tickers y benchmark cuentan como siempre invertidos).",
           "Sharpe and Sortino with a 0% risk-free rate · Calmar = CAGR / |Max DD| · "
           "Max days in DD = longest stretch (calendar days) below the previous peak · "
           "In market = % of sessions with a non-zero return (tickers and benchmark count as always invested).")
    )
    st.download_button(
        tx("Descargar métricas (CSV)", "Download metrics (CSV)"), data=metrics_csv(),
        file_name=f"quant4all_{tx('metricas', 'metrics')}_{current_end:%Y%m%d}.csv",
        mime="text/csv", icon=":material/download:", key="dl_metrics", on_click="ignore",
    )

    c2, c3 = st.columns(2, gap="small")
    with c2:
        st.markdown(render_top_table(tx("Mejores días", "Best days"), "trending-up", top_dict, SERIES_COLOR), unsafe_allow_html=True)
    with c3:
        st.markdown(render_top_table(tx("Peores días", "Worst days"), "trending-down", worst_dict, SERIES_COLOR), unsafe_allow_html=True)

    st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)

    # Section 2 — Equity & Drawdown
    c_title, c_ctrl = st.columns([0.75, 0.25])
    with c_title:
        section_header(tx("Curva de capital y drawdown", "Equity curve and drawdown"), "trending-up")
    with c_ctrl:
        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        col_u, col_s = st.columns(2)
        with col_u:
            unit_choice = st.radio("Unidad", options=["$", "%"], index=0, horizontal=True, label_visibility="collapsed")
        with col_s:
            scale_choice = st.radio("Escala", options=["Lin", "Log"], index=1, horizontal=True, label_visibility="collapsed")

    st.plotly_chart(
        plot_equity(eq_map, ordered_labels, SERIES_COLOR, bench_key=bench_key, unit=unit_choice, scale=scale_choice),
        use_container_width=True, config={"displayModeBar": False},
    )
    st.plotly_chart(
        plot_dd(eq_map, ordered_labels, SERIES_COLOR, bench_key=bench_key),
        use_container_width=True, config={"displayModeBar": False},
    )
    st.download_button(
        tx("Descargar curvas de capital y drawdown (CSV)", "Download equity and drawdown curves (CSV)"),
        data=curves_csv(), file_name=f"quant4all_{tx('curvas', 'curves')}_{current_start:%Y%m%d}_{current_end:%Y%m%d}.csv",
        mime="text/csv", icon=":material/download:", key="dl_curves", on_click="ignore",
    )

    # Section 3 — Peores drawdowns
    st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)
    section_header(tx("Peores drawdowns", "Worst drawdowns"), "trending-down")
    dd_label = series_picker("Serie (drawdowns)", ordered_labels)
    dc1, dc2 = st.columns(2)
    with dc1:
        dd_sort_names = {"depth": tx("Más profundos", "Deepest"), "days": tx("Más largos", "Longest")}
        dd_sort = series_picker("Orden (drawdowns)", list(dd_sort_names), format_func=dd_sort_names.get)
    with dc2:
        dd_scope_names = {"range": tx("Periodo seleccionado", "Selected period"),
                          "full": tx("Histórico completo", "Full history")}
        dd_scope = series_picker("Periodo (drawdowns)", list(dd_scope_names), format_func=dd_scope_names.get)
    if dd_scope == "full":
        # Toda la historia de la serie, sin recortar al rango común de fechas
        dd_series = compute_equity_and_dd_from_returns(full_daily[dd_label], float(initial_capital))["dd"]
    else:
        dd_series = eq_map[dd_label]["dd"]
    eps = drawdown_episodes(dd_series)
    if eps.empty:
        st.info(tx("Esta serie no tiene drawdowns en el periodo elegido.", "This series has no drawdowns in the chosen period."))
    else:
        st.markdown(render_drawdowns_table(eps, sort_by=dd_sort), unsafe_allow_html=True)
        span = f"{dd_series.index[0]:%d/%m/%Y} → {dd_series.index[-1]:%d/%m/%Y}"
        st.caption(tx(f"Datos: {span}. Inicio = máximo previo · Valle = punto más bajo · Recuperación = primer día "
                      "en que se supera el máximo previo. Duraciones en días naturales; un drawdown aún abierto "
                      "se cuenta hasta el último dato (marcado con +).",
                      f"Data: {span}. Start = previous peak · Trough = lowest point · Recovery = first day above "
                      "the previous peak. Lengths in calendar days; an open drawdown is counted up to the last "
                      "data point (marked with +)."))

    # Section 4 — Frente al benchmark
    rel_labels = [l for l in ordered_labels if l != bench_key and l in daily_map]
    if has_bench and bench_key in daily_map and rel_labels:
        st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)
        section_header(tx(f"Frente al benchmark ({bench_label})", f"Versus the benchmark ({bench_label})"), "layers")
        rel_rows = [(series_label_html(l, SERIES_COLOR), relative_metrics(daily_map[l], daily_map[bench_key]))
                    for l in rel_labels]
        st.markdown(render_relative_table(rel_rows, bench_label), unsafe_allow_html=True)
        st.caption(
            tx("Beta y alpha sobre retornos diarios (alpha anualizada, tipo libre de riesgo 0 %). "
               "Captura alcista / bajista = retorno medio de la serie en los meses en que el benchmark sube / baja, "
               "en % del retorno del benchmark: lo ideal es alcista alta y bajista baja (o negativa).",
               "Beta and alpha on daily returns (annualised alpha, 0% risk-free rate). "
               "Upside / downside capture = the series' average return in months when the benchmark rises / falls, "
               "as a % of the benchmark's return: ideally high upside and low (or negative) downside.")
        )

    # Section 5 — Métricas rolling
    st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)
    section_header(tx("Métricas rolling", "Rolling metrics"), "trending-up")
    roll_names = {"ret": tx("Rentabilidad", "Return"), "sharpe": "Sharpe", "vol": tx("Volatilidad", "Volatility"),
                  "corr": tx(f"Correlación con {bench_label}", f"Correlation with {bench_label}")}
    roll_kinds = ["ret", "sharpe", "vol"]
    if has_bench and bench_key in daily_map and rel_labels:
        roll_kinds.append("corr")
    rc1, rc2 = st.columns([0.6, 0.4])
    with rc1:
        roll_kind = series_picker("Métrica rolling", roll_kinds, format_func=roll_names.get)
    with rc2:
        roll_windows = {126: tx("6 meses", "6 months"), 252: tx("1 año", "1 year"), 756: tx("3 años", "3 years")}
        win = series_picker("Ventana rolling", list(roll_windows), default=252, format_func=roll_windows.get)

    fig_roll = go.Figure()
    is_corr = roll_kind == "corr"
    roll_labels = rel_labels if is_corr else [l for l in ordered_labels if l in daily_map]
    for l in roll_labels:
        r = daily_map[l]
        if roll_kind == "ret":
            y = np.expm1(np.log1p(r).rolling(win).sum()) * 100
        elif roll_kind == "sharpe":
            y = r.rolling(win).mean() / r.rolling(win).std() * np.sqrt(TRADING_DAYS)
        elif roll_kind == "vol":
            y = r.rolling(win).std() * np.sqrt(TRADING_DAYS) * 100
        else:
            pair = pd.concat([r.rename("r"), daily_map[bench_key].rename("b")], axis=1, join="inner").dropna()
            y = pair["r"].rolling(win).corr(pair["b"])
        y = y.dropna()
        if y.empty:
            continue
        is_b = l == bench_key
        fig_roll.add_trace(go.Scatter(
            x=y.index, y=y.values, mode="lines", name=l,
            line=dict(color=SERIES_COLOR[l], width=1.6 if is_b else 2, dash="dot" if is_b else None),
            hovertemplate=f"<b>{l}</b><br>%{{x|%d %b %Y}}<br>%{{y:.2f}}"
                          f"{'%' if roll_kind in ('ret', 'vol') else ''}<extra></extra>",
        ))
    if fig_roll.data:
        _apply_layout(fig_roll, f"{roll_names[roll_kind]} — {tx('ventana', 'window')} {roll_windows[win]}", height=360)
        if roll_kind in ("ret", "vol"):
            fig_roll.update_yaxes(ticksuffix=" %")
        if roll_kind != "vol":
            fig_roll.add_hline(y=0, line=dict(color="#94A3B8", width=1))
        st.plotly_chart(fig_roll, use_container_width=True, config={"displayModeBar": False})
        st.caption(
            tx("Cada punto resume la ventana que termina ese día: rentabilidad acumulada, Sharpe anualizado "
               "(rf = 0), volatilidad anualizada o correlación de los retornos diarios con el benchmark. "
               "Sirve para ver si la ventaja de un sistema es estable o depende de una época concreta.",
               "Each point summarises the window ending that day: cumulative return, annualised Sharpe "
               "(rf = 0), annualised volatility or correlation of daily returns with the benchmark. "
               "It shows whether a system's edge is stable or depends on a particular period.")
        )
    else:
        st.info(tx("El periodo seleccionado es más corto que la ventana elegida.", "The selected period is shorter than the chosen window."))

    # Section 6 — Crisis
    st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)
    section_header(tx("Stress test: grandes caídas del mercado", "Stress test: major market sell-offs"), "target")
    crisis_html, n_crisis = render_crisis_table(full_daily, ordered_labels, SERIES_COLOR)
    if n_crisis:
        st.markdown(crisis_html, unsafe_allow_html=True)
        st.caption(
            tx("Retorno de cada serie entre el máximo y el mínimo del S&P 500 en cada episodio, y debajo su peor "
               "drawdown dentro de ese tramo. Usa todo el histórico disponible de cada serie (no depende del rango "
               "de fechas elegido); «—» = la serie no tiene datos para ese periodo.",
               "Return of each series between the S&P 500 peak and trough of each episode, with its worst "
               "drawdown within that stretch below. Uses each series' full history (independent of the selected "
               "date range); “—” = no data for that period.")
        )
    else:
        st.info(tx("Ninguna de las series seleccionadas tiene datos en los periodos de crisis analizados.", "None of the selected series has data for the crisis periods analysed."))

    # Section 7 — Matriz de correlación
    st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)
    section_header(tx("Matriz de correlación", "Correlation matrix"), "grid")
    corr_labels = list(daily_map.keys())
    if len(corr_labels) >= 2:
        ddf = pd.concat(list(daily_map.values()), axis=1)
        ddf.columns = corr_labels
        corr_df = ddf.corr(method="pearson", min_periods=3).reindex(index=corr_labels, columns=corr_labels)
        st.plotly_chart(
            corr_heatmap_figure(corr_df, corr_labels, SERIES_COLOR),
            use_container_width=True, config={"displayModeBar": False},
        )
        st.caption(tx("Correlación de Pearson de los retornos diarios en el periodo seleccionado.", "Pearson correlation of daily returns over the selected period."))
    else:
        st.info(tx("Añade al menos **dos** series con datos en el periodo para ver la correlación.", "Add at least **two** series with data in the period to see the correlation."))

    st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)

    # Section 8 — Distribución de retornos diarios
    section_header(tx("Distribución de retornos diarios", "Distribution of daily returns"), "bar-chart")

    labels_all = [l for l in ordered_labels if l in daily_map]
    if not labels_all:
        st.info(tx("No hay series disponibles para el periodo seleccionado.", "No series available for the selected period."))
    else:
        selected_label = series_picker("Serie (distribución)", labels_all)

        vals = daily_map[selected_label].dropna() * 100.0
        if vals.empty:
            st.info(tx("No hay datos de retornos diarios para la serie seleccionada.", "No daily return data for the selected series."))
        else:
            mu = float(vals.mean())
            sigma = float(vals.std(ddof=1)) if len(vals) > 1 else 0.0
            skew_val = float(vals.skew()) if len(vals) > 2 else 0.0
            kurt_val = float(vals.kurtosis()) if len(vals) > 3 else 0.0

            col_plot, col_side = st.columns([0.75, 0.25], gap="large")

            hist_fig = go.Figure()
            series_col = SERIES_COLOR.get(selected_label, PALETTE[0])
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
            for k, lbl in zip((1, 2, 3), ("1σ", "2σ", "3σ")):
                for sign, prefix in ((1, "+"), (-1, "−")):
                    hist_fig.add_annotation(
                        x=mu + sign * k * sigma, y=1.06, xref="x", yref="paper",
                        text=f"{prefix}{lbl}", showarrow=False, font=dict(size=10, color="#6b7280"),
                    )
            _apply_layout(hist_fig, "", height=460)
            hist_fig.update_layout(
                xaxis_title=tx("Retorno diario (%)", "Daily return (%)"),
                yaxis=dict(title=tx("Frecuencia", "Frequency"), side="left", showgrid=True,
                           gridcolor="#f3f4f6", tickfont=dict(size=11)),
                bargap=0.02, showlegend=False,
            )

            with col_plot:
                st.plotly_chart(hist_fig, use_container_width=True, config={"displayModeBar": False})

            with col_side:
                st.markdown(f"""
                <div class='stats-card'>
                    <div class='stats-title'>{tx('Estadísticas', 'Statistics')}</div>
                    <div class='stats-row'>
                        <span class='stat-label'>{tx('Media', 'Mean')} (μ)</span>
                        <span class='stat-val'>{mu:+.3f}%</span>
                    </div>
                    <div class='stats-row'>
                        <span class='stat-label'>{tx('Desv. típica', 'Std dev')} (σ)</span>
                        <span class='stat-val'>{sigma:.3f}%</span>
                    </div>
                    <div class='stats-row'>
                        <span class='stat-label'>{tx('Asimetría', 'Skewness')}</span>
                        <span class='stat-val'>{skew_val:+.3f}</span>
                    </div>
                    <div class='stats-row'>
                        <span class='stat-label'>{tx('Curtosis (exceso)', 'Excess kurtosis')}</span>
                        <span class='stat-val'>{kurt_val:+.3f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

                _, th_col, _ = st.columns([0.15, 0.7, 0.15])
                with th_col:
                    st.markdown("<div style='text-align:center; font-size:0.82rem; font-weight:700; color:#6b7280; text-transform:uppercase; letter-spacing:.05em; margin-bottom:4px;'>" + tx("Umbral (%)", "Threshold (%)") + "</div>", unsafe_allow_html=True)
                    threshold_pct = st.number_input(
                        "Umbral", min_value=0.0, max_value=100.0, value=5.0,
                        step=0.5, format="%.1f", label_visibility="collapsed",
                    )

                thr = float(threshold_pct)
                pos_days = int((vals >= +thr).sum())
                neg_days = int((vals <= -thr).sum())

                st.markdown("<div style='text-align:center; font-size:0.82rem; font-weight:700; color:#6b7280; text-transform:uppercase; letter-spacing:.05em; margin-bottom:6px; margin-top:1rem;'>" + tx("Días más allá del umbral", "Days beyond threshold") + "</div>", unsafe_allow_html=True)

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

    # Section 9 — Rentabilidades mensuales
    section_header(tx("Rentabilidades mensuales", "Monthly returns"), "calendar")
    if not labels_all:
        st.info(tx("Añade al menos un ticker, sistema o benchmark.", "Add at least one ticker, system or benchmark."))
    else:
        monthly_label = series_picker("Serie (mensual)", labels_all)
        st.markdown(monthly_heat_html(daily_map[monthly_label]), unsafe_allow_html=True)


with tab_compare:
    render_comparador()


# =============================================
# TAB 2 — Simulador de Cartera
# =============================================
def _normalize_weights(keys: list) -> None:
    """Reescala los sliders para que sumen 100 manteniendo sus proporciones."""
    vals = [float(st.session_state.get(k, 0)) for k in keys]
    if sum(vals) <= 0:
        return
    for k, v in zip(keys, to_int_percent(np.array(vals), 100)):
        st.session_state[k] = v


def _apply_optimized(keys: list, weights: list, cash_key: str) -> None:
    """Pone en los sliders los pesos del optimizador; el Cash se respeta y el resto se reparte."""
    risky = 100 - int(st.session_state.get(cash_key, 0))
    for k, v in zip(keys, to_int_percent(np.array(weights), risky)):
        st.session_state[k] = v


def _kpi_html(label: str, value: str, color: str = "#111827", foot: str = "") -> str:
    foot_html = f"<div class='kpi-foot'>{foot}</div>" if foot else ""
    return (f"<div class='kpi-card'><div class='kpi-label'>{label}</div>"
            f"<div class='kpi-value' style='color:{color};'>{value}</div>{foot_html}</div>")


def _ratio_fmt(v):
    return ("—", "#111827") if pd.isna(v) else (f"{v:.2f}", _ratio_color(v))


@st.fragment
def render_simulador():
    # Series disponibles: sistemas + tickers (sin benchmark, sin cash), en el orden global
    series_list = [l for l in ordered_labels if l != bench_key and l in daily_map]
    if not series_list:
        st.info(tx("Añade al menos un **ticker** o **sistema** en la barra lateral para usar el simulador.",
                   "Add at least one **ticker** or **system** in the sidebar to use the simulator."))
        return

    # Alinear todas las series al índice común
    df_daily = pd.concat([daily_map[k] for k in series_list], axis=1).dropna()
    df_daily.columns = series_list
    if df_daily.empty:
        st.info(tx("No hay datos en el rango seleccionado para simular.", "No data in the selected range to simulate."))
        return
    n_series = len(series_list)
    capital = float(initial_capital)

    # ---- Controles: pesos + rebalanceo + cash ----
    section_header(tx("Pesos de la cartera", "Portfolio weights"), "pie-chart")

    # Pesos por defecto: distribución equitativa entre series (sin cash), suma = 100
    base_w = 100 // n_series
    remainder_w = 100 - base_w * n_series
    w_keys = {k: f"sim_w_{k}" for k in series_list}
    for i, k in enumerate(series_list):
        if w_keys[k] not in st.session_state:
            st.session_state[w_keys[k]] = base_w + (remainder_w if i == 0 else 0)
    if "sim_w_cash" not in st.session_state:
        st.session_state["sim_w_cash"] = 0

    slider_items = [(k, SERIES_COLOR[k], w_keys[k]) for k in series_list] + [("Cash", BENCH_COLOR, "sim_w_cash")]

    # Máximo 4 sliders por fila, repartidos de forma equilibrada (6 → 3+3).
    # Todas las filas usan el mismo nº de columnas para que los sliders midan lo mismo.
    n_rows = -(-len(slider_items) // 4)
    cols_per_row = -(-len(slider_items) // n_rows)
    for row_start in range(0, len(slider_items), cols_per_row):
        cols = st.columns(cols_per_row)
        for col, (name, color, wkey) in zip(cols, slider_items[row_start:row_start + cols_per_row]):
            with col:
                st.markdown(
                    f"<div style='color:{color}; font-weight:700; font-size:0.85rem; margin-bottom:2px;'>{name}</div>",
                    unsafe_allow_html=True,
                )
                st.slider(f"Peso {name}", 0, 100, step=1, label_visibility="collapsed", key=wkey)

    raw_weights = {k: st.session_state[w_keys[k]] for k in series_list}
    w_cash_pct = st.session_state["sim_w_cash"]
    total_w = sum(raw_weights.values()) + w_cash_pct

    # Barra visual de pesos
    if total_w > 0:
        segs = [(SERIES_COLOR[k], w) for k, w in raw_weights.items()] + [(BENCH_COLOR, w_cash_pct)]
        bar_segs = "".join(
            f"<div style='width:{w / total_w * 100:.1f}%; background:{c}; height:100%;'></div>"
            for c, w in segs if w > 0
        )
        st.markdown(f"""
        <div style='display:flex; height:10px; border-radius:5px; overflow:hidden;
                    gap:2px; margin:0.5rem 0 0.25rem 0;'>{bar_segs}</div>
        """, unsafe_allow_html=True)

    # Indicador suma + botón para cuadrar al 100 %
    c_sum, c_fix = st.columns([0.7, 0.3], vertical_alignment="center")
    with c_sum:
        sum_color = POS_COLOR if total_w == 100 else NEG_COLOR
        st.markdown(
            f"<div style='font-size:0.82rem; font-weight:700; color:{sum_color};'>"
            + tx("Suma de pesos", "Sum of weights") + f": {total_w}% "
            + ("✓" if total_w == 100 else tx("— deben sumar 100%", "— must add up to 100%")) + "</div>",
            unsafe_allow_html=True,
        )
    with c_fix:
        if total_w != 100 and total_w > 0:
            st.button(
                tx("Ajustar a 100 %", "Scale to 100%"), key="sim_fix100", icon=":material/balance:", width="stretch",
                on_click=_normalize_weights, args=(list(w_keys.values()) + ["sim_w_cash"],),
                help=tx("Reescala los pesos actuales manteniendo sus proporciones.",
                        "Rescales the current weights keeping their proportions."),
            )

    # ---- Rebalanceo + Cash rate ----
    ctrl1, ctrl2, ctrl3 = st.columns([0.25, 0.35, 0.4])
    with ctrl1:
        rebal_names = {1: tx("Mensual", "Monthly"), 3: tx("Trimestral", "Quarterly"), 6: tx("Semestral", "Semi-annual"),
                       12: tx("Anual", "Annual"), 0: tx("Sin rebalanceo", "No rebalancing")}
        rebal_months = st.selectbox(tx("Rebalanceo", "Rebalancing"), list(rebal_names), index=3,
                                    format_func=rebal_names.get, key="sim_rebal")
    with ctrl2:
        cash_names = {"tbill": "T-bills (^IRX)", "fixed": tx("Tipo fijo", "Fixed rate")}
        cash_mode = st.radio(tx("Remuneración del cash", "Cash yield"), list(cash_names), horizontal=True,
                             format_func=cash_names.get, key="sim_cash_mode",
                             help=tx("T-bills: rentabilidad histórica de las letras del Tesoro de EE. UU. a 3 meses, "
                                     "día a día. Tipo fijo: el mismo tipo anual en todo el periodo.",
                                     "T-bills: historical yield of 3-month US Treasury bills, day by day. "
                                     "Fixed rate: the same annual rate over the whole period."))
    with ctrl3:
        fixed_rate = st.number_input(tx("Tipo fijo (% anual)", "Fixed rate (% p.a.)"), min_value=0.0, max_value=10.0,
                                     value=2.0, step=0.25, format="%.2f", disabled=cash_mode != "fixed",
                                     key="sim_fixed_rate")

    # ---- Optimizador de pesos (con el rebalanceo elegido) ----
    if n_series >= 2:
        with st.expander(tx("Optimizador de pesos", "Weight optimiser"), icon=":material/tune:"):
            opt = optimize_weights(df_daily)
            opt_names = {"Equiponderado": tx("Equiponderado", "Equal weight"), "Risk parity": "Risk parity",
                         "Mínima varianza": tx("Mínima varianza", "Minimum variance"),
                         "Máximo Sharpe": tx("Máximo Sharpe", "Maximum Sharpe")}
            heads = [tx("Método", "Method")] + [series_label_html(k, SERIES_COLOR) for k in series_list] + \
                    ["CAGR", tx("Volatilidad", "Volatility"), "Max DD", "Sharpe"]
            rows = []
            for method, w in opt.items():
                # Trayectoria real con esos pesos (sin cash) y el rebalanceo elegido
                eq_w = simulate_portfolio(df_daily, dict(zip(series_list, w)), 0.0, 0.0, rebal_months, 1.0)
                r_w = eq_w.pct_change().fillna(eq_w.iloc[0] - 1)
                m_w = perf_metrics(compute_equity_and_dd_from_returns(r_w, 1.0))
                row = f"<tr><td><span class='sys-name' style='font-size:0.82rem'>{opt_names[method]}</span></td>"
                row += "".join(f"<td><span class='num'>{p}%</span></td>" for p in to_int_percent(w, 100))
                row += _cell(m_w["cagr"], lambda v: f"{v * 100:.1f}%", _sign_color)
                row += _cell(m_w["vol"], lambda v: f"{v * 100:.1f}%")
                row += _cell(m_w["max_dd"], lambda v: f"{v * 100:.1f}%", lambda v: NEG_COLOR)
                row += _cell(m_w["sharpe"], lambda v: f"{v:.2f}", _ratio_color)
                rows.append(row + "</tr>")
            st.markdown(
                f"<div class='table-wrap'><div class='table-scroll'><table class='table-common metrics-table narrow' "
                f"style='min-width:{160 + 80 * (n_series + 4)}px'>"
                + _colgroup(len(heads), 16) + "<thead><tr>" + "".join(f"<th>{h}</th>" for h in heads)
                + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div></div>",
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            bcols = st.columns(len(opt))
            for bcol, (method, w) in zip(bcols, opt.items()):
                bcol.button(
                    tx(f"Aplicar {opt_names[method].lower()}", f"Apply {opt_names[method].lower()}"),
                    key=f"opt_{method}", width="stretch",
                    on_click=_apply_optimized, args=(list(w_keys.values()), list(w), "sim_w_cash"),
                )
            st.caption(
                tx("Pesos estimados con los retornos diarios del periodo seleccionado (solo largos). "
                   "**Risk parity**: cada activo aporta el mismo riesgo · **Mínima varianza**: la combinación "
                   "menos volátil · **Máximo Sharpe**: mejor rentabilidad por unidad de riesgo (rf = 0). "
                   f"CAGR, volatilidad, Max DD y Sharpe salen de simular esos pesos sin cash "
                   f"(rebalanceo: {rebal_names[rebal_months].lower()}). Al aplicar, el peso del Cash se mantiene y "
                   "el resto se reparte entre los activos. Ojo: son óptimos a posteriori; con otros datos los pesos "
                   "óptimos serían otros.",
                   "Weights estimated from the daily returns of the selected period (long only). "
                   "**Risk parity**: every asset contributes the same risk · **Minimum variance**: the least "
                   "volatile mix · **Maximum Sharpe**: best return per unit of risk (rf = 0). "
                   f"CAGR, volatility, Max DD and Sharpe come from simulating those weights without cash "
                   f"(rebalancing: {rebal_names[rebal_months].lower()}). When applied, the Cash weight is kept and "
                   "the rest is split among the assets. Note: they are optimal in hindsight; with other data the "
                   "optimal weights would differ.")
            )

    if total_w != 100:
        st.warning(tx("Ajusta los pesos para que sumen exactamente 100% (o pulsa **Ajustar a 100 %**).",
                      "Adjust the weights so they add up to exactly 100% (or press **Scale to 100%**)."))
        return

    # Tipo del cash: serie diaria de T-bills (con el tipo fijo como respaldo si no hay datos)
    rf_annual = fixed_rate / 100.0
    rf_label = tx(f"tipo fijo del {fixed_rate:.2f} %", f"a fixed {fixed_rate:.2f}% rate")
    if cash_mode == "tbill":
        tb = load_tbill_rate()
        if tb.empty:
            st.warning(tx(f"No se ha podido descargar ^IRX: se usa el tipo fijo del {fixed_rate:.2f} %.",
                          f"Could not download ^IRX: using the fixed {fixed_rate:.2f}% rate."))
        else:
            rf_annual = tb.reindex(tb.index.union(df_daily.index)).ffill().reindex(df_daily.index).bfill().clip(lower=0)
            rf_label = tx(f"T-bills a 3 meses (media del periodo {rf_annual.mean() * 100:.2f} %)",
                          f"3-month T-bills (period average {rf_annual.mean() * 100:.2f}%)")
    cash_rate_d = (1 + rf_annual) ** (1 / TRADING_DAYS) - 1

    # ---- Simulación (diaria) ----
    eq_sim = simulate_portfolio(
        df_daily, {k: v / 100.0 for k, v in raw_weights.items()}, w_cash_pct / 100.0,
        cash_rate_d, rebal_months, capital,
    )
    ret_sim = eq_sim.pct_change()
    ret_sim.iloc[0] = eq_sim.iloc[0] / capital - 1
    df_sim = compute_equity_and_dd_from_returns(ret_sim, capital)
    m = perf_metrics(df_sim, rf_annual=rf_annual)

    # VaR / CVaR históricos diarios: sin supuesto de normalidad, recogen las colas reales
    var95 = float(np.percentile(ret_sim, 5)) if len(ret_sim) > 1 else np.nan
    cvar95 = float(ret_sim[ret_sim <= var95].mean()) if len(ret_sim) > 1 else np.nan
    var99 = float(np.percentile(ret_sim, 1)) if len(ret_sim) > 1 else np.nan
    cvar99 = float(ret_sim[ret_sim <= var99].mean()) if len(ret_sim) > 1 else np.nan

    # ---- KPI cards ----
    st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)
    section_header(tx("Resultados", "Results"), "bar-chart")

    # Periodo realmente simulado (intersección común de todas las series)
    st.caption(
        "📅 " + tx(f"Periodo común simulado: **{df_daily.index[0]:%d/%m/%Y} → {df_daily.index[-1]:%d/%m/%Y}** "
                  f"({len(df_daily)} sesiones · {n_series} activo(s)). "
                  "Si una serie empieza más tarde, la simulación se recorta al solape de todas.",
                  f"Common simulated period: **{df_daily.index[0]:%d/%m/%Y} → {df_daily.index[-1]:%d/%m/%Y}** "
                  f"({len(df_daily)} sessions · {n_series} asset(s)). "
                  "If a series starts later, the simulation is trimmed to the overlap of all of them.")
    )

    st.markdown(
        "<div class='kpi-grid kpi-5'>"
        # Fila 1: rentabilidad y ratios · Fila 2: riesgo
        + _kpi_html("CAGR", f"{m['cagr'] * 100:.2f}%", _sign_color(m["cagr"]))
        + _kpi_html(tx("Volatilidad", "Volatility"), f"{m['vol'] * 100:.2f}%")
        + _kpi_html("Sharpe", *_ratio_fmt(m["sharpe"]))
        + _kpi_html("Sortino", *_ratio_fmt(m["sortino"]))
        + _kpi_html("Calmar", *_ratio_fmt(m["calmar"]))
        + _kpi_html("Max Drawdown", f"{m['max_dd'] * 100:.2f}%", NEG_COLOR)
        + _kpi_html(tx("VaR 95% (diario)", "VaR 95% (daily)"), f"{var95 * 100:.2f}%", NEG_COLOR)
        + _kpi_html(tx("CVaR 95% (diario)", "CVaR 95% (daily)"), f"{cvar95 * 100:.2f}%", NEG_COLOR)
        + _kpi_html(tx("VaR 99% (diario)", "VaR 99% (daily)"), f"{var99 * 100:.2f}%", NEG_COLOR)
        + _kpi_html(tx("CVaR 99% (diario)", "CVaR 99% (daily)"), f"{cvar99 * 100:.2f}%", NEG_COLOR)
        + "</div>",
        unsafe_allow_html=True,
    )
    st.caption(
        tx(f"Cash remunerado con {rf_label}; Sharpe y Sortino lo descuentan como tipo libre de riesgo. "
           "Calmar = CAGR / |Max DD|. VaR 95 % / 99 % = pérdida diaria que solo se supera el 5 % / 1 % de las "
           "sesiones; CVaR = pérdida media en ese 5 % / 1 % de peores sesiones.",
           f"Cash earns {rf_label}; Sharpe and Sortino use it as the risk-free rate. "
           "Calmar = CAGR / |Max DD|. VaR 95% / 99% = daily loss exceeded in only 5% / 1% of sessions; "
           "CVaR = average loss in that worst 5% / 1% of sessions.")
    )

    # ---- Cartera frente a sus componentes y el benchmark (mismo periodo) ----
    sim_start, sim_end = df_daily.index[0], df_daily.index[-1]
    comp_eq = {k: compute_equity_and_dd_from_returns(df_daily[k], capital) for k in series_list}
    bench_eq = None
    if has_bench and bench_key in daily_map:
        br = daily_map[bench_key].loc[sim_start:sim_end]
        if not br.empty:
            bench_eq = compute_equity_and_dd_from_returns(br, capital)

    port_name = tx("Cartera", "Portfolio")
    cmp_rows = [(f"<span style='color:{PORTFOLIO_COLOR}; font-weight:800'>{port_name}</span>", m)]
    cmp_rows += [(series_label_html(k, SERIES_COLOR), perf_metrics(comp_eq[k], rf_annual=rf_annual,
                                                                   always_invested=k not in dict_system_rets))
                 for k in series_list]
    if bench_eq is not None:
        cmp_rows.append((series_label_html(bench_key, SERIES_COLOR),
                         perf_metrics(bench_eq, rf_annual=rf_annual, always_invested=True)))
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    st.markdown(render_metrics_table(cmp_rows, title=tx("Cartera frente a sus componentes y el benchmark",
                                                        "Portfolio versus its components and the benchmark")),
                unsafe_allow_html=True)
    st.caption(tx("Mismo periodo y mismo tipo libre de riesgo para todas las filas.",
                  "Same period and same risk-free rate for every row."))

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ---- Gráficos (con el capital inicial como primer punto) ----
    start_pt = sim_start - pd.tseries.offsets.BDay(1)

    def _with_start(s: pd.Series, first: float) -> pd.Series:
        return pd.concat([pd.Series([first], index=[start_pt]), s])

    eq_plot = _with_start(df_sim["equity"], capital)
    dd_plot = _with_start(df_sim["dd"] * 100, 0.0)
    annual_sim = (1 + ret_sim).groupby(ret_sim.index.year).prod() - 1

    show_overlay = st.toggle(tx("Mostrar componentes y benchmark en los gráficos",
                                "Show components and benchmark on the charts"), value=True, key="sim_overlay")

    sim_tab1, sim_tab2, sim_tab3 = st.tabs([":material/show_chart: " + tx("Capital", "Equity"),
                                            ":material/trending_down: Drawdown",
                                            ":material/calendar_month: " + tx("Rentabilidad anual", "Annual return")])

    overlay = []
    if show_overlay:
        overlay = [(k, comp_eq[k], SERIES_COLOR[k], None) for k in series_list]
        if bench_eq is not None:
            overlay.append((bench_key, bench_eq, BENCH_COLOR, "dot"))

    with sim_tab1:
        fig_eq = go.Figure()
        for name, dfe, color, dash in overlay:
            s = _with_start(dfe["equity"], capital)
            fig_eq.add_trace(go.Scatter(
                x=s.index, y=s.values, mode="lines", name=name, opacity=0.75,
                line=dict(color=color, width=1.4, dash=dash),
                hovertemplate=f"<b>{name}</b><br>%{{x|%d %b %Y}}<br>$%{{y:,.0f}}<extra></extra>",
            ))
        fig_eq.add_trace(go.Scatter(
            x=eq_plot.index, y=eq_plot.values, mode="lines", name=port_name,
            line=dict(color=PORTFOLIO_COLOR, width=3),
            fill=None if overlay else "tozeroy", fillcolor=_hex_to_rgba(PORTFOLIO_COLOR, 0.08),
            hovertemplate=f"<b>{port_name}</b><br>%{{x|%d %b %Y}}<br>$%{{y:,.0f}}<extra></extra>",
        ))
        _apply_layout(fig_eq, tx("Curva de capital", "Equity curve"), height=400)
        fig_eq.update_layout(showlegend=bool(overlay))
        fig_eq.update_yaxes(tickformat="$~s" if overlay else "$,.0f", side="right", type="log" if overlay else "linear")
        st.plotly_chart(fig_eq, use_container_width=True, config={"displayModeBar": False})
        if overlay:
            st.caption(tx("Escala logarítmica para comparar series con rentabilidades muy distintas.",
                          "Log scale to compare series with very different returns."))

    with sim_tab2:
        fig_dd2 = go.Figure()
        for name, dfe, color, dash in overlay:
            s = _with_start(dfe["dd"] * 100, 0.0)
            fig_dd2.add_trace(go.Scatter(
                x=s.index, y=s.values, mode="lines", name=name, opacity=0.6,
                line=dict(color=color, width=1.2, dash=dash),
                hovertemplate=f"<b>{name}</b><br>%{{x|%d %b %Y}}<br>%{{y:.2f}}%<extra></extra>",
            ))
        fig_dd2.add_trace(go.Scatter(
            x=dd_plot.index, y=dd_plot.values, mode="lines", name=port_name,
            line=dict(color=PORTFOLIO_COLOR if overlay else "#e11d48", width=2.5),
            fill="tozeroy", fillcolor=_hex_to_rgba(PORTFOLIO_COLOR if overlay else "#e11d48", 0.10),
            hovertemplate=f"<b>{port_name}</b><br>%{{x|%d %b %Y}}<br>%{{y:.2f}}%<extra></extra>",
        ))
        _apply_layout(fig_dd2, "Drawdown (%)", height=400)
        fig_dd2.update_layout(showlegend=bool(overlay))
        fig_dd2.update_yaxes(ticksuffix=" %", side="right")
        st.plotly_chart(fig_dd2, use_container_width=True, config={"displayModeBar": False})

    with sim_tab3:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=annual_sim.index.astype(str),
            y=(annual_sim * 100).round(2),
            name=port_name,
            marker_color=[_sign_color(v) for v in annual_sim.values],
            hovertemplate=f"<b>{port_name}</b><br>%{{x}}<br>%{{y:.2f}}%<extra></extra>",
        ))
        if bench_eq is not None and show_overlay:
            b_annual = (1 + bench_eq["ret"]).groupby(bench_eq.index.year).prod() - 1
            fig_bar.add_trace(go.Scatter(
                x=b_annual.index.astype(str), y=(b_annual * 100).round(2), name=bench_key,
                mode="markers", marker=dict(color="#475569", size=9, symbol="line-ew-open", line=dict(width=3)),
                hovertemplate=f"<b>{bench_key}</b><br>%{{x}}<br>%{{y:.2f}}%<extra></extra>",
            ))
        _apply_layout(fig_bar, tx("Rentabilidad anual (%)", "Annual return (%)"), height=400)
        fig_bar.update_layout(bargap=0.3, showlegend=bench_eq is not None and show_overlay)
        fig_bar.update_yaxes(ticksuffix=" %", side="right")
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        st.caption(tx("El primer y el último año pueden ser parciales (según el periodo seleccionado).",
                      "The first and last years may be partial (depending on the selected period).")
                   + (tx(" La marca gris es el benchmark.", " The grey mark is the benchmark.")
                      if bench_eq is not None and show_overlay else ""))

    sim_csv = pd.DataFrame({tx("Capital", "Equity"): df_sim["equity"],
                            tx("Retorno diario %", "Daily return %"): ret_sim * 100,
                            "Drawdown %": df_sim["dd"] * 100})
    sim_csv.index = sim_csv.index.strftime("%Y-%m-%d")
    sim_csv.index.name = tx("Fecha", "Date")
    st.download_button(
        tx("Descargar la cartera simulada (CSV)", "Download the simulated portfolio (CSV)"), data=_to_csv(sim_csv),
        file_name=f"quant4all_{tx('cartera', 'portfolio')}_{sim_start:%Y%m%d}_{sim_end:%Y%m%d}.csv", mime="text/csv",
        icon=":material/download:", key="dl_sim", on_click="ignore",
    )

    # ---- Monte Carlo ----
    st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)
    section_header(tx("Monte Carlo: ¿qué podría pasar a partir de ahora?", "Monte Carlo: what could happen from here?"),
                   "layers")
    if len(ret_sim) < 252:
        st.info(tx("Hace falta al menos un año de datos para la simulación de Monte Carlo.",
                   "The Monte Carlo simulation needs at least one year of data."))
    else:
        mc1, mc2 = st.columns([0.5, 0.5])
        with mc1:
            horizons = {y: tx(f"{y} año" + ("s" if y > 1 else ""), f"{y} year" + ("s" if y > 1 else ""))
                        for y in (1, 3, 5, 10)}
            h_years = series_picker("Horizonte Monte Carlo", list(horizons), default=5, format_func=horizons.get)
            h_label = horizons[h_years]
        with mc2:
            dd_thr = st.slider(tx("Umbral de drawdown (%)", "Drawdown threshold (%)"), 5, 60, 25, step=5,
                               key="mc_dd_thr",
                               help=tx("Probabilidad de sufrir, en algún momento del horizonte, una caída mayor que esta.",
                                       "Probability of suffering, at some point within the horizon, a fall larger than this."))
        horizon = h_years * TRADING_DAYS
        mc = monte_carlo(ret_sim.values.astype(float), horizon)
        cagr_p = np.percentile(mc["cagr"], [5, 50, 95])
        dd_p = np.percentile(mc["max_dd"], [50, 5])
        p_dd = float((mc["max_dd"] <= -dd_thr / 100).mean())
        p_loss = float((mc["cagr"] < 0).mean())

        st.markdown(
            "<div class='kpi-grid kpi-4'>"
            + _kpi_html(tx("CAGR mediano", "Median CAGR"), f"{cagr_p[1] * 100:.1f}%", _sign_color(cagr_p[1]),
                        tx(f"90 % de escenarios: {cagr_p[0] * 100:.1f}% a {cagr_p[2] * 100:.1f}%",
                           f"90% of scenarios: {cagr_p[0] * 100:.1f}% to {cagr_p[2] * 100:.1f}%"))
            + _kpi_html(tx("Max DD mediano", "Median Max DD"), f"{dd_p[0] * 100:.1f}%", NEG_COLOR,
                        tx(f"5 % peores escenarios: {dd_p[1] * 100:.1f}% o más",
                           f"Worst 5% of scenarios: {dd_p[1] * 100:.1f}% or more"))
            + _kpi_html(tx(f"Prob. de DD &gt; {dd_thr}%", f"Prob. of DD &gt; {dd_thr}%"), f"{p_dd * 100:.0f}%",
                        NEG_COLOR if p_dd >= 0.5 else (MID_COLOR if p_dd >= 0.2 else POS_COLOR),
                        tx(f"en {h_label}", f"within {h_label}"))
            + _kpi_html(tx("Prob. de acabar en pérdidas", "Prob. of ending at a loss"), f"{p_loss * 100:.0f}%",
                        NEG_COLOR if p_loss >= 0.2 else (MID_COLOR if p_loss >= 0.05 else POS_COLOR),
                        tx(f"al cabo de {h_label}", f"after {h_label}"))
            + "</div>",
            unsafe_allow_html=True,
        )

        years_x = np.arange(1, horizon + 1) / TRADING_DAYS
        bands = mc["bands"] * capital
        fig_mc = go.Figure()
        for lo, hi, alpha, name in ((0, 4, 0.12, "5 %–95 %"), (1, 3, 0.25, "25 %–75 %")):
            fig_mc.add_trace(go.Scatter(x=years_x, y=bands[hi], mode="lines", line=dict(width=0),
                                        showlegend=False, hoverinfo="skip"))
            fig_mc.add_trace(go.Scatter(
                x=years_x, y=bands[lo], mode="lines", line=dict(width=0), fill="tonexty",
                fillcolor=_hex_to_rgba(PORTFOLIO_COLOR, alpha), name=tx(f"Escenarios {name}", f"Scenarios {name}"),
                hoverinfo="skip",
            ))
        fig_mc.add_trace(go.Scatter(
            x=years_x, y=bands[2], mode="lines", name=tx("Mediana", "Median"),
            line=dict(color=PORTFOLIO_COLOR, width=2.5),
            hovertemplate=tx("Año", "Year") + " %{x:.1f}<br>" + tx("Mediana", "Median") + ": $%{y:,.0f}<extra></extra>",
        ))
        _apply_layout(fig_mc, tx(f"Capital simulado a {h_label} (1.000 escenarios)",
                                 f"Simulated equity over {h_label} (1,000 scenarios)"), height=380)
        fig_mc.update_xaxes(title=tx("Años", "Years"), ticksuffix="")
        fig_mc.update_yaxes(tickformat="$~s", side="right", type="log")
        st.plotly_chart(fig_mc, use_container_width=True, config={"displayModeBar": False})
        st.caption(
            tx("1.000 trayectorias construidas remuestreando al azar bloques de 21 sesiones (≈ 1 mes) de los retornos "
               "diarios reales de la cartera, lo que conserva rachas y periodos de alta volatilidad. Supone que el "
               "futuro se parece al periodo simulado: es una forma de medir el rango de resultados razonables, "
               "no una predicción.",
               "1,000 paths built by randomly resampling 21-session blocks (≈ 1 month) of the portfolio's real "
               "daily returns, which preserves streaks and high-volatility periods. It assumes the future looks "
               "like the simulated period: a way to gauge the range of reasonable outcomes, not a forecast.")
        )

    # ---- Tabla mensual de la cartera ----
    st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)
    section_header(tx("Rentabilidades mensuales — Cartera", "Monthly returns — Portfolio"), "calendar")
    st.markdown(monthly_heat_html(ret_sim), unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.caption(
        tx("Simulación basada en retornos históricos. El rebalanceo se aplica al final de cada periodo. "
           "Resultados pasados no garantizan rentabilidades futuras.",
           "Simulation based on historical returns. Rebalancing is applied at the end of each period. "
           "Past performance does not guarantee future results.")
    )


with tab_simulator:
    render_simulador()


# =============================================
# TAB 3 — Calculadora de Posición (sistemas de corto plazo)
# =============================================
@st.fragment
def render_calculadora():

    section_header(tx("Tamaño de posición — Sistemas de corto plazo", "Position sizing — Short-term systems"), "calculator")

    today_ny = datetime.now(ZoneInfo("America/New_York")).date()

    sz_controls = st.container(border=True)
    c_cap, c_lev, c_date = sz_controls.columns([0.30, 0.40, 0.30], gap="large")
    with c_cap:
        sz_capital = st.number_input(
            "Capital ($)", min_value=1000, value=10000, step=1000, key="sz_capital",
        )
    with c_lev:
        sz_leverage = st.select_slider(
            tx("Apalancamiento", "Leverage"),
            options=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0],
            value=1.25,
            key="sz_leverage",
            help=tx("Para RSI2, BoW, EoM, 7DL y Oversold se usa tal cual. "
                    "ADST usa Min(1, apalanc. − 0,25) y BlackMonday Max(2, apalanc. + 0,25).",
                    "RSI2, BoW, EoM, 7DL and Oversold use it as is. "
                    "ADST uses Min(1, leverage − 0.25) and BlackMonday Max(2, leverage + 0.25)."),
        )
    with c_date:
        sz_date = st.date_input(
            tx("Fecha", "Date"), value=today_ny, min_value=date(2006, 1, 1), max_value=today_ny,
            format="DD/MM/YYYY", key="sz_date",
            help=tx("Cierre de esa fecha (o de la última sesión anterior si fue festivo). "
                    "Para hoy se usa el último valor disponible.",
                    "Close of that date (or of the previous session if it was a holiday). "
                    "For today, the latest available price is used."),
        )

    with st.spinner(tx("Descargando precios…", "Downloading prices…")):
        sz_stats, sz_errors = {}, []
        for mkt, yticker in SIZING_TICKERS.items():
            try:
                df_mkt = download_ohlc_sizing(yticker, sz_date)
            except Exception:
                df_mkt = pd.DataFrame()
            if len(df_mkt) < 60:
                sz_errors.append(tx(f"No hay datos suficientes de {yticker} para esa fecha.",
                                      f"Not enough {yticker} data for that date."))
            else:
                sz_stats[mkt] = sizing_market_stats(df_mkt)

    with st.expander(tx("Márgenes por contrato (edítalos según tu bróker)", "Margin per contract (edit to match your broker)"),
                     icon=":material/account_balance:"):
        mc1, mc2, _ = st.columns([0.3, 0.3, 0.4])
        margin_micro = {
            "SPX": mc1.number_input(tx("Margen 1 e-micro MES ($)", "Margin 1 MES e-micro ($)"), min_value=0, value=DEFAULT_MICRO_MARGIN["SPX"],
                                    step=50, key="sz_margin_spx"),
            "RUT": mc2.number_input(tx("Margen 1 e-micro M2K ($)", "Margin 1 M2K e-micro ($)"), min_value=0, value=DEFAULT_MICRO_MARGIN["RUT"],
                                    step=50, key="sz_margin_rut"),
        }
        st.caption(tx("Valores orientativos: cada bróker fija sus márgenes y cambian con la volatilidad. "
                      "Un e-nano se calcula como 1/10 del e-micro. GLD se compra al contado (sin margen).",
                      "Indicative values: each broker sets its own margins and they change with volatility. "
                      "An e-nano is taken as 1/10 of the e-micro. GLD is bought in cash (no margin)."))

    for msg in sz_errors:
        st.warning(msg)

    if not sz_stats:
        return

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
                        f"{tx('Último', 'Last')} · {now_ny:%d/%m/%Y %H:%M} NY</div>")
            else:
                foot = f"<div class='kpi-foot'>{tx('Cierre', 'Close')} · {s['date']:%d/%m/%Y}</div>"
            kpi_html.append(
                f"<div class='kpi-card'><div class='kpi-label'>{label}</div>"
                f"<div class='kpi-value'>{s['close']:,.2f}</div>{foot}</div>"
            )
    kpi_html.append("</div>")
    st.markdown("".join(kpi_html), unsafe_allow_html=True)

    # ---- Tabla de tamaños ----
    rows_html, export_rows, order_lines = [], [], []
    total_notional = total_risk = total_margin = 0.0
    for cfg in SHORT_TERM_SYSTEMS:
        stats = sz_stats.get(cfg["market"])
        if stats is None:
            continue
        r = size_short_term_system(cfg, stats, float(sz_capital), float(sz_leverage))
        n = r["n"]
        total_notional += r["notional"]
        # Riesgo: movimiento diario típico (1σ, volatilidad de Carver) de la posición, en $
        if cfg["tipo"] == 5:
            risk = n * stats["carver"]
            margin = np.nan
        else:
            risk = n * stats["carver"] * NANO_PV
            margin = n / NANOS_PER_MICRO * margin_micro[cfg["market"]]
        total_risk += risk
        total_margin += 0.0 if np.isnan(margin) else margin
        if cfg["side"] == "Largo":
            side_chip = f"<span class='chip chip-long'>{icon('arrow-up-right', 14, 2.5)}{tx('Largo', 'Long')}</span>"
        else:
            side_chip = f"<span class='chip chip-short'>{icon('arrow-down-right', 14, 2.5)}{tx('Corto', 'Short')}</span>"

        if n == 0:
            chips = [f"<span class='chip chip-off'>{tx('No opera', 'No trade')}</span>"]
        elif cfg["tipo"] == 5:
            chips = [f"<span class='chip chip-shares'><b>{r['pct']:.0f} %</b> - <b>{n:,}</b> {tx('acciones', 'shares')} GLD</span>"]
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
            f"<td><span class='num'>{risk:,.0f} $</span><span class='tw-date'>{risk / sz_capital * 100:.2f} % {tx('del capital', 'of capital')}</span></td>"
            + (f"<td><span class='na'>{tx('Contado', 'Cash')}</span></td>" if np.isnan(margin)
               else f"<td><span class='num'>{margin:,.0f} $</span></td>")
            + "</tr>"
        )

        # Exportación: fila de la tabla y línea de orden legible
        action = tx("Comprar", "Buy") if cfg["side"] == "Largo" else tx("Vender", "Sell")
        no_trade = tx("No opera", "No trade")
        if cfg["tipo"] == 5:
            qty_txt = f"{n:,} {tx('acciones', 'shares')} GLD" if n else no_trade
            micros = nanos = 0
        else:
            micros, nanos = split_micro_nano(n)
            parts = ([f"{micros} e-micro {MICRO_SYMBOL[cfg['market']]}"] if micros else []) + \
                    ([f"{nanos} e-nano {NANO_SYMBOL[cfg['market']]}"] if nanos else [])
            qty_txt = " + ".join(parts) if parts else no_trade
        order_lines.append(f"{cfg['name']:<12} {cfg['market']:<4} {action if n else '—':<8} {qty_txt}")
        export_rows.append({
            tx("Sistema", "System"): cfg["name"], tx("Mercado", "Market"): cfg["market"],
            tx("Dirección", "Direction"): tx(cfg["side"], "Long" if cfg["side"] == "Largo" else "Short"),
            tx("Acción", "Action"): action if n else no_trade,
            "E-micro": micros, "E-nano": nanos, tx("Acciones GLD", "GLD shares"): n if cfg["tipo"] == 5 else 0,
            tx("Precio de referencia", "Reference price"): stats["close"], tx("Nocional $", "Notional $"): r["notional"],
            tx("Riesgo diario 1σ $", "Daily risk 1σ $"): risk, tx("Margen aprox. $", "Approx. margin $"): margin,
        })

    table_html = (
        "<div class='table-wrap' style='overflow-x:auto'><table class='table-common sizing-table'><thead><tr>"
        + "".join(f"<th>{h}</th>" for h in (
            tx("Sistema", "System"), tx("Mercado", "Market"), tx("Dirección", "Direction"),
            tx("Comprar / vender", "Buy / sell"), tx("Nocional", "Notional"),
            tx("Apalanc. efectivo", "Effective leverage"), tx("Riesgo diario (1σ)", "Daily risk (1σ)"),
            tx("Margen aprox.", "Approx. margin")))
        + "</tr></thead><tbody>" + "".join(rows_html) + "</tbody></table></div>"
    )
    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown(
        f"<div class='sizing-foot'>{icon('layers', 16)}<span>"
        + tx(f"Si los {len(rows_html)} sistemas estuvieran "
             f"en posición a la vez, el nocional bruto sería <b>{total_notional:,.0f} $</b> "
             f"(<b>{total_notional / sz_capital:.2f}x</b> el capital), con un riesgo diario típico de "
             f"<b>{total_risk:,.0f} $</b> (suma de 1σ, sin contar diversificación) y un margen aproximado de "
             f"<b>{total_margin:,.0f} $</b>.",
             f"If all {len(rows_html)} systems were in a position at the same time, gross notional would be "
             f"<b>{total_notional:,.0f} $</b> (<b>{total_notional / sz_capital:.2f}x</b> capital), with a typical "
             f"daily risk of <b>{total_risk:,.0f} $</b> (sum of 1σ, ignoring diversification) and an approximate "
             f"margin of <b>{total_margin:,.0f} $</b>.")
        + "</span></div>",
        unsafe_allow_html=True,
    )
    st.caption(tx("Riesgo diario (1σ) = cuánto se mueve la posición en un día normal, según la volatilidad reciente "
                  "del subyacente (la misma medida de Carver que usa el dimensionado).",
                  "Daily risk (1σ) = how much the position moves on a normal day, based on the underlying's recent "
                  "volatility (the same Carver measure used for sizing)."))

    # ---- Exportar / copiar la orden ----
    ex1, ex2 = st.columns([0.35, 0.65], vertical_alignment="top")
    with ex1:
        df_export = pd.DataFrame(export_rows)
        df_export.insert(0, tx("Fecha precios", "Price date"), f"{max(s['date'] for s in sz_stats.values()):%Y-%m-%d}")
        df_export.insert(1, "Capital $", float(sz_capital))
        df_export.insert(2, tx("Apalancamiento", "Leverage"), float(sz_leverage))
        st.download_button(
            tx("Descargar la orden (CSV)", "Download the order (CSV)"), data=_to_csv(df_export, index=False),
            file_name=f"quant4all_{tx('posiciones', 'positions')}_{sz_date:%Y%m%d}.csv", mime="text/csv",
            icon=":material/download:", key="dl_sizing", on_click="ignore", width="stretch",
        )
    with ex2:
        with st.expander(tx("Copiar la orden como texto", "Copy the order as text"), icon=":material/content_copy:"):
            st.code(
                f"Quant4all · Short-term · {sz_date:%d/%m/%Y} · capital {sz_capital:,.0f} $ · "
                f"{tx('apalanc.', 'leverage')} {sz_leverage}\n"
                + "\n".join(order_lines),
                language=None,
            )
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.caption(
        tx("Herramienta informativa: no constituye recomendación de inversión. "
           "Verifica el tamaño con tu bróker antes de operar.",
           "Informational tool: not investment advice. Check the size with your broker before trading.")
    )


with tab_sizing:
    render_calculadora()


# =============================================
# TAB 4 — Sistemas (fichas descriptivas)
# =============================================
# Descripción conceptual (fuente: Guía del suscriptor v3.1). Sin reglas: solo qué hace cada sistema.
SUBSTACK_URL = "https://quant4all.substack.com/"

def system_info() -> list:
    """Fichas en el idioma activo (se construyen al pintar la pestaña)."""
    return [
        dict(
            name="ROCStar", subtitle=tx("Momentum · Acciones de EE. UU.", "Momentum · US equities"),
            series=["ROCStar"],
            tagline=tx("Sistema tendencial de medio plazo basado en el factor Momentum: las acciones que lo han "
                       "hecho bien recientemente tienden a seguir haciéndolo bien.",
                       "Medium-term trend system based on the Momentum factor: stocks that have done well "
                       "recently tend to keep doing well."),
            bullets=[
                tx("Selecciona las mejores acciones del S&P 500 y del Nasdaq 100 tras aplicar filtros de volatilidad.",
                   "Picks the best S&P 500 and Nasdaq 100 stocks after applying volatility filters."),
                tx("Cinco filtros de mercado externos actúan como protección y fijan la exposición a renta variable (0 %–95 %).",
                   "Five external market filters act as protection and set the equity exposure (0%–95%)."),
                tx("A fin de mes elige las acciones, que se operan en la primera sesión del mes siguiente.",
                   "Stocks are chosen at month-end and traded in the first session of the following month."),
            ],
            specs=[(tx("Tipo", "Type"), tx("Momentum + filtros de mercado", "Momentum + market filters")),
                   (tx("Activos", "Assets"), tx("Acciones S&P 500 y Nasdaq 100", "S&P 500 and Nasdaq 100 stocks")),
                   (tx("Temporalidad", "Timeframe"), tx("Mensual", "Monthly")),
                   (tx("Dirección", "Direction"), tx("Solo largos", "Long only")),
                   (tx("Posiciones", "Positions"), "10–15"),
                   (tx("Capital mínimo", "Minimum capital"), tx("15.000 $", "$15,000"))],
        ),
        dict(
            name="All Stars", subtitle=tx("Momentum concentrado · Acciones de EE. UU.", "Concentrated momentum · US equities"),
            series=["All Stars"],
            tagline=tx("La versión más agresiva y concentrada de la misma idea que ROCStar: Momentum de medio plazo "
                       "en las mejores acciones de EE. UU.",
                       "The more aggressive, concentrated version of the same idea as ROCStar: medium-term "
                       "Momentum in the best US stocks."),
            bullets=[
                tx("Selecciona las mejores acciones del S&P 500 y del Nasdaq 100 tras aplicar filtros de volatilidad.",
                   "Picks the best S&P 500 and Nasdaq 100 stocks after applying volatility filters."),
                tx("Cinco filtros de mercado fijan la exposición a renta variable (0 %–95 %); difieren ligeramente "
                   "de los de ROCStar en lógica y ponderación.",
                   "Five market filters set the equity exposure (0%–95%); they differ slightly from ROCStar's "
                   "in logic and weighting."),
                tx("Selección a fin de mes y ejecución en la primera sesión del mes siguiente.",
                   "Selection at month-end, execution in the first session of the following month."),
            ],
            specs=[(tx("Tipo", "Type"), tx("Momentum + filtros de mercado", "Momentum + market filters")),
                   (tx("Activos", "Assets"), tx("Acciones S&P 500 y Nasdaq 100", "S&P 500 and Nasdaq 100 stocks")),
                   (tx("Temporalidad", "Timeframe"), tx("Mensual", "Monthly")),
                   (tx("Dirección", "Direction"), tx("Solo largos", "Long only")),
                   (tx("Posiciones", "Positions"), "5"),
                   (tx("Capital mínimo", "Minimum capital"), tx("3.000 $", "$3,000"))],
        ),
        dict(
            name="TAA", subtitle=tx("Tactical Asset Allocation · Multiactivo", "Tactical Asset Allocation · Multi-asset"),
            series=["TAA"],
            tagline=tx("Funciona como un capitán de barco: adapta el rumbo a las condiciones de mercado ajustando "
                       "dinámicamente la exposición a cada activo.",
                       "Works like a ship's captain: it adapts its course to market conditions by dynamically "
                       "adjusting the exposure to each asset."),
            bullets=[
                tx("Busca aprovechar las fases alcistas y proteger el capital en los momentos adversos.",
                   "Aims to capture bull phases and protect capital in adverse times."),
                tx("La cesta la forman ETFs de índices, bonos, materias primas, oro y REITs.",
                   "The basket is made of ETFs on indices, bonds, commodities, gold and REITs."),
                tx("Tres subsistemas con reglas independientes que operan como uno solo.",
                   "Three sub-systems with independent rules that trade as one."),
            ],
            specs=[(tx("Tipo", "Type"), tx("Asignación táctica de activos", "Tactical asset allocation")),
                   (tx("Activos", "Assets"), tx("Índices, bonos, materias primas, oro y REITs",
                                                "Indices, bonds, commodities, gold and REITs")),
                   (tx("Temporalidad", "Timeframe"), tx("Mensual", "Monthly")),
                   (tx("Dirección", "Direction"), tx("Solo largos", "Long only")),
                   (tx("Posiciones", "Positions"), "3–6"),
                   (tx("Capital mínimo", "Minimum capital"), tx("5.000 $", "$5,000"))],
        ),
        dict(
            name="Short-term", subtitle=tx("ST x1 · ST x1.25 · Cartera de sistemas diarios",
                                           "ST x1 · ST x1.25 · Portfolio of daily systems"),
            series=["ST x1", "ST x1.25"],
            tagline=tx("Cartera de sistemas diarios de corto plazo, poco correlacionados entre sí, sobre el S&P 500, "
                       "el Russell 2000 y el oro.",
                       "Portfolio of short-term daily systems with low correlation to each other, on the S&P 500, "
                       "the Russell 2000 and gold."),
            bullets=[
                tx("Combina reversión a la media, estacionalidad y coberturas: largos o cortos según el sistema.",
                   "Combines mean reversion, seasonality and hedges: long or short depending on the system."),
                tx("Opera futuros micro y nano (MES, M2K) y GLD; el tamaño de cada posición se ajusta a la volatilidad "
                   "del mercado y al apalancamiento elegido (ver la pestaña Calculadora de Posición).",
                   "Trades micro and nano futures (MES, M2K) and GLD; each position is sized to market volatility "
                   "and the chosen leverage (see the Position Sizing tab)."),
                tx("x1 y x1.25 indican el apalancamiento objetivo de la cartera.",
                   "x1 and x1.25 are the portfolio's target leverage."),
            ],
            subs=[
                ("RSI2", tx("S&P 500 · largo", "S&P 500 · long"),
                 tx("reversión a la media en retrocesos bruscos.", "mean reversion on sharp pullbacks.")),
                ("BoW", tx("S&P 500 · largo", "S&P 500 · long"),
                 tx("estacionalidad y reversión a la media; mantiene la posición de 1 a 4 días.",
                    "seasonality and mean reversion; holds the position for 1 to 4 days.")),
                ("EoM", tx("S&P 500 · largo", "S&P 500 · long"),
                 tx("estacional: entra en los momentos históricamente más favorables.",
                    "seasonal: enters at historically favourable times.")),
                ("7DL", tx("S&P 500 · largo", "S&P 500 · long"),
                 tx("reversión a la media en retrocesos de corto plazo.", "mean reversion on short-term pullbacks.")),
                ("Oversold", tx("Russell 2000 · largo", "Russell 2000 · long"),
                 tx("reversión a la media con precio y amplitud de mercado.",
                    "mean reversion using price and market breadth.")),
                ("Black Monday", tx("Russell 2000 · corto", "Russell 2000 · short"),
                 tx("cobertura del fin de semana: corto del viernes al lunes, a cierre.",
                    "weekend hedge: short from Friday to Monday, at the close.")),
                ("ADST", tx("Russell 2000 · corto", "Russell 2000 · short"),
                 tx("cobertura cuando la amplitud de mercado no acompaña.", "hedge when market breadth weakens.")),
                ("Gold", tx("GLD · largo", "GLD · long"),
                 tx("sistema de corto plazo sobre el oro.", "short-term system on gold.")),
            ],
            specs=[(tx("Tipo", "Type"), tx("Cartera de sistemas diarios", "Portfolio of daily systems")),
                   (tx("Activos", "Assets"), tx("MES, M2K y GLD", "MES, M2K and GLD")),
                   (tx("Temporalidad", "Timeframe"), tx("Diaria", "Daily")),
                   (tx("Dirección", "Direction"), tx("Largos y cortos", "Long and short")),
                   (tx("Posiciones", "Positions"), tx("Hasta 8 (una por sistema)", "Up to 8 (one per system)"))],
        ),
    ]


@st.cache_data(show_spinner=False)
def system_full_history_stats(system_name: str) -> dict:
    """CAGR, Max DD y fecha de inicio de todo el histórico disponible del sistema."""
    rets = load_system_returns(system_name).fillna(0.0)
    nz = rets[rets != 0]
    first = nz.index[0] if not nz.empty else rets.index[0]
    m = perf_metrics(compute_equity_and_dd_from_returns(rets.loc[first:], 25000.0))
    return {"start": first, "end": rets.index[-1], "cagr": m["cagr"], "max_dd": m["max_dd"], "sharpe": m["sharpe"]}


def system_card_html(info: dict) -> str:
    specs = "".join(f"<div class='sys-spec'><div class='k'>{k}</div><div class='v'>{v}</div></div>"
                    for k, v in info["specs"])
    bullets = "".join(f"<li>{b}</li>" for b in info["bullets"])
    subs = ""
    if info.get("subs"):
        subs = "<div class='sys-subs'>" + "".join(
            f"<div class='sys-sub'><b>{n}</b> <span class='chip chip-market' style='font-size:0.66rem; padding:1px 7px'>"
            f"{mk}</span><br>{d[0].upper() + d[1:]}</div>" for n, mk, d in info["subs"]
        ) + "</div>"
    stats = []
    for s in info["series"]:
        try:
            h = system_full_history_stats(s)
        except Exception:
            continue
        prefix = f"<b>{s}</b> · " if len(info["series"]) > 1 else ""
        stats.append(
            f"<span>{prefix}{tx('Desde', 'Since')} <b>{h['start']:%Y}</b> · CAGR <b style='color:{_sign_color(h['cagr'])}'>"
            f"{h['cagr'] * 100:.1f}%</b> · Max DD <b style='color:{NEG_COLOR}'>{h['max_dd'] * 100:.1f}%</b>"
            f" · Sharpe <b>{h['sharpe']:.2f}</b></span>"
        )
    return (
        f"<div class='sys-card{' wide' if info.get('subs') else ''}'>"
        f"<div class='sys-card-head'><div><div class='sys-card-title'>{info['name']}</div>"
        f"<div class='sys-card-sub'>{info['subtitle']}</div></div>"
        f"<span class='sys-real'>✅ {tx('Operado con capital real', 'Traded with real money')}</span></div>"
        f"<div class='sys-tagline'>{info['tagline']}</div>"
        f"<ul class='sys-bullets'>{bullets}</ul>{subs}"
        f"<div class='sys-bottom'><div class='sys-specs'>{specs}</div>"
        f"<div class='sys-stats'>{''.join(stats)}</div></div>"
        "</div>"
    )


def render_sistemas():
    section_header(tx("Los sistemas de Quant4all", "The Quant4all systems"), "layers")
    st.markdown(
        "<div class='cta-band'><div class='cta-text'>"
        + tx("<b>Todos los sistemas se operan con dinero real.</b> "
             "Los suscriptores reciben cada señal y, periódicamente, el extracto del bróker que lo demuestra. "
             "Aquí tienes qué hace cada uno; las reglas exactas no se publican.",
             "<b>Every system is traded with real money.</b> "
             "Subscribers get every signal and, periodically, the broker statement that proves it. "
             "Here is what each one does; the exact rules are not published.")
        + f"</div><a href='{SUBSTACK_URL}' target='_blank' rel='noopener' class='newsletter-btn'>"
        f"{icon('mail', 16, 2.2)} {tx('Suscríbete gratis', 'Subscribe free')}</a></div>",
        unsafe_allow_html=True,
    )
    info = system_info()
    # Una sola rejilla HTML: las tres tarjetas se estiran a la misma altura
    st.markdown("<div class='sys-grid'>" + "".join(system_card_html(i) for i in info[:3]) + "</div>",
                unsafe_allow_html=True)
    # La ficha de Short-term es más larga (subsistemas): a todo el ancho
    st.markdown(system_card_html(info[3]), unsafe_allow_html=True)
    st.caption(tx(
        "CAGR, Max DD y Sharpe de todo el histórico disponible en la app, con reinversión. "
        "Para comparar en un mismo periodo, usa el Comparador. Rentabilidades pasadas no garantizan "
        "rentabilidades futuras.",
        "CAGR, Max DD and Sharpe over the full history available in the app, with reinvestment. "
        "To compare over the same period, use the Comparator. Past performance does not guarantee future results."
    ))


with tab_systems:
    render_sistemas()
