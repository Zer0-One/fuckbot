import discord
import logging

TRADING_API_URL='https://cloud.iexapis.com/stable/stock/{0}/quote'
TRADING_API_ICON='https://iextrading.com/favicon.ico'

def ticker_embed(symbol):
    ticker = discord.Embed(title=f"{symbol}".upper(), type="rich", color=3029236, url=TRADING_API_URL.format(symbol))
    ticker.set_author(name="IEXTrading")

    return ticker
