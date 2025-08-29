# app.py

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, time, date
import base64

# función para convertir la imagen en base64
def get_base64_of_bin_file(filename):
    with open(filename, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
logo_base64 = get_base64_of_bin_file("Logo.jpg")

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="Quant4all | Let's compare", page_icon=logo_base64, layout="wide")

# -----------------------
# Global CSS
# -----------------------
st.markdown("""
<style>
/* ===== Layout base ===== */
.block-container {padding-top: 1rem !important; padding-bottom: 0.5rem !important; padding-left: 2rem !important; padding-right: 2rem !important;}
h2 {margin-top: 0.25rem !important; margin-bottom: 0.25rem !important;}
.section-title {margin-top: 2rem; margin-bottom: 0.25rem;}

/* ===== Tablas unificadas y autoajuste ===== */
.table-common{
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;             /* columnas proporcionales y alturas consistentes por fila */
}
.table-common th, .table-common td{
  border: 1px solid #ddd;
  padding: 6px;
  text-align: center;
  vertical-align: middle;
  line-height: 1.15;
  font-size: 0.95rem;
  white-space: nowrap;             /* evita saltos de línea que alterarían altura por fila */
  overflow: hidden;
  text-overflow: ellipsis;
}
.table-common th{ font-weight: 700; }

/* Top/Worst: 1ª col Asset + 5 cols de valores */
.tw-tabular th:nth-child(1), .tw-tabular td:nth-child(1){ width: 20%; }
.tw-tabular th:nth-child(n+2), .tw-tabular td:nth-child(n+2){ width: 10%; }

/* Títulos compactos de las 3 tablas superiores */
.tri-title{
  text-align:center; margin-top: 0.25rem; margin-bottom: 0.5rem; font-size: 0.95rem;
}

/* Espacio entre bloques del centro */
.left-block-gap { height: 2rem; }
            
/* Fuerza mismo tamaño de celdas en todas las tablas de performance summary */
.table-common {
  table-layout: fixed;       /* columnas uniformes */
  width: 100%;
}

.table-common th, .table-common td {
  height: 3rem;              /* altura fija de cada fila */
  width: 16.6%;              /* 6 columnas => 100/6 ≈ 16.6% */
  text-align: center;
  vertical-align: middle;
  padding: 0.25rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
/* Columna Asset consistente en todas las tablas de Performance Summary */
.summary-table th:first-child,
.summary-table td:first-child,
.tw-tabular th:first-child,
.tw-tabular td:first-child {
  width: 15%;
}
.sticky-slider {
    position: sticky;
    top: 0;                  /* se queda pegado arriba */
    background-color: white; /* fondo para tapar lo de detrás */
    z-index: 999;            /* por encima del resto */
    padding-top: 0.5rem;     
    padding-bottom: 0.5rem;
}
/* Aumenta SOLO los números de las celdas de datos (no headers, no 1ª columna) */
.table-common.summary-table td:not(:first-child) .num,
.table-common.tw-tabular   td:not(:first-child) .num{
  font-size: 1.20rem !important;  /* súbelo si quieres (1.25rem, 1.3rem…) */
  font-weight: 600;
  color: #6b7280 !important;      /* gris muy oscuro */
  line-height: 1;                 /* no estira la altura de la celda */
  display: inline-block;
  vertical-align: middle;
}
.summary-table th, .summary-table td { width: 18.75%; }
.summary-table th:first-child,
.summary-table td:first-child { width: 20%; }

/* Fechas Top/Worst: exactamente igual que antes */
.table-common.tw-tabular td .tw-date{
  font-size: 0.8em !important;
  color: #6b7280 !important;
}
/* ===== KPI cards centradas ===== */
.kpi-card{
  text-align:center;
  border:1px solid #e5e7eb;
  border-radius:12px;
  padding:12px;
  box-shadow:0 2px 6px rgba(0,0,0,0.04);
}
.kpi-card .kpi-label{
  font-size:0.85rem;
  color:#6b7280;
  font-weight:600;
  margin-bottom:4px;
}
.kpi-card .kpi-value{
  font-size:1.6rem;
  font-weight:800;
  line-height:1;
}
 [data-testid="stSidebar"] {
        min-width: 18rem;
    }
            
</style>
""", unsafe_allow_html=True)


# -----------------------
# Sidebar
# -----------------------
with st.sidebar:
    st.markdown(f"""
    <style>
    /* ===== LOGO ===== */
    .sidebar-logo {{
        text-align: center;
        margin-top: 0rem;
        margin-bottom: 1.5rem;
    }}
    .sidebar-logo img {{
        width: 80px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}

    /* ===== BOTÓN NEWSLETTER ROJO ===== */
    .newsletter-btn {{
    display: inline-block;
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    color: #ffffff !important;      /* 👈 fuerza texto blanco */
    text-decoration: none !important; /* 👈 quita subrayado */
    padding: 0.6rem 1.6rem;
    border-radius: 999px;
    font-size: 1rem;
    font-weight: 700;
    text-transform: uppercase;
    transition: all 0.2s ease-in-out;
    box-shadow: 0 3px 6px rgba(0,0,0,0.15);
    }}
    .newsletter-btn:hover {{
        background: linear-gradient(135deg, #b91c1c, #dc2626);
        box-shadow: 0 6px 12px rgba(0,0,0,0.25);
        transform: translateY(-2px);
    }}
    </style>

    <!-- Logo -->
    <div class="sidebar-logo">
        <img src="data:image/jpg;base64,{logo_base64}">
    </div>

    <!-- Botón -->
    <div style='text-align:center; margin-bottom:2rem;'>
        <a href='https://quant4all.substack.com/' target='_blank' class='newsletter-btn'>
            SUBSCRIBE FREE
        </a>
    </div>
    
    """, unsafe_allow_html=True)

