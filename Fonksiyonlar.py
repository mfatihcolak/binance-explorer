import math

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
    fastLength = 8
    slowLength = 16
    signalLength = 11
    fastMA = ta.ema(close, fastLength)
    slowMA = ta.ema(close, slowLength)
    macd = fastMA - slowMA
    signal = ta.sma(macd, signalLength)
    if crossover(macd, signal) is True:
        return True
    elif crossbelow(macd, signal) is True:
        return False

def volumeUp(vol):
    prevvvVolume = vol[len(vol)-4]
    prevvVolume = vol[len(vol)-3]
    prevVolume = vol[len(vol)-2]
    nowVolume = vol[len(vol)-1]

    if nowVolume > (prevvvVolume + prevvVolume + prevVolume) / 3 * 1.6:
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

def ottControl(ott):
    ottL = ott["OTT"]
    mavgL = ott["MAvg"]
    if mavgL[len(mavgL)-1] > ottL[len(ottL)-1]:
        return True
    else:
        return False

def cciCrossover(close, high, low):
    cci = ta.cci(high, low, close, 20)
    anlik = cci[len(cci)-1]
    onceki = cci[len(cci)-2]
    if onceki < -100 and anlik > -100:
        return True
    elif onceki > 100 and anlik < 100:
        return False

def stochControl(close, high, low):
    stoch = ta.stoch(high, low, close)
    stochK = stoch["STOCHk_14_3_3"]
    if stochK[499] > 50:
        return True
    elif stochK[499] < 50:
        return False

def highest(series_a, length):
    """
    Returns the highest element in the given series
    :param series_a:
    :param length:
    :return:
    """

    series_a = pd.Series(series_a) if isinstance(series_a, list) else series_a
    newList = pd.Series(dtype=series_a.dtype, index=np.arange(length))
    length = series_a.size if length > series_a.size else length
    for x in range(length):
        newList[x] = series_a.iloc[-1-x]
    return newList.max()

def lowest(series_a, length):
    """
    Returns the lowest element in the given series
    :param series_a:
    :param length:
    :return:
    """

    series_a = pd.Series(series_a) if isinstance(series_a, list) else series_a
    newList = pd.Series(dtype=series_a.dtype, index=np.arange(length))
    length = series_a.size if length > series_a.size else length
    for x in range(length):
        newList[x] = series_a.iloc[-1-x]
    return newList.min()

def fisherTransformStrategy(high, low):
    length = 10
    fishLine = ta.fisher(high, low, length)["FISHERT_10_1"]
    signalLine = ta.fisher(high, low, length)["FISHERTs_10_1"]
    if crossover(fishLine, signalLine) is True:
        return True
    elif crossbelow(fishLine, signalLine) is True:
        return False


def strategyIFTORSI(close):
    rsiLength = 5
    wmaLength = 9
    v1 = 0.1 * (ta.rsi(close, rsiLength) - 50)
    v2 = ta.wma(v1, wmaLength)
    INV = (np.exp(2*v2)-1)/(np.exp(2*v2)+1)

    if INV[len(INV)-1] > -0.50:
        return True
    else:
        return None


