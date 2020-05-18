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
    strategy = the_investment.strategies #[:-10] #request.GET['Strategy']
    print("strategy: ", strategy)

    strategiesArray = strategy.split(",")
    print(strategiesArray)

    numberofStrategies = int(len(strategiesArray))


    if numberofStrategies == 1:

        PortfolioCombinedInfo = return_portfolio_combined_info(strategiesArray[0], investAmount)

        return render_template("investment_detail.html", PortfolioCombinedInfo=PortfolioCombinedInfo)


    elif numberofStrategies == 2:

        P1 = return_portfolio_combined_info(strategiesArray[0], investAmount)
        P2 = return_portfolio_combined_info(strategiesArray[1], investAmount)


        PortfolioCombinedInfo = {"strategy1": P1["strategy"], "portfoliovalue1": P1["portfoliovalue"],
                                 "returnedmoney1": P1["returnedmoney"], "time": P1["time"], "stockonename1": P1["stockonename"],
                                 "stockonesymbol1": P1["stockonesymbol"], "stockoneprice1": P1["stockoneprice"],
                                 "stockonesharesbought1": P1["stockonesharesbought"],
                                 "stockonesharestotalvalue1": P1["stockonesharestotalvalue"], "stocktwoname1": P1["stocktwoname"],
                                 "stocktwosymbol1": P1["stocktwosymbol"], "stocktwoprice1": P1["stocktwoprice"],
                                 "stocktwosharesbought1": P1["stocktwosharesbought"],
                                 "stocktwosharestotalvalue1": P1["stocktwosharestotalvalue"], "stockthreename1": P1["stockthreename"],
                                 "stockthreesymbol1": P1["stockthreesymbol"], "stockthreeprice1": P1["stockthreeprice"],
                                 "stockthreesharesbought1": P1["stockthreesharesbought"],
                                 "stockthreesharestotalvalue1": P1["stockthreesharestotalvalue"], "strategy2": P2["strategy"],
                                 "portfoliovalue2": P2["portfoliovalue"], "returnedmoney2": P2["returnedmoney"],
                                 "stockonename2": P2["stockonename"], "stockonesymbol2": P2["stockonesymbol"],
                                 "stockoneprice2": P2["stockoneprice"], "stockonesharesbought2": P2["stockonesharesbought"],
                                 "stockonesharestotalvalue2": P2["stockonesharestotalvalue"], "stocktwoname2": P2["stocktwoname"],
                                 "stocktwosymbol2": P2["stocktwosymbol"], "stocktwoprice2": P2["stocktwoprice"],
                                 "stocktwosharesbought2": P2["stocktwosharesbought"],
                                 "stocktwosharestotalvalue2": P2["stocktwosharestotalvalue"], "stockthreename2": P2["stockthreename"],
                                 "stockthreesymbol2": P2["stockthreesymbol"], "stockthreeprice2": P2["stockthreeprice"],
                                 "stockthreesharesbought2": P2["stockthreesharesbought"],
                                 "stockthreesharestotalvalue2": P2["stockthreesharestotalvalue"],
                                 "histories1":P1["histories"], "histories2":P2["histories"]}

        return render_template("investment_detail_2.html", PortfolioCombinedInfo=PortfolioCombinedInfo)


def stocks_selector_based_on_strategy(strategyName):

    if strategyName == "Ethical Investing":
        return ["AAPL", "ADBE", "NSRGY"]

    elif strategyName == "Index Investing":
        return ["VTI", "IXUS", "ILTB"]

    elif strategyName == "Growth Investing":
        return ["VUG", "SPYG", "IWF"]

    elif strategyName == "Value Investing":
        return ["ALB", "BTI", "CVS"]

    elif strategyName == "Quality Investing":
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

def return_portfolio_combined_info(strategy, investAmount):

    now = datetime.datetime.now()
    currentTime = now.strftime("%Y-%m-%d %H:%M:%S")

    stockSelectionArray = stocks_selector_based_on_strategy(strategy)

    S1Info = return_stock_information(stockSelectionArray[0], investAmount)
    S2Info = return_stock_information(stockSelectionArray[1], investAmount)
    S3Info = return_stock_information(stockSelectionArray[2], investAmount)

    histories = {}
    for stock in [S1Info, S2Info, S3Info]:
        histories[stock[1]] = get_history(stock[1], stock[3])

    total = {}
    for stock in stockSelectionArray:
        for date in histories[stock].keys():
            if date not in total:
                total[date] = 0

            total[date] += histories[stock][date]

    histories['total'] = total

    portfolioValue = round((S1Info[4] + S2Info[4] + S3Info[4]), 2)
    returnedMoney = round((investAmount - portfolioValue), 2)

    PortfolioCombinedInfo = {"strategy": strategy,
                             "portfoliovalue": portfolioValue, "returnedmoney": returnedMoney, "time": currentTime,
                             "stockonename": S1Info[0], "stockonesymbol": S1Info[1], "stockoneprice": S1Info[2],
                             "stockonesharesbought": S1Info[3], "stockonesharestotalvalue": S1Info[4],
                             "stocktwoname": S2Info[0], "stocktwosymbol": S2Info[1], "stocktwoprice": S2Info[2],
                             "stocktwosharesbought": S2Info[3], "stocktwosharestotalvalue": S2Info[4],
                             "stockthreename": S3Info[0], "stockthreesymbol": S3Info[1], "stockthreeprice": S3Info[2],
                             "stockthreesharesbought": S3Info[3], "stockthreesharestotalvalue": S3Info[4],
                             "histories": {"date": histories['total'].keys(),
                                           "data": histories}}

    return PortfolioCombinedInfo

def get_history(stockName, amount):
    financeInfo = yf.Ticker(stockName)
    history = financeInfo.history(period="5d")
    ret = {}
    for date, data in history.iterrows():
        ret[date.strftime('%Y-%m-%d')] = round(float(data['Close']) * amount)
    return ret
