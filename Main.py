import time
from binance.spot import Spot as Client
import Keys
from Fonksiyonlar import *
from Keys import *
from Telegram import telegramBotSendText as telebot

spotClient = Client(apiKey, secretKey)


# İstenilen coinin ortalama fiyatını getirir
def avgPrice(coinName: str):
    coinAvg = spotClient.avg_price(symbol=str(coinName))
    return coinAvg["price"]


# borsa verileri
def exchangeInfo(coinName: str = None):
    exchange = spotClient.exchange_info(symbol=str(coinName))
    return exchange


# mum verileri
def klineData(coinName: str, period: str, limit: int = None):
    mum = spotClient.klines(symbol=str(coinName), interval=str(period), limit=limit)
    return mum


# 24 saatlik değişimin verisi
def ticker24h(coinName: str):
    ticker = spotClient.ticker_24hr(symbol=str(coinName))
    return ticker


# coin fiyatını getirir
def price(coinName: str):
    return spotClient.ticker_price(symbol=str(coinName))["price"]

# timestamp
def serverTime():
    return spotClient.time()["serverTime"]


# emir defteri
def book(coinName: str, limit: int):
    return spotClient.depth(symbol=str(coinName), limit=limit)


def getAllSymbols():
    response = spotClient.exchange_info()
    return list(map(lambda symbol: symbol["symbol"], response["symbols"]))

def lotSize(coinName: str):
    return exchangeInfo(coinName)["symbols"][0]["filters"][2]["minQty"]

def base(coinName: str):
    return exchangeInfo(coinName)["symbols"][0]["baseAsset"]

def step(coinName: str):
    basamak = 0
    for i in lotSize(coinName):
        if i == str(0):
            basamak +=1
        elif i == str(1):
            break
    return basamak

usdtList = []
btcList = []
ethList = []
for coin in getAllSymbols():
    if "USDT" in coin and "UP" not in coin and "DOWN" not in coin and "ERDUSDT" not in coin and "BCCUSDT" not in coin: #and coin.startswith("USDT", 0,2) is True not in coin:
        usdtList.append(coin)
        for coin in usdtList:
            result = coin.startswith("USDT") or coin.startswith("BUSD") or coin.startswith("EUR") or coin.startswith("TUSD")
            if result is True:
                usdtList.remove(coin)
    elif "BTC" in coin:
        btcList.append(coin)
    elif "ETH" in coin:
        ethList.append(coin)

def symbolsData(coinName: str, period: str, limit: int):
    kline = klineData(coinName, period, limit)
    converted = pd.DataFrame(kline,
                             columns=["open-time", "open", "high", "low", "close", "volume", "close-time", "qav", "not",
                                      "tbbav", "tbqav", "ignore"], dtype=float)
    return converted

def dailyVolume(coinName : str):
    volumeDaily = float(ticker24h(coinName)["quoteVolume"])
    if volumeDaily > 2000000:
        return True
    else:
        return False

def scanner(coinList):
    result = []
    while True:
        try:
            for coin in coinList:
                data = symbolsData(coin, "4h", 500)
                close = data["close"]
                low = data["low"]
                high = data["high"]
                volume = data["volume"]
                ott(data)
                if fisherTransformStrategy(high, low) is True and volumeUp(volume) is True and dailyVolume(coin) is True \
                        and strategyIFTORSI(close) is True:
                    result.append(coin)
                    for i in result:
                        direnc = []
                        destek = []
                        data = symbolsData(i, "1d", 310)
                        high = data["high"]
                        low = data["low"]
                        close = data["close"]
                        anlikFiyat = close[len(close) - 1]
                        for i in direncNoktalari(data):
                            if i > anlikFiyat:
                                direnc.append(i)
                        for i in destekNoktalari(data):
                            if i < anlikFiyat:
                                destek.append(i)
                        roundDestek = [round(x, 3) for x in destek]
                        telebot(f"🚀 {coin} paritesinde yükseliş dalgası tespiti!!\n₿ Anlık Fiyat = {anlikFiyat}\n"
                                f"🟥 Önündeki ilk direnç = {round(direnc[0],3)}\n"
                                f"🟩 Destek Noktaları  = {roundDestek}", Keys.telegramGroupId)
                        destek.clear()
                        direnc.clear()
                        result.clear()
                        break
        except:
            pass
        print("HEPSİ TARANDI ŞİMDİ BAŞTAN TARAYACAK")
        telebot("---- Hepsi Tarandı ----", Keys.telegramGroupId)
        time.sleep(300)
scanner(usdtList)
