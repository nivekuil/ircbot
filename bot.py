#!/usr/bin/env python3
import socket, ssl, sys, time

class IRC:

    def __init__(self):
        self.host = "nivekuil.com"
        self.port = 7000
        self.nick = "ucsdbot"
        self.passwd = open("ircbotpass.txt", 'r').read().strip("\n")
        self.channels = ["#nivekuil", "#ucsd"]
        self.sock = ssl.wrap_socket(
            socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    def auth(self):
        self.sock.connect((self.host, 7000))
        self.sock.setblocking(False)
        self.sock.send(
            str.encode("PASS {passwd}\n".format(passwd=self.passwd)))
        self.sock.send(
            str.encode("NICK {nick}\n".format(nick=self.nick)))
        self.sock.send(
            str.encode("USER {nick} {nick} {nick} :{nick}\n"
                       .format(nick=self.nick)))

        for c in self.channels:
            self.sock.send(
                str.encode("JOIN " + c + "\n"))

    def poll(self):
        data = self.sock.recv(2040)

        if b"PING" in data:
            irc.send("PONG " + text.split()[1] + "\r\n".encode())

        return data

    def send_msg(self, channel, message):
        self.sock.send(
            str.encode("PRIVMSG {channel} {message}\n"
                       .format(channel=channel, message=message)))

def main():
    irc = IRC()
    irc.auth()

    while True:
        time.sleep(0.05)

        try:
            data = irc.poll()
            print(data)
        except: continue

        if b"PRIVMSG" in data:
            # Check for the channel name.
            for c in irc.channels:
                if c.encode() in data:
                    channel = c
                    break
            else:
                # If no channel name is found (shouldn't happen?) then
                # start again from the top.
                continue

            if b':,hi' in data:
                irc.send_msg(channel, "hi")

if __name__ == "__main__":
    main()