with st.sidebar:
    # 1) Initial Capital
    st.markdown("**Initial Capital ($)**")
    initial_capital = st.number_input("", min_value=1000, value=25000, step=500, label_visibility="collapsed")
    
    # 2) Begin / End
    st.markdown("**Begin | End**")
    dates_container = st.container()
    range_slider_container = st.container()

    st.markdown("")

    # 3) Tickers y Systems
    col_assets, col_systems = st.columns(2)
    with col_assets:
        st.markdown("**Tickers (Yahoo)**")
        tickers = []
        for i in range(4):
            v = st.text_input("", value="",  # 👈 por defecto vacío
                            placeholder=f"Ticker {i+1}", label_visibility="collapsed")
            if v.strip():
                tickers.append(v.strip())
    
        show_benchmark = st.checkbox("Use benchmark", value=True)
        benchmark = st.text_input("Benchmark", value="^GSPC", label_visibility="collapsed")

    with col_systems:
        st.markdown("**Quant4all Systems**")
        system_choices = ["", "ROCStar", "All Stars", "Big Three", "TAA"]  
        systems = []

        # Valores por defecto (All Stars, ROCStar, vacío)
        default_selection = ["All Stars", "ROCStar", "", ""]

        for i in range(4):
            choice = st.selectbox(
                f"sys{i}",
                system_choices,
                index=system_choices.index(default_selection[i]),
                label_visibility="collapsed"
            )
            if choice:
                systems.append(choice)



# -----------------------
# Helpers
# -----------------------
@st.cache_data(show_spinner=False)
def download_prices(ticker) -> pd.Series:
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
    return total_ret ** (1/years) - 1

def ann_vol_from_equity(df: pd.DataFrame) -> float:
    if df is None or df.empty or "ret" not in df.columns:
        return np.nan
    s = pd.Series(df["ret"]).dropna()
    if len(s) < 2:
        return np.nan
    return float(s.std(ddof=1) * np.sqrt(252) * 100.0)

# --- CSV systems loader (retornos DIARIOS en % -> proporción) ---
SYSTEM_FILES = {
    "ROCStar": "data/ROCStar.csv",
    "All Stars": "data/AllStars.csv",
    "Big Three": "data/BigThree.csv",
    "TAA": "data/TAA.csv",
}

@st.cache_data(show_spinner=False)
def load_system_returns(system_name: str) -> pd.Series:
    import os
    path = SYSTEM_FILES.get(system_name)
    if not path or not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el fichero para {system_name}: {path or '—'}")

    raw = pd.read_csv(
        path,
        header=None,
        engine="python",
        sep=None,
        comment="#",
        skip_blank_lines=True,
        dtype=str,
        na_values=["", "NA", "NaN", "nan", None]
    )

    if raw.shape[1] < 2:
        s = raw.iloc[:, 0].dropna().astype(str)
        parts = s.str.split(r"[;,|\s]\s*", n=1, expand=True)
        if parts.shape[1] < 2:
            raise ValueError("CSV inválido: necesito 2 columnas (fecha y retorno).")
        raw = parts

    raw = raw.iloc[:, :2].copy()
    raw.columns = ["date", "ret"]

    # Fechas (se espera DIARIO)
    raw["date"] = raw["date"].astype(str).str.strip()
    idx = pd.to_datetime(raw["date"], dayfirst=True, errors="coerce")
    if idx.isna().all():
        raise ValueError("No se han podido parsear las fechas (esperado DD/MM/YYYY).")
    idx = pd.to_datetime(idx.dt.date)

    # Retornos en % -> proporción
    ret_txt = raw["ret"].astype(str).str.replace("%", "", regex=False).str.strip()
    ret_txt = ret_txt.str.replace(",", ".", regex=False)
    ret = pd.to_numeric(ret_txt, errors="coerce")
    if ret.isna().all():
        raise ValueError("No se han podido parsear los retornos. Revisa que la 2ª columna sean números (en %).")
    ret = ret / 100.0

    s = pd.Series(ret.values, index=idx).sort_index()
    s = s.groupby(s.index).mean()  # por si hubiera duplicados de fecha
    s.name = system_name
    return s

# --- Plotting helpers ---
PALETTE = ["#06b6d4", "#e11d48", "#22c55e", "#f59e0b", "#8b5cf6"]
BENCH_COLOR = "#9ca3af"

def plot_equity(dict_equities, df_bench=None, bench_label=None, show_bench=True,
                unit="$", scale="Lin", series_color=None):
    fig = go.Figure()
    use_log = (unit == "$" and scale == "Log")

    # series
    for i, (label, df) in enumerate(dict_equities.items()):
        if df.empty:
            continue
        if unit == "$":
            y = df["equity"]
        else:
            base = df["equity"].iloc[0]
            y = (df["equity"] / base - 1.0) * 100.0
        color = series_color.get(label) if series_color else PALETTE[i % len(PALETTE)]
        fig.add_trace(go.Scatter(
            x=df.index, y=y, mode="lines", name=label,
            line=dict(color=color, width=2)
        ))

    # benchmark
    if show_bench and df_bench is not None and not df_bench.empty:
        if unit == "$":
            yb = df_bench["equity"]
        else:
            baseb = df_bench["equity"].iloc[0]
            yb = (df_bench["equity"] / baseb - 1.0) * 100.0
        fig.add_trace(go.Scatter(
            x=df_bench.index, y=yb, mode="lines", name=bench_label,
            line=dict(color=BENCH_COLOR, width=3)
        ))

    fig.update_layout(
        title="Equity Curve" + (" (%)" if unit == "%" else ""),
        height=360, margin=dict(l=0, r=0, t=40, b=2),
        yaxis_title=None, showlegend=False,
    )
    fig.update_yaxes(side="right", type="log" if (unit == "$" and use_log) else "linear")
    if unit == "%":
        fig.update_yaxes(ticksuffix=" %", tickformat=".1f")
    return fig

