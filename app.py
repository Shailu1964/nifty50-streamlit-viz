"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   VOLATILITY & MOMENTUM: NIFTY 50 TECHNICAL ANALYSIS DASHBOARD (2024-2026) ║
║   Senior Financial Data Scientist | Python + Streamlit + Plotly             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG — must be the very first Streamlit call
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NIFTY 50 | Volatility & Momentum",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL THEME — Professional Trading Terminal Dark Mode
# ─────────────────────────────────────────────────────────────────────────────
DARK_BG       = "#0A0E1A"
CARD_BG       = "#0F1629"
BORDER_COLOR  = "#1E2D4A"
ACCENT_BLUE   = "#00C4FF"
ACCENT_GREEN  = "#00FF94"
ACCENT_RED    = "#FF3D71"
ACCENT_GOLD   = "#FFD700"
TEXT_PRIMARY  = "#E8EAF0"
TEXT_MUTED    = "#6B7A99"
PLOTLY_THEME  = "plotly_dark"

PLOTLY_LAYOUT = dict(
    template=PLOTLY_THEME,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(10,14,26,0.8)",
    font=dict(family="JetBrains Mono, monospace", color=TEXT_PRIMARY, size=12),
    xaxis=dict(gridcolor=BORDER_COLOR, showgrid=True, zeroline=False),
    yaxis=dict(gridcolor=BORDER_COLOR, showgrid=True, zeroline=False),
    margin=dict(l=50, r=30, t=60, b=40),
    legend=dict(
        bgcolor="rgba(15,22,41,0.9)",
        bordercolor=BORDER_COLOR,
        borderwidth=1,
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — Trading Terminal Aesthetic
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import fonts ── */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Orbitron:wght@400;600;800&display=swap');

/* ── Root & Background ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0A0E1A !important;
    color: #E8EAF0 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

[data-testid="stSidebar"] {
    background-color: #0D1528 !important;
    border-right: 1px solid #1E2D4A !important;
}

/* ── Header ── */
.terminal-header {
    background: linear-gradient(135deg, #0F1629 0%, #0A1933 50%, #0F1629 100%);
    border: 1px solid #1E2D4A;
    border-radius: 8px;
    padding: 20px 28px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}

.terminal-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00C4FF, #00FF94, #FFD700, #FF3D71, #00C4FF);
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
}

@keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

.terminal-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #00C4FF;
    letter-spacing: 3px;
    margin: 0;
    text-shadow: 0 0 20px rgba(0,196,255,0.4);
}

.terminal-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #6B7A99;
    letter-spacing: 2px;
    margin-top: 4px;
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}

