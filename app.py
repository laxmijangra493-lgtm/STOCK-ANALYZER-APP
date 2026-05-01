# python -m streamlit run app.py
import streamlit as st
from auth import register_user, login_user

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

# SESSION
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

menu = st.selectbox("Menu", ["Login", "Sign Up"])

# ---------------------------
# 🔐 LOGIN
# ---------------------------
if menu == "Login":
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.form_submit_button("Login"):
            if login_user(email, password):
                st.session_state["logged_in"] = True
                st.success("Login successful")

                # 🔁 Redirect
                st.switch_page("pages/dashboard.py")
            else:
                st.error("Invalid credentials")

# ---------------------------
# 🆕 SIGNUP
# ---------------------------
else:
    with st.form("signup_form"):
        name = st.text_input("Name")
        mobile = st.text_input("Mobile")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.form_submit_button("Sign Up"):
            if register_user(name, mobile, email, password):
                st.success("Account created")
            else:
                st.error("Email already exists")