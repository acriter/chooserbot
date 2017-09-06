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
        command = e.arguments[0].split(' ')[0]
        if command == '!' + cfg.STARTPOLL:
            if len(e.arguments[0]) > 2:
                self.add_poll(e, e.arguments[0].split(' ')[1:])
        elif command == '!' + cfg.VOTE:
            if len(e.arguments[0]) > 1:
                self.add_vote(e, e.arguments[0].split(' ')[1:])
        
        elif e.arguments[0][:1] == '!':
            cmd = command[1:]
            print 'Received command: ' + cmd
            self.do_command(e, cmd)
        return
        
    def add_poll(self, e, args):
        self.poll = p.Poll(args)
        print "poll started"
        
    def add_vote(self, e, args):
        userId = (item for item in e.tags if item["key"] == "user-id").next()["value"]
        
        #TODO require bits for real
        bits = 100
        bitsFound = False
        
        for item in e.tags:
            if 'bits' in item.values():
                bits = int(item['value'])
                bitsFound = True
        
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

    def end_poll(self, e, args):
        self.poll = None
        print "poll ended"

    def do_command(self, e, cmd):
        c = self.connection

        # Poll the API to get current game.
        if cmd == "game":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])

        # Poll the API the get the current status of the stream
        elif cmd == "title":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + (r['status'] or 'offline'))

        # Provide basic information to viewers for specific commands
        elif cmd == "raffle":
            message = "This is an example bot, replace this text with your raffle text."
            c.privmsg(self.channel, message)
        elif cmd == "schedule":
            message = "This is an example bot, replace this text with your schedule text."            
            c.privmsg(self.channel, message)
            
        elif cmd == "scores":
            if self.poll is not None:
                message = ""
                for option in self.poll.optionList:
                    message += (option.validNames[0] + ": " + str(option.totalBits) + "!" + "     ")

                c.privmsg(self.channel, message)

        # The command was not recognized
        else:
            c.privmsg(self.channel, "Did not understand command: " + cmd)

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