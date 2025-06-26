import streamlit as st
import pandas as pd
import re
import os
from glob import glob
from func import highlight_max_except_id, kelly_criterion, margina, arbitrazni_kalkulator_2, arbitrazni_kalkulator_3
from datetime import timedelta

    

USERS = st.secrets["valid_users"]


def safe_float(x):
  try:
    return float(x)
  except:
    return None

st.set_page_config(page_title="Kvote", layout="wide")
st.title('📊 Arb utakmice')

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

with st.sidebar:
    st.title("📈 KELLY")

    k1 = st.text_input("kvota 1", "",)
    k2 = st.text_input("kvota 2", "",)
    k3 = st.text_input("kvota 3 (opciono)", "", )
    k4 = st.text_input("Kladionica kvota", "", )
    k5 = st.text_input("Realna kvota", "", )
    def try_parse_float(x):
        try:
            return float(x)
        except:
            return None
    col1, col2 = st.columns(2)  

    with col1:
        btn_izracunaj = st.button("Margina")
    with col2:
        btn_kelly = st.button("Kelly")
    if btn_izracunaj:

      kvote = []
      for val in [k1, k2, k3]:
          try:
              f = float(val)
              kvote.append(f)
          except:
              pass
      kvote = margina(kvote)
      st.markdown(f"**Kvote bez margine:** {kvote}")

    if  btn_kelly:
      procenat = kelly_criterion(float(k4), float(k5))
      st.markdown(f"** ULOG: **   {procenat}%")

folder_path = "csv"  
csv_files = glob(os.path.join(folder_path, "*.csv"))


for file_path in csv_files:
    file_name = os.path.basename(file_path)  
    match = re.search(r'_(\d+(?:\.\d+)?)\.csv$', file_name)
    procenat = float(match.group(1)) if match else None
    df = pd.read_csv(file_path)
    df['vreme'] = pd.to_datetime(df['vreme']) + timedelta(hours=1)
    df['ID'] = df['ID'].str.replace(r'\d+', '', regex=True)
    df_new = df.drop(columns=['vreme', 'domaci', 'gosti']).reset_index(drop=True)
    df_new = highlight_max_except_id(df_new)  
    title = f" 🔥 {df.iloc[0]['domaci']} vs {df.iloc[0]['gosti']} — 🕒 {df.iloc[0]['vreme']} — {procenat}%"

    with st.expander(title):
        st.dataframe(df_new)

        with st.expander("Arbitražni kalkulator", expanded=False):
            cols = st.columns(3) 

            k1 = cols[0].text_input("Kvota 1", key=f"k1_{file_name}", label_visibility="collapsed")
            k2 = cols[1].text_input("Kvota 2", key=f"k2_{file_name}", label_visibility="collapsed")
            kx = cols[2].text_input("(opciono)", key=f"kx_{file_name}")

            ulog_str = st.text_input("Ukupni ulog", key=f"ulog_{file_name}")
            k1_f = safe_float(k1)
            kx_f = safe_float(kx)
            k2_f = safe_float(k2)
            ulog = safe_float(ulog_str)

            if k1_f and k2_f and ulog and ulog > 0:
                if kx_f:
                    ulozi, profit = arbitrazni_kalkulator_3([k1_f, kx_f, k2_f], ulog)
                    st.markdown(f"**Ulozi:** 1: {ulozi[0]} RSD, X: {ulozi[1]} RSD, 2: {ulozi[2]} RSD")
                    st.markdown(f"**Profit:** {profit} RSD")
                else:
                    ulozi, profit = arbitrazni_kalkulator_2([k1_f, k2_f], ulog)
                    st.markdown(f"**Ulozi:** 1: {ulozi[0]} RSD, 2: {ulozi[1]} RSD")
                    st.markdown(f"**Profit:** {profit} RSD")
