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

import streamlit as st

# Jednostavan arbitražni kalkulator za 2 ishoda
def arbitrazni_kalkulator_2(kvote, ulog):
    k1, k2 = kvote
    ukupno = (1/k1) + (1/k2)
    if ukupno >= 1:
        return None, None  # Nema arbitraže
    ulog_1 = (ulog / k1) / ukupno
    ulog_2 = (ulog / k2) / ukupno
    profit = ulog_1 * k1 - ulog
    return (round(ulog_1, 2), round(ulog_2, 2)), round(profit, 2)

st.set_page_config(page_title="Arbitražni Kalkulator", layout="wide", initial_sidebar_state="collapsed")

st.title("📊 ARBITRAŽNI KALKULATOR")

# Dugme za prikaz/sakrivanje kalkulatora u sidebaru
if "show_calc" not in st.session_state:
    st.session_state["show_calc"] = False

if st.button("🧮 Prikaži / Sakrij arbitražni kalkulator"):
    st.session_state["show_calc"] = not st.session_state["show_calc"]

if st.session_state["show_calc"]:
    with st.sidebar:
        st.header("⚖️ Kalkulator za 2 ishoda")
        k1 = st.number_input("Kvota 1", min_value=1.01, step=0.01, value=2.0, key="k1")
        k2 = st.number_input("Kvota 2", min_value=1.01, step=0.01, value=2.0, key="k2")
        ulog = st.number_input("Ukupan ulog (€)", min_value=1.0, step=1.0, value=100.0, key="ulog")

        if st.button("Izračunaj arbitražu", key="calc_btn"):
            rezultati, profit = arbitrazni_kalkulator_2((k1, k2), ulog)
            if rezultati is None:
                st.error("❌ Nema arbitraže za ove kvote.")
            else:
                st.success(f"✅ Profit: {profit} €")
                st.write(f"Ulog na kvotu 1: **{rezultati[0]} €**")
                st.write(f"Ulog na kvotu 2: **{rezultati[1]} €**")

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

