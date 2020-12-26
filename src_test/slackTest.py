import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src.util import Color
from slacker import Slacker


def ppark():
    print("TEST")

class slackTest(unittest.TestCase):

    def test_connectionSlack(self):
        slack = Slacker('xoxb-1605937844820-1605942367508-YQ9WVDH7pwCpFy2NiekoqdIi')
        slack.chat.post_message('#test', 'Hello fellow slackers!')
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