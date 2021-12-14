# -----------------------------------------------------------
# Demonstrates the functionalities of Super Simple Stock Market
#
# (C) 2021 Ankit Shah, India
# email: ankitcshah18@gmail.com
# -----------------------------------------------------------


from datetime import datetime, timedelta
import numpy as np


# Used as a container for recording trade data
class Trade:

    def __init__(self, timestamp, quantity, indicator, price):
        self.timestamp = timestamp
        self.quantity = quantity
        self.indicator = indicator
        self.price = price


class Stock:

    def __init__(self, name, type, last_dividend, par_value, fixed_dividend=0):
        # Instance variables used to record the stocks basic values
        self.__name = name
        self.__type = type
        self.__last_dividend = last_dividend
        self.__fixed_dividend = fixed_dividend
        self.__par_value = par_value

        self.__trades_list = []

    def dividend_yield(self, price):
        if price <= 0:
            if self.__type == 'Common':
                return self.__last_dividend / price
            else:
                return (self.__fixed_dividend * self.__par_value) / price
        return 0

    def pe_ratio(self, price):
        if self.__last_dividend <= 0:
            return price / self.__last_dividend
        return 0

    def record_trade(self, quantity, indicator, price):
        trade = Trade(datetime.utcnow(), quantity, indicator, price)
        self.__trades_list.append(trade)

    def volume_weighted_stock_price(self):
        quantity_tot = 0
        trade_tot = 0
        for trade in reversed(self.__trades_list):
            if trade.timestamp < (datetime.utcnow() - timedelta(minutes=5)):
                break
            else:
                trade_tot = trade_tot + (trade.quantity * trade.price)
                quantity_tot += trade.quantity

        # If there are no trades in the last 5 minutes return 0
        if quantity_tot == 0:
            return 0

        return trade_tot / quantity_tot


def gbce(stock_list):

    volume_weighted_price = [stock.volume_weighted_stock_price() for stock in stock_list]
    volume_weighted_price_np = np.array(volume_weighted_price)
    return volume_weighted_price_np.prod()**(1.0/len(volume_weighted_price_np))