.kpi-card {
    background: linear-gradient(135deg, #0F1629, #0A1933);
    border: 1px solid #1E2D4A;
    border-radius: 8px;
    padding: 16px 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease;
}

.kpi-card:hover { border-color: #00C4FF; }

.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
}

.kpi-card.blue::after  { background: #00C4FF; }
.kpi-card.green::after { background: #00FF94; }
.kpi-card.red::after   { background: #FF3D71; }
.kpi-card.gold::after  { background: #FFD700; }

.kpi-label {
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: #6B7A99;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.kpi-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #E8EAF0;
    line-height: 1;
}

.kpi-badge {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 4px;
    margin-top: 6px;
    letter-spacing: 1px;
}

.badge-pos { background: rgba(0,255,148,0.15); color: #00FF94; }
.badge-neg { background: rgba(255,61,113,0.15); color: #FF3D71; }
.badge-neu { background: rgba(0,196,255,0.15);  color: #00C4FF; }

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 24px 0 14px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid #1E2D4A;
}

.section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: #00C4FF;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.section-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #00C4FF;
    box-shadow: 0 0 8px #00C4FF;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

/* ── Stat Table ── */
.stat-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 0.8rem;
}

.stat-table th {
    background: #0F1629;
    color: #6B7A99;
    font-weight: 600;
    letter-spacing: 2px;
    font-size: 0.65rem;
    padding: 10px 14px;
    border-bottom: 1px solid #1E2D4A;
    text-transform: uppercase;
}

.stat-table td {
    padding: 10px 14px;
    border-bottom: 1px solid #1A2540;
    color: #E8EAF0;
}

.stat-table tr:hover td { background: rgba(0,196,255,0.04); }

/* ── Sidebar ── */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stDateInput label,
[data-testid="stSidebar"] .stSlider label {
    color: #6B7A99 !important;
    font-size: 0.72rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tab"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 1.5px !important;
    color: #6B7A99 !important;
    text-transform: uppercase !important;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #00C4FF !important;
    border-bottom: 2px solid #00C4FF !important;
}

/* ── Plotly chart containers ── */
.stPlotlyChart { border-radius: 8px; overflow: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0A0E1A; }
::-webkit-scrollbar-thumb { background: #1E2D4A; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #00C4FF; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# NIFTY 50 STOCK UNIVERSE
# ─────────────────────────────────────────────────────────────────────────────
NIFTY50_STOCKS = {
    "NIFTY 50 Index":       "^NSEI",
    "Reliance Industries":  "RELIANCE.NS",
    "TCS":                  "TCS.NS",
    "HDFC Bank":            "HDFCBANK.NS",
    "Infosys":              "INFY.NS",
    "ICICI Bank":           "ICICIBANK.NS",
    "Hindustan Unilever":   "HINDUNILVR.NS",
    "ITC":                  "ITC.NS",
    "Kotak Mahindra Bank":  "KOTAKBANK.NS",
    "State Bank of India":  "SBIN.NS",
    "Larsen & Toubro":      "LT.NS",
    "Bajaj Finance":        "BAJFINANCE.NS",
    "Axis Bank":            "AXISBANK.NS",
    "Asian Paints":         "ASIANPAINT.NS",
    "HCL Technologies":     "HCLTECH.NS",
    "Wipro":                "WIPRO.NS",
    "Maruti Suzuki":        "MARUTI.NS",
    "Sun Pharma":           "SUNPHARMA.NS",
    "ONGC":                 "ONGC.NS",
    "Power Grid":           "POWERGRID.NS",
    "NTPC":                 "NTPC.NS",
    "Tata Motors":          "TATAMOTORS.NS",
    "UltraTech Cement":     "ULTRACEMCO.NS",
    "Nestle India":         "NESTLEIND.NS",
    "JSW Steel":            "JSWSTEEL.NS",
    "Tata Steel":           "TATASTEEL.NS",
    "M&M":                  "M&M.NS",
    "Bharti Airtel":        "BHARTIARTL.NS",
    "Adani Ports":          "ADANIPORTS.NS",
    "Dr. Reddy's Labs":     "DRREDDY.NS",
}

# ─────────────────────────────────────────────────────────────────────────────
# DATA FETCHING & CACHING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=900, show_spinner=False)  # Cache for 15 minutes
def fetch_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Download OHLCV data from Yahoo Finance with robust error handling.
    Returns a clean DataFrame with computed technical indicators.
    """
    try:
        df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()

        # Flatten MultiIndex columns if present (yfinance ≥0.2.x)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        df.dropna(inplace=True)
        return df
    except Exception as e:
        st.error(f"Data fetch error: {e}")
        return pd.DataFrame()


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute all technical indicators:
    SMA, RSI, Bollinger Bands, Daily Returns, Rolling Volatility, VWAP.
    """
    df = df.copy()
    close = df["Close"]

    # ── Moving Averages ──────────────────────────────────────────────────────
    df["SMA_50"]  = close.rolling(window=50).mean()
    df["SMA_200"] = close.rolling(window=200).mean()

    # ── RSI (14-period) ──────────────────────────────────────────────────────
    delta  = close.diff()
    gain   = delta.clip(lower=0)
    loss   = -delta.clip(upper=0)
    avg_g  = gain.ewm(com=13, adjust=False).mean()
    avg_l  = loss.ewm(com=13, adjust=False).mean()
    rs     = avg_g / avg_l.replace(0, np.nan)
    df["RSI"] = 100 - (100 / (1 + rs))

    # ── Bollinger Bands (20-period, 2σ) ──────────────────────────────────────
    bb_mid        = close.rolling(20).mean()
    bb_std        = close.rolling(20).std()
    df["BB_Mid"]  = bb_mid
    df["BB_Upper"]= bb_mid + 2 * bb_std
    df["BB_Lower"]= bb_mid - 2 * bb_std
    df["BB_Width"]= (df["BB_Upper"] - df["BB_Lower"]) / bb_mid  # Normalized width

    # ── Daily Returns & Volatility ────────────────────────────────────────────
    df["Daily_Return"] = close.pct_change() * 100
    df["Rolling_Vol"]  = df["Daily_Return"].rolling(21).std()  # 21-day rolling σ

    # ── MACD ─────────────────────────────────────────────────────────────────
    ema12       = close.ewm(span=12, adjust=False).mean()
    ema26       = close.ewm(span=26, adjust=False).mean()
    df["MACD"]  = ema12 - ema26
    df["Signal"]= df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["Signal"]

    return df


def compute_stats(df: pd.DataFrame, risk_free_rate: float = 0.065) -> dict:
    """
    Compute summary statistics: Mean Return, Std Dev, Sharpe Ratio, etc.
    Default risk-free rate = 6.5% (approximate Indian T-bill rate).
    """
    returns = df["Daily_Return"].dropna()
    mean_ret     = returns.mean()
    std_ret      = returns.std()
    ann_ret      = mean_ret * 252
    ann_vol      = std_ret * np.sqrt(252)
    daily_rf     = risk_free_rate / 252 * 100
    sharpe       = (mean_ret - daily_rf) / std_ret * np.sqrt(252) if std_ret != 0 else 0
    skewness     = float(returns.skew())
    kurt         = float(returns.kurtosis())
    max_dd       = _max_drawdown(df["Close"])
    pos_days     = (returns > 0).sum()
    neg_days     = (returns < 0).sum()
    hit_rate     = pos_days / (pos_days + neg_days) * 100 if (pos_days + neg_days) > 0 else 0

    return {
        "Mean Daily Return (%)": round(mean_ret, 4),
        "Std Dev Daily (%)":     round(std_ret, 4),
        "Annualised Return (%)": round(ann_ret, 2),
        "Annualised Volatility":round(ann_vol, 2),
        "Sharpe Ratio":          round(sharpe, 3),
        "Skewness":              round(skewness, 3),
        "Excess Kurtosis":       round(kurt, 3),
        "Max Drawdown (%)":      round(max_dd * 100, 2),
        "Win Rate (%)":          round(hit_rate, 1),
        "Positive Days":         int(pos_days),
        "Negative Days":         int(neg_days),
    }


def _max_drawdown(prices: pd.Series) -> float:
    """Compute the maximum peak-to-trough drawdown of a price series."""
    cummax = prices.cummax()
    drawdown = (prices - cummax) / cummax
    return float(drawdown.min())


# ─────────────────────────────────────────────────────────────────────────────
# CHART BUILDERS
# ─────────────────────────────────────────────────────────────────────────────

def build_candlestick_rsi(df: pd.DataFrame, title: str) -> go.Figure:
    """
    Two-row subplot: Candlestick + SMA overlays (top) | RSI (bottom).
    """
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.72, 0.28],
        subplot_titles=["", "RSI (14)"],
    )

    # ── Row 1: Candlestick ────────────────────────────────────────────────────
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"], high=df["High"],
        low=df["Low"],   close=df["Close"],
        name="OHLC",
        increasing=dict(line=dict(color=ACCENT_GREEN, width=1),
                        fillcolor="rgba(0,255,148,0.7)"),
        decreasing=dict(line=dict(color=ACCENT_RED, width=1),
                        fillcolor="rgba(255,61,113,0.7)"),
        showlegend=True,
    ), row=1, col=1)

    # SMA 50
    fig.add_trace(go.Scatter(
        x=df.index, y=df["SMA_50"],
        name="SMA 50", mode="lines",
        line=dict(color="#FFA500", width=1.5, dash="solid"),
    ), row=1, col=1)

    # SMA 200
    fig.add_trace(go.Scatter(
        x=df.index, y=df["SMA_200"],
        name="SMA 200", mode="lines",
        line=dict(color="#DA70D6", width=1.8, dash="dash"),
    ), row=1, col=1)

    # ── Row 2: RSI ────────────────────────────────────────────────────────────
    rsi_colors = [
        ACCENT_RED if v >= 70 else (ACCENT_GREEN if v <= 30 else ACCENT_BLUE)
        for v in df["RSI"].fillna(50)
    ]
    fig.add_trace(go.Scatter(
        x=df.index, y=df["RSI"],
        name="RSI", mode="lines",
        line=dict(color=ACCENT_BLUE, width=1.5),
        fill="tozeroy",
        fillcolor="rgba(0,196,255,0.05)",
    ), row=2, col=1)

    # Overbought / Oversold bands
    for level, color, label in [(70, ACCENT_RED, "OB 70"), (30, ACCENT_GREEN, "OS 30")]:
        fig.add_hline(y=level, row=2, col=1,
                      line=dict(color=color, dash="dot", width=1),
                      annotation_text=label,
                      annotation_position="right",
                      annotation_font=dict(color=color, size=10))

    # Midline
    fig.add_hline(y=50, row=2, col=1,
                  line=dict(color=TEXT_MUTED, dash="dot", width=0.8))

    # ── Layout ────────────────────────────────────────────────────────────────
    layout = PLOTLY_LAYOUT.copy()
    layout.update(
        title=dict(text=f"📊 {title} — Candlestick + SMAs + RSI",
                   font=dict(size=14, color=ACCENT_BLUE), x=0.01),
        height=600,
        xaxis_rangeslider_visible=False,
        yaxis2=dict(range=[0, 100], gridcolor=BORDER_COLOR),
    )
    fig.update_layout(**layout)
    return fig


def build_bollinger(df: pd.DataFrame, title: str) -> go.Figure:
    """
    Bollinger Bands chart with price, upper/lower bands, and band-width indicator.
    """
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.04, row_heights=[0.75, 0.25],
        subplot_titles=["", "BB Width (Squeeze Indicator)"],
    )

    # ── Row 1: Price + Bollinger ──────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=df.index, y=df["BB_Upper"],
        name="Upper Band (2σ)", mode="lines",
        line=dict(color="rgba(255,61,113,0.6)", width=1, dash="dot"),
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df.index, y=df["BB_Lower"],
        name="Lower Band (2σ)", mode="lines",
        line=dict(color="rgba(0,255,148,0.6)", width=1, dash="dot"),
        fill="tonexty",
        fillcolor="rgba(0,196,255,0.04)",
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df.index, y=df["BB_Mid"],
        name="Middle Band (SMA 20)", mode="lines",
        line=dict(color=ACCENT_GOLD, width=1.2, dash="dash"),
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"],
        name="Close Price", mode="lines",
        line=dict(color=ACCENT_BLUE, width=1.8),
    ), row=1, col=1)

    # ── Row 2: BB Width ───────────────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=df.index, y=df["BB_Width"],
        name="BB Width", mode="lines",
        line=dict(color=ACCENT_GOLD, width=1.5),
        fill="tozeroy",
        fillcolor="rgba(255,215,0,0.06)",
    ), row=2, col=1)

    layout = PLOTLY_LAYOUT.copy()
    layout.update(
        title=dict(text=f"📉 {title} — Bollinger Bands Analysis",
                   font=dict(size=14, color=ACCENT_BLUE), x=0.01),
        height=520,
        xaxis_rangeslider_visible=False,
    )
    fig.update_layout(**layout)
    return fig


