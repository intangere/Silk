#!/usr/bin/env python
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import msgpack
from protocol import *

### Protocol Implementation

def log(msg):
    print('[INFO]: %s' % msg)


users = {}
class Echo(Protocol):

    def __init__(self):
        self.username = None
        self.mapper = {
                       '0' : self.usernamePacket,
                       '4' : self.relayMessage,
                       '5' : self.relayMessage,
                       '6' : self.relayMessage,
                      }

    def dataReceived(self, data):

        pdata = data
        data = msgpack.unpackb(data[:-2], raw=False)

        self.mapper.get(data['code'], self.unknownPacket)(data, pdata)

    def usernamePacket(self, data, pdata):
        if data['u'] not in users.keys():
           self.username = data['u']
           users[self.username] = self
           log('%s connected successfully' % self.username)
        else:
           log('Username %s taken' % data['u'])
           self.transport.write(username_takenp(data['u']))
           self.transport.loseConnection() #send username taken

    def relayMessage(self, data, pdata):
        if data['u'] in users.keys():
           if data['t'] in users.keys():
              users[data['t']].transport.write(pdata)
           else:
              self.transport.write(offlinep(data['t']) + b'\r\n')

    def unknownPacket(self, data):
        print('Received unknown packet with data: %s' % repr(data))

    def connectionLost(self, reason):
        if self.username:
           del users[self.username]
           print('%s disconnected' % self.username)
        else:
           print('Failed connection')

def main():
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(8000, f)
    reactor.run()

if __name__ == '__main__':
    main()