def plot_dd(dict_equities, df_bench=None, bench_label=None, show_bench=True, series_color=None):
    fig = go.Figure()
    for i, (label, df) in enumerate(dict_equities.items()):
        if df.empty:
            continue
        color = series_color.get(label) if series_color else PALETTE[i % len(PALETTE)]
        fig.add_trace(go.Scatter(x=df.index, y=df["dd"] * 100, mode="lines", name=label,
                                 line=dict(color=color, width=2)))
    if show_bench and df_bench is not None and not df_bench.empty:
        fig.add_trace(go.Scatter(x=df_bench.index, y=df_bench["dd"] * 100, mode="lines", name=bench_label,
                                 line=dict(color=BENCH_COLOR, width=3)))
    fig.update_layout(
        title="Drawdown (%)", height=360, margin=dict(l=0, r=0, t=40, b=2),
        yaxis_title=None, showlegend=False,
    )
    fig.update_yaxes(ticksuffix=" %", side="right")
    return fig

def render_summary_table(rows):
    html = ['<table class="table-common summary-table">']
    html.append("<thead><tr>")
    for h in ["Asset", "Return", "CAGR", "Max DD", "Vol"]:
        html.append(f"<th>{h}</th>")
    html.append("</tr></thead><tbody>")
    for r in rows:
        tr = "<tr>"
        tr += f"<td>{r['Serie']}</td>"
        if np.isnan(r["Total Return"]):
            tr += "<td>—</td><td>—</td><td>—</td><td>—</td>"
        else:
            tr += f"<td><span class='num'>{r['Total Return']:.1f}x</span></td>"
            tr += f"<td><span class='num'>{r['CAGR']:.1f} %</span></td>"
            tr += f"<td><span class='num'>{r['Max DD']:.1f} %</span></td>"
            tr += f"<td><span class='num'>{r['Vol']:.1f} %</span></td>"
        tr += "</tr>"
        html.append(tr)
    html.append("</tbody></table>")
    return "\n".join(html)

# ---------- Correlation helpers (DIARIO) ----------
def daily_returns_from_close(close: pd.Series) -> pd.Series:
    if close.empty:
        return pd.Series(dtype=float, name=close.name)
    rets = close.pct_change().dropna()
    rets.name = close.name
    return rets

def corr_heatmap_figure(corr_df: pd.DataFrame, labels_order, bench_color, series_color):
    """
    Heatmap sin título, paleta rojo(+1)->blanco(0)->verde(-1),
    diagonal gris (benchmark). Nombres coloreados en los ejes via anotaciones.
    """
    z = corr_df.values
    labels = labels_order

    colorscale = [
        [0.0, "#16a34a"],   # verde intenso (-1)
        [0.5, "#ffffff"],   # blanco (0)
        [1.0, "#dc2626"],   # rojo intenso (+1)
    ]

    base_heatmap = go.Heatmap(
        z=z, x=labels, y=labels, zmin=-1, zmax=1,
        colorscale=colorscale, showscale=True, colorbar=dict(title="ρ")
    )

    # Diagonal en gris benchmark
    diag = np.full_like(z, np.nan, dtype=float)
    np.fill_diagonal(diag, 1.0)
    diag_heatmap = go.Heatmap(
        z=diag, x=labels, y=labels, zmin=0, zmax=1,
        colorscale=[[0, bench_color], [1, bench_color]],
        showscale=False, hoverinfo="skip", opacity=1.0
    )

    fig = go.Figure(data=[base_heatmap, diag_heatmap])

    # Valores dentro de celdas
    for i, yi in enumerate(labels):
        for j, xj in enumerate(labels):
            val = z[i][j]
            if pd.notna(val):
                fig.add_annotation(
                    x=xj, y=yi, text=f"{val:.2f}",
                    showarrow=False,
                    font=dict(size=14, color="white" if abs(val) > 0.5 else "black")
                )

    # Quitar ticks y dibujar etiquetas horizontales coloreadas
    fig.update_xaxes(side="top", showticklabels=False)
    fig.update_yaxes(autorange="reversed", showticklabels=False)

    # Etiquetas arriba (X) y a la izquierda (Y) en el color de la serie
    for lab in labels:
        fig.add_annotation(
            x=lab, xref="x", y=1.02, yref="paper", text=lab,
            showarrow=False, font=dict(color=series_color.get(lab, "#111827"), size=14),
            yanchor="bottom"
        )
        fig.add_annotation(
            x=-0.02, xref="paper", y=lab, yref="y", text=lab,
            showarrow=False, font=dict(color=series_color.get(lab, "#111827"), size=14),
            xanchor="right", yanchor="middle"
        )

    fig.update_layout(height=520, margin=dict(l=100, r=20, t=60, b=20))
    return fig