def build_returns_histogram(df: pd.DataFrame) -> go.Figure:
    """
    Daily Returns distribution: Histogram with KDE-like normal curve overlay.
    """
    returns = df["Daily_Return"].dropna()
    mean_r  = returns.mean()
    std_r   = returns.std()

    # Normal distribution overlay
    x_range = np.linspace(returns.min(), returns.max(), 300)
    normal_y = (1 / (std_r * np.sqrt(2 * np.pi))) * \
               np.exp(-0.5 * ((x_range - mean_r) / std_r) ** 2)
    # Scale to histogram height
    bin_count = 60
    hist_range = returns.max() - returns.min()
    bin_width  = hist_range / bin_count
    scale      = len(returns) * bin_width
    normal_y   *= scale

    fig = go.Figure()

    # Histogram with conditional coloring
    colors = [ACCENT_GREEN if v >= 0 else ACCENT_RED for v in returns]
    fig.add_trace(go.Histogram(
        x=returns,
        nbinsx=bin_count,
        name="Daily Returns",
        marker=dict(
            color=returns.apply(lambda v: "rgba(0,255,148,0.7)" if v >= 0
                                else "rgba(255,61,113,0.7)"),
            line=dict(color="rgba(0,0,0,0.3)", width=0.5),
        ),
    ))

    # Normal curve overlay
    fig.add_trace(go.Scatter(
        x=x_range, y=normal_y,
        name="Normal Dist.",
        mode="lines",
        line=dict(color=ACCENT_GOLD, width=2, dash="solid"),
    ))

    # Mean & ±1σ lines
    for val, color, label in [
        (mean_r, ACCENT_BLUE, f"μ={mean_r:.2f}%"),
        (mean_r + std_r, ACCENT_GOLD, f"+1σ={mean_r+std_r:.2f}%"),
        (mean_r - std_r, ACCENT_GOLD, f"-1σ={mean_r-std_r:.2f}%"),
    ]:
        fig.add_vline(x=val, line=dict(color=color, dash="dot", width=1.5),
                      annotation_text=label,
                      annotation_font=dict(color=color, size=10),
                      annotation_position="top right")

    layout = PLOTLY_LAYOUT.copy()
    layout.update(
        title=dict(text="📊 Daily Returns Distribution — Statistical Inference",
                   font=dict(size=14, color=ACCENT_BLUE), x=0.01),
        xaxis_title="Daily Return (%)",
        yaxis_title="Frequency",
        height=420,
    )
    fig.update_layout(**layout)
    return fig


