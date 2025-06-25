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
st.title("📊ARB UTAKMICE")

st.markdown("""
<style>
div.row-widget.stRadio > div {
    flex-direction: row;
}

div[data-testid="stTextInput"] > div > div > input {
    width: 100% !important;
    min-width: 60px;
}

.css-1adrfps {
    flex-wrap: nowrap !important;  /* spreči prelazak u novi red */
    display: flex !important;
    gap: 10px;
}
</style>
""", unsafe_allow_html=True)

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

    title = f" 💸 {df.iloc[0]['domaci']} vs {df.iloc[0]['gosti']} — 🕒 {df.iloc[0]['vreme']} — {procenat}%"

    with st.expander(title):
        st.dataframe(df_new)

        # Dinamički pronađi kolone sa kvotama
        meta_cols = ['vreme', 'domaci', 'gosti', 'id']
        kvote_cols = [col for col in df_new.columns if col not in meta_cols]

        # Podrazumevane vrednosti iz prvog reda
        default_kvote_values = [str(df_new[col].iloc[0]) for col in kvote_cols]

        cols = st.columns(len(kvote_cols))
        k_inputs = []
        for i, col in enumerate(kvote_cols):
            k = cols[i].text_input(f"{col}", value=default_kvote_values[i], key=f"{col}_{file_name}")
            k_inputs.append(k)

        ulog_str = st.text_input("Ukupni ulog (€)", key=f"ulog_{file_name}")

        def safe_float(x):
            try:
                return float(x)
            except:
                return None

        kvote_float = [safe_float(k) for k in k_inputs]
        ulog = safe_float(ulog_str)

        if ulog and ulog > 0 and all(kvote_float) and len(kvote_float) in [2, 3]:
            if len(kvote_float) == 2:
                ulozi, profit = arbitrazni_kalkulator_2(kvote_float, ulog)
                st.markdown(f"**Ulozi:** {kvote_cols[0]}: {ulozi[0]} €, {kvote_cols[1]}: {ulozi[1]} €")
                st.markdown(f"**Profit:** {profit} €")
            else:
                ulozi, profit = arbitrazni_kalkulator_3(kvote_float, ulog)
                st.markdown(
                    f"**Ulozi:** {kvote_cols[0]}: {ulozi[0]} €, "
                    f"{kvote_cols[1]}: {ulozi[1]} €, "
                    f"{kvote_cols[2]}: {ulozi[2]} €"
                )
                st.markdown(f"**Profit:** {profit} €")
        else:
            st.info("Unesite validne kvote (2 ili 3) i ulog > 0.")