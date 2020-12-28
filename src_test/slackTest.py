import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src.util import common
from slacker import Slacker
from src.trading import trading_object


def ppark():
    print("TEST")

class slackTest(unittest.TestCase):

    def test_connectionSlack(self):
        slack = trading_object.slack
        slack.chat.post_message('#test', 'Hello')
        print(slack.users)
        response = slack.users.list()
        users = response.body['members']
        print(users)
        self.assertTrue(len(users) > 0)

if __name__ == '__main__':  
    unittest.main()



# slack = Slacker('xoxb-1605937844820-1585025166151-y0szvrXCgW6aK94uWrr9lvHk')

# # Send a message to #general channel
# slack.chat.post_message('#test', 'Hello fellow slackers!')