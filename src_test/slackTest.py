import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from src.util import common
from slacker import Slacker
from src.trading import PersonalData

class slackTest(unittest.TestCase):

    def test_connectionSlack(self):
        slack = PersonalData.slack
        slack.chat.post_message('#to-break-even', 'Trading App Run !')
        response = slack.users.list()
        users = response.body['members']
        self.assertTrue(len(users) > 0)

if __name__ == '__main__':  
    unittest.main()



# slack = Slacker('xoxb-1605937844820-1585025166151-y0szvrXCgW6aK94uWrr9lvHk')

# # Send a message to #general channel
# slack.chat.post_message('#test', 'Hello fellow slackers!')