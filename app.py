import streamlit as st
import pandas as pd
import re
import os
from glob import glob
from func import highlight_max_except_id

st.set_page_config(page_title="Kvote", layout="wide")
st.title("  📊 ARB UTAKMICE  ")

folder_path = "csv"  
csv_files = glob(os.path.join(folder_path, "*.csv"))

for file_path in csv_files:
    file_name = os.path.basename(file_path)  
    match = re.search(r'_(\d+(?:\.\d+)?)\.csv$', file_name)
    procenat = float(match.group(1)) if match else None
    df = pd.read_csv(file_path)
    df_new = df.drop(columns=['vreme', 'domaci', 'gosti']).reset_index(drop=True)
    df_new = highlight_max_except_id(df_new)

    
    title = f"⚽ {df.iloc[0]['domaci']} vs {df.iloc[0]['gosti']}  —  🕒 {df.iloc[0]['vreme']}  —  {procenat}%"
    with st.expander(title):
      st.dataframe(df_new)  

