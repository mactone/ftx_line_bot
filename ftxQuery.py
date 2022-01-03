
#     LINE_API_KEY = '8a8jB8T49TQXkyPIZXtX11wLCYIV4gnpqApstRZ0kIX'
#     API_KEY='IwmD-bL7OYFzSvE1KGivL0ERwaJDxnAzEQ494XaR'
#     API_SECRET='vCq3wFmxT7NdMyGI-MVip_5R4YBTjKjRLxoihB9J'
#     SUBACCOUNT_NAME='LuBao'
#     subaccount = FtxClient(API_KEY,API_SECRET,SUBACCOUNT_NAME)
def getSpotMarginProfit(subaccount, coinlist):
    total = 0
    account = subaccount.get_account()
    balance = subaccount.get_balances()
    for coin in balance:
        total = total + coin['usdValue']
    
    # USD利息支出
    cost = subaccount.get_borrow_history()
    # print(cost)
    if(cost):
        cost = subaccount.get_borrow_history()[0]['cost']
    else:
        cost=0
    print(type(cost))
    
    # 資金費率收入
    payment = 0
    for coin in coinlist:
        funding_payments = subaccount.get_funding_payments(future=coin)
        payment = payment + funding_payments[0]['payment']
    print(type(payment))
    print ('本次收益：' + str(round((-payment-cost),2)) +
    '\n當次年化：' + str(round(((-payment-cost)*24*365/total*100),2)) + '%' +
    '\n帳戶餘額：' + str(round(total,2)) +
    '\n保證金：' + str(round((account['marginFraction']*100),2))+ '%' #lower than 3% will be liquidated
    )

    message='本次收益：' + str(round((-payment-cost),2)) +
    '\n當次年化：' + str(round(((-payment-cost)*24*365/total*100),2)) + '%' +
    '\n帳戶餘額：' + str(round(total,2)) +
    '\n保證金：' + str(round((account['marginFraction']*100),2))+ '%'

    return message