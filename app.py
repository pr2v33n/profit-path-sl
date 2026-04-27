import streamlit as st
import math

# 1. Page Config
st.set_page_config(page_title="ProfitPath SL", layout="centered")

# 2. Language Data
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
        "theme_label": "Dark Mode"
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
        "theme_label": "අඳුරු ප්‍රකාරය"
    },
    "தமிழ்": {
        "title": "💰 ProfitPath SL",
        "subtitle": "உங்கள் விற்பனை விலையை எளிதாகக் கணக்கிடுங்கள்.",
        "prod_name": "பொருளின் பெயர்",
        "batch": "மொத்த அலகுகள்",
        "ing_cost": "தேவையான பொருட்களின் விலை (ரூ.)",
        "pkg_cost": "பேக்கேஜிங் விலை (ரூ.)",
        "margin": "எதிர்பார்த்தும் லாபம் %",
        "result_retail": "விற்பனை விலை",
        "result_profit": "ஒரு அலகின் லாபம்",
        "theme_label": "டார்க் மோட்"
    }
}

# 3. Theme State Logic
col_l, col_t = st.columns([2, 1])
with col_l:
    lang_choice = st.selectbox("Language / භාෂාව / மொழி", ["English", "සිංහල", "தமிழ்"])
    s = strings[lang_choice]
with col_t:
    dark_mode = st.toggle(s["theme_label"], value=False)

# 4. The "Invisible Text" Fix (Universal CSS)
if dark_mode:
    bg_color = "#0E1117"
    txt_color = "#FFFFFF"
    input_bg = "#262730"
else:
    bg_color = "#FFFFFF"
    txt_color = "#121212" # Strong dark black for high contrast
    input_bg = "#F0F2F6"

st.markdown(f"""
    <style>
    /* Global Background */
    .stApp {{
        background-color: {bg_color} !important;
    }}
    /* Target ALL text elements: headers, paragraphs, labels, and metrics */
    h1, h2, h3, p, span, label, .stMetric label, [data-testid="stMetricValue"] {{
        color: {txt_color} !important;
    }}
    /* Ensure input boxes are readable */
    .stTextInput input, .stNumberInput input {{
        background-color: {input_bg} !important;
        color: {txt_color} !important;
    }}
    /* Divider color adjust */
    hr {{
        border-color: {txt_color}55 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 5. Application Interface
st.title(s["title"])
st.write(s["subtitle"])
st.divider()

name = st.text_input(s["prod_name"], value="Yethu Product #1")

c1, c2 = st.columns(2)
with c1:
    batch = st.number_input(s["batch"], min_value=1, value=10)
    ing = st.number_input(s["ing_cost"], min_value=0.0, value=1000.0)
with c2:
    pkg = st.number_input(s["pkg_cost"], min_value=0.0, value=50.0)
    margin = st.number_input(s["margin"], min_value=1, max_value=99, value=30)

# Math
total_cost = ing + (pkg * batch)
cost_per_unit = total_cost / batch
retail_price = cost_per_unit / (1 - (margin/100))
profit_per_unit = retail_price - cost_per_unit

st.divider()
res1, res2 = st.columns(2)
res1.metric(s["result_retail"], f"Rs. {math.ceil(retail_price)}")
res2.metric(s["result_profit"], f"Rs. {math.floor(profit_per_unit)}")

st.caption("© 2026 ProfitPath SL | Empowering Local Businesses")