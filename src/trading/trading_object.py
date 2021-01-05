import win32com.client

# 크레온 플러스 공통 OBJECT
class trading_object():
    if __name__ == '__main__':
        cpCodeMgr = win32com.client.Dispatch('CpUtil.CpStockCode')
        cpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
        cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')
        cpStock = win32com.client.Dispatch('DsCbo1.StockMst')
        cpOhlc = win32com.client.Dispatch('CpSysDib.StockChart')
        cpBalance = win32com.client.Dispatch('CpTrade.CpTd6033')
        cpCash = win32com.client.Dispatch('CpTrade.CpTdNew5331A')
        cpOrder = win32com.client.Dispatch('CpTrade.CpTd0311')  

