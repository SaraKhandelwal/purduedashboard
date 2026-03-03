"""
Purdue University Publishing Analytics Dashboard
McKinsey-style executive intelligence tool for university leadership

Author: Analytics Team
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Purdue Publishing Intelligence",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# DESIGN TOKENS — consulting palette
# ─────────────────────────────────────────────
GOLD       = "#C28840"   # Purdue gold
DARK_GOLD  = "#8B5E2A"
BLACK      = "#1A1A1A"
CHARCOAL   = "#2D2D2D"
SLATE      = "#4A5568"
LIGHT_GREY = "#F7F7F7"
MID_GREY   = "#E2E8F0"
WHITE      = "#FFFFFF"
ACCENT_1   = "#2B4C7E"   # deep navy
ACCENT_2   = "#5B8DB8"   # steel blue
ACCENT_3   = "#8FAF6E"   # muted sage
ACCENT_4   = "#C28840"   # gold

PURDUE_PALETTE = [ACCENT_1, GOLD, ACCENT_2, ACCENT_3, CHARCOAL, DARK_GOLD, "#7B8FA1", "#A0866E"]

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  /* ---- Google Fonts ---- */
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400&display=swap');

  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    color: #1A1A1A;
  }

  /* ---- Hide Streamlit chrome ---- */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

  /* ---- Sidebar ---- */
  [data-testid="stSidebar"] {
    background-color: #1A1A1A !important;
  }
  [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stMultiSelect label,
  [data-testid="stSidebar"] .stSlider label { color: #C28840 !important; font-weight: 600; }
  [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #C28840 !important;
  }

  /* ---- KPI Cards ---- */
  .kpi-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #C28840;
    border-radius: 6px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }
  .kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #4A5568;
    margin-bottom: 0.3rem;
  }
  .kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: #1A1A1A;
    line-height: 1.1;
  }
  .kpi-sub {
    font-size: 0.78rem;
    color: #718096;
    margin-top: 0.25rem;
  }
  .kpi-badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    margin-top: 0.3rem;
  }
  .badge-gold { background: #FEF3C7; color: #92400E; }
  .badge-blue { background: #DBEAFE; color: #1E40AF; }
  .badge-green { background: #D1FAE5; color: #065F46; }

  /* ---- Section headers ---- */
  .section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #1A1A1A;
    border-bottom: 2px solid #C28840;
    padding-bottom: 0.4rem;
    margin-top: 0.5rem;
    margin-bottom: 1.2rem;
  }
  .section-sub {
    font-size: 0.88rem;
    color: #4A5568;
    margin-top: -0.8rem;
    margin-bottom: 1rem;
    font-style: italic;
  }

  /* ---- Insight boxes ---- */
  .insight-box {
    background: #FFFBEB;
    border-left: 4px solid #C28840;
    border-radius: 0 6px 6px 0;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
  }
  .insight-box-blue {
    background: #EFF6FF;
    border-left: 4px solid #2B4C7E;
    border-radius: 0 6px 6px 0;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
  }
  .insight-icon { font-size: 1.1rem; margin-right: 0.4rem; }
  .insight-title { font-weight: 600; color: #1A1A1A; margin-bottom: 0.3rem; }
  .insight-text { font-size: 0.85rem; color: #374151; line-height: 1.5; }

  /* ---- Page nav pills ---- */
  .stRadio > div { flex-direction: row; gap: 0.5rem; }
  .stRadio label {
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    padding: 0.3rem 0.9rem;
    cursor: pointer;
    font-size: 0.85rem;
  }

  /* ---- Dividers ---- */
  .subtle-divider {
    border: none;
    border-top: 1px solid #E2E8F0;
    margin: 1.2rem 0;
  }

  /* ---- Watermark header ---- */
  .dash-header {
    background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%);
    padding: 1.2rem 2rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .dash-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #C28840;
  }
  .dash-subtitle {
    font-size: 0.78rem;
    color: #9CA3AF;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .dash-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    color: #6B7280;
    text-align: right;
  }

  /* ---- Table styling ---- */
  .dataframe { font-size: 0.82rem !important; }

  /* ---- Rank badge ---- */
  .rank-1 { color: #B7791F; font-weight: 700; }
  .rank-2 { color: #718096; font-weight: 700; }
  .rank-3 { color: #9C6644; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING & PROCESSING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load and clean both sheets from the Excel workbook."""
    xl = pd.ExcelFile("Dashboard.xlsx")

    # ── Sheet 1: Purdue University ──────────────────
    raw_purdue = pd.read_excel(xl, sheet_name="Purdue University")

    # Column A-B: Publisher Name + Publication count (Scopus-style)
    purdue_scopus = raw_purdue[["Publisher Name", "Publication count"]].dropna()
    purdue_scopus.columns = ["Publisher", "Scopus_Count"]
    purdue_scopus["Scopus_Count"] = pd.to_numeric(purdue_scopus["Scopus_Count"], errors="coerce")
    purdue_scopus = purdue_scopus.dropna().reset_index(drop=True)

    # Column D-E: Publisher Name.1 + Open Alex count
    purdue_openalex = raw_purdue[["Publisher Name.1", "Open alex count"]].dropna()
    purdue_openalex.columns = ["Publisher", "OpenAlex_Count"]
    purdue_openalex["OpenAlex_Count"] = pd.to_numeric(purdue_openalex["OpenAlex_Count"], errors="coerce")
    purdue_openalex = purdue_openalex.dropna().reset_index(drop=True)

    # Column G-H: Top cited publications
    top_cited = raw_purdue[["Publication", "Cited_by_count"]].dropna(subset=["Cited_by_count"])
    top_cited.columns = ["Publication", "Citations"]
    top_cited = top_cited.dropna(subset=["Publication"])
    top_cited["Citations"] = pd.to_numeric(top_cited["Citations"], errors="coerce")
    top_cited = top_cited.dropna().reset_index(drop=True)

    # ── Sheet 2: Purdue Agriculture ─────────────────
    raw_ag = pd.read_excel(xl, sheet_name="Purdue Agriculture")

    # Column A-B: Publisher Name + Publisher count (Scopus)
    ag_scopus = raw_ag[["Publisher Name", "Publisher count"]].dropna()
    ag_scopus.columns = ["Publisher", "Scopus_Count"]
    ag_scopus["Scopus_Count"] = pd.to_numeric(ag_scopus["Scopus_Count"], errors="coerce")
    ag_scopus = ag_scopus.dropna().reset_index(drop=True)

    # Column D-E: Publisher name + Publisher count.1 (OpenAlex)
    ag_openalex = raw_ag[["Publisher name", "Publisher count.1"]].dropna()
    ag_openalex.columns = ["Publisher", "OpenAlex_Count"]
    ag_openalex["OpenAlex_Count"] = pd.to_numeric(ag_openalex["OpenAlex_Count"], errors="coerce")
    ag_openalex = ag_openalex.dropna().reset_index(drop=True)

    return {
        "purdue_scopus": purdue_scopus,
        "purdue_openalex": purdue_openalex,
        "top_cited": top_cited,
        "ag_scopus": ag_scopus,
        "ag_openalex": ag_openalex,
    }


