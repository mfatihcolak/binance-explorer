import time

from binance.spot import Spot as Client

from Fonksiyonlar import *
from Keys import *
from Telegram import *

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


usdtList = []
btcList = []
ethList = []
for coin in getAllSymbols():
    if "USDT" in coin and "UP" not in coin and "DOWN" not in coin:
        usdtList.append(coin)
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


def scanner(coinList):
    result = []
    while True:
        try:
            for coin in coinList:
                time.sleep(10)
                data = symbolsData(coin, "5m", 500)
                close = data["close"]
                low = data["low"]
                high = data["high"]
                volume = data["volume"]
                if macdCrossover(close) is True and \
                        emaCross(close) is True and \
                        volumeUp(volume) is True and stochRsi(close) is True:
                    result.append(coin)
                    print(f"{coin}' paritesinde yükseliş dalgası tespiti!!")
                    telegramBotSendText(f"{coin}' paritesinde yükseliş dalgası tespiti!!", Keys.telegramId)
        except:
            pass
        print("HEPSİ TARANDI ŞİMDİ BAŞTAN TARAYACAK")
        telegramBotSendText("HEPSİ TARANDI ŞİMDİ BAŞTAN TARAYACAK", Keys.telegramId)


scanner(usdtList)
