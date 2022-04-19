import pandas as pd
import pandas_ta as ta
import numpy as np
from pandas_ta import df


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
    if t3_last > t3_previous: #and t3_previous < t3_prev_previous:
        return True

    # yeşilden kırmızıya dönüyor
    elif t3_last < t3_previous: #and t3_previous > t3_prev_previous:
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
        return str(print("Önündeki ilk direnç = ", a[0]))
    else:
        return str(print("Coinin önü açık"))

def destekVarMi(a: list):
    if a:
        return str(print("Destek Noktaları = ", a))
    else:
        return str(print("Coinin Fibonacci Desteği Kırılmış"))


def ott(data, lentgh=2, percent=1.4, mav='VAR'):
    """Availaeble MA's:
    dema, ema, fwma, hma, linreg, midpoint, pwma, rma,
    sinwma, sma, swma, t3, tema, trima, vidya, wma, zlma"""

    def var():
        alpha = 2 / (lentgh + 1)
        data['ud1'] = np.where(data['close'] > data['close'].shift(1), (data['close'] - data['close'].shift()), 0)
        data['dd1'] = np.where(data['close'] < data['close'].shift(1), (data['close'].shift() - data['close']), 0)
        data['UD'] = data['ud1'].rolling(9).sum()
        data['DD'] = data['dd1'].rolling(9).sum()
        data['CMO'] = ((data['UD'] - data['DD']) / (data['UD'] + data['DD'])).fillna(0).abs()

        data['Var'] = 0.0
        for i in range(lentgh, len(data)):
            data['Var'].iat[i] = (alpha * data['CMO'].iat[i] * data['close'].iat[i]) + (
                    1 - alpha * data['CMO'].iat[i]) * \
                                 data['Var'].iat[
                                     i - 1]
        return data['Var']

    def getMA(src, length):
        if mav == 'VAR':
            return var()
        else:
            return ta.ma(mav, src, length=length).fillna(value=0)

    data['MAvg'] = getMA(data['close'], lentgh)
    data['fark'] = data['MAvg'] * percent * 0.01
    data['newlongstop'] = data['MAvg'] - data['fark']
    data['newshortstop'] = data['MAvg'] + data['fark']
    data['longstop'] = 0.0
    data['shortstop'] = 0.0

    i = 0
    while i < len(data):
        def maxlongstop():
            data.loc[(data['newlongstop'] > data['longstop'].shift(1)), 'longstop'] = data['newlongstop']
            data.loc[(data['longstop'].shift(1) > data['newlongstop']), 'longstop'] = data['longstop'].shift(1)

            return data['longstop']

        def minshortstop():
            data.loc[(data['newshortstop'] < data['shortstop'].shift(1)), 'shortstop'] = data['newshortstop']
            data.loc[(data['shortstop'].shift(1) < data['newshortstop']), 'shortstop'] = data['shortstop'].shift(1)

            return data['shortstop']

        data['longstop'] = np.where((data['MAvg'] > data['longstop'].shift(1)), maxlongstop(), data['newlongstop'])

        data['shortstop'] = np.where((data['MAvg'] < data['shortstop'].shift(1)), minshortstop(),
                                     data['newshortstop'])
        i += 1

    # get xover

    data['xlongstop'] = np.where(
        (
                (data['MAvg'].shift(1) > data['longstop'].shift(1)) &
                (data['MAvg'] < data['longstop'].shift(1))
        ), 1, 0)

    data['xshortstop'] = np.where(
        ((data['MAvg'].shift(1) < data['shortstop'].shift(1)) & (data['MAvg'] > data['shortstop'].shift(1))), 1, 0)

    data['trend'] = 0
    data['dir'] = 0

    i = 0
    while i < len(data):
        data['trend'] = np.where((data['xshortstop'] == 1), 1,
                                 (np.where((data['xlongstop'] == 1), -1, data['trend'].shift(1))))

        data['dir'] = np.where((data['xshortstop'] == 1), 1,
                               (np.where((data['xlongstop'] == 1), -1, data['dir'].shift(1).fillna(1))))

        i += 1

    data['MT'] = np.where(data['dir'] == 1, data['longstop'], data['shortstop'])
    data['OTT'] = np.where(data['MAvg'] > data['MT'], (data['MT'] * (200 + percent) / 200),
                           (data['MT'] * (200 - percent) / 200))
    data['OTT'] = data['OTT'].shift(2)
    ott = pd.DataFrame(data['OTT'])
    ott['MAvg'] = data['MAvg']
    return ott

def KDJ(close,high,low, k_,m1,m2):
    # en yüksek
    df['n_high'] = high.rolling(k_).max()
    # en düşük
    df['n_low'] = low.rolling(k_).min()
    RSV = (close - df['n_low'].astype(float)) / (df['n_high'].astype(float) - df['n_low'].astype(float)) * 100
    K = ta.ema(RSV, (m1*2-1));  D = ta.ema(K,(m2*2-1));  J=K*3-D*2
    if J[len(J)-1] > K[len(K)-1] > D[len(D)-1] :
        return True
    else:
        return False

def rsiControl(close):
    rsi6 = ta.rsi(close, 6)
    rsi14 = ta.rsi(close, 14)

    if rsi6[len(rsi6)-1] > rsi14[len(rsi14)-1]:
        return True
    elif rsi6[len(rsi6)-1] < rsi14[len(rsi14)-1]:
        return False