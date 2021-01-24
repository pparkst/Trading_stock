from trading.service import Trading
import trading.service.AutoConnection as autoConnection
import slack.postMessage as postMessage
import trading.trading_object as tradingObj
import time
from datetime import datetime
import ctypes
from util.common import printlog
import threading

crObj = tradingObj.CreonObject()

def check_creon_system():
    """크레온 플러스 시스템 연결 상태를 점검한다."""

    # 관리자 권한으로 프로세스 실행 여부
    if not ctypes.windll.shell32.IsUserAnAdmin():
        printlog('check_creon_system() : admin user -> FAILED')
        return False

    # 연결 여부 체크
    if (crObj.cpStatus.IsConnect == 0):
        printlog('check_creon_system() : connect to server -> FAILED')
        return False

    # 주문 관련 초기화 - 계좌 관련 코드가 있을 때만 사용
    if (crObj.cpTradeUtil.TradeInit(0) != 0):
        printlog('check_creon_system() : init trade -> FAILED')
        return False

    return True

def run():
    t_now = datetime.now()
    t_8 = t_now.replace(hour=8, minute=0, second=0, microsecond=0)
    t_830 = t_now.replace(hour=8, minute=30, second=0, microsecond=0)
    t_start = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
    t_sell = t_now.replace(hour=15, minute=20, second=0, microsecond=0)
    today = datetime.today().weekday()

    runTimer = threading.Timer(60, run)
    holdTimer = threading.Timer(60, run)

    if today != 5 and today !=6 and t_8 < t_now < t_830:
        printlog(" Trading App Running Is Successfully ")
        run()

    if today != 5 and today !=6 and t_830 < t_now and crObj.cpStatus.IsConnect == 0:
        autoConnection.AutoConnectionCreon()

        if crObj.cpStatus.IsConnect == 1:
            printlog(" AutoConnection is Successfully ")

        run()

    if today != 5 and today !=6 and t_start < t_now < t_sell:
        printlog(" Trading Creon App Run !")
        creonStatus = check_creon_system()
        printlog('check_creon_system() :', creonStatus)  # 크레온 접속 점검
        
        if creonStatus:
            Trading.run()
            holdTimer.start()
        else:
            run() 
    else:
        runTimer.start()
        
    #월 : 0
    #화 : 1
    #수 : 2
    #목 : 3
    #금 : 4
    #토 : 5
    #일 : 6

run()