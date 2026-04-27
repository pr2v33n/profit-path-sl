import streamlit as st
import math
import urllib.parse
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="ProfitPath SL", page_icon="💰", layout="wide")

# 2. Language Data
strings = {
    "English": {
        "title": "ProfitPath SL", "calc": "Costs", "biz": "Settings", "sum": "Results",
        "add": "Add", "i_name": "Item", "i_price": "Price", "unit": "Batch Units",
        "pkg": "Packaging", "margin": "Margin %", "waste": "Waste %", "retail": "Retail Price",
        "profit": "Profit", "share": "WhatsApp Share"
    },
    "සිංහල": {
        "title": "ProfitPath SL", "calc": "පිරිවැය", "biz": "සැකසුම්", "sum": "ප්‍රතිඵල",
        "add": "එක් කරන්න", "i_name": "අයිතමය", "i_price": "මිල", "unit": "ඒකක ගණන",
        "pkg": "ඇසුරුම්", "margin": "ලාභ %", "waste": "අපතේ %", "retail": "විකුණුම් මිල",
        "profit": "ලාභය", "share": "WhatsApp පණිවිඩය"
    },
    "தமிழ்": {
        "title": "ProfitPath SL", "calc": "செலவு", "biz": "அமைப்பு", "sum": "முடிவு",
        "add": "சேர்", "i_name": "பொருள்", "i_price": "விலை", "unit": "அலகுகள்",
        "pkg": "பேக்கேஜிங்", "margin": "லாபம் %", "waste": "வீணடிப்பு %", "retail": "விற்பனை விலை",
        "profit": "லாபம்", "share": "WhatsApp பகிர்வு"
    }
}

# 3. Header Logic
h_left, h_mid, h_right = st.columns([3, 1, 0.5])
with h_mid:
    lang = st.selectbox("Lang", ["English", "සිංහල", "தமிழ்"], label_visibility="collapsed")
    s = strings[lang]
with h_right:
    dark = st.toggle("🌙" if st.session_state.get('dark', False) else "☀️", value=True, key='dark')

# 4. Minimal Aesthetic CSS
if dark:
    bg, card, txt, accent, border, input_bg = "#0B0C10", "#141519", "#C5C6C7", "#66FCF1", "#1F2833", "#1F2833"
else:
    bg, card, txt, accent, border, input_bg = "#F8F9FA", "#FFFFFF", "#2D3436", "#0984E3", "#D1D8E0", "#FFFFFF"

st.markdown(f"""
    <style>
    /* Viewport Lock for Desktop */
    @media (min-width: 1024px) {{
        .main {{ height: 100vh; overflow: hidden; }}
    }}
    
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    
    /* Card/Tile Styling */
    [data-testid="column"] {{
        background-color: {card} !important;
        border: 1px solid {border};
        padding: 1.5rem !important;
        border-radius: 12px;
    }}
    
    /* Clean Typography */
    h1, h2, h3, label, p, span {{ color: {txt} !important; font-family: 'Inter', sans-serif; opacity: 0.95; }}
    
    /* Metric Styling - Fixing the "Too White" contrast */
    [data-testid="stMetricValue"] {{ color: {accent} !important; font-weight: 800; font-size: 2rem; }}
    [data-testid="stMetricLabel"] {{ color: {txt} !important; opacity: 0.6; }}
    
    /* Force Input & Editor colors to match Minimal Dark */
    .stTextInput input, .stNumberInput input, .stDataEditor div {{
        background-color: {input_bg} !important; 
        color: {txt} !important; 
        border: 1px solid {border} !important;
    }}
    
    /* Button Styling */
    .stButton button {{
        background-color: {input_bg};
        color: {txt};
        border: 1px solid {border};
        transition: 0.3s;
    }}
    .stButton button:hover {{ border-color: {accent}; color: {accent}; }}
    
    /* Expanders & Table Headers */
    .streamlit-expanderHeader {{ background-color: {card} !important; color: {txt} !important; }}
    </style>""", unsafe_allow_html=True)

# 5. Dashboard Layout
st.title(s["title"])

c_left, c_right = st.columns([1.3, 1], gap="small")

with c_left:
    st.subheader(f"📋 {s['calc']}")
    if 'ing_df' not in st.session_state:
        st.session_state.ing_df = pd.DataFrame(columns=["Item", "Price"])

    with st.container():
        ca, cb, cc = st.columns([2, 1.5, 0.8])
        ni = ca.text_input("N", placeholder=s["i_name"], label_visibility="collapsed", key="ni")
        np = cb.number_input("P", min_value=0.0, step=10.0, label_visibility="collapsed", key="np")
        if cc.button("➕"):
            if ni:
                nr = pd.DataFrame({"Item": [ni], "Price": [np]})
                st.session_state.ing_df = pd.concat([st.session_state.ing_df, nr], ignore_index=True)

    # Dynamic Editor - The width="stretch" satisfies the 2026 API
    edited = st.data_editor(
        st.session_state.ing_df, 
        num_rows="dynamic", 
        width="stretch", 
        height=300,
        column_config={
            "Item": st.column_config.TextColumn(s["i_name"]),
            "Price": st.column_config.NumberColumn(s["i_price"], format="Rs. %.2f")
        }
    )
    st.session_state.ing_df = edited
    total = edited["Price"].sum()

with c_right:
    st.subheader(f"⚙️ {s['biz']}")
    
    r1, r2 = st.columns(2)
    units = r1.number_input(s["unit"], min_value=1, value=10)
    pkg = r2.number_input(s["pkg"], min_value=0.0, value=0.0)
    
    r3, r4 = st.columns(2)
    margin = r3.number_input(s["margin"], min_value=1, max_value=99, value=30)
    waste = r4.number_input(s["waste"], min_value=0, value=5)

    # Calculation logic
    adj_cost = total * (1 + (waste/100))
    cpu = (adj_cost + (pkg * units)) / units
    retail = math.ceil(cpu / (1 - (margin/100))) if margin < 100 else 0
    prof = retail - cpu

    st.markdown(f"<div style='border-top: 1px solid {border}; margin: 20px 0;'></div>", unsafe_allow_html=True)
    st.subheader(f"📊 {s['sum']}")
    
    res1, res2 = st.columns(2)
    res1.metric(s["retail"], f"Rs. {retail:,}")
    res2.metric(s["profit"], f"Rs. {math.floor(prof):,}")

    # WhatsApp Share (The only "Bold" element left for CTAs)
    msg = f"*{s['title']}* | Retail: Rs. {retail} | Profit: Rs. {math.floor(prof)}"
    url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'''
        <a href="{url}" target="_blank" style="text-decoration:none;">
            <div style="background:{accent}; color:{bg}; padding:12px; text-align:center; border-radius:10px; font-weight:800; margin-top:10px;">
                {s["share"]}
            </div>
        </a>''', unsafe_allow_html=True)