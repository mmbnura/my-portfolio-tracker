# 📈 My Stock Portfolio Tracker

A personal stock portfolio dashboard built with **Python + Streamlit**, powered by **Yahoo Finance** — no API key required. Tracks BSE-listed equities, ETFs, and Sovereign Gold Bonds in real time.

---

## ✨ Features

| Feature | Details |
|---|---|
| 📡 Live Prices | Yahoo Finance BSE (EOD) — no API key, no rate limits |
| 🏦 All Securities | Equities, ETFs, and manually-tracked Sovereign Gold Bonds |
| 📊 Holdings Table | Per-share & total values, colour-coded P&L |
| 📈 Trend Analysis | 7-day + 3-day momentum combined signal per stock |
| 💰 Summary Cards | Total Invested · Current Value · Net P&L · Overall Return % |
| 🏆 Gainers / Losers | At-a-glance top performers and underperformers |
| ⚡ Fast Refresh | All 12 live tickers fetched in ~5–10 seconds |
| 🌙 Dark Theme | GitHub-style dark UI with IBM Plex Mono |

---

## 📦 Portfolio Holdings

| Stock | Symbol | Qty | Avg Cost |
|---|---|---|---|
| ITC Hotels Ltd | `ITCHOTEL.BO` | 10 | ₹580.95 |
| ITC Ltd | `ITC.BO` | 200 | ₹391.80 |
| Indian Oil Corp | `IOC.BO` | 125 | ₹135.83 |
| J&K Bank | `J&KBANK.BO` | 200 | ₹99.57 |
| LIC of India | `LICI.BO` | 15 | ₹904.00 |
| Larsen & Toubro | `LT.BO` | 10 | ₹3,641.52 |
| Punjab National Bank | `PNB.BO` | 160 | ₹73.42 |
| SBI Cards | `SBICARD.BO` | 63 | ₹753.84 |
| SBI ETF Gold | `SETFGOLD.BO` | 1500 | ₹47.79 |
| SBI Life Insurance | `SBILIFE.BO` | 49 | ₹700.00 |
| SAIL | `SAIL.BO` | 500 | ₹87.31 |
| Tejas Networks | `TEJASNET.BO` | 50 | ₹330.32 |
| 2.50% Gold Bonds 2029 SR-XII | *(manual)* | 2 | ₹4,662.00 |

> **Note:** Sovereign Gold Bonds (SGBs) are not listed on Yahoo Finance and are tracked at purchase price.  
> Update the `current_price` field manually in `app.py` using the RBI-published NAV.

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/mmbnura/portfolio-tracker.git
cd portfolio-tracker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

App opens automatically at **http://localhost:8501**

---

## ☁️ Deploy to Streamlit Cloud (Free)

Get a public URL like `https://mmbnura-portfolio-tracker.streamlit.app` in minutes.

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/mmbnura/portfolio-tracker.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub
2. Click **"New app"**
3. Set:
   - **Repository:** `mmbnura/portfolio-tracker`
   - **Branch:** `main`
   - **Main file:** `app.py`
4. Click **"Deploy!"**

Your app will be live in ~2 minutes. ✅

---

## ⚙️ Customise Your Portfolio

Edit the `PORTFOLIO` list at the top of `app.py`:

```python
PORTFOLIO = [
    {"name": "Reliance Industries", "symbol": "RELIANCE.BO", "shares": 10, "buy_price": 2450.00},
    # Add more rows as needed...
]
```

### Finding the right Yahoo Finance symbol

| Exchange | Format | Example |
|---|---|---|
| BSE | `TICKER.BO` | `RELIANCE.BO` |
| NSE | `TICKER.NS` | `RELIANCE.NS` |

Search [finance.yahoo.com](https://finance.yahoo.com) to confirm the exact ticker.

### Updating Sovereign Gold Bond (SGB) price

SGBs are not on Yahoo Finance. Update the price manually:

```python
GOLD_BONDS = [
    {
        "name": "2.50% Gold Bonds 2029 SR-XII",
        "shares": 2,
        "buy_price": 4662.00,
        "current_price": 7500.00,   # ← update with current RBI NAV
        ...
    }
]
```

RBI publishes SGB NAV weekly at [rbi.org.in](https://www.rbi.org.in).

---

## 📉 Trend Signal Logic

| Signal | Condition |
|---|---|
| 🔺 Increasing | 7-day change > +1.5% **AND** 3-day change > +0.5% |
| 🔸 Weak Increasing | Either 7-day or 3-day change is positive |
| 🔻 Decreasing | 7-day change < −1.5% **AND** 3-day change < −0.5% |
| ➡ Flat | All other cases |
| 📌 Manual | Gold Bonds / non-market securities |

---

## 🗂️ Project Structure

```
portfolio-tracker/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io)** — Web UI framework
- **[yfinance](https://github.com/ranaroussi/yfinance)** — Yahoo Finance data (free, no key needed)
- **[pandas](https://pandas.pydata.org)** — Data wrangling

---

## 💡 Possible Future Enhancements

- 📊 7-day sparkline chart per stock
- 🔔 Profit/loss threshold alerts via email or Telegram
- 📤 Export holdings to Excel / CSV
- ☁️ Auto-sync portfolio from broker CSV upload

---

## ⚠️ Disclaimer

This app is for **personal tracking only** and is not financial advice.  
Data is sourced from Yahoo Finance (EOD); prices may be delayed.

---

*Built with Python · Streamlit · Yahoo Finance*
