import streamlit as st
import pandas as pd
import re
import os
from glob import glob
from datetime import timedelta

# Funkcije za kalkulatore
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

for file_path in csv_files:
    file_name = os.path.basename(file_path)  
    match = re.search(r'_(\d+(?:\.\d+)?)\.csv$', file_name)
    procenat = float(match.group(1)) if match else None
    
    df = pd.read_csv(file_path)
    df['vreme'] = pd.to_datetime(df['vreme']) + timedelta(hours=1)
    
    # Prikaži osnovne podatke utakmice kao naslov u expanderu
    title = f"⚽ {df.iloc[0]['domaci']} vs {df.iloc[0]['gosti']} — 🕒 {df.iloc[0]['vreme']} — {procenat}%"
    with st.expander(title):
        # Prikazujemo tabelu bez kolona domaci, gosti, vreme
        df_new = df.drop(columns=['vreme', 'domaci', 'gosti']).reset_index(drop=True)
        st.dataframe(df_new)
        
        # Unos ukupnog uloga za arbitražu
        ulog = st.number_input("Unesi ukupni ulog za arbitražu (€):", min_value=1.0, step=1.0, format="%.2f", key=file_name)
        
        # Čitamo kvote iz tabele (pretpostavljam da su kvote u kolonama, npr. prva 2 ili 3 kolone)
        kvote = df_new.columns.tolist()
        kvote_values = df_new.iloc[0].tolist()
        kvote_floats = []
        
        # Pretvaranje u float kvota (možeš prilagoditi ako je potrebno)
        try:
            kvote_floats = [float(k) for k in kvote_values if k and str(k) != 'nan']
        except:
            st.error("Greška pri parsiranju kvota!")
            continue
        
        # Izračun i prikaz rezultata
        if len(kvote_floats) == 2:
            ulozi, profit = arbitrazni_kalkulator_2(kvote_floats, ulog)
            st.write(f"Ulozi po ishodima: {ulozi[0]} €, {ulozi[1]} €")
            st.write(f"Očekivani profit: {profit} €")
        elif len(kvote_floats) == 3:
            ulozi, profit = arbitrazni_kalkulator_3(kvote_floats, ulog)
            st.write(f"Ulozi po ishodima: {ulozi[0]} €, {ulozi[1]} €, {ulozi[2]} €")
            st.write(f"Očekivani profit: {profit} €")
        else:
            st.info("Nisu pronađene 2 ili 3 kvote za arbitražni proračun.")