@st.cache_data
def compute_metrics(data):
    """Derive key analytical metrics from raw data."""
    p_s = data["purdue_scopus"]
    p_oa = data["purdue_openalex"]
    a_s = data["ag_scopus"]
    a_oa = data["ag_openalex"]
    tc = data["top_cited"]

    total_purdue_scopus   = int(p_s["Scopus_Count"].sum())
    total_purdue_openalex = int(p_oa["OpenAlex_Count"].sum())
    total_ag_scopus       = int(a_s["Scopus_Count"].sum())
    total_ag_openalex     = int(a_oa["OpenAlex_Count"].sum())

    ag_share_scopus   = round(total_ag_scopus   / total_purdue_scopus   * 100, 1)
    ag_share_openalex = round(total_ag_openalex / total_purdue_openalex * 100, 1)

    top3_purdue = p_s.nlargest(3, "Scopus_Count")["Scopus_Count"].sum()
    concentration_purdue = round(top3_purdue / total_purdue_scopus * 100, 1)

    top3_ag = a_s.nlargest(3, "Scopus_Count")["Scopus_Count"].sum()
    concentration_ag = round(top3_ag / total_ag_scopus * 100, 1)

    n_publishers_purdue = len(p_s)
    n_publishers_ag     = len(a_s)

    max_cited = tc["Citations"].max()
    top_cited_pub = tc.loc[tc["Citations"].idxmax(), "Publication"]

    return {
        "total_purdue_scopus":   total_purdue_scopus,
        "total_purdue_openalex": total_purdue_openalex,
        "total_ag_scopus":       total_ag_scopus,
        "total_ag_openalex":     total_ag_openalex,
        "ag_share_scopus":       ag_share_scopus,
        "ag_share_openalex":     ag_share_openalex,
        "concentration_purdue":  concentration_purdue,
        "concentration_ag":      concentration_ag,
        "n_publishers_purdue":   n_publishers_purdue,
        "n_publishers_ag":       n_publishers_ag,
        "max_cited":             max_cited,
        "top_cited_pub":         top_cited_pub,
    }

# ─────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="IBM Plex Sans", color="#1A1A1A", size=12),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor="white", bordercolor="#E2E8F0", borderwidth=1),
    xaxis=dict(gridcolor="#F0F0F0", linecolor="#E2E8F0"),
    yaxis=dict(gridcolor="#F0F0F0", linecolor="#E2E8F0"),
)

def apply_layout(fig, title="", **kwargs):
    fig.update_layout(title=dict(text=title, font=dict(size=14, family="IBM Plex Sans", color="#1A1A1A")),
                      **PLOTLY_LAYOUT, **kwargs)
    return fig


def kpi_card(label, value, sub="", badge_text="", badge_class="badge-gold"):
    badge_html = f'<span class="kpi-badge {badge_class}">{badge_text}</span>' if badge_text else ""
    return f"""
    <div class="kpi-card">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-sub">{sub}</div>
      {badge_html}
    </div>"""


def insight_box(title, text, blue=False):
    cls = "insight-box-blue" if blue else "insight-box"
    icon = "🔵" if blue else "💡"
    return f"""
    <div class="{cls}">
      <div class="insight-title"><span class="insight-icon">{icon}</span>{title}</div>
      <div class="insight-text">{text}</div>
    </div>"""

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
try:
    data    = load_data()
    metrics = compute_metrics(data)
except Exception as e:
    st.error(f"⚠️ Error loading data: {e}")
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏛️ Purdue Publishing\nIntelligence Dashboard")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["Executive Summary", "Purdue Overview", "Agriculture Deep Dive", "Comparative Analytics"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### Filters")

    # Top-N slider
    top_n = st.slider("Top N Publishers", min_value=5, max_value=30, value=15, step=5)

    # Source toggle
    source = st.selectbox("Data Source", ["Scopus", "OpenAlex", "Both"])

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem; color:#6B7280; line-height:1.5;'>"
        "Data sourced from Scopus &amp; OpenAlex.<br>"
        "Analysis covers Purdue University and its Agriculture sub-portfolio."
        "</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# DASHBOARD HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div>
    <div class="dash-title">Purdue University Publishing Intelligence</div>
    <div class="dash-subtitle">Executive Analytics · Academic Publishing Portfolio</div>
  </div>
  <div class="dash-logo">
    Purdue University<br>
    <span style="color:#C28840;">Analytics &amp; Insights</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE 1: EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════
