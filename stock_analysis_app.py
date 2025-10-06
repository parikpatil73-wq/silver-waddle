import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yaml
import streamlit_authenticator as stauth

# --------------------------
# Load Authentication
# --------------------------
with open('config.yaml') as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.success(f"Welcome {name}!")
    
    # --------------------------
    # App Title
    # --------------------------
    st.title("📊 AI-Powered Multi-Stock Valuation Dashboard")
    
    # Sidebar Inputs
    tickers = st.sidebar.text_input("Enter Stock Tickers (comma separated)", "AAPL, MSFT, NVDA")
    days = st.sidebar.selectbox("Historical Period (Days)", [30, 90, 180, 365], index=1)
    analyze = st.sidebar.button("Run Analysis")
    
    # Factor Weights
    weights = {
        'Customer_Value': 0.10,
        'Unit_Economics': 0.15,
        'TAM': 0.10,
        'Competition': 0.10,
        'Risks': 0.15,
        'Valuation_Score': 0.40
    }

    # Helper Functions
    def fetch_current_price(ticker):
        try:
            return yf.Ticker(ticker).info.get('regularMarketPrice')
        except Exception:
            return None

    def normalize(value, low, high):
        if value is None or np.isnan(value):
            return 50
        return max(0, min(100, (value - low) / (high - low) * 100))

    def score_factors_auto(ticker):
        t = yf.Ticker(ticker)
        info = t.info
        pe_ratio = info.get('trailingPE', np.nan)
        pb_ratio = info.get('priceToBook', np.nan)
        gross_margins = info.get('grossMargins', np.nan)
        operating_margins = info.get('operatingMargins', np.nan)
        revenue_growth = info.get('revenueGrowth', np.nan)
        beta = info.get('beta', np.nan)

        customer_value = normalize(gross_margins or 0.3, 0.1, 0.7)
        unit_economics = normalize(operating_margins or 0.2, 0.05, 0.4)
        tam = normalize(revenue_growth or 0.1, -0.1, 0.3)
        competition = 100 - normalize(pb_ratio or 5, 1, 15)
        risks = 100 - normalize(beta or 1.2, 0.5, 2.5)
        valuation_score = 100 - normalize(pe_ratio or 30, 5, 60)

        return {
            'Customer_Value': round(customer_value, 1),
            'Unit_Economics': round(unit_economics, 1),
            'TAM': round(tam, 1),
            'Competition': round(competition, 1),
            'Risks': round(risks, 1),
            'Valuation_Score': round(valuation_score, 1)
        }

    # --------------------------
    # Analysis
    # --------------------------
    if analyze:
        ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
        results = []
        st.subheader("📈 Stock Comparison Dashboard")

        for ticker in ticker_list:
            current_price = fetch_current_price(ticker)
            if current_price is None:
                st.warning(f"Skipping {ticker}: could not fetch data.")
                continue

            scores = score_factors_auto(ticker)
            weighted_score = sum(scores[f] * weights[f] for f in weights)
            intrinsic_value = current_price * (weighted_score / 100)
            undervaluation = (intrinsic_value - current_price) / current_price * 100

            results.append({
                'Ticker': ticker,
                'Current Price': round(current_price, 2),
                'Intrinsic Value': round(intrinsic_value, 2),
                '% Undervaluation': round(undervaluation, 2),
                'Weighted Score': round(weighted_score, 2),
                **scores
            })

        if results:
            df = pd.DataFrame(results)
            df = df.sort_values(by="% Undervaluation", ascending=False).reset_index(drop=True)
            st.dataframe(df)

            # Historical chart
            st.markdown(f"### 📉 {days}-Day Historical Price Trends")
            fig, ax = plt.subplots(figsize=(10, 5))
            for ticker in ticker_list:
                hist = yf.Ticker(ticker).history(period=f"{days}d")
                if not hist.empty:
                    ax.plot(hist.index, hist["Close"], label=ticker)
            ax.set_xlabel("Date")
            ax.set_ylabel("Closing Price ($)")
            ax.legend()
            st.pyplot(fig)

    # --------------------------
    # Disclaimer
    # --------------------------
    st.markdown("""
    ---
    ⚠️ This app is for educational/internal purposes only.  
    Data from Yahoo Finance may be delayed/inaccurate.  
    Always consult a qualified financial advisor before making investment decisions.
    """)
    
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
