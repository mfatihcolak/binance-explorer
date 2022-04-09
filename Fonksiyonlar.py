import pandas as pd
import pandas_ta as ta
def crossover(a : list, b : list):
    oncekiKisa = a[len(a) - 3]
    kisa = a[len(a) - 2]
    simdikiKisa = a[len(a) - 1]

    oncekiUzun = b[len(b) - 3]
    uzun = b[len(b) - 2]
    simdikiUzun = b[len(b) - 1]

    if oncekiKisa < oncekiUzun and kisa > uzun and simdikiKisa > simdikiUzun:
        return True
    else:
        return False

def crossbelow(a : list, b : list):
    oncekiKisa = a[len(a) - 3]
    kisa = a[len(a) - 2]
    simdikiKisa = a[len(a) - 1]

    oncekiUzun = b[len(b) - 3]
    uzun = b[len(b) - 2]
    simdikiUzun = b[len(b) - 1]

    if oncekiKisa > oncekiUzun and kisa < uzun and simdikiKisa < simdikiUzun:
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

def ema20(close):
    ema = ta.ema(close, 20)
    if close[len(close)-1] > ema[len(ema)-1]:
        return True
    elif close[len(close)-1] < ema[len(ema)-1]:
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
    fastLength = 8
    slowLength = 16
    signalLength = 11
    fastMA = ta.ema(close, fastLength)
    slowMA = ta.ema(close, slowLength)
    macd = fastMA - slowMA
    signal = ta.sma(macd, signalLength)
    if signal[len(signal) - 2] >= macd[len(macd) - 2] and signal[len(signal)-1] < macd[len(macd)-1]:
        return True
    elif signal[len(signal)-2] <= macd[len(macd)-2] and signal[len(signal)-1] > macd[len(macd)-1]:
        return False

def volumeUp(vol):
    prevVolume = vol[len(vol)-2]
    nowVolume = vol[len(vol)-1]

    if nowVolume > prevVolume * 2:
        return True
    else:
        return False
