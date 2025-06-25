import streamlit as st
import pandas as pd
import re
import os
from glob import glob
from func import highlight_max_except_id
from datetime import timedelta

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

# Sidebar sa kontrolom prikaza kalkulatora
show_calc = st.sidebar.checkbox("Prikaži arbitražni kalkulator")

if show_calc:
    st.sidebar.header("Arbitražni kalkulator")
    option = st.sidebar.selectbox("Izaberi broj ishoda", options=[2, 3])

    if option == 2:
        k1 = st.sidebar.number_input("Kvote za ishod 1", min_value=1.01, format="%.2f", step=0.01, key="k1")
        k2 = st.sidebar.number_input("Kvote za ishod 2", min_value=1.01, format="%.2f", step=0.01, key="k2")
        kvote = [k1, k2]
    else:
        k1 = st.sidebar.number_input("Kvote za ishod 1", min_value=1.01, format="%.2f", step=0.01, key="k1")
        kx = st.sidebar.number_input("Kvote za ishod X", min_value=1.01, format="%.2f", step=0.01, key="kx")
        k2 = st.sidebar.number_input("Kvote za ishod 2", min_value=1.01, format="%.2f", step=0.01, key="k2")
        kvote = [k1, kx, k2]

    ulog = st.sidebar.number_input("Ukupni ulog (€)", min_value=1.0, format="%.2f", step=0.5, key="ulog")

    if st.sidebar.button("Izračunaj"):
        if option == 2:
            ulozi, profit = arbitrazni_kalkulator_2(kvote, ulog)
            st.sidebar.markdown(f"**Ulozi po ishodima:** {ulozi[0]} €, {ulozi[1]} €")
            st.sidebar.markdown(f"**Očekivani profit:** {profit} €")
        else:
            ulozi, profit = arbitrazni_kalkulator_3(kvote, ulog)
            st.sidebar.markdown(f"**Ulozi po ishodima:** {ulozi[0]} €, {ulozi[1]} €, {ulozi[2]} €")
            st.sidebar.markdown(f"**Očekivani profit:** {profit} €")

# Glavni prikaz utakmica

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
    title = f"⚽ {df.iloc[0]['domaci']} vs {df.iloc[0]['gosti']} — 🕒 {df.iloc[0]['vreme']} — {procenat}%"
    with st.expander(title):
        st.dataframe(df_new)


