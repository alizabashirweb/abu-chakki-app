import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd

if not firebase_admin._apps:
    cred = credentials.Certificate("abu-chakki-app-firebase-adminsdk-fbsvc-8efe79a6bb.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://abu-chakki-app-default-rtdb.firebaseio.com/' 
    })

st.set_page_config(page_title="Abu Ji ki Chakki", layout="wide")
st.title("🌾 ابو جی کی اسمارٹ چکی")

# --- Form (Naya Data) ---
st.subheader("📝 نیا اندراج (New Entry)")
with st.form("khata_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        naam = st.text_input("گاہک کا نام")
        wazan = st.number_input("آٹے کا وزن (کلو)", min_value=0.0)
    with col2:
        paise = st.number_input("رقم وصول کی", min_value=0.0)
        submit = st.form_submit_button("محفوظ کریں")

    if submit:
        data = {"Name": naam, "Weight": wazan, "Paid": paise, "Bill": wazan * 120}
        db.reference('Daily_Records').push(data)
        st.success(f"✅ {naam} ka record save ho gaya!")

# --- Search & Table (Purana Record) ---
st.divider()
st.subheader("🔍 ریکارڈ تلاش کریں (Search Record)")

# Firebase se data lena
ref = db.reference('Daily_Records')
all_data = ref.get()

if all_data:
    df = pd.DataFrame.from_dict(all_data, orient='index')
    
    # SEARCH BOX: Yahan naam likh kar search hoga
    search_query = st.text_input("Naam likhein (Search by Name):")
    
    if search_query:
        # Sirf wo records dikhana jo naam se match karein
        filtered_df = df[df['Name'].str.contains(search_query, case=False, na=False)]
        st.dataframe(filtered_df[['Name', 'Weight', 'Bill', 'Paid']], use_container_width=True)
    else:
        # Agar search khali hai to saara data dikhao
        st.dataframe(df[['Name', 'Weight', 'Bill', 'Paid']], use_container_width=True)
else:
    st.info("Abhi koi record nahi hai.")
