import pandas as pd

def highlight_max_per_column(df, columns):
    def highlight_max(s):
        is_max = s == s.max()
        return ['background-color: lightgreen' if v else '' for v in is_max]

    return df.style.apply(lambda col: highlight_max(col) if col.name in columns else ['' for _ in col], axis=0)
