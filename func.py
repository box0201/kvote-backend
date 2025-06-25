def highlight_max_except_id(df):
    def highlight_max(s):
        is_max = s == s.max()
        return ['background-color: lightgreen' if v else '' for v in is_max]

    styler = df.style.apply(
        lambda col: highlight_max(col) if col.name != 'ID' else ['' for _ in col],
        axis=0
    )
    
    # Formatiraj samo float kolone sa dve decimale
    float_cols = df.select_dtypes(include=['float', 'float64']).columns
    if len(float_cols) > 0:
        styler = styler.format({col: "{:.2f}" for col in float_cols})

    return styler
