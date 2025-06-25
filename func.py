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



def arbitrazni_kalkulator_2(kvote, ulog, tolerancija=1000):
    kvota_1, kvota_2 = kvote
    najmanja_razlika = float('inf') 
    najbolje_uloge = None 
    for i in range(int(ulog - tolerancija), int(ulog), 100):
        ulog_1 = (i / kvota_1) / ((1 / kvota_1) + (1 / kvota_2))
        ulog_2 = i - ulog_1
        ulog_1 = round(ulog_1 / 100) * 100  
        ulog_2 = round(ulog_2 / 100) * 100  
        profit_1 = ulog_1 * kvota_1 - i
        profit_2 = ulog_2 * kvota_2 - i
        razlika = abs(profit_1 - profit_2)
        if razlika < najmanja_razlika:
            najmanja_razlika = razlika
            najbolje_uloge = (ulog_1, ulog_2)
    i = sum(najbolje_uloge)
    profit_1 = najbolje_uloge[0] * kvota_1 - i
    profit_2 = najbolje_uloge[1] * kvota_2 - i
    profit = (profit_1 + profit_2) / 2 
    return najbolje_uloge, round(profit, 2)

def arbitrazni_kalkulator_3(kvote, ulog, tolerancija=1000):
    kvota_1, kvota_2, kvota_3 = kvote
    najmanja_razlika = float('inf')
    najbolje_uloge = None
    for i in range(int(ulog - tolerancija), int(ulog), 100):
        ulog_1 = (i / kvota_1) / ((1 / kvota_1) + (1 / kvota_2) + (1 / kvota_3))
        ulog_2 = (i / kvota_2) / ((1 / kvota_1) + (1 / kvota_2) + (1 / kvota_3))
        ulog_3 = i - ulog_1 - ulog_2
        ulog_1 = round(ulog_1 / 100) * 100
        ulog_2 = round(ulog_2 / 100) * 100
        ulog_3 = round(ulog_3 / 100) * 100
        profit_1 = ulog_1 * kvota_1 - i
        profit_2 = ulog_2 * kvota_2 - i
        profit_3 = ulog_3 * kvota_3 - i
        razlika = abs(profit_1 - profit_2) + abs(profit_1 - profit_3) + abs(profit_2 - profit_3)
        if razlika < najmanja_razlika:
            najmanja_razlika = razlika
            najbolje_uloge = (ulog_1, ulog_2, ulog_3)
    i = sum(najbolje_uloge)
    profit_1 = najbolje_uloge[0] * kvota_1 - i
    profit_2 = najbolje_uloge[1] * kvota_2 - i
    profit_3 = najbolje_uloge[2] * kvota_3 - i
    profit = (profit_1 + profit_2 + profit_3) / 3
    return najbolje_uloge, round(profit, 2)
