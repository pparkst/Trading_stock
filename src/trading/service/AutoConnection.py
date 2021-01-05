from pywinauto import application
import time
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
import PersonalData as pD

def AutoConnectionCreon():
    os.system('taskkill /IM coStarter* /F /T')
    os.system('taskkill /IM CpStart* /F /T')
    os.system('wmic process where "name like \'%coStarter%\'" call terminate')
    os.system('wmic process where "name like \'%CpStart%\'" call terminate')
    time.sleep(5)        

    app = application.Application()
    app.start('C:\CREON\STARTER\coStarter.exe%s/autostart' % pD.accountInfo)
    time.sleep(60)