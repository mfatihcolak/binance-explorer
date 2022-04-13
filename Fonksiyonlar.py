import pandas as pd
import pandas_ta as ta

def crossover(a : list, b : list):
    kisa = a[len(a) - 2]
    simdikiKisa = a[len(a) - 1]

    uzun = b[len(b) - 2]
    simdikiUzun = b[len(b) - 1]

    if kisa < uzun and simdikiKisa > simdikiUzun:
        return True
    else:
        return False

def crossbelow(a : list, b : list):
    kisa = a[len(a) - 2]
    simdikiKisa = a[len(a) - 1]

    uzun = b[len(b) - 2]
    simdikiUzun = b[len(b) - 1]

    if kisa > uzun and simdikiKisa < simdikiUzun:
        return True
    else:
        return False

def heikinAshi(df):
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['open', 'high', 'low', 'close'])

    heikin_ashi_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4

    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i - 1, 0] + heikin_ashi_df.iat[i - 1, 3]) / 2

    heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['high']).max(axis=1)

    heikin_ashi_df['low'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['low']).min(axis=1)

    return heikin_ashi_df

def emaCross(close):
    emaSlow = ta.ema(close, 22)
    emaFast = ta.ema(close, 5)
    if crossover(emaFast, emaSlow) is True:
        return True
    elif crossbelow(emaFast, emaSlow) is True:
        return False

def crossOverMacd_CCI(close,low,high):
    cci = ta.cci(close=close, high=high, low=low,length=14)
    fastLength = 12
    slowLength = 26
    signalLength = 9
    macd, macdSignal, macdHist = ta.macd(close, fastperiod=fastLength , slowperiod=slowLength , signalperiod=signalLength)
    #fastMA = talib.EMA(close, fastLength)
    #slowMA = talib.EMA(close, slowLength)
    #macd = fastMA - slowMA
    if crossover(cci,macd) is True:
        return True
    elif crossbelow(cci,macd) is True:
        return False

def colorHeikinAshi(data):
    heikin = heikinAshi(data)
    haClose = heikin["close"]
    haOpen = heikin["open"]
    if haClose[len(haClose) -1] > haOpen[len(haOpen) -1] and haClose[len(haClose) -2] <= haOpen[len(haOpen) -2]:
        return True #yeşile dönüş
    elif  haClose[len(haClose) -1] <= haOpen[len(haOpen) -1] and haClose[len(haClose) -2] > haOpen[len(haOpen) -2]:
        return False #kırmızıya dönüş

def macdCrossover(close):
    fastLength = 12
    slowLength = 26
    signalLength = 9
    fastMA = ta.ema(close, fastLength)
    slowMA = ta.ema(close, slowLength)
    macd = fastMA - slowMA
    signal = ta.sma(macd, signalLength)
    if crossover(macd, signal) is True:
        return True
    elif crossbelow(macd, signal) is True:
        return False

def volumeUp(vol):
    prevVolume = vol[len(vol)-2]
    nowVolume = vol[len(vol)-1]

    if nowVolume > prevVolume * 1.6:
        return True
    else:
        return False

def stochRsi(close):
    dataStoch = ta.stochrsi(close)
    stochK = dataStoch["STOCHRSIk_14_14_3_3"]
    stochD = dataStoch["STOCHRSId_14_14_3_3"]
    if crossover(stochK, stochD) is True:
        return True
    elif crossbelow(stochK, stochD) is True:
        return False

def myFibonacci(high,low):
    maxPrice = high.max()
    minPrice = low.min()
    difference = maxPrice - minPrice

    levelOne = maxPrice - difference * 1
    levelTwo = maxPrice - difference * 0.786
    levelThree = maxPrice - difference * 0.618
    levelFour = maxPrice - difference * 0.5
    levelFive = maxPrice - difference * 0.382
    levelSix = maxPrice - difference * 0.236
    levelSeven = maxPrice - difference * 0
    return levelOne, levelTwo, levelThree, levelFour, levelFive, levelSix, levelSeven

def T3TillsonIndicatorHesaplama(close_array, high_array, low_array, volume_factor=0.7, t3Length=8):
    ema_first_input = (high_array + low_array + 2 * close_array) / 4

    e1 = ta.ema(ema_first_input, t3Length)
    e2 = ta.ema(e1, t3Length)
    e3 = ta.ema(e2, t3Length)
    e4 = ta.ema(e3, t3Length)
    e5 = ta.ema(e4, t3Length)
    e6 = ta.ema(e5, t3Length)

    c1 = -1 * volume_factor * volume_factor * volume_factor
    c2 = 3 * volume_factor * volume_factor + 3 * volume_factor * volume_factor * volume_factor
    c3 = -6 * volume_factor * volume_factor - 3 * volume_factor - 3 * volume_factor * volume_factor * volume_factor
    c4 = 1 + 3 * volume_factor + volume_factor * volume_factor * volume_factor + 3 * volume_factor * volume_factor
    T3 = c1 * e6 + c2 * e5 + c3 * e4 + c4 * e3

    return T3
def T3TillsonSinyal(tillsont3):
    t3_last = tillsont3[len(tillsont3)-1]
    t3_previous = tillsont3[len(tillsont3)-2]
    t3_prev_previous = tillsont3[len(tillsont3)-3]

    # kırmızıdan yeşile dönüyor
    if t3_last > t3_previous and t3_previous < t3_prev_previous:
        return True

    # yeşilden kırmızıya dönüyor
    elif t3_last < t3_previous and t3_previous > t3_prev_previous:
        return False

def ema20(close):
    ema = ta.ema(close, 22)
    anlikFiyat = close[len(close)-1]
    anlikEMA = ema[len(ema)-1]
    if anlikFiyat > anlikEMA:
        return True
    elif anlikFiyat < anlikEMA:
        return False
    else:
        return None

def direncVarMi(a : list):
    if a:
        return print("Önündeki ilk direnç = ", a[0])
    else:
        return print("Coinin önü açık")

def destekVarMi(a: list):
    if a:
        return print("Destek Noktaları = ", a)
    else:
        return print("Coinin Fibonacci Desteği Kırılmış")