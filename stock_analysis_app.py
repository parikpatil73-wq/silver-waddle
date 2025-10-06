import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yaml
import streamlit_authenticator as stauth
import smtplib
import ssl
import random
import time
from email.message import EmailMessage

# --------------------------
# Config & Helpers
# --------------------------
CONFIG_PATH = 'config.yaml'

def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

def save_config(cfg: dict):
    with open(CONFIG_PATH, 'w') as f:
        yaml.safe_dump(cfg, f)

# Email sending via SMTP (use your SMTP creds from Streamlit secrets)
SMTP_HOST = st.secrets.get('SMTP_HOST', '')
SMTP_PORT = int(st.secrets.get('SMTP_PORT', 587))
SMTP_USER = st.secrets.get('SMTP_USER', '')
SMTP_PASS = st.secrets.get('SMTP_PASS', '')
FROM_EMAIL = st.secrets.get('FROM_EMAIL', SMTP_USER)

def send_otp_email(to_email: str, otp: str):
    if not (SMTP_HOST and SMTP_USER and SMTP_PASS and FROM_EMAIL):
        st.error('Email is not configured. Set SMTP_* and FROM_EMAIL in Streamlit secrets.')
        return False
    msg = EmailMessage()
    msg['Subject'] = 'Your verification code'
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg.set_content(f"Your verification code is: {otp}. It expires in 10 minutes.")
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f'Failed to send email: {e}')
        return False

# OTP store in session
if 'otp_store' not in st.session_state:
    st.session_state.otp_store = {}

# --------------------------
# Authentication (existing login)
# --------------------------
cfg = load_config()
authenticator = stauth.Authenticate(
    cfg['credentials'],
    cfg['cookie']['name'],
    cfg['cookie']['key'],
    cfg['cookie']['expiry_days']
)

# Tabs for Auth actions
auth_tab = st.sidebar.radio('Account', ['Login', 'Sign up', 'Reset password'])

if auth_tab == 'Login':
    authenticator.login()
    if st.session_state.get('authentication_status'):
        st.success(f"Welcome {st.session_state.get('name')}!")
    elif st.session_state.get('authentication_status') is False:
        st.error('Username/password is incorrect')
    else:
        st.info('Please enter your username and password')

# --------------------------
# Sign up with Email OTP (adds to config.yaml)
# --------------------------
if auth_tab == 'Sign up':
    st.subheader('Create a new account')
    new_name = st.text_input('Full name')
    new_username = st.text_input('Username (unique)')
    new_email = st.text_input('Work email')
    new_password = st.text_input('Password', type='password')

    # Step 1: Send OTP
    if st.button('Send verification code'):
        if not (new_name and new_username and new_email and new_password):
            st.warning('Please fill all fields')
        elif new_username in cfg.get('credentials', {}).get('usernames', {}):
            st.error('Username already exists')
        else:
            otp = f"{random.randint(100000, 999999)}"
            st.session_state.otp_store[new_email] = {
                'otp': otp,
                'ts': time.time(),
                'payload': {
                    'name': new_name,
                    'username': new_username,
                    'password': new_password,
                    'email': new_email,
                }
            }
            if send_otp_email(new_email, otp):
                st.success('Verification code sent to your email')

    # Step 2: Verify OTP and create user
    code = st.text_input('Enter verification code')
    if st.button('Verify and create account'):
        item = st.session_state.otp_store.get(new_email)
        if not item:
            st.error('No code sent or session expired')
        else:
            if time.time() - item['ts'] > 600:
                st.error('Code expired. Please request a new one')
            elif code.strip() != item['otp']:
                st.error('Invalid code')
            else:
                # Hash password with streamlit_authenticator
                hashed_pw = stauth.Hasher([item['payload']['password']]).generate()[0]
                # Persist to config.yaml
                cfg = load_config()
                cfg.setdefault('credentials', {}).setdefault('usernames', {})
                cfg['credentials']['usernames'][item['payload']['username']] = {
                    'name': item['payload']['name'],
                    'password': hashed_pw,
                    'email': item['payload']['email']
                }
                save_config(cfg)
                st.success('Account created. You can now log in')
                # cleanup
                st.session_state.otp_store.pop(new_email, None)

# --------------------------
# Reset password with Email OTP
# --------------------------
if auth_tab == 'Reset password':
    st.subheader('Reset password')
    rp_username = st.text_input('Username')
    rp_email = st.text_input('Registered email')

    if st.button('Send reset code'):
        user = cfg.get('credentials', {}).get('usernames', {}).get(rp_username)
        if not user:
            st.error('Username not found')
        elif user.get('email') != rp_email:
            st.error('Email does not match our records')
        else:
            otp = f"{random.randint(100000, 999999)}"
            st.session_state.otp_store[rp_email] = {'otp': otp, 'ts': time.time(), 'username': rp_username}
            if send_otp_email(rp_email, otp):
                st.success('Reset code sent to your email')

    rp_code = st.text_input('Enter reset code')
    new_pw = st.text_input('New password', type='password')
    if st.button('Verify and update password'):
        item = st.session_state.otp_store.get(rp_email)
        if not item:
            st.error('No code sent or session expired')
        else:
            if time.time() - item['ts'] > 600:
                st.error('Code expired. Please request a new one')
            elif rp_code.strip() != item['otp']:
                st.error('Invalid code')
            else:
                hashed_pw = stauth.Hasher([new_pw]).generate()[0]
                cfg = load_config()
                cfg['credentials']['usernames'][item['username']]['password'] = hashed_pw
                save_config(cfg)
                st.success('Password updated. You can now log in')
                st.session_state.otp_store.pop(rp_email, None)

# --------------------------
# Main App (requires auth)
# --------------------------
if st.session_state.get('authentication_status'):
    st.title('📊 AI-Powered Multi-Stock Valuation Dashboard')

    tickers = st.sidebar.text_input('Enter Stock Tickers (comma separated)', 'AAPL, MSFT, NVDA')
    days = st.sidebar.selectbox('Historical Period (Days)', [30, 90, 180, 365], index=1)
    analyze = st.sidebar.button('Run Analysis')

    weights = {
        'Customer_Value': 0.10,
        'Unit_Economics': 0.15,
        'TAM': 0.10,
        'Competition': 0.10,
        'Risks': 0.15,
        'Valuation_Score': 0.40
    }

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

    if analyze:
        ticker_list = [t.strip().upper() for t in tickers.split(',') if t.strip()]
        results = []
        st.subheader('📈 Stock Comparison Dashboard')
        for ticker in ticker_list:
            current_price = fetch_current_price(ticker)
            if current_price is None:
                st.warning(f'Skipping {ticker}: could not fetch data.')
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
            df = df.sort_values(by='% Undervaluation', ascending=False).reset_index(drop=True)
            st.dataframe(df)
            st.markdown(f'### 📉 {days}-Day Historical Price Trends')
            fig, ax = plt.subplots(figsize=(10, 5))
            for ticker in ticker_list:
                hist = yf.Ticker(ticker).history(period=f'{days}d')
                if not hist.empty:
                    ax.plot(hist.index, hist['Close'], label=ticker)
            ax.set_xlabel('Date')
            ax.set_ylabel('Closing Price ($)')
            ax.legend()
            st.pyplot(fig)

    st.markdown('''
    ---
    ⚠️ This app is for educational/internal purposes only.
    Data from Yahoo Finance may be delayed/inaccurate.
    Always consult a qualified financial advisor before making investment decisions.
    ''')
