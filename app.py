import streamlit as st
import math
import urllib.parse

# 1. Page Configuration
st.set_page_config(
    page_title="ProfitPath SL Pro", 
    page_icon="💰", 
    layout="centered"
)

# 2. Complete Language Dictionary
strings = {
    "English": {
        "title": "💰 ProfitPath SL Pro",
        "subtitle": "Professional Pricing for Sri Lankan Entrepreneurs",
        "prod_name": "Product Name",
        "batch": "Total units in this batch",
        "ing_cost": "Cost of ingredients (Rs.)",
        "pkg_cost": "Packaging per unit (Rs.)",
        "margin": "Desired Profit %",
        "waste": "Wastage Allowance (%)",
        "comp": "Competitor Price (Rs.)",
        "result_retail": "Suggested Selling Price",
        "result_profit": "Profit per Unit",
        "theme_label": "Dark Mode",
        "share": "Share Breakdown via WhatsApp",
        "msg": "Pricing for {name}: *Retail Rs. {price}*. Cost Rs. {cost}. Profit Rs. {prof}."
    },
    "සිංහල": {
        "title": "💰 ProfitPath SL Pro",
        "subtitle": "ශ්‍රී ලංකාවේ ව්‍යවසායකයින් සඳහා වෘත්තීය මිල ගණනය කිරීම්",
        "prod_name": "නිෂ්පාදනයේ නම",
        "batch": "මුළු ඒකක ගණන",
        "ing_cost": "අමුද්‍රව්‍ය පිරිවැය (රු.)",
        "pkg_cost": "ඇසුරුම් පිරිවැය (රු.)",
        "margin": "බලාපොරොත්තු වන ලාභ %",
        "waste": "අපතේ යාමේ ප්‍රතිශතය (%)",
        "comp": "තරඟකාරී මිල (රු.)",
        "result_retail": "විකුණුම් මිල",
        "result_profit": "ඒකකයක ලාභය",
        "theme_label": "අඳුරු ප්‍රකාරය",
        "share": "WhatsApp මගින් විස්තර යවන්න",
        "msg": "{name} සඳහා මිල: *විකුණුම් මිල රු. {price}*. පිරිවැය රු. {cost}. ලාභය රු. {prof}."
    },
    "தமிழ்": {
        "title": "💰 ProfitPath SL Pro",
        "subtitle": "இலங்கை தொழில்முயற்சியாளர்களுக்கான தொழில்முறை விலை நிர்ணயம்",
        "prod_name": "பொருளின் பெயர்",
        "batch": "மொத்த அலகுகள்",
        "ing_cost": "தேவையான பொருட்களின் விலை (ரூ.)",
        "pkg_cost": "பேக்கேஜிங் விலை (ரூ.)",
        "margin": "எதிர்பார்த்தும் லாபம் %",
        "waste": "வீணடிப்பு சதவீதம் (%)",
        "comp": "போட்டியாளர் விலை (ரூ.)",
        "result_retail": "விற்பனை விலை",
        "result_profit": "ஒரு அலகின் லாபம்",
        "theme_label": "டார்க் மோட்",
        "share": "WhatsApp மூலம் பகிரவும்",
        "msg": "{name} க்கான விலை: *விற்பனை விலை ரூ. {price}*. செலவு ரூ. {cost}. லாபம் ரூ. {prof}."
    }
}

# 3. Top Row: Language and Theme Selection
col_l, col_t = st.columns([2, 1])
with col_l:
    lang_choice = st.selectbox("Language / භාෂාව / மொழி", ["English", "සිංහල", "தமிழ்"])
    s = strings[lang_choice]
with col_t:
    dark_mode = st.toggle(s["theme_label"], value=False)

# 4. Universal High-Contrast Theme Engine
if dark_mode:
    bg_color = "#0E1117"
    txt_color = "#FFFFFF"
    input_bg = "#262730"
    metric_val = "#00FFAA" # Neon green for dark mode visibility
else:
    bg_color = "#FFFFFF"
    txt_color = "#121212" # Solid black for sunlight visibility
    input_bg = "#F0F2F6"
    metric_val = "#1D3557" # Deep blue for light mode visibility

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color} !important; color: {txt_color} !important; }}
    h1, h2, h3, p, span, label, .stMetric label {{ color: {txt_color} !important; }}
    [data-testid="stMetricValue"] {{ color: {metric_val} !important; font-weight: bold !important; }}
    .stTextInput input, .stNumberInput input {{ background-color: {input_bg} !important; color: {txt_color} !important; border: 1px solid {txt_color}22 !important; }}
    hr {{ border-color: {txt_color}44 !important; }}
    </style>
    """, unsafe_allow_html=True)

# 5. Application UI
st.title(s["title"])
st.write(s["subtitle"])
st.divider()

# Main Inputs
prod_name = st.text_input(s["prod_name"], value="Yethu Product #1")

col1, col2 = st.columns(2)
with col1:
    batch = st.number_input(s["batch"], min_value=1, value=10)
    ing_cost = st.number_input(s["ing_cost"], min_value=0.0, value=1000.0)
with col2:
    pkg_cost = st.number_input(s["pkg_cost"], min_value=0.0, value=50.0)
    margin = st.number_input(s["margin"], min_value=1, max_value=99, value=30)

# Advanced Settings (Wastage & Competitor)
with st.expander("Advanced Business Tools / උසස් මෙවලම්"):
    c_adv1, c_adv2 = st.columns(2)
    with c_adv1:
        wastage = st.number_input(s["waste"], min_value=0, max_value=50, value=5)
    with c_adv2:
        comp_price = st.number_input(s["comp"], min_value=0, value=0)

# 6. Core Logic
adjusted_ing_cost = ing_cost * (1 + (wastage/100))
total_batch_cost = adjusted_ing_cost + (pkg_cost * batch)
cost_per_unit = total_batch_cost / batch

# Margin Formula: Price = Cost / (1 - Margin%)
retail_price = math.ceil(cost_per_unit / (1 - (margin/100)))
profit_per_unit = retail_price - cost_per_unit

# 7. Final Results Display
st.divider()
res1, res2 = st.columns(2)
res1.metric(s["result_retail"], f"Rs. {retail_price}")
res2.metric(s["result_profit"], f"Rs. {math.floor(profit_per_unit)}")

# Market Feedback
if comp_price > 0:
    diff = retail_price - comp_price
    if diff > 0:
        st.warning(f"⚠️ Price is Rs. {diff} higher than competitor.")
    else:
        st.success(f"✅ Your price is Rs. {abs(diff)} cheaper! Competitive.")

st.divider()

# 8. WhatsApp Integration
msg_body = s["msg"].format(name=prod_name, price=retail_price, cost=round(cost_per_unit, 2), prof=round(profit_per_unit, 2))
whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(msg_body)}"

st.markdown(f'''
    <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
        <div style="background-color:#25D366; color:white; padding:15px; text-align:center; border-radius:10px; font-weight:bold; cursor:pointer;">
            {s["share"]}
        </div>
    </a>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 ProfitPath SL | Optimized for ables.app")