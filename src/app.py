from trading.service import Trading as trading
import trading.service.AutoConnection as autoConnection
import slack.postMessage as postMessage
import trading.service.ExchangeStock


class app():
    if __name__ == '__main__':
        print("hi")
        #trading.run()

        # creonStatus = check_creon_system()
        # printlog('check_creon_system() :', creonStatus)  # 크레온 접속 점검

        # if not creonStatus:
        #     Ac.AutoConnectionCreon()