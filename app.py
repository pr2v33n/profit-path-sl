import streamlit as st
import math

# Page Config for a professional look
st.set_page_config(page_title="ProfitPath SL", page_icon="💰")

st.title("💰 ProfitPath SL")
st.markdown("### Precision Pricing for Sri Lankan Vendors")

# Sidebar for inputs
st.sidebar.header("Product Details")
product_name = st.sidebar.text_input("Product Name", "Spicy Achcharu")
batch_size = st.sidebar.number_input("Units in Batch", min_value=1, value=10)

st.sidebar.header("Cost Breakdown")
ing_cost = st.sidebar.number_input("Total Ingredients (LKR)", min_value=0.0, value=1500.0)
pkg_cost = st.sidebar.number_input("Packaging per Unit (LKR)", min_value=0.0, value=45.0)

# Main Interaction
st.subheader(f"Pricing Strategy: {product_name}")
margin = st.slider("Target Profit Margin (%)", 10, 70, 30)

# Logic
total_cost = ing_cost + (pkg_cost * batch_size)
cost_per_unit = total_cost / batch_size
retail_price = cost_per_unit / (1 - (margin/100))
profit_per_unit = retail_price - cost_per_unit

# Display Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Cost / Unit", f"Rs. {cost_per_unit:.2f}")
col2.metric("Retail Price", f"Rs. {math.ceil(retail_price)}")
col3.metric("Profit / Unit", f"Rs. {profit_per_unit:.2f}")

# Summary Table
st.info(f"Selling at **Rs. {math.ceil(retail_price)}** gives you a total batch profit of **Rs. {profit_per_unit * batch_size:.2f}**")