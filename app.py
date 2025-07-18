import streamlit as st
import pandas as pd

st.set_page_config(page_title="OfficeOps AI", page_icon="📋", layout="wide")

st.title("📋 OfficeOps AI – Your Intelligent Front-of-House Dashboard")
st.subheader("Welcome to your AI-powered office manager!")

st.markdown("""
This is your intelligent hub for managing visitors, supplies, access, compliance tasks,  
and communication with your building and security teams.
""")

st.success("✅ Connected to Streamlit successfully.")

# --- INVENTORY TRACKER ---
st.header("📦 Restaurant Supply & Inventory Tracker")

# Initialize inventory in session state
if "inventory" not in st.session_state:
    st.session_state.inventory = []

# --- Form to Add New Items ---
with st.form("inventory_add_form"):
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

# --- Low Stock Alert ---
low_stock_items = [item for item in st.session_state.inventory if item['Status'] in ["Low", "Out of Stock"]]
if low_stock_items:
    st.warning(f"⚠️ {len(low_stock_items)} item(s) need restocking!")
    for item in low_stock_items:
        st.write(f"- {item['Item']} ({item['Status']})")

# --- Inventory Table with Editable Fields ---
if st.session_state.inventory:
    st.subheader("🗃️ Current Inventory")

    df_inventory = pd.DataFrame(st.session_state.inventory)
    
    # Let user edit inventory directly in the table
    edited_df = st.data_editor(
        df_inventory,
        use_container_width=True,
        num_rows="dynamic",
        key="editable_inventory"
    )

    # Sync session state with edited data
    st.session_state.inventory = edited_df.to_dict("records")

    # --- Export Button ---
    st.download_button(
        "📥 Download Inventory as CSV",
        data=edited_df.to_csv(index=False).encode("utf-8"),
        file_name="restaurant_inventory.csv",
        mime="text/csv"
    )

    # --- Simple AI Assistant for Reorders ---
    if st.button("🤖 Suggest Reorders"):
        restock = edited_df[edited_df["Status"].isin(["Low", "Out of Stock"])]
        if not restock.empty:
            st.info("🔁 Suggested Reorders:")
            for _, row in restock.iterrows():
                st.write(f"• Reorder `{row['Item']}` — current status: {row['Status']}")
        else:
            st.success("✅ All items are well stocked!")



# --- Smarter AI Assistant for Reorders ---
if st.button("🤖 Suggest Reorders"):
    if "editable_inventory" in st.session_state:
        edited_df = pd.DataFrame(st.session_state["editable_inventory"]["edited_rows"])
        if not edited_df.empty:
            restock = edited_df[edited_df["Status"].isin(["Low", "Out of Stock"])]
            if not restock.empty:
                st.info("🔁 Smart Reorder Suggestions:")
                for _, row in restock.iterrows():
                    current_qty = row['Quantity']
                    item = row['Item']
                    status = row['Status']
                    
                    # Suggest reorder quantity
                    if status == "Out of Stock":
                        suggested_reorder = "10 units"
                    elif status == "Low":
                        suggested_reorder = "enough to bring stock to 10 units"
                    else:
                        suggested_reorder = "N/A"

                    st.write(f"• `{item}` is `{status}` → 📦 Reorder: **{suggested_reorder}** (current: `{current_qty}`)")
            else:
                st.success("✅ All items are well stocked!")
        else:
            st.info("ℹ️ No data to analyze. Add items first.")
    else:
        st.warning("⚠️ Inventory data not loaded yet. Please interact with the inventory first.")