def build_volatility_gauge(current_vol: float, hist_mean: float, hist_std: float) -> go.Figure:
    """
    Speedometer-style gauge showing current rolling volatility
    relative to its historical range (Fear / Greed indicator).
    """
    # Normalize: 0 = calm, 100 = extreme fear
    z_score = (current_vol - hist_mean) / hist_std if hist_std != 0 else 0
    gauge_val = max(0, min(100, 50 + z_score * 16.67))

    if gauge_val < 30:
        state, color = "LOW VOLATILITY", ACCENT_GREEN
    elif gauge_val < 60:
        state, color = "MODERATE", ACCENT_GOLD
    elif gauge_val < 80:
        state, color = "ELEVATED", "#FF8C00"
    else:
        state, color = "EXTREME FEAR", ACCENT_RED

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=round(current_vol, 2),
        delta=dict(reference=round(hist_mean, 2),
                   valueformat=".2f",
                   increasing=dict(color=ACCENT_RED),
                   decreasing=dict(color=ACCENT_GREEN)),
        title=dict(text=f"Rolling Volatility (21-day σ)<br><span style='font-size:0.85em;color:{color}'>{state}</span>",
                   font=dict(size=13, color=TEXT_PRIMARY)),
        number=dict(suffix="%", font=dict(size=32, color=color)),
        gauge=dict(
            axis=dict(range=[0, max(current_vol * 1.8, hist_mean * 2)],
                      tickwidth=1, tickcolor=TEXT_MUTED,
                      tickfont=dict(size=10)),
            bar=dict(color=color, thickness=0.25),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=1,
            bordercolor=BORDER_COLOR,
            steps=[
                dict(range=[0, hist_mean * 0.7], color="rgba(0,255,148,0.08)"),
                dict(range=[hist_mean * 0.7, hist_mean * 1.3], color="rgba(255,215,0,0.08)"),
                dict(range=[hist_mean * 1.3, max(current_vol * 1.8, hist_mean * 2)],
                     color="rgba(255,61,113,0.08)"),
            ],
            threshold=dict(
                line=dict(color=ACCENT_BLUE, width=2),
                thickness=0.75,
                value=hist_mean,
            ),
        ),
    ))

    fig.update_layout(
        **{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ["xaxis", "yaxis", "margin"]},
        height=300,
        margin=dict(l=30, r=30, t=60, b=20),
    )
    return fig


def build_macd(df: pd.DataFrame) -> go.Figure:
    """
    MACD chart: MACD line, Signal line, and histogram bars.
    """
    hist_colors = [
        "rgba(0,255,148,0.7)" if v >= 0 else "rgba(255,61,113,0.7)"
        for v in df["MACD_Hist"].fillna(0)
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df.index, y=df["MACD_Hist"],
        name="MACD Histogram",
        marker_color=hist_colors,
    ))

    fig.add_trace(go.Scatter(
        x=df.index, y=df["MACD"],
        name="MACD", mode="lines",
        line=dict(color=ACCENT_BLUE, width=1.8),
    ))

    fig.add_trace(go.Scatter(
        x=df.index, y=df["Signal"],
        name="Signal (9)", mode="lines",
        line=dict(color=ACCENT_RED, width=1.5, dash="dash"),
    ))

    fig.add_hline(y=0, line=dict(color=TEXT_MUTED, width=0.8, dash="dot"))

    layout = PLOTLY_LAYOUT.copy()
    layout.update(
        title=dict(text="⚡ MACD — Moving Average Convergence Divergence",
                   font=dict(size=14, color=ACCENT_BLUE), x=0.01),
        height=380,
        xaxis_rangeslider_visible=False,
    )
    fig.update_layout(**layout)
    return fig


