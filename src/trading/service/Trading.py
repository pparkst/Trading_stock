import os, sys, ctypes
import win32com.client
import pandas as pd
from datetime import datetime
import time, calendar
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import trading.trading_object as tradingObj
from util.common import printlog
from slack.postMessage import postMessage
import trading.service.AutoConnection as Ac

crObj = tradingObj.CreonObject()
bought_list = []
buy_amount = 0

def get_current_price(code):
    """인자로 받은 종목의 현재가, 매수호가, 매도호가를 반환한다."""
    crObj.cpStock.SetInputValue(0, code)  # 종목코드에 대한 가격 정보
    crObj.cpStock.BlockRequest()
    item = {}
    item['cur_price'] = crObj.cpStock.GetHeaderValue(11)   # 현재가
    item['ask'] =  crObj.cpStock.GetHeaderValue(16)        # 매수호가
    item['bid'] =  crObj.cpStock.GetHeaderValue(17)        # 매도호가    
    return item['cur_price'], item['ask'], item['bid']

def get_ohlc(code, qty):
    """인자로 받은 종목의 OHLC 가격 정보를 qty 개수만큼 반환한다."""
    crObj.cpOhlc.SetInputValue(0, code)           # 종목코드
    crObj.cpOhlc.SetInputValue(1, ord('2'))        # 1:기간, 2:개수
    crObj.cpOhlc.SetInputValue(4, qty)             # 요청개수
    crObj.cpOhlc.SetInputValue(5, [0, 2, 3, 4, 5]) # 0:날짜, 2~5:OHLC
    crObj.cpOhlc.SetInputValue(6, ord('D'))        # D:일단위
    crObj.cpOhlc.SetInputValue(9, ord('1'))        # 0:무수정주가, 1:수정주가
    crObj.cpOhlc.BlockRequest()
    count = crObj.cpOhlc.GetHeaderValue(3)   # 3:수신개수
    columns = ['open', 'high', 'low', 'close']
    index = []
    rows = []
    for i in range(count): 
        index.append(crObj.cpOhlc.GetDataValue(0, i)) 
        rows.append([crObj.cpOhlc.GetDataValue(1, i), crObj.cpOhlc.GetDataValue(2, i),
            crObj.cpOhlc.GetDataValue(3, i), crObj.cpOhlc.GetDataValue(4, i)]) 
    df = pd.DataFrame(rows, columns=columns, index=index) 
    return df

def get_stock_balance(code):
    """인자로 받은 종목의 종목명과 수량을 반환한다."""
    crObj.cpTradeUtil.TradeInit()
    acc = crObj.cpTradeUtil.AccountNumber[0]      # 계좌번호
    accFlag = crObj.cpTradeUtil.GoodsList(acc, 1) # -1:전체, 1:주식, 2:선물/옵션
    crObj.cpBalance.SetInputValue(0, acc)         # 계좌번호
    crObj.cpBalance.SetInputValue(1, accFlag[0])  # 상품구분 - 주식 상품 중 첫번째
    crObj.cpBalance.SetInputValue(2, 50)          # 요청 건수(최대 50)
    crObj.cpBalance.BlockRequest()
    if code == 'ALL':
        postMessage('계좌명: ' + str(crObj.cpBalance.GetHeaderValue(0)))
        postMessage('결제잔고수량 : ' + str(crObj.cpBalance.GetHeaderValue(1)))
        postMessage('평가금액: ' + str(crObj.cpBalance.GetHeaderValue(3)))
        postMessage('평가손익: ' + str(crObj.cpBalance.GetHeaderValue(4)))
        postMessage('종목수: ' + str(crObj.cpBalance.GetHeaderValue(7)))
    stocks = []
    for i in range(crObj.cpBalance.GetHeaderValue(7)):
        stock_code = crObj.cpBalance.GetDataValue(12, i)  # 종목코드
        stock_name = crObj.cpBalance.GetDataValue(0, i)   # 종목명
        stock_qty = crObj.cpBalance.GetDataValue(15, i)   # 수량
        if code == 'ALL':
            postMessage(str(i+1) + ' ' + stock_code + '(' + stock_name + ')' 
                + ':' + str(stock_qty))
            stocks.append({'code': stock_code, 'name': stock_name, 
                'qty': stock_qty})
        if stock_code == code:  
            return stock_name, stock_qty
    if code == 'ALL':
        return stocks
    else:
        stock_name = crObj.cpCodeMgr.CodeToName(code)
        return stock_name, 0

def get_current_cash():
    """증거금 100% 주문 가능 금액을 반환한다."""
    crObj.cpTradeUtil.TradeInit()
    acc = crObj.cpTradeUtil.AccountNumber[0]    # 계좌번호
    accFlag = crObj.cpTradeUtil.GoodsList(acc, 1) # -1:전체, 1:주식, 2:선물/옵션
    crObj.cpCash.SetInputValue(0, acc)              # 계좌번호
    crObj.cpCash.SetInputValue(1, accFlag[0])      # 상품구분 - 주식 상품 중 첫번째
    crObj.cpCash.BlockRequest() 
    return crObj.cpCash.GetHeaderValue(9) # 증거금 100% 주문 가능 금액

