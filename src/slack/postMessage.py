from slacker import Slacker
slack = Slacker('xoxb-1605937844820-1585025166151-y0szvrXCgW6aK94uWrr9lvHk')
# Send a message to #general channel
slack.chat.post_message('#test', 'Hello fellow slackers!')