def build_rolling_vol(df: pd.DataFrame) -> go.Figure:
    """Rolling 21-day annualised volatility over time."""
    ann_vol = df["Rolling_Vol"] * np.sqrt(252)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=ann_vol,
        name="Ann. Volatility", mode="lines",
        line=dict(color=ACCENT_RED, width=1.8),
        fill="tozeroy",
        fillcolor="rgba(255,61,113,0.06)",
    ))

    # Historical mean line
    mean_v = ann_vol.mean()
    fig.add_hline(y=mean_v,
                  line=dict(color=ACCENT_GOLD, dash="dash", width=1.2),
                  annotation_text=f"Avg: {mean_v:.1f}%",
                  annotation_font=dict(color=ACCENT_GOLD, size=10))

    layout = PLOTLY_LAYOUT.copy()
    layout.update(
        title=dict(text="📈 Rolling Annualised Volatility (21-day window)",
                   font=dict(size=14, color=ACCENT_BLUE), x=0.01),
        yaxis_title="Ann. Volatility (%)",
        height=340,
    )
    fig.update_layout(**layout)
    return fig


def build_forecast(df: pd.DataFrame, forecast_days: int = 180) -> go.Figure:
    """
    Simple OLS linear regression trendline with confidence interval forecast.
    Projects price into the future using the fitted trend.
    """
    close = df["Close"].dropna()

    # Numeric x for regression
    x_num = np.arange(len(close))
    coeffs = np.polyfit(x_num, close.values, 1)
    slope, intercept = coeffs

    # Historical fit
    fitted = np.polyval(coeffs, x_num)

    # Residual std dev for confidence band
    residuals = close.values - fitted
    resid_std  = residuals.std()

    # Forecast
    x_fc   = np.arange(len(close), len(close) + forecast_days)
    fc_val = np.polyval(coeffs, x_fc)

    # Build future dates (approximate trading days)
    last_date = close.index[-1]
    fc_dates  = pd.bdate_range(start=last_date + pd.Timedelta(days=1),
                                periods=forecast_days)

    fig = go.Figure()

    # Actual price
    fig.add_trace(go.Scatter(
        x=close.index, y=close,
        name="Actual Price", mode="lines",
        line=dict(color=ACCENT_BLUE, width=1.8),
    ))

    # Regression line (history)
    fig.add_trace(go.Scatter(
        x=close.index, y=fitted,
        name="Linear Trend", mode="lines",
        line=dict(color=ACCENT_GOLD, width=1.5, dash="dash"),
    ))

    # Forecast line
    fig.add_trace(go.Scatter(
        x=fc_dates, y=fc_val,
        name="Forecast", mode="lines",
        line=dict(color=ACCENT_GOLD, width=2, dash="dot"),
    ))

    # Confidence band (±2σ)
    fig.add_trace(go.Scatter(
        x=list(fc_dates) + list(fc_dates[::-1]),
        y=list(fc_val + 2 * resid_std) + list((fc_val - 2 * resid_std)[::-1]),
        fill="toself",
        fillcolor="rgba(255,215,0,0.07)",
        line=dict(color="rgba(0,0,0,0)"),
        name="95% Confidence Band",
        showlegend=True,
    ))

    # Vertical separator using a shape (avoids Plotly add_vline string/numeric type error)
    fig.add_shape(
        type="line",
        x0=last_date, x1=last_date,
        y0=0, y1=1,
        xref="x", yref="paper",
        line=dict(color=ACCENT_BLUE, dash="dot", width=1.5),
    )
    fig.add_annotation(
        x=last_date, y=1,
        xref="x", yref="paper",
        text="Forecast →",
        font=dict(color=ACCENT_BLUE, size=11),
        showarrow=False,
        yanchor="bottom",
        xanchor="left",
    )

    # Annotation: projected end value
    fig.add_annotation(
        x=fc_dates[-1], y=fc_val[-1],
        text=f"₹{fc_val[-1]:,.0f}",
        font=dict(color=ACCENT_GOLD, size=12),
        bgcolor="rgba(15,22,41,0.9)",
        bordercolor=ACCENT_GOLD,
        borderwidth=1,
        showarrow=True,
        arrowcolor=ACCENT_GOLD,
    )

    layout = PLOTLY_LAYOUT.copy()
    layout.update(
        title=dict(text=f"🔮 Price Forecast — Linear Regression Trendline ({forecast_days}d Outlook)",
                   font=dict(size=14, color=ACCENT_BLUE), x=0.01),
        height=480,
    )
    fig.update_layout(**layout)

    # Trend metadata
    daily_drift = slope
    pct_change  = (fc_val[-1] - close.iloc[-1]) / close.iloc[-1] * 100
    return fig, daily_drift, pct_change


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-family:Orbitron,sans-serif;font-size:0.9rem;
                color:#00C4FF;letter-spacing:3px;margin-bottom:20px;
                padding-bottom:12px;border-bottom:1px solid #1E2D4A;'>
        ⚙ CONTROLS
    </div>
    """, unsafe_allow_html=True)

    # Asset selection
    selected_name   = st.selectbox("SELECT INSTRUMENT", list(NIFTY50_STOCKS.keys()), index=0)
    selected_ticker = NIFTY50_STOCKS[selected_name]

    st.markdown("<br>", unsafe_allow_html=True)

    # Date range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("FROM", value=datetime(2024, 1, 1),
                                   min_value=datetime(2024, 1, 1),
                                   max_value=datetime(2026, 12, 31))
    with col2:
        end_date   = st.date_input("TO",   value=datetime.today(),
                                   min_value=datetime(2024, 1, 1),
                                   max_value=datetime(2026, 12, 31))

    st.markdown("<br>", unsafe_allow_html=True)

    # Forecast horizon
    forecast_days = st.slider("FORECAST HORIZON (Days)", 30, 365, 180, step=30)

    # Risk-free rate
    risk_free = st.slider("RISK-FREE RATE (%)", 4.0, 9.0, 6.5, step=0.25)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.65rem;color:#6B7A99;letter-spacing:1px;
                border-top:1px solid #1E2D4A;padding-top:12px;'>
        DATA SOURCE: Yahoo Finance via yfinance<br>
        REFRESH: Every 15 minutes (cached)<br>
        INDICATORS: SMA·RSI·BB·MACD·σ
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="terminal-header">
    <div class="terminal-title">VOLATILITY &amp; MOMENTUM</div>
    <div class="terminal-subtitle">
        NIFTY 50 TECHNICAL ANALYSIS TERMINAL &nbsp;|&nbsp;
        {selected_name.upper()} ({selected_ticker}) &nbsp;|&nbsp;
        {start_date.strftime('%d %b %Y')} → {end_date.strftime('%d %b %Y')}
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOAD
# ─────────────────────────────────────────────────────────────────────────────
with st.spinner("⟳ Fetching market data..."):
    raw_df = fetch_data(selected_ticker, str(start_date), str(end_date))

if raw_df.empty:
    st.error("❌ Could not retrieve data. Check the ticker or date range and try again.")
    st.stop()

df = compute_indicators(raw_df)
stats = compute_stats(df, risk_free_rate=risk_free / 100)

# ─────────────────────────────────────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────────────────────────────────────
close_vals = df["Close"].dropna()
current_price = float(close_vals.iloc[-1])
prev_price    = float(close_vals.iloc[-2]) if len(close_vals) > 1 else current_price
daily_chg_pct = (current_price - prev_price) / prev_price * 100

# 52-week window
one_year_ago  = df.index[-1] - pd.Timedelta(weeks=52)
df_52w        = df[df.index >= one_year_ago]["Close"]
high_52w      = float(df_52w.max())
low_52w       = float(df_52w.min())
current_vol   = float(df["Rolling_Vol"].dropna().iloc[-1])
hist_mean_vol = float(df["Rolling_Vol"].dropna().mean())
hist_std_vol  = float(df["Rolling_Vol"].dropna().std())

chg_class  = "badge-pos" if daily_chg_pct >= 0 else "badge-neg"
chg_symbol = "▲" if daily_chg_pct >= 0 else "▼"
vol_class  = "badge-neg" if current_vol > hist_mean_vol * 1.3 else \
             ("badge-pos" if current_vol < hist_mean_vol * 0.7 else "badge-neu")

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card blue">
        <div class="kpi-label">📌 Current Price</div>
        <div class="kpi-value">₹{current_price:,.2f}</div>
        <span class="kpi-badge {chg_class}">{chg_symbol} {abs(daily_chg_pct):.2f}% TODAY</span>
    </div>
    <div class="kpi-card {'green' if daily_chg_pct >= 0 else 'red'}">
        <div class="kpi-label">📈 Daily Change</div>
        <div class="kpi-value" style="color:{'#00FF94' if daily_chg_pct >= 0 else '#FF3D71'}">
            {'+' if daily_chg_pct >= 0 else ''}{daily_chg_pct:.2f}%
        </div>
        <span class="kpi-badge {chg_class}">
            ₹{'+' if (current_price-prev_price)>=0 else ''}{current_price-prev_price:,.2f} ABS
        </span>
    </div>
    <div class="kpi-card gold">
        <div class="kpi-label">🏔 52-Week High</div>
        <div class="kpi-value">₹{high_52w:,.2f}</div>
        <span class="kpi-badge badge-pos">
            {((current_price - high_52w) / high_52w * 100):+.1f}% FROM HIGH
        </span>
    </div>
    <div class="kpi-card {'red' if current_vol > hist_mean_vol else 'green'}">
        <div class="kpi-label">⚡ Rolling Volatility</div>
        <div class="kpi-value" style="color:{'#FF3D71' if current_vol > hist_mean_vol else '#00FF94'}">
            {current_vol:.2f}%
        </div>
        <span class="kpi-badge {vol_class}">21-DAY σ</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Secondary KPIs (52W Low + Sharpe + Win Rate + Mean Return)
sharpe_class = "badge-pos" if stats["Sharpe Ratio"] > 1 else \
               ("badge-neu" if stats["Sharpe Ratio"] > 0 else "badge-neg")

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card green">
        <div class="kpi-label">🪨 52-Week Low</div>
        <div class="kpi-value">₹{low_52w:,.2f}</div>
        <span class="kpi-badge badge-pos">
            {((current_price - low_52w) / low_52w * 100):+.1f}% FROM LOW
        </span>
    </div>
    <div class="kpi-card blue">
        <div class="kpi-label">⚖ Sharpe Ratio</div>
        <div class="kpi-value">{stats['Sharpe Ratio']:.3f}</div>
        <span class="kpi-badge {sharpe_class}">RF={risk_free:.1f}% ANN.</span>
    </div>
    <div class="kpi-card gold">
        <div class="kpi-label">🎯 Win Rate</div>
        <div class="kpi-value">{stats['Win Rate (%)']:.1f}%</div>
        <span class="kpi-badge badge-neu">{stats['Positive Days']}+ / {stats['Negative Days']}- DAYS</span>
    </div>
    <div class="kpi-card {'green' if stats['Mean Daily Return (%)'] >= 0 else 'red'}">
        <div class="kpi-label">📊 Mean Daily Return</div>
        <div class="kpi-value" style="color:{'#00FF94' if stats['Mean Daily Return (%)'] >= 0 else '#FF3D71'}">
            {stats['Mean Daily Return (%)']:+.4f}%
        </div>
        <span class="kpi-badge badge-neu">ANN. {stats['Annualised Return (%)']:+.1f}%</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  MOMENTUM ANALYSIS",
    "📉  VOLATILITY ANALYSIS",
    "📋  STATISTICAL SUMMARY",
    "🔮  FORECASTING",
])

# ════════════════════════════════════════════════════════════
# TAB 1 — MOMENTUM ANALYSIS
# ════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="section-header">
        <div class="section-dot"></div>
        <div class="section-title">Candlestick · SMA 50/200 · RSI</div>
    </div>
    """, unsafe_allow_html=True)

    fig_candle = build_candlestick_rsi(df, selected_name)
    st.plotly_chart(fig_candle, width="stretch", config={"displayModeBar": True})

    # SMA crossover signal
    if not df["SMA_50"].isna().all() and not df["SMA_200"].isna().all():
        sma50_last  = float(df["SMA_50"].dropna().iloc[-1])
        sma200_last = float(df["SMA_200"].dropna().iloc[-1])
        rsi_last    = float(df["RSI"].dropna().iloc[-1])

        signal_col1, signal_col2, signal_col3 = st.columns(3)
        with signal_col1:
            cross = "🟢 GOLDEN CROSS (Bullish)" if sma50_last > sma200_last \
                    else "🔴 DEATH CROSS (Bearish)"
            st.markdown(f"""
            <div class="kpi-card {'green' if sma50_last > sma200_last else 'red'}" style="margin:0">
                <div class="kpi-label">SMA Crossover Signal</div>
                <div style="font-size:0.85rem;color:#E8EAF0;margin-top:6px;">{cross}</div>
                <div style="font-size:0.72rem;color:#6B7A99;margin-top:4px;">
                    SMA50: ₹{sma50_last:,.1f} | SMA200: ₹{sma200_last:,.1f}
                </div>
            </div>""", unsafe_allow_html=True)

        with signal_col2:
            rsi_signal = "🔴 OVERBOUGHT" if rsi_last >= 70 else \
                         ("🟢 OVERSOLD" if rsi_last <= 30 else "🔵 NEUTRAL")
            rsi_cls = "red" if rsi_last >= 70 else ("green" if rsi_last <= 30 else "blue")
            st.markdown(f"""
            <div class="kpi-card {rsi_cls}" style="margin:0">
                <div class="kpi-label">RSI Signal (14)</div>
                <div style="font-size:0.85rem;color:#E8EAF0;margin-top:6px;">{rsi_signal}</div>
                <div style="font-size:0.72rem;color:#6B7A99;margin-top:4px;">
                    Current RSI: {rsi_last:.1f} | OB:70 / OS:30
                </div>
            </div>""", unsafe_allow_html=True)

        with signal_col3:
            macd_last = float(df["MACD"].dropna().iloc[-1])
            sig_last  = float(df["Signal"].dropna().iloc[-1])
            macd_sig  = "🟢 BULLISH" if macd_last > sig_last else "🔴 BEARISH"
            macd_cls  = "green" if macd_last > sig_last else "red"
            st.markdown(f"""
            <div class="kpi-card {macd_cls}" style="margin:0">
                <div class="kpi-label">MACD Signal</div>
                <div style="font-size:0.85rem;color:#E8EAF0;margin-top:6px;">{macd_sig}</div>
                <div style="font-size:0.72rem;color:#6B7A99;margin-top:4px;">
                    MACD: {macd_last:.1f} | Signal: {sig_last:.1f}
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-dot" style="background:#FFD700;box-shadow:0 0 8px #FFD700;"></div>
        <div class="section-title" style="color:#FFD700;">MACD Analysis</div>
    </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(build_macd(df), width="stretch")

# ════════════════════════════════════════════════════════════
# TAB 2 — VOLATILITY ANALYSIS
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="section-header">
        <div class="section-dot" style="background:#FF3D71;box-shadow:0 0 8px #FF3D71;"></div>
        <div class="section-title">Bollinger Bands · Squeeze Detection</div>
    </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(build_bollinger(df, selected_name), width="stretch")

    col_hist, col_gauge = st.columns([1.6, 1])
    with col_hist:
        st.markdown("""
        <div class="section-header">
            <div class="section-dot" style="background:#00FF94;box-shadow:0 0 8px #00FF94;"></div>
            <div class="section-title">Returns Distribution</div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(build_returns_histogram(df), width="stretch")

    with col_gauge:
        st.markdown("""
        <div class="section-header">
            <div class="section-dot" style="background:#FFD700;box-shadow:0 0 8px #FFD700;"></div>
            <div class="section-title">Volatility Gauge</div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(
            build_volatility_gauge(current_vol, hist_mean_vol, hist_std_vol),
            width="stretch",
        )

    st.markdown("""
    <div class="section-header">
        <div class="section-dot" style="background:#FF3D71;box-shadow:0 0 8px #FF3D71;"></div>
        <div class="section-title">Rolling Annualised Volatility</div>
    </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(build_rolling_vol(df), width="stretch")

# ════════════════════════════════════════════════════════════
# TAB 3 — STATISTICAL SUMMARY
# ════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class="section-header">
        <div class="section-dot" style="background:#FFD700;box-shadow:0 0 8px #FFD700;"></div>
        <div class="section-title">Statistical Summary Table</div>
    </div>
    """, unsafe_allow_html=True)

    # Build styled HTML table
    rows_html = ""
    for metric, value in stats.items():
        # Determine value color
        if "Return" in metric or "Win" in metric or "Sharpe" in metric:
            val_color = ACCENT_GREEN if (isinstance(value, (int, float)) and value >= 0) else ACCENT_RED
        elif "Drawdown" in metric or "Negative" in metric:
            val_color = ACCENT_RED
        else:
            val_color = TEXT_PRIMARY

        rows_html += f"""
        <tr>
            <td style='color:{TEXT_MUTED};letter-spacing:1px;font-size:0.78rem;'>{metric}</td>
            <td style='color:{val_color};font-weight:600;text-align:right;'>{value}</td>
        </tr>"""

    st.markdown(f"""
    <table class="stat-table">
        <thead>
            <tr>
                <th style='text-align:left;'>METRIC</th>
                <th style='text-align:right;'>VALUE</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # Interpretation notes
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-dot" style="background:#00C4FF;box-shadow:0 0 8px #00C4FF;"></div>
        <div class="section-title">Interpretation Guide</div>
    </div>
    <div style='font-size:0.78rem;color:#6B7A99;line-height:2;'>
        <b style='color:#00C4FF;'>Sharpe Ratio</b> &gt; 1.0 = Good | &gt; 2.0 = Excellent | &lt; 0 = Underperforming risk-free rate<br>
        <b style='color:#FFD700;'>Skewness</b>: Negative = left-tail risk (crash risk); Positive = right-tail (upside surprise)<br>
        <b style='color:#FF3D71;'>Kurtosis</b>: &gt; 0 = fat tails (more extreme events than a normal distribution predicts)<br>
        <b style='color:#00FF94;'>Max Drawdown</b>: Peak-to-trough decline — a key measure of downside risk<br>
        <b style='color:#DA70D6;'>Win Rate</b>: Fraction of positive-return days — ideally above 50% for trending assets
    </div>
    """, unsafe_allow_html=True)

    # Correlation matrix for OHLCV
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-dot" style="background:#DA70D6;box-shadow:0 0 8px #DA70D6;"></div>
        <div class="section-title">OHLCV Correlation Matrix</div>
    </div>
    """, unsafe_allow_html=True)

    corr_cols = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]
    corr_df   = df[corr_cols].corr()
    fig_corr  = px.imshow(
        corr_df, text_auto=".2f", color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        aspect="auto",
    )
    corr_layout = {k: v for k, v in PLOTLY_LAYOUT.items() if k not in ["xaxis", "yaxis"]}
    corr_layout.update(
        title=dict(text="Pearson Correlation — OHLCV Features",
                   font=dict(size=13, color=ACCENT_BLUE), x=0.01),
        height=340,
    )
    fig_corr.update_layout(**corr_layout)
    st.plotly_chart(fig_corr, width="stretch")

