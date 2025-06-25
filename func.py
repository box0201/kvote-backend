def highlight_max_except_id(df):

    def highlight_max(s):
        is_max = s == s.max()
        return [
            'background-color: #228B22; color: white;' if v else '' for v in is_max
        ]

    styler = df.style.apply(
        lambda col: highlight_max(col) if col.name != 'ID' else ['' for _ in col],
        axis=0
    )

    # Formatiraj samo numeričke kolone na 2 decimale
    numeric_cols = df.select_dtypes(include='number').columns
    fmt = {col: "{:.2f}" for col in numeric_cols}

    return styler.format(fmt)


def margina(odds):
    if not odds or any(odd <= 0 for odd in odds):
        return None
    inverse_odds = [1 / odd for odd in odds]
    margin = sum(inverse_odds)
    adjusted_odds = [(1 / (inverse / margin)) for inverse in inverse_odds]
    lista = []
    for i in adjusted_odds:
        lista.append(round(i, 2))
    return lista

def kelly_criterion(kladionica_kvota, realna_kvota):
    verovatnoca = 1 / realna_kvota
    ulog = ((kladionica_kvota * verovatnoca) - 1) / (kladionica_kvota - 1)
    if ulog <= 0:
        return 0

    p = 1
    return round(ulog * 100 * p, 2)
