import streamlit as st
import pandas as pd
import re
import os
from glob import glob
from func import highlight_max_except_id
from datetime import timedelta

def arbitrazni_kalkulator_2(kvote, ulog, tolerancija=1000):
    kvota_1, kvota_2 = kvote
    najmanja_razlika = float('inf') 
    najbolje_uloge = None 
    for i in range(int(ulog - tolerancija), int(ulog), 100):
        ulog_1 = (i / kvota_1) / ((1 / kvota_1) + (1 / kvota_2))
        ulog_2 = i - ulog_1
        ulog_1 = round(ulog_1 / 100) * 100  
        ulog_2 = round(ulog_2 / 100) * 100  
        profit_1 = ulog_1 * kvota_1 - i
        profit_2 = ulog_2 * kvota_2 - i
        razlika = abs(profit_1 - profit_2)
        if razlika < najmanja_razlika:
            najmanja_razlika = razlika
            najbolje_uloge = (ulog_1, ulog_2)
    i = sum(najbolje_uloge)
    profit_1 = najbolje_uloge[0] * kvota_1 - i
    profit_2 = najbolje_uloge[1] * kvota_2 - i
    profit = (profit_1 + profit_2) / 2 
    return najbolje_uloge, round(profit, 2)

def arbitrazni_kalkulator_3(kvote, ulog, tolerancija=1000):
    kvota_1, kvota_2, kvota_3 = kvote
    najmanja_razlika = float('inf')
    najbolje_uloge = None
    for i in range(int(ulog - tolerancija), int(ulog), 100):
        ulog_1 = (i / kvota_1) / ((1 / kvota_1) + (1 / kvota_2) + (1 / kvota_3))
        ulog_2 = (i / kvota_2) / ((1 / kvota_1) + (1 / kvota_2) + (1 / kvota_3))
        ulog_3 = i - ulog_1 - ulog_2
        ulog_1 = round(ulog_1 / 100) * 100
        ulog_2 = round(ulog_2 / 100) * 100
        ulog_3 = round(ulog_3 / 100) * 100
        profit_1 = ulog_1 * kvota_1 - i
        profit_2 = ulog_2 * kvota_2 - i
        profit_3 = ulog_3 * kvota_3 - i
        razlika = abs(profit_1 - profit_2) + abs(profit_1 - profit_3) + abs(profit_2 - profit_3)
        if razlika < najmanja_razlika:
            najmanja_razlika = razlika
            najbolje_uloge = (ulog_1, ulog_2, ulog_3)
    i = sum(najbolje_uloge)
    profit_1 = najbolje_uloge[0] * kvota_1 - i
    profit_2 = najbolje_uloge[1] * kvota_2 - i
    profit_3 = najbolje_uloge[2] * kvota_3 - i
    profit = (profit_1 + profit_2 + profit_3) / 3
    return najbolje_uloge, round(profit, 2)

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
    
    def safe_float(x):
        try:
            return float(x)
        except:
            return None
    
    k1_f = safe_float(k1)
    kx_f = safe_float(kx)
    k2_f = safe_float(k2)
    ulog = safe_float(ulog_str)
    
    if k1_f and k2_f and ulog and ulog > 0:
        if kx_f:
            ulozi, profit = arbitrazni_kalkulator_3([k1_f, kx_f, k2_f], ulog)
            st.sidebar.markdown(f"**Ulozi po ishodima:**\n- Ishod 1: {ulozi[0]} €\n- Ishod X: {ulozi[1]} €\n- Ishod 2: {ulozi[2]} €")
            st.sidebar.markdown(f"**Očekivani profit:** {profit} €")
        else:
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