# ---------- TOP/WORST helpers como TABLA ----------
def render_top_table(title: str, table_dict: dict, series_color: dict):
    """
    Tablas verdaderas para Top/Worst: 1ª col Asset, 5 cols Top/Worst.
    Se asume que table_dict contiene las MISMAS etiquetas (orden maestro),
    para que el nº de filas coincida con Performance Summary.
    """
    html = [f"<h4 class='tri-title'>{title}</h4>"]
    html.append("<table class='table-common tw-tabular'>")
    # Header
    html.append("<thead><tr>")
    html.append("<th>Asset</th>")
    for k in range(1, 6):
        html.append(f"<th>{'#' if '#' in title else '#'} {k}</th>")
    html.append("</tr></thead><tbody>")
    # Rows
    for label, items in table_dict.items():
        color = series_color.get(label, "#111827")
        row = f"<tr><td><span style='color:{color}; font-weight:600'>{label}</span></td>"
        for d, r in items:
            if pd.isna(r) or d is None:
                row += "<td>—</td>"
            else:
                sign = "+" if r >= 0 else ""
                row += (
                    "<td>"
                    f"<span class='num'>{sign}{r*100:.1f}</span><br>"
                    f"<span class='tw-date'>{d:%d/%m/%y}</span>"
                    "</td>"
                )
        row += "</tr>"
        html.append(row)
    html.append("</tbody></table>")
    return "\n".join(html)

def compute_top_bottom(series: pd.Series, k=5):
    """Devuelve top k y bottom k como listas de (fecha, retorno)."""
    if series is None or series.empty:
        return [], []
    s = series.dropna()
    if s.empty:
        return [], []
    top = s.sort_values(ascending=False).head(k)
    bottom = s.sort_values(ascending=True).head(k)
    return list(zip(top.index.to_pydatetime(), top.values)), list(zip(bottom.index.to_pydatetime(), bottom.values))

# -----------------------
# Data load (tickers + systems)
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
        sret = load_system_returns(sys)  # retornos DIARIOS (proporción)
        if not sret.empty:
            dict_system_rets[sys] = sret
    except Exception as e:
        errors.append(f"⚠️ Error cargando {sys}: {e}")

# Benchmark (descarga pero NO condiciona el rango global)
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
# Equity series (antes de fechas)
# -----------------------
equity_from_assets = {}
for label, close in dict_closes.items():
    equity_from_assets[label] = compute_equity_and_dd_from_close(close, initial_capital=25000)

equity_from_systems = {}
for label, rets in dict_system_rets.items():
    equity_from_systems[label] = compute_equity_and_dd_from_returns(rets, initial_capital=25000)

# -----------------------
# Determinar rango global común por RANGOS (benchmark fuera)
# -----------------------
series_ranges = []
for df in equity_from_assets.values():
    if not df.empty:
        series_ranges.append((df.index.min(), df.index.max()))
for df in equity_from_systems.values():
    if not df.empty:
        series_ranges.append((df.index.min(), df.index.max()))

if not series_ranges:
    st.error("No hay datos válidos para las series seleccionadas.")
    st.stop()

global_start = max(start for start, _ in series_ranges)
global_end   = min(end for _, end in series_ranges)

if global_end < global_start:
    st.error("No hay **rango temporal común** entre los activos/sistemas seleccionados.")
    st.stop()

# -----------------------
# Sidebar dates + capital (estado)
# -----------------------
# Mantener SIEMPRE la última fecha válida introducida por el usuario.
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
    a = max(a, global_start)
    b = min(b, global_end)
    return a, b

# --- Callbacks robustos ante borrado manual del campo de fecha ---
def on_slider_change():
    s, e = st.session_state["date_slider"]
    s, e = _clamp_to_global(s, e)
    st.session_state["start_input"] = s.date()
    st.session_state["end_input"] = e.date()
    st.session_state["start_valid"] = s.date()   # actualizar última válida
    st.session_state["end_valid"] = e.date()
    st.session_state["date_slider"] = (s, e)

def on_dates_change():
    # Si el usuario borra el contenido, mantener la última fecha válida
    raw_si = st.session_state.get("start_input")
    raw_ei = st.session_state.get("end_input")

    si = raw_si if isinstance(raw_si, date) else st.session_state.get("start_valid")
    ei = raw_ei if isinstance(raw_ei, date) else st.session_state.get("end_valid")

    sdt, edt = _clamp_to_global(datetime.combine(si, time.min), datetime.combine(ei, time.min))

    # Sincronizar todos los estados y persistir "última válida"
    st.session_state["date_slider"] = (sdt, edt)
    st.session_state["start_valid"] = sdt.date()
    st.session_state["end_valid"] = edt.date()
    st.session_state["start_input"] = st.session_state["start_valid"]
    st.session_state["end_input"] = st.session_state["end_valid"]

# --- Validar estado previo dentro de rango (tolerante a None/strings) ---
raw_si = st.session_state.get("start_input")
raw_ei = st.session_state.get("end_input")
si = raw_si if isinstance(raw_si, date) else st.session_state["start_valid"]
ei = raw_ei if isinstance(raw_ei, date) else st.session_state["end_valid"]

# Clamp y coherencia de orden
si = max(si, global_start.date())
ei = min(ei, global_end.date())
if si > ei:
    si, ei = global_start.date(), global_end.date()

# Sincronizar estados
st.session_state["start_valid"], st.session_state["end_valid"] = si, ei
st.session_state["start_input"], st.session_state["end_input"] = si, ei
st.session_state["date_slider"] = (datetime.combine(si, time.min), datetime.combine(ei, time.min))

