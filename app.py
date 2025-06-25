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

show_calc = st.sidebar.checkbox("Prikaži arbitražni kalkulator", value=True)

if show_calc:
    st.sidebar.markdown("## Arbitražni kalkulator")
    st.sidebar.markdown("Unesi kvote i ulog. Ako treća kvota nije unesena, računa se kao 2-way.")
    
    k1 = st.sidebar.text_input("Kvote za ishod 1", key="k1")
    kx = st.sidebar.text_input("Kvote za ishod X (ostavi prazno za 2-way)", key="kx")
    k2 = st.sidebar.text_input("Kvote za ishod 2", key="k2")
    ulog_str = st.sidebar.text_input("Ukupni ulog (€)", key="ulog")
    
    # Pokušaj da parsiraš unose u float, ignoriši ako prazno ili nevalidno
    def safe_float(x):
        try:
            return float(x)
        except:
            return None
    
    k1_f = safe_float(k1)
    kx_f = safe_float(kx)
    k2_f = safe_float(k2)
    ulog = safe_float(ulog_str)
    
    # Provera minimalnih uslova da krenemo sa računom
    if k1_f and k2_f and ulog and ulog > 0:
        if kx_f:
            # 3-way kalkulator
            ulozi, profit = arbitrazni_kalkulator_3([k1_f, kx_f, k2_f], ulog)
            st.sidebar.markdown(f"**Ulozi po ishodima:**\n- Ishod 1: {ulozi[0]} €\n- Ishod X: {ulozi[1]} €\n- Ishod 2: {ulozi[2]} €")
            st.sidebar.markdown(f"**Očekivani profit:** {profit} €")
        else:
            # 2-way kalkulator bez ishoda X
            ulozi, profit = arbitrazni_kalkulator_2([k1_f, k2_f], ulog)
            st.sidebar.markdown(f"**Ulozi po ishodima:**\n- Ishod 1: {ulozi[0]} €\n- Ishod 2: {ulozi[1]} €")
            st.sidebar.markdown(f"**Očekivani profit:** {profit} €")
    else:
        st.sidebar.info("Unesite ispravne kvote (najmanje ishod 1 i ishod 2) i ulog > 0.")

# Prikaz utakmica (tvoj postojeći kod)

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


