"""
styles.py — Global CSS styles and helper functions for the SET50 Network app.
Dark premium theme matching the UI mockup.
"""
import streamlit as st
from utils.data_fetcher import SECTOR_COLORS, STAKEHOLDER_COLORS


def inject_global_styles():
    """Inject global CSS styles and Google Fonts."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@400;500;700&display=swap');

        /* ── Global ── */
        [data-testid="stAppViewContainer"] {
            font-family: 'Outfit', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {
            color: #F8FAFC;
        }

        /* ── Banner ── */
        .banner-container {
            background: linear-gradient(135deg, #1E1B4B 0%, #311042 50%, #0F172A 100%);
            border-radius: 16px;
            padding: 32px 40px;
            margin-bottom: 28px;
            border: 1px solid #312E81;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .banner-title {
            font-family: 'Space Grotesk', sans-serif;
            color: #F8FAFC;
            font-size: 2.4rem;
            font-weight: 800;
            margin-bottom: 8px;
        }
        .banner-subtitle {
            color: #94A3B8;
            font-size: 1rem;
        }

        /* ── Section Title ── */
        .section-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.6rem;
            font-weight: 700;
            color: #F8FAFC;
            margin-top: 32px;
            margin-bottom: 16px;
            border-bottom: 2px solid rgba(168, 85, 247, 0.3);
            padding-bottom: 8px;
        }

        /* ── KPI Cards ── */
        .kpi-card {
            background: rgba(30, 41, 59, 0.45);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px;
            padding: 20px 18px;
            text-align: left;
            transition: transform 0.25s ease, border-color 0.25s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .kpi-card:hover {
            transform: translateY(-3px);
            border-color: rgba(168,85,247,0.4);
        }
        .kpi-label {
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 6px;
        }
        .kpi-value {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.8rem;
            font-weight: 800;
            color: #F8FAFC;
            line-height: 1.2;
        }

        /* ── Data Table ── */
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
            table-layout: fixed;
            word-wrap: break-word;
        }
        .styled-table thead th {
            background: rgba(30, 41, 59, 0.6);
            color: #94A3B8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.75rem;
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        .styled-table tbody td {
            padding: 10px 16px;
            color: #E2E8F0;
            border-bottom: 1px solid rgba(255,255,255,0.04);
        }
        .styled-table tbody tr:hover {
            background: rgba(99, 102, 241, 0.08);
        }
        .styled-table tbody td.num {
            text-align: right;
            font-family: 'Space Grotesk', monospace;
            font-weight: 500;
        }

        /* ── Legend ── */
        .legend-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            padding: 14px 0;
            margin-bottom: 8px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.78rem;
            color: #CBD5E1;
        }
        .legend-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
            flex-shrink: 0;
        }

        /* ── Sector Badge ── */
        .sector-badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            cursor: default;
            transition: filter 0.2s;
        }
        .sector-badge:hover {
            filter: brightness(1.2);
        }
        .sector-badge .x-btn {
            margin-left: 4px;
            cursor: pointer;
            font-weight: 400;
            opacity: 0.7;
        }

        /* ── Profiler Panel ── */
        .profiler-panel {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px;
            padding: 20px;
            min-height: 400px;
        }
        .profiler-info {
            background: rgba(99, 102, 241, 0.08);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 8px;
            padding: 14px 16px;
            color: #94A3B8;
            font-size: 0.88rem;
            line-height: 1.5;
        }

        /* ── Footer ── */
        .footer-text {
            font-size: 0.75rem;
            color: #475569;
            margin-top: 8px;
        }
        .footer-text .green-dot {
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #10B981;
            margin-right: 4px;
        }
        .footer-text .red-dot {
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #EF4444;
            margin-right: 4px;
        }

        /* ── PyVis iframe ── */
        .pyvis-container iframe {
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.06);
        }

        /* ── Streamlit overrides ── */
        .stSelectbox label, .stMultiSelect label, .stRadio label {
            color: #94A3B8 !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Helper: KPI Card
# ---------------------------------------------------------------------------
def render_kpi_card(label: str, value: str, color: str = "#3B82F6", font_size: str = None):
    """Render a compact KPI card."""
    style_str = f' style="font-size: {font_size}; word-break: break-word;"' if font_size else ' style="word-break: break-word;"'
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label" style="color:{color};">{label}</div>
            <div class="kpi-value"{style_str}>{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Helper: Legend
# ---------------------------------------------------------------------------
def render_legend(sectors: list[str]):
    """Render a horizontal color legend for sectors + stakeholder types."""
    items_html = ""

    # Sector colors
    for sector in sorted(sectors):
        color = SECTOR_COLORS.get(sector, "#94A3B8")
        items_html += f'<div class="legend-item"><span class="legend-dot" style="background:{color};"></span>{sector}</div>'

    # Stakeholder type colors
    for stype, color in STAKEHOLDER_COLORS.items():
        items_html += f'<div class="legend-item"><span class="legend-dot" style="background:{color};"></span>{stype}</div>'

    st.markdown(
        f'<div class="legend-container">{items_html}</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Helper: Top Connected Table
# ---------------------------------------------------------------------------
def render_top_table(df):
    """Render the top-connected-nodes table with custom HTML styling."""
    if df.empty:
        st.info("No data to display.")
        return

    rows_html = ""
    for _, row in df.iterrows():
        rows_html += f"<tr><td>{row['Node']}</td><td>{row['Type']}</td><td class='num'>{row['Connections']}</td><td class='num'>{row['Centrality']}</td></tr>\n"

    html_content = f"""<table class="styled-table">
<thead>
    <tr>
        <th>Node</th>
        <th>Type</th>
        <th style="text-align:right">Connections</th>
        <th style="text-align:right">Centrality</th>
    </tr>
</thead>
<tbody>
{rows_html}</tbody>
</table>"""

    st.markdown(html_content, unsafe_allow_html=True)