with st.sidebar:
    with dates_container:
        col_start, col_end = st.columns(2)
        with col_start:
            st.date_input(
                "",
                key="start_input",
                min_value=global_start.date(),
                max_value=global_end.date(),
                label_visibility="collapsed",
                format="DD/MM/YYYY",
                on_change=on_dates_change
            )
        with col_end:
            st.date_input(
                "",
                key="end_input",
                min_value=global_start.date(),
                max_value=global_end.date(),
                label_visibility="collapsed",
                format="DD/MM/YYYY",
                on_change=on_dates_change
            )
    with range_slider_container:
        st.slider(
            "",
            min_value=datetime.combine(global_start.date(), time.min),
            max_value=datetime.combine(global_end.date(), time.min),
            key="date_slider",
            on_change=on_slider_change,
            format="DD/MM/YYYY"
        )
    

# -----------------------
# Slice por fechas elegidas + recomputar equity con capital inicial
# -----------------------
current_start, current_end = st.session_state["date_slider"]

dict_equities = {}

# Activos (tickers)
for label, close in dict_closes.items():
    c = close.loc[current_start:current_end]
    if c.empty:
        continue
    df = compute_equity_and_dd_from_close(c, float(initial_capital))
    dict_equities[label] = df

# Sistemas (diarios ya en proporción)
for label, rets in dict_system_rets.items():
    r = rets.loc[current_start:current_end]
    if r.empty:
        continue
    df = compute_equity_and_dd_from_returns(r, float(initial_capital))
    dict_equities[label] = df

# Benchmark adaptado a rango
df_bench = None
if show_benchmark and close_bench is not None:
    cb = close_bench.loc[current_start:current_end]
    if not cb.empty:
        df_bench = compute_equity_and_dd_from_close(cb, float(initial_capital))

# -----------------------
# Colores coherentes
# -----------------------
SERIES_COLOR = {}
for i, label in enumerate(dict_equities.keys()):
    SERIES_COLOR[label] = PALETTE[i % len(PALETTE)]
if show_benchmark and df_bench is not None and not df_bench.empty:
    SERIES_COLOR[benchmark.upper()] = BENCH_COLOR

# -----------------------
# Retornos DIARIOS mapa (para correlación, histogramas y TOP5)
# Orden correlación: Benchmark -> Sistemas -> Tickers
# -----------------------
daily_map = {}
if show_benchmark and close_bench is not None:
    bench_daily = daily_returns_from_close(close_bench.loc[current_start:current_end])
    if not bench_daily.empty:
        daily_map[benchmark.upper()] = bench_daily
for sys in systems:
    if sys in dict_system_rets:
        r_daily = dict_system_rets[sys].loc[current_start:current_end]
        if not r_daily.empty:
            daily_map[sys] = r_daily
for t in tickers:
    key = t.upper()
    if key in dict_closes:
        r = daily_returns_from_close(dict_closes[key].loc[current_start:current_end])
        if not r.empty:
            daily_map[key] = r

# ======================================================
# ======  BLOQUE ÚNICO CENTRAL (sin columna derecha) ===
# ======================================================


st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

