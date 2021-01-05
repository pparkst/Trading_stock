from trading import PersonalData
from datetime import datetime

slack = PersonalData.slack
# Send a message to #general channel
slack.chat.post_message('#to-break-even', 'Hello fellow slackers!')

def postMessage(message):
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    # 로컬에서만 파이썬 셀 출력
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)

    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    slack.chat.post_message('#to-break-even', strbuf)
