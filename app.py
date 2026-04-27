import streamlit as st
import math
import urllib.parse
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import datetime

# 1. Page Configuration
st.set_page_config(page_title="ProfitPath SL Pro", page_icon="💰", layout="wide")

# 2. Language Data
strings = {
    "English": {
        "title": "ProfitPath SL Pro", "calc": "Costs", "biz": "Settings", "sum": "Results",
        "add": "Add", "i_name": "Item", "i_price": "Price", "unit": "Batch Units",
        "pkg": "Packaging", "margin": "Margin %", "waste": "Waste %", "retail": "Retail Price",
        "profit": "Profit", "revenue": "Total Revenue", "share": "WhatsApp Share", 
        "csv": "Export CSV", "pdf": "Download PDF Report"
    },
    "සිංහල": {
        "title": "ProfitPath SL Pro", "calc": "පිරිවැය", "biz": "සැකසුම්", "sum": "ප්‍රතිඵල",
        "add": "එක් කරන්න", "i_name": "අයිතමය", "i_price": "මිල", "unit": "ඒකක ගණන",
        "pkg": "ඇසුරුම්", "margin": "ලාභ %", "waste": "අපතේ %", "retail": "විකුණුම් මිල",
        "profit": "ලාභය", "revenue": "මුළු ආදායම", "share": "WhatsApp යවන්න", 
        "csv": "CSV ලබාගන්න", "pdf": "PDF වාර්තාව ලබාගන්න"
    },
    "தமிழ்": {
        "title": "ProfitPath SL Pro", "calc": "செலவு", "biz": "அமைப்பு", "sum": "முடிவு",
        "add": "சேர்", "i_name": "பொருள்", "i_price": "விலை", "unit": "அலகுகள்",
        "pkg": "பேக்கேஜிங்", "margin": "லாபம் %", "waste": "வீணடிப்பு %", "retail": "விற்பனை விலை",
        "profit": "லாபம்", "revenue": "மொத்த வருமானம்", "share": "WhatsApp பகிர்வு", 
        "csv": "CSV சேமி", "pdf": "PDF அறிக்கை"
    }
}

# 3. Theme State
if 'dark' not in st.session_state:
    st.session_state.dark = True

h_left, h_mid, h_right = st.columns([3, 1, 0.5])
with h_mid:
    lang = st.selectbox("Language", ["English", "සිංහල", "தமிழ்"], label_visibility="collapsed")
    s = strings[lang]
with h_right:
    dark = st.toggle("🌙" if st.session_state.dark else "☀️", value=st.session_state.dark, key='dark_toggle')
    st.session_state.dark = dark

# 4. CSS
if st.session_state.dark:
    bg, card, txt, accent, border, input_bg = "#0B0C10", "#141519", "#C5C6C7", "#66FCF1", "#1F2833", "#1F2833"
else:
    bg, card, txt, accent, border, input_bg = "#F8F9FA", "#FFFFFF", "#2D3436", "#0984E3", "#D1D8E0", "#FFFFFF"

st.markdown(f"""
    <style>
    @media (min-width: 1024px) {{ .main {{ height: 100vh; overflow: hidden; }} }}
    .stApp {{ background-color: {bg} !important; color: {txt} !important; }}
    [data-testid="column"] {{
        background-color: {card} !important; border: 1px solid {border};
        padding: 1.2rem !important; border-radius: 12px;
    }}
    h1, h2, h3, label, p, span {{ color: {txt} !important; font-family: 'Inter', sans-serif; }}
    [data-testid="stMetricValue"] {{ color: {accent} !important; font-weight: 800; font-size: 1.8rem; }}
    .stTextInput input, .stNumberInput input, [data-testid="stDataEditor"] {{
        background-color: {input_bg} !important; color: {txt} !important; border: 1px solid {border} !important;
    }}
    .stButton button {{ background-color: {input_bg}; color: {txt}; border: 1px solid {border}; border-radius: 8px; width: 100%; }}
    </style>""", unsafe_allow_html=True)

