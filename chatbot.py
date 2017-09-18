'''
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
'''

import sys
import irc.bot
import requests
import cfg as cfg
import poll as p
import vote as v

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
        self.poll = None

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print 'Connecting to ' + server + ' on port ' + str(port) + '...'
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)
        

    def on_welcome(self, c, e):
        print 'Joining ' + self.channel

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):

        for item in e.tags:
            if 'bits' in item.values():
                bits = item['value']
                print "found bits!"
                print bits
                print e

        command = e.arguments[0].split(' ')[0]
        if command == '!' + cfg.STARTPOLL:
            if len(e.arguments[0]) > 2:
                self.add_poll(e, e.arguments[0].split(' ')[1:])
        elif command == '!' + cfg.VOTE:
            if len(e.arguments[0]) > 1:
                self.add_vote(e, e.arguments[0].split(' ')[1:])
        elif command == '!' + cfg.SETQUESTION:
            question = e.arguments[0].split(' ')[1:]
            self.set_question(e, ' '.join(question))
        
        elif e.arguments[0][:1] == '!':
            cmd = command[1:]
            print 'Received command: ' + cmd
            self.do_command(e, cmd)
        return

    def user_is_mod(self, e):
        for item in e.tags:
            if 'mod' in item.values():
                return bool(item['value'])
        return False 

    def set_question(self, e, question):
        if self.poll is None:
            return;
        self.poll = p.Poll(question);
        
    def add_poll(self, e, args):
        if not self.user_is_mod(e):
            return;
        if self.poll is None:
            return;
        if self.poll.question is None:
            return;
        if self.poll.has_started():
            self.end_poll(e)
        
        self.poll.set_options(args)

        message1 = "Starting poll! Options are: "
        for option in self.poll.optionList:
            message1 += (option.name + " (" + str(option.number) + ")" + ", ")
        message1 = message1[:-2]
        self.connection.privmsg(self.channel, message1)
        self.connection.privmsg(self.channel, "Question: " + self.poll.question)
        self.connection.privmsg(self.channel, "Cast a vote by typing !vote, then a choice, then cheering for bits!")
        self.connection.privmsg(self.channel, "Examples: \"!vote " + self.poll.optionList[0].name + " cheer50\" OR \"!vote 1 cheer5\"")
        print "poll started"
        
    def add_vote(self, e, args):
        userId = (item for item in e.tags if item["key"] == "user-id").next()["value"]
        
        bits = 0
        
        for item in e.tags:
            if 'bits' in item.values():
                bits = int(item['value'])
                break
        
        print args
        
        if self.poll is not None:
            print "got here"
            loop = True
            for word in args:
                print "word: " + word
                for option in self.poll.optionList:
                    for name in option.validNames:
                        print "option: " + name
                        if word == name:
                            print "got here it's a miracle"
                            vote = v.Vote(userId, bits)
                            self.poll.add_vote(option, vote)
                            loop = False
                            break
                    if loop == False:
                        break
                if loop == False:
                    break         

    def end_poll(self, e):
        if not self.user_is_mod(e):
            return;

        if self.poll is not None:
            self.display_scores(e)
            self.connection.privmsg(self.channel, "Ending poll! Winner is " + self.poll.winning_option().name + "!")

        print "poll ended"
        self.poll = None

    def display_scores(self, e):
        c = self.connection
        if self.poll is not None:
                message = ""
                for option in self.poll.optionList:
                    message += (option.name + ": " + str(option.totalBits) + "!" + "     ")

                c.privmsg(self.channel, message)

    def do_command(self, e, cmd):            
        if cmd == cfg.SCORES:
            self.display_scores(e)
        elif cmd == cfg.ENDPOLL:
            self.end_poll(e)
            

def main():
    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <client id> <token> <channel>")
        sys.exit(1)

    username  = sys.argv[1]
    client_id = sys.argv[2]
    token     = sys.argv[3]
    channel   = sys.argv[4]

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()

if __name__ == "__main__":
    main()