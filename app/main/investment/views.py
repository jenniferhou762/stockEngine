# -*- coding:utf-8 -*-
from app import db
from app.models import Permission, Investment
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user
from . import investment
from ..decorators import admin_required, permission_required
import yfinance as yf
import datetime
import math


@investment.route('/')
def index():
    page = request.args.get('page', 1, type=int)

    current_user_id = int(current_user.get_id())
    print(current_user_id)
    the_investments = Investment.query.filter_by(user_id=current_user_id)

    pagination = the_investments.paginate(page, per_page=8)
    result_investments = pagination.items
    return render_template("investment.html", investments=result_investments, pagination=pagination, 
                           title=u"Investments")


@investment.route('/<investment_id>/')
def detail(investment_id):
    the_investment = Investment.query.get_or_404(investment_id)

    investAmount = float(the_investment.amount) #float(request.GET['InvestAmount'])
    strategy = the_investment.strategies[:-10] #request.GET['Strategy']
    print("strategy: ", strategy)

    now = datetime.datetime.now()
    currentTime = now.strftime("%Y-%m-%d %H:%M:%S")

    #returns array of 3 stock names per strategy
    stockSelectionArray = stocks_selector_based_on_strategy(strategy)

    S1Info = return_stock_information(stockSelectionArray[0], investAmount)
    S2Info = return_stock_information(stockSelectionArray[1], investAmount)
    S3Info = return_stock_information(stockSelectionArray[2], investAmount)


    portfolioValue = round((S1Info[4] + S2Info[4] + S3Info[4]), 2)
    returnedMoney = round((investAmount - portfolioValue), 2)

    PortfolioCombinedInfo = {"strategy": (strategy + " Investing"), 
    "portfoliovalue": portfolioValue, "returnedmoney": returnedMoney, "time": currentTime, 
    "stockonename": S1Info[0], "stockonesymbol": S1Info[1], "stockoneprice": S1Info[2], 
    "stockonesharesbought": S1Info[3], "stockonesharestotalvalue": S1Info[4], 
    "stocktwoname": S2Info[0], "stocktwosymbol": S2Info[1], "stocktwoprice": S2Info[2], 
    "stocktwosharesbought": S2Info[3], "stocktwosharestotalvalue": S2Info[4], 
    "stockthreename": S3Info[0], "stockthreesymbol": S3Info[1], "stockthreeprice": S3Info[2], 
    "stockthreesharesbought": S3Info[3], "stockthreesharestotalvalue": S3Info[4]}

    return render_template("investment_detail.html", PortfolioCombinedInfo=PortfolioCombinedInfo)


def stocks_selector_based_on_strategy(strategyName):

    if strategyName == "Ethical":
        return ["AAPL", "ADBE", "NSRGY"]

    elif strategyName == "Index":
        return ["VTI", "IXUS", "ILTB"]

    elif strategyName == "Growth":
        return ["VUG", "SPYG", "IWF"]

    elif strategyName == "Value":
        return ["ALB", "BTI", "CVS"]

    elif strategyName == "Quality":
        return ["MSFT", "PEP", "NKE"]

def return_stock_information(stockName, investAmount):

    financeInfo = yf.Ticker(stockName)

    companyName = financeInfo.info['longName']
    stockSymbol = financeInfo.info['symbol']

    stockPrice = round(financeInfo.info['regularMarketPrice'], 2)

    stockSharesBought = int(math.floor(((investAmount / 3) / stockPrice)))

    stockSharesValue = round((stockPrice * stockSharesBought), 2)

    #example of stockCombinedInfo: [Google, GOOGL, $100, 10 shares bought, $1,000 total value]
    stockCombinedInfo = [companyName, stockSymbol, stockPrice, 
    stockSharesBought, stockSharesValue]

    return stockCombinedInfo


