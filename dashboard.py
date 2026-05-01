
import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import sqlite3
import bcrypt
import pandas as pd # FIXED: Needed for checking if dataframe is empty

# 🔐 INIT SESSION (Removed st.stop() so your fallback login logic actually runs)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def show_logo():
    st.markdown("""
<style>
.logo-container {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 20px 10px;
}

.logo-icon {
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #22d3ee, #6366f1, #a855f7);
    clip-path: polygon(10% 90%, 40% 10%, 55% 40%, 75% 25%, 90% 10%, 90% 90%);
    position: relative;
}

.logo-text {
    font-size: 42px;
    font-weight: 600;
    font-family: 'Poppins', sans-serif;
    color: #e5e7eb;
}

.logo-text span {
    background: linear-gradient(135deg, #22d3ee, #6366f1, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.tagline {
    margin-top: -10px;
    margin-left: 80px;
    font-size: 14px;
    letter-spacing: 3px;
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(90deg, #22d3ee, #6366f1, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>

<div class="logo-container">
    <div class="logo-icon"></div>
    <div>
        <div class="logo-text">Analy<span>zr</span></div>
        <div class="tagline">INSIGHTS • ANALYSIS • GROWTH</div>
    </div>
</div>
""", unsafe_allow_html=True)

show_logo()

