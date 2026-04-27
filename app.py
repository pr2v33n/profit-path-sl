import streamlit as st
import math
import urllib.parse
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="ProfitPath SL Pro", page_icon="💰", layout="centered")

# 2. Language Data
strings = {
    "English": {
        "title": "💰 ProfitPath SL Pro",
        "subtitle": "Professional Pricing for Sri Lankan Entrepreneurs",
        "calc_header": "Ingredient List (Edit or Delete rows below)",
        "add_item": "Add to List",
        "item_name": "Item Name",
        "item_price": "Price (Rs.)",
        "prod_name": "Product Name",
        "batch": "Total units in this batch",
        "pkg_cost": "Packaging per unit (Rs.)",
        "margin": "Desired Profit %",
        "waste": "Wastage Allowance (%)",
        "result_retail": "Suggested Selling Price",
        "result_profit": "Profit per Unit",
        "share": "Share via WhatsApp",
        "msg": "Pricing for {name}: *Retail Rs. {price}*. Cost Rs. {cost}. Profit Rs. {prof}."
    },
    "සිංහල": {
        "title": "💰 ProfitPath SL Pro",
        "subtitle": "ශ්‍රී ලංකාවේ ව්‍යවසායකයින් සඳහා වෘත්තීය මිල ගණනය කිරීම්",
        "calc_header": "අමුද්‍රව්‍ය ලැයිස්තුව (පේළි සංස්කරණය කරන්න හෝ මකන්න)",
        "add_item": "එක් කරන්න",
        "item_name": "අයිතමය",
        "item_price": "මිල (රු.)",
        "prod_name": "නිෂ්පාදනයේ නම",
        "batch": "මුළු ඒකක ගණන",
        "pkg_cost": "ඇසුරුම් පිරිවැය (රු.)",
        "margin": "බලාපොරොත්තු වන ලාභ %",
        "waste": "අපතේ යාමේ ප්‍රතිශතය (%)",
        "result_retail": "විකුණුම් මිල",
        "result_profit": "ඒකකයක ලාභය",
        "share": "WhatsApp මගින් යවන්න",
        "msg": "{name} සඳහා මිල: *විකුණුම් මිල රු. {price}*. පිරිවැය රු. {cost}. ලාභය රු. {prof}."
    },
    "தமிழ்": {
        "title": "💰 ProfitPath SL Pro",
        "subtitle": "இலங்கை தொழில்முயற்சியாளர்களுக்கான தொழில்முறை விலை நிர்ணயம்",
        "calc_header": "மூலப்பொருள் பட்டியல் (வரிசைகளை மாற்றவும் அல்லது நீக்கவும்)",
        "add_item": "சேர்க்கவும்",
        "item_name": "பொருள்",
        "item_price": "விலை (ரூ.)",
        "prod_name": "பொருளின் பெயர்",
        "batch": "மொத்த அலகுகள்",
        "pkg_cost": "பேக்கேஜிங் விலை (ரூ.)",
        "margin": "எதிர்பார்த்தும் லாபம் %",
        "waste": "வீணடிப்பு சதவீதம் (%)",
        "result_retail": "விற்பனை விலை",
        "result_profit": "ஒரு அலகின் லாபம்",
        "share": "WhatsApp மூலம் பகிரவும்",
        "msg": "{name} க்கான விலை: *விற்பனை விலை ரூ. {price}*. செலவு ரூ. {cost}. லாபம் ரூ. {prof}."
    }
}

# 3. Language & Theme Selection (With Icon)
col_l, col_t = st.columns([3, 1])
with col_l:
    lang_choice = st.selectbox("Language / භාෂාව / மொழி", ["English", "සිංහල", "தமிழ்"])
    s = strings[lang_choice]
with col_t:
    # Using an icon instead of text for the toggle
    dark_mode = st.toggle("🌙" if st.session_state.get('dark', False) else "☀️", value=False, key='dark')