def support(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1["low"][i]>df1["low"][i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1["low"][i]<df1["low"][i-1]):
            return 0
    return 1

def resistance(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1["high"][i]<df1["high"][i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1["high"][i]>df1["high"][i-1]):
            return 0
    return 1


def detectResistanceSupport(data):
    global destekler, direncler
    destekler = []
    direncler = []
    n1 = 2
    n2 = 2
    for row in range(3, 300):  # len(df)-n2
        if support(data, row, n1, n2):
            destekler.append((row, data["low"][row]))
        if resistance(data, row, n1, n2):
            direncler.append((row, data["high"][row]))
    return destekler, direncler

def destekNoktalari(data):
    global desteks
    desteks = []
    destek, direnc = detectResistanceSupport(data)
    for i, tuple in enumerate(destek):
        desteks.append(destek[i][1])
    return desteks

def direncNoktalari(data):
    global direncs
    direncs = []
    destek, direnc = detectResistanceSupport(data)
    for i, tuple in enumerate(direnc):
        direncs.append(direnc[i][1])
    return direncs

def btcRSI(close):
    rsi = ta.rsi(close, 14)
    if rsi[len(rsi)-1] < 30:
        return True
    elif rsi[len(rsi)-1] > 70:
        return False

def btcEMA(close):
    ema20 = ta.ema(close, 22)
    anlikFiyat = close[len(close)-1]
    if anlikFiyat > ema20[len(ema20)-1]:
        return True
    elif anlikFiyat < ema20[len(ema20)-1]:
        return False

def cakmaUstadRSI(close):
    rsi = ta.rsi(close, 22)
    ema = ta.ema(close, 66)
    if crossover(rsi, ema) is True:
        return True
    elif crossbelow(rsi, ema) is True:
        return False

def waveTrend(high,low,close):
    n1 = 10
    n2 = 21
    obLevelone = 60
    obLeveltwo = 53
    osLevelone = -60
    osLeveltwo = -53

    ap = ta.hlc3(high=high, low=low, close=close)
    esa = ta.ema(ap, n1)
    d = ta.ema(abs(ap-esa), n1)
    ci = (ap-esa) / (0.015 * d)
    tci = ta.ema(ci, n2)

    wt1 = tci
    wt2 = ta.sma(ci, 4)

    if wt1[len(wt1)-1] < 0:
        return True
    elif wt1[len(wt1)-1] > 0:
        return False




def QQE(_candles):
    # https://www.tradingview.com/script/tJ6vtBBe-QQE/
    # Close = _candles.Close
    Close = _candles["close"]
    Fast = 2.6180
    Slow = 4.2360
    RSI = 14
    SF = 2

    def WiMA(src, length):
        MA_s = [0]
        for i, x in enumerate(src):
            MA_s.append((x + (MA_s[i] * (length - 1))) / length)

        return MA_s

    def crossovers(p1, p2):
        a = []
        for i in range(1, min(len(p1), len(p2))):
            if p1[i] < p2[i] and not p1[i - 1] < p2[i - 1]:
                a.append(True)
            elif p1[i] > p2[i] and not p1[i - 1] > p2[i - 1]:
                a.append(True)
            else:
                a.append(False)
        return a

    RSIndex = ta.ema(ta.rsi(Close, RSI, fillna=0), SF, fillna=0)

    TR = [0]
    for i in range(1, len(Close)):
        TH = RSIndex[i - 1] if RSIndex[i - 1] > RSIndex[i] else RSIndex[i]
        TL = RSIndex[i - 1] if RSIndex[i - 1] < RSIndex[i] else RSIndex[i]
        TR.append(TH - TL)

    AtrRsi = WiMA(TR, 14)
    SmoothedAtrRsi = WiMA(AtrRsi, 14)

    # FastQQE
    DeltaFastAtrRsi = [x * Fast for x in SmoothedAtrRsi]
    newlongband = [x - i for x, i in zip(RSIndex, DeltaFastAtrRsi)]
    longband = [0]
    for i in range(1, len(RSIndex)):
        if RSIndex[i - 1] > longband[i - 1] and RSIndex[i] > longband[i - 1]:
            longband.append(max(longband[i - 1], newlongband[i]))
        else:
            longband.append(newlongband[i])
    newshortband = [x + i for x, i in zip(RSIndex, DeltaFastAtrRsi)]
    shortband = [0]
    for i in range(1, len(RSIndex)):
        if RSIndex[i - 1] < shortband[i - 1] and RSIndex[i] < shortband[i - 1]:
            shortband.append(min(shortband[i - 1], newshortband[i]))
        else:
            shortband.append(newshortband[i])

    trend = [0, 0]
    shortbandCross = crossovers(RSIndex, [0] + shortband)
    longbandCross = crossovers([0] + longband, RSIndex)
    for i in range(1, len(shortbandCross)):
        if shortbandCross[i] == True:
            trend.append(1)
        elif longbandCross[i] == True:
            trend.append(-1)
        else:
            trend.append(trend[i])
    FastAtrRsiTL = [longband[i] if trend[i] == 1 else shortband[i] for i in range(len(trend))]

    # SlowQQE
    DeltaSlowAtrRsi = [x * Slow for x in SmoothedAtrRsi]
    newlongband1 = [x - i for x, i in zip(RSIndex, DeltaSlowAtrRsi)]
    longband1 = [0]
    for i in range(1, len(RSIndex)):
        if RSIndex[i - 1] > longband1[i - 1] and RSIndex[i] > longband1[i - 1]:
            longband1.append(max(longband1[i - 1], newlongband1[i]))
        else:
            longband1.append(newlongband1[i])

    newshortband1 = [x + i for x, i in zip(RSIndex, DeltaSlowAtrRsi)]
    shortband1 = [0]
    for i in range(1, len(RSIndex)):
        if RSIndex[i - 1] < shortband1[i - 1] and RSIndex[i] < shortband1[i - 1]:
            shortband1.append(min(shortband1[i - 1], newshortband1[i]))
        else:
            shortband1.append(newshortband1[i])
    trend1 = [0, 0]
    shortbandCross1 = crossovers(RSIndex, [0] + shortband1)
    longbandCross1 = crossovers([0] + longband1, RSIndex)
    for i in range(1, len(shortbandCross1)):
        if shortbandCross1[i] == True:
            trend1.append(1)
        elif longbandCross1[i] == True:
            trend1.append(-1)
        else:
            trend1.append(trend1[i])
    SlowAtrRsiTL = [longband1[i] if trend1[i] == 1 else shortband1[i] for i in range(len(trend1))]
    return FastAtrRsiTL, SlowAtrRsiTL

#RsiTL = QQE(df)
#Fast = RsiTL[0]
#Slow = RsiTL[1]
#FastAtrRsiTL = RsiTL[0][i-1]
#SlowAtrRsiTL = RsiTL[1][i-1]

