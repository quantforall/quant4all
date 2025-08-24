# q4a_ui.py
# -----------------------------------------------------------------------------
# Quant4all Streamlit UI helper: dark-mode aware + mobile responsive + Plotly theme.
# Import in your app:
#   from q4a_ui import setup_page, inject_css, make_fig
#   setup_page(page_title="Quant4all | Let's compare", page_icon="📈", layout="centered", collapse_sidebar=True)
#   inject_css(max_width_px=1100)
#   # Use make_fig(...) for Plotly figures + st.plotly_chart(fig, use_container_width=True)
# -----------------------------------------------------------------------------

from __future__ import annotations
from typing import Optional
import streamlit as st
import plotly.graph_objects as go

# -------------------- Theme helpers --------------------
def _theme_is_dark() -> bool:
    try:
        return (st.get_option("theme.base") or "light") == "dark"
    except Exception:
        return False

def _theme_tokens():
    is_dark = _theme_is_dark()
    return {
        "primary": st.get_option("theme.primaryColor") or "#4F46E5",
        "bg": st.get_option("theme.backgroundColor") or ("#0E1117" if is_dark else "#FFFFFF"),
        "bg2": st.get_option("theme.secondaryBackgroundColor") or ("#262730" if is_dark else "#F5F5F5"),
        "text": st.get_option("theme.textColor") or ("#FAFAFA" if is_dark else "#0E1117"),
        "muted": "#3A3A3A" if is_dark else "#E5E7EB",
        "muted2": "#2F3136" if is_dark else "#E5E7EB",
        "is_dark": is_dark,
    }

TOK = _theme_tokens()
IS_DARK = TOK["is_dark"]

# -------------------- CSS injection --------------------
def inject_css(max_width_px: int = 1500):
    st.markdown(f"""
    <style>
    /* Container width */
    .block-container {{ max-width: {max_width_px}px; margin: auto; }}

    /* Background + text according to theme */
    html, body, [data-testid="stAppViewContainer"] {{ background:{TOK["bg"]}!important; color:{TOK["text"]}!important; }}
    [data-testid="stSidebar"] {{ background:{TOK["bg2"]}!important; border-right:1px solid {TOK["muted2"]}; }}

    /* Columns stack on small screens */
    @media (max-width: 900px) {{
      .block-container {{
          max-width: 1100px;
          margin: auto;
          padding-left: 0rem;
          padding-right: 0rem;
          padding-top: 0.5rem;
          padding-bottom: 0.5rem;
        }}
      [data-testid="stHorizontalBlock"] > div[data-testid="column"] {{ width:100%!important; flex:1 1 100%!important; }}
    }}

    /* Fluid type */
    h1, h2 {{ line-height: 1.2; }}
    h1 {{ font-size: clamp(22px, 4.5vw, 34px); }}
    h2 {{ font-size: clamp(18px, 3.6vw, 28px); }}
    p, li, label, span {{ font-size: clamp(14px, 2.8vw, 16px); }}

    /* Table style */
    .table-common {{
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
      background: transparent;
      color: {TOK["text"]};
    }}
    .table-common th, .table-common td {{
      padding: 8px 10px;
      border-bottom: 1px solid {TOK["muted"]};
      text-overflow: ellipsis;
      overflow: hidden;
      white-space: nowrap;
    }}
    .table-common th {{ background: {TOK["bg2"]}; font-weight: 600; }}
    @media (max-width: 600px) {{
      .table-common th, .table-common td {{ padding: 6px 8px; font-size: 13px; }}
    }}

    /* Cards */
    .card {{
      background: {TOK["bg2"]};
      border-radius: 12px;
      padding: 14px 16px;
      border: 1px solid {TOK["muted2"]};
    }}

    /* Plotly: denser mobile */
    @media (max-width: 900px) {{
      .js-plotly-plot .plotly .modebar {{ display: none !important; }}
      .plot-container {{ margin: 0 !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# -------------------- Plotly figure factory --------------------
def make_fig(title: Optional[str]=None, **kwargs) -> go.Figure:
    tpl = "plotly_dark" if IS_DARK else "plotly_white"
    fig = go.Figure(**kwargs)
    fig.update_layout(
        template=tpl,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TOK["text"]),
        title=title or "",
        margin=dict(l=10, r=10, t=56, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True, tickformat=",~s")  # 300k / 3M
    return fig
