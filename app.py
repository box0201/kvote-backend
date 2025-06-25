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

# Globalni spisak odabranih kvota za kalkulator
if 'selected_odds' not in st.session_state:
    st.session_state['selected_odds'] = []

def prikazi_utakmicu(df, procenat):
    # Prikaz utakmice i interaktivni izbor kvota
    domaci = df.iloc[0]['domaci']
    gosti = df.iloc[0]['gosti']
    vreme = df.iloc[0]['vreme'] + timedelta(hours=1)
    
    st.write(f"⚽ **{domaci} vs {gosti}**  —  🕒 {vreme}  —  {procenat}%")

    # Pretpostavimo da su kvote u kolonama posle 'gosti', npr: ['1', 'X', '2', 'GG', 'NG', ...]
    kvote_df = df.drop(columns=['vreme', 'domaci', 'gosti']).reset_index(drop=True)
    
    # Napravi checkbox za svaku kvotu po koloni
    for col in kvote_df.columns:
        kvota = kvote_df.loc[0, col]
        key = f"{domaci}_{gosti}_{col}"
        # Checkbox za izbor kvote
        izabrano = st.checkbox(f"{col}: {kvota}", key=key)
        
        if izabrano:
            # Dodaj u globalni izbor kvota ako nije već tu
            if (domaci, gosti, col, kvota) not in st.session_state['selected_odds']:
                st.session_state['selected_odds'].append((domaci, gosti, col, kvota))
        else:
            # Ako checkbox nije štikliran, ukloni iz izbora ako postoji
            if (domaci, gosti, col, kvota) in st.session_state['selected_odds']:
                st.session_state['selected_odds'].remove((domaci, gosti, col, kvota))

for file_path in csv_files:
    file_name = os.path.basename(file_path)  
    match = re.search(r'_(\d+(?:\.\d+)?)\.csv$', file_name)
    procenat = float(match.group(1)) if match else None
    df = pd.read_csv(file_path)
    df['vreme'] = pd.to_datetime(df['vreme']) + timedelta(hours=1)

    with st.expander(f"⚽ {df.iloc[0]['domaci']} vs {df.iloc[0]['gosti']}  —  🕒 {df.iloc[0]['vreme'] + timedelta(hours=1)}  —  {procenat}%"):
        prikazi_utakmicu(df, procenat)

st.write("---")
st.header("🧮 Arbitražni kalkulator")

# Prikaži trenutno izabrane kvote
st.write("Izabrane kvote (klikom u listi utakmica):")
for item in st.session_state['selected_odds']:
    st.write(f"{item[0]} vs {item[1]} — Tip: {item[2]} — Kvota: {item[3]}")

# Ako je izabrano 2 ili 3 kvote, omogući izračunavanje
if 2 <= len(st.session_state['selected_odds']) <= 3:
    ulog = st.number_input("Ukupan ulog", min_value=100, value=1000, step=100)
    tolerancija = st.number_input("Tolerancija (razlika)", min_value=0, value=1000, step=100)

    if st.button("📊 Izračunaj arbitražu"):
        kvote = tuple(od[3] for od in st.session_state['selected_odds'])
        # pozovi arbitražni kalkulator za 2 ili 3 kvote
        if len(kvote) == 3:
            uloge, profit, roi = arbitrazni_kalkulator_3(kvote, ulog, tolerancija)
            st.success(f"✅ PROFIT: {profit:.2f} €  |  ROI: {roi:.2f}%")
            st.write(f"Ulog 1: **{uloge[0]:.2f} €**")
            st.write(f"Ulog 2: **{uloge[1]:.2f} €**")
            st.write(f"Ulog 3: **{uloge[2]:.2f} €**")
        elif len(kvote) == 2:
            # Ovde možeš implementirati funkciju za 2 kvote, npr. arbitrazni_kalkulator_2
            st.warning("Kalkulator za 2 kvote još nije implementiran.")
else:
    st.info("Izaberi tačno 2 ili 3 kvote za arbitražni kalkulator.")


