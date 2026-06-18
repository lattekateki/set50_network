"""
data_fetcher.py — Async wrapper for settfex library.
Fetches SET50 stock list, shareholder data, and board of directors.
"""
import asyncio
import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------------------------
# SET50 Symbol List (as of June 2026)
# ---------------------------------------------------------------------------
SET50_SYMBOLS = [
    "ADVANC", "AOT", "AWC", "BANPU", "BBL",
    "BDMS", "BEM", "BGRIM", "BH", "BTS",
    "CBG", "CENTEL", "COM7", "CPALL", "CPF",
    "CPN", "CRC", "DELTA", "EA", "EGCO",
    "GLOBAL", "GPSC", "GULF", "HMPRO", "INTUCH",
    "IVL", "JMART", "KBANK", "KCE", "KTB",
    "KTC", "LH", "MINT", "MTC", "OR",
    "OSP", "PTT", "PTTEP", "PTTGC", "RATCH",
    "SAWAD", "SCB", "SCC", "SCGP", "TIDLOR",
    "TISCO", "TOP", "TRUE", "TTB", "TU",
]

# ---------------------------------------------------------------------------
# Sector color map — matches UI mockup legend
# ---------------------------------------------------------------------------
SECTOR_COLORS = {
    "BANK":    "#EF4444",
    "COMM":    "#6366F1",
    "CONMAT":  "#D97706",
    "ENERG":   "#F97316",
    "ETRON":   "#06B6D4",
    "FIN":     "#3B82F6",
    "FINCIAL": "#3B82F6",
    "FOOD":    "#84CC16",
    "HELTH":   "#FBBF24",
    "HEALTH":  "#FBBF24",
    "ICT":     "#10B981",
    "INSUR":   "#8B5CF6",
    "PETRO":   "#F43F5E",
    "PKG":     "#14B8A6",
    "PROP":    "#EC4899",
    "PROPCON": "#EC4899",
    "RESOURC": "#F43F5E",
    "TECH":    "#06B6D4",
    "TOURISM": "#A855F7",
    "TRANS":   "#64748B",
}

# Stakeholder node type colors
STAKEHOLDER_COLORS = {
    "Shareholder": "#FB923C",
    "Director":    "#14B8A6",
}


def _get_sector_color(sector: str) -> str:
    """Get color for a sector, falling back to a default gray."""
    return SECTOR_COLORS.get(sector, "#94A3B8")


# ---------------------------------------------------------------------------
# Async data fetching
# ---------------------------------------------------------------------------
async def _fetch_stock_info():
    """Fetch full stock list from SET and return a lookup dict for SET50."""
    from settfex.services.set import get_stock_list
    stock_list = await get_stock_list()
    lookup = {}
    for s in stock_list.security_symbols:
        if s.symbol in SET50_SYMBOLS:
            lookup[s.symbol] = {
                "symbol": s.symbol,
                "name_en": s.name_en,
                "name_th": s.name_th,
                "market": s.market,
                "industry": s.industry,
                "sector": s.sector,
            }
    return lookup


async def _fetch_shareholders(symbol: str, lang: str = "en"):
    """Fetch top-5 major shareholders for a symbol."""
    from settfex.services.set import get_shareholder_data
    try:
        data = await get_shareholder_data(symbol, lang=lang)
        results = []
        for sh in data.major_shareholders[:5]:
            results.append({
                "company": symbol,
                "stakeholder_name": sh.name,
                "stakeholder_type": "Shareholder",
                "percent_share": getattr(sh, "percent_of_share", None),
            })
        return results
    except Exception as e:
        st.warning(f"⚠️ Could not fetch shareholders for {symbol}: {e}")
        return []


async def _fetch_directors(symbol: str, lang: str = "en"):
    """Fetch board of directors for a symbol."""
    from settfex.services.set import get_board_of_directors
    try:
        directors = await get_board_of_directors(symbol, lang=lang)
        results = []
        for d in directors:
            positions = ", ".join(d.positions) if d.positions else ""
            results.append({
                "company": symbol,
                "stakeholder_name": d.name,
                "stakeholder_type": "Director",
                "positions": positions,
            })
        return results
    except Exception as e:
        st.warning(f"⚠️ Could not fetch directors for {symbol}: {e}")
        return []


async def _fetch_all(symbols: list[str], mode: str = "shareholders", lang: str = "en"):
    """
    Fetch data for all symbols concurrently.
    mode: "shareholders" | "directors" | "both"
    """
    stock_info = await _fetch_stock_info()

    all_edges = []
    tasks = []

    for sym in symbols:
        if mode in ("shareholders", "both"):
            tasks.append(("sh", sym, _fetch_shareholders(sym, lang)))
        if mode in ("directors", "both"):
            tasks.append(("dir", sym, _fetch_directors(sym, lang)))

    # Run in batches to avoid overwhelming the API
    batch_size = 10
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i + batch_size]
        coros = [t[2] for t in batch]
        results = await asyncio.gather(*coros, return_exceptions=True)
        for (tag, sym, _), result in zip(batch, results):
            if isinstance(result, Exception):
                st.warning(f"⚠️ Error fetching {tag} for {sym}: {result}")
                continue
            all_edges.extend(result)

    return stock_info, all_edges


# ---------------------------------------------------------------------------
# Cached public API (called from Streamlit pages)
# ---------------------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner="🔄 Fetching data from SET...")
def fetch_network_data(
    symbols: tuple,
    mode: str = "shareholders",
    lang: str = "en",
) -> tuple[dict, list[dict]]:
    """
    Cached wrapper around async fetcher.
    Returns (stock_info_dict, edges_list).
    """
    try:
        # In some Streamlit environments, a loop might already be running.
        # asyncio.run() is the safest way to execute async code in a sync function.
        return asyncio.run(_fetch_all(list(symbols), mode, lang))
    except RuntimeError:
        # Fallback if there's an already running event loop in the thread
        import nest_asyncio
        nest_asyncio.apply()
        return asyncio.run(_fetch_all(list(symbols), mode, lang))


def get_available_sectors(stock_info: dict) -> list[str]:
    """Extract sorted unique industry values from stock info."""
    industries = set()
    for info in stock_info.values():
        ind = info.get("industry", "")
        if ind:
            industries.add(ind)
    return sorted(industries)
