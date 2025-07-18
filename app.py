import streamlit as st

st.set_page_config(page_title="OfficeOps AI", page_icon="📋", layout="wide")

st.title("📋 OfficeOps AI – Your Intelligent Front-of-House Dashboard")
st.subheader("Welcome to your AI-powered office manager!")

st.markdown("""
This is your intelligent hub for managing visitors, supplies, access, compliance tasks,  
and communication with your building and security teams.
""")

st.success("✅ Connected to Streamlit successfully.")


st.header("📦 Restaurant Supply & Inventory Tracker")

# Initialize inventory in session state
if "inventory" not in st.session_state:
    st.session_state.inventory = []

with st.form("inventory_form"):
    item_name = st.text_input("Ingredient / Item Name")
    quantity = st.text_input("Quantity (e.g. '2kg', '10 packs')")
    category = st.selectbox("Category", ["Fresh", "Dry", "Frozen", "Other"])
    status = st.selectbox("Stock Status", ["In Stock", "Low", "Out of Stock"])
    
    submitted = st.form_submit_button("Add to Inventory")

    if submitted and item_name and quantity:
        st.session_state.inventory.append({
            "Item": item_name,
            "Quantity": quantity,
            "Category": category,
            "Status": status
        })
        st.success("✅ Item added to inventory!")

# Display inventory table
if st.session_state.inventory:
    st.subheader("🗃️ Current Inventory")
    df_inventory = pd.DataFrame(st.session_state.inventory)
    st.dataframe(df_inventory)

