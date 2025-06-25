def highlight_max_except_id(df):
    def highlight_max(s):
        is_max = s == s.max()
        return ['background-color: lightgreen' if v else '' for v in is_max]

    # Primenjuj funkciju samo na kolone osim 'ID'
    return df.style.apply(
      lambda col: highlight_max(col) if col.name != 'ID' else ['' for _ in col],
      axis=0
      ).format("{:.2f}")