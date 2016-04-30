#!/usr/bin/env python3
import os.path, socket
import re
from time import sleep
from ssl import wrap_socket
from random import choice

class IRC:

    def __init__(self):
        self.host = "nivekuil.com"
        self.port = 7000
        self.nick = "rebelbot"
        self.channels = ["#nivekuil", "#ucsd"]
        self.sock = wrap_socket(
            socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        passwdfile = os.path.join(os.path.dirname(__file__), 'ircbotpass.txt')
        self.passwd = open(passwdfile, 'r').read().strip("\n")

    def auth(self):
        self.sock.connect((self.host, self.port))
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
            # Destructure the received data and give each part a name.
            # This will throw an error if data.split() returns less than 4
            # elements, but any message we care about will have more.
            sender, irc_command, channel, command, *message = data.split()

            # Get the nickname of the sender, which is the text before !
            sender_nick = sender.split('!', 1)[0]
            # Format the message into a single string
            message = " ".join(message)

        except: continue

        if "PRIVMSG" == irc_command:

            if ':,alive' == command:
                irc.send_msg(channel, "yes")

            if ':bot-:' == command:
                msg = ": yes, m'lord" if message else ": m'lord?"
                irc.send_msg(channel, sender_nick + msg)

            if ':,name' == command:
                irc.send_msg(channel, "not shitbot")

            if ':,eval' == command:
                irc.send_msg(channel, "no")

            if ':,echo' == command:
                irc.send_msg(channel, message)

            if ':,rray' == command:
                irc.send_msg(channel, "ded")

            if ':,yt' == command:
                from urllib.parse import urlencode
                from urllib.request import urlopen
                query_string = urlencode({'search_query': message})
                html_content = urlopen('https://www.youtube.com/results?' +
                                       query_string)
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})',
                                            html_content.read().decode())
                url = 'https://www.youtube.com/watch?v=' + search_results[0]
                irc.send_msg(channel, url)

            if ':,help' in data or ':,info' in data:
                irc.send_msg(channel, "https://github.com/nivekuil/ircbot")

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

            if ':,8ball' in data:
                responses = [
                    "It is certain",
                    "It is decidedly so",
                    "Without a doubt",
                    "Yes, definitely",
                    "You may rely on it",
                    "As I see it, yes",
                    "Most likely",
                    "Outlook good",
                    "Yes",
                    "Signs point to yes",
                    "Reply hazy try again",
                    "Ask again later",
                    "Better not tell you now",
                    "Cannot predict now",
                    "Concentrate and ask again",
                    "Don't count on it",
                    "My reply is no",
                    "My sources say no",
                    "Outlook not so good",
                    "Very doubtful",
                ]

                irc.send_msg(channel, choice(responses))


if __name__ == "__main__":
    main()
