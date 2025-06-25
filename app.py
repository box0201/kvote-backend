import streamlit as st
import pandas as pd
import re
import os
from glob import glob
from datetime import timedelta

if "selected_odds" not in st.session_state:
    st.session_state["selected_odds"] = []  # Čuvaj tuple (kladionica, tip kvote, vrednost)

def prikazi_utakmicu(df, prefix):
    domaci = df.iloc[0]['domaci']
    gosti = df.iloc[0]['gosti']
    vreme = df.iloc[0]['vreme'] + timedelta(hours=1)
    st.write(f"⚽ **{domaci} vs {gosti}**  —  🕒 {vreme}")

    # Prikaži tabelu kvota sa checkbox-ovima po polju:
    for i, row in df.iterrows():
        kladionica = row['ID']
        cols = df.columns.drop(['ID', 'vreme', 'domaci', 'gosti'])
        cols_data = []
        for col in cols:
            kvota = row[col]
            key = f"{prefix}_{kladionica}_{col}_{i}"
            izabrano = st.checkbox(f"{kladionica} {col} ({kvota})", key=key, value=False)
            if izabrano:
                if (kladionica, col, kvota) not in st.session_state['selected_odds']:
                    st.session_state['selected_odds'].append((kladionica, col, kvota))
            else:
                if (kladionica, col, kvota) in st.session_state['selected_odds']:
                    st.session_state['selected_odds'].remove((kladionica, col, kvota))

st.set_page_config(page_title="Kvote", layout="wide")
st.title("📊 ARB UTAKMICE")

folder_path = "csv"
csv_files = glob(os.path.join(folder_path, "*.csv"))

for file_path in csv_files:
    file_name = os.path.basename(file_path)
    prefix = os.path.splitext(file_name)[0]
    df = pd.read_csv(file_path)
    df['vreme'] = pd.to_datetime(df['vreme'])
    with st.expander(f"{prefix} - {df.iloc[0]['domaci']} vs {df.iloc[0]['gosti']}"):
        prikazi_utakmicu(df, prefix)

# Sidebar sa arbitražnim kalkulatorom
with st.sidebar:
    st.header("🧮 Arbitražni kalkulator")

    if len(st.session_state['selected_odds']) < 2:
        st.info("Izaberi najmanje 2 kvote za kalkulaciju.")
    else:
        # Prikaz izabranih kvota
        st.write("Izabrane kvote:")
        for klad, tip, kv in st.session_state['selected_odds']:
            st.write(f"{klad} - {tip}: {kv}")

        # Unos uloga i tolerancije
        ulog = st.number_input("Ukupan ulog", min_value=100, value=1000, step=100)
        tolerancija = st.number_input("Tolerancija", min_value=0, value=1000, step=100)

        if st.button("Izračunaj arbitražu"):
            # Ovde treba da pozoveš svoju funkciju arbitraznog kalkulatora,
            # proslediš kvote kao tuple od float vrednosti
            try:
                kvote = tuple([kv for _, _, kv in st.session_state['selected_odds']])
                # Pretpostavimo da imaš arbitrazni_kalkulator_3 za tri kvote
                if len(kvote) == 3:
                    uloge, profit, roi = arbitrazni_kalkulator_3(kvote, ulog, tolerancija)
                    st.success(f"Profit: {profit} €, ROI: {roi}%")
                    st.write(f"Ulogovi: {uloge}")
                else:
                    st.warning("Trenutno podržan samo kalkulator za 3 kvote.")
            except Exception as e:
                st.error(f"Greška u kalkulaciji: {e}")

