import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, time, date
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
)

# -----------------------
# Global CSS — Modern Dark-Accent Design
# -----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 1400px;
}

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.25rem;
    font-weight: 700;
    color: #111827;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #f3f4f6;
}

/* ── Divider ── */
.q-divider {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 2rem 0;
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
}
.kpi-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 1rem 1.25rem;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    transition: box-shadow 0.2s;
}
.kpi-card:hover { box-shadow: 0 4px 14px rgba(0,0,0,0.10); }
.kpi-card .kpi-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.3rem;
}
.kpi-card .kpi-value {
    font-size: 1.75rem;
    font-weight: 800;
    line-height: 1;
    color: #111827;
}

/* ── Summary / Top-Worst tables ── */
.table-wrap {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.table-common {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    font-family: 'Inter', sans-serif;
}
.table-common thead th {
    background: #f9fafb;
    padding: 10px 8px;
    font-size: 0.78rem;
    font-weight: 700;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    text-align: center;
    border-bottom: 1px solid #e5e7eb;
    white-space: nowrap;
}
.table-common tbody td {
    padding: 10px 8px;
    text-align: center;
    vertical-align: middle;
    border-bottom: 1px solid #f3f4f6;
    font-size: 0.92rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.table-common tbody tr:last-child td { border-bottom: none; }
.table-common tbody tr:hover td { background: #f9fafb; }

/* Numbers inside cells */
.num {
    font-size: 1.05rem;
    font-weight: 700;
    color: #111827;
}
.tw-date {
    font-size: 0.72rem;
    color: #9ca3af;
    display: block;
    margin-top: 2px;
}

/* Column widths — summary */
.summary-table th:first-child, .summary-table td:first-child { width: 22%; text-align: left; padding-left: 14px; }
.summary-table th:not(:first-child), .summary-table td:not(:first-child) { width: 19.5%; }

/* Column widths — top/worst */
.tw-tabular th:first-child, .tw-tabular td:first-child { width: 22%; text-align: left; padding-left: 14px; }
.tw-tabular th:not(:first-child), .tw-tabular td:not(:first-child) { width: 15.6%; }

/* Table title pill */
.table-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: #374151;
    padding: 10px 14px 8px 14px;
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
    letter-spacing: 0.01em;
}

/* ── Chart card wrapper ── */
.chart-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 0.5rem 0.75rem 0.25rem 0.75rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}

/* ── Monthly heat table ── */
.monthly-heat-wrap { width: 88%; margin: 0 auto; }
.monthly-heat {
    border-collapse: collapse;
    width: 100%;
    table-layout: fixed;
    font-size: 0.88rem;
    border-radius: 12px;
    overflow: hidden;
    font-family: 'Inter', sans-serif;
}
.monthly-heat th, .monthly-heat td {
    border: 1px solid #e5e7eb;
    padding: 6px 4px;
    text-align: center;
    vertical-align: middle;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.monthly-heat thead th {
    background: #f3f4f6;
    font-weight: 700;
    font-size: 0.78rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.monthly-heat tfoot td { background: #f9fafb; font-weight: 700; }
.monthly-heat td.year-col, .monthly-heat th.year-col { width: 7%; font-weight: 700; color: #374151; }
.monthly-heat th.mon-col, .monthly-heat td.mon-col { width: 6.5%; }
.monthly-heat th.ytd-col, .monthly-heat td.ytd-col { width: 7.5%; font-weight: 800; }
.monthly-heat .cell { color: #111827; font-weight: 600; font-size: 0.82rem; }
.monthly-heat .na { color: #9ca3af; font-weight: 500; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    min-width: 18rem;
    background: #fafafa;
}
[data-testid="stSidebar"] .stMarkdown p { font-size: 0.85rem; font-weight: 600; color: #374151; margin-bottom: 4px; }

/* ── Stats card ── */
.stats-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 1rem 1.25rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    text-align: center;
    margin-top: 0.5rem;
}
.stats-card .stats-title {
    font-size: 0.75rem;
    font-weight: 700;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.75rem;
}
.stats-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0;
    border-bottom: 1px solid #f3f4f6;
    font-size: 0.88rem;
}
.stats-row:last-child { border-bottom: none; }
.stats-row .stat-label { color: #6b7280; }
.stats-row .stat-val { font-weight: 700; color: #111827; }

/* ── Threshold counter cards ── */
.count-card {
    border-radius: 14px;
    padding: 1rem 0.5rem;
    text-align: center;
    margin-top: 0.5rem;
}
.count-card .count-label { font-size: 0.82rem; font-weight: 700; margin-bottom: 4px; }
.count-card .count-val { font-size: 2.8rem; font-weight: 800; line-height: 1; }
.count-card.positive { background: #dcfce7; border: 1px solid #86efac; }
.count-card.positive .count-label { color: #16a34a; }
.count-card.positive .count-val { color: #15803d; }
.count-card.negative { background: #fee2e2; border: 1px solid #fca5a5; }
.count-card.negative .count-label { color: #dc2626; }
.count-card.negative .count-val { color: #b91c1c; }

/* ── Hero ── */
.hero-title {
    font-size: 2rem;
    font-weight: 800;
    color: #111827;
    line-height: 1.2;
    margin-bottom: 0.25rem;
}
.hero-sub { color: #dc2626; }
.hero-desc {
    background: #f9fafb;
    border-left: 4px solid #dc2626;
    border-radius: 0 10px 10px 0;
    padding: 0.85rem 1.25rem;
    color: #374151;
    font-size: 0.95rem;
    line-height: 1.7;
    margin-bottom: 0.5rem;
}

/* ── Radio / controls pill ── */
div[data-testid="stHorizontalBlock"] .stRadio > label { font-size: 0.8rem; }

/* ── Newsletter button ── */
.newsletter-btn {
    display: inline-block;
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    color: #ffffff !important;
    text-decoration: none !important;
    padding: 0.55rem 1.4rem;
    border-radius: 999px;
    font-size: 0.9rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    transition: all 0.2s;
    box-shadow: 0 3px 8px rgba(220,38,38,0.35);
}
.newsletter-btn:hover {
    box-shadow: 0 6px 16px rgba(220,38,38,0.45);
    transform: translateY(-2px);
}

/* ── Sidebar logo ── */
.sidebar-logo { text-align: center; margin-bottom: 1.2rem; }
.sidebar-logo img { width: 72px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.12); }

/* hide default streamlit header/footer noise */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


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

    st.markdown("""
    <div style='text-align:center; margin-bottom:1.5rem;'>
        <a href='https://quant4all.substack.com/' target='_blank' class='newsletter-btn'>
            ✉ SUBSCRIBE FREE
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
        system_choices = ["", "ROCStar", "All Stars", "Big Three", "TAA"]
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
    raw = pd.read_csv(
        path, header=None, engine="python", sep=None,
        comment="#", skip_blank_lines=True, dtype=str,
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
    font=dict(family="Inter, sans-serif", size=13, color="#374151"),
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=0, r=0, t=40, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(showgrid=False, zeroline=False, showline=True,
               linecolor="#e5e7eb", tickfont=dict(size=11)),
    yaxis=dict(showgrid=True, gridcolor="#f3f4f6", zeroline=False,
               showline=False, tickfont=dict(size=11), side="right"),
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
        fig.add_trace(go.Scatter(
            x=df.index, y=df["dd"] * 100, mode="lines", name=label,
            line=dict(color=color, width=2),
            fill="tozeroy",
            fillcolor=color.replace(")", ", 0.08)").replace("rgb(", "rgba(").replace("#", "").replace(
                color, color + "18"
            ) if color.startswith("#") else color,
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
    html = ['<div class="table-wrap"><div class="table-title">🎯 Key Metrics</div>']
    html.append('<table class="table-common summary-table"><thead><tr>')
    for h in ["Asset", "Total Return", "CAGR", "Max DD", "Vol"]:
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


def render_top_table(title: str, icon: str, table_dict: dict, series_color: dict):
    html = [f'<div class="table-wrap"><div class="table-title">{icon} {title}</div>']
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

# ---- Hero ----
st.markdown("""
<div class='hero-title'>
  Let's compare &nbsp;<span class='hero-sub'>by Quant4all</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='hero-desc'>
  📊 Compara activos y sistemas de trading de forma interactiva — rentabilidad, riesgo y correlación.<br>
  🕹️ Usa la barra lateral para configurar capital, tickers, sistemas y rango temporal.<br>
  📩 <strong style='color:#dc2626;'>Suscríbete gratis</strong> a la newsletter y recibe el PDF con todos los detalles de los sistemas,
  acceso al grupo de Telegram con indicadores de Amplitud de Mercado y señales del sistema Big Three.
</div>
""", unsafe_allow_html=True)

# ---- Master label order: Systems → Tickers → Benchmark ----
ordered_labels: list[str] = []
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

# =============================================
# Section 1 — Performance Summary (3 tables)
# =============================================
st.markdown("<div class='section-header'>🏆 Performance Summary</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    if summary_rows:
        st.markdown(render_summary_table(summary_rows), unsafe_allow_html=True)
    else:
        st.info("Sin datos en el rango seleccionado.")
with c2:
    st.markdown(render_top_table("Top Daily Returns", "🚀", top_dict, SERIES_COLOR), unsafe_allow_html=True)
with c3:
    st.markdown(render_top_table("Worst Daily Returns", "🔥", worst_dict, SERIES_COLOR), unsafe_allow_html=True)

st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)

# =============================================
# Section 2 — Equity & Drawdown
# =============================================
c_title, c_ctrl = st.columns([0.75, 0.25])
with c_title:
    st.markdown("<div class='section-header'>📈 Equity & Drawdown</div>", unsafe_allow_html=True)
with c_ctrl:
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    col_u, col_s = st.columns(2)
    with col_u:
        unit_choice = st.radio("", options=["$", "%"], index=0, horizontal=True, label_visibility="collapsed")
    with col_s:
        scale_choice = st.radio("", options=["Lin", "Log"], index=0, horizontal=True, label_visibility="collapsed")

st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
equity_fig = plot_equity(
    dict_equities, df_bench, benchmark.upper() if show_benchmark else None,
    show_bench=show_benchmark, unit=unit_choice, scale=scale_choice,
    series_color=SERIES_COLOR,
)
st.plotly_chart(equity_fig, use_container_width=True, config={"displayModeBar": False})
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
dd_fig = plot_dd(
    dict_equities, df_bench, benchmark.upper() if show_benchmark else None,
    show_bench=show_benchmark, series_color=SERIES_COLOR,
)
st.plotly_chart(dd_fig, use_container_width=True, config={"displayModeBar": False})
st.markdown("</div>", unsafe_allow_html=True)

# ---- Legend (color dots + labels) ----
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

# =============================================
# Section 3 — Correlation Matrix
# =============================================
st.markdown("<div class='section-header'>🪢 Correlation Matrix</div>", unsafe_allow_html=True)
if len(daily_map) >= 2:
    ddf = pd.concat(list(daily_map.values()), axis=1)
    ddf.columns = list(daily_map.keys())
    ddf = ddf.dropna(how="all")
    corr_df = ddf.corr(method="pearson", min_periods=3)
    ordered_corr = list(daily_map.keys())
    corr_df = corr_df.reindex(index=ordered_corr, columns=ordered_corr)
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.plotly_chart(
        corr_heatmap_figure(corr_df, ordered_corr, BENCH_COLOR, SERIES_COLOR),
        use_container_width=True, config={"displayModeBar": False},
    )
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Añade al menos **dos** series con datos en el periodo para ver la correlación.")

st.markdown("<div class='q-divider'></div>", unsafe_allow_html=True)

# =============================================
# Section 4 — Distribution of Daily Returns
# =============================================
st.markdown("<div class='section-header'>📊 Distribution of Daily Returns</div>", unsafe_allow_html=True)

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

        # histogram
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
        for k, lab in zip((1, 2, 3), ("±1σ", "±2σ", "±3σ")):
            for sign, prefix in ((1, "+"), (-1, "-")):
                hist_fig.add_annotation(
                    x=mu + sign * k * sigma, y=1.06, xref="x", yref="paper",
                    text=f"{prefix}{lab}", showarrow=False, font=dict(size=10, color="#6b7280"),
                )
        _apply_layout(hist_fig, "", height=460)
        hist_fig.update_layout(
            xaxis_title="Daily Return (%)",
            yaxis=dict(title="Frequency", side="left", showgrid=True,
                       gridcolor="#f3f4f6", tickfont=dict(size=11)),
            bargap=0.02, showlegend=False,
        )

        with col_plot:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.plotly_chart(hist_fig, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        with col_side:
            # Stats card
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

            # Threshold input
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

# =============================================
# Section 5 — Distribution of Monthly Returns
# =============================================
st.markdown("<div class='section-header'>📅 Distribution of Monthly Returns</div>", unsafe_allow_html=True)

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

available_labels: list[str] = []
label_to_series: dict[str, pd.Series] = {}
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
