from Keys import *
from binance.spot import Spot as Client
import pandas as pd
import talib
import  pandas_ta as ta
from Fonksiyonlar import *
from binance.futures import Futures
from Telegram import *


spotClient = Client(apiKey,secretKey)

#İstenilen coinin ortalama fiyatını getirir
def avgPrice(coinName: str):
    coinAvg = spotClient.avg_price(symbol=str(coinName))
    return coinAvg["price"]

#borsa verileri
def exchangeInfo(coinName: str = None):
    exchange = spotClient.exchange_info(symbol=str(coinName))
    return exchange

#mum verileri
def klineData(coinName: str, period: str, limit: int = None):
    mum = spotClient.klines(symbol=str(coinName), interval=str(period), limit=limit)
    return mum

#24 saatlik değişimin verisi
def ticker24h(coinName: str):
    ticker = spotClient.ticker_24hr(symbol=str(coinName))
    return ticker

#coin fiyatını getirir
def price(coinName: str):
    return spotClient.ticker_price(symbol=str(coinName))["price"]

#timestamp
def serverTime():
    return spotClient.time()["serverTime"]

#emir defteri
def book(coinName: str, limit: int):
   return spotClient.depth(symbol=str(coinName), limit=limit)


def getAllSymbols():
    response = spotClient.exchange_info()
    return list(map(lambda symbol: symbol["symbol"],response["symbols"]))


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
    kline = klineData(coinName,period,limit)
    converted = pd.DataFrame(kline, columns=["open-time", "open", "high", "low", "close", "volume", "close-time", "qav", "not", "tbbav", "tbqav", "ignore"], dtype=float)
    return converted

dataBtc = symbolsData("BTCUSDT","4h",500)
rsi = talib.RSI(dataBtc["close"],14)

def scanner(coinList):
    result = []
    while True:
        try:
            for coin in coinList:
                data = symbolsData(coin, "15m", 500)
                close = data["close"]
                low = data["low"]
                high = data["high"]
                volume = data["volume"]
                if colorHeikinAshi(data) is True and crossOverMacd_CCI(close,low,high) is True and volumeUp(volume) is True and ema20(close) is True:
                    result.append(coin)
                    print(f"{coin}' paritesinde PUMP ALERT")
                    telegramBotSendText(f"{coin}' paritesinde PUMP ALERT",Keys.telegramId)

                """elif colorHeikinAshi(data) is False and macdCrossover(close) is False:
                    result.append(coin)
                    print(f"{coin}' paritesinde aşağı yönlü hareketlenme mevcut")"""
        except:
            pass
        print("HEPSİ TARANDI ŞİMDİ BAŞTAN TARAYACAK")
        telegramBotSendText("HEPSİ TARANDI ŞİMDİ BAŞTAN TARAYACAK",Keys.telegramId)

scanner(usdtList)