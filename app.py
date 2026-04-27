import streamlit as st
import math

# 1. Page Configuration & Theme State
st.set_page_config(page_title="ProfitPath SL", layout="centered")

# Language Dictionary
strings = {
    "English": {
        "title": "💰 ProfitPath SL",
        "subtitle": "Calculate your selling price easily.",
        "prod_name": "Product Name",
        "batch": "Total units made",
        "ing_cost": "Cost of ingredients (Rs.)",
        "pkg_cost": "Packaging per unit (Rs.)",
        "margin": "Desired Profit %",
        "result_retail": "Selling Price",
        "result_profit": "Profit per unit",
        "theme": "Dark Mode",
        "lang": "Language"
    },
    "සිංහල": {
        "title": "💰 ProfitPath SL",
        "subtitle": "ඔබේ විකුණුම් මිල පහසුවෙන් ගණනය කරන්න.",
        "prod_name": "නිෂ්පාදනයේ නම",
        "batch": "මුළු ඒකක ගණන",
        "ing_cost": "අමුද්‍රව්‍ය පිරිවැය (රු.)",
        "pkg_cost": "ඇසුරුම් පිරිවැය (රු.)",
        "margin": "බලාපොරොත්තු වන ලාභ %",
        "result_retail": "විකුණුම් මිල",
        "result_profit": "ඒකකයක ලාභය",
        "theme": "අඳුරු ප්‍රකාරය (Dark Mode)",
        "lang": "භාෂාව"
    },
    "தமிழ்": {
        "title": "💰 ProfitPath SL",
        "subtitle": "உங்கள் விற்பனை விலையை எளிதாகக் கணக்கிடுங்கள்.",
        "prod_name": "பொருளின் பெயர்",
        "batch": "மொத்த அலகுகள்",
        "ing_cost": "தேவையான பொருட்களின் விலை (ரூ.)",
        "pkg_cost": "பேக்கேஜிங் விலை (ரூ.)",
        "margin": "எதிர்பார்க்கும் லாபம் %",
        "result_retail": "விற்பனை விலை",
        "result_profit": "ஒரு அலகின் லாபம்",
        "theme": "டார்க் மோட்",
        "lang": "மொழி"
    }
}

# 2. UI Controls (Top Row)
col_l, col_t = st.columns([2, 1])
with col_l:
    lang = st.selectbox("", ["English", "සිංහල", "தமிழ்"])
with col_t:
    dark_mode = st.toggle(strings[lang]["theme"])

# Apply Theme via CSS
if dark_mode:
    st.markdown("""<style>stApp {background-color: #121212; color: white;}</style>""", unsafe_allow_html=True)

s = strings[lang]

# 3. Main Interface
st.title(s["title"])
st.write(s["subtitle"])
st.divider()

# Input Section (No Hidden Sliders)
name = st.text_input(s["prod_name"], value="Yethu Achcharu")

c1, c2 = st.columns(2)
with c1:
    batch = st.number_input(s["batch"], min_value=1, value=10)
    ing = st.number_input(s["ing_cost"], min_value=0.0, value=1000.0)
with c2:
    pkg = st.number_input(s["pkg_cost"], min_value=0.0, value=50.0)
    margin = st.number_input(s["margin"], min_value=1, max_value=99, value=30)

# 4. Calculation Logic
total_cost = ing + (pkg * batch)
cost_per_unit = total_cost / batch
# Simple, transparent retail price formula
retail_price = cost_per_unit / (1 - (margin/100))
profit_per_unit = retail_price - cost_per_unit

# 5. Results (Big and Bold)
st.divider()
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.success(f"### {s['result_retail']}\n# Rs. {math.ceil(retail_price)}")

with res_col2:
    st.info(f"### {s['result_profit']}\n# Rs. {math.floor(profit_per_unit)}")

st.caption("ProfitPath SL - Empowering Local Entrepreneurs")