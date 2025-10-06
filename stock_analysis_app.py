import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import os

# --------------------------
# Page Config
# --------------------------
st.set_page_config(page_title="Stock Analysis App", page_icon="📈", layout="wide")

# --------------------------
# Chatbot Utilities (Hugging Face Inference API - free endpoint)
# --------------------------
HF_CHAT_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # good free-chat model via HF Inference API
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_CHAT_MODEL}"
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")  # optional; public/free tier often works without token

SYSTEM_PROMPT = (
    "You are a helpful support assistant for a Streamlit stock analysis app. "
    "Answer user questions about using the app, understanding metrics (P/E, P/B, ROE), "
    "data sources, and general app troubleshooting. Keep answers concise."
)

def hf_chat_completion(messages: list[dict], max_new_tokens: int = 256, temperature: float = 0.2) -> str:
    headers = {"Accept": "application/json"}
    if HF_API_TOKEN:
        headers["Authorization"] = f"Bearer {HF_API_TOKEN}"
    payload = {
        "inputs": {
            "past_user_inputs": [m["content"] for m in messages if m["role"] == "user"],
            "generated_responses": [m["content"] for m in messages if m["role"] == "assistant"],
            "text": messages[-1]["content"] if messages else "Hello",
        },
        "parameters": {"max_new_tokens": max_new_tokens, "temperature": temperature}
    }
    try:
        r = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        # HF conversation models may return dict with 'generated_text' or a list
        if isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"].strip()
        if isinstance(data, list) and len(data) and isinstance(data[0], dict):
            # some endpoints return [{'generated_text': '...'}]
            gt = data[0].get("generated_text") or data[0].get("summary_text")
            if gt:
                return gt.strip()
        # Fallback if text generation style
        if isinstance(data, dict) and "conversation" in data:
            conv = data["conversation"]
            if isinstance(conv, dict) and "generated_responses" in conv and conv["generated_responses"]:
                return conv["generated_responses"][-1].strip()
        return "Sorry, I couldn't generate a response right now. Please try again."
    except Exception as e:
        return f"Chat service error: {e}"

# --------------------------
# Helper Functions
# --------------------------

def fetch_sp500_tickers():
    """Fetch S&P 500 tickers from Wikipedia"""
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        tables = pd.read_html(url)
        sp500_table = tables[0]
        tickers = sp500_table['Symbol'].tolist()
        # Clean tickers (replace dots with dashes for Yahoo Finance compatibility)
        tickers = [ticker.replace('.', '-') for ticker in tickers]
        return tickers
    except Exception as e:
        st.error(f"Error fetching S&P 500 tickers: {e}")
        return []

