#!/usr/bin/env python3
import os, socket, ssl
import random

class IRC:

    def __init__(self):
        self.host = "nivekuil.com"
        self.port = 7000
        self.nick = "bot"
        self.channels = ["#nivekuil", "#ucsd"]
        self.sock = ssl.wrap_socket(
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

        if "PING" in data:
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

            if ':,hi' in data:
                irc.send_msg(channel, "iloveyou")

            if ':,rray' in data:
                irc.send_msg(channel, "ded")

            if ':,echo' in data:
                irc.send_msg(channel, message)

            if ':,kirby' in data:
                left = ['(>', '(>', '<(', '<(',
                        '^(', 'v(']
                right = ['<)', '<)', ')>', ')>',
                         ')^', ')v']
                face = ['^-^', '^-^', '.-.', '._.', '*-*', '^o^',
                        'x.x', 'o.o', '*.*', '^.^', 'v.v', 'o=o',
                        '^v^', '*O*', '^,^', '^0^', '^o^', '-.-',
                ]

                kirby = random.choice(left) + random.choice(face) + \
                        random.choice(right)
                irc.send_msg(channel, kirby)

            if ':,eval' in data:
                irc.send_msg(channel, "no")

if __name__ == "__main__":
    main()
