import win32com.client
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))))
from src_test import test_Trading_unittest as ptest
from src_test import slackTest as slackTest

class ExchangeStock:
    def getExchangeStockList(self):
        # 종목코드 리스트 구하기
        objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        codeList = objCpCodeMgr.GetStockListByMarket(1) #거래소
        codeList2 = objCpCodeMgr.GetStockListByMarket(2) #코스닥
 
 
        print("거래소 종목코드", len(codeList))
        for i, code in enumerate(codeList):
            secondCode = objCpCodeMgr.GetStockSectionKind(code)
            name = objCpCodeMgr.CodeToName(code)
            stdPrice = objCpCodeMgr.GetStockStdPrice(code)
            print(i, code, secondCode, stdPrice, name)
        
        print("코스닥 종목코드", len(codeList2))
        for i, code in enumerate(codeList2):
            secondCode = objCpCodeMgr.GetStockSectionKind(code)
            name = objCpCodeMgr.CodeToName(code)
            stdPrice = objCpCodeMgr.GetStockStdPrice(code)
            print(i, code, secondCode, stdPrice, name)
 
        print("거래소 + 코스닥 종목코드 ",len(codeList) + len(codeList2))

test = ptest.Test()
test.test_connection()

slackTest = slackTest.slackTest()
slackTest.test_connectionSlack()

# stock = ExchangeStock()
# stock.getExchangeStockList()
