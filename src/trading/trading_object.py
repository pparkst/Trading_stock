import win32com.client

# 크레온 플러스 공통 OBJECT

class CreonObject:
    _instance = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        return cls._instance

    def __init__(self):
        self.cpCodeMgr = win32com.client.Dispatch('CpUtil.CpStockCode')
        self.cpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
        self.cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')
        self.cpStock = win32com.client.Dispatch('DsCbo1.StockMst')
        self.cpOhlc = win32com.client.Dispatch('CpSysDib.StockChart')
        self.cpBalance = win32com.client.Dispatch('CpTrade.CpTd6033')
        self.cpCash = win32com.client.Dispatch('CpTrade.CpTdNew5331A')
        self.cpOrder = win32com.client.Dispatch('CpTrade.CpTd0311')
