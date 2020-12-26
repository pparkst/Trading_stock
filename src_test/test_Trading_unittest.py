import win32com.client
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src.util import Color


def ppark():
    print("TEST")

class Test(unittest.TestCase):
    global Colors
    Colors = Color.Colors()
    """
    Test
    """
    # def run(self):
    #     unittest.main()

    def test_connection(self):
        
        objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        bConnect = objCpCybos.IsConnect
        bConnect = 1
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")            
            exit()
        else:
            print(Colors.GREEN + "정상 연결")
        self.assertTrue(bConnect != 0)
        
if __name__ == '__main__':  
    unittest.main()