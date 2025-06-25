def highlight_max_except_id(df):
    # Zaokruži sve numeričke kolone osim 'ID' na 2 decimale
    df_rounded = df.copy()
    for col in df_rounded.columns:
        if col != 'ID' and pd.api.types.is_numeric_dtype(df_rounded[col]):
            df_rounded[col] = df_rounded[col].round(2)
    
    def highlight_max(s):
        is_max = s == s.max()
        return ['background-color: lightgreen' if v else '' for v in is_max]

    # Primeni stil na zaokruženi DataFrame
    return df_rounded.style.apply(
        lambda col: highlight_max(col) if col.name != 'ID' else ['' for _ in col],
        axis=0
    )
