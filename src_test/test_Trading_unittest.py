import win32com.client
import unittest


def ppark():
    print("TEST")

class Test(unittest.TestCase):
    """
    Test
    """
    def run(self):
        unittest.main()

    def test_connection(self):
        objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        bConnect = objCpCybos.IsConnect
        bConnect = 1
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")            
            exit()
        self.assertTrue(bConnect != 0)
        
if __name__ == '__main__':  
    unittest.main()