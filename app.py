import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="My Portfolio",
    page_icon="📈",
    layout="wide",
)

# ─────────────────────────────────────────────
# PASSWORD PROTECTION
# Password stored in Streamlit secrets — never hardcoded.
# Streamlit Cloud: App Settings → Secrets → add:
#   APP_PASSWORD = "your_password_here"
# Local dev: create .streamlit/secrets.toml with same line.
# ─────────────────────────────────────────────
def check_password():
    """Returns True if the user has entered the correct password."""
    correct_password = st.secrets.get("APP_PASSWORD", "")

    if not correct_password:
        st.error("⚠️ APP_PASSWORD not set in Streamlit secrets. Please configure it.")
        st.stop()

    if st.session_state.get("authenticated"):
        return True

    # ── Login screen ──
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap');
    .login-wrap {
        max-width: 380px; margin: 10vh auto; padding: 40px 36px;
        background: #161b22; border: 1px solid #30363d; border-radius: 16px;
        text-align: center;
    }
    .login-icon  { font-size: 2.8rem; margin-bottom: 8px; }
    .login-title {
        font-family: "IBM Plex Mono", monospace;
        font-size: 1.3rem; font-weight: 600; color: #58a6ff; margin-bottom: 4px;
    }
    .login-sub { color: #8b949e; font-size: 0.82rem; margin-bottom: 24px; }
    .stButton > button {
        background: #238636 !important; color: white !important;
        border: none !important; border-radius: 8px !important;
        font-family: "IBM Plex Mono", monospace !important;
        font-weight: 600 !important; font-size: 0.9rem !important;
    }
    .stButton > button:hover { background: #2ea043 !important; }
    </style>
    <div class="login-wrap">
        <div class="login-icon">🔒</div>
        <div class="login-title">Portfolio Tracker</div>
        <div class="login-sub">Enter password to continue</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd   = st.text_input("Password", type="password",
                              label_visibility="collapsed",
                              placeholder="Enter password…")
        login = st.button("🔓 Unlock", use_container_width=True)

        if login or pwd:
            if pwd == correct_password:
                st.session_state["authenticated"] = True
                st.rerun()
            elif pwd:
                st.error("❌ Incorrect password.")

    return False

if not check_password():
    st.stop()


# ─────────────────────────────────────────────
# PORTFOLIO  (Equity_Summary_Details 20-03-2026)
# Yahoo Finance BSE format : SYMBOL.BO
# Yahoo Finance NSE format : SYMBOL.NS
#
# Special securities:
#   SBI ETF Gold     → SETFGOLD.BO  (ETF, trades on BSE)
#   2.50% Gold Bonds → Not listed on Yahoo Finance; tracked manually below.
# ─────────────────────────────────────────────
PORTFOLIO = [
    # name                            symbol           shares   buy_price
    {"name": "ITC Hotels Ltd",        "symbol": "ITCHOTEL.BO",  "shares":   10, "buy_price":  580.95},
    {"name": "ITC Ltd",               "symbol": "ITC.BO",       "shares":  200, "buy_price":  391.80},
    {"name": "Indian Oil Corp",       "symbol": "IOC.BO",       "shares":  125, "buy_price":  135.83},
    {"name": "J&K Bank",              "symbol": "J&KBANK.BO",   "shares":  200, "buy_price":   99.57},
    {"name": "LIC of India",          "symbol": "LICI.BO",      "shares":   15, "buy_price":  904.00},
    {"name": "Larsen & Toubro",       "symbol": "LT.BO",        "shares":   10, "buy_price": 3641.52},
    {"name": "Punjab National Bank",  "symbol": "PNB.BO",       "shares":  160, "buy_price":   73.42},
    {"name": "SBI Cards",             "symbol": "SBICARD.BO",   "shares":   63, "buy_price":  753.84},
    {"name": "SBI ETF Gold",          "symbol": "SETFGOLD.BO",  "shares": 1500, "buy_price":   47.79},
    {"name": "SBI Life Insurance",    "symbol": "SBILIFE.BO",   "shares":   49, "buy_price":  700.00},
    {"name": "SAIL",                  "symbol": "SAIL.BO",      "shares":  500, "buy_price":   87.31},
    {"name": "Tejas Networks",        "symbol": "TEJASNET.BO",  "shares":   50, "buy_price":  330.32},
]

# Gold Bonds — not on Yahoo Finance; tracked at fixed purchase value
# (Update current_price manually when you know the redemption NAV)
GOLD_BONDS = [
    {"name": "2.50% Gold Bonds 2029 SR-XII",
     "shares": 2, "buy_price": 4662.00, "current_price": 4662.00,
     "note": "SGB — not on Yahoo Finance. Price fixed at purchase cost. Update manually."},
]

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }

.header-box {
    background: linear-gradient(135deg, #1a2332 0%, #0d1117 100%);
    border: 1px solid #30363d; border-radius: 12px;
    padding: 28px 32px; margin-bottom: 24px;
}
.header-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.8rem; font-weight: 600; color: #58a6ff; margin: 0;
}
.header-sub { color: #8b949e; font-size: 0.85rem; margin-top: 4px; font-family: 'IBM Plex Mono', monospace; }

.summary-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 10px; padding: 20px 24px; text-align: center; height: 100%;
}
.summary-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #8b949e; margin-bottom: 6px; }
.summary-value { font-family: 'IBM Plex Mono', monospace; font-size: 1.5rem; font-weight: 600; color: #e6edf3; }
.summary-value.positive { color: #3fb950; }
.summary-value.negative { color: #f85149; }

.stButton > button {
    background: #238636; color: white; border: none; border-radius: 8px;
    font-family: 'IBM Plex Mono', monospace; font-weight: 600;
    padding: 10px 28px; font-size: 0.9rem; transition: background 0.2s;
}
.stButton > button:hover { background: #2ea043; }

.warn-box {
    background: #2d2200; border: 1px solid #d29922; border-radius: 8px;
    padding: 8px 14px; font-size: 0.8rem; color: #d29922;
    font-family: 'IBM Plex Mono', monospace; margin: 4px 0;
}
.error-box {
    background: #2d1b1b; border: 1px solid #f85149; border-radius: 8px;
    padding: 8px 14px; font-size: 0.8rem; color: #f85149;
    font-family: 'IBM Plex Mono', monospace; margin: 4px 0;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def fetch_yf_prices(symbol: str, days: int = 10):
    """
    Returns (prices_list_latest_first, error_string).
    prices[0] = most recent closing price.
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=f"{days}d", auto_adjust=True)
        if hist.empty:
            return [], f"No data returned for `{symbol}` — symbol may be wrong or delisted."
        closes = hist["Close"].dropna().tolist()
        closes.reverse()          # latest first
        return closes, ""
    except Exception as e:
        return [], str(e)


def analyze_trend(prices):
    if len(prices) < 2:
        return "➡ Flat"
    latest    = prices[0]
    week_old  = prices[min(6, len(prices) - 1)]
    three_ago = prices[min(2, len(prices) - 1)]
    week_chg  = (latest - week_old)  / week_old  * 100
    mom_chg   = (latest - three_ago) / three_ago * 100
    if week_chg > 1.5 and mom_chg > 0.5:
        return "🔺 Increasing"
    elif week_chg > 0 or mom_chg > 0:
        return "🔸 Weak Increasing"
    elif week_chg < -1.5 and mom_chg < -0.5:
        return "🔻 Decreasing"
    else:
        return "➡ Flat"


def get_position(buy_price, current_price):
    return "✅ Profitable" if current_price >= buy_price else "🔴 Loss"


def format_inr(value):
    sign = "-" if value < 0 else ""
    return f"{sign}₹{abs(value):,.2f}"


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <p class="header-title">📈 My Stock Portfolio</p>
    <p class="header-sub">BSE · Yahoo Finance · Live EOD Data · No API Key Required</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📋 Holdings")
    st.markdown("**Equity (Yahoo Finance)**")
    for s in PORTFOLIO:
        st.markdown(f"- {s['name']}  `{s['symbol']}`")
    st.markdown("**Fixed / Manual**")
    for g in GOLD_BONDS:
        st.markdown(f"- {g['name']}")
    st.markdown("---")
    st.markdown(
        "<small style='color:#8b949e'>Data: Yahoo Finance (BSE EOD)<br>"
        "Refresh loads all tickers in ~5–10 seconds.</small>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# REFRESH BUTTON + STATE
# ─────────────────────────────────────────────
col_btn, _ = st.columns([1, 5])
with col_btn:
    refresh = st.button("🔄 Refresh Data")

if "rows" not in st.session_state:
    st.session_state.rows = None
    st.session_state.fetch_time = None
    st.session_state.errors = []
    st.session_state.warnings = []

# ─────────────────────────────────────────────
# DATA FETCH
# ─────────────────────────────────────────────
if refresh or st.session_state.rows is None:
    rows    = []
    errors  = []
    warnings = []

    total_stocks = len(PORTFOLIO)
    progress = st.progress(0, text="Fetching live prices from Yahoo Finance…")

    # ── Live equity tickers ──────────────────
    for i, stock in enumerate(PORTFOLIO):
        progress.progress(
            (i + 1) / total_stocks,
            text=f"Fetching {stock['name']} ({stock['symbol']})…",
        )
        prices, err = fetch_yf_prices(stock["symbol"], days=10)

        if err:
            errors.append(f"**{stock['name']}** (`{stock['symbol']}`): {err}")
            continue
        if not prices:
            errors.append(f"**{stock['name']}**: Empty price list.")
            continue

        current_price  = prices[0]
        buy_price      = stock["buy_price"]
        shares         = stock["shares"]
        total_invested = buy_price  * shares
        current_value  = current_price * shares
        net_profit     = current_value - total_invested

        rows.append({
            "Stock":             stock["name"],
            "Shares":            shares,
            "Buy Price (₹)":     round(buy_price, 2),
            "Current Price (₹)": round(current_price, 2),
            "Invested (₹)":      round(total_invested, 2),
            "Value (₹)":         round(current_value, 2),
            "Net P&L (₹)":       round(net_profit, 2),
            "Trend":             analyze_trend(prices),
            "Position":          get_position(buy_price, current_price),
            "_sort":             net_profit,
        })

    # ── Gold Bonds (manual / fixed) ──────────
    for g in GOLD_BONDS:
        cp  = g["current_price"]
        bp  = g["buy_price"]
        qty = g["shares"]
        net = (cp - bp) * qty
        rows.append({
            "Stock":             g["name"],
            "Shares":            qty,
            "Buy Price (₹)":     round(bp, 2),
            "Current Price (₹)": round(cp, 2),
            "Invested (₹)":      round(bp * qty, 2),
            "Value (₹)":         round(cp * qty, 2),
            "Net P&L (₹)":       round(net, 2),
            "Trend":             "📌 Manual",
            "Position":          get_position(bp, cp),
            "_sort":             net,
        })
        warnings.append(
            f"**{g['name']}**: {g['note']}"
        )

    progress.empty()

    rows.sort(key=lambda x: x["_sort"], reverse=True)
    for r in rows:
        del r["_sort"]

    st.session_state.rows     = rows
    st.session_state.errors   = errors
    st.session_state.warnings = warnings
    st.session_state.fetch_time = datetime.now().strftime("%d %b %Y, %I:%M %p")

# ─────────────────────────────────────────────
# ALERTS
# ─────────────────────────────────────────────
if st.session_state.warnings:
    with st.expander(f"📌 {len(st.session_state.warnings)} manual / fixed price entries"):
        for w in st.session_state.warnings:
            st.markdown(f'<div class="warn-box">⚠️ {w}</div>', unsafe_allow_html=True)

if st.session_state.errors:
    with st.expander(f"❌ {len(st.session_state.errors)} ticker(s) failed to load"):
        for e in st.session_state.errors:
            st.markdown(f'<div class="error-box">{e}</div>', unsafe_allow_html=True)
        st.markdown("""
**Fixes to try:**
- Wrong symbol → Search on [finance.yahoo.com](https://finance.yahoo.com) and update `PORTFOLIO` in `app.py`
- Delisted / renamed → Update the symbol  
- Network issue → Try again in a moment
""")

rows = st.session_state.rows
if not rows:
    st.error("No data loaded. Check the error details above.")
    st.stop()

# ─────────────────────────────────────────────
# SUMMARY CARDS
# ─────────────────────────────────────────────
total_invested = sum(r["Invested (₹)"] for r in rows)
total_value    = sum(r["Value (₹)"]    for r in rows)
net_total      = total_value - total_invested
pct_change     = (net_total / total_invested * 100) if total_invested else 0
loaded         = sum(1 for r in rows if r["Trend"] != "📌 Manual")

c1, c2, c3, c4, c5 = st.columns(5)
cards = [
    ("Total Invested",  format_inr(total_invested), ""),
    ("Current Value",   format_inr(total_value),    ""),
    ("Net P&L",         format_inr(net_total),       "positive" if net_total >= 0 else "negative"),
    ("Overall Return",  f"{'+'if pct_change>=0 else ''}{pct_change:.2f}%",
                        "positive" if pct_change >= 0 else "negative"),
    ("Stocks Tracked",  f"{loaded} live + {len(GOLD_BONDS)} fixed", ""),
]
for col, (label, value, cls) in zip([c1, c2, c3, c4, c5], cards):
    with col:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-label">{label}</div>
            <div class="summary-value {cls}">{value}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HOLDINGS TABLE
# ─────────────────────────────────────────────
st.markdown("#### 📊 Holdings")

df = pd.DataFrame(rows)

def colour_pnl(val):
    return f"color: {'#3fb950' if val >= 0 else '#f85149'}; font-weight: 600"

def colour_position(val):
    if val == "✅ Profitable":
        return "color: #3fb950"
    elif val == "🔴 Loss":
        return "color: #f85149"
    return ""

styled = (
    df.style
      .map(colour_pnl,       subset=["Net P&L (₹)"])
      .map(colour_position,  subset=["Position"])
      .format({
          "Buy Price (₹)":     "₹{:,.2f}",
          "Current Price (₹)": "₹{:,.2f}",
          "Invested (₹)":      "₹{:,.2f}",
          "Value (₹)":         "₹{:,.2f}",
          "Net P&L (₹)":       lambda v: f"{'+'if v>=0 else ''}₹{v:,.2f}",
      })
      .set_properties(**{
          "background-color": "#161b22",
          "color":            "#e6edf3",
          "border-color":     "#30363d",
          "font-family":      "IBM Plex Mono, monospace",
          "font-size":        "13px",
      })
      .set_table_styles([{"selector": "th", "props": [
          ("background-color", "#0d1117"),
          ("color", "#8b949e"),
          ("font-size", "11px"),
          ("text-transform", "uppercase"),
          ("letter-spacing", "0.08em"),
          ("border-bottom", "1px solid #30363d"),
      ]}])
)
st.dataframe(styled, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# GAINERS / WATCH LIST
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("#### 🏆 Top Gainers")
    gainers = [r for r in rows if r["Net P&L (₹)"] > 0][:4]
    for r in gainers:
        pnl = r["Net P&L (₹)"]
        pct = (pnl / r["Invested (₹)"]) * 100
        st.markdown(
            f"**{r['Stock']}** &nbsp; "
            f"<span style='color:#3fb950;font-family:monospace'>+₹{pnl:,.0f} &nbsp;(+{pct:.1f}%)</span>"
            f" &nbsp; {r['Trend']}",
            unsafe_allow_html=True,
        )
    if not gainers:
        st.markdown("_No gainers in loaded data._")

with col_b:
    st.markdown("#### 🔻 Watch List (Losses)")
    losers = [r for r in reversed(rows) if r["Net P&L (₹)"] < 0][:4]
    for r in losers:
        pnl = r["Net P&L (₹)"]
        pct = (pnl / r["Invested (₹)"]) * 100
        st.markdown(
            f"**{r['Stock']}** &nbsp; "
            f"<span style='color:#f85149;font-family:monospace'>₹{pnl:,.0f} &nbsp;({pct:.1f}%)</span>"
            f" &nbsp; {r['Trend']}",
            unsafe_allow_html=True,
        )
    if not losers:
        st.markdown("_No losses — great portfolio! 🎉_")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
if st.session_state.fetch_time:
    st.markdown(
        f"<small style='color:#8b949e;font-family:monospace'>"
        f"Last updated: {st.session_state.fetch_time} &nbsp;·&nbsp; "
        f"{len(rows)}/{len(PORTFOLIO) + len(GOLD_BONDS)} securities loaded &nbsp;·&nbsp; "
        f"Prices via Yahoo Finance (BSE EOD)</small>",
        unsafe_allow_html=True,
    )
