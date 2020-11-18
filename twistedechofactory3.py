#!/usr/bin/python3

from twisted.internet import protocol, reactor

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        print(data.decode('utf-8').strip())
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

if __name__ == '__main__':
    PORT = 8080
    print(f'Listening on port {PORT}')
    reactor.listenTCP(PORT, EchoFactory())
    reactor.run()
