import streamlit as st
import pandas as pd
import re
import os
from glob import glob

st.set_page_config(page_title="Kvote", layout="wide")
st.title("  📊 ARB UTAKMICE  ")

folder_path = "csv"  # Tvoj folder sa CSV fajlovima
csv_files = glob(os.path.join(folder_path, "*.csv"))

for file_path in csv_files:
    file_name = os.path.basename(file_path)  # npr. 'utakmica_123_47.csv'
    match = re.search(r'_(\d+)\.csv$', file_name)
    procenat = match.group(1) if match else "?" 
    df = pd.read_csv(file_path)
    df_new = df.drop(columns=['vreme', 'domaci', 'gosti']).reset_index(drop=True)
    title = f"⚽ {df.iloc[0]['domaci']} vs {df.iloc[0]['gosti']}  —  🕒 {df.iloc[0]['vreme']}  —  {procenat}"

    with st.expander(title):
        st.dataframe(df_new)
