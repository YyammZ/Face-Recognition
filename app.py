import streamlit as st
import pandas as pd
import joblib

# Judul
st.title("Dashboard Absensi Wajah")

# Load model
model = joblib.load("model.pkl")

# Load data absensi
absen = pd.read_excel("attendance.xlsx")

# Tampilkan data absensi
st.subheader("Data Absensi")
st.dataframe(absen)

# Form input untuk prediksi manual
st.subheader("Prediksi Manual")
name = st.text_input("Masukkan nama siswa")
if st.button("Prediksi"):
    # contoh dummy prediksi, sesuaikan dengan model asli kamu
    st.success(f"Prediksi berhasil untuk {name}")