def get_target_price(code):
    """매수 목표가를 반환한다."""
    try:
        time_now = datetime.now()
        str_today = time_now.strftime('%Y%m%d')
        ohlc = get_ohlc(code, 10)
        if str_today == str(ohlc.iloc[0].name):
            today_open = ohlc.iloc[0].open 
            lastday = ohlc.iloc[1]
        else:
            lastday = ohlc.iloc[0]                                      
            today_open = lastday[3]
        lastday_high = lastday[1]
        lastday_low = lastday[2]
        target_price = today_open + (lastday_high - lastday_low) * 0.5
        return target_price
    except Exception as ex:
        postMessage("`get_target_price() -> exception! " + str(ex) + "`")
        return None
    
def get_movingaverage(code, window):
    """인자로 받은 종목에 대한 이동평균가격을 반환한다."""
    try:
        time_now = datetime.now()
        str_today = time_now.strftime('%Y%m%d')
        ohlc = get_ohlc(code, 20)
        if str_today == str(ohlc.iloc[0].name):
            lastday = ohlc.iloc[1].name
        else:
            lastday = ohlc.iloc[0].name
        closes = ohlc['close'].sort_index()         
        ma = closes.rolling(window=window).mean()
        return ma.loc[lastday]
    except Exception as ex:
        postMessage('get_movingavrg(' + str(window) + ') -> exception! ' + str(ex))
        return None    

def buy_etf(code):
    """인자로 받은 종목을 최유리 지정가 FOK 조건으로 매수한다."""
    try:
        global bought_list      # 함수 내에서 값 변경을 하기 위해 global로 지정
        global buy_amount
        if code in bought_list: # 매수 완료 종목이면 더 이상 안 사도록 함수 종료
            #printlog('code:', code, 'in', bought_list)
            return False
        time_now = datetime.now()
        current_price, ask_price, bid_price = get_current_price(code) 
        target_price = get_target_price(code)    # 매수 목표가
        ma5_price = get_movingaverage(code, 5)   # 5일 이동평균가
        ma10_price = get_movingaverage(code, 10) # 10일 이동평균가
        buy_qty = 0        # 매수할 수량 초기화
        if ask_price > 0:  # 매수호가가 존재하면   
            buy_qty = buy_amount // ask_price  
        stock_name, stock_qty = get_stock_balance(code)  # 종목명과 보유수량 조회
        #printlog('bought_list:', bought_list, 'len(bought_list):',
        #    len(bought_list), 'target_buy_count:', target_buy_count)     
        if current_price > target_price and current_price > ma5_price \
            and current_price > ma10_price:  
            printlog(stock_name + '(' + str(code) + ') ' + str(buy_qty) +
                'EA : ' + str(current_price) + ' meets the buy condition!`')            
            crObj.cpTradeUtil.TradeInit()
            acc = crObj.cpTradeUtil.AccountNumber[0]      # 계좌번호
            accFlag = crObj.cpTradeUtil.GoodsList(acc, 1) # -1:전체,1:주식,2:선물/옵션                
            # 최유리 FOK 매수 주문 설정
            crObj.cpOrder.SetInputValue(0, "2")        # 2: 매수
            crObj.cpOrder.SetInputValue(1, acc)        # 계좌번호
            crObj.cpOrder.SetInputValue(2, accFlag[0]) # 상품구분 - 주식 상품 중 첫번째
            crObj.cpOrder.SetInputValue(3, code)       # 종목코드
            crObj.cpOrder.SetInputValue(4, buy_qty)    # 매수할 수량
            crObj.cpOrder.SetInputValue(7, "2")        # 주문조건 0:기본, 1:IOC, 2:FOK
            crObj.cpOrder.SetInputValue(8, "12")       # 주문호가 1:보통, 3:시장가
                                                 # 5:조건부, 12:최유리, 13:최우선 
            # 매수 주문 요청
            ret = crObj.cpOrder.BlockRequest() 
            printlog('최유리 FoK 매수 ->', stock_name, code, buy_qty, '->', ret)
            if ret == 4:
                remain_time = crObj.cpStatus.LimitRequestRemainTime
                printlog('주의: 연속 주문 제한에 걸림. 대기 시간:', remain_time/1000)
                time.sleep(remain_time/1000) 
                return False
            time.sleep(2)
            printlog('현금주문 가능금액 :', buy_amount)
            stock_name, bought_qty = get_stock_balance(code)
            printlog('get_stock_balance :', stock_name, stock_qty)
            if bought_qty > 0:
                bought_list.append(code)
                postMessage("`buy_etf("+ str(stock_name) + ' : ' + str(code) + 
                    ") -> " + str(bought_qty) + "EA bought!" + "`")
    except Exception as ex:
        printlog("`buy_etf("+ str(code) + ") -> exception! " + str(ex) + "`")

