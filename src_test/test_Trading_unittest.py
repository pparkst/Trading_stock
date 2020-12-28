import unittest
import sys
import os
import ctypes
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src.util import common
from src.trading import trading_object
import win32com.client

def ppark():
    print("TEST")

class Test(unittest.TestCase):
    global Colors
    Colors = common.Colors()
    """
    Test
    """
    def test_connection(self):
        common.printlog("Creon Plus Connection test")
        objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        bConnect = objCpCybos.IsConnect
        bConnect = 1
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")            
            exit()
        else:
            print(Colors.GREEN + "정상 연결")
        self.assertTrue(bConnect != 0)
    """
    Test
    """
    def test_creon_system(self):
        """크레온 플러스 시스템 연결 상태를 점검한다."""
        common.printlog("Creon Plus System Connection test")

        # 관리자 권한으로 프로세스 실행 여부
        admin = ctypes.windll.shell32.IsUserAnAdmin()
        self.assertTrue(admin, 'check_creon_system() : admin user -> FAILED')

        # 연결 여부 체크
        IsConnect = trading_object.cpStatus.IsConnect
        self.assertTrue(IsConnect != 0, 'check_creon_system() : connect to server -> FAILED')
        
        # 주문 관련 초기화 - 계좌 관련 코드가 있을 때만 사용
        InitTrade = trading_object.cpTradeUtil.TradeInit(0)
        self.assertTrue(InitTrade == 0, 'check_creon_system() : init trade -> FAILED')
        
if __name__ == '__main__':  
    unittest.main()