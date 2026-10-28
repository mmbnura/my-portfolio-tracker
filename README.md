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
| ⚡ Fast Refresh | All 24 live tickers fetched in ~5–10 seconds |
| 🌙 Dark Theme | GitHub-style dark UI with IBM Plex Mono |

---

## 📦 Portfolio Holdings

| Stock | Symbol | Qty | Avg Cost |
|---|---|---|---|
| Coal India Ltd | `COALINDIA.BO` | 10 | ₹460.07 |
| ITC Hotels Ltd | `ITCHOTELS.BO` | 10 | ₹580.95 |
| ITC Ltd | `ITC.BO` | 200 | ₹391.80 |
| Indian Oil Corporation Ltd | `IOC.BO` | 125 | ₹135.83 |
| Jammu and Kashmir Bank Ltd | `J&KBANK.BO` | 200 | ₹99.57 |
| Life Insurance Corporation of India | `LICI.BO` | 30 | ₹452.00 |
| Larsen & Toubro Ltd | `LT.BO` | 10 | ₹3,641.52 |
| Muthoot Finance Ltd | `MUTHOOTFIN.BO` | 5 | ₹3,351.83 |
| Punjab National Bank | `PNB.BO` | 160 | ₹73.42 |
| SBI Cards & Payment Services Ltd | `SBICARD.BO` | 63 | ₹753.84 |
| SBI ETF Gold | `SBIGETS.BO` | 1500 | ₹47.79 |
| SBI Funds Management Ltd | `SBIFUNDS.BO` | 39 | ₹520.00 |
| SBI Life Insurance Company Ltd | `SBILIFE.BO` | 49 | ₹700.00 |
| Steel Authority of India Ltd | `SAIL.BO` | 500 | ₹87.31 |
| Tejas Networks Ltd | `TEJASNET.BO` | 50 | ₹330.32 |
| Aeroflex Neu Ltd | `AERONEU.BO` | 130 | ₹80.22 |
| APAR Industries Ltd | `APARINDS.BO` | 25 | ₹17,776.00 |
| Bajaj Finserv Ltd | `BAJAJFINSV.BO` | 30 | ₹1,771.00 |
| Coforge Ltd | `COFORGE.BO` | 50 | ₹1,784.00 |
| Indian Railway Finance Corporation Ltd | `IRFC.BO` | 391 | ₹79.95 |
| Jio Financial Services Ltd | `JIOFIN.BO` | 100 | ₹227.00 |
| Maan Aluminium Ltd | `MAANALU.BO` | 400 | ₹100.18 |
| Orient Paper & Industries Ltd | `ORIENTPPR.BO` | 170 | ₹16.76 |
| Tata Steel Ltd | `TATASTEEL.BO` | 405 | ₹187.97 |
| 2.50% Gold Bonds 2029 SR-XII | *(manual)* | 2 | ₹4,662.00 |

> **Note:** Sovereign Gold Bonds (SGBs) are configured in `portfolio.json`; their current value is derived live from COMEX gold futures and USD/INR.

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

Edit the holdings in `portfolio.json` instead of changing the Python code:

```json
{
  "portfolio": [
    {
      "name": "Reliance Industries",
      "symbol": "RELIANCE.BO",
      "shares": 10,
      "buy_price": 2450.00
    }
  ],
  "gold_bonds": [
    {
      "name": "2.50% Gold Bonds 2029 SR-XII",
      "shares": 2,
      "buy_price": 4662.00
    }
  ]
}
```

### Finding the right Yahoo Finance symbol

| Exchange | Format | Example |
|---|---|---|
| BSE | `TICKER.BO` | `RELIANCE.BO` |
| NSE | `TICKER.NS` | `RELIANCE.NS` |

Search [finance.yahoo.com](https://finance.yahoo.com) to confirm the exact ticker.

### Updating Sovereign Gold Bond (SGB) holdings

SGB holdings are configured in the `gold_bonds` section of `portfolio.json`. The app derives their current value live from COMEX gold futures and USD/INR.

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
├── portfolio.json    # Portfolio and SGB holdings
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
