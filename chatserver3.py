#!/usr/bin/python3


from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

import sys

class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.state = "REGISTER"

        self.delimiter = b'\n'

    def connectionMade(self):
        self.sendLine(b"Name?")

    def connectionLost(self, reason):
        if self.name in self.factory.users:
            del self.factory.users[self.name]
            self.broadcastMessage(f"{self.name} has left the channel")

    def lineReceived(self, line):
        if self.state == "REGISTER":
            self.handle_REGISTER(line)
        else:
            self.handle_CHAT(line)

    def handle_REGISTER(self, name):
        name = name.decode('utf-8')
        if name in self.factory.users:
            self.sendLine(b"Name taken, please choose another")
            return
        self.sendLine(f"Welcome {name}".encode('utf-8'))
        self.broadcastMessage(f"{name} has joined the channel")
        self.name = name
        self.factory.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = f'<{self.name}> {message.decode("utf-8")}'
        self.broadcastMessage(message)

    def broadcastMessage(self, message):
        for name, protocol in self.factory.users.items():
            if protocol != self:
                protocol.sendLine(message.encode('utf-8'))

class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)

if __name__ == '__main__':
    PORT = 8000
    print(f'Listening on port {PORT}')
    reactor.listenTCP(PORT, ChatFactory())
    reactor.run()
