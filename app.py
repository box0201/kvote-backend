import streamlit as st
import pandas as pd
import os
from glob import glob

st.set_page_config(page_title="Kvote", layout="wide")
st.title("📊 Pregled kvota")

folder_path = "kvote-backend/csv"  # Tvoj folder sa CSV fajlovima
csv_files = glob(os.path.join(folder_path, "*.csv"))

for file in csv_files:
    df = pd.read_csv(file)
    df_new = df.drop(columns=['vreme', 'domaci', 'gosti']).reset_index(drop=True)
    st.markdown(f"## ⚽ {df.iloc[0]['domaci']} vs {df.iloc[0]['gosti']}")
    st.markdown(f"🕒 {df.iloc[0]['vreme']}")
    st.dataframe(df_new)
    st.markdown("---")