# ════════════════════════════════════════════════════════════
# TAB 4 — FORECASTING
# ════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class="section-header">
        <div class="section-dot" style="background:#FFD700;box-shadow:0 0 8px #FFD700;"></div>
        <div class="section-title">Linear Regression Price Forecast</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Computing forecast..."):
        fig_fc, daily_drift, pct_outlook = build_forecast(df, forecast_days)

    st.plotly_chart(fig_fc, width="stretch")

    # Forecast KPIs
    direction = "BULLISH 📈" if pct_outlook > 0 else "BEARISH 📉"
    dir_color = ACCENT_GREEN if pct_outlook > 0 else ACCENT_RED
    last_price = float(df["Close"].dropna().iloc[-1])
    fc_target  = last_price * (1 + pct_outlook / 100)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"""
        <div class="kpi-card {'green' if pct_outlook > 0 else 'red'}" style="margin:0">
            <div class="kpi-label">Trend Direction</div>
            <div style="font-size:0.9rem;color:{dir_color};margin-top:6px;font-weight:700;">{direction}</div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="kpi-card gold" style="margin:0">
            <div class="kpi-label">Projected Price ({forecast_days}d)</div>
            <div style="font-size:0.9rem;color:#FFD700;margin-top:6px;font-weight:700;">₹{fc_target:,.2f}</div>
        </div>""", unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""
        <div class="kpi-card {'green' if pct_outlook > 0 else 'red'}" style="margin:0">
            <div class="kpi-label">Expected Return</div>
            <div style="font-size:0.9rem;color:{dir_color};margin-top:6px;font-weight:700;">{pct_outlook:+.2f}%</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <br>
    <div style='font-size:0.72rem;color:#6B7A99;letter-spacing:1px;
                border:1px solid #1E2D4A;border-radius:6px;padding:12px 16px;'>
        ⚠ <b style='color:#FFD700;'>DISCLAIMER:</b> This forecast uses Ordinary Least Squares (OLS) linear regression
        and is provided for <b>educational and analytical purposes only</b>. It does not constitute financial advice.
        Markets are influenced by macroeconomic, geopolitical, and sentiment factors not captured by linear models.
        Always consult a SEBI-registered investment advisor before making investment decisions.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='margin-top:32px;padding-top:16px;border-top:1px solid #1E2D4A;
            text-align:center;font-size:0.65rem;color:#6B7A99;letter-spacing:2px;'>
    NIFTY 50 ANALYSIS TERMINAL &nbsp;|&nbsp; DATA: YAHOO FINANCE &nbsp;|&nbsp;
    BUILT WITH STREAMLIT + PLOTLY &nbsp;|&nbsp; {datetime.now().strftime('%d %b %Y %H:%M IST')}
</div>
""", unsafe_allow_html=True)