# --- Custom CSS ---
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;   
        }
        .title {
            font-size: 60px;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #cbd5e1;
            margin-bottom: 30px;
        }
        .card {
            background-color: #111827;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 0px 15px rgba(0,0,0,0.4);
        }
        .button {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="title">QuantIQ 📊</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart Stock Analysis & Market Intelligence Platform</div>', unsafe_allow_html=True)

# --- Feature Cards ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>📈 Real-Time Charts</h3>
        <p>Track stock movements with live market data and indicators.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>🧠 AI Insights</h3>
        <p>Get smart predictions using technical indicators like RSI & MA.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>⚡ Fast Analysis</h3>
        <p>Analyze multiple stocks instantly with optimized algorithms.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# --- CTA Section ---
st.markdown("""
    <div style="text-align:center;">
        <h2>Start your trading intelligence journey</h2>
        <p style="color:#94a3b8;">Built for traders, analysts, and learners.</p>
    </div>
""", unsafe_allow_html=True)    

# --- DB ---
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mobile TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

# --- FUNCTIONS ---
def register_user(name, mobile, email, password):
    # FIXED: Added .decode('utf-8') so it perfectly matches auth.py
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        c.execute("INSERT INTO users (name, mobile, email, password) VALUES (?, ?, ?, ?)",
                  (name, mobile, email, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError: # FIXED: Catch proper error
        return False

def login_user(email, password):
    c.execute("SELECT password FROM users WHERE email = ?", (email,))
    result = c.fetchone()

    if result:
        # FIXED: Added .encode('utf-8') to prevent TypeError and match auth.py
        stored_password = result[0].encode('utf-8') 
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return True
    return False

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if not st.session_state["logged_in"]:

    if choice == "Login":
        st.subheader("🔐 Login")

        with st.form("login_form_dashboard"): # Unique key for forms
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button("Login")   

            if submitted:
                if login_user(email, password):
                    st.session_state["logged_in"] = True
                    st.success("Logged in successfully")
                    st.rerun()   # optional but recommended
                else:
                    st.error("Invalid credentials")

    elif choice == "Sign Up":
        st.subheader("🚀 Create Account")

        with st.form("signup_form_dashboard"): # Unique key for forms
            name = st.text_input("Name")
            mobile = st.text_input("Mobile")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            submitted = st.form_submit_button("Sign Up")

            if submitted:
                if register_user(name, mobile, email, password):
                    st.success("Account created! Please login.")
                else:
                    st.error("Email already exists")

# ---------------------------
# 📊 DASHBOARD
# ---------------------------
else:
    col_left, col_right = st.columns([8, 1])

    with col_left:
        st.success("✅ Welcome to QuantIQ Dashboard")

    with col_right:
        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.rerun()

    if st.button("📈 Show NIFTY Chart"):
        stock = yf.Ticker("^NSEI")
        data_stock = stock.history(period="5d", interval="5m")

        # 2. Create the figure
        fig = go.Figure()

        # 3. Add the Candlestick trace with custom colors
        fig.add_trace(go.Candlestick(
            x=data_stock.index,
            open=data_stock['Open'],
            high=data_stock['High'],
            low=data_stock['Low'],
            close=data_stock['Close'],
            increasing_line_color='#00ff00', 
            decreasing_line_color='#ff0000'  
            ))

        # 4. Update the layout
        fig.update_layout(
            title="NIFTY 50",
            xaxis_title="Time",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False, 
            template="plotly_dark"           
        )

        # 5. Hide outside trading hours
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]), 
                dict(bounds=[15.5, 9.25], pattern="hour"), 
            ]
        )

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # 📊 SEARCH BAR (TradingView Style)
    # ---------------------------

    st.markdown("### 🔍 Search Stocks")

    search_col1, search_col2 = st.columns([8, 2])

    with search_col1:
        stock_input = st.text_input(
            "Search (e.g. RELIANCE.NS, TCS.NS, INFY.NS, ^NSEI)",
            placeholder="Type stock symbol..."
        )

    with search_col2:
        search_btn = st.button("Search")

    # Default stock
    if "stock_symbol" not in st.session_state:
        st.session_state["stock_symbol"] = "^NSEI"

    # When user searches
    if search_btn and stock_input:
        st.session_state["stock_symbol"] = stock_input.upper()

    # ---------------------------
    # 📈 LOAD STOCK DATA
    # ---------------------------
    symbol = st.session_state["stock_symbol"]
    
    # FIXED: Initialize data_stock here to prevent NameError on failure
    data_stock = pd.DataFrame() 

    try:
        stock = yf.Ticker(symbol)
        data_stock = stock.history(period="5d", interval="5m")

        if data_stock.empty:
            st.warning("⚠️ No data found. Try a valid symbol like RELIANCE.NS")
        else:
            # ---------------------------
            # 📊 CHART
            # ---------------------------
            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=data_stock.index,
                open=data_stock['Open'],
                high=data_stock['High'],
                low=data_stock['Low'],
                close=data_stock['Close'],
                increasing_line_color='#00ff00',
                decreasing_line_color='#ff0000'
            ))

            fig.update_layout(
                title=f"{symbol} Chart",
                xaxis_title="Time",
                yaxis_title="Price",
                xaxis_rangeslider_visible=False,
                template="plotly_dark"
            )

            fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),
                    dict(bounds=[15.5, 9.25], pattern="hour"),
                ]
            )

            st.plotly_chart(fig, use_container_width=True)

            # ---------------------------
            # 📊 STOCK INFO
            # ---------------------------
            info = stock.info

            col1 , col2 , col3 = st.columns(3)

            with col1:
                st.metric("P/E Ratio", info.get("trailingPE", "N/A"))

            with col2:
                st.metric("EPS", info.get("trailingEps", "N/A"))
            
            with col3:
                st.metric("Market Cap", info.get("marketCap", "N/A"))

    except Exception as e:
        st.error(f"Error loading stock: {e}")

    # ---------------------------
    # 📉 RSI INDICATOR (SEPARATE PANEL BELOW CHART)
    # ---------------------------

    def calculate_rsi(data, period=14):
        delta = data['Close'].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    if data_stock.empty:
        st.warning("⚠️ No data found")
    else:

        data_stock['RSI'] = calculate_rsi(data_stock)

        rsi_fig = go.Figure()

        rsi_fig.add_trace(go.Scatter(
            x=data_stock.index,
            y=data_stock['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color='cyan', width=2)
        ))

        rsi_fig.add_hline(y=70, line_dash="dash", line_color="red")
        rsi_fig.add_hline(y=30, line_dash="dash", line_color="green")

        rsi_fig.update_layout(
        title=f"{symbol} RSI (14)",
        template="plotly_dark",
        height=250,
        margin=dict(l=10, r=10, t=40, b=10)
        )

        st.plotly_chart(rsi_fig, use_container_width=True)