# 5. Corrected PDF Logic
def create_pdf(name, df, units, pkg, waste, total_ing, cpu, retail, prof):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(9, 132, 227)
    pdf.cell(0, 10, 'ProfitPath SL - Pricing Report', align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    clean_name = name.encode('ascii', 'ignore').decode('ascii') if name else "Product"
    pdf.cell(0, 10, f"Product: {clean_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 7, f"Date: {datetime.date.today()}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 7, f"Batch Size: {units} units | Wastage: {waste}% | Packaging: Rs. {pkg}/unit", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(100, 10, "Ingredient", border=1, align='C', fill=True)
    pdf.cell(40, 10, "Cost (Rs.)", border=1, align='C', fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font('helvetica', '', 10)
    for _, row in df.iterrows():
        item_text = str(row['Item']).encode('ascii', 'ignore').decode('ascii')
        pdf.cell(100, 8, item_text, border=1)
        pdf.cell(40, 8, f"{row['Price']:,.2f}", border=1, align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(5)
    
    pdf.set_fill_color(230, 245, 255)
    pdf.rect(10, pdf.get_y(), 140, 35, 'F')
    pdf.set_y(pdf.get_y() + 5)
    pdf.set_x(15)
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 7, f"Cost Per Unit: Rs. {cpu:,.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(15)
    pdf.cell(0, 7, f"Selling Price: Rs. {retail:,.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(15)
    pdf.set_font('helvetica', 'B', 13)
    pdf.set_text_color(9, 132, 227)
    pdf.cell(0, 10, f"Total Revenue Estimate: Rs. {retail * units:,.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # CRITICAL FIX: Convert bytearray to bytes for Streamlit
    return bytes(pdf.output())

# 6. Dashboard
st.title(f"💰 {s['title']}")
col1, col2 = st.columns([1.4, 1], gap="medium")

with col1:
    st.subheader(f"📋 {s['calc']}")
    if 'ing_df' not in st.session_state:
        st.session_state.ing_df = pd.DataFrame(columns=["Item", "Price"])

    with st.container():
        ca, cb, cc = st.columns([2, 1, 0.5])
        ni = ca.text_input("N", placeholder=s["i_name"], label_visibility="collapsed", key="ni")
        np = cb.number_input("P", min_value=0.0, step=1.0, label_visibility="collapsed", key="np")
        if cc.button("➕"):
            if ni:
                new_row = pd.DataFrame({"Item": [ni], "Price": [np]})
                st.session_state.ing_df = pd.concat([st.session_state.ing_df, new_row], ignore_index=True)

    edited_df = st.data_editor(st.session_state.ing_df, num_rows="dynamic", width="stretch", height=280)
    st.session_state.ing_df = edited_df
    total_ing = edited_df["Price"].sum()

with col2:
    st.subheader(f"⚙️ {s['biz']}")
    p_name = st.text_input("Name", value="My Product", label_visibility="collapsed")
    r1, r2 = st.columns(2)
    units = r1.number_input(s["unit"], min_value=1, value=10)
    pkg = r2.number_input(s["pkg"], min_value=0.0, value=0.0)
    r3, r4 = st.columns(2)
    margin = r3.number_input(s["margin"], min_value=1, max_value=99, value=30)
    waste = r4.number_input(s["waste"], min_value=0, value=5)

    waste_adj = total_ing * (1 + (waste/100))
    cpu = (waste_adj + (pkg * units)) / units
    retail = math.ceil(cpu / (1 - (margin/100))) if margin < 100 else 0
    prof = retail - cpu

    st.markdown(f"<div style='border-top:1px solid {border}; margin: 15px 0;'></div>", unsafe_allow_html=True)
    st.subheader(f"📊 {s['sum']}")
    m1, m2 = st.columns(2)
    m1.metric(s["retail"], f"Rs. {retail:,}")
    m2.metric(s["profit"], f"Rs. {math.floor(prof):,}")
    st.metric(s["revenue"], f"Rs. {retail * units:,}")

    # PDF Download Button
    try:
        pdf_bytes = create_pdf(p_name, edited_df, units, pkg, waste, total_ing, cpu, retail, prof)
        st.download_button(s["pdf"], pdf_bytes, f"{p_name}_Report.pdf", "application/pdf")
    except Exception as e:
        st.error(f"Error: {e}")

    wa_msg = f"*{p_name}* | Price: Rs. {retail} | Profit: Rs. {math.floor(prof)}"
    st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(wa_msg)}" target="_blank" style="text-decoration:none;"><div style="background:{accent}; color:{bg}; padding:10px; text-align:center; border-radius:10px; font-weight:800; margin-top:5px;">{s["share"]}</div></a>', unsafe_allow_html=True)