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

# New imports for Gmail API and broker APIs
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
from typing import List, Tuple

# Broker SDKs
from ib_insync import IB
from kiteconnect import KiteConnect

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

# --------------------------
# Gmail API helper (read-only)
# --------------------------
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    token_file = 'token.json'
    client_config = st.secrets.get('GMAIL_OAUTH_CLIENT')
    if os.path.exists(token_file):
        try:
            from google.oauth2.credentials import Credentials
            creds = Credentials.from_authorized_user_file(token_file, GMAIL_SCOPES)
        except Exception:
            creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not client_config:
                st.warning('Set GMAIL_OAUTH_CLIENT in secrets to enable Gmail import.')
                return None
            flow = InstalledAppFlow.from_client_config(client_config, GMAIL_SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
    try:
        return build('gmail', 'v1', credentials=creds)
    except Exception as e:
        st.warning(f'Gmail build error: {e}')
        return None


def gmail_list_recent_subjects(service, max_items=25) -> List[str]:
    try:
        res = service.users().messages().list(userId='me', maxResults=max_items).execute()
        ids = [m['id'] for m in res.get('messages', [])]
        subjects = []
        for mid in ids:
            msg = service.users().messages().get(userId='me', id=mid, format='metadata', metadataHeaders=['Subject']).execute()
            hdrs = msg.get('payload', {}).get('headers', [])
            subj = next((h['value'] for h in hdrs if h['name'] == 'Subject'), '(no subject)')
            subjects.append(subj)
        return subjects
    except Exception as e:
        st.warning(f'Gmail list error: {e}')
        return []

# --------------------------
# Broker connectors
# --------------------------
class IBKRClient:
    def __init__(self):
        self.ib = IB()
    def connect(self, host='127.0.0.1', port=7497, clientId=1):
        try:
            self.ib.connect(host, port, clientId=clientId, timeout=5)
            return True
        except Exception as e:
            st.warning(f'IBKR connection failed: {e}')
            return False
    def get_positions(self) -> List[Tuple[str, float]]:
        try:
            positions = self.ib.positions()
            return [(p.contract.symbol.upper(), float(p.position)) for p in positions]
        except Exception as e:
            st.warning(f'IBKR positions error: {e}')
            return []

class ZerodhaClient:
    def __init__(self, api_key: str, access_token: str = None):
        self.kite = KiteConnect(api_key=api_key)
        if access_token:
            self.kite.set_access_token(access_token)
    def get_holdings(self) -> List[Tuple[str, float]]:
        try:
            holds = self.kite.holdings()
            return [(h['tradingsymbol'].upper(), float(h.get('quantity', 0) or 0)) for h in holds]
        except Exception as e:
            st.warning(f'Zerodha holdings error: {e}')
            return []

class ICICIDirectClient:
    def get_tickers_from_input(self, txt: str) -> List[str]:
        for s in ['\n', '\t', ';', ' ']:
            txt = txt.replace(s, ',')
        return [t.strip().upper() for t in txt.split(',') if t.strip()]

# Existing OTP email for auth

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

# Sidebar source selector and auth tab
source = st.sidebar.selectbox(
    'Import tickers from',
    ['Manual Input', 'Gmail (portfolio emails)', 'IBKR', 'Zerodha', 'ICICI Direct']
)

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
                hashed_pw = stauth.Hasher([item['payload']['password']]).generate()[0]
                cfg = load_config()
                cfg.setdefault('credentials', {}).setdefault('usernames', {})
                cfg['credentials']['usernames'][item['payload']['username']] = {
                    'name': item['payload']['name'],
                    'password': hashed_pw,
                    'email': item['payload']['email']
                }
                save_config(cfg)
                st.success('Account created. You can now log in')
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

    days = st.sidebar.selectbox('Historical Period (Days)', [30, 90, 180, 365], index=1)

    imported_tickers: List[str] = []
    if source == 'Manual Input':
        manual = st.sidebar.text_input('Enter Stock Tickers (comma separated)', 'AAPL, MSFT, NVDA')
        imported_tickers = [t.strip().upper() for t in manual.split(',') if t.strip()]

    elif source == 'Gmail (portfolio emails)':
        st.sidebar.caption('Authenticate once to read recent email subjects for tickers')
        if st.sidebar.button('Connect Gmail'):
            st.session_state.gmail_service_ready = True
        if st.session_state.get('gmail_service_ready'):
            svc = get_gmail_service()
            if svc:
                subs = gmail_list_recent_subjects(svc, max_items=25)
                st.sidebar.write('Recent Subjects:')
                for s in subs:
                    st.sidebar.write(f'- {s}')
                guess = ','.join(sorted({w.strip(' ,.;:()').upper() for s in subs for w in s.split() if w.isalpha() and len(w) <= 6}))
                gmail_tickers = st.sidebar.text_input('Tickers guessed from subjects (edit as needed)', guess)
                imported_tickers = [t.strip().upper() for t in gmail_tickers.split(',') if t.strip()]

    elif source == 'IBKR':
        with st.sidebar.expander('IBKR Connection'):
            host = st.text_input('Host', '127.0.0.1')
            port = st.number_input('Port', 0, 65535, 7497)
            client_id = st.number_input('Client ID', 1, 100, 1)
            if st.button('Connect IBKR'):
                ibc = IBKRClient()
                if ibc.connect(host, int(port), int(client_id)):
                    st.success('Connected to IBKR')
                    positions = ibc.get_positions()
                    imported_tickers = sorted({sym for sym, _ in positions})
                else:
                    st.warning('IBKR connect failed')

    elif source == 'Zerodha':
        with st.sidebar.expander('Zerodha Connection'):
            api_key = st.text_input('API Key', value=st.secrets.get('ZERODHA_API_KEY', ''))
            access_token = st.text_input('Access Token', type='password', value=st.secrets.get('ZERODHA_ACCESS_TOKEN', ''))
            if st.button('Fetch Holdings') and api_key and access_token:
                zc = ZerodhaClient(api_key=api_key, access_token=access_token)
                holds = zc.get_holdings()
                imported_tickers = sorted({sym for sym, _ in holds})

    elif source == 'ICICI Direct':
        with st.sidebar.expander('ICICI Direct Input'):
            raw = st.text_area('Paste tickers or portfolio symbols')
            ic = ICICIDirectClient()
            imported_tickers = ic.get_tickers_from_input(raw)

    if not imported_tickers:
        st.sidebar.info('No tickers imported yet. Use the selector above.')

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
