import streamlit as st
import pandas as pd
import re
import os
from glob import glob
from func import highlight_max_except_id
from datetime import timedelta

# Arbitražni kalkulatori
def arbitrazni_kalkulator_2(kvote, ulog):
    k1, k2 = kvote
    ulog_1 = ulog / (1 + k1/k2)
    ulog_2 = ulog - ulog_1
    profit = ulog_1 * k1 - ulog
    return (round(ulog_1, 2), round(ulog_2, 2)), round(profit, 2)

def arbitrazni_kalkulator_3(kvote, ulog):
    k1, kx, k2 = kvote
    inv_sum = 1/k1 + 1/kx + 1/k2
    ulog_1 = ulog / (k1 * inv_sum)
    ulog_x = ulog / (kx * inv_sum)
    ulog_2 = ulog / (k2 * inv_sum)
    profit = ulog_1 * k1 - ulog
    return (round(ulog_1,2), round(ulog_x,2), round(ulog_2,2)), round(profit, 2)

st.set_page_config(page_title="Kvote", layout="wide")
st.title("📊 ARB UTAKMICE")

folder_path = "csv"  
csv_files = glob(os.path.join(folder_path, "*.csv"))

# Kontrola za prikaz sidebar kalkulatora
if "show_calculator" not in st.session_state:
    st.session_state["show_calculator"] = False

if st.button("🧮 Prikaži / sakrij arbitražni kalkulator"):
    st.session_state["show_calculator"] = not st.session_state["show_calculator"]

# Prikaz utakmica
for file_path in csv_files:
    file_name = os.path.basename(file_path)  
    match = re.search(r'_(\d+(?:\.\d+)?)\.csv$', file_name)
    procenat = float(match.group(1)) if match else None
    df = pd.read_csv(file_path)
    df['vreme'] = pd.to_datetime(df['vreme']) + timedelta(hours=1)
    df_new = df.drop(columns=['vreme', 'domaci', 'gosti']).reset_index(drop=True)
    df_new = highlight_max_except_id(df_new)  
    title = f"⚽ {df.iloc[0]['domaci']} vs {df.iloc[0]['gosti']} — 🕒 {df.iloc[0]['vreme']} — {procenat}%"
    with st.expander(title):
        st.dataframe(df_new)

# Sidebar arbitražni kalkulator
if st.session_state["show_calculator"]:
    with st.sidebar:
        st.header("⚖️ Arbitražni kalkulator")

        mode = st.radio("Izaberi tip kalkulatora:", ("2-way (dva ishoda)", "3-way (tri ishoda)"))

        if mode == "2-way (dva ishoda)":
            k1 = st.number_input("Kvota 1", min_value=1.01, value=2.0, step=0.01, key="k1_arb")
            k2 = st.number_input("Kvota 2", min_value=1.01, value=2.0, step=0.01, key="k2_arb")
            ulog = st.number_input("Ukupan ulog (€)", min_value=1, value=100, step=1, key="ulog_arb")

            if st.button("Izračunaj 2-way arbitražu"):
                kvote = (k1, k2)
                uloge, profit = arbitrazni_kalkulator_2(kvote, ulog)
                st.success(f"Profit: {profit} €")
                st.write(f"Ulog na 1: **{uloge[0]} €**")
                st.write(f"Ulog na 2: **{uloge[1]} €**")

        else:
            k1 = st.number_input("Kvota 1", min_value=1.01, value=2.0, step=0.01, key="k1_arb_3")
            kx = st.number_input("Kvota X", min_value=1.01, value=3.0, step=0.01, key="kx_arb_3")
            k2 = st.number_input("Kvota 2", min_value=1.01, value=2.0, step=0.01, key="k2_arb_3")
            ulog = st.number_input("Ukupan ulog (€)", min_value=1, value=100, step=1, key="ulog_arb_3")

            if st.button("Izračunaj 3-way arbitražu"):
                kvote = (k1, kx, k2)
                uloge, profit = arbitrazni_kalkulator_3(kvote, ulog)
                st.success(f"Profit: {profit} €")
                st.write(f"Ulog na 1: **{uloge[0]} €**")
                st.write(f"Ulog na X: **{uloge[1]} €**")
                st.write(f"Ulog na 2: **{uloge[2]} €**")


