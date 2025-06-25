import streamlit as st
import pandas as pd
import re
import os
from glob import glob
from func import highlight_max_except_id
from datetime import timedelta

st.set_page_config(page_title="Kvote", layout="wide")
st.title("  📊 ARB UTAKMICE  ")

folder_path = "csv"  
csv_files = glob(os.path.join(folder_path, "*.csv"))

for file_path in csv_files:
    file_name = os.path.basename(file_path)  
    match = re.search(r'_(\d+(?:\.\d+)?)\.csv$', file_name)
    procenat = float(match.group(1)) if match else None
    df = pd.read_csv(file_path)
    df['vreme'] = pd.to_datetime(df['vreme']) + timedelta(hours=1)
    df_new = df.drop(columns=['vreme', 'domaci', 'gosti']).reset_index(drop=True)
    df_new = highlight_max_except_id(df_new)  
    title = f"⚽ {df.iloc[0]['domaci']} vs {df.iloc[0]['gosti']}  —  🕒 {df.iloc[0]['vreme']}  —  {procenat}%"
    with st.expander(title):
      st.dataframe(df_new)  

# Prikaz arbitražnog kalkulatora u sidebaru na klik
if "show_calculator" not in st.session_state:
    st.session_state["show_calculator"] = False

if st.button("🧮 Prikaži / sakrij arbitražni kalkulator"):
    st.session_state["show_calculator"] = not st.session_state["show_calculator"]

if st.session_state["show_calculator"]:
    with st.sidebar:
        st.header("⚖️ Arbitražni kalkulator (3 ishoda)")

        k1 = st.number_input("Kvota 1", min_value=1.01, value=2.5, step=0.01, key="k1_arb")
        kx = st.number_input("Kvota X", min_value=1.01, value=3.2, step=0.01, key="kx_arb")
        k2 = st.number_input("Kvota 2", min_value=1.01, value=2.7, step=0.01, key="k2_arb")
        ulog = st.number_input("Ukupan ulog", min_value=100, value=1000, step=100, key="ulog_arb")
        tolerancija = st.number_input("Tolerancija (razlika)", min_value=0, value=1000, step=100, key="tol_arb")

        if st.button("📊 Izračunaj arbitražu"):
            kvote = (k1, kx, k2)
            try:
                uloge, profit, roi = arbitrazni_kalkulator_3(kvote, ulog, tolerancija)
                st.success(f"✅ PROFIT: {profit:.2f} €  |  ROI: {roi:.2f}%")
                st.write(f"Ulog 1: **{uloge[0]:.2f} €**")
                st.write(f"Ulog X: **{uloge[1]:.2f} €**")
                st.write(f"Ulog 2: **{uloge[2]:.2f} €**")
            except Exception as e:
                st.error(f"Greška: {e}")
