
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="PharmaStock",
    page_icon="💊",
    layout="wide"
)

st.title("💊 PharmaStock")
st.caption("Pharmacy Inventory Management System")

# Store medicines during the current session
if "medicines" not in st.session_state:
    st.session_state.medicines = []

# Dashboard
total = len(st.session_state.medicines)
stock = sum(m["Quantity"] for m in st.session_state.medicines)
low_stock = sum(
    1 for m in st.session_state.medicines
    if m["Quantity"] < 20
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Medicines", total)
col2.metric("Total Stock Units", stock)
col3.metric("Low Stock Items", low_stock)

st.divider()

# Add medicine
st.subheader("➕ Add New Medicine")

with st.form("medicine_form"):
    name = st.text_input("Medicine Name")
    batch = st.text_input("Batch Number")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    price = st.number_input("Price (₹)", min_value=0.0, step=0.5)
    expiry = st.date_input("Expiry Date")

    submitted = st.form_submit_button("Add Medicine")

    if submitted:
        if not name.strip() or not batch.strip():
            st.error("Enter medicine name and batch number.")
        elif any(
            m["Batch Number"] == batch.strip()
            for m in st.session_state.medicines
        ):
            st.error("This batch number already exists.")
        else:
            st.session_state.medicines.append({
                "Medicine": name.strip(),
                "Batch Number": batch.strip(),
                "Quantity": quantity,
                "Price": price,
                "Expiry Date": str(expiry)
            })
            st.success("Medicine added successfully!")
            st.rerun()

st.divider()

# Inventory table
st.subheader("📦 Medicine Inventory")

if st.session_state.medicines:
    df = pd.DataFrame(st.session_state.medicines)
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Download Inventory CSV",
        df.to_csv(index=False).encode("utf-8"),
        "pharmastock_inventory.csv",
        "text/csv"
    )
else:
    st.info("No medicines added yet. Start by adding one above.")

# Low stock alerts
st.subheader("⚠️ Stock Alerts")

for medicine in st.session_state.medicines:
    if medicine["Quantity"] < 20:
        st.warning(
            f"{medicine['Medicine']} — "
            f"Only {medicine['Quantity']} units left!"
        )
