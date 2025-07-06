import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Dashboard Absensi Wajah", layout="wide")

st.title("📸 Dashboard Absensi Wajah")

# Tampilkan data absensi
if os.path.exists("attendance.xlsx"):
    df = pd.read_excel("attendance.xlsx")
    st.subheader("📋 Data Absensi")
    st.dataframe(df)
else:
    st.warning("File attendance.xlsx tidak ditemukan!")

# Load model
try:
    model = joblib.load("model.pkl")
    st.success("Model berhasil dimuat.")
except:
    st.error("Gagal memuat model.pkl")

# Prediksi nama (simulasi input teks)
st.subheader("🔍 Prediksi Manual (Simulasi)")
input_text = st.text_input("Masukkan teks atau fitur:")
if st.button("Prediksi"):
    if input_text:
        # Simulasi prediksi (ganti dengan logika asli)
        st.success(f"Hasil prediksi: {input_text}")
    else:
        st.warning("Silakan isi input terlebih dahulu.")
