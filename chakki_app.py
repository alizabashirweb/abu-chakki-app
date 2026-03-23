import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# --- 1. Firebase Connection (Using Secrets) ---
if not firebase_admin._apps:
    try:
        # Secrets se data dictionary format mein lena
        firebase_info = dict(st.secrets["firebase"])
        cred = credentials.Certificate(firebase_info)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://abu-chakki-app-default-rtdb.firebaseio.com/'
        })
    except Exception as e:
        st.error(f"کنکشن میں مسئلہ ہے: {e}")

# --- 2. Page Configuration ---
st.set_page_config(page_title="Abu Ji ki Smart Chakki", layout="wide")
st.title("🌾 ابو جی کی اسمارٹ چکی")

# --- 3. Input Form ---
st.subheader("📝 نیا اندراج (New Entry)")
with st.form("khata_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        naam = st.text_input("گاہک کا نام")
        wazan = st.number_input("آٹے کا وزن (کلو)", min_value=0.0, step=0.1)
    with col2:
        price = st.number_input("کل رقم (روپے)", min_value=0, step=10)
        status = st.selectbox("ادائیگی کی حالت", ["ادا شدہ (Paid)", "ادھار (Pending)"])
    
    submit_button = st.form_submit_button("محفوظ کریں")

if submit_button:
    if naam:
        try:
            data = {
                "Customer_Name": naam,
                "Weight": wazan,
                "Total_Price": price,
                "Payment_Status": status,
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            db.reference('Daily_Records').push(data)
            st.success(f"✅ {naam} کا ریکارڈ محفوظ ہو گیا ہے!")
            st.balloons()
        except Exception as e:
            st.error(f"ڈیٹا محفوظ نہیں ہو سکا: {e}")
    else:
        st.warning("براہ کرم گاہک کا نام لکھیں۔")

# --- 4. Search & Display Data ---
st.divider()
st.subheader("🔍 ریکارڈ تلاش کریں (Search Record)")
search_name = st.text_input("گاہک کا نام لکھیں")

if st.button("تلاش کریں"):
    try:
        records = db.reference('Daily_Records').get()
        if records:
            found = False
            for key, val in records.items():
                if search_name.lower() in val['Customer_Name'].lower():
                    st.write(f"📅 تاریخ: {val['Date']} | ⚖️ وزن: {val['Weight']}kg | 💰 رقم: {val['Total_Price']} | 📌 حالت: {val['Payment_Status']}")
                    found = True
            if not found:
                st.info("کوئی ریکارڈ نہیں ملا۔")
        else:
            st.info("ابھی تک کوئی ڈیٹا موجود نہیں ہے۔")
    except Exception as e:
        st.error(f"ڈیٹا لوڈ کرنے میں مسئلہ: {e}")