st.markdown("""
<h1 style='margin-top:1rem; margin-bottom:.5rem;'>
  Let’s compare |
  <span style='font-size:.65em; font-weight:500; color:#000000;'>
    by <span style='color:#dc2626; font-weight:700;'>Quant4all</span>
  </span>
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div style='color:#6b7280; font-size:1.2rem; line-height:1.2; margin-bottom:1rem;'>
    📝 Compara de manera interactiva diferentes activos entre sí y con los sistemas de Quant4all.<br>
    🔍 Explora métricas clave de rentabilidad, riesgo y correlación a lo largo del tiempo.<br>
    🕹️ Usa la barra lateral para seleccionar capital inicial, tickers y sistemas a evaluar en el periodo que quieras.<br>
    📩 <span style='color:#dc2626; font-weight:600;'>Suscríbete gratis</span> a mi newsletter y recibirás:<br>
        <span style="display:inline-block; margin-left:30px;">- Un pdf con todos los detalles de mis sistemas.<br>
        - Acceso a grupo de Telegram donde comparto diariamente indicadores de Amplitud de Mercado y el sistema de cobertura Agorero.<br>
        - Las entradas y salidas del sistema Big Three.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:0; border-top:1px solid #6b7280; margin:2rem 0;'>", unsafe_allow_html=True)
st.markdown("<h3 class='section-title'>🏆 Performance Summary</h3>", unsafe_allow_html=True)


# ---- Preparar datos para las 3 tablas superiores ----
# Orden maestro: Sistemas -> Tickers -> Benchmark
ordered_labels_tables = []
for sys in systems:
    if (sys in dict_equities) or (sys in daily_map):
        ordered_labels_tables.append(sys)
for t in tickers:
    up = t.upper()
    if (up in dict_equities) or (up in daily_map):
        ordered_labels_tables.append(up)
if show_benchmark and (df_bench is not None and not df_bench.empty):
    ordered_labels_tables.append(benchmark.upper())

# Performance Summary (una fila por etiqueta del orden maestro)
rows = []
for label in ordered_labels_tables:
    df = df_bench if label == benchmark.upper() else dict_equities.get(label)
    if df is None or df.empty:
        rows.append({
            "Serie": f"<span style='color:{SERIES_COLOR.get(label, '#111827')}; font-weight:600'>{label}</span>",
            "Total Return": float("nan"), "CAGR": float("nan"),
            "Max DD": float("nan"), "Vol": float("nan")
        })
    else:
        rows.append({
            "Serie": f"<span style='color:{SERIES_COLOR.get(label, '#111827')}; font-weight:600'>{label}</span>",
            "Total Return": df["equity"].iloc[-1] / df["equity"].iloc[0],
            "CAGR": cagr_from_equity(df) * 100,
            "Max DD": df["dd"].min() * 100,
            "Vol": ann_vol_from_equity(df)
        })

# Top/Worst: siempre incluir TODAS las etiquetas (rellenar con — si no hay diarios)
def _five_dashes():
    return [(None, np.nan)] * 5

top_dict, worst_dict = {}, {}
for label in ordered_labels_tables:
    s = daily_map.get(label)
    if s is None or s.dropna().empty:
        top_dict[label] = _five_dashes()
        worst_dict[label] = _five_dashes()
    else:
        top5, bottom5 = compute_top_bottom(s, k=5)
        if len(top5) < 5: top5 += [(None, np.nan)] * (5 - len(top5))
        if len(bottom5) < 5: bottom5 += [(None, np.nan)] * (5 - len(bottom5))
        top_dict[label] = top5
        worst_dict[label] = bottom5

# ---- Render de las 3 tablas en 3 columnas iguales (sin contenedores visibles) ----
c1, c2, c3 = st.columns(3, gap="small")
with c1:
    st.markdown("<h4 class='tri-title'>🎯 Key Metrics</h4>", unsafe_allow_html=True)
    if rows:
        st.markdown(render_summary_table(rows), unsafe_allow_html=True)
    else:
        st.info("Sin datos en el rango seleccionado.")
with c2:
    st.markdown(render_top_table("🚀 Top Daily Returns", top_dict, series_color=SERIES_COLOR), unsafe_allow_html=True)
with c3:
    st.markdown(render_top_table("🔥 Worst Daily Returns", worst_dict, series_color=SERIES_COLOR), unsafe_allow_html=True)

st.markdown("<hr style='border:0; border-top:1px solid #6b7280; margin:2rem 0;'>", unsafe_allow_html=True)

# ---- Resto de contenidos centrales: gráficas y análisis ----
c1, c2 = st.columns([0.7, 0.3])   # 70% título, 30% controles
with c1:
    st.markdown("<h3 class='section-title'>📈 Equity & Drawdown</h3>", unsafe_allow_html=True)
with c2:
    col_u, col_s = st.columns(2)
    with col_u:
        unit_choice = st.radio("", options=["$", "%"], index=0, horizontal=True, label_visibility="collapsed")
    with col_s:
        scale_choice = st.radio("", options=["Lin", "Log"], index=0, horizontal=True, label_visibility="collapsed")

# Equity
equity_fig = plot_equity(
    dict_equities, df_bench, benchmark.upper() if show_benchmark else None,
    show_bench=show_benchmark, unit=unit_choice, scale=scale_choice,
    series_color=SERIES_COLOR
)
if unit_choice == "%":
    equity_fig.update_yaxes(type="linear", ticksuffix=" %", tickformat=".1f", side="right")
st.plotly_chart(equity_fig, use_container_width=True)

# Drawdown
st.plotly_chart(
    plot_dd(dict_equities, df_bench, benchmark.upper() if show_benchmark else None,
            show_bench=show_benchmark, series_color=SERIES_COLOR),
    use_container_width=True
)

# Gap
st.markdown('<div class="left-block-gap"></div>', unsafe_allow_html=True)


st.markdown("<hr style='border:0; border-top:1px solid #6b7280; margin:2rem 0;'>", unsafe_allow_html=True)

# Correlación
st.markdown("<h3 class='section-title'>🪢 Correlation matrix</h3>", unsafe_allow_html=True)
if len(daily_map) >= 2:
    ddf = pd.concat([s for s in daily_map.values()], axis=1)
    ddf.columns = list(daily_map.keys())
    ddf = ddf.dropna(how="all")
    corr_df = ddf.corr(method="pearson", min_periods=3)
    ordered_labels = list(daily_map.keys())
    corr_df = corr_df.reindex(index=ordered_labels, columns=ordered_labels)
    fig_corr = corr_heatmap_figure(
        corr_df=corr_df,
        labels_order=ordered_labels,
        bench_color=BENCH_COLOR,
        series_color=SERIES_COLOR
    )
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("Añade al menos **dos** series con datos en el periodo para ver la correlación.")

# Gap
st.markdown('<div class="left-block-gap"></div>', unsafe_allow_html=True)

st.markdown("<hr style='border:0; border-top:1px solid #6b7280; margin:2rem 0;'>", unsafe_allow_html=True)


# -----------------------
# 📊 Distribution of Daily Returns
# -----------------------
st.markdown("<h3 class='section-title'> 📊 Distribution of Daily Returns</h3>", unsafe_allow_html=True)

labels_tickers = [t.upper() for t in tickers if t.upper() in daily_map]
labels_systems = [s for s in systems if s in daily_map]
labels_bench = [benchmark.upper()] if (show_benchmark and benchmark.upper() in daily_map) else []
all_choices = labels_tickers + labels_systems + labels_bench

if not all_choices:
    st.info("No hay series disponibles en esta categoría para el periodo seleccionado.")
else:
    # === Selector centrado al 15% del ancho de la página ===
    outer_left, outer_mid, outer_right = st.columns([0.1, 0.8, 0.1])
    with outer_mid:
        sub_l, sub_c, sub_r = st.columns([0.40625, 0.1875, 0.40625])  # centro = 0.8*0.1875 = 15% total
        with sub_c:
            selected_label = st.selectbox("Serie", all_choices, index=0, label_visibility="collapsed")

    vals = (daily_map[selected_label].dropna() * 100.0)
    if vals.empty:
        st.info("No hay datos de retornos diarios para la serie seleccionada en el periodo.")
    else:
        # Layout 75% / 25% para gráfica y stats
        col_plot, col_side = st.columns([0.75, 0.25], gap="large")

        # Métricas
        mu = float(vals.mean())
        sigma = float(vals.std(ddof=1)) if len(vals) > 1 else 0.0
        skew = float(vals.skew()) if len(vals) > 2 else 0.0

        # ---- Figura (histograma + bandas σ) ----
        hist_fig = go.Figure()
        hist_fig.add_trace(go.Histogram(
            x=vals,
            nbinsx=100,
            name=selected_label,
            marker=dict(color=SERIES_COLOR.get(selected_label, "#0ea5e9")),
            opacity=0.95,
            hovertemplate="%{x:.2f}%<extra></extra>"
        ))

        bands = [
            (mu - 3*sigma, mu + 3*sigma, 0.12, "±3σ"),
            (mu - 2*sigma, mu + 2*sigma, 0.18, "±2σ"),
            (mu - 1*sigma, mu + 1*sigma, 0.24, "±1σ"),
        ]
        for x0, x1, opac, _ in bands:
            if np.isfinite(x0) and np.isfinite(x1) and x1 >= x0:
                hist_fig.add_vrect(x0=x0, x1=x1, fillcolor="#9ca3af", opacity=opac, line_width=0)

        hist_fig.add_shape(type="line", x0=mu, x1=mu, y0=0, y1=1, xref="x", yref="paper",
                           line=dict(color="#111827", width=2))
        for k in (1, 2, 3):
            for xk in (mu + k*sigma, mu - k*sigma):
                hist_fig.add_shape(type="line", x0=xk, x1=xk, y0=0, y1=1, xref="x", yref="paper",
                                   line=dict(color="#6b7280", width=1, dash="dash"))

        hist_fig.add_annotation(x=mu, y=1.06, xref="x", yref="paper",
                                text="μ", showarrow=False, font=dict(size=12, color="#111827"))
        for k, lab in zip((1, 2, 3), ("±1σ", "±2σ", "±3σ")):
            hist_fig.add_annotation(x=mu + k*sigma, y=1.06, xref="x", yref="paper",
                                    text=f"+{lab}", showarrow=False, font=dict(size=11, color="#6b7280"))
            hist_fig.add_annotation(x=mu - k*sigma, y=1.06, xref="x", yref="paper",
                                    text=f"-{lab}", showarrow=False, font=dict(size=11, color="#6b7280"))

        hist_fig.update_layout(
            height=540,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title="Daily return (%)",
            yaxis_title="Frequency",
            showlegend=False,
            bargap=0.02
        )

        with col_plot:
            st.plotly_chart(hist_fig, use_container_width=True)

        # ---- Columna derecha con STATS / Threshold / KPIs ----
        with col_side:
            st.markdown(f"""
            <div style="text-align:center; border:1px solid #e5e7eb; border-radius:12px; padding:12px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.04); margin-top:.5rem;">
                <div style="font-weight:700; margin-bottom:.25rem;">STATS</div>
                <div style="display:flex; flex-direction:column; gap:.35rem; font-size:0.95rem; align-items:center;">
                    <div>Mean (μ): <span style="font-weight:600">{mu:.3f}%</span></div>
                    <div>Std. Dev (σ): <span style="font-weight:600">{sigma:.3f}%</span></div>
                    <div>Skewness: <span style="font-weight:600">{skew:.3f}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:5rem;'></div>", unsafe_allow_html=True)

            th_col1, th_col2 = st.columns([0.5, 0.5])
            with th_col1:
                st.markdown("""
                    <div style="display:flex; justify-content:center; align-items:center;
                                height:38px; font-weight:600;">
                        Threshold (%)
                    </div>
                    """, unsafe_allow_html=True)
            with th_col2:
                threshold_pct = st.number_input(
                    "", min_value=0.0, max_value=100.0, value=5.0, step=0.5, format="%.1f",
                    label_visibility="collapsed"
                )

            thr = float(threshold_pct)
            st.markdown("<h4 style='text-align:center;'>Number of days with returns:</h4>", unsafe_allow_html=True)

            pos_days = int((vals >= +thr).sum())
            neg_days = int((vals <= -thr).sum())

            k1, k2 = st.columns(2)
            with k1:
                st.markdown(f"""
                <div style="text-align:center;">
                    <div style="font-size:1rem; font-weight:600;">≥ +{thr:.1f}%</div>
                    <div style="font-size:3rem; color:green;">{pos_days}</div>
                </div>
                """, unsafe_allow_html=True)
            with k2:
                st.markdown(f"""
                <div style="text-align:center;">
                    <div style="font-size:1rem; font-weight:600;">≤ -{thr:.1f}%</div>
                    <div style="font-size:3rem; color:red;">{neg_days}</div>
                </div>
                """, unsafe_allow_html=True)


                
# ======================
# === Distribution of Monthly Returns
# ======================
st.markdown("<hr style='border:0; border-top:1px solid #6b7280; margin:2rem 0;'>", unsafe_allow_html=True)
st.markdown("<h3 class='section-title'>📅 Distribution of Monthly Returns</h3>", unsafe_allow_html=True)

# --- CSS sólo para la tabla (80% centrada) ---
st.markdown("""
<style>
.monthly-heat-wrap { width: 80%; margin: 0 auto; }
.monthly-heat {
  border-collapse: collapse; width: 100%; table-layout: fixed; font-size: 0.95rem;
}
.monthly-heat th, .monthly-heat td {
  border: 1px solid #d1d5db; padding: 6px 8px; text-align: center; vertical-align: middle;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.monthly-heat thead th { background: #f3f4f6; font-weight: 800; }
.monthly-heat tfoot td { background: #f9fafb; font-weight: 700; }
.monthly-heat td.year-col, .monthly-heat th.year-col { width: 8%; font-weight: 700; }
.monthly-heat th.mon-col, .monthly-heat td.mon-col { width: 6.9%; }
.monthly-heat th.ytd-col, .monthly-heat td.ytd-col { width: 7.8%; font-weight: 800; }
.monthly-heat .cell { color: #111827; font-weight: 600; }
.monthly-heat .na { color: #6b7280; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- Construir lista de series: benchmark + sistemas + tickers ---
available_labels = []
label_to_series = {}

# Benchmark
if show_benchmark and close_bench is not None and not close_bench.empty:
    available_labels.append(benchmark.upper())
    label_to_series[benchmark.upper()] = close_bench

# Sistemas (retornos diarios -> agregamos a mensual)
for sys, rets in dict_system_rets.items():
    if not rets.empty:
        available_labels.append(sys)
        label_to_series[sys] = rets

# Tickers
for t, s in dict_closes.items():
    if not s.empty:
        available_labels.append(t.upper())
        label_to_series[t.upper()] = s

if not available_labels:
    st.info("Añade al menos un **ticker**, **sistema** o el benchmark para ver el análisis mensual.")
else:
    # === Selector centrado al 15% del ancho de la página ===
    # 1) Fila de 3 columnas para lograr un contenedor central del 80%
    outer_left, outer_mid, outer_right = st.columns([0.1, 0.8, 0.1])
    with outer_mid:
        # 2) Dentro del 80%, subcolumnas [0.40625, 0.1875, 0.40625] -> centro = 0.8*0.1875 = 0.15 del total
        sub_l, sub_c, sub_r = st.columns([0.40625, 0.1875, 0.40625])
        with sub_c:
            monthly_label = st.selectbox("Serie", available_labels, index=0, label_visibility="collapsed")

    ser = label_to_series[monthly_label].loc[current_start:current_end]
    if ser.empty:
        st.info("No hay datos en el rango seleccionado para esta serie.")
    else:
        # --- Retornos mensuales ---
        if monthly_label in dict_system_rets:   # sistema (retornos diarios en proporción)
            m_ret = ser.resample("M").apply(lambda x: (1 + x).prod() - 1) * 100
        else:                                   # ticker/benchmark (precios)
            m_close = ser.resample("M").last()
            m_ret = m_close.pct_change() * 100

        df = m_ret.to_frame("ret").dropna(how="all")
        df["Year"] = df.index.year
        df["Month"] = df.index.month
        pivot = df.pivot(index="Year", columns="Month", values="ret").sort_index()
        yret = ((1.0 + (pivot / 100.0)).prod(axis=1) - 1.0) * 100.0
        avg_row, avg_y = pivot.mean(axis=0), yret.mean()

        # --- Colores (verde+ / rojo-) con intensidad limitada (±20%) ---
        def bg_color(v: float) -> str:
            if pd.isna(v): return ""
            lim = 20.0
            x = max(-lim, min(lim, float(v)))
            if x >= 0:
                alpha, (r1,g1,b1), (r2,g2,b2) = x/lim, (229,247,233), (22,163,74)
            else:
                alpha, (r1,g1,b1), (r2,g2,b2) = -x/lim, (252,231,231), (220,38,38)
            r = int(r1 + (r2 - r1)*alpha); g = int(g1 + (g2 - g1)*alpha); b = int(b1 + (b2 - b1)*alpha)
            return f"background-color: rgb({r},{g},{b});"

        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

        # --- Render tabla (80% centrado) ---
        html = ["<div class='monthly-heat-wrap'><table class='monthly-heat'>"]
        html.append("<thead><tr><th class='year-col'>Year</th>")
        for m in months: html.append(f"<th class='mon-col'>{m}</th>")
        html.append("<th class='ytd-col'>Yr%</th></tr></thead><tbody>")
        for yr in pivot.index:
            html.append(f"<tr><td class='year-col'>{yr}</td>")
            for m_idx in range(1, 13):
                v = pivot.loc[yr].get(m_idx, np.nan)
                if pd.isna(v):
                    html.append("<td class='mon-col na'>N/A</td>")
                else:
                    html.append(f"<td class='mon-col' style='{bg_color(v)}'><span class='cell'>{v:+.1f}%</span></td>")
            vy = yret.get(yr, np.nan)
            if pd.isna(vy):
                html.append("<td class='ytd-col na'>—</td>")
            else:
                html.append(f"<td class='ytd-col' style='{bg_color(vy)}'><span class='cell'>{vy:+.1f}%</span></td>")
            html.append("</tr>")
        html.append("</tbody><tfoot><tr><td class='year-col'>Avg</td>")
        for m_idx in range(1, 13):
            v = avg_row.get(m_idx, np.nan)
            if pd.isna(v):
                html.append("<td class='mon-col na'>—</td>")
            else:
                html.append(f"<td class='mon-col' style='{bg_color(v)}'><span class='cell'>{v:+.1f}%</span></td>")
        if pd.isna(avg_y):
            html.append("<td class='ytd-col na'>—</td>")
        else:
            html.append(f"<td class='ytd-col' style='{bg_color(avg_y)}'><span class='cell'>{avg_y:+.1f}%</span></td>")
        html.append("</tr></tfoot></table></div>")

        st.markdown("".join(html), unsafe_allow_html=True)
