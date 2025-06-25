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

folder_path = "csv"  
csv_files = glob(os.path.join(folder_path, "*.csv"))

# Prikaz utakmica
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

# CSS za desni "sidebar" panel sa strelicom
st.markdown(
    """
    <style>
    /* Container za arbitrazni kalkulator */
    #right_panel {
        position: fixed;
        top: 100px;
        right: 0;
        width: 320px;
        max-height: 80vh;
        background-color: #f0f2f6;
        border-left: 1px solid #ccc;
        padding: 10px;
        box-shadow: -3px 0 5px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        transform: translateX(0);
        z-index: 9999;
    }
    /* Kad je zatvoren */
    #right_panel.collapsed {
        transform: translateX(300px);
    }
    /* Strelica za otvaranje/zatvaranje */
    #toggle_button {
        position: fixed;
        top: 150px;
        right: 320px;
        background-color: #007bff;
        color: white;
        padding: 5px 10px;
        border-radius: 4px 0 0 4px;
        cursor: pointer;
        z-index: 10000;
        user-select: none;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True
)

# Dodaj div za panel i dugme
st.markdown("""
<div id="right_panel">
    <h3>⚖️ Arbitražni kalkulator</h3>
    <div>
        <label>Izaberi tip kalkulatora:</label><br>
        <input type="radio" id="two_way" name="arb_mode" value="2-way" checked> 2-way (dva ishoda)<br>
        <input type="radio" id="three_way" name="arb_mode" value="3-way"> 3-way (tri ishoda)
    </div>
    <br>
    <div id="inputs_2way">
        Kvota 1: <input type="number" id="k1" min="1.01" value="2.0" step="0.01"><br>
        Kvota 2: <input type="number" id="k2" min="1.01" value="2.0" step="0.01"><br>
        Ukupan ulog (€): <input type="number" id="ulog" min="1" value="100" step="1"><br>
        <button onclick="calculate2()">Izračunaj 2-way</button>
    </div>
    <div id="inputs_3way" style="display:none;">
        Kvota 1: <input type="number" id="k1_3" min="1.01" value="2.0" step="0.01"><br>
        Kvota X: <input type="number" id="kx" min="1.01" value="3.0" step="0.01"><br>
        Kvota 2: <input type="number" id="k2_3" min="1.01" value="2.0" step="0.01"><br>
        Ukupan ulog (€): <input type="number" id="ulog_3" min="1" value="100" step="1"><br>
        <button onclick="calculate3()">Izračunaj 3-way</button>
    </div>
    <br>
    <div id="result"></div>
</div>
<div id="toggle_button">&#9664;</div>

<script>
const panel = document.getElementById('right_panel');
const toggle = document.getElementById('toggle_button');
toggle.onclick = () => {
    if(panel.classList.contains('collapsed')){
        panel.classList.remove('collapsed');
        toggle.innerHTML = '&#9664;';  // strelica levo
    } else {
        panel.classList.add('collapsed');
        toggle.innerHTML = '&#9654;';  // strelica desno
    }
}

document.getElementById('two_way').addEventListener('change', () => {
    document.getElementById('inputs_2way').style.display = 'block';
    document.getElementById('inputs_3way').style.display = 'none';
});
document.getElementById('three_way').addEventListener('change', () => {
    document.getElementById('inputs_2way').style.display = 'none';
    document.getElementById('inputs_3way').style.display = 'block';
});

// Kalkulator se NE MOŽE direktno raditi u Streamlit iz JS, ovo je samo primer UI
// Za pravi izračun koristi Streamlit inpute i Python backend (da javljam ako želiš kako)

</script>
""", unsafe_allow_html=True)


