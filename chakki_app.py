# import streamlit as st
# import firebase_admin
# from firebase_admin import credentials, db
# import json

# # Firebase connection using Streamlit Secrets
# if not firebase_admin._apps:
#     # ییہاں ہم فائل کے بجائے اسٹریم لٹ کے سیکرٹس استعمال کر رہے ہیں
#     key_dict = json.loads(st.secrets["firebase"]["key"])
#     cred = credentials.Certificate(key_dict)
#     firebase_admin.initialize_app(cred, {
#         'databaseURL': 'https://abu-chakki-app-default-rtdb.firebaseio.com/'
#     })
# st.set_page_config(page_title="Abu Ji ki Chakki", layout="wide")
# st.title("🌾 ابو جی کی اسمارٹ چکی")

# # --- Form (Naya Data) ---
# st.subheader("📝 نیا اندراج (New Entry)")
# with st.form("khata_form", clear_on_submit=True):
#     col1, col2 = st.columns(2)
#     with col1:
#         naam = st.text_input("گاہک کا نام")
#         wazan = st.number_input("آٹے کا وزن (کلو)", min_value=0.0)
#     with col2:
#         paise = st.number_input("رقم وصول کی", min_value=0.0)
#         submit = st.form_submit_button("محفوظ کریں")

#     if submit:
#         data = {"Name": naam, "Weight": wazan, "Paid": paise, "Bill": wazan * 120}
#         db.reference('Daily_Records').push(data)
#         st.success(f"✅ {naam} ka record save ho gaya!")

# # --- Search & Table (Purana Record) ---
# st.divider()
# st.subheader("🔍 ریکارڈ تلاش کریں (Search Record)")

# # Firebase se data lena
# ref = db.reference('Daily_Records')
# all_data = ref.get()

# if all_data:
#     df = pd.DataFrame.from_dict(all_data, orient='index')
    
#     # SEARCH BOX: Yahan naam likh kar search hoga
#     search_query = st.text_input("Naam likhein (Search by Name):")
    
#     if search_query:
#         # Sirf wo records dikhana jo naam se match karein
#         filtered_df = df[df['Name'].str.contains(search_query, case=False, na=False)]
#         st.dataframe(filtered_df[['Name', 'Weight', 'Bill', 'Paid']], use_container_width=True)
#     else:
#         # Agar search khali hai to saara data dikhao
#         st.dataframe(df[['Name', 'Weight', 'Bill', 'Paid']], use_container_width=True)
# else:
#     st.info("Abhi koi record nahi hai.")
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json
from datetime import datetime

# --- 1. Firebase Connection (Using Secrets) ---
if not firebase_admin._apps:
    try:
     if not firebase_admin._apps:
    try:
        # یہ لائن اسٹریم لٹ کے نئے فارمیٹ کے لیے ہے
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://abu-chakki-app-default-rtdb.firebaseio.com/'
        })
    except Exception as e:
        st.error(f"ایرر: {e}")

# --- 2. Page Configuration ---
st.set_page_config(page_title="Abu Ji ki Smart Chakki", layout="wide")
st.title("🌾 ابو جی کی اسمارٹ چکی")

# --- 3. Input Form (Naya Data) ---
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
        data = {
            "Customer_Name": naam,
            "Weight": wazan,
            "Total_Price": price,
            "Payment_Status": status,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # فائر بیس میں ڈیٹا بھیجنا
        db.reference('Daily_Records').push(data)
        st.success(f"✅ {naam} کا ریکارڈ محفوظ ہو گیا ہے!")
        st.balloons()
    else:
        st.warning("براہ کرم گاہک کا نام لکھیں۔")

# --- 4. Search & Display Data ---
st.divider()
st.subheader("🔍 ریکارڈ تلاش کریں (Search Record)")
search_name = st.text_input("گاہک کا نام لکھیں")

if st.button("تلاش کریں"):
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