# 4. Final Theme Logic (Forcing Contrast)
bg, txt, input_bg, met = ("#0E1117", "#FFFFFF", "#262730", "#00FFAA") if dark_mode else ("#FFFFFF", "#121212", "#F0F2F6", "#1D3557")

st.markdown(f"""
    <style>
    /* Force every possible text container to inherit the correct color */
    .stApp, div, span, label, p, h1, h2, h3 {{ background-color: {bg} !important; color: {txt} !important; }}
    [data-testid="stMetricValue"] {{ color: {met} !important; font-weight: 800 !important; font-size: 2.5rem !important; }}
    .stMetric label {{ color: {txt} !important; opacity: 0.8; }}
    input {{ background-color: {input_bg} !important; color: {txt} !important; border: 1px solid {txt}33 !important; }}
    /* Styling the data editor */
    div[data-testid="stTable"] {{ background-color: {input_bg}; }}
    </style>""", unsafe_allow_html=True)

st.title(s["title"])
st.caption(s["subtitle"])
st.divider()

# 5. Dynamic Data Editor (The "Delete/Modify" solution)
st.subheader(s["calc_header"])

if 'ing_df' not in st.session_state:
    st.session_state.ing_df = pd.DataFrame(columns=[s["item_name"], s["item_price"]])

# A simple form to add new rows quickly
with st.form("quick_add", clear_on_submit=True):
    ca, cb, cc = st.columns([2, 2, 1])
    new_item = ca.text_input(s["item_name"], key="new_item_name")
    new_price = cb.number_input(s["item_price"], min_value=0.0, key="new_item_price")
    add_btn = cc.form_submit_button(s["add_item"])
    if add_btn and new_item:
        new_row = pd.DataFrame({s["item_name"]: [new_item], s["item_price"]: [new_price]})
        st.session_state.ing_df = pd.concat([st.session_state.ing_df, new_row], ignore_index=True)

# The Data Editor: Users can click a cell to modify or select a row and hit "Delete" on their keyboard
edited_df = st.data_editor(
    st.session_state.ing_df, 
    num_rows="dynamic", # This enables the "Add" and "Delete" icons in the table
    use_container_width=True,
    key="ing_editor"
)
st.session_state.ing_df = edited_df # Sync the changes

total_ing_cost = edited_df[s["item_price"]].sum()
st.info(f"Total Ingredients: Rs. {total_ing_cost:,.2f}")

# 6. Production Inputs
st.divider()
prod_name = st.text_input(s["prod_name"], value="Yethu Product")
c1, c2 = st.columns(2)
with c1:
    batch = st.number_input(s["batch"], min_value=1, value=10)
    pkg = st.number_input(s["pkg_cost"], min_value=0.0, value=45.0)
with c2:
    margin = st.number_input(s["margin"], min_value=1, max_value=99, value=30)
    wastage = st.number_input(s["waste"], min_value=0, value=5)

# 7. Final Calculations
adj_ing_cost = total_ing_cost * (1 + (wastage/100))
cost_per_unit = (adj_ing_cost + (pkg * batch)) / batch
retail_price = math.ceil(cost_per_unit / (1 - (margin/100)))
profit_per_unit = retail_price - cost_per_unit

# 8. High-Impact Results
st.divider()
r1, r2 = st.columns(2)
r1.metric(s["result_retail"], f"Rs. {retail_price:,}")
r2.metric(s["result_profit"], f"Rs. {math.floor(profit_per_unit):,}")

# WhatsApp Sharing
msg = s["msg"].format(name=prod_name, price=retail_price, cost=round(cost_per_unit, 2), prof=round(profit_per_unit, 2))
wa_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
st.markdown(f'<a href="{wa_url}" target="_blank" style="text-decoration:none;"><div style="background:#25D366;color:white;padding:15px;text-align:center;border-radius:12px;font-weight:bold;font-size:1.1rem;">{s["share"]}</div></a>', unsafe_allow_html=True)