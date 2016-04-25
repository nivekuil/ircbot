#!/usr/bin/env python3
import os.path, socket
from time import sleep
from ssl import wrap_socket
from random import choice

class IRC:

    def __init__(self):
        self.host = "nivekuil.com"
        self.port = 7000
        self.nick = "bot"
        self.channels = ["#nivekuil", "#ucsd"]
        self.sock = wrap_socket(
            socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        passwdfile = os.path.join(os.path.dirname(__file__), 'ircbotpass.txt')
        self.passwd = open(passwdfile, 'r').read().strip("\n")

    def auth(self):
        self.sock.connect((self.host, 7000))
        self.sock.settimeout(None)
        self.sock.send("PASS {passwd}\n"
                       .format(passwd=self.passwd).encode())
        self.sock.send("NICK {nick}\n"
                       .format(nick=self.nick).encode())
        self.sock.send("USER {nick} {nick} {nick} :{nick}\n"
                       .format(nick=self.nick).encode())

        for c in self.channels:
            self.sock.send(str.encode("JOIN " + c + "\n"))

    def poll(self):
        data = self.sock.recv(2040).decode()

        if data.startswith('PING'):
            print("ping")
            self.sock.send(str.encode("PONG " + data.split()[1] + "\r\n"))

        return data

    def send_msg(self, channel, message):
        self.sock.send("PRIVMSG {channel} {message}\n"
                       .format(channel=channel, message=message).encode())

def main():
    irc = IRC()
    irc.auth()

    while True:

        sleep(0.05)

        try:
            data = irc.poll()
            print(data)
        except: continue

        if "PRIVMSG" in data:
            # Check for the channel name.
            # Bot won't respond to PMs <- maybe intended?
            channel = data.split()[2]
            # User input after the command starts from index 4,
            # so we get the message by joining everything after that together
            message = str.join(" ", data.split()[4:])

            if ':,help' in data:
                irc.send_msg(channel, "https://github.com/nivekuil/ircbot")

            if ':,alive' in data:
                irc.send_msg(channel, "yes")

            if ':,eval' in data:
                irc.send_msg(channel, "no")

            if ':,echo' in data:
                irc.send_msg(channel, message)

            if ':,rray' in data:
                irc.send_msg(channel, "ded")

            if ':,yt' in data:
                from urllib.parse import urlparse, urlencode
                from urllib.request import urlopen
                import re
                query_string = urlencode({'search_query=': message})
                html_content = urlopen(
                    'https://www.youtube.com/results?search_query=' +
                    query_string)
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})',
                                            html_content.read().decode())
                url = 'https://www.youtube.com/watch?v=' + search_results[0]
                print (search_results)
                irc.send_msg(channel, url)

            if ':,kirby' in data:
                left = ['(>', '(>', '<(', '<(',
                        '^(', 'v(']
                right = ['<)', '<)', ')>', ')>',
                         ')^', ')v']
                face = ['^-^', '^-^', '.-.', '._.', '*-*', '^o^',
                        'x.x', 'o.o', '*.*', '^.^', 'v.v', 'o=o',
                        '^v^', '*O*', '^,^', '^0^', '^o^', '-.-',
                ]

                kirby = choice(left) + choice(face) + choice(right)
                irc.send_msg(channel, kirby)

if __name__ == "__main__":
    main()
