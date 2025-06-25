def highlight_max_except_id(df):

    def highlight_max(s):
        is_max = s == s.max()
        return ['background-color: lightblue' if v else '' for v in is_max]

    styler = df.style.apply(
        lambda col: highlight_max(col) if col.name != 'ID' else ['' for _ in col],
        axis=0
    )

    # Formatiraj samo numeričke kolone na 2 decimale
    numeric_cols = df.select_dtypes(include='number').columns
    fmt = {col: "{:.2f}" for col in numeric_cols}

    return styler.format(fmt)