def fetch_stock_data(ticker):
    """Fetch stock price and financial data using yfinance"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        data = {
            'Ticker': ticker,
            'Name': info.get('longName', 'N/A'),
            'Current_Price': info.get('currentPrice', np.nan),
            'PE_Ratio': info.get('trailingPE', np.nan),
            'PB_Ratio': info.get('priceToBook', np.nan),
            'PS_Ratio': info.get('priceToSalesTrailing12Months', np.nan),
            'Dividend_Yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
            'ROE': info.get('returnOnEquity', np.nan) * 100 if info.get('returnOnEquity') else np.nan,
            'Profit_Margin': info.get('profitMargins', np.nan) * 100 if info.get('profitMargins') else np.nan,
            'Revenue_Growth': info.get('revenueGrowth', np.nan) * 100 if info.get('revenueGrowth') else np.nan,
            'EPS': info.get('trailingEps', np.nan),
            'Beta': info.get('beta', np.nan),
            'Market_Cap': info.get('marketCap', np.nan),
            'Sector': info.get('sector', 'N/A')
        }
        return data
    except Exception:
        return None

def calculate_valuation_score(row):
    """Calculate a composite valuation score based on multiple factors"""
    score = 0
    weight_total = 0
    # Lower P/E is better
    if pd.notna(row['PE_Ratio']) and row['PE_Ratio'] > 0:
        pe_score = max(0, 100 - (row['PE_Ratio'] - 10) * 2)
        score += pe_score * 0.25
        weight_total += 0.25
    # Lower P/B is better
    if pd.notna(row['PB_Ratio']) and row['PB_Ratio'] > 0:
        pb_score = max(0, 100 - (row['PB_Ratio'] - 1) * 20)
        score += pb_score * 0.20
        weight_total += 0.20
    # Lower P/S is better
    if pd.notna(row['PS_Ratio']) and row['PS_Ratio'] > 0:
        ps_score = max(0, 100 - (row['PS_Ratio'] - 1) * 15)
        score += ps_score * 0.15
        weight_total += 0.15
    # Higher ROE is better
    if pd.notna(row['ROE']) and row['ROE'] > 0:
        roe_score = min(100, row['ROE'] * 5)
        score += roe_score * 0.20
        weight_total += 0.20
    # Higher Profit Margin is better
    if pd.notna(row['Profit_Margin']) and row['Profit_Margin'] > 0:
        margin_score = min(100, row['Profit_Margin'] * 5)
        score += margin_score * 0.10
        weight_total += 0.10
    # Higher Dividend Yield is better (bonus)
    if pd.notna(row['Dividend_Yield']) and row['Dividend_Yield'] > 0:
        div_score = min(100, row['Dividend_Yield'] * 20)
        score += div_score * 0.10
        weight_total += 0.10
    if weight_total > 0:
        return score / weight_total
    return 0

# --------------------------
# Main App
# --------------------------

st.title("📈 Global Stock & ETF Analysis App")
st.markdown("### Powered by yfinance - Live Market Data")

# Sidebar
st.sidebar.header("Analysis Options")
analysis_mode = st.sidebar.radio(
    "Select Analysis Mode:",
    ["S&P 500 Top Undervalued Stocks", "Custom Ticker Analysis"]
)

# Chatbot UI in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("💬 Support Chatbot")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
user_msg = st.sidebar.text_input("Ask a question about using this app:", placeholder="e.g., What does P/E mean?")
col_chat1, col_chat2 = st.sidebar.columns([3,1])
with col_chat1:
    ask = st.button("Ask")
with col_chat2:
    clear = st.button("Clear")
if clear:
    st.session_state.chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
if ask and user_msg.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_msg.strip()})
    # build alternating messages excluding system for HF conversation format
    convo = [m for m in st.session_state.chat_history if m["role"] != "system"]
    reply = hf_chat_completion(convo)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# Render recent messages (last 6 shown)
for m in st.session_state.chat_history[-6:]:
    if m["role"] == "user":
        st.sidebar.markdown(f"🧑‍💻 **You:** {m['content']}")
    elif m["role"] == "assistant":
        st.sidebar.markdown(f"🤖 **Bot:** {m['content']}")

if analysis_mode == "S&P 500 Top Undervalued Stocks":
    st.header("🔍 S&P 500 Undervalued Stock Analysis")
    st.markdown("""
    This analysis:
    1. **Fetches S&P 500 tickers** from Wikipedia
    2. **Uses yfinance** to get live price and financial data
    3. **Runs valuation scoring** based on P/E, P/B, P/S, ROE, Profit Margin, and Dividend Yield
    4. **Shows the top 10 undervalued stocks** with the best scores
    """)
    if st.button("🚀 Run S&P 500 Analysis", type="primary"):
        with st.spinner("Fetching S&P 500 tickers from Wikipedia..."):
            sp500_tickers = fetch_sp500_tickers()
        if sp500_tickers:
            st.success(f"✅ Fetched {len(sp500_tickers)} S&P 500 tickers")
            with st.spinner("Analyzing stocks... This may take a few minutes..."):
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                for idx, ticker in enumerate(sp500_tickers):
                    status_text.text(f"Analyzing {ticker} ({idx+1}/{len(sp500_tickers)})")
                    data = fetch_stock_data(ticker)
                    if data:
                        results.append(data)
                    progress_bar.progress((idx + 1) / len(sp500_tickers))
                status_text.empty()
                progress_bar.empty()
                if results:
                    df = pd.DataFrame(results)
                    df['Valuation_Score'] = df.apply(calculate_valuation_score, axis=1)
                    df_valid = df[df['Valuation_Score'] > 0].copy()
                    df_sorted = df_valid.sort_values('Valuation_Score', ascending=False)
                    top_10 = df_sorted.head(10)
                    st.success(f"✅ Analysis complete! Found {len(df_valid)} stocks with sufficient data.")
                    st.header("🏆 Top 10 Undervalued Stocks")
                    display_cols = ['Ticker', 'Name', 'Sector', 'Current_Price', 'PE_Ratio', 'PB_Ratio', 'ROE', 'Profit_Margin', 'Dividend_Yield', 'Valuation_Score']
                    st.dataframe(
                        top_10[display_cols].style.format({
                            'Current_Price': '${:.2f}',
                            'PE_Ratio': '{:.2f}',
                            'PB_Ratio': '{:.2f}',
                            'ROE': '{:.2f}%','Profit_Margin': '{:.2f}%','Dividend_Yield': '{:.2f}%','Valuation_Score': '{:.2f}'
                        }).background_gradient(subset=['Valuation_Score'], cmap='RdYlGn'),
                        use_container_width=True
                    )
                    st.subheader("📊 Valuation Score Comparison")
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.barh(top_10['Ticker'], top_10['Valuation_Score'], color='steelblue')
                    ax.set_xlabel('Valuation Score')
                    ax.set_title('Top 10 Undervalued S&P 500 Stocks')
                    ax.invert_yaxis()
                    st.pyplot(fig)
                    csv = df_sorted.to_csv(index=False)
                    st.download_button(label="📥 Download Full Analysis (CSV)", data=csv, file_name="sp500_valuation_analysis.csv", mime="text/csv")
                else:
                    st.error("No data retrieved. Please try again.")
        else:
            st.error("Failed to fetch S&P 500 tickers.")
elif analysis_mode == "Custom Ticker Analysis":
    st.header("🔎 Custom Ticker Analysis")
    ticker_input = st.text_input("Enter ticker symbol (e.g., AAPL, MSFT, TSLA):", "AAPL")
    if st.button("Analyze Ticker", type="primary"):
        if ticker_input:
            with st.spinner(f"Fetching data for {ticker_input}..."):
                data = fetch_stock_data(ticker_input.upper())
            if data:
                st.success(f"✅ Data retrieved for {ticker_input.upper()}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Company", data['Name'])
                    st.metric("Current Price", f"${data['Current_Price']:.2f}" if pd.notna(data['Current_Price']) else "N/A")
                    st.metric("Sector", data['Sector'])
                with col2:
                    st.metric("P/E Ratio", f"{data['PE_Ratio']:.2f}" if pd.notna(data['PE_Ratio']) else "N/A")
                    st.metric("P/B Ratio", f"{data['PB_Ratio']:.2f}" if pd.notna(data['PB_Ratio']) else "N/A")
                    st.metric("Beta", f"{data['Beta']:.2f}" if pd.notna(data['Beta']) else "N/A")
                with col3:
                    st.metric("ROE", f"{data['ROE']:.2f}%" if pd.notna(data['ROE']) else "N/A")
                    st.metric("Profit Margin", f"{data['Profit_Margin']:.2f}%" if pd.notna(data['Profit_Margin']) else "N/A")
                    st.metric("Dividend Yield", f"{data['Dividend_Yield']:.2f}%" if pd.notna(data['Dividend_Yield']) else "N/A")
                df_temp = pd.DataFrame([data])
                valuation_score = calculate_valuation_score(df_temp.iloc[0])
                st.subheader("Valuation Score")
                st.progress(valuation_score / 100)
                st.write(f"**Score: {valuation_score:.2f} / 100**")
                ticker_obj = yf.Ticker(ticker_input.upper())
                hist = ticker_obj.history(period="6mo")
                if not hist.empty:
                    st.subheader("📈 Price History (Last 6 Months)")
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.plot(hist.index, hist['Close'], linewidth=2, color='steelblue')
                    ax.set_xlabel('Date'); ax.set_ylabel('Price ($)')
                    ax.set_title(f'{ticker_input.upper()} Price History (6 Months)')
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
            else:
                st.error(f"Could not fetch data for {ticker_input.upper()}. Please check the ticker symbol.")
        else:
            st.warning("Please enter a ticker symbol.")

st.sidebar.markdown("---")
st.sidebar.info("📊 **Data Source:** Yahoo Finance via yfinance\n\n⚠️ **Disclaimer:** This tool is for educational purposes only. Not financial advice.")
