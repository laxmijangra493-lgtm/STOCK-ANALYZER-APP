#  this is for dashboard:-

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
    col_left, col_right = st.columns([8, 4])

    with col_left:
        st.success("✅ Welcome to Analyzr Dashboard")

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
            increasing_line_color="#33e433", 
            decreasing_line_color='#ff0000'  
            ))
        fig.update_layout(hovermode = 'x unified')

        fig.update_xaxes(
            showspikes = True,
            spikemode = 'across',
            spikesnap = 'cursor'
        )

        fig.update_yaxes(
            showspikes = True,
            spikemode = 'across',
            spikesnap = 'cursor'
        )


    
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

    search_col1, search_col2  = st.columns([6 , 3])

    with search_col1:
        stock_input = st.text_input(
            "Search (e.g. RELIANCE.NS, TCS.NS, INFY.NS, ^NSEI)",
            placeholder="Type stock symbol..."
        )

    with search_col2:
        search_btn = st.button("Search")

    # with watchlistcol3:
        # watchlist_btn = st.button("<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-eye-icon lucide-eye"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/></svg>  Watchlist")


    # Default stock
    if "stock_symbol" not in st.session_state:
        st.session_state["stock_symbol"] = "^NSEI"

    # When user searches
    if search_btn and stock_input:
        st.session_state["stock_symbol"] = stock_input.upper()
    # if
    # ---------------------------
    # 📈 LOAD STOCK DATA
    # ---------------------------
    symbol = st.session_state["stock_symbol"]
    
    # FIXED: Initialize data_stock here to prevent NameError on failure
    data_stock = pd.DataFrame() 
    timeframe = st.selectbox(
        "Select Timeframe",
        ["1d" , "5d" , "1mo" , "6mo" , "1y" , "5y"]
    )  

    interval_map = {
    "1d": "5m",
    "5d": "15m",
    "1mo": "30m",
    "6mo": "1h",
    "1y": "1d",
    "5y": "1wk"
    }
    try:

        
        stock = yf.Ticker(symbol)
        data_stock = stock.history(period=timeframe, interval=interval_map[timeframe])
        data_stock = data_stock.tail(1000)

        if data_stock.empty:
            st.warning("⚠️ No data found. Try a valid symbol like RELIANCE.NS")
        else:
            # ---------------------------
            # 📊 CHART
            # --------------------------
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
                # fig.update_layout(hovermode = 'x unified')

                # fig.update_xaxes(
                #     showspikes = True,
                #     spikemode = 'across',
                #     spikesnap = 'cursor'
                #     )

                # fig.update_yaxes(
                #     showspikes = True,
                #     spikemode = 'across',
                #     spikesnap = 'cursor'
                #     )

                # fig = go.Figure()

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

    # def calculate_rsi(data, period=14):
    #     delta = data['Close'].diff()

    #     gain = delta.clip(lower=0)
    #     loss = -delta.clip(upper=0)

    #     avg_gain = gain.ewm(alpha=1/period,min_periods = period ,adjust=True).mean()
    #     avg_loss = loss.ewm(alpha=1/period,min_periods = period, adjust=True).mean()

    #     rs = avg_gain / avg_loss
    #     rsi = 100 - (100 / (1 + rs))

    #     return rsi
    def calculate_rsi_tv(close, period=14):
        delta = close.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

    # First average (SMA)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rsi = close.copy()
        rsi[:] = None

    # Start from first valid index
        for i in range(period, len(close)):
            if i == period:
            # first value already from SMA
                current_gain = avg_gain.iloc[i]
                current_loss = avg_loss.iloc[i]
            else:
            # Wilder smoothing
                current_gain = (avg_gain.iloc[i-1] * (period - 1) + gain.iloc[i]) / period
                current_loss = (avg_loss.iloc[i-1] * (period - 1) + loss.iloc[i]) / period

                avg_gain.iloc[i] = current_gain
                avg_loss.iloc[i] = current_loss

        # Avoid division by zero
            if current_loss == 0:
                rsi.iloc[i] = 100
            else:
                rs = current_gain / current_loss
                rsi.iloc[i] = 100 - (100 / (1 + rs))

        return rsi
    if data_stock.empty:
        st.warning("⚠️ No data found")
    else:

        data_stock['RSI'] = calculate_rsi_tv(data_stock['Close'])

        rsi_fig = go.Figure()
        rsi_fig.add_trace(go.Scatter(
        x=data_stock.index,
        y=data_stock['RSI'],
        mode='lines',
        name='RSI',
        line=dict(color='#00FFFF', width=2)
            ))

# Zones
        rsi_fig.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.1, line_width=0)
        rsi_fig.add_hrect(y0=0, y1=30, fillcolor="green", opacity=0.1, line_width=0)

# Levels
        rsi_fig.add_hline(y=70, line_dash="dash", line_color="red")
        rsi_fig.add_hline(y=50, line_dash="dot", line_color="gray")
        rsi_fig.add_hline(y=30, line_dash="dash", line_color="green")

        rsi_fig.update_layout(
            title=f"{symbol} RSI (14)",
            template="plotly_dark",
            height=250,
            margin=dict(l=10, r=10, t=40, b=10)
            )

        st.plotly_chart(rsi_fig, use_container_width=True)

        # rsi_fig.add_trace(go.Scatter(
        #     x=data_stock.index,
        #     y=data_stock['RSI'],
        #     mode='lines',
        #     name='RSI',
        #     line=dict(color='cyan', width=2)
        # ))

        # rsi_fig.add_hline(y=70, line_dash="dash", line_color="red")
        # rsi_fig.add_hline(y=30, line_dash="dash", line_color="green")

        # rsi_fig.update_layout(
        # title=f"{symbol} RSI (14)",
        # template="plotly_dark",
        # height=250,
        # margin=dict(l=10, r=10, t=40, b=10)
        # )

        # st.plotly_chart(rsi_fig, use_container_width=True)



# python -m streamlit run app.py