def sell_all():
    """보유한 모든 종목을 최유리 지정가 IOC 조건으로 매도한다."""
    try:
        crObj.cpTradeUtil.TradeInit()
        acc = crObj.cpTradeUtil.AccountNumber[0]       # 계좌번호
        accFlag = crObj.cpTradeUtil.GoodsList(acc, 1)  # -1:전체, 1:주식, 2:선물/옵션   
        while True:    
            stocks = get_stock_balance('ALL') 
            total_qty = 0 
            for s in stocks:
                total_qty += s['qty'] 
            if total_qty == 0:
                return True
            for s in stocks:
                if s['qty'] != 0:                  
                    crObj.cpOrder.SetInputValue(0, "1")         # 1:매도, 2:매수
                    crObj.cpOrder.SetInputValue(1, acc)         # 계좌번호
                    crObj.cpOrder.SetInputValue(2, accFlag[0])  # 주식상품 중 첫번째
                    crObj.cpOrder.SetInputValue(3, s['code'])   # 종목코드
                    crObj.cpOrder.SetInputValue(4, s['qty'])    # 매도수량
                    crObj.cpOrder.SetInputValue(7, "1")   # 조건 0:기본, 1:IOC, 2:FOK
                    crObj.cpOrder.SetInputValue(8, "12")  # 호가 12:최유리, 13:최우선 
                    # 최유리 IOC 매도 주문 요청
                    ret = crObj.cpOrder.BlockRequest()
                    printlog('최유리 IOC 매도', s['code'], s['name'], s['qty'], 
                        '-> cpOrder.BlockRequest() -> returned', ret)
                    if ret == 4:
                        remain_time = crObj.cpStatus.LimitRequestRemainTime
                        printlog('주의: 연속 주문 제한, 대기시간:', remain_time/1000)
                time.sleep(1)
            time.sleep(30)
    except Exception as ex:
        postMessage("sell_all() -> exception! " + str(ex))

def run():
    try:
        global buy_amount
        global bought_list
        symbol_list = ['A305540']
        bought_list = []     # 매수 완료된 종목 리스트
        target_buy_count = 1 # 매수할 종목 수
        buy_percent = 1
        #stocks = get_stock_balance('ALL')      # 보유한 모든 종목 조회
        total_cash = int(get_current_cash())   # 100% 증거금 주문 가능 금액 조회
        buy_amount = total_cash * buy_percent  # 종목별 주문 금액 계산
        printlog('100% 증거금 주문 가능 금액 :', total_cash)
        printlog('종목별 주문 비율 :', buy_percent)
        printlog('종목별 주문 금액 :', buy_amount)
        printlog('시작 시간 :', datetime.now().strftime('%m/%d %H:%M:%S'))
        soldout = False

        while True:
            t_now = datetime.now()
            t_9 = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
            t_start = t_now.replace(hour=9, minute=5, second=0, microsecond=0)
            t_sell = t_now.replace(hour=15, minute=15, second=0, microsecond=0)
            t_exit = t_now.replace(hour=15, minute=20, second=0,microsecond=0)
            today = datetime.today().weekday()
            if today == 5 or today == 6:  # 토요일이나 일요일이면 자동 종료
                printlog('Today is', 'Saturday.' if today == 5 else 'Sunday.')
                break
            if t_9 < t_now < t_start and soldout == False:
                soldout = True
                sell_all()
            if t_start < t_now < t_sell :  # AM 09:05 ~ PM 03:15 : 매수
                for sym in symbol_list:
                    if len(bought_list) < target_buy_count:
                        buy_etf(sym)
                        time.sleep(1)
                if t_now.hour in (9,11,13,15) and t_now.minute == 10 and 0 <= t_now.second <= 5: 
                    get_stock_balance('ALL')
                    time.sleep(5)
            if t_sell < t_now < t_exit:  # PM 03:15 ~ PM 03:20 : 일괄 매도
                if sell_all() == True:
                    postMessage('`sell_all() returned True -> self-sleep!`')
                    break
            if t_exit < t_now:  # PM 03:20 ~ :프로그램 종료
                postMessage('`self-sleep!`')
                after_cash = int(get_current_cash())
                postMessage('` 금일 손익 : ￦ %s 입니다.`' % (format(after_cash - total_cash, ',')))
                postMessage('` 현 증거금 : ￦ %s 입니다.`' % (format(after_cash, ',')))
                break
            time.sleep(3)

    except Exception as ex:
        postMessage('`main -> exception! ' + str(ex) + '`')
        time.sleep(20)