if page == "Executive Summary":
    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Institutional publishing performance at a glance</div>', unsafe_allow_html=True)

    # ── KPI Row ─────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card(
            "Total Purdue Publications",
            f"{metrics['total_purdue_scopus']:,}",
            sub=f"Scopus indexed publishers: {metrics['n_publishers_purdue']}",
            badge_text="Scopus", badge_class="badge-blue"
        ), unsafe_allow_html=True)

    with c2:
        st.markdown(kpi_card(
            "OpenAlex Publications",
            f"{metrics['total_purdue_openalex']:,}",
            sub="Cross-validated with OpenAlex registry",
            badge_text="OpenAlex", badge_class="badge-blue"
        ), unsafe_allow_html=True)

    with c3:
        st.markdown(kpi_card(
            "Agriculture Publications",
            f"{metrics['total_ag_scopus']:,}",
            sub=f"{metrics['n_publishers_ag']} unique Ag publishers (Scopus)",
            badge_text=f"{metrics['ag_share_scopus']}% of total", badge_class="badge-gold"
        ), unsafe_allow_html=True)

    with c4:
        st.markdown(kpi_card(
            "Peak Citation Impact",
            f"{metrics['max_cited']:,}",
            sub="Citations on highest-impact publication",
            badge_text="Top Cited", badge_class="badge-green"
        ), unsafe_allow_html=True)

    st.markdown('<hr class="subtle-divider"/>', unsafe_allow_html=True)

    # ── Publisher Concentration Row ──────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card(
            "Publisher Concentration (Purdue)",
            f"{metrics['concentration_purdue']}%",
            sub="Share of top-3 publishers in total output",
            badge_text="High Concentration", badge_class="badge-gold"
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card(
            "Publisher Concentration (Ag)",
            f"{metrics['concentration_ag']}%",
            sub="Share of top-3 Ag publishers in Ag output",
            badge_text="High Concentration", badge_class="badge-gold"
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card(
            "Ag Share (OpenAlex)",
            f"{metrics['ag_share_openalex']}%",
            sub="Agriculture as % of Purdue total (OpenAlex)",
            badge_text="Strategic Unit", badge_class="badge-blue"
        ), unsafe_allow_html=True)
    with c4:
        scopus_oa_delta = round(
            (metrics['total_purdue_scopus'] - metrics['total_purdue_openalex'])
            / metrics['total_purdue_scopus'] * 100, 1
        )
        st.markdown(kpi_card(
            "Scopus vs OpenAlex Gap",
            f"{abs(scopus_oa_delta)}%",
            sub="Coverage differential between databases",
            badge_text="Indexing Gap", badge_class="badge-blue"
        ), unsafe_allow_html=True)

    st.markdown('<hr class="subtle-divider"/>', unsafe_allow_html=True)

    # ── Insight Narrative ────────────────────────
    st.markdown("#### Strategic Insights")
    col_i1, col_i2 = st.columns(2)

    with col_i1:
        st.markdown(insight_box(
            "Publisher Dominance Risk",
            f"The top 3 publishers account for <strong>{metrics['concentration_purdue']}%</strong> of all Purdue Scopus publications. "
            "This level of concentration — primarily driven by Elsevier, Springer Nature, and Wiley — signals structural dependency on a narrow set of commercial publishers. "
            "Leadership should monitor open-access alternatives actively."
        ), unsafe_allow_html=True)

        st.markdown(insight_box(
            "Agriculture's Strategic Weight",
            f"Agriculture contributes <strong>{metrics['ag_share_scopus']}%</strong> of total Purdue publications (Scopus). "
            "Given Purdue's land-grant mission, this share reflects the unit's research intensity. "
            "Benchmarking against peer institutions could reveal whether this is above or below expectation."
        ), unsafe_allow_html=True)

    with col_i2:
        st.markdown(insight_box(
            "Database Coverage Gap",
            f"Scopus indexes <strong>{metrics['total_purdue_scopus']:,}</strong> Purdue publications versus "
            f"<strong>{metrics['total_purdue_openalex']:,}</strong> in OpenAlex — a gap of {abs(scopus_oa_delta)}%. "
            "This discrepancy suggests a non-trivial portion of Purdue's research output is only captured in one database, "
            "which has implications for citation analysis and research assessment exercises.",
            blue=True
        ), unsafe_allow_html=True)

        st.markdown(insight_box(
            "Citation Impact Signal",
            f"The highest-cited Purdue publication recorded <strong>{metrics['max_cited']:,} citations</strong>. "
            "The citation distribution is heavily right-skewed, with a small number of publications generating outsized impact — "
            "a pattern consistent with elite research universities. Ag publications show distinct citation profiles worth isolating.",
            blue=True
        ), unsafe_allow_html=True)

    st.markdown('<hr class="subtle-divider"/>', unsafe_allow_html=True)

    # ── Summary charts in executive summary ─────
    col_l, col_r = st.columns([1.2, 1])

    with col_l:
        st.markdown("##### Top 10 Publishers — Purdue University (Scopus)")
        top10 = data["purdue_scopus"].nlargest(10, "Scopus_Count").sort_values("Scopus_Count")
        fig = go.Figure(go.Bar(
            x=top10["Scopus_Count"], y=top10["Publisher"],
            orientation="h",
            marker=dict(
                color=top10["Scopus_Count"],
                colorscale=[[0, "#E8EAF0"], [1, ACCENT_1]],
                showscale=False
            ),
            text=top10["Scopus_Count"].apply(lambda x: f"{x:,.0f}"),
            textposition="outside",
        ))
        apply_layout(fig, height=360)
        fig.update_layout(xaxis_title="Publications", yaxis_title="", yaxis=dict(tickfont=dict(size=10)))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("##### Purdue vs Agriculture — Publisher Landscape")
        categories = ["Purdue Total", "Agriculture"]
        scopus_vals = [metrics["total_purdue_scopus"], metrics["total_ag_scopus"]]
        oa_vals = [metrics["total_purdue_openalex"], metrics["total_ag_openalex"]]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Scopus", x=categories, y=scopus_vals,
                              marker_color=ACCENT_1, text=scopus_vals,
                              texttemplate="%{text:,}", textposition="outside"))
        fig2.add_trace(go.Bar(name="OpenAlex", x=categories, y=oa_vals,
                              marker_color=GOLD, text=oa_vals,
                              texttemplate="%{text:,}", textposition="outside"))
        apply_layout(fig2, height=360, barmode="group")
        fig2.update_layout(yaxis_title="Publications", legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# PAGE 2: PURDUE OVERVIEW
# ═══════════════════════════════════════════════════════════
elif page == "Purdue Overview":
    st.markdown('<div class="section-header">Purdue Publishers — Full Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Comprehensive view of Purdue University\'s publishing portfolio across all disciplines</div>', unsafe_allow_html=True)

    # ── Source selection ─────────────────────────
    if source == "Scopus":
        df_pub = data["purdue_scopus"].rename(columns={"Scopus_Count": "Count"})
        src_label = "Scopus"
    elif source == "OpenAlex":
        df_pub = data["purdue_openalex"].rename(columns={"OpenAlex_Count": "Count"})
        src_label = "OpenAlex"
    else:
        # Merge both
        merged = pd.merge(
            data["purdue_scopus"], data["purdue_openalex"],
            on="Publisher", how="outer"
        ).fillna(0)
        merged["Count"] = merged["Scopus_Count"] + merged["OpenAlex_Count"]
        df_pub = merged[["Publisher", "Count"]]
        src_label = "Combined"

    df_pub = df_pub.sort_values("Count", ascending=False).reset_index(drop=True)

    # ── KPI mini-row ─────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(kpi_card(
            f"Total Publications ({src_label})",
            f"{int(df_pub['Count'].sum()):,}",
            sub=f"Across {len(df_pub)} publishers"
        ), unsafe_allow_html=True)
    with c2:
        top_pub = df_pub.iloc[0]
        st.markdown(kpi_card(
            "Leading Publisher",
            top_pub["Publisher"][:22] + ("…" if len(top_pub["Publisher"]) > 22 else ""),
            sub=f"{int(top_pub['Count']):,} publications",
            badge_text="#1 Rank", badge_class="badge-gold"
        ), unsafe_allow_html=True)
    with c3:
        median_pub = df_pub["Count"].median()
        st.markdown(kpi_card(
            "Median Publisher Output",
            f"{int(median_pub):,}",
            sub="50th percentile of publishers by count",
            badge_text="Benchmark", badge_class="badge-blue"
        ), unsafe_allow_html=True)

    st.markdown('<hr class="subtle-divider"/>', unsafe_allow_html=True)

    # ── Top N Ranked Bar ─────────────────────────
    tab1, tab2, tab3 = st.tabs(["📊 Ranked Publishers", "🎯 Concentration Analysis", "📋 Citations Intelligence"])

    with tab1:
        top_df = df_pub.head(top_n).sort_values("Count")
        colors = [GOLD if i == len(top_df) - 1 else ACCENT_1 for i in range(len(top_df))]

        fig = go.Figure(go.Bar(
            x=top_df["Count"], y=top_df["Publisher"],
            orientation="h",
            marker_color=colors,
            text=top_df["Count"].apply(lambda x: f"{x:,.0f}"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Publications: %{x:,}<extra></extra>",
        ))
        apply_layout(fig, title=f"Top {top_n} Purdue Publishers by Publication Count ({src_label})", height=max(350, top_n * 28))
        fig.update_layout(xaxis_title="Publication Count", yaxis=dict(tickfont=dict(size=10)))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(insight_box(
            "Publisher Landscape Insight",
            f"Elsevier BV dominates the Purdue publishing portfolio with a commanding lead. "
            f"The top {min(5, top_n)} publishers collectively account for "
            f"{round(df_pub.head(5)['Count'].sum() / df_pub['Count'].sum() * 100, 1)}% of total output. "
            "This level of market concentration in academic publishing warrants monitoring as open-access mandates evolve."
        ), unsafe_allow_html=True)

    with tab2:
        # Cumulative concentration curve
        df_sorted = df_pub.sort_values("Count", ascending=False).reset_index(drop=True)
        df_sorted["Cumulative"] = df_sorted["Count"].cumsum()
        df_sorted["Cumulative_Pct"] = df_sorted["Cumulative"] / df_sorted["Count"].sum() * 100
        df_sorted["Publisher_Rank"] = df_sorted.index + 1

        fig_conc = go.Figure()
        fig_conc.add_trace(go.Scatter(
            x=df_sorted["Publisher_Rank"], y=df_sorted["Cumulative_Pct"],
            mode="lines", fill="tozeroy",
            line=dict(color=ACCENT_1, width=2.5),
            fillcolor="rgba(43,76,126,0.1)",
            name="Cumulative Share",
            hovertemplate="Publisher Rank %{x}<br>Cumulative Share: %{y:.1f}%<extra></extra>"
        ))
        # Reference lines
        for pct_target, label_text in [(50, "50%"), (80, "80%"), (95, "95%")]:
            idx_hit = (df_sorted["Cumulative_Pct"] >= pct_target).idxmax() + 1
            fig_conc.add_vline(x=idx_hit, line_dash="dot", line_color=GOLD, line_width=1.5)
            fig_conc.add_annotation(x=idx_hit, y=pct_target, text=f"{pct_target}% at rank {idx_hit}",
                                    showarrow=True, arrowhead=2, arrowcolor=GOLD,
                                    font=dict(size=10, color=DARK_GOLD), bgcolor="white",
                                    bordercolor=GOLD, borderwidth=1)

        apply_layout(fig_conc, title="Publisher Concentration Curve (Cumulative Share)", height=380)
        fig_conc.update_layout(xaxis_title="Publisher Rank", yaxis_title="Cumulative Publication Share (%)")
        st.plotly_chart(fig_conc, use_container_width=True)

        # Pareto insight
        top5_share = round(df_pub.head(5)["Count"].sum() / df_pub["Count"].sum() * 100, 1)
        top10_share = round(df_pub.head(10)["Count"].sum() / df_pub["Count"].sum() * 100, 1)
        st.markdown(insight_box(
            "Pareto Analysis",
            f"The top 5 publishers represent <strong>{top5_share}%</strong> of Purdue's total output, "
            f"and the top 10 represent <strong>{top10_share}%</strong>. "
            "This concentration curve reveals a classic power-law distribution in academic publishing — "
            "a small number of major commercial publishers capture the vast majority of institutional output. "
            "This has significant implications for library budgeting and open-access transition strategies.",
            blue=True
        ), unsafe_allow_html=True)

    with tab3:
        st.markdown("##### Highest-Cited Publications — Purdue University")
        tc_df = data["top_cited"].dropna().nlargest(top_n, "Citations").reset_index(drop=True)
        tc_df["Rank"] = tc_df.index + 1
        tc_df["Citations_fmt"] = tc_df["Citations"].apply(lambda x: f"{int(x):,}")
        tc_df["Publication_short"] = tc_df["Publication"].str[:80] + tc_df["Publication"].apply(
            lambda x: "…" if len(str(x)) > 80 else "")

        fig_cit = go.Figure(go.Bar(
            x=tc_df["Citations"], y=tc_df["Publication_short"],
            orientation="h",
            marker=dict(color=tc_df["Citations"], colorscale=[[0, "#D4E6F1"], [1, ACCENT_1]], showscale=False),
            text=tc_df["Citations_fmt"],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Citations: %{x:,}<extra></extra>",
        ))
        apply_layout(fig_cit, title=f"Top {top_n} Publications by Citation Count", height=max(380, top_n * 30))
        fig_cit.update_layout(xaxis_title="Total Citations", yaxis=dict(tickfont=dict(size=9)))
        st.plotly_chart(fig_cit, use_container_width=True)

        col_stat1, col_stat2, col_stat3 = st.columns(3)
        with col_stat1:
            st.metric("Total Citations (Top Publications)", f"{int(tc_df['Citations'].sum()):,}")
        with col_stat2:
            st.metric("Mean Citations (Top Publications)", f"{int(tc_df['Citations'].mean()):,}")
        with col_stat3:
            st.metric("Median Citations", f"{int(tc_df['Citations'].median()):,}")


# ═══════════════════════════════════════════════════════════
# PAGE 3: AGRICULTURE DEEP DIVE
# ═══════════════════════════════════════════════════════════
elif page == "Agriculture Deep Dive":
    st.markdown('<div class="section-header">Agriculture — Deep Dive Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Granular examination of Purdue\'s Agriculture publishing portfolio and its competitive dynamics</div>', unsafe_allow_html=True)

    if source == "Scopus":
        df_ag = data["ag_scopus"].rename(columns={"Scopus_Count": "Count"})
        df_pu = data["purdue_scopus"].rename(columns={"Scopus_Count": "Count"})
        src_label = "Scopus"
    elif source == "OpenAlex":
        df_ag = data["ag_openalex"].rename(columns={"OpenAlex_Count": "Count"})
        df_pu = data["purdue_openalex"].rename(columns={"OpenAlex_Count": "Count"})
        src_label = "OpenAlex"
    else:
        m_ag = pd.merge(data["ag_scopus"], data["ag_openalex"], on="Publisher", how="outer").fillna(0)
        m_ag["Count"] = m_ag["Scopus_Count"] + m_ag["OpenAlex_Count"]
        df_ag = m_ag[["Publisher", "Count"]]
        m_pu = pd.merge(data["purdue_scopus"], data["purdue_openalex"], on="Publisher", how="outer").fillna(0)
        m_pu["Count"] = m_pu["Scopus_Count"] + m_pu["OpenAlex_Count"]
        df_pu = m_pu[["Publisher", "Count"]]
        src_label = "Combined"

    df_ag = df_ag.sort_values("Count", ascending=False).reset_index(drop=True)
    total_ag  = int(df_ag["Count"].sum())
    total_pu  = int(df_pu["Count"].sum())
    ag_share  = round(total_ag / total_pu * 100, 1)
    n_ag_pub  = len(df_ag)

    # ── KPI Row ─────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("Ag Publications", f"{total_ag:,}",
                             sub=f"{n_ag_pub} unique publishers", badge_text="Agriculture", badge_class="badge-green"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("Ag Share of Purdue", f"{ag_share}%",
                             sub="Agriculture's contribution to total output", badge_text=src_label, badge_class="badge-blue"), unsafe_allow_html=True)
    with c3:
        top3_ag_share = round(df_ag.head(3)["Count"].sum() / total_ag * 100, 1)
        st.markdown(kpi_card("Top-3 Concentration (Ag)", f"{top3_ag_share}%",
                             sub="Share held by top 3 publishers", badge_text="Concentration", badge_class="badge-gold"), unsafe_allow_html=True)
    with c4:
        median_ag = df_ag["Count"].median()
        st.markdown(kpi_card("Median Ag Publisher Output", f"{int(median_ag):,}",
                             sub="Typical publisher volume in Ag portfolio"), unsafe_allow_html=True)

    st.markdown('<hr class="subtle-divider"/>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🌾 Ag Publisher Rankings", "🔬 Portfolio Composition", "🔗 Ag vs Purdue Overlap"])

    with tab1:
        top_ag = df_ag.head(top_n).sort_values("Count")
        bar_colors = [ACCENT_3 if i < len(top_ag) - 1 else GOLD for i in range(len(top_ag))]

        fig_ag = go.Figure(go.Bar(
            x=top_ag["Count"], y=top_ag["Publisher"],
            orientation="h",
            marker_color=bar_colors,
            text=top_ag["Count"].apply(lambda x: f"{x:,.0f}"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Ag Publications: %{x:,}<extra></extra>",
        ))
        apply_layout(fig_ag, title=f"Top {top_n} Agriculture Publishers ({src_label})", height=max(350, top_n * 30))
        fig_ag.update_layout(xaxis_title="Publication Count", yaxis=dict(tickfont=dict(size=10)))
        st.plotly_chart(fig_ag, use_container_width=True)

        # Key insight
        top1_ag = df_ag.iloc[0]
        top2_ag = df_ag.iloc[1]
        st.markdown(insight_box(
            "Agriculture Publisher Dynamics",
            f"<strong>{top1_ag['Publisher']}</strong> leads the Ag portfolio with "
            f"<strong>{int(top1_ag['Count']):,}</strong> publications, followed by "
            f"<strong>{top2_ag['Publisher']}</strong> at <strong>{int(top2_ag['Count']):,}</strong>. "
            "Unlike the overall Purdue portfolio where Elsevier dominates overwhelmingly, "
            "the Ag portfolio shows a more competitive top tier, with multiple publishers maintaining meaningful share. "
            "This may reflect the interdisciplinary nature of modern agricultural science."
        ), unsafe_allow_html=True)

    with tab2:
        col_l, col_r = st.columns([1, 1])

        with col_l:
            # Treemap of Ag publishers
            ag_tree = df_ag.head(20).copy()
            fig_tree = px.treemap(
                ag_tree, path=["Publisher"], values="Count",
                color="Count",
                color_continuous_scale=[[0, "#E8F5E9"], [0.5, ACCENT_3], [1, ACCENT_1]],
                title=f"Ag Publisher Portfolio — Treemap (Top 20, {src_label})"
            )
            fig_tree.update_layout(**{k: v for k, v in PLOTLY_LAYOUT.items() if k in
                                      ["paper_bgcolor", "plot_bgcolor", "font", "margin"]})
            fig_tree.update_layout(height=380, coloraxis_showscale=False,
                                   title_font=dict(size=13, family="IBM Plex Sans"))
            st.plotly_chart(fig_tree, use_container_width=True)

        with col_r:
            # Distribution by output tier
            def tier(c):
                if c >= 50:   return "High (≥50)"
                elif c >= 10: return "Medium (10–49)"
                elif c >= 3:  return "Low (3–9)"
                else:         return "Marginal (1–2)"

            df_ag_tier = df_ag.copy()
            df_ag_tier["Tier"] = df_ag_tier["Count"].apply(tier)
            tier_counts = df_ag_tier["Tier"].value_counts().reset_index()
            tier_counts.columns = ["Tier", "Publishers"]
            tier_order = ["High (≥50)", "Medium (10–49)", "Low (3–9)", "Marginal (1–2)"]
            tier_counts["Tier"] = pd.Categorical(tier_counts["Tier"], categories=tier_order, ordered=True)
            tier_counts = tier_counts.sort_values("Tier")

            fig_tier = go.Figure(go.Bar(
                x=tier_counts["Tier"], y=tier_counts["Publishers"],
                marker_color=[ACCENT_1, ACCENT_2, ACCENT_3, MID_GREY],
                text=tier_counts["Publishers"], textposition="outside",
            ))
            apply_layout(fig_tier, title="Agriculture Publishers by Output Tier", height=380)
            fig_tier.update_layout(xaxis_title="Output Tier", yaxis_title="# Publishers")
            st.plotly_chart(fig_tier, use_container_width=True)

        # Insight
        high_tier_vol = df_ag_tier[df_ag_tier["Tier"] == "High (≥50)"]["Count"].sum()
        high_tier_n   = (df_ag_tier["Tier"] == "High (≥50)").sum()
        st.markdown(insight_box(
            "Portfolio Depth Analysis",
            f"Only <strong>{high_tier_n}</strong> publisher(s) qualify as 'High Output' (≥50 publications) in the Ag portfolio, "
            f"accounting for <strong>{round(high_tier_vol/total_ag*100,1)}%</strong> of Ag publications. "
            "The long tail of marginal publishers (1–2 publications each) indicates that a significant portion of Ag research "
            "is scattered across niche or specialist outlets — which is typical for interdisciplinary fields like food systems, "
            "soil science, and sustainable agriculture.",
            blue=True
        ), unsafe_allow_html=True)

    with tab3:
        # Find publishers in both Purdue overall and Ag
        pu_pubs = set(df_pu["Publisher"].str.lower())
        ag_pubs = set(df_ag["Publisher"].str.lower())
        overlap = pu_pubs & ag_pubs
        ag_only = ag_pubs - pu_pubs

        st.markdown(f"""
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem; margin-bottom:1rem;">
          <div class="kpi-card">
            <div class="kpi-label">Shared Publishers</div>
            <div class="kpi-value" style="font-size:1.8rem;">{len(overlap)}</div>
            <div class="kpi-sub">In both Purdue & Ag portfolios</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Ag-Exclusive Publishers</div>
            <div class="kpi-value" style="font-size:1.8rem;">{len(ag_only)}</div>
            <div class="kpi-sub">Only in Agriculture sub-portfolio</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Overlap Rate</div>
            <div class="kpi-value" style="font-size:1.8rem;">{round(len(overlap)/len(ag_pubs)*100,1)}%</div>
            <div class="kpi-sub">Ag publishers also in Purdue total</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Show top Ag-exclusive publishers
        ag_df_lower = df_ag.copy()
        ag_df_lower["pub_lower"] = ag_df_lower["Publisher"].str.lower()
        ag_exclusive_df = ag_df_lower[ag_df_lower["pub_lower"].isin(ag_only)].drop("pub_lower", axis=1)

        if not ag_exclusive_df.empty:
            fig_excl = go.Figure(go.Bar(
                x=ag_exclusive_df.head(15).sort_values("Count", ascending=True)["Count"],
                y=ag_exclusive_df.head(15).sort_values("Count", ascending=True)["Publisher"],
                orientation="h",
                marker_color=ACCENT_3,
                text=ag_exclusive_df.head(15).sort_values("Count", ascending=True)["Count"],
                textposition="outside",
            ))
            apply_layout(fig_excl, title="Ag-Exclusive Publishers (Not in General Purdue Portfolio)", height=380)
            fig_excl.update_layout(xaxis_title="Publications", yaxis=dict(tickfont=dict(size=10)))
            st.plotly_chart(fig_excl, use_container_width=True)

        st.markdown(insight_box(
            "Portfolio Segmentation Finding",
            f"<strong>{round(len(overlap)/len(ag_pubs)*100,1)}%</strong> of Agriculture publishers also appear in the broader Purdue portfolio, "
            "indicating strong integration with mainstream academic publishing channels. "
            f"The <strong>{len(ag_only)}</strong> Ag-exclusive publishers represent specialist outlets — "
            "including agricultural societies, domain-specific university presses, and regional journals — "
            "that cater uniquely to the agricultural research community."
        ), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PAGE 4: COMPARATIVE ANALYTICS
# ═══════════════════════════════════════════════════════════
elif page == "Comparative Analytics":
    st.markdown('<div class="section-header">Comparative Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Side-by-side analysis of Purdue overall versus Agriculture sub-portfolio</div>', unsafe_allow_html=True)

    # Prepare data
    p_s = data["purdue_scopus"].rename(columns={"Scopus_Count": "Count"})
    p_oa = data["purdue_openalex"].rename(columns={"OpenAlex_Count": "Count"})
    a_s = data["ag_scopus"].rename(columns={"Scopus_Count": "Count"})
    a_oa = data["ag_openalex"].rename(columns={"OpenAlex_Count": "Count"})

    # ── Side-by-side top publishers ─────────────
    st.markdown("#### Head-to-Head: Top Publishers by Portfolio")
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("**Purdue University (Scopus)**")
        top_p = p_s.nlargest(top_n, "Count").sort_values("Count")
        fig_p = go.Figure(go.Bar(
            x=top_p["Count"], y=top_p["Publisher"],
            orientation="h",
            marker_color=ACCENT_1,
            text=top_p["Count"].apply(lambda x: f"{x:,.0f}"),
            textposition="outside",
        ))
        apply_layout(fig_p, height=max(320, top_n * 27))
        fig_p.update_layout(yaxis=dict(tickfont=dict(size=9)), xaxis_title="Publications")
        st.plotly_chart(fig_p, use_container_width=True)

    with col_r:
        st.markdown("**Agriculture (Scopus)**")
        top_a = a_s.nlargest(top_n, "Count").sort_values("Count")
        fig_a = go.Figure(go.Bar(
            x=top_a["Count"], y=top_a["Publisher"],
            orientation="h",
            marker_color=ACCENT_3,
            text=top_a["Count"].apply(lambda x: f"{x:,.0f}"),
            textposition="outside",
        ))
        apply_layout(fig_a, height=max(320, top_n * 27))
        fig_a.update_layout(yaxis=dict(tickfont=dict(size=9)), xaxis_title="Publications")
        st.plotly_chart(fig_a, use_container_width=True)

    st.markdown('<hr class="subtle-divider"/>', unsafe_allow_html=True)

    # ── Scopus vs OpenAlex comparison ───────────
    st.markdown("#### Scopus vs OpenAlex: Coverage Comparison by Portfolio")
    col_l, col_r = st.columns([1.2, 1])

    with col_l:
        # Waterfall-style comparison
        labels = ["Purdue Scopus", "Purdue OpenAlex", "Ag Scopus", "Ag OpenAlex"]
        values = [
            p_s["Count"].sum(),
            p_oa["Count"].sum(),
            a_s["Count"].sum(),
            a_oa["Count"].sum(),
        ]
        colors_wf = [ACCENT_1, ACCENT_2, ACCENT_3, GOLD]
        fig_wf = go.Figure(go.Bar(
            x=labels, y=values,
            marker_color=colors_wf,
            text=[f"{v:,}" for v in values],
            textposition="outside",
            hovertemplate="%{x}<br>Publications: %{y:,}<extra></extra>",
        ))
        apply_layout(fig_wf, title="Total Publications by Source & Database", height=380)
        fig_wf.update_layout(yaxis_title="Publications", showlegend=False)
        st.plotly_chart(fig_wf, use_container_width=True)

    with col_r:
        # Coverage gap analysis
        pu_gap  = round((p_s["Count"].sum() - p_oa["Count"].sum()) / p_s["Count"].sum() * 100, 1)
        ag_gap  = round((a_s["Count"].sum() - a_oa["Count"].sum()) / a_s["Count"].sum() * 100, 1)

        gap_data = pd.DataFrame({
            "Portfolio": ["Purdue University", "Agriculture"],
            "Scopus":    [int(p_s["Count"].sum()), int(a_s["Count"].sum())],
            "OpenAlex":  [int(p_oa["Count"].sum()), int(a_oa["Count"].sum())],
        })
        gap_data["Scopus-OA Gap"] = gap_data["Scopus"] - gap_data["OpenAlex"]
        gap_data["Gap %"] = gap_data.apply(lambda r: f"{round(r['Scopus-OA Gap']/r['Scopus']*100,1)}%", axis=1)

        fig_gap = go.Figure()
        fig_gap.add_trace(go.Bar(
            name="Scopus", x=gap_data["Portfolio"], y=gap_data["Scopus"],
            marker_color=ACCENT_1, text=gap_data["Scopus"],
            texttemplate="%{text:,}", textposition="outside"
        ))
        fig_gap.add_trace(go.Bar(
            name="OpenAlex", x=gap_data["Portfolio"], y=gap_data["OpenAlex"],
            marker_color=ACCENT_2, text=gap_data["OpenAlex"],
            texttemplate="%{text:,}", textposition="outside"
        ))
        apply_layout(fig_gap, title="Database Coverage by Portfolio", height=380, barmode="group")
        fig_gap.update_layout(yaxis_title="Publications", legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_gap, use_container_width=True)

    st.markdown('<hr class="subtle-divider"/>', unsafe_allow_html=True)

    # ── Shared Publisher Analysis ────────────────
    st.markdown("#### Publisher Overlap — Shared vs Exclusive")

    merged_compare = pd.merge(
        p_s.rename(columns={"Count": "Purdue"}),
        a_s.rename(columns={"Count": "Agriculture"}),
        on="Publisher", how="outer"
    ).fillna(0)
    merged_compare["In_Both"] = (merged_compare["Purdue"] > 0) & (merged_compare["Agriculture"] > 0)
    shared = merged_compare[merged_compare["In_Both"]].sort_values("Agriculture", ascending=False).head(top_n)

    if not shared.empty:
        fig_shared = make_subplots(specs=[[{"secondary_y": False}]])
        shared_sorted = shared.sort_values("Purdue", ascending=True)
        fig_shared.add_trace(go.Bar(
            x=shared_sorted["Purdue"], y=shared_sorted["Publisher"],
            orientation="h", name="Purdue Total",
            marker_color=ACCENT_1,
        ))
        fig_shared.add_trace(go.Bar(
            x=shared_sorted["Agriculture"], y=shared_sorted["Publisher"],
            orientation="h", name="Agriculture",
            marker_color=ACCENT_3,
        ))
        apply_layout(fig_shared, title=f"Shared Publishers — Purdue vs Agriculture (Top {top_n})",
                     barmode="overlay", height=max(350, top_n * 28))
        fig_shared.update_layout(
            xaxis_title="Publications",
            yaxis=dict(tickfont=dict(size=9)),
            legend=dict(orientation="h", y=-0.12)
        )
        st.plotly_chart(fig_shared, use_container_width=True)

        # Ag capture rate
        shared["Ag_Capture_Rate"] = (shared["Agriculture"] / shared["Purdue"] * 100).round(1)
        shared_display = shared[["Publisher", "Purdue", "Agriculture", "Ag_Capture_Rate"]].sort_values(
            "Ag_Capture_Rate", ascending=False
        ).head(10).reset_index(drop=True)
        shared_display.columns = ["Publisher", "Purdue Total", "Agriculture", "Ag Capture Rate (%)"]

        st.markdown("##### Agriculture Capture Rate by Publisher *(Ag publications as % of total Purdue for that publisher)*")
        st.dataframe(
            shared_display.style
            .format({"Purdue Total": "{:,.0f}", "Agriculture": "{:,.0f}", "Ag Capture Rate (%)": "{:.1f}%"}),
            use_container_width=True,
            hide_index=True
        )

        st.markdown(insight_box(
            "Structural Observation — Capture Rate",
            "The 'Ag Capture Rate' reveals how much of a publisher's Purdue output originates from Agriculture. "
            "Publishers with high capture rates are effectively Agriculture-specialized from Purdue's perspective. "
            "A high capture rate for a major commercial publisher (e.g., Elsevier) signals that Ag researchers are "
            "concentrated in that publisher's journals, creating leverage in institutional licensing negotiations.",
            blue=True
        ), unsafe_allow_html=True)

    st.markdown('<hr class="subtle-divider"/>', unsafe_allow_html=True)

    # ── Final comparative summary table ─────────
    st.markdown("#### Portfolio Comparison Summary")
    summary_data = {
        "Metric": [
            "Total Publications (Scopus)",
            "Total Publications (OpenAlex)",
            "Unique Publishers (Scopus)",
            "Top Publisher",
            "Top Publisher Count",
            "Top-3 Publisher Concentration",
            "Median Publisher Output",
        ],
        "Purdue University": [
            f"{int(p_s['Count'].sum()):,}",
            f"{int(p_oa['Count'].sum()):,}",
            f"{len(p_s)}",
            p_s.nlargest(1,'Count')['Publisher'].values[0][:30] + "…",
            f"{int(p_s['Count'].max()):,}",
            f"{round(p_s.nlargest(3,'Count')['Count'].sum()/p_s['Count'].sum()*100,1)}%",
            f"{int(p_s['Count'].median()):,}",
        ],
        "Agriculture": [
            f"{int(a_s['Count'].sum()):,}",
            f"{int(a_oa['Count'].sum()):,}",
            f"{len(a_s)}",
            a_s.nlargest(1,'Count')['Publisher'].values[0][:30] + "…",
            f"{int(a_s['Count'].max()):,}",
            f"{round(a_s.nlargest(3,'Count')['Count'].sum()/a_s['Count'].sum()*100,1)}%",
            f"{int(a_s['Count'].median()):,}",
        ]
    }
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown('<hr class="subtle-divider"/>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; font-size:0.72rem; color:#9CA3AF; padding:0.5rem 0 1rem;">
  Purdue University Publishing Intelligence Dashboard &nbsp;·&nbsp;
  Data: Scopus &amp; OpenAlex &nbsp;·&nbsp;
  Built with Streamlit &amp; Plotly
</div>
""", unsafe_allow_html=True)
